import re
import pandas as pd
import numpy as np
from aoc23.common import get_puzzle_input

pd.set_option('display.max_columns', None)

EXAMPLE_INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
EXAMPLE_SOLUTION_A = 4361
EXAMPLE_SOLUTION_B = 467835


def solve_a(puzzle_input):
    xn = re.search(r"\n", puzzle_input).start()
    lines = puzzle_input.split("\n")

    def slice_at_xy(x, y, n):
        if y < 0 or y >= len(lines):
            return ""
        return lines[y][max(0, x):x+n]

    total = 0
    for match in re.finditer(r"\d+", puzzle_input):
        x = match.start() % (xn + 1)
        y = match.start() // (xn + 1)
        ndig = len(match.group())
        partnum = int(match.group())
        for y_offset in (-1, 0, 1):
            slice = slice_at_xy(x - 1, y + y_offset, ndig + 2)
            if re.search(r"[^\.^\d]", slice):
                total += partnum
                break
    return total


def solve_b(puzzle_input):
    xn = re.search(r"\n", puzzle_input).start()
    lines = puzzle_input.split("\n")

    total = 0
    for gear_match in re.finditer(r"\*", puzzle_input):
        gear_x = gear_match.start() % (xn + 1)
        gear_y = gear_match.start() // (xn + 1)
        parts = []
        for y_offset in (-1, 0, 1):
            for match in re.finditer(r"\d+", lines[gear_y + y_offset]):
                x1, x2 = match.span()
                x1 = (x1 % (xn + 1)) - 1
                x2 = (x2 % (xn + 1))
                if x1 <= gear_x <= x2:
                    parts.append(int(match.group()))
        if len(parts) == 2:
            total += parts[0] * parts[1]
    return total


if __name__ == "__main__":
    puzzle_input = get_puzzle_input(__file__)

    assert solve_a(EXAMPLE_INPUT) == EXAMPLE_SOLUTION_A
    print(solve_a(puzzle_input))

    assert solve_b(EXAMPLE_INPUT) == EXAMPLE_SOLUTION_B
    print(solve_b(puzzle_input))
