# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-descent/. The authors are listed in prov/E223P3.jsonl.

import math
import random

from double_descent import (
    asymptotic_risk,
    exact_expected_risk,
    min_norm_least_squares,
    simulate_curve,
)


def gauss_matrix(n, p, rng):
    return [[rng.gauss(0.0, 1.0) for _ in range(p)] for _ in range(n)]


def matvec(x, w):
    return [sum(a * b for a, b in zip(row, w)) for row in x]


def test_underparameterized_matches_normal_equations():
    rng = random.Random(1)
    x = gauss_matrix(12, 4, rng)
    y = [rng.gauss(0.0, 1.0) for _ in range(12)]
    w = min_norm_least_squares(x, y)
    # The residual is orthogonal to every column (the normal equations).
    res = [a - b for a, b in zip(y, matvec(x, w))]
    for j in range(4):
        assert abs(sum(x[i][j] * res[i] for i in range(12))) < 1e-9


def test_overparameterized_interpolates_with_minimum_norm():
    rng = random.Random(2)
    n, p = 5, 11
    x = gauss_matrix(n, p, rng)
    y = [rng.gauss(0.0, 1.0) for _ in range(n)]
    w = min_norm_least_squares(x, y)
    fit = matvec(x, w)
    assert max(abs(a - b) for a, b in zip(fit, y)) < 1e-9
    norm_w = sum(t * t for t in w)
    # Any other interpolant is w + z with X z = 0, and has a larger norm.
    for _ in range(20):
        v = [rng.gauss(0.0, 1.0) for _ in range(p)]
        # Project v onto the null space of X: z = v - X^T (X X^T)^{-1} X v.
        coef = min_norm_least_squares(x, matvec(x, v))
        z = [a - b for a, b in zip(v, coef)]
        assert max(abs(t) for t in matvec(x, z)) < 1e-9
        other = [a + b for a, b in zip(w, z)]
        assert sum(t * t for t in other) >= norm_w - 1e-12
        # w is orthogonal to the null space.
        assert abs(sum(a * b for a, b in zip(w, z))) < 1e-9


def test_square_case_solves_exactly():
    rng = random.Random(3)
    x = gauss_matrix(6, 6, rng)
    y = [rng.gauss(0.0, 1.0) for _ in range(6)]
    w = min_norm_least_squares(x, y)
    assert max(abs(a - b) for a, b in zip(matvec(x, w), y)) < 1e-8


def test_simulation_agrees_with_exact_expectation_away_from_threshold():
    n, r, sigma = 20, 1.0, 0.5
    ps = [5, 10, 40, 80]
    sim = simulate_curve(n, ps, r, sigma, trials=300, seed=7)
    for p, s in zip(ps, sim):
        e = exact_expected_risk(n, p, r, sigma)
        assert abs(s - e) < 0.15 * e + 0.02, (p, s, e)


def test_peak_is_at_the_interpolation_threshold():
    n, r, sigma = 20, 1.0, 0.5
    ps = list(range(2, 61, 2))
    sim = simulate_curve(n, ps, r, sigma, trials=40, seed=11)
    best = ps[max(range(len(ps)), key=lambda i: sim[i])]
    assert abs(best - n) <= 2
    # The curve falls again on both sides of the peak.
    assert sim[ps.index(n)] > 10 * sim[ps.index(10)]
    assert sim[ps.index(n)] > 10 * sim[ps.index(60)]


def test_exact_formulas():
    assert exact_expected_risk(20, 10, 1.0, 0.5) == 0.25 * 10 / 9
    assert exact_expected_risk(20, 40, 1.0, 0.5) == 0.5 + 0.25 * 20 / 19
    assert math.isinf(exact_expected_risk(20, 20, 1.0, 0.5))
    assert asymptotic_risk(0.5, 1.0, 0.5) == 0.25
    assert abs(asymptotic_risk(2.0, 1.0, 0.5) - 0.75) < 1e-15
    assert math.isinf(asymptotic_risk(1.0, 1.0, 0.5))
