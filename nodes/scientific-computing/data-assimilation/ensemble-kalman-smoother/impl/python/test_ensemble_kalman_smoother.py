# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ensemble-kalman-smoother/. The authors are listed in prov/G9PNFT.jsonl.

import math
import random

import scimat
from ensemble_kalman_smoother import apply_weights, enks, ensemble_moments, transform_weights


def exact_ensemble(m0, P0, N, rng):
    """N members whose sample mean is m0 and sample covariance is P0 exactly."""
    n = len(m0)
    rows = []
    for _ in range(n):
        v = [rng.gauss(0, 1) for _ in range(N)]
        for u in [[1.0 / math.sqrt(N)] * N] + rows:
            c = scimat.dot(u, v)
            v = [a - c * b for a, b in zip(v, u)]
        nv = scimat.norm2(v)
        rows.append([a / nv for a in v])
    L = scimat.cholesky(P0)
    Z = [[math.sqrt(N - 1) * a for a in row] for row in rows]
    return [[m0[j] + sum(L[j][k] * Z[k][i] for k in range(n)) for j in range(n)] for i in range(N)]


def batch_posterior(m0, P0, A, H, R, obs, s, last):
    """Exact mean and covariance of x_s given y_1..y_last, for x_t = A^t x_0."""
    n = len(m0)
    powers = [scimat.eye(n)]
    for _ in range(max(s, last)):
        powers.append(scimat.matmul(A, powers[-1]))
    G, y, blocks = [], [], []
    for t in range(1, last + 1):
        if obs[t - 1] is None:
            continue
        G.extend(scimat.matmul(H, powers[t]))
        y.extend(obs[t - 1])
        blocks.append(R)
    m, P = list(m0), [list(r) for r in P0]
    if G:
        q = len(y)
        Rb = [[0.0] * q for _ in range(q)]
        off = 0
        for B in blocks:
            for a in range(len(B)):
                for b in range(len(B)):
                    Rb[off + a][off + b] = B[a][b]
            off += len(B)
        PGt = scimat.matmul(P0, scimat.transpose(G))
        S = scimat.add(scimat.matmul(G, PGt), Rb)
        K = scimat.transpose(scimat.solve(S, scimat.transpose(PGt)))
        m = scimat.add(m0, scimat.matvec(K, scimat.sub(y, scimat.matvec(G, m0))))
        P = scimat.sub(P0, scimat.matmul(K, scimat.transpose(PGt)))
    As = powers[s]
    return scimat.matvec(As, m), scimat.matmul(scimat.matmul(As, P), scimat.transpose(As))


def check(ens, m, P, tol=1e-8):
    em, eP = ensemble_moments(ens)
    for a in range(len(m)):
        assert abs(em[a] - m[a]) < tol * (1 + abs(m[a]))
        for b in range(len(m)):
            assert abs(eP[a][b] - P[a][b]) < tol * (1 + abs(P[a][b]))


def test_scalar_check_value():
    s = 1 / math.sqrt(2.0)
    filt, smooth = enks([[-s], [s]], lambda x: x, lambda x: x, [[1.0]], [[1.0]], lag=1)
    for ens in (smooth[0], filt[1], smooth[1]):
        m, P = ensemble_moments(ens)
        assert abs(m[0] - 0.5) < 1e-12 and abs(P[0][0] - 0.5) < 1e-12
    m, P = ensemble_moments(filt[0])
    assert abs(m[0]) < 1e-12 and abs(P[0][0] - 1.0) < 1e-12


def test_page_example():
    filt, smooth = enks([[-1.0], [1.0]], lambda x: [2 * x[0]], lambda x: x, [[8.0]], [[4.0]], lag=1)
    r = 1 / math.sqrt(2.0)
    assert abs(smooth[1][0][0] - (2 - 2 * r)) < 1e-12 and abs(smooth[1][1][0] - (2 + 2 * r)) < 1e-12
    assert abs(smooth[0][0][0] - (1 - r)) < 1e-12 and abs(smooth[0][1][0] - (1 + r)) < 1e-12
    m, P = ensemble_moments(smooth[0])
    assert abs(m[0] - 1.0) < 1e-12 and abs(P[0][0] - 1.0) < 1e-12


