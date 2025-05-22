#!/usr/bin/env python3

# Date:     2025-05-22
# Author:   Tamas Vince
# Purpose:  Generate a dice notation expression that can produce integer values in the range [min_val, max_val].
# Runtime:  33.7ms ± 6.8ms over 1000 runs (tested with hyperfine on ThinkPad T480)

import os
from typing import List, Dict, Optional
from functools import lru_cache

DEBUG: bool = os.getenv("HACKATHON_DEBUG", "0") == "1"
DICE_SET: List[int] = [20, 10, 8, 6, 4, 3, 2]


def dice_range_expression(min_val: int, max_val: int) -> str:
    """
    Generate a dice notation expression that can produce integer values in the range [min_val, max_val].

    The function finds a combination of dice that can express the given range using standard dice notation.
    It tries to find the most efficient combination in terms of number of dice used.

    Args:
        min_val: The minimum value in the range (inclusive)
        max_val: The maximum value in the range (inclusive)

    Returns:
        str: A string in dice notation format (e.g. "2d6+1d4-2") that represents a dice roll
             expression capable of producing all integer values in the given range.
             Returns "No solution found" if no valid expression can be generated.

    Example:
        >>> dice_range_expression(3, 8)
        "1d6+2"
        >>> dice_range_expression(1, 20)
        "1d20"
    """
    D: int = max_val - min_val

    assert D >= 0, "max_val must be greater than or equal to min_val"

    @lru_cache(maxsize=1024)
    def find_combination(target: int, n: int) -> Optional[List[int]]:
        if n == 0:
            return [] if target == 0 else None

        if n <= 0 or target <= 0:
            return None

        for die in DICE_SET:
            if die > target:
                continue
            max_use: int = min(target // die, n)
            for use in range(max_use, 0, -1):
                remaining: int = target - die * use
                result = find_combination(remaining, n - use)
                if result is not None:
                    return [die] * use + result
        return None

    for n in range(1, D + 2):
        target: int = D + n
        combination = find_combination(target, n)

        if combination:
            dice_counts: Dict[int, int] = {}

            for die in combination:
                dice_counts[die] = dice_counts.get(die, 0) + 1
            
            terms: List[str] = []
            for die in sorted(dice_counts.keys()):
                terms.append(f"{dice_counts[die]}d{die}")

            expr: str = "+".join(terms)
            offset: int = min_val - n

            if offset != 0:
                expr += f"{offset:+d}"

            return expr

    raise ValueError("No solution found")

def main() -> None:
    with open("input.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        a, b = map(int, line.strip().split())
        result = dice_range_expression(a, b)
        if DEBUG:
            print(f"{a}-{b} => {result}")
        else:
            print(result)


if __name__ == "__main__":
    main()
