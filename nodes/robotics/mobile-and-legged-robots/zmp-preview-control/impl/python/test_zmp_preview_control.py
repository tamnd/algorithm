# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zmp-preview-control/. The authors are listed in prov/CQQDWX.jsonl.

import random

import rbm
from zmp_preview_control import augment, cart_table, preview_control, preview_gains, walking_reference

ZC = 0.8


def test_cart_table_is_exact_for_constant_jerk():
    # The discrete model must agree with c(t) = c0 + v t + a t^2 / 2 + u t^3 / 6.
    T = 0.05
    A, B, _ = cart_table(T, ZC)
    rng = random.Random(3)
    x = [rng.uniform(-1, 1) for _ in range(3)]
    u = rng.uniform(-5, 5)
    y = list(x)
    for _ in range(20):
        y = [a + b * u for a, b in zip(rbm.matvec(A, y), B)]
    t = 20 * T
    want = [
        x[0] + x[1] * t + x[2] * t * t / 2 + u * t ** 3 / 6,
        x[1] + x[2] * t + u * t * t / 2,
        x[2] + u * t,
    ]
    for i in range(3):
        assert abs(y[i] - want[i]) < 1e-12


def test_riccati_residual_is_small():
    T = 0.01
    A, B, C = cart_table(T, ZC)
    at, bt = augment(A, B, C)
    k, f, p = preview_gains(T, ZC, 160)
    r = 1e-6
    q = rbm.zeros(4, 4)
    q[0][0] = 1.0
    pb = rbm.matvec(p, bt)
    s = r + rbm.dot(bt, pb)
    bpa = [rbm.dot(pb, [at[i][j] for i in range(4)]) for j in range(4)]
    apa = rbm.mul(rbm.transpose(at), rbm.mul(p, at))
    big = max(abs(v) for row in p for v in row)
    for i in range(4):
        for j in range(4):
            res = q[i][j] + apa[i][j] - bpa[i] * bpa[j] / s - p[i][j]
            assert abs(res) < 1e-8 * big
    # The first preview gain equals the error gain, and after 1.6 s the gains are small.
    assert abs(f[0] - k[0]) < 1e-9 * abs(k[0])
    assert abs(f[-1]) < 0.01 * max(abs(v) for v in f)


def batch_optimum(T, ref, horizon, r=1e-6):
    """Minimize sum_k X_k^T Q X_k + R du_k^2 + X_H^T P X_H by least squares."""
    A, B, C = cart_table(T, ZC)
    at, bt = augment(A, B, C)
    _, _, p = preview_gains(T, ZC, 1, r=r)
    q = rbm.zeros(4, 4)
    q[0][0] = 1.0
    # X_k = S_k du + c_k, built step by step.
    s_mat = [[0.0] * horizon for _ in range(4)]
    c = [0.0] * 4
    hess = [[0.0] * horizon for _ in range(horizon)]
    grad = [0.0] * horizon
    for i in range(horizon):
        hess[i][i] += r
    for kk in range(horizon):
        new_s = [[0.0] * horizon for _ in range(4)]
        for a in range(4):
            for col in range(horizon):
                new_s[a][col] = sum(at[a][b] * s_mat[b][col] for b in range(4))
            new_s[a][kk] += bt[a]
        dr = ref[kk + 1] - ref[kk]
        c = rbm.matvec(at, c)
        c[0] -= dr
        s_mat = new_s
        w = p if kk == horizon - 1 else q
        ws = rbm.mul(w, s_mat)
        wc = rbm.matvec(w, c)
        for i in range(horizon):
            for j in range(horizon):
                hess[i][j] += sum(s_mat[a][i] * ws[a][j] for a in range(4))
            grad[i] += sum(s_mat[a][i] * wc[a] for a in range(4))
    return rbm.solve(hess, [-g for g in grad])


def test_matches_batch_optimum_when_preview_covers_all_changes():
    # With every reference change inside the preview window, the preview law is
    # the infinite-horizon optimum, which equals a finite problem with terminal cost P.
    T, horizon = 0.05, 40
    ref = [0.0] * 10 + [0.1] * 10 + [-0.05] * 30
    _, _, us = preview_control(ref[:horizon], T, ZC, horizon)
    du = [us[0]] + [us[i] - us[i - 1] for i in range(1, horizon)]
    want = batch_optimum(T, ref, horizon)
    scale = max(abs(v) for v in want)
    for a, b in zip(du, want):
        assert abs(a - b) < 1e-6 * scale


def test_zmp_tracks_walking_reference():
    T = 0.01
    px, py = walking_reference(T, 0.8, 6, 0.3, 0.1)
    for ref, final in ((px, 1.5), (py, 0.0)):
        xs, ps, _ = preview_control(ref, T, ZC, 160)
        # Away from the switch instants the ZMP is close to the reference.
        switches = [i for i in range(1, len(ref)) if ref[i] != ref[i - 1]]
        for i in range(len(ref)):
            if all(abs(i - s) > 15 for s in switches):
                assert abs(ps[i] - ref[i]) < 0.01
        # At the end the CoM rests over the last ZMP.
        assert abs(xs[-1][0] - final) < 1e-3
        assert abs(xs[-1][1]) < 1e-3


def test_com_moves_before_the_zmp_step():
    T = 0.01
    ref = [0.0] * 200 + [0.1] * 300
    xs, ps, _ = preview_control(ref, T, ZC, 160)
    # The CoM has started to move 0.1 s before the step, and the ZMP has not.
    assert xs[190][0] > 0.02
    assert abs(ps[190]) < 1e-3
    # The ZMP first moves a little the wrong way (the model is non-minimum phase).
    assert min(ps[:200]) < 0.0
