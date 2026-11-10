# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dyadic-intervals/. The authors are listed in prov/G0NHYJ.jsonl.
"""Dyadic intervals over the universe [0, 2^L), and the canonical decomposition of a range.

A dyadic interval of level j is [k 2^j, (k + 1) 2^j - 1] for an integer k. It is
written here as the pair (j, k).
"""

from __future__ import annotations


def interval(j: int, k: int) -> tuple[int, int]:
    """Return the closed range of the dyadic interval (j, k)."""
    return (k << j, ((k + 1) << j) - 1)


def decompose(a: int, b: int, levels: int) -> list[tuple[int, int]]:
    """Split [a, b] into the fewest dyadic intervals, as (level, index) pairs.

    Requires 0 <= a <= b < 2^levels. The result has at most 2 * levels pairs
    (one pair when [a, b] is the whole universe).
    """
    if not 0 <= a <= b < (1 << levels):
        raise ValueError("need 0 <= a <= b < 2^levels")
    left: list[tuple[int, int]] = []
    right: list[tuple[int, int]] = []
    lo, hi, j = a, b + 1, 0  # @line L1
    while lo < hi:  # @line L2
        if lo & 1:  # @line L3
            left.append((j, lo))
            lo += 1
        if hi & 1:  # @line L4
            hi -= 1
            right.append((j, hi))
        lo >>= 1  # @line L5
        hi >>= 1
        j += 1
    return left + right[::-1]  # @line L6


def prefix_decompose(b: int, levels: int) -> list[tuple[int, int]]:
    """Split [0, b] into dyadic intervals, one for each 1 bit of b + 1."""
    out = []
    x = b + 1
    start = 0
    for j in range(levels, -1, -1):
        if x >> j & 1:
            out.append((j, start >> j))
            start += 1 << j
    return out


class DyadicCounts:
    """Exact counts for every dyadic interval, for range counts and quantiles.

    A sketch such as Count-Min can replace each level by an approximate counter;
    the queries below stay the same.
    """

    def __init__(self, levels: int) -> None:
        self.levels = levels
        self.n = 0
        self.count: list[dict[int, int]] = [dict() for _ in range(levels + 1)]

    def update(self, x: int, c: int = 1) -> None:
        """Add c copies of x (c may be negative in the turnstile model)."""
        self.n += c
        for j in range(self.levels + 1):
            k = x >> j
            self.count[j][k] = self.count[j].get(k, 0) + c

    def range_count(self, a: int, b: int) -> int:
        """Number of items in [a, b], as a sum over at most 2L dyadic counts."""
        return sum(self.count[j].get(k, 0) for j, k in decompose(a, b, self.levels))

    def quantile(self, r: int) -> int:
        """Smallest x with at least r items in [0, x], by a walk down the levels."""
        if not 1 <= r <= self.n:
            raise ValueError("rank out of range")
        k = 0
        for j in range(self.levels - 1, -1, -1):
            left = self.count[j].get(2 * k, 0)
            if r <= left:
                k = 2 * k
            else:
                r -= left
                k = 2 * k + 1
        return k

    def check_invariant(self) -> None:
        """Each count is the sum of its two children."""
        for j in range(1, self.levels + 1):
            for k, c in self.count[j].items():
                kids = self.count[j - 1].get(2 * k, 0) + self.count[j - 1].get(2 * k + 1, 0)
                assert c == kids
