from unittest.mock import patch

import pytest

from dndgame.character import RACE_BONUSES, Character


def test_character_creation_with_valid_race():
    c = Character("Aria", "Elf", base_hp=10)
    assert c.name == "Aria"
    assert c.race == "Elf"
    assert c.level == 1
    assert c.hp == 0  # not rolled yet


def test_character_creation_with_invalid_race_raises():
    with pytest.raises(ValueError):
        Character("Bob", "Orc", base_hp=10)


def test_roll_stats_sets_all_six_stats():
    c = Character("Bob", "Human", base_hp=10)
    with patch("random.randint", return_value=4):
        c.roll_stats()
    assert set(c.stats.keys()) == {"STR", "DEX", "CON", "INT", "WIS", "CHA"}
    assert all(value == 12 for value in c.stats.values())  # 3d6 of all 4s


def test_roll_stats_derives_hp_from_con_modifier():
    c = Character("Bob", "Human", base_hp=10)
    with patch("random.randint", return_value=4):  # CON = 12 -> modifier +1
        c.roll_stats()
    assert c.get_modifier("CON") == 1
    assert c.max_hp == 11
    assert c.hp == c.max_hp


def test_apply_racial_bonus_dwarf_boosts_con_only():
    c = Character("Grom", "Dwarf", base_hp=10)
    with patch("random.randint", return_value=4):
        c.roll_stats()
    con_before = c.stats["CON"]
    other_stats_before = {k: v for k, v in c.stats.items() if k != "CON"}
    c.apply_racial_bonuses()
    assert c.stats["CON"] == con_before + 2
    assert all(c.stats[k] == v for k, v in other_stats_before.items())


def test_apply_racial_bonus_human_boosts_every_stat():
    c = Character("Sam", "Human", base_hp=10)
    with patch("random.randint", return_value=4):
        c.roll_stats()
    before = dict(c.stats)
    c.apply_racial_bonuses()
    assert all(c.stats[stat] == before[stat] + 1 for stat in before)


def test_new_race_can_be_added_without_code_changes():
    """Regression test for the 'hard to add a race' TODO item."""
    assert "Halfling" in RACE_BONUSES
    c = Character("Pip", "Halfling", base_hp=8)
    with patch("random.randint", return_value=3):
        c.roll_stats()
    dex_before, cha_before = c.stats["DEX"], c.stats["CHA"]
    c.apply_racial_bonuses()
    assert c.stats["DEX"] == dex_before + 1
    assert c.stats["CHA"] == cha_before + 1