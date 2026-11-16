# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-newton-euler-algorithm/. The authors are listed in prov/8QXENF.jsonl.
"""Tests of RNEA against the closed form of the 2R arm and an Euler-Lagrange reference."""

import math
import random

import pytest

import rbm
from recursive_newton_euler_algorithm import GRAVITY, Model, rnea, spatial_inertia

G_PLANE = [0.0, -9.81, 0.0]
Z_AXIS = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]


def planar_2r():
    """2R arm in the x-y plane (y up), links of 1 m, point masses of 1 kg at the link ends."""
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


def random_model(rng, n):
    model = Model()
    for i in range(n):
        parent = rng.randrange(-1, i)
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


# ------------------------------------------------- Euler-Lagrange reference


def fk(model, q):
    """World pose of every body frame."""
    out = []
    for i in range(model.n):
        local = rbm.mul(model.tree[i], rbm.se3_exp(rbm.scale(model.screw[i], q[i])))
        p = model.parent[i]
        out.append(local if p < 0 else rbm.mul(out[p], local))
    return out


def body_jacobians(model, q):
    """J_i with V_i = J_i qd, the body twist of body i in its own frame."""
    poses = fk(model, q)
    jac = []
    for i in range(model.n):
        cols = [[0.0] * 6 for _ in range(model.n)]
        k = i
        inv_i = rbm.T_inv(poses[i])
        while k >= 0:
            cols[k] = rbm.matvec(rbm.adjoint(rbm.mul(inv_i, poses[k])), model.screw[k])
            k = model.parent[k]
        jac.append(rbm.transpose(cols))
    return jac


def mass_matrix_ref(model, q):
    m = rbm.zeros(model.n, model.n)
    for j, inertia in zip(body_jacobians(model, q), model.inertia):
        m = rbm.add(m, rbm.mul(rbm.transpose(j), rbm.mul(inertia, j)))
    return m


def potential(model, q, g):
    total = 0.0
    for pose, inertia in zip(fk(model, q), model.inertia):
        mass = inertia[5][5]
        com = [inertia[2][4] / mass, inertia[0][5] / mass, inertia[1][3] / mass]
        total -= mass * rbm.dot(g, rbm.T_apply(pose, com))
    return total


def tau_ref(model, q, qd, qdd, g, f_ext=None, h=1e-6):
    """M qdd + (dM/dt) qd - (1/2) d(qd^T M qd)/dq + dV/dq - sum J_i^T f_i."""
    n = model.n
    m = mass_matrix_ref(model, q)
    m_dot = rbm.scale(rbm.sub(mass_matrix_ref(model, rbm.add(q, rbm.scale(qd, h))),
                              mass_matrix_ref(model, rbm.sub(q, rbm.scale(qd, h)))), 0.5 / h)
    out = rbm.add(rbm.matvec(m, qdd), rbm.matvec(m_dot, qd))
    for k in range(n):
        qp, qm = list(q), list(q)
        qp[k] += h
        qm[k] -= h
        ke_p = rbm.dot(qd, rbm.matvec(mass_matrix_ref(model, qp), qd))
        ke_m = rbm.dot(qd, rbm.matvec(mass_matrix_ref(model, qm), qd))
        out[k] += -0.25 * (ke_p - ke_m) / h + (potential(model, qp, g) - potential(model, qm, g)) / (2 * h)
    if f_ext is not None:
        for j, f in zip(body_jacobians(model, q), f_ext):
            out = rbm.sub(out, rbm.matvec(rbm.transpose(j), f))
    return out


# ------------------------------------------------- tests


def test_helper_self_test():
    assert rbm.self_test()


def test_2r_check_values():
    model = planar_2r()
    tau = rnea(model, [0.3, 0.7], [0.5, -1.2], [2.0, -1.0], G_PLANE)
    assert abs(tau[0] - 31.184) < 1e-3 and abs(tau[1] - 7.991) < 1e-3
    tau = rnea(model, [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], G_PLANE)
    assert abs(tau[0] - 29.43) < 1e-12 and abs(tau[1] - 9.81) < 1e-12
    tau = rnea(model, [0.0, math.pi / 2], [1.0, 1.0], [0.0, 0.0], [0.0, 0.0, 0.0])
    assert abs(tau[0] + 3.0) < 1e-12 and abs(tau[1] - 1.0) < 1e-12


def test_2r_closed_form_random():
    rng = random.Random(1)
    model = planar_2r()
    for _ in range(50):
        q = [rng.uniform(-math.pi, math.pi) for _ in range(2)]
        qd = [rng.uniform(-3, 3) for _ in range(2)]
        qdd = [rng.uniform(-5, 5) for _ in range(2)]
        got = rnea(model, q, qd, qdd, G_PLANE)
        want = closed_form_2r(q, qd, qdd)
        assert max(abs(x - y) for x, y in zip(got, want)) < 1e-9


def test_default_gravity_is_z_down():
    model = Model()
    model.add_body(-1, rbm.eye(4), [0.0, 0.0, 0.0, 0.0, 0.0, 1.0], spatial_inertia(2.0, [0.0] * 3, rbm.eye(3)))
    assert abs(rnea(model, [0.4], [1.0], [0.0])[0] - 2.0 * 9.81) < 1e-12
    assert abs(rnea(model, [0.4], [1.0], [1.5])[0] - 2.0 * (9.81 + 1.5)) < 1e-12


def test_random_trees_against_euler_lagrange():
    rng = random.Random(2)
    for n in (5, 6, 7):
        model = random_model(rng, n)
        q = [rng.uniform(-1.5, 1.5) for _ in range(n)]
        qd = [rng.uniform(-1.0, 1.0) for _ in range(n)]
        qdd = [rng.uniform(-2.0, 2.0) for _ in range(n)]
        f_ext = [[rng.uniform(-1, 1) for _ in range(6)] if rng.random() < 0.5 else None for _ in range(n)]
        got = rnea(model, q, qd, qdd, GRAVITY, f_ext)
        want = tau_ref(model, q, qd, qdd, GRAVITY, [f or [0.0] * 6 for f in f_ext])
        assert max(abs(x - y) for x, y in zip(got, want)) < 1e-6


def test_mass_matrix_from_rnea_is_symmetric_positive_definite():
    rng = random.Random(3)
    model = random_model(rng, 6)
    q = [rng.uniform(-2, 2) for _ in range(6)]
    zero = [0.0] * 6
    g0 = rnea(model, q, zero, zero)
    cols = []
    for k in range(6):
        e = [1.0 if j == k else 0.0 for j in range(6)]
        cols.append(rbm.sub(rnea(model, q, zero, e), g0))
    m = rbm.transpose(cols)
    assert max(abs(m[i][j] - m[j][i]) for i in range(6) for j in range(6)) < 1e-12
    rbm.cholesky(m)
    ref = mass_matrix_ref(model, q)
    assert max(abs(m[i][j] - ref[i][j]) for i in range(6) for j in range(6)) < 1e-12


def test_bad_input():
    model = planar_2r()
    with pytest.raises(ValueError):
        rnea(model, [0.0], [0.0, 0.0], [0.0, 0.0])
    with pytest.raises(ValueError):
        model.add_body(5, rbm.eye(4), Z_AXIS, rbm.eye(6))
