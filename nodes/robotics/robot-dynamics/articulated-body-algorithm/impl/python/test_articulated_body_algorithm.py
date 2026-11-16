# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/articulated-body-algorithm/. The authors are listed in prov/0W0KC6.jsonl.
"""Tests of ABA against RNEA, a dense mass matrix solve and energy conservation."""

import math
import random

import pytest

import rbm
from articulated_body_algorithm import (
    GRAVITY,
    Model,
    aba,
    cross_force,
    cross_motion,
    joint_transform,
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


def rnea_ref(model, q, qd, qdd, gravity, f_ext=None):
    """Plain recursive Newton-Euler inverse dynamics, used as the reference."""
    n = model.n
    a_base = [0.0, 0.0, 0.0] + [-x for x in gravity]
    xs, v, a, f = [None] * n, [None] * n, [None] * n, [None] * n
    for i in range(n):
        p = model.parent[i]
        s = model.screw[i]
        xs[i] = joint_transform(model, i, q[i])
        vj = rbm.scale(s, qd[i])
        v[i] = rbm.add(rbm.matvec(xs[i], [0.0] * 6 if p < 0 else v[p]), vj)
        a[i] = rbm.add(rbm.add(rbm.matvec(xs[i], a_base if p < 0 else a[p]), rbm.scale(s, qdd[i])),
                       cross_motion(v[i], vj))
        f[i] = rbm.add(rbm.matvec(model.inertia[i], a[i]),
                       cross_force(v[i], rbm.matvec(model.inertia[i], v[i])))
        if f_ext is not None and f_ext[i] is not None:
            f[i] = rbm.sub(f[i], f_ext[i])
    tau = [0.0] * n
    for i in range(n - 1, -1, -1):
        tau[i] = rbm.dot(model.screw[i], f[i])
        if model.parent[i] >= 0:
            f[model.parent[i]] = rbm.add(f[model.parent[i]], rbm.matvec(rbm.transpose(xs[i]), f[i]))
    return tau


def dense_forward_dynamics(model, q, qd, tau, gravity):
    """Build M from n + 1 RNEA calls and solve M qdd = tau - bias by elimination."""
    n = model.n
    zero = [0.0] * n
    bias = rnea_ref(model, q, qd, zero, gravity)
    cols = []
    for k in range(n):
        e = [1.0 if j == k else 0.0 for j in range(n)]
        cols.append(rnea_ref(model, q, zero, e, [0.0, 0.0, 0.0]))
    return rbm.solve(rbm.transpose(cols), rbm.sub(tau, bias))


def potential(model, q, g):
    total = 0.0
    pose = []
    for i in range(model.n):
        local = rbm.mul(model.tree[i], rbm.se3_exp(rbm.scale(model.screw[i], q[i])))
        p = model.parent[i]
        pose.append(local if p < 0 else rbm.mul(pose[p], local))
        inertia = model.inertia[i]
        mass = inertia[5][5]
        com = [inertia[2][4] / mass, inertia[0][5] / mass, inertia[1][3] / mass]
        total -= mass * rbm.dot(g, rbm.T_apply(pose[i], com))
    return total


def test_2r_check_values():
    model = planar_2r()
    qdd = aba(model, [0.0, math.pi / 2], [1.0, 1.0], [0.0, 0.0], [0.0, 0.0, 0.0])
    assert abs(qdd[0] - 2.0) < 1e-12 and abs(qdd[1] + 3.0) < 1e-12
    qdd = aba(model, [0.0, 0.0], [0.0, 0.0], [29.43, 9.81], [0.0, -9.81, 0.0])
    assert max(abs(x) for x in qdd) < 1e-12


def test_inverts_rnea_on_random_trees():
    rng = random.Random(1)
    for n in (1, 5, 6, 7):
        model = random_model(rng, n)
        for _ in range(3):
            q = [rng.uniform(-2, 2) for _ in range(n)]
            qd = [rng.uniform(-1.5, 1.5) for _ in range(n)]
            tau = [rng.uniform(-5, 5) for _ in range(n)]
            f_ext = [[rng.uniform(-1, 1) for _ in range(6)] if rng.random() < 0.4 else None for _ in range(n)]
            qdd = aba(model, q, qd, tau, GRAVITY, f_ext)
            back = rnea_ref(model, q, qd, qdd, GRAVITY, f_ext)
            assert max(abs(x - y) for x, y in zip(back, tau)) < 1e-9
            qdd_ref = [rng.uniform(-3, 3) for _ in range(n)]
            tau_ref = rnea_ref(model, q, qd, qdd_ref, GRAVITY, f_ext)
            got = aba(model, q, qd, tau_ref, GRAVITY, f_ext)
            assert max(abs(x - y) for x, y in zip(got, qdd_ref)) < 1e-9


def test_against_dense_solve():
    rng = random.Random(2)
    model = random_model(rng, 7)
    q = [rng.uniform(-2, 2) for _ in range(7)]
    qd = [rng.uniform(-1, 1) for _ in range(7)]
    tau = [rng.uniform(-5, 5) for _ in range(7)]
    got = aba(model, q, qd, tau)
    want = dense_forward_dynamics(model, q, qd, tau, GRAVITY)
    assert max(abs(x - y) for x, y in zip(got, want)) < 1e-9


def test_serial_chain_and_star():
    rng = random.Random(3)
    for parents in ([-1, 0, 1, 2, 3, 4], [-1, 0, 0, 0, 0, 0], [-1, -1, -1, 2, 2]):
        model = random_model(rng, len(parents), parents)
        n = model.n
        q = [rng.uniform(-2, 2) for _ in range(n)]
        qd = [rng.uniform(-1, 1) for _ in range(n)]
        tau = [rng.uniform(-5, 5) for _ in range(n)]
        qdd = aba(model, q, qd, tau)
        assert max(abs(x - y) for x, y in zip(rnea_ref(model, q, qd, qdd, GRAVITY), tau)) < 1e-9


def test_energy_is_constant_without_torque():
    """RK4 with dt = 5e-3 for 120 steps; tau = 0 and no friction. The drift must stay below 1e-6 J."""
    rng = random.Random(6)
    model = random_model(rng, 3, [-1, 0, 1])
    q = [0.3, -0.5, 0.8]
    qd = [0.5, -0.4, 0.2]
    zero = [0.0] * 3

    def deriv(x, v):
        return v, aba(model, x, v, zero)

    def energy(x, v):
        ke = 0.5 * rbm.dot(v, rnea_ref(model, x, [0.0] * 3, v, [0.0] * 3))  # (1/2) v^T M v
        return ke + potential(model, x, GRAVITY)

    e0 = energy(q, qd)
    dt = 5e-3
    for _ in range(120):
        k1 = deriv(q, qd)
        k2 = deriv(rbm.add(q, rbm.scale(k1[0], dt / 2)), rbm.add(qd, rbm.scale(k1[1], dt / 2)))
        k3 = deriv(rbm.add(q, rbm.scale(k2[0], dt / 2)), rbm.add(qd, rbm.scale(k2[1], dt / 2)))
        k4 = deriv(rbm.add(q, rbm.scale(k3[0], dt)), rbm.add(qd, rbm.scale(k3[1], dt)))
        q = [x + dt / 6 * (a + 2 * b + 2 * c + d) for x, a, b, c, d in zip(q, k1[0], k2[0], k3[0], k4[0])]
        qd = [x + dt / 6 * (a + 2 * b + 2 * c + d) for x, a, b, c, d in zip(qd, k1[1], k2[1], k3[1], k4[1])]
    assert max(abs(x - y) for x, y in zip(q, [0.3, -0.5, 0.8])) > 0.05
    assert abs(energy(q, qd) - e0) < 1e-6


def test_massless_body_is_rejected():
    model = Model()
    model.add_body(-1, rbm.eye(4), Z_AXIS, rbm.zeros(6, 6))
    with pytest.raises(ValueError):
        aba(model, [0.0], [0.0], [1.0])
    with pytest.raises(ValueError):
        aba(planar_2r(), [0.0], [0.0, 0.0], [0.0, 0.0])
