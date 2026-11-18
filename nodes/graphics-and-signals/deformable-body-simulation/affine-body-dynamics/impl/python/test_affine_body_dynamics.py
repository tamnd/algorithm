# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affine-body-dynamics/. The authors are listed in prov/J2K8MW.jsonl.

"""Tests of affine body dynamics: the affine map, the mass matrix, the orthogonality energy, Newton and contact."""

import math
import random

from anim import num_grad
import affine_body_dynamics as ab

GROUND = [((0.0, 1.0), 0.0)]


def spin_rate(q, w):
    """qdot of a rotation at rate w: Adot = W A with W = [[0, -w], [w, 0]]."""
    return [0.0, 0.0, -w * q[4], -w * q[5], w * q[2], w * q[3]]


def is_psd(h, tol):
    lam, _ = ab.jacobi_eigen(h)
    return min(lam) >= -tol


def test_affine_map_is_j_times_q():
    rng = random.Random(1)
    for _ in range(50):
        q = [rng.uniform(-2, 2) for _ in range(6)]
        xb = (rng.uniform(-1, 1), rng.uniform(-1, 1))
        j = ab.jac(xb)
        jq = [sum(j[r][c] * q[c] for c in range(6)) for r in range(2)]
        x = ab.world(q, xb)
        assert max(abs(a - b) for a, b in zip(jq, x)) < 1e-14


def test_kinetic_energy_identity_and_constant_mass():
    rng = random.Random(2)
    b = ab.box(0.4, 0.2, 1000.0, 1e5, [], 1e-3, 1.0, refine=2)
    for _ in range(20):
        qd = [rng.uniform(-3, 3) for _ in range(6)]
        t1 = 0.5 * sum(qd[r] * b.mass[r][c] * qd[c] for r in range(6) for c in range(6))
        t2 = sum(0.5 * m * sum(u * u for u in ab.world(qd, xb)) for xb, m in zip(b.xb, b.m))
        assert abs(t1 - t2) < 1e-10 * t2
    total = sum(b.m)
    assert abs(b.mass[0][0] - total) < 1e-12 and abs(b.mass[0][2]) < 1e-12 and abs(b.mass[1][4]) < 1e-12


def test_orthogonality_energy_vanishes_on_rotations_and_matches_num_grad():
    rng = random.Random(3)
    for _ in range(10):
        q = ab.rest_state((rng.uniform(-1, 1), rng.uniform(-1, 1)), rng.uniform(-3, 3))
        e, g, _ = ab.ortho_energy(q, 7.0)
        assert e < 1e-24 and max(abs(c) for c in g) < 1e-12
    e, g, _ = ab.ortho_energy([0.0, 0.0, 1.0, 0.0, 0.0, -1.0], 7.0)
    assert e == 0.0 and max(abs(c) for c in g) == 0.0
    for _ in range(10):
        q = [0.0, 0.0] + [rng.uniform(-1.5, 1.5) for _ in range(4)]
        e, g, h = ab.ortho_energy(q, 3.0)
        ng = num_grad(lambda a: ab.ortho_energy([0.0, 0.0] + a, 3.0)[0], q[2:])
        assert max(abs(x - y) for x, y in zip(g, ng)) < 1e-5 * max(1.0, max(abs(c) for c in g))
        for r in range(4):
            col = num_grad(lambda a, r=r: ab.ortho_energy([0.0, 0.0] + a, 3.0)[1][r], q[2:])
            assert max(abs(col[c] - h[r][c]) for c in range(4)) < 1e-4 * max(1.0, max(map(abs, h[r])))


def test_psd_projection():
    rng = random.Random(4)
    for _ in range(20):
        q = [0.0, 0.0] + [rng.uniform(-1.0, 1.0) for _ in range(4)]
        _, _, h = ab.ortho_energy(q, 1.0)
        lam, v = ab.jacobi_eigen(h)
        back = [[sum(lam[k] * v[i][k] * v[j][k] for k in range(4)) for j in range(4)] for i in range(4)]
        assert max(abs(back[i][j] - h[i][j]) for i in range(4) for j in range(4)) < 1e-10
        p = ab.project_psd(h)
        assert is_psd(p, 1e-10)
        if min(lam) >= 0.0:
            assert max(abs(p[i][j] - h[i][j]) for i in range(4) for j in range(4)) < 1e-10
    _, _, h = ab.ortho_energy([0.0, 0.0, 0.3, 0.0, 0.0, 0.3], 1.0)
    assert not is_psd(h, 0.0)


