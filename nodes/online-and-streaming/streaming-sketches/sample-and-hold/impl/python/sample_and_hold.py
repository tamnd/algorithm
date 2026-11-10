# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sample-and-hold/. The authors are listed in prov/HS0C9K.jsonl.

import random
from collections.abc import Hashable, Iterable
from fractions import Fraction


class SampleAndHold:
    """Sample and hold of Estan and Varghese, for units of traffic.

    Each unit (a byte or a packet) of an item without an entry is sampled
    with probability p; once an item has an entry, every later unit is
    counted. estimate(x) = count + (1 - p)/p is unbiased, with variance at
    most (1 - p)/p^2, and the expected number of entries is at most p * m.
    The probability p may be a Fraction, which keeps the estimates exact.
    """

    def __init__(self, p: float | Fraction, rng: random.Random) -> None:
        if not 0 < p <= 1:
            raise ValueError("p must be in (0, 1]")
        self.p = p
        self.rng = rng
        self.m = 0
        self.count: dict[Hashable, int] = {}

    def update(self, x: Hashable) -> None:
        """Process one unit of item x."""
        self.m += 1
        if x in self.count:  # @line L1
            self.count[x] += 1  # @line L1
        elif self.rng.random() < self.p:  # @line L2
            self.count[x] = 1  # @line L2

    def extend(self, stream: Iterable[Hashable]) -> None:
        for x in stream:
            self.update(x)

    def estimate(self, x: Hashable) -> float | Fraction:
        """An unbiased estimate of f_x."""
        if x in self.count:  # @line L3
            return self.count[x] + (1 - self.p) / self.p  # @line L3
        return 0  # @line L4

    def raw(self, x: Hashable) -> int:
        """The held count, a lower bound of f_x."""
        return self.count.get(x, 0)

    def large(self, threshold: float) -> list[Hashable]:
        """The held items whose estimate is at least the threshold."""
        return [x for x in self.count if self.estimate(x) >= threshold]

    def __len__(self) -> int:
        return len(self.count)
