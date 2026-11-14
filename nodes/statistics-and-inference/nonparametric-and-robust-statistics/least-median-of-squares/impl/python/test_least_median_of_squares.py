# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-median-of-squares/. The authors are listed in prov/0GC0T5.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from least_median_of_squares import (
    best_intercept, coverage, hth_squared_residual, lms_line, lms_random,
)


def chebyshev_error(pts):
    """Minimax error of the best line through pts (distinct x), by the
    de la Vallee Poussin rule: the largest levelled error over all triples."""
    if len(pts) < 3:
        return Fraction(0)
    best = Fraction(0)
    for (xa, ya), (xb, yb), (xc, yc) in combinations(sorted(pts), 3):
        on_line = ya + (yc - ya) * (xb - xa) / (xc - xa)
        best = max(best, abs(yb - on_line) / 2)
    return best


def brute_force_objective(x, y):
    """min over h-subsets of the squared Chebyshev error of the subset."""
    pts = [(Fraction(a), Fraction(b)) for a, b in zip(x, y)]
    h = coverage(len(pts))
    return min(chebyshev_error(sub) for sub in combinations(pts, h)) ** 2


def test_page_example() -> None:
    x = [1, 2, 3, 4, 5, 6, 7]
    y = [2, 4, 5, 8, 30, 33, 1]
    s, a, obj = lms_line(x, y)
    assert (s, a, obj) == (2, Fraction(-1, 2), Fraction(1, 4))
    assert hth_squared_residual(s, a, x, y) == obj
    assert obj == brute_force_objective(x, y)


def test_against_subset_brute_force() -> None:
    rng = random.Random(31)
    for _ in range(120):
        n = rng.randint(4, 9)
        x = rng.sample(range(-8, 9), n)
        y = [rng.randint(-8, 8) for _ in range(n)]
        s, a, obj = lms_line(x, y)
        assert obj == brute_force_objective(x, y)
        assert hth_squared_residual(s, a, x, y) == obj


def test_fixed_slope_intercept_is_optimal() -> None:
    rng = random.Random(32)
    for _ in range(200):
        n = rng.randint(2, 9)
        x = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        y = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        s = Fraction(rng.randint(-6, 6), rng.randint(1, 3))
        h = coverage(n)
        a, r = best_intercept(s, x, y, h)
        assert hth_squared_residual(s, a, x, y) == r * r
        # No other intercept from a fine grid does better.
        for t in range(-60, 61):
            assert hth_squared_residual(s, Fraction(t, 4), x, y) >= r * r


def test_ties_in_x() -> None:
    rng = random.Random(33)
    for _ in range(100):
        n = rng.randint(3, 8)
        x = [rng.randint(0, 3) for _ in range(n)]
        y = [rng.randint(-5, 5) for _ in range(n)]
        s, a, obj = lms_line(x, y)
        # Compare with every line through two points and every slope on a grid.
        for t in range(-40, 41):
            sl = Fraction(t, 4)
            ai, r = best_intercept(sl, [Fraction(v) for v in x], [Fraction(v) for v in y], coverage(n))
            assert obj <= r * r


def test_exact_fit_and_outliers() -> None:
    # 6 of 10 points on y = 3 - 2x, the rest anywhere: LMS finds the line.
    x = list(range(10))
    y = [3 - 2 * v for v in x]
    for i, v in zip((1, 4, 6, 9), (100, -50, 77, 0)):
        y[i] = v
    assert lms_line(x, y) == (-2, 3, 0)


def test_random_pairs_never_beat_exact() -> None:
    rng = random.Random(34)
    for _ in range(40):
        n = rng.randint(5, 14)
        x = [rng.randint(0, 20) for _ in range(n)]
        y = [rng.randint(0, 20) for _ in range(n)]
        if len(set(x)) == 1:
            continue
        exact = lms_line(x, y)[2]
        approx = lms_random(x, y, 30, random.Random(n))[2]
        assert approx >= exact
        # With many draws every pair is seen, and the answer is exact.
        assert lms_random(x, y, 3000, random.Random(n))[2] == exact
