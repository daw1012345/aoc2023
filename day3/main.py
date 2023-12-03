#!/usr/bin/env python3
import re
import math
from collections import defaultdict

INPUT = "input.txt"


def get_surrounding_area(start_x, start_y, end_x, end_y):
    # We can get some negatives here, but it doesn't matter since specials will always be positive so no match with them is possible
    area = []
    # Left
    area.append((start_x - 1, start_y))
    # Right
    area.append((end_x, end_y))
    # Top and bottom
    # Extend by 1 in either direction to allow diagonal matches
    for x in range(start_x - 1, end_x + 1):
        area.append((x, start_y - 1))
        area.append((x, start_y + 1))

    return area


def part1(digits, specials):
    total = 0
    for m in digits:
        if any(
            [
                x in specials
                for x in get_surrounding_area(
                    m[0][0][0], m[0][0][1], m[0][1][0], m[0][1][1]
                )
            ]
        ):
            total += m[1]

    print(total)


def part2(digits, specials):
    # We only want the gears
    matches = defaultdict(list)
    total = 0

    for m in digits:
        for possible_loc in get_surrounding_area(
            m[0][0][0], m[0][0][1], m[0][1][0], m[0][1][1]
        ):
            if possible_loc in specials:
                matches[possible_loc].append(m[1])

    for _, v in matches.items():
        if len(v) == 2:
            total += math.prod(v)

    print(total)


def parse(f=None):
    # Approach - parse all numbers into format: (((xs,ys),(xe,ye)), num)
    # Parse all chars into: [((x, y), char)]
    digit_re = re.compile(r"(\d+)")
    char_re = re.compile(r"([^\w\.]+)")

    digits = []
    specials = []

    with open(INPUT, "r") as fd:
        raw_data = fd.readlines()

    for i, line in enumerate(raw_data):
        for digit_match in digit_re.finditer(line):
            digits.append(
                (
                    ((digit_match.start(), i), (digit_match.end(), i)),
                    int(digit_match.group()),
                )
            )
        for symbol_match in char_re.finditer(line.strip()):
            specials.append(((symbol_match.start(), i), symbol_match.group()))

    if f:
        specials = list(filter(lambda g: g[1] == f, specials))
    specials = list(map(lambda x: x[0], specials))

    return digits, specials


if __name__ == "__main__":
    part1(*parse())
    part2(*parse(f="*"))
