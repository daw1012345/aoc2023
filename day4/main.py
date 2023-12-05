#!/usr/bin/env python3
from collections import defaultdict


INPUT = "input.txt"


def part1(data):
    total = 0
    for winning, nums in data:
        partial_total = 0
        for n in nums:
            if n in winning:
                if partial_total == 0:
                    partial_total += 1
                else:
                    partial_total *= 2
        total += partial_total
    return total


def part2(data):
    data = [(i, x[0], x[1]) for i, x in enumerate(data)]
    queue = data[:]
    total = len(data)
    # This can be improved by DP

    while queue:
        card = queue.pop()
        card_num, winning, nums = card
        matches = 0
        for n in nums:
            if n in winning:
                matches += 1
        for x in range(1, matches + 1):
            # card_num = data.index(card)
            # print(f"Won {card_num+x+1}")
            queue.append(data[card_num + x])

        total += matches
    return total


def parse():
    with open(INPUT, "r") as fd:
        raw_data = fd.readlines()

    raw_data = [x[x.index(":") + 2 :].strip() for x in raw_data]
    raw_data = [x.split(" | ") for x in raw_data]
    raw_data = [
        (
            list(filter(lambda a: a != "", x[0].split(" "))),
            list(filter(lambda a: a != "", x[1].split(" "))),
        )
        for x in raw_data
    ]

    return raw_data


if __name__ == "__main__":
    d = parse()
    # print(d)
    print(part1(d))
    print(part2(d))
