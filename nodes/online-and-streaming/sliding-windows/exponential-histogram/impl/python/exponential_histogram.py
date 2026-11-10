# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-histogram/. The authors are listed in prov/PRB8V8.jsonl.
"""The exponential histogram for the sum of the last W integers in {0, ..., R}.

An item of value v counts as v units with the timestamp of the item. Buckets
hold 2^j consecutive units; level j keeps the timestamps of its buckets,
newest at the left. With L = ceil(k/2), each level below the largest has L or
L + 1 buckets, and the largest has 1 to L + 1.
"""

from collections import deque
from fractions import Fraction
from typing import Deque, List, Tuple


class ExponentialHistogram:
    """Sum over a count-based window of W items, with relative error less than 1/k."""

    def __init__(self, window: int, k: int, max_value: int) -> None:
        if window < 1 or k < 1 or max_value < 0:
            raise ValueError("need window >= 1, k >= 1 and max_value >= 0")
        self.window = window
        self.k = k
        self.max_value = max_value
        self.cap = (k + 1) // 2
        self.levels: List[Deque[int]] = []
        self.t = 0
        self.total = 0
        self.merges = 0

    def _expire(self) -> None:
        while self.levels and self.levels[-1][-1] <= self.t - self.window:  # @line L2
            top = len(self.levels) - 1
            self.levels[top].pop()
            self.total -= 1 << top
            if not self.levels[top]:
                self.levels.pop()

    def _add_unit(self) -> None:
        if not self.levels:
            self.levels.append(deque())
        self.levels[0].appendleft(self.t)  # @line L4
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

    def update(self, value: int) -> None:
        """Read one item of value 0 <= value <= R (lines L1 to L8)."""
        if not 0 <= value <= self.max_value:
            raise ValueError("value out of range")
        self.t += 1  # @line L1
        self._expire()
        for _ in range(value):  # @line L3
            self._add_unit()

    def buckets(self) -> List[Tuple[int, int]]:
        out = []
        for j, lev in enumerate(self.levels):
            out.extend((ts, 1 << j) for ts in lev)
        return out

    def query(self, w: int = 0) -> Fraction:
        """Estimate the sum of the last w items, 1 <= w <= W (default W); lines L9 to L11."""
        if w == 0:
            w = self.window
        if not 1 <= w <= self.window:
            raise ValueError("w must be in 1..W")
        inside = [size for ts, size in self.buckets() if ts > self.t - w]  # @line L9
        if not inside:
            return Fraction(0)
        last = inside[-1]  # @line L10
        return sum(inside) - last + Fraction(last + 1, 2)  # @line L11

    def bucket_bound(self) -> int:
        """(L + 1)(floor(log2((W R - 1)/L + 1)) + 1), the bound on the number of buckets."""
        cap, most = self.cap, self.window * self.max_value
        if most == 0:
            return 0
        r = 0
        while cap * ((1 << (r + 1)) - 1) + 1 <= most:
            r += 1
        return (cap + 1) * (r + 1)
