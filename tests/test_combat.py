from unittest.mock import patch

from dndgame.combat import Combat
from dndgame.entities import Entity


def make_entity(name="Fighter", str_score=14, dex_score=10, hp=10, armor_class=10):
    return Entity(name, {"STR": str_score, "DEX": dex_score}, hp, armor_class)


def test_roll_initiative_ties_go_to_player():
    player = make_entity("Player", dex_score=10)
    enemy = make_entity("Enemy", dex_score=10)
    combat = Combat(player, enemy)
    with patch("random.randint", return_value=10):
        order = combat.roll_initiative()
    assert order == [player, enemy]


def test_attack_hit_deals_damage():
    attacker = make_entity("Attacker", str_score=14)  # +2 modifier
    defender = make_entity("Defender", hp=10, armor_class=10)
    combat = Combat(attacker, defender)
    with patch("random.randint", side_effect=[15, 4]):  # 15+2=17 hits AC10; 4 damage
        damage = combat.attack(attacker, defender)
    assert damage == 4
    assert defender.hp == 6


def test_attack_miss_deals_no_damage():
    attacker = make_entity("Attacker", str_score=8)  # -1 modifier
    defender = make_entity("Defender", hp=10, armor_class=20)
    combat = Combat(attacker, defender)
    with patch("random.randint", return_value=5):  # 5-1=4, misses AC20
        damage = combat.attack(attacker, defender)
    assert damage == 0
    assert defender.hp == 10


def test_run_player_defeats_enemy():
    player = make_entity("Player", str_score=14, hp=20, armor_class=10)
    enemy = make_entity("Enemy", str_score=8, hp=1, armor_class=1)
    combat = Combat(player, enemy)
    with patch("random.randint", side_effect=[10, 10, 15, 6]), patch(
        "builtins.input", return_value="1"
    ):
        result = combat.run()
    assert result is True
    assert enemy.hp == 0


def test_run_player_flees():
    player = make_entity("Player", hp=10)
    enemy = make_entity("Enemy", hp=10)
    combat = Combat(player, enemy)
    with patch("random.randint", return_value=10), patch("builtins.input", return_value="2"):
        result = combat.run()
    assert result is False


def test_run_enemy_can_defeat_player():
    """Regression test: the Goblin must be able to knock the player out."""
    player = make_entity("Player", hp=1, armor_class=1, str_score=8)
    enemy = make_entity("Enemy", hp=20, str_score=14, armor_class=1)
    combat = Combat(player, enemy)
    # init: player 5, enemy 15 -> enemy goes first
    # enemy attack: 15 + 2(STR mod) = 17, hits AC1; damage roll 6
    with patch("random.randint", side_effect=[5, 15, 15, 6]), patch(
        "builtins.input", return_value="1"
    ):
        result = combat.run()
    assert result is False
    assert player.hp == 0
    assert not player.is_alive


def test_run_combat_never_lets_hp_go_negative():
    player = make_entity("Player", hp=3, armor_class=1, str_score=8)
    enemy = make_entity("Enemy", hp=20, str_score=14, armor_class=1)
    combat = Combat(player, enemy)
    with patch("random.randint", side_effect=[5, 15, 15, 20]), patch(
        "builtins.input", return_value="1"
    ):
        combat.run()
    assert player.hp == 0  # not negative, even though 20 damage > 3 HP