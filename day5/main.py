#!/usr/bin/env python3.12
from dataclasses import dataclass
from typing import List, Optional
import itertools
import re


@dataclass(frozen=True)
class AOCMapping:
    start: int
    len: int

    dst: int

    # Returns the consumed range and the actual mapping
    def doMapRange(self, start: int, leng: int) -> ((int, int), (int, int)):
        range_start = max(start, self.start)
        range_end = min(start + leng, self.start + self.len)

        if range_start > range_end:
            return ((None, None), (None, None))

        return (range_start, range_end), (
            self.dst + abs(self.start - range_start),
            self.dst + abs(self.start - range_end),
        )

    def doMap(self, pos: int) -> Optional[int]:
        if self.start <= pos < self.start + self.len:
            return self.dst + abs(pos - self.start)
        return None


@dataclass(frozen=True)
class AOCMap:
    src: str
    dst: str
    mapping: List[AOCMapping]

    def doMapRange(self, start: int, leng: int):
        ranges = []
        all_consumed = []
        for x in self.mapping:
            consumed, mapped = x.doMapRange(start, leng)
            if not mapped[0]:
                continue
            ranges.append(mapped)
            all_consumed.append(consumed)

        all_consumed = list(sorted(all_consumed, key=lambda x: x[0]))

        if not all_consumed:
            ranges.append((start, start + leng))

        # Fix beginning and end
        if all_consumed and all_consumed[0][0] != start:
            ranges.append((start, all_consumed[0][0] - 1))

        if all_consumed and all_consumed[-1][1] != start + leng:
            ranges.append((all_consumed[-1][1], start + leng))

        for p, c in zip(all_consumed, all_consumed[1:]):
            if p[1] + 1 != c[0]:
                ranges.append((p[1] + 1, c[0] - 1))
        return ranges

    def doMap(self, pos: int) -> Optional[int]:
        for m in self.mapping:
            res = m.doMap(pos)
            if res:
                return res

        return pos


INPUT = "input.txt"


def part2(parsed, seeds):
    m = {x.src: x for x in parsed}
    res = float("inf")

    for s, len in itertools.batched(seeds, 2):
        print(s)
        current = "seed"

        ranges = [(s, len)]

        while current != "location":
            tmp_ranges = []
            for x in ranges:
                tmp_ranges.extend(m[current].doMapRange(*x))
            ranges = tmp_ranges

            current = m[current].dst
        res = min(res, min(list(map(lambda x: x[0], ranges))))

    print(res)


def part1(parsed, seeds):
    m = {x.src: x for x in parsed}
    res = float("inf")

    for s in seeds:
        current = "seed"
        a = s
        while current != "location":
            a = m[current].doMap(a)
            current = m[current].dst
        res = min(res, a)

    print(res)


def parse():
    map_re = re.compile(r"(\w+)-to-(\w+)")
    with open(INPUT, "r") as fd:
        raw_data = fd.read()

    sections = raw_data.split("\n\n")
    seeds = list(map(int, sections[0][len("seeds: ") :].split(" ")))

    parsed = []

    for sect in sections[1:]:
        sect_lines = sect.split("\n")

        src, dest = map_re.findall(sect_lines[0])[0]

        maps = []

        for mp in sect_lines[1:]:
            # print(mp)
            dst, start, leng = list(map(int, mp.split(" ")))
            maps.append(AOCMapping(start, leng, dst))

        parsed.append(AOCMap(src, dest, maps))

    return parsed, seeds


if __name__ == "__main__":
    parsed, seeds = parse()
    part1(parsed, seeds)
    part2(parsed, seeds)
