# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/p3p/. The authors are listed in prov/E145BQ.jsonl.
"""Tests of P3P by Grunert's elimination."""

import math
import random

import pytest

from cvgeom import random_scene, rot_x, rot_y
from cvla import det, dot, matvec, mul, norm, polyroots_real, sub, transpose
from p3p import (bearing, grunert_polynomials, p3p, p3p_select,
                 reprojection_error)

I3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
K1 = I3

# The worked example of the page.
X_EX = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.3, 1.0, 0.0], [1.0, 1.0, 1.0]]
R_EX = mul(rot_y(0.3), rot_x(0.2))
T_EX = [0.2, -0.1, 4.0]


def image(R, t, X):
    xc = [a + b for a, b in zip(matvec(R, X), t)]
    return [xc[0] / xc[2], xc[1] / xc[2]]


def rotation_angle(R1, R2):
    """The angle of R1^T R2, as 2 asin(||R1 - R2||_F / (2 sqrt 2)), which
    keeps its accuracy near 0."""
    d = norm(sub(R1, R2)) / (2.0 * math.sqrt(2.0))
    return 2.0 * math.asin(min(1.0, d))


def pose_error(R, t, sol):
    Rs, ts = sol
    return rotation_angle(R, Rs) + norm(sub(t, ts)) / max(1.0, norm(t))


def root_gap(X, y):
    """The smallest distance between two positive real roots of G."""
    f = [bearing(v) for v in y[:3]]
    ca, cb, cg = dot(f[1], f[2]), dot(f[0], f[2]), dot(f[0], f[1])
    a, b, c = norm(sub(X[1], X[2])), norm(sub(X[0], X[2])), norm(sub(X[0], X[1]))
    g, _, _ = grunert_polynomials(ca, cb, cg, a, b, c)
    r = sorted(v for v in polyroots_real(g) if v > 0)
    return min((r[i + 1] - r[i] for i in range(len(r) - 1)), default=math.inf)


def test_worked_example():
    y = [image(R_EX, T_EX, X) for X in X_EX]
    sols = p3p(X_EX[:3], y[:3])
    assert len(sols) == 2
    errs = sorted(pose_error(R_EX, T_EX, s) for s in sols)
    assert errs[0] <= 1e-8 and errs[1] > 0.1
    # the other pose misses the fourth point by about 0.18
    other = [s for s in sols if pose_error(R_EX, T_EX, s) > 0.1][0]
    assert abs(reprojection_error(other[0], other[1], X_EX[3], y[3]) - 0.1798) <= 1e-4
    Rb, tb = p3p_select(X_EX, y)
    assert pose_error(R_EX, T_EX, (Rb, tb)) <= 1e-8


def test_quartic_of_the_example():
    y = [image(R_EX, T_EX, X) for X in X_EX]
    f = [bearing(v) for v in y[:3]]
    ca, cb, cg = dot(f[1], f[2]), dot(f[0], f[2]), dot(f[0], f[1])
    g, _, _ = grunert_polynomials(ca, cb, cg, math.sqrt(1.49), math.sqrt(1.09), 1.0)
    roots = polyroots_real(g)
    assert len(roots) == 2
    assert abs(roots[0] - 0.867775) <= 1e-6 and abs(roots[1] - 1.055802) <= 1e-6


@pytest.mark.parametrize("seed", range(4))
def test_all_solutions_are_valid(seed):
    rng = random.Random(seed)
    for _ in range(8):
        sc = random_scene(rng, n=3, n_cams=1, K=K1)
        X, y = sc["X"], sc["x"][0]
        sols = p3p(X, y)
        assert 1 <= len(sols) <= 4
        for R, t in sols:
            assert abs(det(R) - 1.0) <= 1e-9
            assert norm(sub(mul(transpose(R), R), I3)) <= 1e-9
            for i in range(3):
                assert reprojection_error(R, t, X[i], y[i]) <= 1e-7


@pytest.mark.parametrize("seed", range(4, 8))
def test_true_pose_is_among_the_solutions(seed):
    rng = random.Random(seed)
    for _ in range(8):
        sc = random_scene(rng, n=3, n_cams=1, K=K1)
        X, y = sc["X"], sc["x"][0]
        R, t = sc["R"][0], sc["t"][0]
        best = min(pose_error(R, t, s) for s in p3p(X, y))
        # near a double root of G the roots lose half of their digits
        tol = 1e-8 if root_gap(X, y) > 0.05 else 1e-4
        assert best <= tol


def test_select_with_a_fourth_point():
    rng = random.Random(21)
    for _ in range(12):
        sc = random_scene(rng, n=4, n_cams=1, K=K1)
        X, y = sc["X"], sc["x"][0]
        R, t = sc["R"][0], sc["t"][0]
        if root_gap(X, y) <= 0.05:
            continue
        assert pose_error(R, t, p3p_select(X, y)) <= 1e-8


def test_pixel_input_after_normalization():
    # Pixels are mapped by K^-1 before the solver is called.
    rng = random.Random(22)
    K = [[800.0, 0.0, 320.0], [0.0, 800.0, 240.0], [0.0, 0.0, 1.0]]
    sc = random_scene(rng, n=4, n_cams=1, K=K)
    y = [[(u - 320.0) / 800.0, (v - 240.0) / 800.0] for u, v in sc["x"][0]]
    Rb, tb = p3p_select(sc["X"], y)
    assert pose_error(sc["R"][0], sc["t"][0], (Rb, tb)) <= 1e-8


def test_common_root_of_n_and_d_is_rejected():
    # Here cos(alpha) = cos(beta) cos(gamma), so N and D share a root and G
    # has a double root that is not a solution. Only two poses remain.
    R = [[1.0, 0.0, 0.0], [0.0, 0.8, -0.6], [0.0, 0.6, 0.8]]
    t = [0.0, 0.0, 4.0]
    X = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    y = [image(R, t, p) for p in X]
    sols = p3p(X, y)
    assert len(sols) == 2
    assert min(pose_error(R, t, s) for s in sols) <= 1e-8
    for Rs, ts in sols:
        for i in range(3):
            assert reprojection_error(Rs, ts, X[i], y[i]) <= 1e-9


def test_zero_denominator_uses_the_quadratic():
    # Ray 2 is orthogonal to the side X1 X3 at the true pose, so D(v) = 0
    # there; the solver must still return the true pose.
    R = [[0.8, 0.0, 0.6], [0.0, 1.0, 0.0], [-0.6, 0.0, 0.8]]
    t = [0.0, 0.0, 4.0]
    X = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    y = [image(R, t, p) for p in X]
    sols = p3p(X, y)
    assert min(pose_error(R, t, s) for s in sols) <= 1e-8


def test_noise_gives_a_close_pose():
    # sigma = 0.0005 in normalized coordinates (0.4 pixel at f = 800).
    rng = random.Random(23)
    sc = random_scene(rng, n=6, n_cams=1, K=K1)
    y = [[c + rng.gauss(0.0, 0.0005) for c in p] for p in sc["x"][0]]
    Rb, tb = p3p_select(sc["X"], y)
    assert rotation_angle(sc["R"][0], Rb) <= 0.05
    assert norm(sub(tb, sc["t"][0])) <= 0.1 * norm(sc["t"][0])


def test_collinear_points_raise():
    X = [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [2.0, 2.0, 2.0]]
    y = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2]]
    with pytest.raises(ValueError):
        p3p(X, y)
