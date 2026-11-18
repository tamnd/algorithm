# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/position-based-dynamics/. The authors are listed in prov/AGQN60.jsonl.

"""Tests of position based dynamics against closed forms, a KKT solve and conservation laws."""

import math
import random

from anim import num_grad, solve
import position_based_dynamics as pbd


def test_example_two_particles():
    p = [(0.0, 0.0), (1.5, 0.0)]
    w = [1.0, 1.0 / 3.0]
    out = dict(pbd.project(pbd.Distance(0, 1, 1.0), p, w, 1.0))
    assert abs(out[0][0] - 0.375) < 1e-15 and abs(out[1][0] + 0.125) < 1e-15
    assert abs(1.0 * out[0][0] + 3.0 * out[1][0]) < 1e-15
    assert abs(math.dist(p[0], p[1]) - 1.0) < 1e-15


def test_distance_projection_closed_form():
    """Equations (10) and (11): dp1 = -w1 / (w1 + w2) (|p12| - d) n, dp2 = +w2 / (w1 + w2) (|p12| - d) n."""
    rng = random.Random(3)
    for _ in range(200):
        p = [(rng.uniform(-1, 1), rng.uniform(-1, 1)), (rng.uniform(-1, 1), rng.uniform(-1, 1))]
        w = [rng.uniform(0.1, 2.0), rng.uniform(0.1, 2.0)]
        d = rng.uniform(0.1, 1.0)
        dx, dy = p[0][0] - p[1][0], p[0][1] - p[1][1]
        ln = math.hypot(dx, dy)
        n = (dx / ln, dy / ln)
        e = ln - d
        want0 = (-w[0] / (w[0] + w[1]) * e * n[0], -w[0] / (w[0] + w[1]) * e * n[1])
        want1 = (w[1] / (w[0] + w[1]) * e * n[0], w[1] / (w[0] + w[1]) * e * n[1])
        got = dict(pbd.project(pbd.Distance(0, 1, d), p, w, 1.0))
        assert max(abs(got[0][k] - want0[k]) for k in range(2)) < 1e-14
        assert max(abs(got[1][k] - want1[k]) for k in range(2)) < 1e-14


def test_projection_equals_kkt_solve():
    """The correction is the smallest in the mass norm that zeroes the linearized constraint."""
    rng = random.Random(4)
    for _ in range(100):
        p = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(3)]
        w = [rng.uniform(0.2, 2.0) for _ in range(3)]
        c = pbd.Area(0, 1, 2, rng.uniform(-0.3, 0.3))
        cv = c.value(p)
        g = dict(c.gradients(p))
        # KKT: M dp - grad^T lam = 0, grad dp = -C, unknowns (dp in R^6, lam)
        a = [[0.0] * 7 for _ in range(7)]
        b = [0.0] * 7
        for i in range(3):
            for k in range(2):
                r = 2 * i + k
                a[r][r] = 1.0 / w[i]
                a[r][6] = -g[i][k]
                a[6][r] = g[i][k]
        b[6] = -cv
        sol = solve(a, b)
        q = list(p)
        got = dict(pbd.project(c, q, w, 1.0))
        for i in range(3):
            for k in range(2):
                assert abs(got[i][k] - sol[2 * i + k]) < 1e-11


def test_gradients_against_num_grad():
    rng = random.Random(5)
    for _ in range(30):
        p = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(3)]
        for c in (pbd.Distance(0, 2, 0.5), pbd.Area(0, 1, 2, 0.1), pbd.Ground(1, 0.2)):
            flat = [u for q in p for u in q]

            def f(z, c=c):
                return c.value([(z[0], z[1]), (z[2], z[3]), (z[4], z[5])])

            ng = num_grad(f, flat)
            g = dict(c.gradients(p))
            for i in range(3):
                gi = g.get(i, (0.0, 0.0))
                for k in range(2):
                    assert abs(gi[k] - ng[2 * i + k]) <= 1e-6 * max(1.0, abs(ng[2 * i + k]))


def test_torque_free_corrections():
    """Each projection keeps sum m dp = 0 and sum m p x dp = 0 at the positions where it acts (equations (1) and (2))."""
    rng = random.Random(6)
    for _ in range(100):
        p = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(3)]
        w = [rng.uniform(0.2, 2.0) for _ in range(3)]
        for c in (pbd.Distance(0, 1, 0.3), pbd.Area(0, 1, 2, 0.05)):
            q = list(p)
            corr = pbd.project(c, q, w, 1.0)
            lin = [sum(d[k] / w[i] for i, d in corr) for k in range(2)]
            ang = sum((p[i][0] * d[1] - p[i][1] * d[0]) / w[i] for i, d in corr)
            assert max(abs(lin[0]), abs(lin[1]), abs(ang)) < 1e-14


