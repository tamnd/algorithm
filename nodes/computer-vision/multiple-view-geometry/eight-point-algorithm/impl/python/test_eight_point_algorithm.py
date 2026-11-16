# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eight-point-algorithm/. The authors are listed in prov/ZB0KR6.jsonl.
"""Tests of the plain eight-point algorithm."""

import math
import random

import pytest

from cvla import det, inv, matvec, mul, norm, skew, sub, svd, transpose
from eight_point_algorithm import (algebraic_residuals, canonical,
                                   design_singular_values, eight_point,
                                   epipolar_row)

K1 = [[500.0, 0.0, 320.0], [0.0, 500.0, 240.0], [0.0, 0.0, 1.0]]
K2 = [[450.0, 0.0, 300.0], [0.0, 460.0, 250.0], [0.0, 0.0, 1.0]]
R_EX = [[0.8, 0.0, 0.6], [0.0, 1.0, 0.0], [-0.6, 0.0, 0.8]]
T_EX = [1.0, 0.0, 0.0]


def rotation(axis, angle):
    """Rodrigues formula, written out (independent of the code under test)."""
    a = [c / norm(axis) for c in axis]
    k = skew(a)
    k2 = mul(k, k)
    s, c = math.sin(angle), math.cos(angle)
    return [[(1.0 if i == j else 0.0) + s * k[i][j] + (1.0 - c) * k2[i][j]
             for j in range(3)] for i in range(3)]


def project(K, X):
    y = matvec(K, X)
    return [y[0] / y[2], y[1] / y[2]]


def scene(rng, n, R, t, planar=False):
    """n points in front of both cameras, as 3D points of camera 1."""
    pts = []
    while len(pts) < n:
        x, y = rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0)
        z = 6.0 + 0.3 * x - 0.2 * y if planar else rng.uniform(4.0, 8.0)
        X1 = [x, y, z]
        X2 = [a + b for a, b in zip(matvec(R, X1), t)]
        if X2[2] > 0.5:
            pts.append((X1, X2))
    return pts


def true_F(R, t):
    E = mul(skew(t), R)
    return canonical(mul(mul(transpose(inv(K2)), E), inv(K1)))


def test_row_is_kronecker_product():
    row = epipolar_row([2.0, 3.0], [5.0, 7.0])
    assert row == [10.0, 15.0, 5.0, 14.0, 21.0, 7.0, 2.0, 3.0, 1.0]
    F = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
    f = [x for r in F for x in r]
    direct = algebraic_residuals(F, [[2.0, 3.0]], [[5.0, 7.0]])[0]
    assert abs(sum(a * b for a, b in zip(row, f)) - direct) <= 1e-12


def test_worked_example_essential():
    # Normalized coordinates, R about the Y axis, t = (1, 0, 0).
    rng = random.Random(1)
    pts = scene(rng, 8, R_EX, T_EX)
    x1 = [[X1[0] / X1[2], X1[1] / X1[2]] for X1, _ in pts]
    x2 = [[X2[0] / X2[2], X2[1] / X2[2]] for _, X2 in pts]
    E = eight_point(x1, x2, essential=True)
    expected = canonical([[0.0, 0.0, 0.0], [0.6, 0.0, -0.8], [0.0, 1.0, 0.0]])
    assert norm(sub(E, expected)) <= 1e-8
    s = svd(E)[1]
    assert abs(s[0] - s[1]) <= 1e-12 and abs(s[2]) <= 1e-12


def test_one_pair_of_the_example():
    # X1 = (0, 0, 5) gives X2 = R X1 + t = (4, 0, 4), so x1 = (0, 0) and x2 = (1, 0).
    X2 = [a + b for a, b in zip(matvec(R_EX, [0.0, 0.0, 5.0]), T_EX)]
    assert max(abs(a - b) for a, b in zip(X2, [4.0, 0.0, 4.0])) <= 1e-12
    E = [[0.0, 0.0, 0.0], [0.6, 0.0, -0.8], [0.0, 1.0, 0.0]]
    assert abs(algebraic_residuals(E, [[0.0, 0.0]], [[1.0, 0.0]])[0]) <= 1e-15


