import re
import pandas as pd
import numpy as np
from aoc23.common import get_puzzle_input

pd.set_option('display.max_columns', None)

EXAMPLE_INPUT = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
EXAMPLE_SOLUTION_A = 35
EXAMPLE_SOLUTION_B = 46


def create_lookups(puzzle_input):
    def create_lookup(match):
        y = tuple(int(x) for x in match[1:])
        # remap from dest, src, range length to start, end, adj
        return y[1], y[1] + y[2] - 1, y[0] - y[1]

    return (
        pd.DataFrame({'raw': re.split(r"\n(?=.*:)", puzzle_input, flags=re.MULTILINE)})
        .assign(
            seeds=lambda df: np.where(
                df.index == 0,
                df["raw"].str.findall(r"\d+").apply(lambda x: [int(v) for v in x]),
                np.nan,
            ),
            lines=lambda df: (
                df["raw"]
                .str.findall(r"((\d+) (\d+) (\d+))")
                .apply(lambda line: [create_lookup(x) for x in line])
            ),
        )
    )


def map_seeds(seeds, maps):
    """ mutates seeds """
    def map_val(v, lines):
        for line in lines:
            if line[0] <= v <= line[1]:
                return v + line[2]
        else:
            return v

    for map in maps:
        seeds = [map_val(v, map) for v in seeds]
    return seeds


def solve_a(puzzle_input):
    df = create_lookups(puzzle_input)
    return min(map_seeds(df.loc[0, "seeds"], df.loc[1:, "lines"]))


def map_seed_ranges(ranges, maps):
    new_ranges = ranges.copy()
    for map in maps:
        old_ranges = new_ranges
        new_ranges = []
        for l1, l2, adj in map:
            i = 0
            while i < len(old_ranges):
                start, end = old_ranges[i]
                if l2 < start or l1 > end:
                    i += 1
                elif l1 <= start and end <= l2:  # map line covers entire range
                    old_ranges.pop(i)
                    new_ranges.append((start + adj, end + adj))
                elif l1 <= start and end > l2:  # map line covers first part of range
                    old_ranges.pop(i)
                    old_ranges.append((l2 + 1, end))
                    new_ranges.append((start + adj, l2 + adj))
                elif end <= l2:  # map line covers last part of range
                    old_ranges.pop(i)
                    old_ranges.append((start, l1 - 1))
                    new_ranges.append((l1 + adj, end + adj))
                elif end > l2:  # map line covers middle part of range
                    old_ranges.pop(i)
                    old_ranges.append((start, l1 - 1))
                    old_ranges.append((l2 + 1, end))
                    new_ranges.append((l1 + adj, l2 + adj))
        new_ranges += old_ranges  # ranges that weren't covered by any map line get carried over
    return new_ranges


def solve_b(puzzle_input):
    df = create_lookups(puzzle_input)
    ranges = [(start, start + length) for start, length in zip(df.loc[0, "seeds"][::2], df.loc[0, "seeds"][1::2])]
    return min(map_seed_ranges(ranges, df.loc[1:, "lines"]))[0]


if __name__ == "__main__":
    puzzle_input = get_puzzle_input(__file__)

    assert solve_a(EXAMPLE_INPUT) == EXAMPLE_SOLUTION_A
    print(solve_a(puzzle_input))

    assert solve_b(EXAMPLE_INPUT) == EXAMPLE_SOLUTION_B
    print(solve_b(puzzle_input))
