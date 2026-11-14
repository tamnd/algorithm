# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/repeated-median-regression/. The authors are listed in prov/DYDSMR.jsonl.

import random
from fractions import Fraction

import pytest

from repeated_median_regression import (
    NEG_INF, POS_INF, breakdown_count, naive_repeated_median_slope,
    per_point_between, repeated_median, repeated_median_slope,
)


def F(v):
    return [Fraction(t) for t in v]


def test_page_example() -> None:
    x = [1, 2, 3, 4, 5, 6]
    y = [2, 3, 5, 6, 8, 40]
    assert naive_repeated_median_slope(x, y) == Fraction(3, 2)
    b, a = repeated_median(x, y)
    assert b == Fraction(3, 2)
    assert a == Fraction(1, 2)


def test_per_point_counts_against_brute_force() -> None:
    rng = random.Random(21)
    for _ in range(300):
        n = rng.randint(1, 10)
        x = F(rng.randint(0, 4) for _ in range(n))
        y = F(rng.randint(-4, 4) for _ in range(n))
        lo = Fraction(rng.randint(-10, 10), rng.randint(1, 3))
        hi = lo + Fraction(rng.randint(1, 20), 3)
        for a, b in ((NEG_INF, POS_INF), (NEG_INF, hi), (lo, POS_INF), (lo, hi)):
            got = per_point_between(a, b, x, y)
            for i in range(n):
                want = 0
                for j in range(n):
                    if x[j] == x[i]:
                        continue
                    s = (y[j] - y[i]) / (x[j] - x[i])
                    if (a == NEG_INF or s > a) and (b == POS_INF or s < b):
                        want += 1
                assert got[i] == want


def test_against_naive_small() -> None:
    rng = random.Random(22)
    for t in range(400):
        n = rng.randint(2, 12)
        x = [rng.randint(0, 5) for _ in range(n)]
        y = [rng.randint(-6, 6) for _ in range(n)]
        if len(set(x)) == 1:
            with pytest.raises(ValueError):
                repeated_median_slope(F(x), F(y))
            continue
        want = naive_repeated_median_slope(x, y)
        assert repeated_median_slope(F(x), F(y), random.Random(t)) == want


def test_against_naive_large() -> None:
    rng = random.Random(23)
    n = 200
    x = [rng.randint(0, 10**6) for _ in range(n)]
    y = [rng.randint(0, 10**6) for _ in range(n)]
    want = naive_repeated_median_slope(x, y)
    for seed in range(3):
        assert repeated_median_slope(F(x), F(y), random.Random(seed)) == want


def test_exact_line_and_equivariance() -> None:
    x = [0, 1, 3, 4, 7, 9, 12]
    y = [Fraction(5) - Fraction(2, 3) * v for v in x]
    assert repeated_median(x, y) == (Fraction(-2, 3), 5)
    rng = random.Random(24)
    x = [rng.randint(0, 50) for _ in range(25)]
    y = [rng.randint(0, 50) for _ in range(25)]
    b, a = repeated_median(x, y)
    b2, a2 = repeated_median(x, [yi + 3 + 2 * xi for xi, yi in zip(x, y)])
    assert (b2, a2) == (b + 2, a + 3)


def test_breakdown() -> None:
    rng = random.Random(25)
    for n in (9, 10):
        m_star = breakdown_count(n)
        xc = list(range(n))
        yc = [rng.randint(0, 5) for _ in range(n)]
        lo = min((yc[j] - yc[i]) / (j - i) for i in range(n) for j in range(i + 1, n))
        hi = max((yc[j] - yc[i]) / (j - i) for i in range(n) for j in range(i + 1, n))
        # m* - 1 bad points, of any kind, keep the slope in the clean range.
        for _ in range(100):
            x, y = list(xc), list(yc)
            for i in rng.sample(range(n), m_star - 1):
                x[i] = rng.randint(-10**6, 10**6)
                y[i] = rng.randint(-10**6, 10**6)
            if len(set(x)) < n:
                continue
            assert lo <= naive_repeated_median_slope(x, y) <= hi
        # m* bad points far right on a steep parabola carry it away.
        last = None
        for t in (10, 10**3, 10**5):
            x, y = list(xc), list(yc)
            for j in range(m_star):
                x[j] = n + j
                y[j] = (j + 1) ** 2 * t
            b = repeated_median_slope(F(x), F(y))
            assert b == naive_repeated_median_slope(x, y)
            assert last is None or b > 50 * last
            last = b
