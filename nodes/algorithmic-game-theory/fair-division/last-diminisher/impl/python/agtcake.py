# SPDX-License-Identifier: MIT
# Shared helper of the algorithmic game theory pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Piecewise-constant cake valuations and a Robertson-Webb query oracle.

The cake is the interval [0, 1]. A valuation is a list of k nonnegative
Fraction densities d[0], ..., d[k - 1]. Density d[j] holds on the segment
[j/k, (j + 1)/k], so that segment has value d[j] / k. A valuation is
normalized when the value of the whole cake is 1, that is, sum(d) = k.

All numbers are Fraction, so every value and every cut point is exact.
This module holds no cake cutting protocol.
"""

from fractions import Fraction
from random import Random
from typing import Optional, Sequence

Valuation = list[Fraction]
Interval = tuple[Fraction, Fraction]

ZERO = Fraction(0)
ONE = Fraction(1)


def normalize(dens: Sequence) -> Valuation:
    """Scale nonnegative densities so that the whole cake has value 1."""
    d = [Fraction(x) for x in dens]
    if not d:
        raise ValueError("a valuation needs at least one segment")
    if any(x < 0 for x in d):
        raise ValueError("densities must be nonnegative")
    total = sum(d)
    if total == 0:
        raise ValueError("densities must not all be zero")
    k = len(d)
    return [x * k / total for x in d]


def _check_point(x: Fraction) -> None:
    if x < 0 or x > 1:
        raise ValueError("a point of the cake must be in [0, 1]")


def value(v: Valuation, a, b) -> Fraction:
    """Return the value of the interval [a, b] under v. Needs 0 <= a <= b <= 1."""
    a, b = Fraction(a), Fraction(b)
    _check_point(a)
    _check_point(b)
    if a > b:
        raise ValueError("value(v, a, b) needs a <= b")
    k = len(v)
    total = ZERO
    j = min(int(a * k), k - 1)
    while j < k:
        lo = Fraction(j, k)
        if lo >= b:
            break
        hi = Fraction(j + 1, k)
        left = a if a > lo else lo
        right = b if b < hi else hi
        if right > left:
            total += v[j] * (right - left)
        j += 1
    return total


def cut(v: Valuation, a, t) -> Optional[Fraction]:
    """Return the least x >= a with value(v, a, x) = t, or None if there is none."""
    a, t = Fraction(a), Fraction(t)
    _check_point(a)
    if t < 0:
        raise ValueError("cut(v, a, t) needs t >= 0")
    if t == 0:
        return a
    k = len(v)
    pos = a
    rest = t
    j = min(int(a * k), k - 1)
    while j < k:
        hi = Fraction(j + 1, k)
        d = v[j]
        if d > 0 and hi > pos:
            here = d * (hi - pos)
            if rest <= here:
                return pos + rest / d
            rest -= here
        if hi > pos:
            pos = hi
        j += 1
    return None


def piece_value(v: Valuation, piece: Sequence[Interval]) -> Fraction:
    """Return the value of a piece, given as a list of intervals (a, b)."""
    return sum((value(v, a, b) for a, b in piece), ZERO)


def random_valuation(rng: Random, k: int, hi: int) -> Valuation:
    """Return a normalized valuation with k segments and integer densities in 0..hi."""
    if k < 1 or hi < 1:
        raise ValueError("random_valuation needs k >= 1 and hi >= 1")
    while True:
        dens = [rng.randint(0, hi) for _ in range(k)]
        if any(dens):
            return normalize(dens)


class Oracle:
    """Answer Robertson-Webb queries for a list of valuations and count them.

    eval_query(i, a, b) returns V_i([a, b]). cut_query(i, a, t) returns the
    least x with V_i([a, x]) = t, or None. The lists evals and cuts hold the
    number of queries of each kind for each agent.
    """

    def __init__(self, valuations: Sequence[Valuation]) -> None:
        self.valuations = [list(v) for v in valuations]
        n = len(self.valuations)
        self.evals = [0] * n
        self.cuts = [0] * n

    @property
    def n(self) -> int:
        return len(self.valuations)

    def eval_query(self, i: int, a, b) -> Fraction:
        self.evals[i] += 1
        return value(self.valuations[i], a, b)

    def cut_query(self, i: int, a, t) -> Optional[Fraction]:
        self.cuts[i] += 1
        return cut(self.valuations[i], a, t)

    def total_evals(self) -> int:
        return sum(self.evals)

    def total_cuts(self) -> int:
        return sum(self.cuts)

    def total(self) -> int:
        return self.total_evals() + self.total_cuts()
