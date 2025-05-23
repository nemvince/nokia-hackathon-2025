#!/usr/bin/env python3

# Date:     2025-05-23
# Author:   Tamas Vince
# Purpose:  Decode and assign codes to days.
# Runtime:  35.6ms ± 6.6ms over 1000 runs (tested with hyperfine on Ryzen 7 2700)

import ast
import os
import json
from collections import defaultdict, deque
from typing import List, Tuple, Dict, Set, DefaultDict, Any

DEBUG = os.environ.get("HACKATHON_DEBUG", "0") == "1"

def debug_print(*args):
    if DEBUG:
        print(*args)

def build_day_data(data: List[Tuple[List[str], List[str]]]) -> Tuple[List[Dict[str, Any]], DefaultDict[str, List[int]]]:
    days: List[Dict[str, Any]] = []
    code_to_days: DefaultDict[str, List[int]] = defaultdict(list)

    for idx, (codes, events) in enumerate(data):
        events_set = set(events)
        days.append({
            "codes": codes,
            "events": events_set,
            "covered": set()
        })
        for code in codes:
            code_to_days[code].append(idx)

    debug_print("code to days mapping:", dict(code_to_days))
    return days, code_to_days

def compute_possible_events(days: List[Dict[str, Any]], code_to_days: DefaultDict[str, List[int]]) -> DefaultDict[str, Set[str]]:
    possible_events: DefaultDict[str, Set[str]] = defaultdict(set)

    for code in code_to_days:
        possible: Set[str] = set()
        for day_idx in code_to_days[code]:
            current_events = days[day_idx]["events"]
            if not possible:
                possible = current_events.copy()
            else:
                possible &= current_events
        possible_events[code] = possible

    debug_print("initial possible events:", dict(possible_events))
    return possible_events

def propagate_assignments(
    days: List[Dict[str, Any]],
    code_to_days: DefaultDict[str, List[int]],
    possible_events: DefaultDict[str, Set[str]]
) -> Dict[str, str]:
    assignments: Dict[str, str] = {}
    queue: deque[str] = deque(code for code, events in possible_events.items() if len(events) == 1)

    while queue:
        code = queue.popleft()
        if code in assignments:
            continue

        event = next(iter(possible_events[code]))
        assignments[code] = event
        debug_print(f"assign {event} to {code}")

        for day_idx in code_to_days[code]:
            day = days[day_idx]
            if event not in day["covered"]:
                day["covered"].add(event)
                remaining_events = day["events"] - day["covered"]

                for e in remaining_events:
                    candidates = [
                        c for c in day["codes"]
                        if c not in assignments and e in possible_events[c]
                    ]
                    if len(candidates) == 1:
                        candidate_code = candidates[0]
                        new_possible = possible_events[candidate_code].intersection({e})
                        if new_possible != possible_events[candidate_code]:
                            debug_print(f"narrow {candidate_code} to {new_possible}")
                            possible_events[candidate_code] = new_possible
                            if len(new_possible) == 1:
                                queue.append(candidate_code)

    return assignments

def solve(data: List[Tuple[List[str], List[str]]]) -> Dict[str, str]:
    days, code_to_days = build_day_data(data)
    possible_events = compute_possible_events(days, code_to_days)
    assignments = propagate_assignments(days, code_to_days, possible_events)

    sorted_codes = sorted(
        assignments.keys(),
        key=lambda x: [int(part) for part in x.split(".")],
        reverse=True
    )

    return {code: assignments[code] for code in sorted_codes}


def main() -> None:
    with open("input.txt", "r") as f:
        file_contents = f.read()

    data = ast.literal_eval(file_contents)
    result = solve(data)

    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
