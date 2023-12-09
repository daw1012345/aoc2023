#!/usr/bin/env python3
from typing import List

INPUT = "input.txt"


def sequences_until_zero(prev_seq):
    n = list(map(lambda x: x[1] - x[0], zip(prev_seq, prev_seq[1:])))
    if not frozenset(prev_seq) == {0}:
        a = sequences_until_zero(n)
        a.append(prev_seq)
        return a
    return [prev_seq]


def extrapolate(seq, revsd=True):
    n = sequences_until_zero(seq)
    prev = n[0][-1]
    for s in n[1:]:
        s = s if not revsd else list(reversed(s))
        prev = s[-1] - prev if revsd else s[-1] + prev
    return prev


def part1(data, revsd=False):
    total = 0
    for x in data:
        total += extrapolate(x, revsd)
    print(total)


def part2(data):
    part1(data, True)


def parse():
    sequences = []
    with open(INPUT, "r") as fd:
        lines = fd.readlines()

    for l in lines:
        sequences.append(list(map(int, l.strip().split(" "))))

    return sequences


if __name__ == "__main__":
    d = parse()
    part1(d)
    part2(d)
