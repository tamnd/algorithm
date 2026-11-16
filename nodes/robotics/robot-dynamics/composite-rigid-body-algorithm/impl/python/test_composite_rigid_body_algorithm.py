# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/composite-rigid-body-algorithm/. The authors are listed in prov/7BWY71.jsonl.
"""Tests of CRBA against the 2R closed form, RNEA columns and the kinetic energy."""

import math
import random

import pytest

import rbm
from composite_rigid_body_algorithm import (
    GRAVITY,
    Model,
    cross_force,
    cross_motion,
    crba,
    forward_dynamics,
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


def rnea_ref(model, q, qd, qdd, gravity):
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
    tau = [0.0] * n
    for i in range(n - 1, -1, -1):
        tau[i] = rbm.dot(model.screw[i], f[i])
        if model.parent[i] >= 0:
            f[model.parent[i]] = rbm.add(f[model.parent[i]], rbm.matvec(rbm.transpose(xs[i]), f[i]))
    return tau


def fk(model, q):
    out = []
    for i in range(model.n):
        local = rbm.mul(model.tree[i], rbm.se3_exp(rbm.scale(model.screw[i], q[i])))
        p = model.parent[i]
        out.append(local if p < 0 else rbm.mul(out[p], local))
    return out


def kinetic_energy_brute(model, q, qd, h=1e-6):
    """Sum of (1/2) V_i^T I_i V_i, with V_i from finite differences of the poses."""
    poses = fk(model, q)
    plus = fk(model, rbm.add(q, rbm.scale(qd, h)))
    minus = fk(model, rbm.sub(q, rbm.scale(qd, h)))
    total = 0.0
    for t, tp, tm, inertia in zip(poses, plus, minus, model.inertia):
        tdot = rbm.scale(rbm.sub(tp, tm), 0.5 / h)
        twist = rbm.vee6(rbm.mul(rbm.T_inv(t), tdot))
        total += 0.5 * rbm.dot(twist, rbm.matvec(inertia, twist))
    return total


def potential(model, q, g):
    total = 0.0
    for pose, inertia in zip(fk(model, q), model.inertia):
        mass = inertia[5][5]
        com = [inertia[2][4] / mass, inertia[0][5] / mass, inertia[1][3] / mass]
        total -= mass * rbm.dot(g, rbm.T_apply(pose, com))
    return total


def maxdiff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def test_2r_closed_form():
    rng = random.Random(1)
    model = planar_2r()
    for _ in range(30):
        q = [rng.uniform(-math.pi, math.pi) for _ in range(2)]
        c2 = math.cos(q[1])
        assert maxdiff(crba(model, q), [[3 + 2 * c2, 1 + c2], [1 + c2, 1.0]]) < 1e-12


def test_2r_forward_dynamics_check_value():
    qdd = forward_dynamics(planar_2r(), [0.0, math.pi / 2], [1.0, 1.0], [0.0, 0.0], [0.0, 0.0, 0.0])
    assert abs(qdd[0] - 2.0) < 1e-12 and abs(qdd[1] + 3.0) < 1e-12


def test_columns_against_rnea():
    rng = random.Random(2)
    zero3 = [0.0, 0.0, 0.0]
    for n in (5, 6, 7):
        model = random_model(rng, n)
        q = [rng.uniform(-2, 2) for _ in range(n)]
        h = crba(model, q)
        zero = [0.0] * n
        for k in range(n):
            e = [1.0 if j == k else 0.0 for j in range(n)]
            col = rnea_ref(model, q, zero, e, zero3)
            assert max(abs(h[r][k] - col[r]) for r in range(n)) < 1e-12


def test_symmetric_positive_definite_and_kinetic_energy():
    rng = random.Random(3)
    for n in (5, 7):
        model = random_model(rng, n)
        q = [rng.uniform(-2, 2) for _ in range(n)]
        qd = [rng.uniform(-1, 1) for _ in range(n)]
        h = crba(model, q)
        assert maxdiff(h, rbm.transpose(h)) == 0.0
        rbm.cholesky(h)
        ke = 0.5 * rbm.dot(qd, rbm.matvec(h, qd))
        assert abs(ke - kinetic_energy_brute(model, q, qd)) < 1e-8


def test_branch_induced_sparsity():
    rng = random.Random(4)
    parents = [-1, 0, 1, 0, 3, -1]
    model = random_model(rng, 6, parents)
    h = crba(model, [rng.uniform(-2, 2) for _ in range(6)])

    def path(i):
        out = set()
        while i >= 0:
            out.add(i)
            i = parents[i]
        return out

    for i in range(6):
        for j in range(6):
            related = i in path(j) or j in path(i)
            assert (h[i][j] == 0.0) == (not related)


def test_forward_dynamics_inverts_rnea():
    rng = random.Random(5)
    model = random_model(rng, 6)
    for _ in range(5):
        q = [rng.uniform(-2, 2) for _ in range(6)]
        qd = [rng.uniform(-1, 1) for _ in range(6)]
        tau = [rng.uniform(-3, 3) for _ in range(6)]
        qdd = forward_dynamics(model, q, qd, tau)
        assert max(abs(x - y) for x, y in zip(rnea_ref(model, q, qd, qdd, GRAVITY), tau)) < 1e-9


def test_energy_is_constant_without_torque():
    """RK4 with dt = 5e-3 for 120 steps; tau = 0 and no friction. The drift must stay below 1e-6 J."""
    rng = random.Random(6)
    model = random_model(rng, 3, [-1, 0, 1])
    q = [0.3, -0.5, 0.8]
    qd = [0.5, -0.4, 0.2]
    zero = [0.0] * 3

    def deriv(x, v):
        return v, forward_dynamics(model, x, v, zero)

    def energy(x, v):
        return 0.5 * rbm.dot(v, rbm.matvec(crba(model, x), v)) + potential(model, x, GRAVITY)

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


def test_bad_input():
    with pytest.raises(ValueError):
        crba(planar_2r(), [0.0])
