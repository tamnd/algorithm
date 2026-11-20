# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/representer-method/. The authors are listed in prov/6YYQY7.jsonl.

import random
from fractions import Fraction

import scimat
from representer_method import linear_model, representer_method


def random_spd(rng, n, shift=0.5):
    L = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    S = scimat.matmul(L, scimat.transpose(L))
    for i in range(n):
        S[i][i] += shift
    return S


def frac(rng, lo=-3, hi=3, den=4):
    return Fraction(rng.randint(lo * den, hi * den), den)


def frac_spd(rng, n):
    L = [[frac(rng, -1, 1) for _ in range(n)] for _ in range(n)]
    S = scimat.matmul(L, scimat.transpose(L))
    for i in range(n):
        S[i][i] += Fraction(1, 2)
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


def gaussian_conditioning(xb, B, M, Q, obs, K):
    """Brute force: condition the stacked trajectory on all observations at once.

    Return (E[x | y] as a list of states, prior covariance of the stacked observations).
    """
    n = len(xb)
    N = n * (K + 1)
    # T maps z = (x_0, eta_1, ..., eta_K) to the stacked trajectory.
    T = scimat.zeros(N)
    powers = [scimat.eye(n)]
    for _ in range(K):
        powers.append(scimat.matmul(M, powers[-1]))
    for k in range(K + 1):
        for j in range(k + 1):
            blk = powers[k - j]
            for a in range(n):
                for b in range(n):
                    T[k * n + a][j * n + b] = blk[a][b]
    C = scimat.zeros(N)
    for j in range(K + 1):
        cov = B if j == 0 else Q[j]
        for a in range(n):
            for b in range(n):
                C[j * n + a][j * n + b] = cov[a][b]
    mean_z = list(xb) + [0] * (n * K)
    mean = scimat.matvec(T, mean_z)
    cov = scimat.matmul(scimat.matmul(T, C), scimat.transpose(T))
    rows, y, blocks = [], [], []
    for k in sorted(obs):
        H, yk, R = obs[k]
        for row, v in zip(H, yk):
            full = [0] * N
            for a in range(n):
                full[k * n + a] = row[a]
            rows.append(full)
            y.append(v)
        blocks.append(R)
    p = len(rows)
    Rall = scimat.zeros(p)
    i = 0
    for R in blocks:
        for a in range(len(R)):
            for b in range(len(R)):
                Rall[i + a][i + b] = R[a][b]
        i += len(R)
    Hs = rows
    HC = scimat.matmul(Hs, cov)
    S = scimat.matmul(HC, scimat.transpose(Hs))
    gain_t = scimat.solve(scimat.add(S, Rall), HC)
    post = scimat.add(mean, scimat.matvec(scimat.transpose(gain_t), scimat.sub(y, scimat.matvec(Hs, mean))))
    return [post[k * n : (k + 1) * n] for k in range(K + 1)], S


def close(a, b, tol):
    return all(abs(u - v) <= tol * (1 + abs(v)) for u, v in zip(a, b))


def test_scalar_check_value():
    step, adj = linear_model([[1]])
    est, beta, P = representer_method([0], [[1]], [None], {0: ([[1]], [1], [[1]])}, step, adj, 0)
    assert est[0][0] == Fraction(1, 2) and P == [[1]]


def test_page_example():
    # x_1 = x_0 + eta_1, x^b = 0, B = Q = R = 1, y_1 = 3: r = (1, 2), P = 2, beta = 1, estimate (1, 2).
    step, adj = linear_model([[1]])
    est, beta, P = representer_method([0], [[1]], [None, [[1]]], {1: ([[1]], [3], [[1]])}, step, adj, 1)
    assert P == [[2]] and beta == [1] and est == [[1], [2]]


def test_exact_against_gaussian_conditioning():
    rng = random.Random(71)
    for _ in range(12):
        n = rng.randint(1, 3)
        K = rng.randint(0, 3)
        M = [[frac(rng, -1, 1) + (1 if i == j else 0) for j in range(n)] for i in range(n)]
        B = frac_spd(rng, n)
        Q = [None] + [frac_spd(rng, n) for _ in range(K)]
        xb = [frac(rng) for _ in range(n)]
        obs = {}
        for k in range(K + 1):
            if rng.random() < 0.7 or k == K:
                p = rng.randint(1, 2)
                obs[k] = ([[frac(rng, -1, 1) for _ in range(n)] for _ in range(p)], [frac(rng) for _ in range(p)], frac_spd(rng, p))
        step, adj = linear_model(M)
        est, beta, P = representer_method(xb, B, Q, obs, step, adj, K)
        ref, S = gaussian_conditioning(xb, B, M, Q, obs, K)
        assert est == ref
        assert P == S  # the representer matrix is the prior covariance of the observations


def test_equals_kalman_smoother_with_q():
    rng = random.Random(72)
    for _ in range(30):
        n = rng.randint(1, 3)
        K = rng.randint(1, 6)
        M = [[(1.0 if i == j else 0.0) + 0.3 * rng.uniform(-1, 1) for j in range(n)] for i in range(n)]
        B = random_spd(rng, n)
        Q = [None] + [random_spd(rng, n, 0.2) for _ in range(K)]
        xb = [rng.uniform(-2, 2) for _ in range(n)]
        obs = {}
        for k in range(K + 1):
            if rng.random() < 0.6 or k == K:
                p = rng.randint(1, 3)
                obs[k] = ([[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)], [rng.uniform(-2, 2) for _ in range(p)], random_spd(rng, p))
        step, adj = linear_model(M)
        est, _, _ = representer_method(xb, B, Q, obs, step, adj, K)
        xa, xs = kalman_and_rts(xb, B, M, Q, obs, K)
        for k in range(K + 1):
            assert close(est[k], xs[k], 1e-9)


def test_one_adjoint_and_one_forward_run_per_observation():
    rng = random.Random(73)
    n, K = 2, 5
    M = [[1.0, 0.1], [-0.1, 1.0]]
    step0, adj0 = linear_model(M)
    calls = {"step": 0, "adjoint": 0}

    def step(k, x):
        calls["step"] += 1
        return step0(k, x)

    def adj(k, lam):
        calls["adjoint"] += 1
        return adj0(k, lam)

    obs = {1: ([[1.0, 0.0]], [0.5], [[0.1]]), 3: ([[0.0, 1.0], [1.0, 1.0]], [0.2, -0.4], [[0.1, 0.0], [0.0, 0.2]]), 5: ([[1.0, -1.0]], [1.0], [[0.3]])}
    p = 4
    Q = [None] + [[[0.05, 0.0], [0.0, 0.05]] for _ in range(K)]
    representer_method([rng.uniform(-1, 1) for _ in range(n)], [[1.0, 0.0], [0.0, 1.0]], Q, obs, step, adj, K)
    assert calls["adjoint"] == (p + 1) * K
    assert calls["step"] == (p + 2) * K
