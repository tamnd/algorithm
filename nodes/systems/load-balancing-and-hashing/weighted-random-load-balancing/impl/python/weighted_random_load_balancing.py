# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-random-load-balancing/. The authors are listed in prov/BWGAF8.jsonl.

"""Weighted random load balancing: pick backend i with probability w[i] / W.

WeightedRandom keeps the prefix sums P of the integer weights, draws a uniform
integer r in [0, W) and returns the smallest i with P[i + 1] > r by binary
search. Build: Theta(n); pick: Theta(log n); space: Theta(n).

AliasPicker is Walker's alias method with Vose's construction, for O(1) picks
after Theta(n) preprocessing. Its table uses exact fractions, so the tests can
compute the exact probability of each backend.
"""

import random
from fractions import Fraction
from typing import List, Sequence


class WeightedRandom:
    """Prefix sums and binary search. Precondition: integer weights >= 0 with a positive sum."""

    def __init__(self, weights: Sequence[int]) -> None:
        if any(w < 0 for w in weights) or sum(weights) <= 0:
            raise ValueError("weights must be >= 0 with a positive sum")
        self.p = [0]  # @line L1
        for w in weights:  # @line L2
            self.p.append(self.p[-1] + w)

    def locate(self, r: int) -> int:
        """The smallest i with P[i + 1] > r, for 0 <= r < W."""
        lo, hi = 0, len(self.p) - 2  # @line L4
        while lo < hi:  # @line L5
            mid = (lo + hi) // 2  # @line L6
            if self.p[mid + 1] > r:  # @line L7
                hi = mid
            else:
                lo = mid + 1
        return lo  # @line L8

    def pick(self, rng: random.Random) -> int:
        r = rng.randrange(self.p[-1])  # @line L3
        return self.locate(r)


class AliasPicker:
    """Walker's alias method with Vose's stable O(n) construction."""

    def __init__(self, weights: Sequence[int]) -> None:
        n, total = len(weights), sum(weights)
        if n == 0 or total <= 0 or any(w < 0 for w in weights):
            raise ValueError("weights must be >= 0 with a positive sum")
        scaled = [Fraction(w * n, total) for w in weights]
        self.prob: List[Fraction] = [Fraction(1)] * n
        self.alias = list(range(n))
        small = [i for i, s in enumerate(scaled) if s < 1]
        large = [i for i, s in enumerate(scaled) if s >= 1]
        while small and large:
            s, g = small.pop(), large.pop()
            self.prob[s] = scaled[s]
            self.alias[s] = g
            scaled[g] = scaled[g] + scaled[s] - 1
            (small if scaled[g] < 1 else large).append(g)
        for i in small + large:  # only rounding-free leftovers, each with scaled value 1
            self.prob[i] = Fraction(1)

    def pick(self, rng: random.Random) -> int:
        i = rng.randrange(len(self.prob))
        return i if rng.random() < self.prob[i] else self.alias[i]

    def exact_distribution(self) -> List[Fraction]:
        """The exact probability of each index under the table."""
        n = len(self.prob)
        out = [Fraction(0)] * n
        for i in range(n):
            out[i] += self.prob[i] / n
            out[self.alias[i]] += (1 - self.prob[i]) / n
        return out


def chi_square(counts: Sequence[int], weights: Sequence[int]) -> float:
    """Pearson's statistic of observed counts against the weights (zero weights skipped)."""
    m, total = sum(counts), sum(weights)
    return sum((c - m * w / total) ** 2 / (m * w / total) for c, w in zip(counts, weights) if w > 0)
