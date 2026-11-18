# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-potential-contact/. The authors are listed in prov/TZGCEP.jsonl.

"""Tests of incremental potential contact: derivatives, the collision check, monotone Newton and no crossing."""

import math
import random

from anim import num_grad
import incremental_potential_contact as ipc

GROUND = [((-5.0, 0.0), (5.0, 0.0))]


def flat(x, free):
    return [c for i in free for c in x[i]]


def unflat(z, x, free):
    y = list(x)
    for k, i in enumerate(free):
        y[i] = (z[2 * k], z[2 * k + 1])
    return y


def is_psd(h):
    """Cholesky of h + 1e-9 (1 + max |h_ii|) I succeeds."""
    n = len(h)
    shift = 1e-9 * (1.0 + max(abs(h[i][i]) for i in range(n)))
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = h[i][j] + (shift if i == j else 0.0) - sum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                if s <= 0.0:
                    return False
                low[i][i] = math.sqrt(s)
            else:
                low[i][j] = s / low[j][j]
    return True


def test_barrier_derivatives_and_smoothness():
    dhat = 0.01
    for d in (1e-4, 1e-3, 4e-3, 9e-3):
        b, b1, b2 = ipc.barrier(d, dhat)
        assert b > 0.0 and b1 < 0.0 and b2 > 0.0
        assert abs(num_grad(lambda z: ipc.barrier(z[0], dhat)[0], [d], 1e-8)[0] - b1) < 1e-5 * abs(b1)
        assert abs(num_grad(lambda z: ipc.barrier(z[0], dhat)[1], [d], 1e-8)[0] - b2) < 1e-5 * abs(b2)
    near = ipc.barrier(dhat * (1.0 - 1e-6), dhat)
    assert all(abs(c) < 1e-5 for c in near)
    assert ipc.barrier(dhat, dhat) == (0.0, 0.0, 0.0)
    assert ipc.barrier(1e-12, dhat)[0] > 1e-3


def test_gradient_and_hessian_against_num_grad():
    rng = random.Random(7)
    segs = GROUND + [((0.3, -1.0), (0.3, 1.0))]
    sc = ipc.box((0.15, 0.1), 0.2, 300.0, 0.25, segs, 0.06, 2.0)
    x = [(p[0] + rng.uniform(-0.02, 0.02), p[1] + rng.uniform(-0.02, 0.02)) for p in sc.rest]
    x[0] = (0.07, 0.03)
    x[1] = (0.27, 0.01)
    xhat = [(p[0] + 0.01, p[1] - 0.02) for p in x]
    dt = 0.02
    assert ipc.min_distance(sc, x) < sc.dhat
    g, h = ipc.gradient_and_hessian(sc, x, xhat, dt, project=False)
    z0 = flat(x, sc.free)
    ng = num_grad(lambda z: ipc.potential(sc, unflat(z, x, sc.free), xhat, dt), z0, 1e-7)
    scale = max(abs(c) for c in g)
    assert max(abs(a - b) for a, b in zip(g, ng)) < 1e-5 * scale
    for r in range(len(z0)):
        col = num_grad(lambda z: ipc.gradient_and_hessian(sc, unflat(z, x, sc.free), xhat, dt, False)[0][r], z0, 1e-7)
        for c in range(len(z0)):
            assert abs(col[c] - h[r][c]) < 1e-4 * max(1.0, abs(h[r][c]))


def test_projected_hessian_is_psd_and_unprojected_can_be_indefinite():
    """The point near a segment end has an indefinite barrier Hessian; the projection removes the negative part."""
    sc = ipc.Scene([(0.0, 0.0), (0.0, 0.0)], [(0, 1, 1.0, 50.0)], [1.0, 1.0], [((-1.0, 0.0), (0.0, 0.0))], 0.1, 10.0)
    x = [(0.01, 0.02), (0.01, 0.52)]
    _, h0 = ipc.gradient_and_hessian(sc, x, x, 0.1, project=False)
    _, h1 = ipc.gradient_and_hessian(sc, x, x, 0.1, project=True)
    big = [[1e3 * c for c in row] for row in h0]
    for i in range(4):
        big[i][i] -= 1e3 * 1.0
    assert not is_psd(big)
    sub = [[h1[i][j] - (1.0 if i == j else 0.0) for j in range(4)] for i in range(4)]
    assert is_psd(sub)


