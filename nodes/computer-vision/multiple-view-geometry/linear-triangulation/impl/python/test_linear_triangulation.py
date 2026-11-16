# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-triangulation/. The authors are listed in prov/8H0B6Z.jsonl.
"""Tests of linear (DLT) triangulation."""

import random

import pytest

from cvgeom import add_noise, random_scene
from cvla import inv, matvec, mul, norm, sub
from linear_triangulation import (dlt_rows, linear_triangulation,
                                  linear_triangulation_inhomogeneous,
                                  triangulate_homogeneous)

P1 = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
P2 = [[1.0, 0.0, 0.0, -1.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]


def rel(a, b):
    return norm(sub(a, b)) / max(1.0, norm(b))


def test_worked_example_exact():
    X = linear_triangulation([P1, P2], [[0.25, 0.5], [0.0, 0.5]])
    assert rel(X, [1.0, 2.0, 4.0]) <= 1e-12
    Xh = triangulate_homogeneous([P1, P2], [[0.25, 0.5], [0.0, 0.5]])
    assert abs(norm(Xh) - 1.0) <= 1e-12 and Xh[3] > 0


def test_worked_example_noisy():
    xs = [[0.25, 0.5], [0.0, 0.52]]
    X = linear_triangulation([P1, P2], xs)
    assert rel(X, [0.99986, 2.03926, 3.99827]) <= 1e-5
    Xi = linear_triangulation_inhomogeneous([P1, P2], xs)
    assert rel(Xi, [0.99682, 2.02703, 3.97456]) <= 1e-5


def test_rows_vanish_at_the_true_point():
    A = dlt_rows([P1, P2], [[0.25, 0.5], [0.0, 0.5]])
    assert len(A) == 4
    assert max(abs(v) for v in matvec(A, [1.0, 2.0, 4.0, 1.0])) <= 1e-15


@pytest.mark.parametrize("seed", range(4))
def test_exact_recovery_in_pixels(seed):
    rng = random.Random(seed)
    sc = random_scene(rng, n=10, n_cams=2 + seed)
    for j, X in enumerate(sc["X"]):
        xs = [sc["x"][i][j] for i in range(len(sc["P"]))]
        assert rel(linear_triangulation(sc["P"], xs), X) <= 1e-8
        assert rel(linear_triangulation_inhomogeneous(sc["P"], xs), X) <= 1e-8


def test_noise_error_shrinks_with_views():
    rng = random.Random(10)
    errs = []
    for m in (2, 8):
        sc = random_scene(rng, n=30, n_cams=m)
        e = 0.0
        for j, X in enumerate(sc["X"]):
            xs = [add_noise(rng, [sc["x"][i][j]], 0.5)[0] for i in range(m)]
            e += norm(sub(linear_triangulation(sc["P"], xs), X))
        errs.append(e / 30)
    assert errs[1] < errs[0]
    assert errs[0] < 0.05


def test_inhomogeneous_is_affine_invariant():
    rng = random.Random(11)
    sc = random_scene(rng, n=5, n_cams=3)
    H = [[2.0, 0.3, 0.0, 10.0], [0.1, 1.0, 0.2, -3.0], [0.0, 0.4, 1.5, 2.0], [0.0, 0.0, 0.0, 1.0]]
    Hi = inv(H)
    Ps2 = [mul(P, Hi) for P in sc["P"]]
    for j in range(5):
        xs = add_noise(rng, [sc["x"][i][j] for i in range(3)], 1.0)
        X = linear_triangulation_inhomogeneous(sc["P"], xs)
        Y = linear_triangulation_inhomogeneous(Ps2, xs)
        assert rel(matvec(H, X + [1.0])[:3], Y) <= 1e-8


def test_homogeneous_is_not_translation_invariant():
    xs = [[0.25, 0.5], [0.0, 0.52]]
    H = [[1.0, 0.0, 0.0, 10.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    Hi = inv(H)
    X = linear_triangulation([P1, P2], xs)
    Y = linear_triangulation([mul(P1, Hi), mul(P2, Hi)], xs)
    back = [Y[0] - 10.0, Y[1], Y[2]]
    assert rel(back, X) > 1e-3


def test_homogeneous_is_invariant_under_world_rotation():
    rng = random.Random(12)
    sc = random_scene(rng, n=3, n_cams=2)
    c, s = 0.6, 0.8
    H = [[c, -s, 0.0, 0.0], [s, c, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    Ps2 = [mul(P, inv(H)) for P in sc["P"]]
    for j in range(3):
        xs = add_noise(rng, [sc["x"][i][j] for i in range(2)], 1.0)
        X = linear_triangulation(sc["P"], xs)
        Y = linear_triangulation(Ps2, xs)
        assert rel(matvec(H, X + [1.0])[:3], Y) <= 1e-8


def test_point_at_infinity_raises():
    # Two parallel rays along +Z from centers (0, 0, 0) and (1, 0, 0).
    with pytest.raises(ValueError):
        linear_triangulation([P1, P2], [[0.0, 0.0], [0.0, 0.0]])


def test_needs_two_views():
    with pytest.raises(ValueError):
        dlt_rows([P1], [[0.0, 0.0]])
