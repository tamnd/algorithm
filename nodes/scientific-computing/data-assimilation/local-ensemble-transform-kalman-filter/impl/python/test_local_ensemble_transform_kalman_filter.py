# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-ensemble-transform-kalman-filter/. The authors are listed in prov/HEPB83.jsonl.

import math
import random
from fractions import Fraction as Fr

import scimat
from local_ensemble_transform_kalman_filter import (
    gaspari_cohn,
    letkf_analysis,
    mean_and_spread,
    periodic_distance,
    sym_eig,
)


def lorenz96(x, forcing=8.0):
    n = len(x)
    return [(x[(k + 1) % n] - x[k - 2]) * x[k - 1] - x[k] + forcing for k in range(n)]


def rk4(x, dt):
    k1 = lorenz96(x)
    k2 = lorenz96([a + 0.5 * dt * b for a, b in zip(x, k1)])
    k3 = lorenz96([a + 0.5 * dt * b for a, b in zip(x, k2)])
    k4 = lorenz96([a + dt * b for a, b in zip(x, k3)])
    return [a + dt / 6.0 * (b + 2.0 * c + 2.0 * d + e) for a, b, c, d, e in zip(x, k1, k2, k3, k4)]


def dense_point_update(ens, yo, h, r_var, j, weights, rho):
    """Oracle for one grid point: form the N by N ETKF matrices of Hunt et al. (2007)."""
    N = len(ens)
    hx = [h(x) for x in ens]
    ybar = [sum(v[k] for v in hx) / N for k in range(len(yo))]
    xbar = sum(x[j] for x in ens) / N
    Xj = [x[j] - xbar for x in ens]
    S = [[math.sqrt(w / r_var[k]) * (hx[i][k] - ybar[k]) for i in range(N)] for k, w in weights]
    d = [math.sqrt(w / r_var[k]) * (yo[k] - ybar[k]) for k, w in weights]
    A = scimat.add(scimat.scale((N - 1) / rho, scimat.eye(N)), scimat.matmul(scimat.transpose(S), S))
    Pt = scimat.inv(A)
    wbar = scimat.matvec(Pt, scimat.matvec(scimat.transpose(S), d)) if S else [0.0] * N
    vals, V = sym_eig(scimat.scale(N - 1, Pt))
    W = [[sum(V[a][m] * math.sqrt(vals[m]) * V[b][m] for m in range(N)) for b in range(N)] for a in range(N)]
    return [xbar + sum(Xj[k] * (wbar[k] + W[k][i]) for k in range(N)) for i in range(N)]


def random_ensemble(rng, N, n):
    return [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]


def test_scalar_check_value():
    s = 1 / math.sqrt(2.0)
    out = letkf_analysis([[-s], [s]], [1.0], lambda x: [x[0]], [1.0])
    mean, var = mean_and_spread(out)
    assert abs(mean[0] - 0.5) < 1e-12
    assert abs(var[0] - 0.5) < 1e-12


def test_two_member_example():
    out = letkf_analysis([[-1.0], [1.0]], [1.0], lambda x: [x[0]], [1.0])
    assert abs(out[0][0] - (2 / 3 - 1 / math.sqrt(3))) < 1e-12
    assert abs(out[1][0] - (2 / 3 + 1 / math.sqrt(3))) < 1e-12


def test_page_example():
    # Two grid points at 0 and 3, one observation at 0, half-width c = 2.
    ens = [[-1.0, -1.0], [1.0, 1.0]]
    out = letkf_analysis(ens, [1.0], lambda x: [x[0]], [1.0], [0, 3], [0], 2)
    assert gaspari_cohn(Fr(3), Fr(2)) == Fr(19, 1152)
    assert abs(out[0][0] - (2 / 3 - 1 / math.sqrt(3))) < 1e-12
    assert abs(out[1][0] - (2 / 3 + 1 / math.sqrt(3))) < 1e-12
    spread = math.sqrt(1152 / 1190)
    assert abs(out[0][1] - (19 / 595 - spread)) < 1e-12
    assert abs(out[1][1] - (19 / 595 + spread)) < 1e-12


def test_gaspari_cohn_values():
    assert gaspari_cohn(0, 3) == 1
    assert gaspari_cohn(Fr(3), Fr(3)) == Fr(5, 24)
    assert gaspari_cohn(Fr(-3), Fr(3)) == Fr(5, 24)
    assert gaspari_cohn(6, 3) == 0
    assert gaspari_cohn(7.5, 3) == 0
    assert gaspari_cohn(Fr(599, 100), Fr(3)) > 0


def test_sym_eig_reconstructs():
    rng = random.Random(3)
    for n in (1, 2, 5, 8):
        L = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        A = scimat.add(L, scimat.transpose(L))
        vals, V = sym_eig(A)
        B = [[sum(V[i][m] * vals[m] * V[j][m] for m in range(n)) for j in range(n)] for i in range(n)]
        VtV = scimat.matmul(scimat.transpose(V), V)
        for i in range(n):
            for j in range(n):
                assert abs(B[i][j] - A[i][j]) < 1e-12
                assert abs(VtV[i][j] - (1.0 if i == j else 0.0)) < 1e-12


