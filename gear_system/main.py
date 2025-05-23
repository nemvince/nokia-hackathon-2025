#!/usr/bin/env python3

# Date:     2025-05-23
# Author:   Tamas Vince
# Purpose:  Solve a puzzle involving gears manipulated by left and right levers
# Runtime:  33.6ms ± 6.9ms over 1000 runs (tested on Ryzen 7 2700)

import collections
import ast
from typing import List, Tuple, Deque

NUM_GEARS: int = 3
INITIAL_GEARS_STATE: Tuple[int, int, int] = (3, 3, 3)

LEFT_LEVER_EFFECT: Tuple[int, int, int] = (1, 1, 0)
RIGHT_LEVER_EFFECT: Tuple[int, int, int] = (0, 1, 1)
DEFAULT_MAX_PULLS: int = 8


def _apply_lever_action(current_gears: Tuple[int, int, int],
                        lever_effect: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Apply a lever's effect to the current gear configuration.

    Gear values cycle in the range 1 -> 2 -> 3 -> 1.

    Args:
        current_gears: The current state of the gears as a tuple of 3 integers.
        lever_effect: A tuple of 3 integers indicating which gears are affected by the lever.

    Returns:
        A new tuple representing the updated gear state.
    """
    new_gears_list = list(current_gears)
    for i in range(NUM_GEARS):
        increment = lever_effect[i]
        if increment > 0:
            current_val = new_gears_list[i]
            new_gears_list[i] = (current_val - 1 + increment) % 3 + 1
    return (new_gears_list[0], new_gears_list[1], new_gears_list[2])


def solve_gears_puzzle(target_state_list: List[int], max_pulls: int = DEFAULT_MAX_PULLS) -> str:
    """
    Solve the gears puzzle by determining a sequence of lever pulls to reach the target state.

    Uses breadth-first search to find the shortest sequence within the allowed number of pulls.

    Args:
        target_state_list: A list of 3 integers (values 1 to 3) representing the desired gear state.
        max_pulls: Maximum number of lever pulls allowed to reach the solution.

    Returns:
        A string representing the lever pull sequence (e.g., "left right left"), or an error message,
        or "Megoldhatatlan" if no solution exists within the allowed pulls.
    """
    if not (isinstance(target_state_list, list) and len(target_state_list) == NUM_GEARS and
            all(isinstance(x, int) and 1 <= x <= 3 for x in target_state_list)):
        return f"Error: Invalid target state format: {target_state_list}"

    target_state: Tuple[int, int, int] = (target_state_list[0], target_state_list[1], target_state_list[2])

    if INITIAL_GEARS_STATE == target_state:
        return ""

    queue: Deque[Tuple[Tuple[int, int, int], List[str]]] = collections.deque()
    queue.append((INITIAL_GEARS_STATE, []))
    visited: set[Tuple[int, int, int]] = {INITIAL_GEARS_STATE}

    lever_options = [
        ("left", LEFT_LEVER_EFFECT),
        ("right", RIGHT_LEVER_EFFECT)
    ]

    while queue:
        current_gears, current_path = queue.popleft()

        if len(current_path) == max_pulls:
            continue

        for lever_name, lever_effect in lever_options:
            next_gears_state = _apply_lever_action(current_gears, lever_effect)
            new_path = current_path + [lever_name]

            if next_gears_state == target_state:
                return " ".join(new_path)

            if next_gears_state not in visited:
                visited.add(next_gears_state)
                queue.append((next_gears_state, new_path))

    return "Megoldhatatlan"


def main():
    """
    Main driver function that reads input from 'input.txt', parses gear puzzle targets,
    and prints solutions for each puzzle line.

    Examples:
        [1, 2, 3]
        [2, 1, 3] 10
    """
    with open("input.txt", 'r') as f:
        lines = f.read().splitlines()

    for line in lines:
        if line[-1] != "]":
            rbracket_idx = line.find("]")
            data = ast.literal_eval(line[:rbracket_idx+1])
            max_pulls = int(line[rbracket_idx+1:])

            print(solve_gears_puzzle(data, max_pulls))
        else:
            print(solve_gears_puzzle(ast.literal_eval(line)))


if __name__ == "__main__":
    main()