def linear_setup(seed, n=3, p=2, T=6, N=6):
    rng = random.Random(seed)
    A = [[rng.uniform(-0.8, 0.8) + (1.0 if i == j else 0.0) for j in range(n)] for i in range(n)]
    H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
    L = [[rng.uniform(-1, 1) for _ in range(p)] for _ in range(p)]
    R = scimat.add(scimat.matmul(L, scimat.transpose(L)), scimat.scale(0.5, scimat.eye(p)))
    m0 = [rng.gauss(0, 1) for _ in range(n)]
    B = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    P0 = scimat.add(scimat.matmul(B, scimat.transpose(B)), scimat.scale(0.2, scimat.eye(n)))
    obs = [None if t == 2 else [rng.gauss(0, 2) for _ in range(p)] for t in range(T)]
    ens0 = exact_ensemble(m0, P0, N, rng)
    return A, H, R, m0, P0, obs, ens0


def test_fixed_interval_matches_exact_smoother():
    for seed in range(3):
        A, H, R, m0, P0, obs, ens0 = linear_setup(seed)
        T = len(obs)
        filt, smooth = enks(ens0, lambda x: scimat.matvec(A, x), lambda x: scimat.matvec(H, x), R, obs, lag=T)
        for s in range(T + 1):
            m, P = batch_posterior(m0, P0, A, H, R, obs, s, T)
            check(smooth[s], m, P)
            m, P = batch_posterior(m0, P0, A, H, R, obs, s, s)
            check(filt[s], m, P)


def test_fixed_lag_uses_data_up_to_t_plus_lag():
    A, H, R, m0, P0, obs, ens0 = linear_setup(7)
    T = len(obs)
    for lag in (1, 2):
        _, smooth = enks(ens0, lambda x: scimat.matvec(A, x), lambda x: scimat.matvec(H, x), R, obs, lag=lag)
        for s in range(T + 1):
            m, P = batch_posterior(m0, P0, A, H, R, obs, s, min(s + lag, T))
            check(smooth[s], m, P)


def test_lag_zero_is_the_filter_and_last_time_agrees():
    A, H, R, m0, P0, obs, ens0 = linear_setup(8)
    model, h = (lambda x: scimat.matvec(A, x)), (lambda x: scimat.matvec(H, x))
    filt, smooth = enks(ens0, model, h, R, obs, lag=0)
    assert all(a == b for a, b in zip(filt, smooth))
    filt2, smooth2 = enks(ens0, model, h, R, obs, lag=3)
    assert smooth2[-1] == filt2[-1] == filt[-1]


def test_smoothed_members_keep_the_linear_model_relation():
    A, H, R, m0, P0, obs, ens0 = linear_setup(9)
    T = len(obs)
    _, smooth = enks(ens0, lambda x: scimat.matvec(A, x), lambda x: scimat.matvec(H, x), R, obs, lag=T)
    for t in range(T):
        for a, b in zip(smooth[t], smooth[t + 1]):
            ax = scimat.matvec(A, a)
            assert all(abs(u - v) < 1e-9 for u, v in zip(ax, b))


def test_weights_are_shared_and_keep_the_mean_of_a_constant():
    rng = random.Random(10)
    ens = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(5)]
    wbar, W = transform_weights(ens, [0.5], lambda x: [x[0]], [[0.4]])
    assert abs(sum(wbar)) < 1e-12
    for i in range(5):
        assert abs(sum(W[m][i] for m in range(5)) - 1.0) < 1e-12
    const = [[3.0, -1.0] for _ in range(5)]
    assert all(abs(u - v) < 1e-12 for x in apply_weights(const, wbar, W) for u, v in zip(x, [3.0, -1.0]))
