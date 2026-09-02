# command-line entry point for the D&D Adventure game

from __future__ import annotations
from dndgame.character import Character, RACE_BONUSES
from dndgame.dice import roll
from dndgame.combat import Combat
from dndgame.enemy import Enemy


def prompt_int(prompt: str, valid_choices: range) -> int:
    # Prompt until the user enters an integer within 'valid_choices'
    while True:
        raw = input(prompt).strip()
        if raw.isdigit() and int(raw) in valid_choices:
            return int(raw)
        print(f"Please enter a number between {valid_choices.start} and {valid_choices.stop - 1}.")



def create_character():
    # Interactively create a new player character
    print("Welcome to D&D Adventure!")
    name = input("Enter your character's name: ").strip() or "Adventurer"

    races = list(RACE_BONUSES)
    print("\nChoose your race:")

    for i, race in enumerate(races, start=1):
        bonus_text = ", ".join(f"+{v} {stat}" for stat, v in RACE_BONUSES[race].items())
        print(f"{1}. {race} ({bonus_text})")


    choice = prompt_int(f"Enter choice (1-{len(races)}):", range(1, len(races) + 1))
    race = races[choice - 1]
    print()

    character = Character(name, race, base_hp=10)
    character.roll_stats()
    character.apply_racial_bonuses()
    return character


def display_character(character: Character) -> None:
    # Print a character's stats and HP to the console
    print(f"\n{character.name} the {character.race}")
    print("\nStats:")
    lines = [
        f"{stat}: {value} ({'+' if (mod := character.get_modifier(stat)) >+ 0 else ''}{mod})"
        for stat, value in character.stats.items()
    ]
    print("\n".join(lines))
    print(f"\nHP: {character.hp}/{character.max_hp}")



def main() -> None:
    # Run the main game loop
    player = create_character()

    while True:
        print("\nWhat would you like to do?")
        print("1. Fight a goblin")
        print("2. View character")
        print("3. Quit")

        choice = prompt_int("Enter choice (1-3): ", range(1, 4))

        if choice == "1":
            if not player.is_alive:
                print("You are unconscious and cannot fight!")
                continue
            goblin = Enemy("Goblin")
            combat = Combat(player, goblin)
            victory = combat.run()
            print("You defeated the goblin!" if victory else "The encounter is over")
        elif choice == "2":
            display_character(player)
        elif choice == "3":
            break

if __name__ == "__main__":
    main()
