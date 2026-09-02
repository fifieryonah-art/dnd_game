# Enemy NPC class and enemy-class

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

@dataclass(frozen=True)
class EnemyTemplate:
    # Immutable blueprint for spawning an Enemy of a given kind
    stats: Dict[str, int] = field(default_factory=dict)
    hp: int = 1
    armor_class: int = 10


ENEMY_TEMPLATES: Dict[str, EnemyTemplate] = {
    "Goblin": EnemyTemplate(stats={"STR": 8, "DEX": 10, "CON": 10}, hp=5, armor_class=12),
    "Orc": EnemyTemplate(stats={"STR": 16, "DEX": 10, "CON": 14}, hp=15, armor_class=13),
}


class Enemy(Entity):
    # An NPC opponent, built from a named template in ENEMY_TEMPLATES

    def __init__(self, kind: str) -> None:
        if kind not in ENEMY_TEMPLATES:
            raise ValueError(f"Unknown enemy kind: {kind!r}. Valid kinds: {list(ENEMY_TEMPLATES)}")
        template = ENEMY_TEMPLATES[kind]
        super().__init__(
            name=kind,
            stats=dict(template.stats),
            max_hp=template.hp,
            armor_class=template.armor_class,
        )

        self.kind: str = kind