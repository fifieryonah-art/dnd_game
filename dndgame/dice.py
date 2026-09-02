import random
from typing import List


def roll(dice_type: int, number_of_dice: int) -> int:
    """Roll 'number_of_dice' dice of size 'dice_type' and return their sum."""
    rolls: List[int] = [random.randint(1, dice_type) for _ in range(number_of_dice)]
    total = sum(rolls)
    print(f"Rolling{number_of_dice}d{dice_type}: {rolls} = {total}")
    return total



def roll_with_advantage(dice_type: int) -> int:
    """Roll twice and keep the higher result ("advantage" in D&D terms)."""
    return max(roll(dice_type,1), roll(dice_type, 1))


def roll_with_disadvantage(dice_type: int) -> int:
    """Roll twice and keep the lower result ("disadvantage" in the D&D terms)."""
    return min(roll(dice_type,1), roll(dice_type, 1))
