# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/huber-m-estimator/. The authors are listed in prov/ASDS28.jsonl.

import random
from fractions import Fraction

import pytest

from huber_m_estimator import (
    estimating_function, exact_median, huber_irls, huber_location, mad_scale, objective,
)


def test_page_example() -> None:
    x = [1, 4, 5, 6, 8, 30]
    k, sigma = Fraction(3, 2), Fraction(2)
    assert huber_location(x, k, sigma) == Fraction(23, 4)
    assert estimating_function(x, Fraction(5), k, sigma) == Fraction(3, 2)
    assert estimating_function(x, Fraction(7), k, sigma) == Fraction(-5, 2)
    assert estimating_function(x, Fraction(23, 4), k, sigma) == 0
    # With the default k = 1.345 and the normalized MAD scale (MAD = 2) the clipping is symmetric.
    assert mad_scale(x) == pytest.approx(2.965204437011204)
    assert huber_location(x) == pytest.approx(5.75, abs=1e-12)


def test_flat_root_set_gives_midpoint() -> None:
    # Lambda = 0 on [1, 9]: no residual is inside (-k sigma, k sigma) there.
    assert huber_location([0, 10], 1, 1) == 5
    assert huber_location([0, 0, 10, 10], Fraction(1), Fraction(1)) == 5


def test_root_is_exact_with_fractions() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 25)
        x = [rng.randint(-50, 50) for _ in range(n)]
        k = Fraction(rng.randint(1, 30), 10)
        sigma = Fraction(rng.randint(1, 40), 7)
        t = huber_location(x, k, sigma)
        assert estimating_function(x, t, k, sigma) == 0


def test_against_fine_grid_of_the_objective() -> None:
    rng = random.Random(2)
    for _ in range(20):
        n = rng.randint(2, 30)
        x = [rng.gauss(0.0, 1.0) for _ in range(n)]
        for _ in range(rng.randint(0, n // 3)):
            x[rng.randrange(n)] = rng.uniform(5.0, 50.0)
        k, sigma = 1.345, mad_scale(x)
        t = huber_location(x, k, sigma)
        lo, hi = min(x), max(x)
        steps = 4000
        h = (hi - lo) / steps
        grid = [lo + i * h for i in range(steps + 1)]
        vals = [objective(x, g, k, sigma) for g in grid]
        j = min(range(len(grid)), key=vals.__getitem__)
        # t is a minimizer: no grid point is lower.
        assert objective(x, t, k, sigma) <= vals[j] + 1e-9
        # If some residual is inside the quadratic zone, the minimizer is unique and the
        # best grid point is one of the two grid points around it.
        if any(abs(v - t) < k * sigma for v in x):
            assert abs(grid[j] - t) <= h * (1 + 1e-9)


def test_irls_agrees() -> None:
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randint(3, 40)
        x = [rng.gauss(10.0, 3.0) for _ in range(n)] + [rng.uniform(100, 1000) for _ in range(n // 5)]
        assert huber_irls(x) == pytest.approx(huber_location(x), abs=1e-8)


def test_limits_mean_and_median() -> None:
    rng = random.Random(4)
    for _ in range(100):
        n = rng.randint(1, 15)
        x = [rng.randint(-30, 30) for _ in range(n)]
        # k sigma larger than the range: every residual is inside, the estimate is the mean.
        assert huber_location(x, Fraction(1000), Fraction(1)) == Fraction(sum(x), n)
        # Distinct values, odd n, tiny k: the estimate is the median.
        y = rng.sample(range(-100, 100), 2 * rng.randint(0, 6) + 1)
        assert huber_location(y, Fraction(1, 1000), Fraction(1)) == exact_median(y)


def test_equivariance() -> None:
    rng = random.Random(5)
    for _ in range(50):
        x = [rng.gauss(0.0, 1.0) for _ in range(rng.randint(3, 20))]
        t = huber_location(x)
        a, b = rng.choice([-3.0, 0.5, 7.0]), rng.uniform(-10, 10)
        assert huber_location([a * v + b for v in x]) == pytest.approx(a * t + b, abs=1e-9)


def test_empirical_breakdown() -> None:
    # Move m points to a far value s. For m < n/2 the estimate stays in
    # [min clean - k R / q, max clean + k R / q] with R the clean range (the page proves this).
    # For m = ceil(n/2) it follows s.
    rng = random.Random(6)
    k = 1.345
    for n in (5, 6, 9, 10, 15):
        clean_all = [rng.uniform(0.0, 10.0) for _ in range(n)]
        for s in (1e6, 1e12):
            for m in range((n + 1) // 2 + 1):
                clean = clean_all[: n - m]
                x = clean + [s] * m
                t = huber_location(x, k)
                if 2 * m < n:
                    r = (max(clean) - min(clean)) / 0.6744897501960817
                    assert min(clean) - k * r - 1e-9 <= t <= max(clean) + k * r + 1e-9
                else:
                    assert t >= s / 4


def test_errors() -> None:
    with pytest.raises(ValueError):
        huber_location([])
    with pytest.raises(ValueError):
        huber_location([1, 2], k=0)
    # Zero MAD: the median is returned.
    assert huber_location([3, 3, 3, 3, 100]) == 3
