import pandas as pd
import numpy as np
from aoc23.common import get_puzzle_input

pd.set_option('display.max_columns', None)

EXAMPLE_INPUT = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
EXAMPLE_SOLUTION_A = 13
EXAMPLE_SOLUTION_B = 30


def find_matches(puzzle_input):
    return (
        pd.DataFrame({'raw': puzzle_input.split('\n')})
        .assign(
            winning=lambda df: df["raw"].str.extract(r":\s+(.+)\s+\|", expand=False).str.findall(r"\d+").apply(set),
            chosen=lambda df: df["raw"].str.extract(r"\|\s+(.+)\s*$", expand=False).str.findall(r"\d+").apply(set),
            matches=lambda df: df.apply(lambda x: len(x["winning"] & x["chosen"]), axis=1),
        )
    )


def solve_a(puzzle_input):
    df = (
        find_matches(puzzle_input)
        .assign(value=lambda df: (2 ** (df["matches"] - 1.)).astype(int))
    )
    return df["value"].sum()


def solve_b(puzzle_input):
    df = find_matches(puzzle_input).assign(copies=1)  # start with one copy of each card
    for i in df.index:
        df.loc[i + 1:i + df.loc[i, "matches"], "copies"] += df.loc[i, "copies"]
    return df["copies"].sum()


if __name__ == "__main__":
    puzzle_input = get_puzzle_input(__file__)

    assert solve_a(EXAMPLE_INPUT) == EXAMPLE_SOLUTION_A
    print(solve_a(puzzle_input))

    assert solve_b(EXAMPLE_INPUT) == EXAMPLE_SOLUTION_B
    print(solve_b(puzzle_input))
