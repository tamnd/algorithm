# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/four-dimensional-ensemble-variational/. The authors are listed in prov/5MYERD.jsonl.

import math
import random

import scimat
from four_dimensional_ensemble_variational import four_d_envar, linear_model, lorenz63, run


def random_matrix(rng, m, n):
    return [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(m)]


def random_spd(rng, n, shift=0.5):
    A = random_matrix(rng, n, n)
    S = scimat.matmul(A, scimat.transpose(A))
    for i in range(n):
        S[i][i] += shift
    return S


def gaussian_localization(n, c):
    return [[math.exp(-((i - j) ** 2) / (2.0 * c * c)) for j in range(n)] for i in range(n)]


def close(a, b, tol):
    return all(abs(u - v) <= tol * (1 + abs(v)) for u, v in zip(a, b))


def exact_ensemble(xb, B):
    """Return N = n + 1 members whose scaled perturbations X' satisfy X' X'^T = B exactly."""
    n = len(xb)
    N = n + 1
    basis = [[1.0] * N] + [[1.0 if j == i else 0.0 for j in range(N)] for i in range(n)]
    rows = []
    for v in basis:
        w = list(v)
        for q in rows:
            c = scimat.dot(w, q)
            w = [a - c * b for a, b in zip(w, q)]
        rows.append(scimat.scale(1.0 / scimat.norm2(w), w))
    W = rows[1:]  # n orthonormal rows, each orthogonal to the ones vector
    UB = scimat.cholesky(B)
    cols = scimat.matmul(UB, W)
    return [[xb[j] + math.sqrt(N - 1) * cols[j][i] for j in range(n)] for i in range(N)]


def strong_4dvar_reference(xb, B, M, obs):
    """x^a_0 = x^b + B G^T (G B G^T + R)^-1 (y - G x^b), with G the stacked H_k M^k."""
    n = len(xb)
    G, y, blocks = [], [], []
    for k in sorted(obs):
        H, yk, R = obs[k]
        Mk = scimat.eye(n)
        for _ in range(k):
            Mk = scimat.matmul(M, Mk)
        G.extend(scimat.matmul(H, Mk))
        y.extend(yk)
        blocks.append(R)
    m = len(y)
    Rbig = scimat.zeros(m, m)
    off = 0
    for R in blocks:
        for i in range(len(R)):
            for j in range(len(R)):
                Rbig[off + i][off + j] = R[i][j]
        off += len(R)
    GB = scimat.matmul(G, B)
    S = scimat.add(scimat.matmul(GB, scimat.transpose(G)), Rbig)
    w = scimat.solve(S, scimat.sub(y, scimat.matvec(G, xb)))
    return scimat.add(xb, scimat.matvec(scimat.transpose(GB), w))


def localized_reference(xb, members, L, obs, step, K):
    """Brute force: condition on all observations at once with C_kl = L o (X'_k X'_l^T)."""
    n, N = len(xb), len(members)
    background = run(xb, step, K)
    trajs = [run(m, step, K) for m in members]
    times = sorted(set(obs) | {0, K})
    s = 1.0 / math.sqrt(N - 1)
    X = {}
    for k in times:
        mean = [sum(t[k][j] for t in trajs) / N for j in range(n)]
        X[k] = [[s * (t[k][j] - mean[j]) for t in trajs] for j in range(n)]

    def C(k, l):
        P = scimat.matmul(X[k], scimat.transpose(X[l]))
        return [[L[i][j] * P[i][j] for j in range(n)] for i in range(n)]

    otimes = sorted(obs)
    sizes = [len(obs[k][1]) for k in otimes]
    m = sum(sizes)
    S = scimat.zeros(m, m)
    d = []
    oi = 0
    for a, k in enumerate(otimes):
        Hk, yk, Rk = obs[k]
        d.extend(scimat.sub(yk, scimat.matvec(Hk, background[k])))
        oj = 0
        for b, l in enumerate(otimes):
            Hl = obs[l][0]
            blk = scimat.matmul(scimat.matmul(Hk, C(k, l)), scimat.transpose(Hl))
            for i in range(sizes[a]):
                for j in range(sizes[b]):
                    S[oi + i][oj + j] = blk[i][j] + (Rk[i][j] if a == b else 0.0)
            oj += sizes[b]
        oi += sizes[a]
    w = scimat.solve(S, d)
    out = {}
    for k in times:
        x = list(background[k])
        off = 0
        for l, size in zip(otimes, sizes):
            Hl = obs[l][0]
            g = scimat.matvec(scimat.transpose(Hl), w[off : off + size])
            x = scimat.add(x, scimat.matvec(C(k, l), g))
            off += size
        out[k] = x
    return out


