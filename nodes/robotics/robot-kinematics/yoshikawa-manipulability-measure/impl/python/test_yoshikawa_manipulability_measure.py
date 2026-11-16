# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yoshikawa-manipulability-measure/. The authors are listed in prov/WRDGRM.jsonl.
"""Tests of the manipulability measure: the 2R closed form, the product of
singular values, |det J| for square J, invariance under rotations, scaling,
zero at singularities, and the best posture of the 2R arm."""

import math
import random

import pytest

import rbm
from yoshikawa_manipulability_measure import condition_number, manipulability, singular_values


def rand_matrix(rng, m, n):
    return [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(m)]


def jac_2r(l1, l2, q):
    s1, c1 = math.sin(q[0]), math.cos(q[0])
    s12, c12 = math.sin(q[0] + q[1]), math.cos(q[0] + q[1])
    return [[-l1 * s1 - l2 * s12, -l2 * s12], [l1 * c1 + l2 * c12, l2 * c12]]


def rand_rotation(rng):
    w = [rng.uniform(-1.0, 1.0) for _ in range(3)]
    return rbm.so3_exp(w)


def rand_orthogonal(rng, n):
    """Product of random Givens rotations, an n by n orthogonal matrix."""
    q = rbm.eye(n)
    for _ in range(3 * n):
        i, k = rng.sample(range(n), 2)
        a = rng.uniform(-math.pi, math.pi)
        g = rbm.eye(n)
        g[i][i] = g[k][k] = math.cos(a)
        g[i][k] = -math.sin(a)
        g[k][i] = math.sin(a)
        q = rbm.mul(q, g)
    return q


def test_2r_check_values():
    j = jac_2r(1.0, 1.0, [0.0, math.pi / 2.0])
    assert max(abs(x - y) for r, s in zip(j, [[-1.0, -1.0], [1.0, 0.0]]) for x, y in zip(r, s)) < 1e-15
    assert abs(manipulability(j) - 1.0) < 1e-14
    s = singular_values(j)
    assert abs(s[0] - (1.0 + math.sqrt(5.0)) / 2.0) < 1e-12
    assert abs(s[1] - (math.sqrt(5.0) - 1.0) / 2.0) < 1e-12
    assert abs(condition_number(j) - (3.0 + math.sqrt(5.0)) / 2.0) < 1e-12
    rng = random.Random(31)
    for _ in range(20):
        l1, l2 = rng.uniform(0.2, 2.0), rng.uniform(0.2, 2.0)
        q = [rng.uniform(-math.pi, math.pi) for _ in range(2)]
        assert abs(manipulability(jac_2r(l1, l2, q)) - l1 * l2 * abs(math.sin(q[1]))) < 1e-12


def test_product_of_singular_values():
    rng = random.Random(32)
    for m, n in [(2, 3), (3, 7), (6, 6), (6, 7), (1, 4)]:
        j = rand_matrix(rng, m, n)
        assert abs(manipulability(j) - math.prod(singular_values(j))) < 1e-12


def test_square_is_abs_det():
    rng = random.Random(33)
    for n in (2, 3, 6):
        j = rand_matrix(rng, n, n)
        assert abs(manipulability(j) - abs(rbm.det(j))) < 1e-12


def test_invariance_and_scaling():
    rng = random.Random(34)
    j = rand_matrix(rng, 3, 6)
    w = manipulability(j)
    r = rand_rotation(rng)
    assert abs(manipulability(rbm.mul(r, j)) - w) < 1e-12
    q = rand_orthogonal(rng, 6)
    assert abs(manipulability(rbm.mul(j, q)) - w) < 1e-12
    assert abs(manipulability(rbm.scale(j, 2.0)) - 8.0 * w) < 1e-11


def test_zero_at_singularities():
    rng = random.Random(35)
    # rank 2 Jacobian of size 3 by 5
    j = rbm.mul(rand_matrix(rng, 3, 2), rand_matrix(rng, 2, 5))
    assert manipulability(j) < 1e-7
    assert manipulability(jac_2r(1.0, 1.0, [0.7, 0.0])) < 1e-7
    assert condition_number([[1.0, 0.0], [0.0, 0.0]]) == math.inf
    with pytest.raises(ValueError):
        manipulability(rand_matrix(rng, 3, 2))


def test_best_posture_of_2r():
    grid = [k * math.pi / 180.0 for k in range(-180, 181)]
    best = max(grid, key=lambda q2: manipulability(jac_2r(1.0, 1.0, [0.3, q2])))
    assert abs(abs(best) - math.pi / 2.0) < 1e-12
    # with L1 + L2 = 2 fixed, w at q2 = pi / 2 is L1 L2, largest at L1 = L2 = 1
    lengths = [k / 100.0 for k in range(1, 200)]
    best_l1 = max(lengths, key=lambda l1: manipulability(jac_2r(l1, 2.0 - l1, [0.0, math.pi / 2.0])))
    assert abs(best_l1 - 1.0) < 1e-12
