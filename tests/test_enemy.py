"""Tests for the Enemy class and its templates."""

import pytest

from dndgame.enemy import Enemy, ENEMY_TEMPLATES


def test_enemy_creation_from_valid_template():
    """A Goblin should be built with the exact stats from its template."""
    goblin = Enemy("Goblin")
    assert goblin.name == "Goblin"
    assert goblin.kind == "Goblin"
    assert goblin.hp == goblin.max_hp
    assert goblin.armor_class == 12
    assert goblin.stats == {"STR": 8, "DEX": 10, "CON": 10}


def test_enemy_creation_with_invalid_kind_raises():
    """Requesting an unknown enemy type should fail loudly, not silently."""
    with pytest.raises(ValueError):
        Enemy("Dragon")


def test_all_registered_templates_can_be_instantiated():
    """Every entry in ENEMY_TEMPLATES should produce a valid, living Enemy."""
    for kind in ENEMY_TEMPLATES:
        enemy = Enemy(kind)
        assert enemy.is_alive
        assert enemy.hp > 0


def test_enemy_stats_are_independent_between_instances():
    """Two Goblins shouldn't share the same stats dict in memory."""
    goblin1 = Enemy("Goblin")
    goblin2 = Enemy("Goblin")
    goblin1.stats["STR"] = 999
    assert goblin2.stats["STR"] == 8  # unaffected by goblin1's mutation