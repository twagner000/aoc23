import re
import pandas as pd
import numpy as np
from aoc23.common import get_puzzle_input

EXAMPLE_INPUT = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
EXAMPLE_SOLUTION_A = 142
EXAMPLE_INPUT_2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
EXAMPLE_SOLUTION_B = 281


def solve_a(puzzle_input):
    return (
        pd.DataFrame({'raw': puzzle_input.split('\n')})
        .assign(
            dig1=lambda df: df["raw"].str.extract(r"^\D*(\d)").astype("int"),
            dig2=lambda df: df["raw"].str.extract(r"(\d)\D*$").astype("int"),
            cal_val=lambda df: 10 * df["dig1"] + df["dig2"],
        )
        ["cal_val"].sum()
    )


def solve_b(puzzle_input):
    digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    def word_to_digit(word):
        try:
            return digits.index(word) + 1
        except ValueError:
            return int(word)

    return (
        pd.DataFrame({'raw': puzzle_input.split('\n')})
        .assign(
            dig1=lambda df: df["raw"].str.extract(r"^.*?(\d|" + "|".join(digits) + r")"),
            dig2=lambda df: df["raw"].apply(lambda x: x[::-1]).str.extract(r"(\d|" + "|".join([x[::-1] for x in digits]) + r").*?$"),
        )
        .assign(
            dig1=lambda df: df["dig1"].apply(word_to_digit),
            dig2=lambda df: df["dig2"].apply(lambda x: word_to_digit(x[::-1])),
            cal_val=lambda df: 10 * df["dig1"] + df["dig2"],
        )
        ["cal_val"].sum()
    )


if __name__ == "__main__":
    puzzle_input = get_puzzle_input(__file__)

    assert solve_a(EXAMPLE_INPUT) == EXAMPLE_SOLUTION_A
    print(solve_a(puzzle_input))

    assert solve_b(EXAMPLE_INPUT_2) == EXAMPLE_SOLUTION_B
    print(solve_b(puzzle_input))
