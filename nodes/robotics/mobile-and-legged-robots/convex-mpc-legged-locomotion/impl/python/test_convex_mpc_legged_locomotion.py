# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convex-mpc-legged-locomotion/. The authors are listed in prov/01NY1Z.jsonl.
# The closed-loop test integrates the full rigid body with semi-implicit Euler
# (rotation by so3_exp) at dt = 1e-3 s, at most 1000 steps.

import random

import rbm
from convex_mpc_legged_locomotion import (
    G,
    RigidBody,
    build_qp,
    convex_mpc,
    discretize,
    friction_rows,
    model_matrices,
    solve_qp,
)

M = 10.0
IB = [[0.1, 0.0, 0.0], [0.0, 0.25, 0.0], [0.0, 0.0, 0.3]]
FEET = [[0.2, 0.12, -0.3], [0.2, -0.12, -0.3], [-0.2, 0.12, -0.3], [-0.2, -0.12, -0.3]]
W = [20, 20, 5, 1, 1, 50, 0.5, 0.5, 0.5, 2, 2, 2, 0]
REF = [0, 0, 0, 0, 0, 0.3, 0, 0, 0, 0, 0, 0, G]


def test_zero_order_hold_matches_fine_integration():
    rng = random.Random(1)
    a, b = model_matrices(M, IB, 0.4, FEET)
    dt = 0.05
    ad, bd = discretize(a, b, dt)
    x = [rng.uniform(-1, 1) for _ in range(12)] + [G]
    u = [rng.uniform(-20, 20) for _ in range(12)]
    want = [p + q for p, q in zip(rbm.matvec(ad, x), rbm.matvec(bd, u))]
    # RK4 on x' = A x + B u with 100 steps.
    bu = rbm.matvec(b, u)

    def f(y):
        return [p + q for p, q in zip(rbm.matvec(a, y), bu)]

    h = dt / 100
    y = list(x)
    for _ in range(100):
        k1 = f(y)
        k2 = f([p + h / 2 * q for p, q in zip(y, k1)])
        k3 = f([p + h / 2 * q for p, q in zip(y, k2)])
        k4 = f([p + h * q for p, q in zip(y, k3)])
        y = [p + h / 6 * (q + 2 * r + 2 * s + t) for p, q, r, s, t in zip(y, k1, k2, k3, k4)]
    for p, q in zip(y, want):
        assert abs(p - q) < 1e-12


def test_standing_robot_puts_a_quarter_of_the_weight_on_each_foot():
    plan = [(0.0, FEET)] * 3
    forces, _, _ = convex_mpc(REF, [REF] * 3, plan, M, IB, 0.03, W, 1e-6, 0.6, 0.0, 150.0)
    for f in forces:
        assert abs(f[2] - M * G / 4) < 0.01 * M * G / 4
        assert abs(f[0]) < 1e-6 and abs(f[1]) < 1e-6


def small_qp(mu):
    feet = [FEET[0], FEET[3]]
    x0 = [0.05, -0.03, 0, 0, 0, 0.29, 0.4, 0, 0, 0, 0.8, -0.2, G]
    steps = [discretize(*model_matrices(M, IB, 0.0, feet), 0.04)] * 2
    hm, g, _ = build_qp(x0, [REF] * 2, steps, W, 1e-4)
    rows, h = friction_rows(steps, mu, 2.0, 50.0)
    return hm, g, rows, h


def test_kkt_conditions_hold():
    hm, g, rows, h = small_qp(0.1)
    u, z = solve_qp(hm, g, rows, h)
    n = len(u)
    grad = [p + q for p, q in zip(rbm.matvec(hm, u), g)]
    for row, zi in zip(rows, z):
        for i, c in row:
            grad[i] += c * zi
    scale = max(abs(v) for v in g)
    assert max(abs(v) for v in grad) < 1e-8 * scale
    active = 0
    for row, hi, zi in zip(rows, h, z):
        slack = hi - sum(c * u[i] for i, c in row)
        assert slack > -1e-8 and zi > -1e-12
        assert abs(slack * zi) < 1e-6
        active += zi > 1e-6
    # The friction pyramid binds for this push.
    assert active >= 4
    assert n == 12


def test_matches_hildreth_dual_coordinate_ascent():
    hm, g, rows, h = small_qp(0.1)
    u, _ = solve_qp(hm, g, rows, h)
    n, m = len(g), len(rows)
    gm = [[0.0] * n for _ in range(m)]
    for i, row in enumerate(rows):
        for j, c in row:
            gm[i][j] = c
    hinv = rbm.inv(hm)
    hg = rbm.matvec(hinv, g)
    ghi = rbm.mul(gm, hinv)
    p = rbm.mul(ghi, rbm.transpose(gm))
    d = [hi + v for hi, v in zip(h, rbm.matvec(gm, hg))]
    lam = [0.0] * m
    for _ in range(1000):
        for i in range(m):
            r = sum(p[i][j] * lam[j] for j in range(m)) + d[i]
            lam[i] = max(0.0, lam[i] - r / p[i][i])
    uh = [-a - b for a, b in zip(hg, rbm.matvec(rbm.transpose(ghi), lam))]
    for a, b in zip(u, uh):
        assert abs(a - b) < 1e-5 * max(abs(v) for v in u)


def test_push_recovery_on_the_full_rigid_body():
    feet_w = [[a, b, c + 0.3] for a, b, c in FEET]
    body = RigidBody(M, IB, [0.0, 0.0, 0.3], rbm.eye(3), [0.0, 0.5, 0.0], [0.5, 0.0, 0.2])
    mu, f_max, dt_mpc, horizon = 0.6, 150.0, 0.05, 3
    steps = 0
    for _ in range(20):
        x = body.state()
        rel = [[a - b for a, b in zip(f, body.p)] for f in feet_w]
        forces, _, _ = convex_mpc(x, [REF] * horizon, [(x[2], rel)] * horizon, M, IB, dt_mpc, W, 1e-6, mu, 0.0, f_max)
        for f in forces:
            assert -1e-6 <= f[2] <= f_max + 1e-6
            assert abs(f[0]) <= mu * f[2] + 1e-6 and abs(f[1]) <= mu * f[2] + 1e-6
        for _ in range(50):
            body.step(feet_w, forces, 1e-3)
            steps += 1
    assert steps <= 1000
    x = body.state()
    # Attitude and speed are back near the reference; the sideways drift stays small.
    assert max(abs(v) for v in x[0:3]) < 0.005
    assert max(abs(v) for v in x[6:12]) < 0.01
    assert abs(x[4]) < 0.05 and abs(x[5] - 0.3) < 0.005
