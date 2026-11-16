# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epnp/. The authors are listed in prov/ATAF9X.jsonl.
"""Tests of EPnP."""

import math
import random

import pytest

from cvgeom import add_noise, make_K, random_rotation, rot_x, rot_y
from cvla import matvec, mul, norm, sub, transpose
from epnp import (barycentric, build_M, control_points, epnp, epnp_pixels,
                  reprojection_error)

R0 = mul(rot_y(0.3), rot_x(0.2))
T0 = [0.2, -0.1, 4.0]
X0 = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0.5], [0.3, 0.7, 1.2]]


def rotation_angle(Ra, Rb):
    return 2.0 * math.asin(min(1.0, norm(sub(Ra, Rb)) / (2.0 * math.sqrt(2.0))))


def project_all(R, t, P):
    out = []
    for p in P:
        q = [a + b for a, b in zip(matvec(R, p), t)]
        out.append([q[0] / q[2], q[1] / q[2]])
    return out


def random_problem(rng, n):
    R = random_rotation(rng)
    t = [rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(4, 8)]
    P = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(n)]
    return R, t, P, project_all(R, t, P)


def test_worked_example():
    y = project_all(R0, T0, X0)
    R, t, info = epnp(X0, y, details=True)
    assert norm(sub(R, R0)) <= 1e-10
    assert norm(sub(t, T0)) <= 1e-10 * norm(T0)
    assert abs(info["eigenvalues"][0]) <= 1e-12
    assert abs(info["eigenvalues"][1] - 0.035921) <= 1e-6
    assert abs(info["trials"][0]["beta0"][0] - 9.27247) <= 1e-5
    rho = [0.2613, 0.2364, 0.1620, 0.4977, 0.4233, 0.3984]
    assert all(abs(a - b) <= 1e-4 for a, b in zip(info["rho"], rho))


def test_worked_example_noisy():
    y = project_all(R0, T0, X0)
    yn = [[p[0] + 0.002 * (-1) ** i, p[1] - 0.001 * i / 3] for i, p in enumerate(y)]
    R, t = epnp(X0, yn)
    assert abs(rotation_angle(R, R0) - 0.013227) <= 1e-5
    assert norm(sub(t, [0.199704, -0.095312, 3.994757])) <= 1e-5
    assert abs(reprojection_error(R, t, X0, yn) - 0.0017014) <= 1e-6


def test_control_points_and_weights():
    rng = random.Random(1)
    P = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(10)]
    cps = control_points(P)
    assert norm(sub(cps[0], [sum(p[k] for p in P) / 10 for k in range(3)])) <= 1e-12
    for p, a in zip(P, barycentric(P, cps)):
        assert abs(sum(a) - 1.0) <= 1e-12
        rec = [sum(a[j] * cps[j][k] for j in range(4)) for k in range(3)]
        assert norm(sub(rec, p)) <= 1e-12


def test_true_control_points_are_in_the_null_space():
    rng = random.Random(2)
    R, t, P, y = random_problem(rng, 8)
    cps = control_points(P)
    x = []
    for c in cps:
        x += [a + b for a, b in zip(matvec(R, c), t)]
    M = build_M(barycentric(P, cps), y)
    assert len(M) == 16 and len(M[0]) == 12
    assert norm(matvec(M, x)) <= 1e-12 * norm(x)


def test_random_exact_scenes():
    rng = random.Random(3)
    for _ in range(25):
        n = rng.choice([6, 9, 20])
        R, t, P, y = random_problem(rng, n)
        Re, te = epnp(P, y)
        assert rotation_angle(Re, R) <= 1e-6
        assert norm(sub(te, t)) <= 1e-6 * norm(t)


def test_five_points():
    rng = random.Random(4)
    for _ in range(10):
        R, t, P, y = random_problem(rng, 5)
        Re, te = epnp(P, y)
        assert rotation_angle(Re, R) <= 1e-6
        assert norm(sub(te, t)) <= 1e-6 * norm(t)


def test_noise():
    rng = random.Random(5)
    for _ in range(5):
        R, t, P, y = random_problem(rng, 40)
        yn = add_noise(rng, y, 1.0 / 800.0)
        Re, te = epnp(P, yn)
        assert rotation_angle(Re, R) <= 0.02
        assert norm(sub(te, t)) <= 0.05 * norm(t)
        assert reprojection_error(Re, te, P, yn) <= 3.0 / 800.0


def test_pixels():
    rng = random.Random(6)
    K = make_K(800, 780, 320, 240, 0.5)
    R, t, P, y = random_problem(rng, 10)
    x = [matvec(K, [u, v, 1.0])[:2] for u, v in y]
    Re, te = epnp_pixels(P, x, K)
    assert rotation_angle(Re, R) <= 1e-6
    assert norm(sub(te, t)) <= 1e-6 * norm(t)


def test_change_of_world_frame():
    rng = random.Random(7)
    R, t, P, y = random_problem(rng, 10)
    yn = add_noise(rng, y, 0.002)
    Ra, ta = epnp(P, yn)
    I3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    T = [rng.uniform(-5, 5) for _ in range(3)]
    # A translation of the world moves the centroid only: the same pose.
    # A rotation can flip the signs of the principal directions, which
    # changes the control points, so on noisy data the pose moves a little.
    for Q, tol in ((I3, 1e-8), (random_rotation(rng), 0.01)):
        P2 = [[a + b for a, b in zip(matvec(Q, p), T)] for p in P]
        Rb, tb = epnp(P2, yn)
        # The same camera in the new frame: R' = R Q^T, t' = t - R Q^T T.
        Rexp = mul(Ra, transpose(Q))
        texp = [a - b for a, b in zip(ta, matvec(Rexp, T))]
        assert rotation_angle(Rb, Rexp) <= tol
        assert norm(sub(tb, texp)) <= tol * norm(texp)


def test_selected_pose_has_least_error():
    rng = random.Random(8)
    R, t, P, y = random_problem(rng, 12)
    yn = add_noise(rng, y, 0.003)
    Re, te, info = epnp(P, yn, details=True)
    err = reprojection_error(Re, te, P, yn)
    assert err == min(tr["error"] for tr in info["trials"])


def test_bad_input():
    with pytest.raises(ValueError):
        epnp([[0, 0, 0], [1, 0, 0], [0, 1, 0]], [[0, 0], [0.1, 0], [0, 0.1]])
    rng = random.Random(9)
    planar = [[rng.uniform(-1, 1), rng.uniform(-1, 1), 0.0] for _ in range(8)]
    y = project_all(R0, T0, planar)
    with pytest.raises(ValueError):
        epnp(planar, y)
