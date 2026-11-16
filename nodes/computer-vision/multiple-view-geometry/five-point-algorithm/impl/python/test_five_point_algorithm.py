# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/five-point-algorithm/. The authors are listed in prov/SJPGET.jsonl.
"""Tests of the five-point algorithm."""

import math
import random

import pytest

from cvla import det, matvec, mul, norm, skew, sub, svd, transpose
from five_point_algorithm import (MONOMIALS, canonical, constraint_matrix,
                                  five_point)

R_EX = [[0.8, 0.0, 0.6], [0.0, 1.0, 0.0], [-0.6, 0.0, 0.8]]
T_EX = [1.0, 0.0, 0.0]


def rotation(axis, angle):
    """Rodrigues formula, written out."""
    a = [c / norm(axis) for c in axis]
    k = skew(a)
    k2 = mul(k, k)
    s, c = math.sin(angle), math.cos(angle)
    return [[(1.0 if i == j else 0.0) + s * k[i][j] + (1.0 - c) * k2[i][j]
             for j in range(3)] for i in range(3)]


def scene(rng, n, R, t, planar=False):
    """n pairs of normalized points of 3D points in front of both cameras."""
    x1, x2 = [], []
    while len(x1) < n:
        x, y = rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0)
        X1 = [x, y, 6.0 + 0.4 * x - 0.3 * y if planar else rng.uniform(4.0, 8.0)]
        X2 = [a + b for a, b in zip(matvec(R, X1), t)]
        if X2[2] > 0.5:
            x1.append([X1[0] / X1[2], X1[1] / X1[2]])
            x2.append([X2[0] / X2[2], X2[1] / X2[2]])
    return x1, x2


def random_pose(rng):
    R = rotation([rng.uniform(-1, 1) for _ in range(3)], rng.uniform(0.05, 0.5))
    t = [rng.uniform(-1, 1), rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)]
    return R, t


def check_solutions(sols, x1, x2, E_true):
    assert len(sols) % 2 == 0 and len(sols) <= 10
    assert any(norm(sub(E, canonical(E_true))) <= 1e-8 for E in sols)
    for E in sols:
        assert abs(norm(E) - 1.0) <= 1e-12
        for p, q in zip(x1, x2):
            r = matvec(E, [p[0], p[1], 1.0])
            assert abs(r[0] * q[0] + r[1] * q[1] + r[2]) <= 1e-9
        s = svd(E)[1]
        assert abs(s[0] - s[1]) <= 1e-8 and s[2] <= 1e-8


def test_constraint_matrix_against_direct_evaluation():
    rng = random.Random(1)
    X, Y, Z, W = ([[rng.uniform(-1, 1) for _ in range(3)] for _ in range(3)] for _ in range(4))
    M = constraint_matrix(X, Y, Z, W)
    for _ in range(3):
        x, y, z = rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(-2, 2)
        mono = [x ** a * y ** b * z ** c for a, b, c in MONOMIALS]
        values = [sum(m * v for m, v in zip(row, mono)) for row in M]
        E = [[x * X[i][j] + y * Y[i][j] + z * Z[i][j] + W[i][j] for j in range(3)] for i in range(3)]
        EEt = mul(E, transpose(E))
        tr = EEt[0][0] + EEt[1][1] + EEt[2][2]
        T = mul(EEt, E)
        direct = [det(E)] + [2.0 * T[i][j] - tr * E[i][j] for i in range(3) for j in range(3)]
        assert max(abs(a - b) for a, b in zip(values, direct)) <= 1e-10


def test_worked_example():
    # The five points of the page, R about the Y axis and t = (1, 0, 0).
    x1, x2 = [], []
    for X1 in ([0, 0, 5], [1, 1, 4], [-1, 2, 6], [2, -1, 5], [-2, -2, 8]):
        X2 = [a + b for a, b in zip(matvec(R_EX, X1), T_EX)]
        x1.append([X1[0] / X1[2], X1[1] / X1[2]])
        x2.append([X2[0] / X2[2], X2[1] / X2[2]])
    assert max(abs(a - b) for a, b in zip(x2[1], [21 / 13, 5 / 13])) <= 1e-15
    sols = five_point(x1, x2)
    assert len(sols) == 4
    check_solutions(sols, x1, x2, [[0.0, 0.0, 0.0], [0.6, 0.0, -0.8], [0.0, 1.0, 0.0]])


def test_random_example_scene():
    rng = random.Random(2)
    x1, x2 = scene(rng, 5, R_EX, T_EX)
    check_solutions(five_point(x1, x2), x1, x2, [[0.0, 0.0, 0.0], [0.6, 0.0, -0.8], [0.0, 1.0, 0.0]])


@pytest.mark.parametrize("seed", range(3, 9))
def test_random_scenes(seed):
    rng = random.Random(seed)
    R, t = random_pose(rng)
    x1, x2 = scene(rng, 5, R, t)
    check_solutions(five_point(x1, x2), x1, x2, mul(skew(t), R))


def test_planar_scene_still_contains_the_truth():
    rng = random.Random(11)
    R, t = random_pose(rng)
    x1, x2 = scene(rng, 5, R, t, planar=True)
    check_solutions(five_point(x1, x2), x1, x2, mul(skew(t), R))


def test_more_than_five_points():
    rng = random.Random(12)
    R, t = random_pose(rng)
    x1, x2 = scene(rng, 9, R, t)
    sols = five_point(x1, x2)
    assert any(norm(sub(E, canonical(mul(skew(t), R)))) <= 1e-6 for E in sols)


def test_solution_counts_are_even_and_vary():
    counts = set()
    for seed in range(20, 30):
        rng = random.Random(seed)
        R, t = random_pose(rng)
        x1, x2 = scene(rng, 5, R, t)
        n = len(five_point(x1, x2))
        assert n % 2 == 0 and 2 <= n <= 10
        counts.add(n)
    assert len(counts) >= 2


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        five_point([[0.0, 0.0]] * 4, [[0.0, 0.0]] * 4)
    with pytest.raises(ValueError):
        five_point([[0.0, 0.0]] * 5, [[0.0, 0.0]] * 6)
