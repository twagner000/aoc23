import re
import pandas as pd
import numpy as np
from aoc23.common import get_puzzle_input

pd.set_option('display.max_columns', None)

EXAMPLE_INPUT = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
EXAMPLE_SOLUTION_A = 8
EXAMPLE_SOLUTION_B = 2286


def max_per_color(puzzle_input):
    def count_for_color(draw, color):
        counts = re.findall(rf"(\d+)\s+{color}", draw)
        if counts:
            return int(counts[0])
        return 0

    def parse_draw(draw):
        return [count_for_color(draw, color) for color in ["red", "green", "blue"]]

    return (
        pd.DataFrame({'raw': puzzle_input.split('\n')})
        .assign(
            game=lambda df: df["raw"].str.extract(r"^Game (\d+):").astype("int"),
            draws=lambda df: df["raw"].str.extract(r": (.*)$", expand=False).str.split("; "),
            draws_arr=lambda df: df["draws"].apply(lambda x: np.array([parse_draw(y) for y in x])),
            max=lambda df: df["draws_arr"].apply(lambda x: x.max(axis=0)),
        )
    )


def solve_a(puzzle_input):
    possible = [12, 13, 14]
    return (
        max_per_color(puzzle_input)
        .assign(possible=lambda df: df["max"].apply(lambda x: all(x <= possible)) * df["game"])
        ["possible"].sum()
    )


def solve_b(puzzle_input):
    return (
        max_per_color(puzzle_input)
        .assign(power=lambda df: df["max"].apply(lambda x: x[0] * x[1] * x[2]))
        ["power"].sum()
    )


if __name__ == "__main__":
    puzzle_input = get_puzzle_input(__file__)

    assert solve_a(EXAMPLE_INPUT) == EXAMPLE_SOLUTION_A
    print(solve_a(puzzle_input))

    assert solve_b(EXAMPLE_INPUT) == EXAMPLE_SOLUTION_B
    print(solve_b(puzzle_input))
