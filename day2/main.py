#!/usr/bin/env python3
import re
import itertools

INPUT = "input.txt"
import math


def part1(data):
    TOTAL_RED = 12
    TOTAL_GREEN = 13
    TOTAL_BLUE = 14

    total = 0

    for gid, games in data.items():
        impossible = False
        for g in games:
            if g[0] > TOTAL_RED or g[1] > TOTAL_GREEN or g[2] > TOTAL_BLUE:
                impossible = True
                break

        if not impossible:
            total += gid

        impossible = False

    print(total)


def part2(data):
    total = 0

    for _, games in data.items():
        total += math.prod(
            (
                max([x[0] for x in games]),
                max([x[1] for x in games]),
                max([x[2] for x in games]),
            )
        )

    print(total)


def parse():
    # Is this robust? No. Does it work? Yes.
    with open(INPUT, "r") as fd:
        raw_data = fd.readlines()

    r = re.compile(r"(\d+)\s+red")
    g = re.compile(r"(\d+)\s+green")
    b = re.compile(r"(\d+)\s+blue")

    data = {int(l[5 : l.index(":")]): l[l.index(":") + 1 :].strip() for l in raw_data}

    # This is fine, we are not adding/deling keys
    for gid in list(data.keys()):
        sets = data[gid].split(";")
        sets = [
            (
                int(r.findall(x)[0]) if r.findall(x) else 0,
                int(g.findall(x)[0]) if g.findall(x) else 0,
                int(b.findall(x)[0]) if b.findall(x) else 0,
            )
            for x in sets
        ]
        data[gid] = sets

    return data


if __name__ == "__main__":
    # Data structure:
    # {game_id : [(RGB),...]}
    d = parse()
    part1(d)
    part2(d)
