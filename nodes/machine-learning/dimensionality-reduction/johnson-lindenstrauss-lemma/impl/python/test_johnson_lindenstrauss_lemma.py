# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/johnson-lindenstrauss-lemma/. The authors are listed in prov/E6QYBH.jsonl.

import math
import random

import pytest

from johnson_lindenstrauss_lemma import (
    bad_fraction,
    distortion_ratios,
    gaussian_matrix,
    jl_dimension,
    project,
    tail_bound,
)


def test_dimension_formula_values():
    # k = ceil(4 ln n / (eps^2/2 - eps^3/3)), the bound of Dasgupta and Gupta.
    assert jl_dimension(1000, 0.1) == 5921
    assert jl_dimension(1000, 0.5) == 332
    assert jl_dimension(10 ** 6, 0.2) == 3189
    assert jl_dimension(40, 0.5) == 178
    for n in (2, 10, 1000, 10 ** 9):
        for eps in (0.05, 0.1, 0.3, 0.5, 0.9):
            k = jl_dimension(n, eps)
            assert k >= 4 * math.log(n) / (eps ** 2 / 2 - eps ** 3 / 3)
            assert k - 1 < 4 * math.log(n) / (eps ** 2 / 2 - eps ** 3 / 3)


def test_dimension_grows_like_log_n_over_eps_squared():
    # Doubling ln n doubles k up to rounding; halving eps multiplies k by about 4.
    assert abs(jl_dimension(10 ** 6, 0.2) / jl_dimension(10 ** 3, 0.2) - 2) < 0.002
    ratio = jl_dimension(10 ** 6, 0.05) / jl_dimension(10 ** 6, 0.1)
    assert 3.6 < ratio < 4.0


def test_dimension_rejects_bad_arguments():
    with pytest.raises(ValueError):
        jl_dimension(1, 0.5)
    with pytest.raises(ValueError):
        jl_dimension(10, 1.0)


def test_union_bound_is_below_one_at_the_dimension():
    for n in (2, 5, 100, 10 ** 6):
        for eps in (0.1, 0.5, 0.9):
            k = jl_dimension(n, eps)
            pairs = n * (n - 1) / 2
            assert 2 * tail_bound(k, eps) <= 2 / n ** 2 + 1e-15
            assert pairs * 2 * tail_bound(k, eps) < 1


def test_logarithm_inequalities_used_in_the_proof():
    for i in range(1, 1000):
        e = i / 1000
        assert math.log(1 + e) <= e - e * e / 2 + e ** 3 / 3 + 1e-15
        assert math.log(1 - e) <= -e - e * e / 2 + 1e-15


def test_chi_square_tails_are_below_the_bound():
    # For a unit u, ||f(u)||^2 is chi-square with k degrees of freedom divided by k.
    rng = random.Random(1)
    k, eps, trials = 30, 0.4, 4000
    upper = lower = 0
    total = 0.0
    for _ in range(trials):
        z = sum(rng.gauss(0, 1) ** 2 for _ in range(k)) / k
        total += z
        upper += z >= 1 + eps
        lower += z <= 1 - eps
    bound = tail_bound(k, eps)
    assert upper / trials <= bound
    assert lower / trials <= bound
    assert abs(total / trials - 1) < 0.02


def seeded_points(seed, n, d):
    rng = random.Random(seed)
    return [[rng.gauss(0, 1) for _ in range(d)] for _ in range(n)]


def test_no_pair_is_distorted_at_the_lemma_dimension():
    n, d, eps = 30, 300, 0.5
    pts = seeded_points(42, n, d)
    k = jl_dimension(n, eps)
    assert k == 164
    r = gaussian_matrix(k, d, random.Random(7))
    ys = [project(r, x) for x in pts]
    assert bad_fraction(pts, ys, eps) == 0.0


def test_fraction_of_distorted_pairs_is_small_below_the_dimension():
    # With k = 100 the expected fraction of bad pairs is at most 2 exp(-(k/2)(eps^2/2 - eps^3/3)).
    n, d, eps, k = 30, 300, 0.3, 100
    pts = seeded_points(43, n, d)
    r = gaussian_matrix(k, d, random.Random(8))
    ys = [project(r, x) for x in pts]
    frac = bad_fraction(pts, ys, eps)
    assert frac <= 2 * tail_bound(k, eps)
    assert frac < 0.1


def test_projection_is_linear():
    rng = random.Random(9)
    r = gaussian_matrix(5, 8, rng)
    x = [rng.gauss(0, 1) for _ in range(8)]
    y = [rng.gauss(0, 1) for _ in range(8)]
    fx, fy = project(r, x), project(r, y)
    fxy = project(r, [a - 2 * b for a, b in zip(x, y)])
    assert all(abs(u - (a - 2 * b)) < 1e-9 for u, a, b in zip(fxy, fx, fy))


def test_ratios_cover_all_pairs():
    pts = seeded_points(1, 6, 4)
    assert len(distortion_ratios(pts, pts)) == 15
    assert all(abs(v - 1) < 1e-12 for v in distortion_ratios(pts, pts))
