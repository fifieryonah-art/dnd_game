"""Turn-based combat engine."""

from __future__ import annotations

from typing import List

from dndgame.dice import roll
from dndgame.entities import Entity


class Combat:
    """Runs a turn-based fight between the player and one enemy."""

    def __init__(self, player: Entity, enemy: Entity, weapon_die: int = 6):
        self.player = player
        self.enemy = enemy
        self.weapon_die = weapon_die
        self.round: int = 0
        self.initiative_order: List[Entity] = []

    def roll_initiative(self) -> List[Entity]:
        """Decide turn order via a DEX-modified d20 roll for each side."""
        player_init = roll(20, 1) + self.player.get_modifier("DEX")
        enemy_init = roll(20, 1) + self.enemy.get_modifier("DEX")
        self.initiative_order = (
            [self.player, self.enemy] if player_init >= enemy_init else [self.enemy, self.player]
        )
        return self.initiative_order

    def attack(self, attacker: Entity, defender: Entity) -> int:
        """Resolve a single attack; rolls to-hit, then damage on a hit."""
        attack_roll = roll(20, 1) + attacker.get_modifier("STR")
        if attack_roll >= defender.armor_class:
            damage = roll(self.weapon_die, 1)
            return defender.take_damage(damage)
        return 0

    def run(self) -> bool:
        """Run the full combat loop. Returns True if the player wins."""
        self.roll_initiative()
        while self.player.is_alive and self.enemy.is_alive:
            self.round += 1
            print(f"\n--- Round {self.round} ---")
            for combatant in self.initiative_order:
                if combatant is self.player:
                    if not self._player_turn():
                        print("You ran away!")
                        return False
                else:
                    self._enemy_turn(combatant)

                fallen = list(filter(lambda e: not e.is_alive, [self.player, self.enemy]))
                if self.enemy in fallen:
                    return True
                if self.player in fallen:
                    print("\nYou have been defeated...")
                    return False
        return not self.enemy.is_alive

    def _player_turn(self) -> bool:
        """Handle the player's turn. Returns False if they flee."""
        print(f"\n{self.enemy.name} HP: {self.enemy.hp}")
        print("1. Attack")
        print("2. Run away")
        choice = input("What do you do? ").strip()
        if choice == "2":
            return False
        damage = self.attack(self.player, self.enemy)
        print(f"You hit for {damage} damage!" if damage else "You missed!")
        return True

    def _enemy_turn(self, enemy: Entity) -> None:
        """Handle one enemy's attack against the player."""
        damage = self.attack(enemy, self.player)
        if damage:
            print(f"The {enemy.name} hits you for {damage} damage!")
        else:
            print(f"The {enemy.name} misses!")