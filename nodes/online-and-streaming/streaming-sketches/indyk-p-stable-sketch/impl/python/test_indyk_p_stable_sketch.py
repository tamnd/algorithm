# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/indyk-p-stable-sketch/. The authors are listed in prov/RGY2FY.jsonl.

import math
import random

import pytest

from indyk_p_stable_sketch import (
    StableSketch,
    estimate_median_abs,
    lower_median,
    rows_for,
)

# The matrix of the worked example: row j, item i (seeded Cauchy draws, rounded).
EXAMPLE_X = [
    [-0.15, 0.19, 4.12],
    [-0.11, 0.02, 0.28],
    [-1.53, 0.04, 0.43],
    [1.31, -3.28, -0.71],
    [-3.42, 1.47, 0.70],
]


def example_column(i: int) -> list[float]:
    return [row[i] for row in EXAMPLE_X]


def norm_p(f: dict, p: float) -> float:
    return sum(abs(v) ** p for v in f.values()) ** (1 / p)


def test_worked_example() -> None:
    sk = StableSketch(1, 5, random.Random(0), column=example_column)
    for item, c in [(0, 2), (2, 2), (1, -1), (0, 1)]:
        sk.update(item, c)
    assert all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(sk.y, [7.6, 0.21, -3.77, 5.79, -10.33]))
    assert math.isclose(sk.norm(), 5.79)
    assert norm_p({0: 3, 1: -1, 2: 2}, 1) == 6


def test_sketch_is_the_matrix_times_f() -> None:
    rng = random.Random(1)
    for p in (1, 2):
        sk = StableSketch(p, 40, rng)
        f: dict[int, int] = {}
        for _ in range(200):
            x, c = rng.randrange(30), rng.randint(-3, 3)
            sk.update(x, c)
            f[x] = f.get(x, 0) + c
        cols = {x: sk._seeded_column(x) for x in f}
        direct = [sum(cols[x][j] * f[x] for x in f) for j in range(sk.k)]
        assert all(math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-6) for a, b in zip(sk.y, direct))


def test_merge_equals_sketch_of_concatenation_and_deletions_cancel() -> None:
    rng = random.Random(2)
    a = StableSketch(1, 50, rng)
    b = a.empty_like()
    whole = a.empty_like()
    s1 = [(rng.randrange(20), rng.randint(-2, 5)) for _ in range(100)]
    s2 = [(rng.randrange(20), rng.randint(-2, 5)) for _ in range(100)]
    for x, c in s1:
        a.update(x, c)
        whole.update(x, c)
    for x, c in s2:
        b.update(x, c)
        whole.update(x, c)
    m = a.merge(b)
    assert all(math.isclose(u, v, rel_tol=1e-9, abs_tol=1e-6) for u, v in zip(m.y, whole.y))
    with pytest.raises(ValueError):
        a.merge(StableSketch(1, 50, rng))
    # Delete everything again: the sketch of the zero vector is 0 up to rounding.
    for x, c in s1 + s2:
        whole.update(x, -c)
    assert max(abs(v) for v in whole.y) < 1e-6


def test_row_probabilities_used_in_the_proof() -> None:
    # For |Cauchy|, P(|X| <= x) = (2/pi) arctan x. The proof needs both tails
    # around the median 1 to have mass at most 1/2 - eta, eta = 2 eps / (5 pi).
    def cdf(x: float) -> float:
        return 2 / math.pi * math.atan(x)

    for step in range(1, 101):
        eps = step / 100
        eta = 2 * eps / (5 * math.pi)
        assert cdf(1 - eps) <= 0.5 - eta + 1e-12
        assert 1 - cdf(1 + eps) <= 0.5 - eta + 1e-12
    assert rows_for(0.25, 0.1) == math.ceil(math.log(20) * 25 * math.pi**2 / (8 * 0.0625))


def test_failure_rate_for_l1_is_below_delta() -> None:
    eps, delta, trials = 0.25, 0.1, 25
    k = rows_for(eps, delta)
    rng = random.Random(3)
    f = {0: 5, 1: -3, 2: 1, 3: 7}
    true = norm_p(f, 1)
    failures = 0
    for _ in range(trials):
        sk = StableSketch(1, k, rng)
        for x, c in f.items():
            sk.update(x, c)
        if abs(sk.norm() - true) > eps * true:
            failures += 1
    # The theorem gives a rate at most delta; the bound is loose, and the
    # tolerance allows delta * trials failures, rounded down.
    assert failures <= int(delta * trials)


def test_l2_and_half_norm_estimates() -> None:
    rng = random.Random(4)
    f = {0: 4, 1: -2, 2: 1, 3: 1, 4: -1}
    # p = 2: the median of |N(0, 2)| is known in closed form.
    fails = 0
    for _ in range(20):
        sk = StableSketch(2, 401, rng)
        for x, c in f.items():
            sk.update(x, c)
        fails += abs(sk.norm() - norm_p(f, 2)) > 0.2 * norm_p(f, 2)
    assert fails <= 2
    # p = 1/2: the median of |X| comes from a seeded Monte Carlo run.
    mu = estimate_median_abs(0.5, random.Random(5))
    fails = 0
    for _ in range(20):
        sk = StableSketch(0.5, 401, rng, median_abs=mu)
        for x, c in f.items():
            sk.update(x, c)
        fails += abs(sk.moment() - norm_p(f, 0.5) ** 0.5) > 0.3 * norm_p(f, 0.5) ** 0.5
    assert fails <= 2


def test_lower_median_and_bad_input() -> None:
    assert lower_median([3, 1, 2]) == 2
    assert lower_median([4, 1, 3, 2]) == 2
    with pytest.raises(ValueError):
        StableSketch(3, 5, random.Random(0))
    with pytest.raises(ValueError):
        StableSketch(1.5, 5, random.Random(0))
