#!/usr/bin/env python3
import re
import math

INPUT = "input.txt"


def part1(instr, nodes_dict, start="AAA", ptwo=False):
    current = start
    steps = 0
    current_instr = 0

    while (not ptwo and current != "ZZZ") or (ptwo and current[-1] != "Z"):
        if instr[current_instr] == "L":
            current = nodes_dict[current][0]
        else:
            current = nodes_dict[current][1]
        steps += 1
        current_instr = (current_instr + 1) % len(instr)
    return steps


def part2(instr, nodes_dict):
    status = list(filter(lambda x: x[-1] == "A", nodes_dict.keys()))
    return math.lcm(
        *list(map(lambda x: part1(instr, nodes_dict, start=x, ptwo=True), status))
    )


def parse():
    r = re.compile(r"(\w+)\s+=\s+\((\w+),\s+(\w+)\)\s*")

    # Node_str : (left, right)
    nodes_dict = dict()

    with open(INPUT, "r") as fd:
        lines = fd.readlines()

    instr = list(lines[0].strip())

    for l in lines[2:]:
        for name, left, right in r.findall(l.strip()):
            nodes_dict[name] = (left, right)

    return instr, nodes_dict


if __name__ == "__main__":
    d = parse()
    # print(d)
    print(part1(*d))
    print(part2(*d))
