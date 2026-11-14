# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mann-whitney-u-test/. The authors are listed in prov/9WF4CP.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from mann_whitney_u_test import (
    doubled_midranks, mann_whitney, mann_whitney_normal, null_counts_2u, tie_sizes, u_statistic,
)

X = [1.1, 3.4, 2.9, 5.0]
Y = [0.8, 2.0, 1.9, 2.9, 1.2]


def pair_count(x: list[float], y: list[float]) -> Fraction:
    return sum((Fraction(1) if a > b else Fraction(1, 2) if a == b else Fraction(0))
               for a in x for b in y)


def brute_force(x: list[float], y: list[float]) -> tuple[Fraction, Fraction, Fraction]:
    """U and its tails by listing every choice of m of the pooled values as the first sample."""
    pooled = list(x) + list(y)
    m, big_n = len(x), len(pooled)
    u = pair_count(x, y)
    upper = lower = total = 0
    for idx in itertools.combinations(range(big_n), m):
        chosen = set(idx)
        a = [pooled[i] for i in idx]
        b = [pooled[i] for i in range(big_n) if i not in chosen]
        v = pair_count(a, b)
        total += 1
        upper += v >= u
        lower += v <= u
    return u, Fraction(upper, total), Fraction(lower, total)


def test_page_examples() -> None:
    assert u_statistic(X, Y) == 15.5
    assert mann_whitney(X, Y, exact=True) == (15.5, Fraction(13, 63))
    assert mann_whitney(X, Y, "greater", exact=True) == (15.5, Fraction(13, 126))
    z, p = mann_whitney_normal(X, Y)
    assert (round(z, 4), round(p, 5)) == (1.2299, 0.21874)
    z, p = mann_whitney_normal(X, Y, correction=False)
    assert (round(z, 4), round(p, 5)) == (1.3529, 0.17610)
    assert sorted(null_counts_2u([2, 4, 6, 8, 10], 2).items()) == [
        (0, 1), (2, 1), (4, 2), (6, 2), (8, 2), (10, 1), (12, 1)]


def test_u_is_the_pair_count() -> None:
    rng = random.Random(1)
    for _ in range(300):
        x = [rng.randint(0, 5) for _ in range(rng.randint(1, 8))]
        y = [rng.randint(0, 5) for _ in range(rng.randint(1, 8))]
        assert Fraction(u_statistic(x, y)) == pair_count(x, y)
        assert u_statistic(x, y) + u_statistic(y, x) == len(x) * len(y)


def test_against_all_labelings() -> None:
    rng = random.Random(2)
    for _ in range(120):
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        x = [rng.randint(0, 4) for _ in range(m)]  # small range: many ties
        y = [rng.randint(0, 4) for _ in range(n)]
        u, upper, lower = brute_force(x, y)
        assert mann_whitney(x, y, "greater", exact=True) == (float(u), upper)
        assert mann_whitney(x, y, "less", exact=True)[1] == lower
        assert mann_whitney(x, y, exact=True)[1] == min(Fraction(1), 2 * min(upper, lower))


def test_counts_both_orientations() -> None:
    # The table counts subsets of size min(m, n); both choices must give the same law of 2U.
    rng = random.Random(4)
    for _ in range(40):
        m, n = rng.randint(1, 7), rng.randint(1, 7)
        values = [rng.randint(0, 6) for _ in range(m + n)]
        r2 = doubled_midranks(values)
        a = null_counts_2u(r2, m)
        b = null_counts_2u(r2, n)  # the law of 2U for the other sample, mirrored about mn
        assert sum(a.values()) == math.comb(m + n, m)
        assert a == {2 * m * n - v: c for v, c in b.items()}
        distinct = null_counts_2u(list(range(2, 2 * (m + n) + 1, 2)), m)
        assert distinct == {2 * m * n - v: c for v, c in distinct.items()}  # symmetric, no ties


def test_ties_can_break_symmetry() -> None:
    # Ranks 1, 2.5, 2.5, 4, 5 with m = 2: the conditional law of U is not symmetric about mn/2.
    a = null_counts_2u(doubled_midranks([1, 2, 2, 3, 4]), 2)
    assert a != {12 - v: c for v, c in a.items()}


def test_null_mean_and_variance() -> None:
    for values, m in (([1, 2, 3, 4, 5, 6, 7, 8, 9], 4), ([1, 1, 2, 3, 3, 3, 4, 5, 5, 6], 4)):
        big_n = len(values)
        n = big_n - m
        counts = null_counts_2u(doubled_midranks(values), m)
        total = math.comb(big_n, m)
        mean = sum(Fraction(v, 2) * c for v, c in counts.items()) / total
        var = sum(Fraction(v, 2) ** 2 * c for v, c in counts.items()) / total - mean**2
        ties = sum(t**3 - t for t in tie_sizes(values))
        assert mean == Fraction(m * n, 2)
        assert var == Fraction(m * n, 12) * ((big_n + 1) - Fraction(ties, big_n * (big_n - 1)))


def test_size_monte_carlo() -> None:
    rng = random.Random(6)
    m, n, r, alpha = 8, 10, 1500, 0.05
    hits = 0
    for _ in range(r):
        x = [rng.gauss(0.0, 1.0) for _ in range(m)]
        y = [rng.gauss(0.0, 1.0) for _ in range(n)]
        hits += mann_whitney(x, y)[1] <= alpha
    assert hits / r <= alpha + 4 * math.sqrt(alpha * (1 - alpha) / r)


def test_equal_medians_are_not_enough() -> None:
    # X = E - ln 2 and Y = -(E - ln 2) both have median 0, but P(X > Y) = 0.597.
    rng = random.Random(21)
    m = n = 50
    r, alpha = 300, 0.05
    hits = 0
    for _ in range(r):
        x = [rng.expovariate(1.0) - math.log(2.0) for _ in range(m)]
        y = [math.log(2.0) - rng.expovariate(1.0) for _ in range(n)]
        hits += mann_whitney_normal(x, y)[1] <= alpha
    assert hits / r > alpha + 4 * math.sqrt(alpha * (1 - alpha) / r)


def test_edges() -> None:
    with pytest.raises(ValueError):
        mann_whitney([], [1.0])
    with pytest.raises(ValueError):
        mann_whitney([1.0], [2.0], "both")
    assert mann_whitney([1.0], [2.0], exact=True) == (0.0, 1)
    assert mann_whitney([2.0, 3.0], [0.0, 1.0], "greater", exact=True) == (4.0, Fraction(1, 6))