def test_time_of_impact_against_sampling():
    rng = random.Random(11)
    hits = 0
    n = 1000
    for _ in range(300):
        a = (rng.uniform(-1, 1), rng.uniform(-1, 1))
        b = (rng.uniform(-1, 1), rng.uniform(-1, 1))
        p = (rng.uniform(-1, 1), rng.uniform(-1, 1))
        dp = (rng.uniform(-2, 2), rng.uniform(-2, 2))
        t = ipc.segment_toi(p, dp, a, b)
        ex, ey = b[0] - a[0], b[1] - a[1]
        pts = [(p[0] + s / n * dp[0], p[1] + s / n * dp[1]) for s in range(n + 1)]
        side = [ex * (q[1] - a[1]) - ey * (q[0] - a[0]) for q in pts]
        par = [((q[0] - a[0]) * ex + (q[1] - a[1]) * ey) / (ex * ex + ey * ey) for q in pts]
        crossings = [k for k in range(n) if side[k] * side[k + 1] < 0.0 and 0.0 < par[k] < 1.0 and 0.0 < par[k + 1] < 1.0]
        if t is None:
            assert not crossings
        else:
            hits += 1
            q = (p[0] + t * dp[0], p[1] + t * dp[1])
            assert ipc.point_segment(q, a, b)[0] < 1e-9
            assert all(abs(k / n - t) <= 1.0 / n for k in crossings)
            assert all(side[j] * side[0] > 0.0 for j in range(int(t * n)))
    assert 30 < hits < 270
    assert ipc.segment_toi((-2.0, 0.0), (3.0, 0.0), (-1.0, 0.0), (1.0, 0.0)) == 1.0 / 3.0


def test_one_spring_without_contact_is_backward_euler():
    m, k, r, dt, y = 1.0, 100.0, 1.0, 0.1, 1.5
    sc = ipc.Scene([(0.0, 0.0), (1.5, 0.0)], [(0, 1, r, k)], [m, m], GROUND[:0], 0.01, 1.0, pinned=[0])
    x1, _, it = ipc.ipc_step(sc, [(0.0, 0.0), (1.5, 0.0)], [(0.0, 0.0)] * 2, dt, gravity=(0.0, 0.0), eps_d=1e-12)
    assert abs(x1[1][0] - (m * y + dt * dt * k * r) / (m + dt * dt * k)) < 1e-14 and abs(x1[1][1]) < 1e-15
    assert it == 1


def test_potential_never_increases_and_distance_stays_positive():
    sc = ipc.box((0.0, 0.6), 0.2, 1e4, 0.25, GROUND, 1e-3, 1.0)
    x, v = list(sc.rest), [(0.0, -20.0)] * 4
    dt = 1.0 / 30.0
    for _ in range(30):
        hist = []
        x, v, _ = ipc.ipc_step(sc, x, v, dt, history=hist)
        assert all(b <= a for a, b in zip(hist, hist[1:]))
        assert ipc.min_distance(sc, x) > 0.0 and all(p[1] > 0.0 for p in x)


def test_fast_point_does_not_tunnel_through_a_thin_wall():
    sc = ipc.Scene([(0.0, 0.5)], [], [1.0], [((-1.0, 0.0), (1.0, 0.0))], 1e-3, 1.0)
    x, v = [(0.0, 0.5)], [(0.0, -1000.0)]
    for _ in range(5):
        x, v, _ = ipc.ipc_step(sc, x, v, 1.0 / 30.0)
        assert 0.0 < x[0][1] < 1e-3


def test_resting_contact_forces_carry_the_weight():
    sc = ipc.box((0.0, 0.1005), 0.2, 1e4, 0.25, GROUND, 1e-3, 1.0)
    x, v = list(sc.rest), [(0.0, 0.0)] * 4
    dt = 1.0 / 100.0
    for _ in range(60):
        x, v, _ = ipc.ipc_step(sc, x, v, dt, eps_d=1e-8)
    lam = ipc.contact_forces(sc, x, dt)
    assert len(lam) == 2 and all(f >= 0.0 for _, f in lam)
    assert abs(sum(f for _, f in lam) - 4 * 0.25 * 9.81) < 1e-4
    assert max(abs(c) for u in v for c in u) < 1e-4


def test_free_fall_is_symplectic_euler():
    sc = ipc.Scene([(0.0, 0.0)], [], [1.0], [], 1e-3, 1.0)
    x, v = [(0.0, 0.0)], [(0.0, 0.0)]
    for _ in range(10):
        x, v, _ = ipc.ipc_step(sc, x, v, 0.1)
    assert abs(x[0][1] + 5.3955) < 1e-12