def test_global_matches_kalman_moments():
    # With every observation at weight 1 and rho = 1 the analysis mean is xbar + K d
    # and the analysis sample covariance is (I - K H) P^f, with the sample P^f.
    rng = random.Random(5)
    for _ in range(30):
        n, p, N = rng.randint(1, 5), rng.randint(1, 4), rng.randint(2, 8)
        ens = random_ensemble(rng, N, n)
        H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
        r = [rng.uniform(0.2, 2.0) for _ in range(p)]
        yo = [rng.gauss(0, 2) for _ in range(p)]
        out = letkf_analysis(ens, yo, lambda x: scimat.matvec(H, x), r)
        xbar = [sum(x[j] for x in ens) / N for j in range(n)]
        X = [[x[j] - xbar[j] for j in range(n)] for x in ens]
        Pf = [[sum(X[i][a] * X[i][b] for i in range(N)) / (N - 1) for b in range(n)] for a in range(n)]
        Rm = [[r[a] if a == b else 0.0 for b in range(p)] for a in range(p)]
        PHt = scimat.matmul(Pf, scimat.transpose(H))
        K = scimat.transpose(scimat.solve(scimat.add(scimat.matmul(H, PHt), Rm), scimat.transpose(PHt)))
        d = scimat.sub(yo, scimat.matvec(H, xbar))
        xa = scimat.add(xbar, scimat.matvec(K, d))
        Pa = scimat.matmul(scimat.sub(scimat.eye(n), scimat.matmul(K, H)), Pf)
        ma = [sum(x[j] for x in out) / N for j in range(n)]
        Xa = [[x[j] - ma[j] for j in range(n)] for x in out]
        Pe = [[sum(Xa[i][a] * Xa[i][b] for i in range(N)) / (N - 1) for b in range(n)] for a in range(n)]
        for a in range(n):
            assert abs(ma[a] - xa[a]) < 1e-9 * (1 + abs(xa[a]))
            for b in range(n):
                assert abs(Pe[a][b] - Pa[a][b]) < 1e-9 * (1 + abs(Pf[a][b]))


def test_local_equals_dense_oracle():
    rng = random.Random(7)
    n, N = 12, 6
    obs_idx = [0, 3, 4, 8, 11]
    dist = periodic_distance(n)
    for rho in (1.0, 1.2):
        ens = random_ensemble(rng, N, n)
        h = lambda x: [x[k] ** 2 / 4 + x[k] for k in obs_idx]  # nonlinear operator
        r = [rng.uniform(0.3, 1.5) for _ in obs_idx]
        yo = [rng.gauss(0, 1) for _ in obs_idx]
        out = letkf_analysis(ens, yo, h, r, list(range(n)), obs_idx, 2.0, rho, dist)
        for j in range(n):
            w = [(k, gaspari_cohn(dist(j, q), 2.0)) for k, q in enumerate(obs_idx)]
            w = [(k, v) for k, v in w if v > 0]
            ref = dense_point_update(ens, yo, h, r, j, w, rho)
            for i in range(N):
                assert abs(out[i][j] - ref[i]) < 1e-9


def test_useless_observations_keep_forecast():
    rng = random.Random(9)
    n, N = 10, 5
    obs_idx = [1, 4, 7]
    ens = random_ensemble(rng, N, n)
    out = letkf_analysis(ens, [0.5, -1.0, 2.0], lambda x: [x[k] for k in obs_idx], [1e12] * 3,
                         list(range(n)), obs_idx, 1.5, 1.0, periodic_distance(n))
    for i in range(N):
        for j in range(n):
            assert abs(out[i][j] - ens[i][j]) < 1e-9


def test_far_point_keeps_inflated_forecast():
    rng = random.Random(10)
    n, N = 20, 4
    ens = random_ensemble(rng, N, n)
    obs_idx = [0]
    out = letkf_analysis(ens, [3.0], lambda x: [x[0]], [1.0], list(range(n)), obs_idx, 2.0, 1.44,
                         periodic_distance(n))
    for j in range(4, 17):  # distance at least 4 = 2c from point 0
        xbar = sum(x[j] for x in ens) / N
        for i in range(N):
            assert abs(out[i][j] - (xbar + 1.2 * (ens[i][j] - xbar))) < 1e-12
    assert abs(out[0][0] - ens[0][0]) > 1e-3


def test_lorenz96_twin_rmse():
    # Measurement on the page: n = 40, every other variable observed every 0.05 with R = I.
    rng = random.Random(1)
    n, N, dt = 40, 10, 0.05
    x = [8.0] * n
    x[0] += 0.01
    for _ in range(1000):
        x = rk4(x, dt)
    ens, z = [], list(x)
    for _ in range(N):
        for _ in range(50):
            z = rk4(z, dt)
        ens.append(list(z))
    free = [list(e) for e in ens]
    obs_idx = list(range(0, n, 2))
    h = lambda s: [s[k] for k in obs_idx]
    dist = periodic_distance(n)
    errs, free_errs = [], []
    for _ in range(150):
        x = rk4(x, dt)
        ens = [rk4(e, dt) for e in ens]
        free = [rk4(e, dt) for e in free]
        yo = [x[k] + rng.gauss(0, 1) for k in obs_idx]
        ens = letkf_analysis(ens, yo, h, [1.0] * len(yo), list(range(n)), obs_idx, 2.0, 1.1, dist)
        m, _ = mean_and_spread(ens)
        mf, _ = mean_and_spread(free)
        errs.append(math.sqrt(sum((m[j] - x[j]) ** 2 for j in range(n)) / n))
        free_errs.append(math.sqrt(sum((mf[j] - x[j]) ** 2 for j in range(n)) / n))
    tail = errs[50:]
    assert sum(tail) / len(tail) < 0.7
    assert sum(free_errs[50:]) / 100 > 2.0