def test_scalar_check_value():
    # x_1 = 2 x_0, B = 1 from the members -1/sqrt(2) and 1/sqrt(2), y_1 = 2 with R = 1: x^a_0 = 0.8.
    r = 1.0 / math.sqrt(2.0)
    obs = {1: ([[1.0]], [2.0], [[1.0]])}
    xa = four_d_envar([0.0], [[-r], [r]], [[1.0]], obs, linear_model([[2.0]]), 1)
    assert abs(xa[0][0] - 0.8) < 1e-12
    assert abs(xa[1][0] - 1.6) < 1e-12


def test_equals_strong_4dvar_for_exact_ensemble():
    # Linear model, no localization and X' X'^T = B: 4DEnVar is 4D-Var with the same B.
    rng = random.Random(11)
    n, K = 4, 3
    M = scimat.add(scimat.eye(n), scimat.scale(0.3, random_matrix(rng, n, n)))
    B = random_spd(rng, n)
    xb = [rng.gauss(0, 1) for _ in range(n)]
    obs = {}
    for k in (1, 3):
        H = random_matrix(rng, 2, n)
        obs[k] = (H, [rng.gauss(0, 1) for _ in range(2)], random_spd(rng, 2, 0.3))
    members = exact_ensemble(xb, B)
    ones = [[1.0] * n for _ in range(n)]
    xa = four_d_envar(xb, members, ones, obs, linear_model(M), K)
    ref0 = strong_4dvar_reference(xb, B, M, obs)
    assert close(xa[0], ref0, 1e-8)
    refK = ref0
    for _ in range(K):
        refK = scimat.matvec(M, refK)
    assert close(xa[K], refK, 1e-8)


def test_localized_against_stacked_conditioning():
    rng = random.Random(5)
    n, N, K = 5, 3, 2
    M = scimat.add(scimat.eye(n), scimat.scale(0.2, random_matrix(rng, n, n)))
    xb = [rng.gauss(0, 1) for _ in range(n)]
    members = [[x + rng.gauss(0, 1) for x in xb] for _ in range(N)]
    L = gaussian_localization(n, 1.0)
    obs = {}
    for k in (1, 2):
        H = random_matrix(rng, 2, n)
        obs[k] = (H, [rng.gauss(0, 1) for _ in range(2)], random_spd(rng, 2, 0.3))
    for step in (linear_model(M), lorenz_like(n)):
        xa = four_d_envar(xb, members, L, obs, step, K)
        ref = localized_reference(xb, members, L, obs, step, K)
        for k in ref:
            assert close(xa[k], ref[k], 1e-8)


def lorenz_like(n):
    """A small nonlinear map, to show that the formula holds for any member trajectories."""
    return lambda k, x: [x[j] + 0.1 * (x[(j + 1) % n] - x[j - 2]) * x[j - 1] - 0.05 * x[j] for j in range(n)]


def test_model_runs_forward_only():
    calls = [0]
    base = linear_model([[0.9, 0.1], [0.0, 1.1]])

    def step(k, x):
        calls[0] += 1
        return base(k, x)

    rng = random.Random(3)
    N, K = 4, 6
    xb = [0.0, 0.0]
    members = [[rng.gauss(0, 1), rng.gauss(0, 1)] for _ in range(N)]
    obs = {k: ([[1.0, 0.0]], [1.0], [[0.5]]) for k in (2, 4, 6)}
    four_d_envar(xb, members, [[1.0, 0.5], [0.5, 1.0]], obs, step, K)
    assert calls[0] == (N + 1) * K


def test_lorenz63_twin_reduces_error():
    step = lorenz63(0.01)
    K = 25
    obs_times = (10, 25)
    H = scimat.eye(3)
    R = scimat.scale(0.25, scimat.eye(3))
    ones = [[1.0] * 3 for _ in range(3)]
    err_b = err_a = 0.0
    seeds = range(20)
    for seed in seeds:
        rng = random.Random(100 + seed)
        spin = run([1.0, 1.0, 20.0], step, 200 + 37 * seed)[-1]
        truth = run(spin, step, K)
        xb = [v + rng.gauss(0, 1) for v in spin]
        members = [[v + rng.gauss(0, 1) for v in xb] for _ in range(10)]
        obs = {k: (H, [v + rng.gauss(0, 0.5) for v in truth[k]], R) for k in obs_times}
        xa = four_d_envar(xb, members, ones, obs, step, K)
        back = run(xb, step, K)
        err_b += scimat.norm2(scimat.sub(back[K], truth[K])) / len(seeds)
        err_a += scimat.norm2(scimat.sub(xa[K], truth[K])) / len(seeds)
    assert err_a < 0.6 * err_b
