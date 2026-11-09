# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fisher-yates-shuffle/. The authors are listed in prov/NRAJQ8.jsonl.

import random
from typing import TypeVar

T = TypeVar("T")


def fisher_yates_shuffle(a: list[T], rng: random.Random) -> list[T]:
    """Put the list a in a uniformly random order, in place, and return it.

    This is Durstenfeld's form of the Fisher-Yates shuffle (Knuth's Algorithm P).
    Each of the n! orders has probability exactly 1/n!, if rng.randrange(i + 1)
    is uniform on 0..i. It makes n - 1 calls to rng.randrange and n - 1 swaps,
    so it takes Theta(n) time and O(1) extra space.
    """
    for i in range(len(a) - 1, 0, -1):  # @line L1
        j = rng.randrange(i + 1)  # @line L2
        a[i], a[j] = a[j], a[i]  # @line L3
    return a


def inside_out_shuffle(items: list[T], rng: random.Random) -> list[T]:
    """Return a new list with the items in a uniformly random order.

    The inside-out form reads the input once, left to right, and never
    changes it. After step i the prefix b[0..i] is a uniform order of
    items[0..i]. Theta(n) time, Theta(n) space for the output.
    """
    b: list[T] = []
    for i in range(len(items)):
        j = rng.randrange(i + 1)
        b.append(items[i])
        b[i], b[j] = b[j], b[i]
    return b


def random_below(m: int, rng: random.Random) -> int:
    """Return an integer uniform on 0..m-1 from random bits, by rejection.

    It draws k = bit_length(m - 1) bits at a time and rejects a value of m or
    more. One draw is accepted with probability m / 2^k > 1/2, so the
    expected number of bits is k * 2^k / m < 2k. Requires m >= 1.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    k = (m - 1).bit_length()
    while True:
        v = rng.getrandbits(k) if k else 0
        if v < m:
            return v