def test_energy_gradient_against_num_grad_with_active_contact():
    b = ab.box(0.4, 0.2, 1000.0, 1e3, GROUND, 0.01, 2.0)
    q = ab.rest_state((0.0, 0.104), 0.02)
    qt = [c + 0.001 for c in q]
    assert ab.min_gap(b, q) < b.dhat
    g, _ = ab.gradient_and_hessian(b, q, qt, 0.01)
    ng = num_grad(lambda z: ab.energy(b, z, qt, 0.01), q, 1e-8)
    assert max(abs(x - y) for x, y in zip(g, ng)) < 1e-5 * max(abs(c) for c in g)


def test_drop_with_spin_never_penetrates_and_energy_decreases():
    b = ab.box(0.4, 0.2, 1000.0, 1e7, GROUND, 1e-3, 1.0)
    q = ab.rest_state((0.0, 1.0), 0.3)
    qd = spin_rate(q, 10.0)
    qd[1] = -5.0
    for _ in range(60):
        hist = []
        q, qd, _ = ab.abd_step(b, q, qd, 0.01, history=hist)
        assert all(y <= x for x, y in zip(hist, hist[1:]))
        assert ab.min_gap(b, q) > 0.0
        assert ab.orthogonality_error(q) < 1e-2


def test_step_is_a_local_minimum_of_the_incremental_potential():
    """Brute force: no random point near the result has a lower energy."""
    rng = random.Random(5)
    b = ab.box(0.4, 0.2, 1000.0, 1e5, GROUND, 1e-3, 1.0)
    q = ab.rest_state((0.0, 0.1012), 0.0)
    qd = spin_rate(q, 3.0)
    qd[1] = -1.0
    qt = ab.predict(b, q, qd, 0.01)
    q1, _, _ = ab.abd_step(b, q, qd, 0.01, eps_d=1e-12)
    e1 = ab.energy(b, q1, qt, 0.01)
    for _ in range(300):
        z = [c + rng.uniform(-1e-4, 1e-4) for c in q1]
        assert ab.energy(b, z, qt, 0.01) >= e1 - 1e-12 * abs(e1)


def test_linear_momentum_follows_gravity_in_free_flight():
    b = ab.box(0.4, 0.2, 1000.0, 1e6, [], 1e-3, 1.0)
    q = ab.rest_state((0.0, 0.0), 0.4)
    qd = spin_rate(q, 6.0)
    qd[0], qd[1] = 1.0, 2.0
    total = sum(b.m)
    for _ in range(20):
        p0 = [sum(m * ab.world(qd, xb)[d] for xb, m in zip(b.xb, b.m)) for d in range(2)]
        q, qd, _ = ab.abd_step(b, q, qd, 0.01, eps_d=1e-10)
        p1 = [sum(m * ab.world(qd, xb)[d] for xb, m in zip(b.xb, b.m)) for d in range(2)]
        assert abs(p1[0] - p0[0]) < 1e-9 * total and abs(p1[1] - p0[1] + 0.01 * 9.81 * total) < 1e-9 * total


def test_resting_contact_forces_carry_the_weight():
    b = ab.box(0.4, 0.2, 1000.0, 1e7, GROUND, 1e-3, 1.0)
    q, qd = ab.rest_state((0.0, 0.1005), 0.0), [0.0] * 6
    dt = 0.01
    for _ in range(60):
        q, qd, _ = ab.abd_step(b, q, qd, dt, eps_d=1e-8)
    lam = [-b.kappa / (dt * dt) * ab.barrier(ab.gap(b, q, v, GROUND[0]), b.dhat)[1] for v in range(len(b.xb))]
    assert all(f >= 0.0 for f in lam)
    assert abs(sum(lam) - sum(b.m) * 9.81) < 1e-3 * sum(b.m) * 9.81


def test_stiffer_orthogonality_keeps_a_spinning_body_closer_to_rigid():
    """Measured: the largest orthogonality error falls about 100 times for each factor 100 in kappa_o."""
    errs = []
    for ko in (1e5, 1e7):
        b = ab.box(0.4, 0.2, 1000.0, ko, [], 1e-3, 1.0)
        q = ab.rest_state((0.0, 0.0), 0.0)
        qd = spin_rate(q, 10.0)
        worst = 0.0
        for _ in range(30):
            q, qd, _ = ab.abd_step(b, q, qd, 0.01, gravity=(0.0, 0.0))
            worst = max(worst, ab.orthogonality_error(q))
        errs.append(worst)
    assert 50.0 < errs[0] / errs[1] < 200.0


def test_free_fall_is_symplectic_euler():
    b = ab.box(0.4, 0.2, 1000.0, 1e5, [], 1e-3, 1.0)
    q, qd = ab.rest_state(), [0.0] * 6
    for _ in range(10):
        q, qd, _ = ab.abd_step(b, q, qd, 0.1)
    assert abs(q[1] + 5.3955) < 1e-12 and abs(q[0]) < 1e-14
