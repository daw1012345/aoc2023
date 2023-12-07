#!/usr/bin/env python3
INPUT = "input.txt"

from enum import IntEnum
from collections import Counter
import functools


class HandType(IntEnum):
    # Lower = better
    FIVE = 0
    FOUR = 1
    FULL = 2
    THREE = 3
    TWO = 4
    ONE = 5
    HIGH = 6

    NONE = 7


class Hand:
    def __init__(self, hand: str, bid: str):
        assert len(hand) == 5
        self.hand = list(hand)
        self._hand_tally = Counter(self.hand)

        self._jokerless_tally = Counter(self.hand)
        self._jokercount = self.hand.count("J")

        if "J" in self._jokerless_tally:
            self._jokerless_tally.pop("J")

        self.bid = int(bid)

    def _is_five(self):
        return 5 in self._hand_tally.values()

    def _is_four(self):
        return 4 in self._hand_tally.values()

    def _is_full(self):
        return (3 in self._hand_tally.values()) and (2 in self._hand_tally.values())

    def _is_three(self):
        return (3 in self._hand_tally.values()) and (2 not in self._hand_tally.values())

    def _is_two(self):
        return list(self._hand_tally.values()).count(2) == 2

    def _is_one(self):
        return (
            list(self._hand_tally.values()).count(2) == 1
            and list(self._hand_tally.values()).count(1) == 3
        )

    def _is_high(self):
        return list(self._hand_tally.values()).count(1) == 5

    # ---------------------------------------------------------------

    def _can_be_five(self):
        if self._jokercount >= 5:
            return True

        m = list(zip(*self._jokerless_tally.most_common(1)))[1][0]
        return m + self._jokercount >= 5

    def _can_be_four(self):
        m = list(zip(*self._jokerless_tally.most_common(1)))[1][0]
        return (
            m <= 4
            and m + self._jokercount >= 4
            and len(set(self._jokerless_tally.values())) == 2
        )

    def _can_be_full(self):
        a, b = list(zip(*self._jokerless_tally.most_common(2)))[1]
        return (
            a <= 3
            and b <= 2
            and a + self._jokercount >= 3
            and b + (self._jokercount - (3 - a)) >= 2
        )

    def _can_be_three(self):
        m = list(zip(*self._jokerless_tally.most_common(1)))[1][0]
        return (
            m <= 3
            and m + self._jokercount >= 3
            and list(self._jokerless_tally.values()).count(1) >= 2
        )

    def _can_be_two(self):
        a, b = list(zip(*self._jokerless_tally.most_common(2)))[1]
        return a <= 2 and b <= 2 and a + b + self._jokercount >= 4

    def _can_be_one(self):
        m = list(zip(*self._jokerless_tally.most_common(1)))[1][0]
        return m <= 2 and m + self._jokercount >= 2

    def _can_be_high(self):
        return self._is_high() or (
            list(self._jokerless_tally.values()).count(1) == (5 - self._jokercount)
        )

    # ---------------------------------------------------------------

    def get_possible_type(self):
        m = {
            HandType.FIVE: self._can_be_five,
            HandType.FOUR: self._can_be_four,
            HandType.FULL: self._can_be_full,
            HandType.THREE: self._can_be_three,
            HandType.TWO: self._can_be_two,
            HandType.ONE: self._can_be_one,
            HandType.HIGH: self._can_be_high,
        }
        if self._jokercount <= 0:
            return self.get_hand_type()
        for t, check in m.items():
            if check():
                return t

        return HandType.NONE

    def get_hand_type(self):
        m = {
            HandType.FIVE: self._is_five,
            HandType.FOUR: self._is_four,
            HandType.FULL: self._is_full,
            HandType.THREE: self._is_three,
            HandType.TWO: self._is_two,
            HandType.ONE: self._is_one,
            HandType.HIGH: self._is_high,
        }

        for t, check in m.items():
            if check():
                return t

        return HandType.NONE

    @staticmethod
    def compare_joker(hand1, hand2) -> int:
        m = {"A": 14, "K": 13, "Q": 12, "J": 0, "T": 10}
        # Smaller = better
        if hand1.get_possible_type() < hand2.get_possible_type():
            return 1
        elif hand1.get_possible_type() > hand2.get_possible_type():
            return -1
        else:
            for a, b in zip(hand1.hand, hand2.hand):
                if a == b:
                    continue

                a_val = int(a) if a not in m else m[a]
                b_val = int(b) if b not in m else m[b]
                return a_val - b_val
        return 0

    @staticmethod
    def compare(hand1, hand2) -> int:
        m = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}
        # Smaller = better
        if hand1.get_hand_type() < hand2.get_hand_type():
            return 1
        elif hand1.get_hand_type() > hand2.get_hand_type():
            return -1
        else:
            for a, b in zip(hand1.hand, hand2.hand):
                if a == b:
                    continue

                a_val = int(a) if a not in m else m[a]
                b_val = int(b) if b not in m else m[b]
                return a_val - b_val

    def __repr__(self):
        return str(f"{''.join(self.hand)} {self.bid}")


def part1(data):
    total = 0
    s_data = sorted(data, key=functools.cmp_to_key(Hand.compare))
    for i, h in enumerate(s_data):
        total += (i + 1) * h.bid

    print(total)


def part2(data):
    total = 0
    s_data = sorted(data, key=functools.cmp_to_key(Hand.compare_joker))
    for i, h in enumerate(s_data):
        total += (i + 1) * h.bid
    print(total)


def parse():
    hands = []
    with open(INPUT, "r") as fd:
        raw_data = fd.readlines()
        for l in raw_data:
            s_l = l.split(" ")
            hands.append(Hand(s_l[0], s_l[1].strip()))

    return hands


if __name__ == "__main__":
    d = parse()
    part1(d)
    part2(d)
