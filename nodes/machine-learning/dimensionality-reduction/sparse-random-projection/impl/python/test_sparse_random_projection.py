# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-random-projection/. The authors are listed in prov/J2JFH9.jsonl.

import itertools
import math
import random
from fractions import Fraction

from sparse_random_projection import (
    SparseJL,
    SparseRandomProjection,
    draw_sign,
    entry_moments,
    estimator_variance,
    sq_dist,
    sq_norm,
)


def exact_column_moments(x, s):
    """Mean and variance of (r . x)^2 for one column r, by enumeration of all sign patterns."""
    s = Fraction(s)
    prob = {1: 1 / (2 * s), -1: 1 / (2 * s), 0: 1 - 1 / s}
    m1 = m2 = Fraction(0)
    for pattern in itertools.product((-1, 0, 1), repeat=len(x)):
        p = Fraction(1)
        for g in pattern:
            p *= prob[g]
        val = s * sum(g * Fraction(v) for g, v in zip(pattern, x)) ** 2  # (r . x)^2 with r = sqrt(s) g
        m1 += p * val
        m2 += p * val * val
    return m1, m2 - m1 * m1


def test_achlioptas_entry_moments():
    assert entry_moments(3) == (1, 3)
    assert entry_moments(1) == (1, 1)
    assert entry_moments(16) == (1, 16)


def test_exact_variance_for_achlioptas_equals_gaussian():
    x = [3, -1, 2, 5]
    mean, var = exact_column_moments(x, 3)
    n2 = sum(v * v for v in x)
    assert mean == n2
    assert var == 2 * n2 * n2  # E[R^4] = 3, the Gaussian value
    assert var == estimator_variance(x, 3)


def test_exact_variance_formula_for_other_densities():
    for x in ([1, 1, 0, 0], [3, -1, 2, 5], [1, 0, 0, 0], [2, 2, 2, 2]):
        for s in (1, 2, 3, 4, 9):
            mean, var = exact_column_moments(x, s)
            assert mean == sum(v * v for v in x)
            assert var == estimator_variance(x, s)


def test_variance_of_k_columns_scales_as_one_over_k():
    x = [1, 2, -2, 0]
    assert estimator_variance(x, 3, k=10) == estimator_variance(x, 3) / 10
    # The worked example of the page: ||x||^2 = 9, sum x^4 = 33.
    assert estimator_variance(x, 3) == 162
    assert estimator_variance(x, 1) == 96
    assert estimator_variance(x, 4) == 195


def test_spike_is_the_worst_case_for_very_sparse():
    # For x = e_1 the estimator is r_1^2 = s with probability 1/s and 0 otherwise.
    for s in (1, 3, 9):
        mean, var = exact_column_moments([1, 0, 0], s)
        assert mean == 1 and var == s - 1


def test_draw_sign_frequencies():
    rng = random.Random(0)
    s = 4
    counts = {1: 0, -1: 0, 0: 0}
    trials = 40000
    for _ in range(trials):
        counts[draw_sign(s, rng)] += 1
    assert abs(counts[1] / trials - 1 / 8) < 0.01
    assert abs(counts[-1] / trials - 1 / 8) < 0.01


def test_sparse_jl_columns_have_exactly_s_nonzeros_and_unit_norm():
    m = SparseJL(50, 8, 4, random.Random(1))
    for col in m.cols:
        rows = [r for r, _ in col]
        assert len(rows) == 4 and len(set(rows)) == 4
        assert sorted(r // 8 for r in rows) == [0, 1, 2, 3]
    for j in range(50):
        e = [0.0] * 50
        e[j] = 1.0
        assert abs(sq_norm(m.apply(e)) - 1.0) < 1e-12


def test_sparse_jl_exact_mean_and_variance():
    # Enumerate all hash and sign choices for d = 3, b = 2, s = 2.
    x = [Fraction(1), Fraction(2), Fraction(-3)]
    b, s, d = 2, 2, 3
    choices = [(blk * b + r, g) for blk in range(s) for r in range(b) for g in (-1, 1)]
    per_col = [c for c in itertools.product(choices, repeat=s) if [r // b for r, _ in c] == list(range(s))]
    assert len(per_col) == (2 * b) ** s
    total = Fraction(0)
    total2 = Fraction(0)
    count = 0
    for cols in itertools.product(per_col, repeat=d):
        y = [Fraction(0)] * (b * s)
        for j in range(d):
            for r, g in cols[j]:
                y[r] += g * x[j]
        val = sum(t * t for t in y) / s
        total += val
        total2 += val * val
        count += 1
    mean = total / count
    var = total2 / count - mean * mean
    n2 = sum(v * v for v in x)
    n4 = sum(v ** 4 for v in x)
    assert mean == n2
    assert var == Fraction(2, b * s) * (n2 * n2 - n4)


def seeded_points(rng, n, d):
    return [[rng.gauss(0, 1) for _ in range(d)] for _ in range(n)]


def test_achlioptas_projection_distortion():
    rng = random.Random(2)
    n, d, k, eps = 20, 300, 250, 0.5
    pts = seeded_points(rng, n, d)
    m = SparseRandomProjection(d, k, 3, random.Random(3))
    ys = [m.apply(x) for x in pts]
    for i in range(n):
        for j in range(i + 1, n):
            r = sq_dist(ys[i], ys[j]) / sq_dist(pts[i], pts[j])
            assert 1 - eps < r < 1 + eps
    # About a third of the entries are nonzero.
    assert abs(m.nonzeros() / (d * k) - 1 / 3) < 0.01


def test_very_sparse_projection_on_dense_data():
    rng = random.Random(4)
    n, d, k = 20, 400, 250
    s = math.sqrt(d)  # density 1/20
    pts = seeded_points(rng, n, d)
    m = SparseRandomProjection(d, k, s, random.Random(5))
    ys = [m.apply(x) for x in pts]
    for i in range(n):
        for j in range(i + 1, n):
            r = sq_dist(ys[i], ys[j]) / sq_dist(pts[i], pts[j])
            assert 0.5 < r < 1.5
    assert abs(m.nonzeros() / (d * k) - 1 / 20) < 0.005


def test_sparse_jl_distortion():
    rng = random.Random(6)
    n, d = 20, 300
    pts = seeded_points(rng, n, d)
    m = SparseJL(d, 25, 8, random.Random(7))  # k = 200
    ys = [m.apply(x) for x in pts]
    for i in range(n):
        for j in range(i + 1, n):
            r = sq_dist(ys[i], ys[j]) / sq_dist(pts[i], pts[j])
            assert 0.5 < r < 1.5