@pytest.mark.parametrize("seed", [2, 3, 4])
def test_exact_recovery_in_pixels(seed):
    rng = random.Random(seed)
    R = rotation([rng.uniform(-1, 1) for _ in range(3)], rng.uniform(0.05, 0.4))
    t = [rng.uniform(-1, 1), rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3)]
    pts = scene(rng, 20, R, t)
    x1 = [project(K1, X1) for X1, _ in pts]
    x2 = [project(K2, X2) for _, X2 in pts]
    F = eight_point(x1, x2)
    Ft = true_F(R, t)
    assert norm(sub(F, Ft)) <= 1e-8
    assert abs(det(F)) <= 1e-12
    assert abs(norm(F) - 1.0) <= 1e-12
    for r, p, q in zip(algebraic_residuals(F, x1, x2), x1, x2):
        assert abs(r) <= 1e-9 * (1.0 + abs(p[0]) + abs(p[1])) * (1.0 + abs(q[0]) + abs(q[1]))


def test_exactly_eight_points():
    rng = random.Random(5)
    R = rotation([0.2, 1.0, 0.1], 0.3)
    t = [0.9, 0.1, -0.2]
    pts = scene(rng, 8, R, t)
    x1 = [project(K1, X1) for X1, _ in pts]
    x2 = [project(K2, X2) for _, X2 in pts]
    assert norm(sub(eight_point(x1, x2), true_F(R, t))) <= 1e-8


def test_noise_gives_rank_two():
    rng = random.Random(6)
    R = rotation([0.0, 1.0, 0.2], 0.25)
    t = [1.0, 0.0, 0.1]
    pts = scene(rng, 40, R, t)
    x1 = [[c + rng.gauss(0.0, 0.5) for c in project(K1, X1)] for X1, _ in pts]
    x2 = [[c + rng.gauss(0.0, 0.5) for c in project(K2, X2)] for _, X2 in pts]
    F = eight_point(x1, x2)
    s = svd(F)[1]
    assert s[2] <= 1e-12 * s[0]
    # the epipole of image 1 is the null vector of F, and F e1 = 0 holds
    e1 = [row[2] for row in svd(F)[2]]
    assert norm(matvec(F, e1)) <= 1e-12


def test_planar_scene_is_degenerate():
    rng = random.Random(7)
    R = rotation([0.1, 1.0, 0.0], 0.2)
    t = [1.0, 0.2, 0.0]
    pts = scene(rng, 12, R, t, planar=True)
    x1 = [[X1[0] / X1[2], X1[1] / X1[2]] for X1, _ in pts]
    x2 = [[X2[0] / X2[2], X2[1] / X2[2]] for _, X2 in pts]
    s = design_singular_values(x1, x2)
    assert s[5] > 1e-6 * s[0]
    assert s[6] <= 1e-10 * s[0]  # a three-dimensional solution space


def test_pure_rotation_is_degenerate():
    rng = random.Random(8)
    R = rotation([0.3, 1.0, 0.1], 0.2)
    pts = scene(rng, 12, R, [0.0, 0.0, 0.0])
    x1 = [[X1[0] / X1[2], X1[1] / X1[2]] for X1, _ in pts]
    x2 = [[X2[0] / X2[2], X2[1] / X2[2]] for _, X2 in pts]
    s = design_singular_values(x1, x2)
    assert s[5] > 1e-6 * s[0]
    assert s[6] <= 1e-10 * s[0]


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        eight_point([[0.0, 0.0]] * 7, [[0.0, 0.0]] * 7)
    with pytest.raises(ValueError):
        eight_point([[0.0, 0.0]] * 8, [[0.0, 0.0]] * 9)


def test_canonical_sign_rule():
    F = [[0.0, -2.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    c = canonical(F)
    assert abs(c[0][1] - 2.0 / math.sqrt(5.0)) <= 1e-15
    assert abs(c[1][0] + 1.0 / math.sqrt(5.0)) <= 1e-15
    assert canonical(F) == canonical([[-x for x in r] for r in F])
