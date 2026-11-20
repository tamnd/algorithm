# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-constraint-4d-var/. The authors are listed in prov/2GGXNP.jsonl.

import random

import scimat
from weak_constraint_4d_var import (
    cost,
    gradient,
    linear_model,
    lorenz63,
    trajectory,
    weak_4dvar,
)


def random_spd(rng, n, shift=0.5):
    L = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    S = scimat.matmul(L, scimat.transpose(L))
    for i in range(n):
        S[i][i] += shift
    return S


def kalman_and_rts(xb, B, M, Q, obs, K):
    """Oracle: Kalman filter and Rauch-Tung-Striebel smoother means with model error Q[k]."""
    Mt = scimat.transpose(M)
    xf, Pf, xa, Pa = [], [], [], []
    x, P = list(xb), B
    for k in range(K + 1):
        if k > 0:
            x = scimat.matvec(M, xa[-1])
            P = scimat.add(scimat.matmul(scimat.matmul(M, Pa[-1]), Mt), Q[k])
        xf.append(x)
        Pf.append(P)
        if k in obs:
            H, y, R = obs[k]
            S = scimat.add(scimat.matmul(scimat.matmul(H, P), scimat.transpose(H)), R)
            G = scimat.transpose(scimat.solve(S, scimat.matmul(H, P)))
            x = scimat.add(x, scimat.matvec(G, scimat.sub(y, scimat.matvec(H, x))))
            P = scimat.sub(P, scimat.matmul(G, scimat.matmul(H, P)))
        xa.append(x)
        Pa.append(P)
    xs = [None] * (K + 1)
    xs[K] = xa[K]
    for k in range(K - 1, -1, -1):
        C = scimat.transpose(scimat.solve(Pf[k + 1], scimat.matmul(M, Pa[k])))
        xs[k] = scimat.add(xa[k], scimat.matvec(C, scimat.sub(xs[k + 1], xf[k + 1])))
    return xa, xs


def close(a, b, tol):
    return all(abs(u - v) <= tol * (1 + abs(v)) for u, v in zip(a, b))


def random_problem(rng, n, K, qscale=1.0):
    M = [[(1.0 if i == j else 0.0) + 0.3 * rng.uniform(-1, 1) for j in range(n)] for i in range(n)]
    B = random_spd(rng, n)
    Q = [None] + [scimat.scale(qscale, random_spd(rng, n, 0.2)) for _ in range(K)]
    xb = [rng.uniform(-2, 2) for _ in range(n)]
    obs = {}
    for k in range(K + 1):
        if rng.random() < 0.6:
            p = rng.randint(1, 3)
            H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
            obs[k] = (H, [rng.uniform(-2, 2) for _ in range(p)], random_spd(rng, p))
    if not obs:
        obs[K] = ([[1.0] + [0.0] * (n - 1)], [1.0], [[1.0]])
    return M, B, Q, xb, obs


def test_scalar_check_value():
    step, tl, adj = linear_model([[1.0]])
    xs, x0, eta, _ = weak_4dvar([0.0], [[1.0]], [None], {0: ([[1.0]], [1.0], [[1.0]])}, step, tl, adj, 0)
    assert abs(x0[0] - 0.5) < 1e-14


def test_page_example():
    # x_1 = x_0 + eta_1, x^b = 0, B = Q = R = 1, y_1 = 3: x_0 = eta_1 = 1 and x_1 = 2.
    step, tl, adj = linear_model([[1.0]])
    xs, x0, eta, _ = weak_4dvar([0.0], [[1.0]], [None, [[1.0]]], {1: ([[1.0]], [3.0], [[1.0]])}, step, tl, adj, 1)
    assert abs(x0[0] - 1.0) < 1e-13 and abs(eta[1][0] - 1.0) < 1e-13 and abs(xs[1][0] - 2.0) < 1e-13


def test_linear_model_equals_kalman_smoother_with_q():
    rng = random.Random(61)
    for _ in range(40):
        n = rng.randint(1, 3)
        K = rng.randint(1, 5)
        M, B, Q, xb, obs = random_problem(rng, n, K)
        step, tl, adj = linear_model(M)
        xs, x0, eta, outer = weak_4dvar(xb, B, Q, obs, step, tl, adj, K)
        xa, xsm = kalman_and_rts(xb, B, M, Q, obs, K)
        for k in range(K + 1):
            assert close(xs[k], xsm[k], 1e-8)
        assert close(xs[K], xa[K], 1e-8)
        assert outer <= 3


