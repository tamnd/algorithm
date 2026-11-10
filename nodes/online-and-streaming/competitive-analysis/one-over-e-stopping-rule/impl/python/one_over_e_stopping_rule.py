# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/one-over-e-stopping-rule/. The authors are listed in prov/19FPEC.jsonl.

import math
from fractions import Fraction
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def cutoff(n: int) -> int:
    """Return floor(n / e), the number of candidates that the rule only observes.

    n / e is never an integer for n >= 1, and a double gives the right floor
    for every n below 2**50.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return math.floor(n / math.e)


def one_over_e_stopping_rule(candidates: list[T], r: int | None = None) -> int | None:
    """Return the 0-based position of the hired candidate, or None.

    The rule observes the first r candidates (r = floor(n/e) by default) and
    hires the first later candidate that is strictly better than each earlier
    one. It returns None when no such candidate comes. The decision about
    position i uses only the candidates at positions 0 to i.
    Cost: n - 1 comparisons at most, O(1) extra space.
    """
    n = len(candidates)
    if r is None:
        r = cutoff(n)  # @line L1
    if not 0 <= r <= n:
        raise ValueError("r must be between 0 and n")
    best: T | None = None  # @line L2
    for i in range(r):  # @line L3
        if best is None or best < candidates[i]:
            best = candidates[i]
    for i in range(r, n):  # @line L4
        if best is None or best < candidates[i]:  # @line L5
            return i
    return None  # @line L6


def success_probability(n: int, r: int) -> Fraction:
    """Exact probability that the cutoff rule with cutoff r hires the best of n.

    The order is uniformly random and the values are distinct. For r = 0 the
    rule hires the first candidate, so the probability is 1/n. For r >= 1 it is
    (r/n) * sum_{j=r+1}^{n} 1/(j-1). Cost: O(n) fraction additions.
    """
    if n < 1 or not 0 <= r < n:
        raise ValueError("need n >= 1 and 0 <= r < n")
    if r == 0:
        return Fraction(1, n)
    return Fraction(r, n) * sum((Fraction(1, j - 1) for j in range(r + 1, n + 1)), Fraction(0))


def optimal_cutoff(n: int) -> tuple[int, Fraction]:
    """Return the least optimal cutoff r* and its success probability.

    For n >= 3, r* is the least r >= 1 with 1/(r+1) + ... + 1/(n-1) <= 1.
    For n <= 2 every cutoff gives the same value, and r* = 0.
    Cost: O(n) fraction operations.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    if n <= 2:
        return 0, Fraction(1, n)
    tail = Fraction(0)  # tail = 1/(r+1) + ... + 1/(n-1)
    r = n - 1
    while r >= 2 and tail + Fraction(1, r) <= 1:
        tail += Fraction(1, r)
        r -= 1
    return r, success_probability(n, r)
