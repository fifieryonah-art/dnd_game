# player character class and race definitions

from __future__ import annotations
from typing import Dict,  List
from dndgame.entities import Entity
from dndgame.dice import roll


RACE_BONUSES: Dict[str, Dict[str, int]] = {
    "Human": {"STR": 1, "DEX": 1, "CON": 1, "INT": 1, "WIS": 1, "CHA": 1},
    "Elf": {"DEX": 2},
    "Dwarf": {"CON": 2},
    "Halfling": {"DEX": 1, "CHA": 1},
}

STAT_NAMES: List[str] = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]



class Character(Entity):
    # A player-controlled character

    def __init__(self, name: str, race: str, base_hp: int) -> None:
        if race not in RACE_BONUSES:
            raise ValueError(f"Unknown race: {race!r}. Valid races: {list(RACE_BONUSES)}")
        super().__init__(name=name, stats={}, max_hp=0, armor_class=10)
        self.race: str = race
        self.base_hp: int = base_hp
        self.level: int = 1

    def roll_stats(self) -> None:
        # Roll 3d6 for each ability score, then derive HP from CON
        print("Rolling stats...\n")
        for stat in STAT_NAMES:
            print(f"Rolling {stat}...")
            self.stats[stat] = roll(6, 3)
        self.max_hp = self.base_hp + self.get_modifier("CON")
        self.hp = self.max_hp



    def apply_racial_bonuses(self) -> None:
        # Apply this character's racial stat bonuses (data-diven)
        for stat, bonus in RACE_BONUSES[self.race].items():
            self.stats[stat] = self.stats.get(stat, 0) + bonus