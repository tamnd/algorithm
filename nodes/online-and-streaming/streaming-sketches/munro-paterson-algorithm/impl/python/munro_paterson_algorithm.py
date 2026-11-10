# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/munro-paterson-algorithm/. The authors are listed in prov/T3177E.jsonl.
"""Exact selection in a few passes over a read-only stream (Munro and Paterson, 1980).

Each pass keeps two filters lo and hi with the answer between them. The items
between the filters are cut into blocks of s items. A sorted block is a sample
at level 0. Two samples at level i are thinned (only the 2nd, 4th, ... smallest
items stay) and merged into one sample at level i + 1, so a sample always has
s items. The final sample at level r gives new filters with at most
(2r - 1) 2^r + 2 items between them, the filters included. When the next
population is small enough, one last pass stores it and selects directly.
"""

from __future__ import annotations

import heapq
from typing import Any, Callable, Iterable

# A key is (0, value, position) for a real item and (1, 0, j) for a pad.
# Pads are larger than every real item, and all keys are distinct.
Key = tuple


def thin(sample: list) -> list:
    """Keep the 2nd, 4th, 6th, ... smallest items."""
    return sample[1::2]


class SampleBuilder:
    """Merge-and-thin samples for one pass, with at most one waiting half per level."""

    def __init__(self, s: int) -> None:
        self.s = s
        self.block: list = []
        self.waiting: list = []  # waiting[i] is a thinned level-i sample or None
        self.blocks = 0
        self.pads = 0
        self.peak = 0  # the largest number of keys held at one time

    def held(self) -> int:
        return len(self.block) + sum(len(w) for w in self.waiting if w is not None)

    def add(self, key: Key) -> None:
        if len(self.block) == self.s:
            sample, self.block = sorted(self.block), []
            self._carry(sample, last=False)
        self.block.append(key)  # @line L11
        self.peak = max(self.peak, self.held())

    def _carry(self, sample: list, last: bool) -> tuple[list, int]:
        """Add one level-0 sample and merge upward, as in a binary counter."""
        self.blocks += 1
        level = 0
        while level < len(self.waiting) and self.waiting[level] is not None:  # @line L12
            sample = list(heapq.merge(self.waiting[level], thin(sample)))
            self.waiting[level] = None
            level += 1
            self.peak = max(self.peak, self.held() + len(sample))
        if not last:
            if level == len(self.waiting):
                self.waiting.append(None)
            self.waiting[level] = thin(sample)  # @line L13
        return sample, level

    def _pad(self) -> Key:
        self.pads += 1
        return (1, 0, self.pads)

    def finish(self) -> tuple[list, int]:
        """Pad with +infinity up to 2^r s items and return the level-r sample and r."""
        if self.blocks == 0 and not self.block:
            self.block.append(self._pad())
        while True:
            while len(self.block) < self.s:  # @line L14
                self.block.append(self._pad())
            last = (self.blocks + 1) & self.blocks == 0
            block, self.block = sorted(self.block), []
            sample, level = self._carry(block, last)
            if last:
                return sample, level


def select(read_pass: Callable[[], Iterable[Any]], k: int, s: int, cap: int | None = None) -> tuple[Any, dict]:
    """Return the k-th smallest item of the stream and statistics of the run.

    read_pass() must return a new iterator over the same stream each time it
    is called; each call is one pass. s is the sample size (even, at least 2).
    The last pass stores the population when its proven bound is at most cap.
    """
    if s < 2 or s % 2:
        raise ValueError("s must be even and at least 2")
    cap = s if cap is None else cap
    lo: Key = (-1, 0, 0)  # @line L1
    hi: Key = (2, 0, 0)
    bound: int | None = None  # a proven bound on the population size
    stats: dict = {"passes": 0, "populations": [], "bounds": [], "peaks": [], "levels": []}
    while True:  # @line L2
        stats["passes"] += 1
        below = 0
        population = 0
        final = bound is not None and bound <= cap  # @line L3
        builder = SampleBuilder(s)
        kept: list = []
        for pos, x in enumerate(read_pass()):
            key = (0, x, pos)
            if key < lo:  # @line L4
                below += 1
            elif key <= hi:
                population += 1
                if final:
                    kept.append(key)
                else:
                    builder.add(key)
        stats["populations"].append(population)
        if bound is not None:
            assert population <= bound
        kk = k - below  # @line L5
        if not 1 <= kk <= population:
            raise ValueError("k is out of range")
        if final:
            kept.sort()
            stats["peaks"].append(len(kept))
            return kept[kk - 1][1], stats  # @line L6
        sample, r = builder.finish()  # @line L7
        stats["peaks"].append(builder.peak)
        stats["levels"].append(r)
        u = (kk - 1) // (1 << r) - r + 1  # @line L8
        v = -(-kk // (1 << r))
        if u >= 1:  # @line L9
            lo = sample[u - 1]
        if sample[v - 1][0] == 0:
            hi = sample[v - 1]
        if lo == hi:
            return lo[1], stats
        bound = min((2 * r - 1) * (1 << r) + 2, population)  # @line L10
        stats["bounds"].append(bound)
        if bound > cap and bound == population:
            raise ValueError("no progress: s must be larger than about 4 log2 n")


def build_sample(keys: list, s: int) -> tuple[list, int]:
    """One pass of the sample scheme over a list of distinct keys; returns the sample and r."""
    builder = SampleBuilder(s)
    for key in keys:
        builder.add(key)
    return builder.finish()


def lemma2_bounds(i: int, j: int) -> tuple[int, int]:
    """L_ij and M_ij: the least and most population items below the j-th item of a level-i sample."""
    return j * (1 << i) - 1, (i + j - 1) * (1 << i)
