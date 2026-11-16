# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/seven-point-algorithm/. The authors are listed in prov/JZGDM0.jsonl.
"""Tests of the seven-point algorithm."""

import math
import random

import pytest

from cvla import inv, matvec, mul, norm, skew, sub, svd, transpose
from seven_point_algorithm import (canonical, cubic_coefficients,
                                   pencil_solutions, seven_point)

K1 = [[500.0, 0.0, 320.0], [0.0, 500.0, 240.0], [0.0, 0.0, 1.0]]
K2 = [[450.0, 0.0, 300.0], [0.0, 460.0, 250.0], [0.0, 0.0, 1.0]]


def diag(a, b, c):
    return [[a, 0.0, 0.0], [0.0, b, 0.0], [0.0, 0.0, c]]


def rotation(axis, angle):
    """Rodrigues formula, written out."""
    a = [c / norm(axis) for c in axis]
    k = skew(a)
    k2 = mul(k, k)
    s, c = math.sin(angle), math.cos(angle)
    return [[(1.0 if i == j else 0.0) + s * k[i][j] + (1.0 - c) * k2[i][j]
             for j in range(3)] for i in range(3)]


def project(K, X):
    y = matvec(K, X)
    return [y[0] / y[2], y[1] / y[2]]


def two_views(rng, n, planar=False):
    R = rotation([rng.uniform(-1, 1) for _ in range(3)], rng.uniform(0.05, 0.4))
    t = [rng.uniform(-1, 1), rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3)]
    x1, x2 = [], []
    while len(x1) < n:
        x, y = rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0)
        X1 = [x, y, 6.0 + 0.3 * x - 0.2 * y if planar else rng.uniform(4.0, 8.0)]
        X2 = [a + b for a, b in zip(matvec(R, X1), t)]
        if X2[2] > 0.5:
            x1.append(project(K1, X1))
            x2.append(project(K2, X2))
    return R, t, x1, x2


def true_F(R, t):
    return canonical(mul(mul(transpose(inv(K2)), mul(skew(t), R)), inv(K1)))


def contains(sols, M, tol):
    M = canonical(M)
    return any(norm(sub(canonical(S), M)) <= tol for S in sols)


def test_cubic_with_three_real_roots():
    # F2 + alpha (F1 - F2) = diag(1 + alpha, 2 - alpha, 3 - 3 alpha)
    F1, F2 = diag(2.0, 1.0, 0.0), diag(1.0, 2.0, 3.0)
    c = cubic_coefficients(F1, F2)
    # det = 3 (1 + alpha)(2 - alpha)(1 - alpha) = 3 alpha^3 - 6 alpha^2 - 3 alpha + 6
    assert max(abs(a - b) for a, b in zip(c, [3.0, -6.0, -3.0, 6.0])) <= 1e-12
    sols = pencil_solutions(F1, F2)
    assert len(sols) == 3
    for M in (diag(0.0, 3.0, 6.0), diag(3.0, 0.0, -3.0), diag(2.0, 1.0, 0.0)):
        assert contains(sols, M, 1e-12)


def test_cubic_with_one_real_root():
    # det [[1, -a, 0], [a, 1, 0], [0, 0, 1 + a]] = (1 + a^2)(1 + a)
    F2 = diag(1.0, 1.0, 1.0)
    F1 = [[1.0, -1.0, 0.0], [1.0, 1.0, 0.0], [0.0, 0.0, 2.0]]
    sols = pencil_solutions(F1, F2)
    assert len(sols) == 1
    assert contains(sols, [[1.0, 1.0, 0.0], [-1.0, 1.0, 0.0], [0.0, 0.0, 0.0]], 1e-12)


def test_leading_coefficient_zero_adds_the_direction():
    # diag(1, 2 - alpha, 3 - 2 alpha): a quadratic, and F1 - F2 = diag(0, -1, -2)
    F1, F2 = diag(1.0, 1.0, 1.0), diag(1.0, 2.0, 3.0)
    sols = pencil_solutions(F1, F2)
    assert len(sols) == 3
    for M in (diag(1.0, 0.0, -1.0), diag(1.0, 0.5, 0.0), diag(0.0, -1.0, -2.0)):
        assert contains(sols, M, 1e-12)


@pytest.mark.parametrize("seed", range(6))
def test_true_F_is_among_the_solutions(seed):
    rng = random.Random(seed)
    R, t, x1, x2 = two_views(rng, 7)
    sols = seven_point(x1, x2)
    assert len(sols) in (1, 3)
    assert contains(sols, true_F(R, t), 1e-8)
    for F in sols:
        s = svd(F)[1]
        assert s[2] <= 1e-10 * s[0]
        for p, q in zip(x1, x2):
            line = matvec(F, [p[0], p[1], 1.0])
            d = abs(line[0] * q[0] + line[1] * q[1] + line[2]) / math.hypot(line[0], line[1])
            assert d <= 1e-6  # pixels


def test_both_solution_counts_occur():
    counts = set()
    for seed in range(12):
        _, _, x1, x2 = two_views(random.Random(seed), 7)
        counts.add(len(seven_point(x1, x2)))
    assert counts == {1, 3}


def test_planar_points_are_rejected():
    _, _, x1, x2 = two_views(random.Random(20), 7, planar=True)
    with pytest.raises(ValueError):
        seven_point(x1, x2)


def test_wrong_number_of_points():
    with pytest.raises(ValueError):
        seven_point([[0.0, 0.0]] * 8, [[1.0, 1.0]] * 8)