def test_linear_momentum_is_conserved():
    rng = random.Random(7)
    x = [(rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(12)]
    v = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(12)]
    w = [rng.uniform(0.5, 2.0) for _ in range(12)]
    cons = [pbd.Distance(i, j, 0.8 * math.dist(x[i], x[j])) for i in range(12) for j in range(i + 1, 12) if (i + j) % 3 == 0]
    cons += [pbd.Area(i, i + 1, i + 2, 0.0) for i in range(0, 9, 3)]
    p0 = pbd.momentum(x, v, w)
    for _ in range(50):
        x, v = pbd.pbd_step(x, v, w, cons, 0.01, 4, gravity=(0.0, 0.0), k_damping=0.1)
    p1 = pbd.momentum(x, v, w)
    scale = sum(math.hypot(*vi) / wi for vi, wi in zip(v, w))
    assert abs(p1[0] - p0[0]) < 1e-10 * scale and abs(p1[1] - p0[1]) < 1e-10 * scale


def test_spinning_dumbbell_loses_angular_momentum():
    """One step of a rigid rod spinning at omega multiplies L by 1 / sqrt(1 + (omega dt)^2)."""
    for omega, dt in ((1.0, 0.1), (1.0, 1.0), (3.0, 0.05)):
        x = [(-0.5, 0.0), (0.5, 0.0)]
        v = [(0.0, -0.5 * omega), (0.0, 0.5 * omega)]
        w = [1.0, 1.0]
        l0 = pbd.momentum(x, v, w)[2]
        x1, v1 = pbd.pbd_step(x, v, w, [pbd.Distance(0, 1, 1.0)], dt, 3, gravity=(0.0, 0.0))
        l1 = pbd.momentum(x1, v1, w)[2]
        assert abs(l1 / l0 - 1.0 / math.sqrt(1.0 + (omega * dt) ** 2)) < 1e-14


def test_damping_keeps_momenta():
    rng = random.Random(8)
    x = [(rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(8)]
    v = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(8)]
    w = [rng.uniform(0.5, 2.0) for _ in range(8)]
    vd = pbd.damp_velocities(x, v, w, 0.7)
    a, b = pbd.momentum(x, v, w), pbd.momentum(x, vd, w)
    assert max(abs(a[k] - b[k]) for k in range(3)) < 1e-12
    vr = pbd.damp_velocities(x, v, w, 1.0)
    # k_damping = 1 leaves a rigid motion: every pair keeps its distance to first order
    for i in range(8):
        for j in range(8):
            dx = (x[i][0] - x[j][0], x[i][1] - x[j][1])
            dv = (vr[i][0] - vr[j][0], vr[i][1] - vr[j][1])
            assert abs(dx[0] * dv[0] + dx[1] * dv[1]) < 1e-12


def test_sweep_stiffness_gives_k_after_n_sweeps():
    """For one particle on a pinned rod along x, n_s sweeps leave the error (1 - k) e."""
    for k in (0.1, 0.5, 0.9):
        for ns in (1, 3, 10):
            p = [(0.0, 0.0), (1.5, 0.0)]
            c = pbd.Distance(0, 1, 1.0, stiffness=k)
            kp = pbd.sweep_stiffness(k, ns)
            for _ in range(ns):
                pbd.project(c, p, [0.0, 1.0], kp)
            assert abs(c.value(p) - (1.0 - k) * 0.5) < 1e-12


def test_pinned_particle_and_ground():
    x, v, w, cons = pbd.chain(6, 0.2)
    for _ in range(200):
        x, v = pbd.pbd_step(x, v, w, cons, 1.0 / 60.0, 10, ground=-0.5)
        assert x[0] == (0.0, 0.0)
        assert min(p[1] for p in x) >= -0.5 - 1e-12


def test_residual_decreases_with_iterations():
    """The stretch of a falling chain depends on the iteration count: the reason for XPBD."""
    stretch = []
    for it in (1, 5, 50):
        x, v, w, cons = pbd.chain(11, 0.1)
        for _ in range(300):
            x, v = pbd.pbd_step(x, v, w, cons, 1.0 / 60.0, it)
        stretch.append(sum(math.dist(x[i], x[i + 1]) for i in range(10)) - 1.0)
    assert stretch[0] > stretch[1] > stretch[2] > 0.0
    assert stretch[0] > 0.1 and stretch[2] < 0.002


def test_free_fall_is_symplectic_euler():
    x, v, w = [(0.0, 0.0)], [(0.0, 0.0)], [1.0]
    for _ in range(10):
        x, v = pbd.pbd_step(x, v, w, [], 0.1, 1)
    assert abs(x[0][1] + 5.3955) < 1e-12
