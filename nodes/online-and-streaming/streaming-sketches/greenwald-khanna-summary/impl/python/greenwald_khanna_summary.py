# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greenwald-khanna-summary/. The authors are listed in prov/C80D8X.jsonl.
"""Greenwald-Khanna quantile summary, in the form of Assadi, Joshi, Prabhu and Shah.

The summary keeps a sorted list of tuples (v, g, delta, band). The stream is cut
into chunks of l = ceil(1/(2 eps)) items. At the end of chunk t the bands of the
older tuples grow, and tuples are merged into their right neighbour while
g + delta stays at most t. Every rank query is answered within eps * n.

Equal values are kept apart by their arrival number, so the order of the
items is the order of (value, arrival number).
"""

from __future__ import annotations

import bisect
import math
from typing import Any, Optional


class GKSummary:
    """An eps-approximate quantile summary for an insertion-only stream."""

    def __init__(self, eps: float) -> None:
        if not 0 < eps < 1:
            raise ValueError("eps must be in (0, 1)")
        self.eps = eps
        self.ell = math.ceil(1 / (2 * eps))  # items per time step
        self.n = 0
        self.xmin: Optional[Any] = None
        self.keys: list[tuple[Any, int]] = []  # (value, arrival number), sorted
        self.g: list[int] = []
        self.delta: list[int] = []
        self.band: list[int] = []

    def __len__(self) -> int:
        return len(self.keys)

    def insert(self, x: Any) -> None:
        """Add one item of the stream."""
        self.n += 1  # @line L1
        if self.xmin is None or x < self.xmin:
            self.xmin = x
        key = (x, self.n)
        i = bisect.bisect_right(self.keys, key)  # @line L2
        if i == len(self.keys):  # @line L3
            new_delta = 0  # a new maximum has an exact rank
        else:  # @line L4
            new_delta = self.g[i] + self.delta[i] - 1
        self.keys.insert(i, key)
        self.g.insert(i, 1)
        self.delta.insert(i, new_delta)
        self.band.insert(i, 0)
        if self.n % self.ell == 0:  # @line L5
            self._end_of_step(self.n // self.ell)

    def _end_of_step(self, t: int) -> None:
        """Raise the band values, then merge tuples while the cap t allows it."""
        first_new = self.n - self.ell + 1  # arrival number of the first item of step t
        for i, (_, arrival) in enumerate(self.keys):  # @line L6
            if arrival < first_new and t % (1 << self.band[i]) == 0:
                self.band[i] += 1
        changed = True
        while changed:  # @line L7
            changed = False
            i = len(self.keys) - 2
            while i >= 0:
                j = i  # j is the first index of seg(e_i)
                while j > 0 and self.band[j - 1] < self.band[i]:
                    j -= 1
                g_star = sum(self.g[j : i + 1])
                if (
                    self.band[i] <= self.band[i + 1]
                    and g_star + self.g[i + 1] + self.delta[i + 1] <= t
                ):
                    self.g[i + 1] += g_star  # @line L8
                    del self.keys[j : i + 1]
                    del self.g[j : i + 1]
                    del self.delta[j : i + 1]
                    del self.band[j : i + 1]
                    changed = True
                    i = j - 1
                else:
                    i -= 1

    def query(self, r: int) -> Any:
        """Return an item whose rank is within eps * n of r, for 1 <= r <= n."""
        if not 1 <= r <= self.n:
            raise ValueError("rank out of range")
        bound = r + self.eps * self.n
        if r - self.eps * self.n <= 1:  # @line L9
            return self.xmin
        rmin = 0
        for j in range(len(self.keys)):  # @line L10
            rmin += self.g[j]
            if rmin + self.delta[j] > bound:
                return self.keys[j - 1][0]  # @line L12
        return self.keys[-1][0]  # @line L11

    def rank_bounds(self) -> list[tuple[Any, int, int, int]]:
        """Return (value, arrival number, rmin, rmax) for each tuple."""
        out = []
        rmin = 0
        for key, g, d in zip(self.keys, self.g, self.delta):
            rmin += g
            out.append((key[0], key[1], rmin, rmin + d))
        return out

    def check_invariant(self) -> None:
        """Check the structural invariants of the summary."""
        assert self.keys == sorted(self.keys)
        assert len(self.keys) == len(self.g) == len(self.delta) == len(self.band)
        assert sum(self.g) == self.n
        cap = max(1, self.n // self.ell)
        for g, d in zip(self.g, self.delta):
            assert g >= 1 and d >= 0
            assert g + d <= cap
        if self.keys:
            assert self.delta[-1] == 0
            assert cap <= 2 * self.eps * self.n or cap == 1


def gk_quantiles(stream: list[Any], eps: float, ranks: list[int]) -> list[Any]:
    """Build a summary of the stream and answer each rank query."""
    s = GKSummary(eps)
    for x in stream:
        s.insert(x)
    return [s.query(r) for r in ranks]
