#!/usr/bin/env python3
import re
import math

INPUT = "input.txt"


def part1(data):
    def getWaysForRace(race: (int, int)):
        total = 0
        for i in range(1, int(race[0])):
            if i * (int(race[0]) - i) > int(race[1]):
                total += 1
        return total

    return math.prod([getWaysForRace(x) for x in data])


def part2(data):
    t, d = zip(*data)
    t = "".join(t)
    d = "".join(d)

    return part1([(t, d)])


def parse():
    dig = re.compile(r"(\d+)")
    with open(INPUT, "r") as fd:
        data = fd.readlines()
    # (time, distance)
    return list(zip(dig.findall(data[0]), dig.findall(data[1])))


if __name__ == "__main__":
    d = parse()
    print(part1(d))
    print(part2(d))
