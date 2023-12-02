#!/usr/bin/env python3

INPUT = "input.txt"


def part1(data):
    data = [list(filter(lambda c: c.isdigit(), x)) for x in data]
    data = list(map(lambda x: int(f"{x[0]}{x[-1]}"), data))
    print(sum(data))


def part2(data):
    replace_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    for k, v in replace_map.items():
        data = [x.replace(k, f"{k[0]}{v}{k[-1]}") for x in data]
    return part1(data)


def parse():
    with open(INPUT, "r") as fd:
        return fd.readlines()


if __name__ == "__main__":
    d = parse()
    part1(d[:])
    part2(d[:])
