# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-decay/. The authors are listed in prov/PZMNKF.jsonl.
"""Exponentially decayed count, sum and average with O(1) state, plus merge."""

import math
from typing import Callable


def exp_factor(lam: float) -> Callable:
    """The decay factor e^(-lam * age) for real ages."""
    return lambda age: math.exp(-lam * age)


def base_factor(beta) -> Callable:
    """The factor beta^age for integer ages; with a Fraction beta all results are exact."""
    return lambda age: beta ** age


class DecayedAggregate:
    """Keeps C = sum of w_i and S = sum of w_i x_i with w_i = factor(t - t_i), scaled to time `at`."""

    def __init__(self, factor: Callable, start=0) -> None:
        self.factor = factor
        self.at = start
        self.c = 0
        self.s = 0

    def advance(self, t) -> None:
        """Rescale the state to the later time t."""
        if t < self.at:
            raise ValueError("time must not go back")
        if t != self.at:
            f = self.factor(t - self.at)
            self.c *= f
            self.s *= f
            self.at = t

    def add(self, t, x=1) -> None:
        self.advance(t)
        self.c += 1
        self.s += x

    def count(self, t):
        return self.c * self.factor(t - self.at)

    def total(self, t):
        return self.s * self.factor(t - self.at)

    def average(self):
        """S/C; it does not depend on the query time."""
        return self.s / self.c

    def merge(self, other: "DecayedAggregate") -> "DecayedAggregate":
        """Combine two aggregates with the same factor, for disjoint sets of items."""
        out = DecayedAggregate(self.factor, max(self.at, other.at))
        for a in (self, other):
            f = a.factor(out.at - a.at)
            out.c += a.c * f
            out.s += a.s * f
        return out
