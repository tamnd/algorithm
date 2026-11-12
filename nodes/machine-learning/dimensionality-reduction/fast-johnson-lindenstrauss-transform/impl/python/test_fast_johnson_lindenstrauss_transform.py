# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-johnson-lindenstrauss-transform/. The authors are listed in prov/E208HD.jsonl.

import math
import random

import pytest

from fast_johnson_lindenstrauss_transform import (
    FJLT,
    SRHT,
    fjlt_sparsity,
    fwht,
    hadamard_matrix,
    sq_dist,
    sq_norm,
)


def matvec(m, x):
    return [sum(a * b for a, b in zip(row, x)) for row in m]


def test_fwht_equals_matrix_product_exactly():
    rng = random.Random(0)
    for p in range(0, 7):
        d = 2 ** p
        h = hadamard_matrix(d)
        for _ in range(5):
            x = [rng.randint(-9, 9) for _ in range(d)]
            assert fwht(x) == matvec(h, x)


def test_fwht_trace_from_the_page():
    assert fwht([1, 2, 3, 4, 0, 0, 0, 0]) == [10, -2, -4, 0, 10, -2, -4, 0]


def test_fwht_is_its_own_inverse_up_to_d_and_keeps_norm():
    rng = random.Random(1)
    for d in (1, 2, 8, 64):
        x = [rng.randint(-5, 5) for _ in range(d)]
        y = fwht(x)
        assert fwht(y) == [d * v for v in x]
        assert sum(v * v for v in y) == d * sum(v * v for v in x)


def test_hadamard_rows_are_orthogonal():
    h = hadamard_matrix(16)
    for i in range(16):
        for j in range(16):
            assert sum(a * b for a, b in zip(h[i], h[j])) == (16 if i == j else 0)


def test_fwht_rejects_bad_length():
    with pytest.raises(ValueError):
        fwht([1, 2, 3])


def test_preconditioning_keeps_norm_and_spreads_a_spike():
    rng = random.Random(2)
    f = FJLT(256, 8, 1.0, rng)
    x = [0.0] * 256
    x[37] = 3.0
    u = f.precondition(x)
    assert abs(sq_norm(u) - 9.0) < 1e-9
    # A spike becomes a flat vector: each coordinate is +-3/sqrt(256).
    assert all(abs(abs(v) - 3.0 / 16.0) < 1e-12 for v in u)


def test_max_coordinate_bound_after_preconditioning():
    # Hoeffding and a union bound: with probability at least 19/20 every coordinate of
    # H D x has absolute value at most sqrt(2 ln(40 n d) / d) for unit x.
    rng = random.Random(3)
    d, n = 256, 20
    pts = []
    for i in range(n):
        x = [0.0] * d
        for _ in range(1 + i % 3):
            x[rng.randrange(d)] = rng.choice((-1.0, 2.0))
        pts.append(x)
    bound = math.sqrt(2 * math.log(40 * n * d) / d)
    for seed in range(10):
        f = FJLT(d, 4, 1.0, random.Random(seed))
        for x in pts:
            u = f.precondition(x)
            assert max(abs(v) for v in u) <= bound * math.sqrt(sq_norm(x)) + 1e-12


def test_fjlt_is_unbiased_on_average():
    rng = random.Random(4)
    d = 64
    x = [rng.gauss(0, 1) for _ in range(d)]
    total = 0.0
    trials = 300
    for seed in range(trials):
        f = FJLT(d, 16, 0.25, random.Random(1000 + seed))
        total += sq_norm(f.apply(x))
    assert abs(total / trials / sq_norm(x) - 1.0) < 0.05


def test_fjlt_distortion_on_seeded_points():
    rng = random.Random(5)
    d0, n, k = 200, 16, 200  # d0 is padded to 256
    pts = []
    for i in range(n):
        if i % 2:
            pts.append([rng.gauss(0, 1) for _ in range(d0)])
        else:
            x = [0.0] * d0
            x[rng.randrange(d0)] = 1.0
            pts.append(x)
    q = fjlt_sparsity(n, 256)
    f = FJLT(d0, k, q, random.Random(6))
    assert f.d == 256
    ys = [f.apply(x) for x in pts]
    for i in range(n):
        for j in range(i + 1, n):
            r = sq_dist(ys[i], ys[j]) / sq_dist(pts[i], pts[j])
            assert 0.5 < r < 1.5


def test_srht_distortion_on_seeded_points():
    rng = random.Random(7)
    d0, n, k = 128, 12, 160
    pts = [[rng.gauss(0, 1) for _ in range(d0)] for _ in range(n)]
    s = SRHT(d0, k, random.Random(8))
    ys = [s.apply(x) for x in pts]
    for i in range(n):
        for j in range(i + 1, n):
            r = sq_dist(ys[i], ys[j]) / sq_dist(pts[i], pts[j])
            assert 0.5 < r < 1.5


def test_srht_is_exact_when_all_coordinates_are_sampled_once():
    rng = random.Random(9)
    s = SRHT(16, 16, rng)
    s.coords = list(range(16))
    x = [rng.gauss(0, 1) for _ in range(16)]
    assert abs(sq_norm(s.apply(x)) - sq_norm(x)) < 1e-9
