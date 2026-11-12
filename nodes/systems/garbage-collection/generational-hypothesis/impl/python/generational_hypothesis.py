# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generational-hypothesis/. The authors are listed in prov/GHBQBX.jsonl.

"""A lifetime model for the generational hypothesis.

Time is counted in allocations: each object has size one, and the clock is
the number of objects allocated so far. An object with lifetime L >= 1 that is
allocated at clock b is live at clock t exactly when t - b < L. A nursery of
n objects holds the objects of ages 0 .. n - 1 when it is collected, and a
copying collection of the nursery costs the number of survivors.
"""

import random
from fractions import Fraction
from typing import Callable

Survival = Callable[[int], Fraction]


def geometric_survival(mean: int, exact: bool = True) -> Survival:
    """S(a) = P(L > a) for a geometric lifetime on 1, 2, ... with the given mean.

    With exact=False the values are floats, which keeps large ages fast.
    """
    if mean < 1:
        raise ValueError("the mean lifetime must be at least 1")
    q = 1 - Fraction(1, mean) if exact else 1.0 - 1.0 / mean
    return lambda a: q ** a


def mixture_survival(parts: list[tuple[Fraction, Survival]]) -> Survival:
    """S(a) of a mixture: a list of (weight, survival function), weights sum to 1."""
    if sum(w for w, _ in parts) != 1:
        raise ValueError("the weights must sum to 1")
    return lambda a: sum(w * s(a) for w, s in parts)


def finite_survival(dist: dict[int, Fraction]) -> Survival:
    """S(a) of a lifetime with finite support: dist maps a lifetime L >= 1 to P(L)."""
    return lambda a: sum((p for life, p in dist.items() if life > a), Fraction(0))


def expected_survivors(s: Survival, n: int) -> Fraction:
    """Expected survivors of a nursery of n objects: the sum of S(a) for a < n.

    Cost: n evaluations of S.
    """
    return sum((s(a) for a in range(n)), Fraction(0))


def survivor_fraction(s: Survival, n: int) -> Fraction:
    """Expected fraction of a nursery of n objects that a collection must copy."""
    return expected_survivors(s, n) / n


def hazard(s: Survival, a: int) -> Fraction:
    """P(L = a + 1 | L > a): the chance that an object of age a dies at the next step."""
    return (s(a) - s(a + 1)) / s(a)


def nursery_survivors(lifetimes: list[int], n: int) -> list[int]:
    """Simulate a nursery of n objects on a trace of lifetimes.

    lifetimes[i] is the lifetime of the object allocated at clock i + 1. The
    nursery is collected each time it holds n objects, and every survivor is
    promoted. Return the number of survivors of each collection.
    """
    out = []
    for end in range(n, len(lifetimes) + 1, n):
        t = end
        out.append(sum(1 for b in range(end - n + 1, end + 1) if t - b < lifetimes[b - 1]))
    return out


def sample_geometric(rng: random.Random, mean: int) -> int:
    """Draw a geometric lifetime on 1, 2, ... with the given mean."""
    p = 1.0 / mean
    life = 1
    while rng.random() >= p:
        life += 1
    return life
