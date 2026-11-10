# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dgim-algorithm/. The authors are listed in prov/KD0VWY.jsonl.
"""The DGIM algorithm for basic counting over a count-based sliding window.

The structure keeps buckets of 1s. A bucket has a size 2^j and a timestamp,
the position of its most recent 1. Level j holds the timestamps of the
buckets of size 2^j, newest first. With L = ceil(k/2), each level below the
largest has L or L + 1 buckets, and the largest has 1 to L + 1.
"""

from collections import deque
from fractions import Fraction
from typing import Deque, List, Tuple


class DGIM:
    """Basic counting over the last W bits with relative error less than 1/k."""

    def __init__(self, window: int, k: int) -> None:
        if window < 1 or k < 1:
            raise ValueError("window and k must be at least 1")
        self.window = window
        self.k = k
        self.cap = (k + 1) // 2  # L = ceil(k/2)
        self.levels: List[Deque[int]] = []  # levels[j]: timestamps, newest at the left
        self.t = 0
        self.total = 0  # the sum of the sizes of all buckets
        self.merges = 0

    def _oldest_level(self) -> int:
        return len(self.levels) - 1

    def update(self, bit: int) -> None:
        """Read one bit (lines L1 to L8)."""
        self.t += 1  # @line L1
        top = self._oldest_level()
        if top >= 0 and self.levels[top][-1] <= self.t - self.window:  # @line L2
            self.levels[top].pop()
            self.total -= 1 << top
            if not self.levels[top]:
                self.levels.pop()
        if bit:  # @line L3
            if not self.levels:  # @line L4
                self.levels.append(deque())
            self.levels[0].appendleft(self.t)
            self.total += 1
            j = 0  # @line L5
            while len(self.levels[j]) == self.cap + 2:  # @line L6
                self.levels[j].pop()  # @line L7
                newer = self.levels[j].pop()
                if j + 1 == len(self.levels):
                    self.levels.append(deque())
                self.levels[j + 1].appendleft(newer)
                self.merges += 1
                j += 1  # @line L8

    def buckets(self) -> List[Tuple[int, int]]:
        """All buckets as (timestamp, size), newest first."""
        out = []
        for j, lev in enumerate(self.levels):
            out.extend((ts, 1 << j) for ts in lev)
        return out

    def query(self, w: int = 0) -> Fraction:
        """Estimate the number of 1s in the last w bits, 1 <= w <= W (default W); lines L9 to L11."""
        if w == 0:
            w = self.window
        if not 1 <= w <= self.window:
            raise ValueError("w must be in 1..W")
        if w == self.window:
            if not self.levels:
                return Fraction(0)
            last = 1 << self._oldest_level()
            s = self.total - last
        else:
            inside = [size for ts, size in self.buckets() if ts > self.t - w]  # @line L9
            if not inside:
                return Fraction(0)
            last = inside[-1]  # @line L10
            s = sum(inside) - last
        return s + Fraction(last + 1, 2)  # @line L11

    def bucket_bound(self) -> int:
        """(L + 1)(floor(log2((W - 1)/L + 1)) + 1), the bound on the number of buckets."""
        cap = self.cap
        r = 0
        while cap * ((1 << (r + 1)) - 1) + 1 <= self.window:
            r += 1
        return (cap + 1) * (r + 1)