def test_small_q_approaches_strong_constraint():
    rng = random.Random(62)
    n, K = 2, 4
    M, B, Q, xb, obs = random_problem(rng, n, K, qscale=1e-9)
    step, tl, adj = linear_model(M)
    xs, x0, eta, _ = weak_4dvar(xb, B, Q, obs, step, tl, adj, K)
    zero = [None] + [[[0.0] * n for _ in range(n)] for _ in range(K)]
    _, strong = kalman_and_rts(xb, B, M, zero, obs, K)
    for k in range(K + 1):
        assert close(xs[k], strong[k], 1e-6)


def test_gradient_matches_finite_differences_lorenz63():
    rng = random.Random(63)
    step, _, adj = lorenz63()
    K = 15
    B = [[1.0, 0.2, 0.0], [0.2, 2.0, 0.1], [0.0, 0.1, 1.5]]
    Q = [None] + [[[0.1, 0.0, 0.0], [0.0, 0.2, 0.0], [0.0, 0.0, 0.1]] for _ in range(K)]
    xb = [1.0, 2.0, 20.0]
    H = [[1.0, 0.0, 0.0], [0.0, 0.5, 0.5]]
    obs = {k: (H, [rng.uniform(-5, 5), rng.uniform(-5, 5)], [[0.5, 0.0], [0.0, 1.0]]) for k in (0, 5, 10, 15)}
    x0 = [v + rng.uniform(-1, 1) for v in xb]
    eta = [None] + [[rng.uniform(-0.3, 0.3) for _ in range(3)] for _ in range(K)]
    g0, geta = gradient(x0, eta, xb, B, Q, obs, step, adj, K)
    eps = 1e-6
    for j in range(3):
        xp, xm = list(x0), list(x0)
        xp[j] += eps
        xm[j] -= eps
        fd = (cost(xp, eta, xb, B, Q, obs, step, K) - cost(xm, eta, xb, B, Q, obs, step, K)) / (2 * eps)
        assert abs(fd - g0[j]) <= 1e-6 * (1 + abs(fd))
    for k in (1, 7, 15):
        for j in range(3):
            ep = [None] + [list(e) for e in eta[1:]]
            em = [None] + [list(e) for e in eta[1:]]
            ep[k][j] += eps
            em[k][j] -= eps
            fd = (cost(x0, ep, xb, B, Q, obs, step, K) - cost(x0, em, xb, B, Q, obs, step, K)) / (2 * eps)
            assert abs(fd - geta[k][j]) <= 1e-6 * (1 + abs(fd))


def test_nonlinear_limit_is_stationary_and_weak_beats_strong_with_model_error():
    # Twin: the truth has a constant forcing that the model lacks (model error).
    step, tl, adj = lorenz63()
    K = 40
    forcing = [0.0, 0.0, 0.05]
    truth0 = trajectory([1.0, 1.0, 1.0], [None] + [[0.0] * 3] * 500, step, 500)[-1]
    truth = trajectory(truth0, [None] + [forcing] * K, step, K)
    H = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    R = [[0.04, 0.0, 0.0], [0.0, 0.04, 0.0], [0.0, 0.0, 0.04]]
    B = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    err_weak = err_strong = 0.0
    for seed in range(64, 70):
        rng = random.Random(seed)
        obs = {k: (H, [v + rng.gauss(0, 0.2) for v in truth[k]], R) for k in range(0, K + 1, 4)}
        xb = [v + rng.gauss(0, 1.0) for v in truth0]
        Qw = [None] + [[[0.01, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.01]] for _ in range(K)]
        Qs = [None] + [[[1e-8, 0.0, 0.0], [0.0, 1e-8, 0.0], [0.0, 0.0, 1e-8]] for _ in range(K)]
        xw, x0, eta, _ = weak_4dvar(xb, B, Qw, obs, step, tl, adj, K)
        g0, geta = gradient(x0, eta, xb, B, Qw, obs, step, adj, K)
        assert scimat.norm2(g0) + sum(scimat.norm2(g) for g in geta[1:]) < 1e-7
        xstr, _, _, _ = weak_4dvar(xb, B, Qs, obs, step, tl, adj, K)
        err_weak += scimat.norm2(scimat.sub(xw[K], truth[K]))
        err_strong += scimat.norm2(scimat.sub(xstr[K], truth[K]))
    assert err_weak < 0.5 * err_strong
