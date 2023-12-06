import re
from functools import reduce
import operator

import pandas as pd
import numpy as np
from aoc23.common import get_puzzle_input

pd.set_option('display.max_columns', None)

EXAMPLE_INPUT = """Time:      7  15   30
Distance:  9  40  200"""
EXAMPLE_SOLUTION_A = 288
EXAMPLE_SOLUTION_B = 71503

def product_of_race_margins(races):
    margins = [0] * len(races)
    for i, (time, record) in enumerate(races):
        for hold in range(time):
            dist = hold * (time - hold)
            if dist > record:
                margins[i] += 1
    return reduce(operator.mul, margins)


def solve_a(puzzle_input):
    races = list(zip(*[[int(x) for x in re.findall(r"\D(\d+)", line)] for line in puzzle_input.split('\n')]))
    return product_of_race_margins(races)


def solve_b(puzzle_input):
    # brute force, but it works
    races = list(zip(*[[int(x.replace(" ", "")) for x in re.findall(r"([\d\s]+)", line)] for line in puzzle_input.split('\n')]))
    return product_of_race_margins(races)


if __name__ == "__main__":
    puzzle_input = get_puzzle_input(__file__)

    assert solve_a(EXAMPLE_INPUT) == EXAMPLE_SOLUTION_A
    print(solve_a(puzzle_input))

    assert solve_b(EXAMPLE_INPUT) == EXAMPLE_SOLUTION_B
    print(solve_b(puzzle_input))
