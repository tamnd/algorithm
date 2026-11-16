# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rigid-body-dynamics-derivatives/. The authors are listed in prov/M6C9BY.jsonl.
"""Tests of the analytical derivatives against central finite differences (h = 1e-6, tolerance 1e-6)."""

import math
import random

import pytest

import rbm
from rigid_body_dynamics_derivatives import (
    GRAVITY,
    Model,
    forward_dynamics_derivatives,
    rnea,
    rnea_derivatives,
    spatial_inertia,
)

Z_AXIS = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
G_PLANE = [0.0, -9.81, 0.0]
TOL = 1e-6


def planar_2r():
    """2R arm in the x-y plane, links of 1 m, point masses of 1 kg at the link ends."""
    model = Model()
    point = spatial_inertia(1.0, [1.0, 0.0, 0.0], rbm.zeros(3, 3))
    model.add_body(-1, rbm.eye(4), Z_AXIS, point)
    model.add_body(0, rbm.make_T(rbm.eye(3), [1.0, 0.0, 0.0]), Z_AXIS, point)
    return model


def closed_form_2r(q, qd, qdd, g=9.81):
    c1, c2, s2 = math.cos(q[0]), math.cos(q[1]), math.sin(q[1])
    c12 = math.cos(q[0] + q[1])
    t1 = (3 + 2 * c2) * qdd[0] + (1 + c2) * qdd[1] - s2 * (2 * qd[0] * qd[1] + qd[1] ** 2) + g * (2 * c1 + c12)
    t2 = (1 + c2) * qdd[0] + qdd[1] + s2 * qd[0] ** 2 + g * c12
    return [t1, t2]


def random_model(rng, n, parents=None):
    model = Model()
    for i in range(n):
        parent = rng.randrange(-1, i) if parents is None else parents[i]
        tree = rbm.se3_exp([rng.uniform(-0.6, 0.6) for _ in range(6)])
        u = [rng.gauss(0.0, 1.0) for _ in range(3)]
        u = rbm.scale(u, 1.0 / rbm.norm(u))
        if rng.random() < 0.8:
            point = [rng.uniform(-0.3, 0.3) for _ in range(3)]
            screw = u + [-x for x in rbm.cross(u, point)]
        else:
            screw = [0.0, 0.0, 0.0] + u
        a = [[rng.uniform(-0.3, 0.3) for _ in range(3)] for _ in range(3)]
        ic = rbm.add(rbm.mul(a, rbm.transpose(a)), rbm.scale(rbm.eye(3), 0.05))
        com = [rng.uniform(-0.3, 0.3) for _ in range(3)]
        model.add_body(parent, tree, screw, spatial_inertia(rng.uniform(0.5, 2.0), com, ic))
    return model


def maxdiff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def numeric_id_jacobians(model, q, qd, qdd, g):
    return (rbm.num_jacobian(lambda x: rnea(model, x, qd, qdd, g), q),
            rbm.num_jacobian(lambda x: rnea(model, q, x, qdd, g), qd),
            rbm.num_jacobian(lambda x: rnea(model, q, qd, x, g), qdd))


def test_2r_against_closed_form():
    rng = random.Random(1)
    model = planar_2r()
    for _ in range(10):
        q = [rng.uniform(-math.pi, math.pi) for _ in range(2)]
        qd = [rng.uniform(-2, 2) for _ in range(2)]
        qdd = [rng.uniform(-3, 3) for _ in range(2)]
        tau, d_q, d_qd, m = rnea_derivatives(model, q, qd, qdd, G_PLANE)
        assert max(abs(x - y) for x, y in zip(tau, closed_form_2r(q, qd, qdd))) < 1e-9
        assert maxdiff(d_q, rbm.num_jacobian(lambda x: closed_form_2r(x, qd, qdd), q)) < TOL
        assert maxdiff(d_qd, rbm.num_jacobian(lambda x: closed_form_2r(q, x, qdd), qd)) < TOL
        c2 = math.cos(q[1])
        assert maxdiff(m, [[3 + 2 * c2, 1 + c2], [1 + c2, 1.0]]) < 1e-12


def test_2r_hand_value():
    """At q = (0, pi/2), qd = (1, 1), qdd = 0 and no gravity: dtau/dqd = [[-2, -4], [2, 0]], dtau/dq = 0."""
    _, d_q, d_qd, _ = rnea_derivatives(planar_2r(), [0.0, math.pi / 2], [1.0, 1.0], [0.0, 0.0], [0.0] * 3)
    assert maxdiff(d_qd, [[-2.0, -4.0], [2.0, 0.0]]) < 1e-12
    assert maxdiff(d_q, [[0.0, 0.0], [0.0, 0.0]]) < 1e-12


def test_inverse_dynamics_derivatives_on_random_trees():
    rng = random.Random(2)
    for n in (1, 5, 7):
        model = random_model(rng, n)
        q = [rng.uniform(-2, 2) for _ in range(n)]
        qd = [rng.uniform(-1.5, 1.5) for _ in range(n)]
        qdd = [rng.uniform(-3, 3) for _ in range(n)]
        tau, d_q, d_qd, m = rnea_derivatives(model, q, qd, qdd)
        n_q, n_qd, n_qdd = numeric_id_jacobians(model, q, qd, qdd, GRAVITY)
        assert maxdiff(d_q, n_q) < TOL
        assert maxdiff(d_qd, n_qd) < TOL
        assert maxdiff(m, n_qdd) < TOL
        assert maxdiff(m, rbm.transpose(m)) < 1e-12


def test_forward_dynamics_derivatives():
    rng = random.Random(3)
    model = random_model(rng, 6, [-1, 0, 1, 1, 3, -1])

    def fd(q, qd, tau):
        n = model.n
        bias = rnea(model, q, qd, [0.0] * n)
        m = rnea_derivatives(model, q, qd, [0.0] * n)[3]
        return rbm.solve(m, rbm.sub(tau, bias))

    q = [rng.uniform(-2, 2) for _ in range(6)]
    qd = [rng.uniform(-1, 1) for _ in range(6)]
    tau = [rng.uniform(-3, 3) for _ in range(6)]
    qdd, d_q, d_qd, d_tau = forward_dynamics_derivatives(model, q, qd, tau)
    assert max(abs(x - y) for x, y in zip(rnea(model, q, qd, qdd), tau)) < 1e-9
    assert maxdiff(d_q, rbm.num_jacobian(lambda x: fd(x, qd, tau), q)) < TOL
    assert maxdiff(d_qd, rbm.num_jacobian(lambda x: fd(q, x, tau), qd)) < TOL
    assert maxdiff(d_tau, rbm.num_jacobian(lambda x: fd(q, qd, x), tau)) < TOL


def test_sparsity_follows_the_tree():
    """dtau_i/dq_k and dtau_i/dqd_k are 0 unless i and k lie on one path to the root."""
    rng = random.Random(4)
    parents = [-1, 0, 1, 0, 3, -1]
    model = random_model(rng, 6, parents)
    _, d_q, d_qd, _ = rnea_derivatives(model, [rng.uniform(-2, 2) for _ in range(6)],
                                       [rng.uniform(-1, 1) for _ in range(6)], [0.5] * 6)

    def path(i):
        out = set()
        while i >= 0:
            out.add(i)
            i = parents[i]
        return out

    for i in range(6):
        for k in range(6):
            if not (i in path(k) or k in path(i)):
                assert d_q[i][k] == 0.0 and d_qd[i][k] == 0.0


def test_bad_input():
    with pytest.raises(ValueError):
        rnea_derivatives(planar_2r(), [0.0], [0.0, 0.0], [0.0, 0.0])
