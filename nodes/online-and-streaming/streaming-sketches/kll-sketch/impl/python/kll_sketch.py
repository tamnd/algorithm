# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kll-sketch/. The authors are listed in prov/1FW1M3.jsonl.
"""The KLL quantile sketch of Karnin, Lang and Liberty, in its basic form.

Level h holds items of weight 2^h. With H levels, level h has capacity
k_h = max(2, ceil(k c^(H - 1 - h))). A full level is compacted: it is sorted,
a fair coin picks the odd or the even positions, those items move up one level
with twice the weight, and the others are dropped. An odd item out stays.
"""

from __future__ import annotations

import bisect
import math
import random
from typing import Any


class KLLSketch:
    """A randomized, mergeable quantile sketch for an insertion-only stream."""

    def __init__(self, k: int, rng: random.Random, c: float = 2 / 3) -> None:
        if k < 2 or not 0.5 < c < 1:
            raise ValueError("need k >= 2 and 1/2 < c < 1")
        self.k = k
        self.c = c
        self.rng = rng
        self.n = 0
        self.levels: list[list[Any]] = [[]]
        self.compactions: list[int] = [0]  # m_h, the number of compactions of level h

    def capacity(self, h: int) -> int:
        """k_h for the current number of levels."""
        depth = len(self.levels) - 1 - h
        return max(2, math.ceil(self.k * self.c**depth))

    def size(self) -> int:
        """Number of stored items."""
        return sum(len(b) for b in self.levels)

    def insert(self, x: Any) -> None:
        """Add one item of the stream."""
        self.levels[0].append(x)  # @line L1
        self.n += 1
        self._compress()

    def _compress(self) -> None:
        while True:
            full = [h for h in range(len(self.levels)) if len(self.levels[h]) >= self.capacity(h)]  # @line L2
            if not full:
                return
            self._compact(full[0])  # @line L3

    def _compact(self, h: int) -> None:
        buf = sorted(self.levels[h])  # @line L4
        keep = [buf.pop()] if len(buf) % 2 else []
        b = self.rng.getrandbits(1)  # @line L5
        if h == len(self.levels) - 1:  # @line L6
            self.levels.append([])
            self.compactions.append(0)
        self.levels[h + 1].extend(buf[b::2])  # @line L7
        self.levels[h] = keep  # @line L8
        self.compactions[h] += 1

    def merge(self, other: "KLLSketch") -> None:
        """Add the items of another sketch with the same k and c, then compress."""
        while len(self.levels) < len(other.levels):
            self.levels.append([])
            self.compactions.append(0)
        for h, buf in enumerate(other.levels):
            self.levels[h].extend(buf)
            self.compactions[h] += other.compactions[h]
        self.n += other.n
        self._compress()

    def rank(self, x: Any) -> int:
        """Estimate of the number of items <= x."""
        total = 0
        for h, buf in enumerate(self.levels):  # @line L9
            total += (1 << h) * sum(1 for y in buf if y <= x)
        return total

    def query(self, r: int) -> Any:
        """Return the stored item at which the weighted rank first reaches r."""
        if not 1 <= r <= self.n:
            raise ValueError("rank out of range")
        items = sorted((y, 1 << h) for h, buf in enumerate(self.levels) for y in buf)  # @line L10
        s = 0
        for y, w in items:
            s += w
            if s >= r:
                return y
        return items[-1][0]

    def variance_bound(self) -> int:
        """V = sum over levels of m_h 4^h, the Azuma variance proxy of the rank error."""
        return sum(m * (1 << (2 * h)) for h, m in enumerate(self.compactions))

    def check_invariant(self) -> None:
        """Weights add up to n and no level is full."""
        assert sum(len(b) << h for h, b in enumerate(self.levels)) == self.n
        for h, b in enumerate(self.levels):
            assert len(b) < self.capacity(h)
        assert self.size() <= sum(self.capacity(h) for h in range(len(self.levels)))


def k_for(eps: float, delta: float) -> int:
    """A k for which Theorem 1 of the proof gives error eps n with probability 1 - delta."""
    return math.ceil(math.sqrt(32 * math.log(2 / delta)) / eps)
