"""Base class shared by every combatant in the game (players and enemies)."""

from typing import Dict

class Entity:
    # A combatant: anything that has stats, HP, and can fight
    def __init__(
        self,
        name: str,
        stats: Dict[str, int],
        max_hp: int,
        armor_class: int = 10,
    ) -> None:
        self.name: str = name 
        self.stats: Dict[str, int] = dict(stats)
        self.max_hp: int = max_hp
        self.hp: int = max_hp
        self.armor_class: int = armor_class

    def get_modifier(self, stat: str) -> int:
        # Return the DnD ability modifier for a stat: (score - 10) // 2.
        return (self.stats[stat] - 10) // 2

    @property
    def is_alive(self) -> bool:
        # True while the entity has more than 0 HP
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        # Reduce HP by 'amount', never going brlow 0. Returns HP actually lost
        actual_loss = min(amount, self.hp)
        self.hp -= actual_loss
        return actual_loss

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, hp={self.hp}/{self.max_hp})"