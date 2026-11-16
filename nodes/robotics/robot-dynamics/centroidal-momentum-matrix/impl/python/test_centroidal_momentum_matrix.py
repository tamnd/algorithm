# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/centroidal-momentum-matrix/. The authors are listed in prov/M8T9ZN.jsonl.
"""Tests of the centroidal momentum matrix against the sum of the link momenta and m J_com."""

import math
import random

import pytest

import rbm
from centroidal_momentum_matrix import (
    Model,
    body_poses,
    centroidal_momentum,
    centroidal_momentum_matrix,
    spatial_inertia,
)

Z_AXIS = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]


def planar_2r():
    """2R arm in the x-y plane, links of 1 m, point masses of 1 kg at the link ends."""
    model = Model()
    point = spatial_inertia(1.0, [1.0, 0.0, 0.0], rbm.zeros(3, 3))
    model.add_body(-1, rbm.eye(4), Z_AXIS, point)
    model.add_body(0, rbm.make_T(rbm.eye(3), [1.0, 0.0, 0.0]), Z_AXIS, point)
    return model


def random_body(rng):
    a = [[rng.uniform(-0.3, 0.3) for _ in range(3)] for _ in range(3)]
    ic = rbm.add(rbm.mul(a, rbm.transpose(a)), rbm.scale(rbm.eye(3), 0.05))
    com = [rng.uniform(-0.3, 0.3) for _ in range(3)]
    return spatial_inertia(rng.uniform(0.5, 2.0), com, ic)


def random_model(rng, n, floating=False):
    """A random tree; with floating=True it hangs below a six-joint floating base."""
    model = Model()
    first = 0
    if floating:
        massless = rbm.zeros(6, 6)
        axes = [[0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0]]
        for k, axis in enumerate(axes):
            model.add_body(k - 1, rbm.eye(4), axis, random_body(rng) if k == 5 else massless)
        first = 6
    for i in range(first, first + n):
        parent = rng.randrange(first - 1, i)
        tree = rbm.se3_exp([rng.uniform(-0.6, 0.6) for _ in range(6)])
        u = [rng.gauss(0.0, 1.0) for _ in range(3)]
        u = rbm.scale(u, 1.0 / rbm.norm(u))
        if rng.random() < 0.8:
            point = [rng.uniform(-0.3, 0.3) for _ in range(3)]
            screw = u + [-x for x in rbm.cross(u, point)]
        else:
            screw = [0.0, 0.0, 0.0] + u
        model.add_body(parent, tree, screw, random_body(rng))
    return model


def com_of(model, q):
    poses = body_poses(model, q)
    total, moment = 0.0, [0.0, 0.0, 0.0]
    for pose, inertia in zip(poses, model.inertia):
        m = inertia[5][5]
        if m > 0.0:
            c = [inertia[2][4] / m, inertia[0][5] / m, inertia[1][3] / m]
            total += m
            moment = rbm.add(moment, rbm.scale(rbm.T_apply(pose, c), m))
    return rbm.scale(moment, 1.0 / total)


def momentum_brute(model, q, qd, h=1e-6):
    """Sum over the bodies of the momentum about G, with twists from finite differences of the poses."""
    poses = body_poses(model, q)
    plus = body_poses(model, rbm.add(q, rbm.scale(qd, h)))
    minus = body_poses(model, rbm.sub(q, rbm.scale(qd, h)))
    pose_g = rbm.make_T(rbm.eye(3), com_of(model, q))
    total = [0.0] * 6
    for t, tp, tm, inertia in zip(poses, plus, minus, model.inertia):
        twist = rbm.vee6(rbm.mul(rbm.T_inv(t), rbm.scale(rbm.sub(tp, tm), 0.5 / h)))
        h_body = rbm.matvec(inertia, twist)
        x_ig = rbm.adjoint(rbm.mul(rbm.T_inv(t), pose_g))
        total = rbm.add(total, rbm.matvec(rbm.transpose(x_ig), h_body))
    return total


def maxdiff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def test_2r_hand_values():
    model = planar_2r()
    q = [0.0, math.pi / 2]
    a_g, m, com = centroidal_momentum_matrix(model, q)
    assert m == 2.0 and max(abs(x - y) for x, y in zip(com, [1.0, 0.5, 0.0])) < 1e-12
    planar = [a_g[2], a_g[3], a_g[4]]
    assert maxdiff(planar, [[0.5, 0.5], [-1.0, -1.0], [2.0, 0.0]]) < 1e-12
    assert maxdiff([a_g[0], a_g[1], a_g[5]], [[0.0, 0.0]] * 3) < 1e-12
    h = centroidal_momentum(model, q, [1.0, 1.0])
    assert max(abs(x - y) for x, y in zip(h, [0.0, 0.0, 1.0, -2.0, 2.0, 0.0])) < 1e-12


def test_against_sum_of_link_momenta():
    rng = random.Random(1)
    for n, floating in ((5, False), (7, False), (4, True)):
        model = random_model(rng, n, floating)
        q = [rng.uniform(-1.5, 1.5) for _ in range(model.n)]
        qd = [rng.uniform(-1, 1) for _ in range(model.n)]
        got = centroidal_momentum(model, q, qd)
        want = momentum_brute(model, q, qd)
        assert max(abs(x - y) for x, y in zip(got, want)) < 1e-6


def test_linear_rows_are_mass_times_com_jacobian():
    rng = random.Random(2)
    model = random_model(rng, 6, True)
    q = [rng.uniform(-1.5, 1.5) for _ in range(model.n)]
    a_g, m, _ = centroidal_momentum_matrix(model, q)
    j_com = rbm.num_jacobian(lambda x: com_of(model, x), q)
    assert maxdiff(a_g[3:], rbm.scale(j_com, m)) < 1e-6


def test_floating_base_columns():
    """The three prismatic base columns give (0, m e_k): moving the whole robot adds only linear momentum."""
    rng = random.Random(3)
    model = random_model(rng, 4, True)
    q = [rng.uniform(-1.5, 1.5) for _ in range(model.n)]
    a_g, m, _ = centroidal_momentum_matrix(model, q)
    for k in range(3):
        col = [row[k] for row in a_g]
        want = [0.0] * 6
        want[3 + k] = m
        assert max(abs(x - y) for x, y in zip(col, want)) < 1e-12


def test_bad_input():
    model = Model()
    model.add_body(-1, rbm.eye(4), Z_AXIS, rbm.zeros(6, 6))
    with pytest.raises(ValueError):
        centroidal_momentum_matrix(model, [0.0])
    with pytest.raises(ValueError):
        centroidal_momentum_matrix(planar_2r(), [0.0])
