from collections import Counter
import pandas as pd
import numpy as np
from aoc23.common import get_puzzle_input

pd.set_option('display.max_columns', None)

EXAMPLE_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
EXAMPLE_SOLUTION_A = 6440
EXAMPLE_SOLUTION_B = 5905

# remap face cards for easy sorting
REMAP_DICT = {
    "A": "z",
    "K": "y",
    "Q": "x",
    "J": "w",
    "T": "v",
}


def hand_type(hand):
    counts = sorted([(b, a) for a, b in Counter(hand).items()], reverse=True)
    if counts[0][0] == 5:
        return 6  # five of a kind
    elif counts[0][0] == 4:
        return 5  # four of a kind
    elif counts[0][0] == 3 and counts[1][0] == 2:
        return 4  # full house
    elif counts[0][0] == 3:
        return 3  # three of a kind
    elif counts[0][0] == 2 and counts[1][0] == 2:
        return 2  # two pair
    elif counts[0][0] == 2:
        return 1  # one pair
    return 0  # high card


def best_hand_type(hand):
    jokers = hand.count("J")
    if jokers == 0:
        return hand_type(hand)
    return max([
        hand_type(hand.replace("J", sub))
        for sub in ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    ])


def solve(puzzle_input, hand_type_func, remap_dict):
    df = (
        pd.DataFrame({'raw': puzzle_input.split('\n')})
        .assign(
            hand=lambda df: df['raw'].str.extract(r'^(\S+)'),
            bid=lambda df: df['raw'].str.extract(r'(\d+)$').astype(int),
            hand_type=lambda df: df["hand"].apply(hand_type_func),
            hand_sortable=lambda df: df["hand"].apply(lambda x: ''.join([remap_dict.get(c, c) for c in x])),
        )
        .sort_values(["hand_type", "hand_sortable"])
        .reset_index(drop=True)
        .assign(winnings=lambda df: df["bid"] * (df.index + 1))
    )
    return df["winnings"].sum()


def solve_a(puzzle_input):
    return solve(puzzle_input, hand_type, REMAP_DICT)


def solve_b(puzzle_input):
    return solve(puzzle_input, best_hand_type, {**REMAP_DICT, "J": "1"})


if __name__ == "__main__":
    puzzle_input = get_puzzle_input(__file__)

    assert solve_a(EXAMPLE_INPUT) == EXAMPLE_SOLUTION_A
    print(solve_a(puzzle_input))

    assert solve_b(EXAMPLE_INPUT) == EXAMPLE_SOLUTION_B
    print(solve_b(puzzle_input))
