# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/theil-sen-estimator/. The authors are listed in prov/VFQ6SW.jsonl.

import random
from fractions import Fraction
from math import comb
from statistics import median

import pytest

from theil_sen_estimator import (
    NEG_INF, POS_INF, breakdown_count, count_at_most, count_between,
    count_less, naive_slopes, select_slope, theil_sen,
)


def F(v):
    return [Fraction(t) for t in v]


def test_page_example() -> None:
    x = [1, 2, 3, 4, 5, 6]
    y = [2, 3, 5, 6, 8, 40]
    slopes = naive_slopes(x, y)
    assert len(slopes) == 15
    b, a = theil_sen(x, y)
    assert b == Fraction(5, 3)
    assert a == Fraction(-1, 6)
    # The count of slopes below 3/2 is the inversion count of y - 1.5 x.
    assert count_less(Fraction(3, 2), F(x), F(y)) == 3
    assert count_at_most(Fraction(3, 2), F(x), F(y)) == 7


def test_counts_against_all_slopes() -> None:
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(1, 12)
        x = F(rng.randint(0, 5) for _ in range(n))
        y = F(rng.randint(-5, 5) for _ in range(n))
        slopes = naive_slopes(x, y)
        assert count_between(NEG_INF, POS_INF, x, y) == len(slopes)
        probes = [Fraction(rng.randint(-12, 12), rng.randint(1, 4))] + slopes[:2]
        for s in probes:
            assert count_less(s, x, y) == sum(1 for v in slopes if v < s)
            assert count_at_most(s, x, y) == sum(1 for v in slopes if v <= s)
            lo = s - Fraction(rng.randint(1, 30), 3)
            assert count_between(lo, s, x, y) == sum(1 for v in slopes if lo < v < s)


def test_selection_against_sorting_small() -> None:
    rng = random.Random(12)
    for _ in range(150):
        n = rng.randint(2, 12)
        x = F(rng.randint(0, 5) for _ in range(n))
        y = F(rng.randint(-5, 5) for _ in range(n))
        slopes = naive_slopes(x, y)
        for k in range(1, len(slopes) + 1):
            assert select_slope(x, y, k, random.Random(k)) == slopes[k - 1]


def test_selection_against_sorting_large() -> None:
    # Large enough that the sampling rounds run before the final enumeration.
    rng = random.Random(13)
    n = 400
    x = [rng.randint(0, 10**6) for _ in range(n)]
    y = [rng.randint(0, 10**6) for _ in range(n)]
    slopes = naive_slopes(x, y)
    xs, ys = F(x), F(y)
    for k in (1, 2, len(slopes) // 3, len(slopes) // 2, len(slopes) - 1, len(slopes)):
        assert select_slope(xs, ys, k, random.Random(k)) == slopes[k - 1]


def test_theil_sen_against_naive_median() -> None:
    rng = random.Random(14)
    for _ in range(200):
        n = rng.randint(2, 15)
        x = [rng.randint(0, 6) for _ in range(n)]
        y = [rng.randint(-9, 9) for _ in range(n)]
        slopes = naive_slopes(x, y)
        if not slopes:
            with pytest.raises(ValueError):
                theil_sen(x, y)
            continue
        b, a = theil_sen(x, y)
        assert b == median(slopes)
        assert a == median([Fraction(yi) - b * xi for xi, yi in zip(x, y)])


def test_exact_line_and_equivariance() -> None:
    x = [0, 1, 3, 4, 7, 9]
    y = [Fraction(5) - Fraction(2, 3) * v for v in x]
    assert theil_sen(x, y) == (Fraction(-2, 3), 5)
    rng = random.Random(15)
    x = [rng.randint(0, 50) for _ in range(30)]
    y = [rng.randint(0, 50) for _ in range(30)]
    b, a = theil_sen(x, y)
    # Adding the line 3 + 2x to y adds 2 to the slope and 3 to the intercept.
    b2, a2 = theil_sen(x, [yi + 3 + 2 * xi for xi, yi in zip(x, y)])
    assert (b2, a2) == (b + 2, a + 3)


def test_breakdown_count() -> None:
    assert [breakdown_count(n) for n in (5, 10, 100, 1000)] == [2, 3, 30, 293]
    for n in range(3, 200):
        m = breakdown_count(n)
        assert 2 * comb(n - m, 2) <= comb(n, 2) < 2 * comb(n - m + 1, 2)


def test_breakdown_by_adversary() -> None:
    rng = random.Random(16)
    n = 10
    m_star = breakdown_count(n)  # 3
    xc = list(range(n))
    yc = [rng.randint(0, 5) for _ in range(n)]
    clean = naive_slopes(xc, yc)
    # m* - 1 bad points of any kind leave the slope inside the clean range.
    for _ in range(200):
        x, y = list(xc), list(yc)
        for i in rng.sample(range(n), m_star - 1):
            x[i] = rng.randint(-10**6, 10**6)
            y[i] = rng.randint(-10**6, 10**6)
        b, _ = theil_sen(x, y)
        assert clean[0] <= b <= clean[-1]
    # m* bad points far to the right on a steep parabola carry it away.
    x, y = list(xc), list(yc)
    last = None
    for t in (10, 10**3, 10**5):
        for j in range(m_star):
            x[j] = n + j
            y[j] = (j + 1) ** 2 * t
        b, _ = theil_sen(x, y)
        assert last is None or b > 50 * last
        last = b
