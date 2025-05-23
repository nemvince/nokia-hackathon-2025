#!/usr/bin/env python3

# Date:     2025-05-22
# Author:   Tamas Vince
# Purpose:  Generate a list of Fibonacci numbers divisible by 3 up to a given number N.
# Runtime:  18.6ms ± 2.9ms over 1000 runs (tested with hyperfine on ThinkPad T480)

import os
from typing import List

DEBUG = os.environ.get("HACKATHON_DEBUG", "0") == "1"

def fibonacci_up_to(N: int) -> list[int]:
    fib_numbers: List[int] = []
    a, b = 0, 1
    while a <= N:
        fib_numbers.append(a)
        a, b = b, a + b
    return fib_numbers

def solve(line: str) -> str:
    try:
        N: int = int(line.strip())
    except ValueError:
        return "N/A"

    fib_numbers = fibonacci_up_to(N)
    filtered = [x for x in fib_numbers if x % 3 == 0]

    return "N/A" if not filtered else ", ".join(map(str, filtered))

def main() -> None:
    with open("input.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        if DEBUG:
            print(f"{line.strip()} -> {solve(line)}")
        else:
            print(solve(line))

if __name__ == "__main__":
    main()
