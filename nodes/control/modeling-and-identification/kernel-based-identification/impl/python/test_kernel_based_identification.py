# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-based-identification/. The authors are listed in prov/BXFFBH.jsonl.

import math
import random

from ctlmat import det, mul, solve, transpose
from kernel_based_identification import (cholesky, dc_kernel, fit, kernel_fir, neg_log_marginal_likelihood,
                                         regressor, tc_kernel)


def _true_g(d):
    return [0.5 * 0.9 ** (k - 1) * math.cos(0.6 * (k - 1)) + 0.3 * 0.6 ** (k - 1) for k in range(1, d + 1)]


def _data(rng, g, N, sigma):
    u = [rng.gauss(0.0, 1.0) for _ in range(N)]
    y = [sum(g[t - 1] * u[k - t] for t in range(1, len(g) + 1) if k - t >= 0) + rng.gauss(0.0, sigma)
         for k in range(N)]
    return u, y


def _normal_eq(u, y, d):
    Phi = regressor(u, d)
    R = mul(transpose(Phi), Phi)
    r = [sum(Phi[k][t] * y[k] for k in range(len(y))) for t in range(d)]
    return Phi, R, r


def test_regressor_layout():
    assert regressor([1, 2, 3], 2) == [[0.0, 0.0], [1.0, 0.0], [2.0, 1.0]]


def test_dc_kernel_contains_tc_kernel():
    # rho = lam^(1/2) turns the DC kernel into the TC kernel
    lam = 0.8
    a, b = dc_kernel(6, 2.0, lam, math.sqrt(lam)), tc_kernel(6, 2.0, lam)
    assert all(abs(x - y) < 1e-14 for ra, rb in zip(a, b) for x, y in zip(ra, rb))
    L = cholesky(tc_kernel(6, 1.0, 0.7))
    back = mul(L, transpose(L))
    assert all(abs(x - y) < 1e-14 for ra, rb in zip(back, tc_kernel(6, 1.0, 0.7)) for x, y in zip(ra, rb))


def test_small_forms_match_the_n_by_n_formulas():
    rng = random.Random(3)
    d, N, sigma2 = 6, 25, 0.04
    u, y = _data(rng, _true_g(d), N, 0.2)
    Phi, R, r = _normal_eq(u, y, d)
    K = tc_kernel(d, 0.5, 0.8)
    Z = mul(mul(Phi, K), transpose(Phi))
    for i in range(N):
        Z[i][i] += sigma2
    zy = solve(Z, y)
    direct = [sum(v * w for v, w in zip(row, zy)) for row in mul(K, transpose(Phi))]
    assert max(abs(a - b) for a, b in zip(fit(R, r, K, sigma2), direct)) < 1e-10
    want = sum(a * b for a, b in zip(y, zy)) + math.log(det(Z))
    got = neg_log_marginal_likelihood(R, r, sum(v * v for v in y), N, K, sigma2)
    assert abs(got - want) < 1e-8 * abs(want)


def test_noise_free_recovery():
    # no noise and a tiny sigma2: the estimate is the exact FIR
    rng = random.Random(5)
    g = _true_g(8)
    u, y = _data(rng, g, 60, 0.0)
    grid = [(c, lam) for c in (0.3, 1.0) for lam in (0.7, 0.9)]
    g_hat, best, s2 = kernel_fir(u, y, 8, grid, sigma2=1e-10)
    assert max(abs(a - b) for a, b in zip(g_hat, g)) < 1e-6


def test_regularization_beats_least_squares():
    # measurement: d = 30, N = 120, noise standard deviation 0.3
    d, N = 30, 120
    g = _true_g(d)
    grid = [(c, lam) for c in (0.1, 0.3, 1.0) for lam in (0.7, 0.8, 0.9)]
    for seed in (1, 2, 3):
        rng = random.Random(seed)
        u, y = _data(rng, g, N, 0.3)
        g_hat, best, s2 = kernel_fir(u, y, d, grid)
        _, R, r = _normal_eq(u, y, d)
        g_ls = solve(R, r)
        err = math.sqrt(sum((a - b) ** 2 for a, b in zip(g_hat, g)))
        err_ls = math.sqrt(sum((a - b) ** 2 for a, b in zip(g_ls, g)))
        size = math.sqrt(sum(b * b for b in g))
        assert err < err_ls
        assert err < 0.2 * size
        assert 0.05 < s2 < 0.15


def test_dc_kernel_search():
    d, N = 20, 100
    g = _true_g(d)
    rng = random.Random(8)
    u, y = _data(rng, g, N, 0.3)
    grid = [(c, lam, rho) for c in (0.3, 1.0) for lam in (0.7, 0.9) for rho in (0.0, 0.9)]
    g_hat, best, s2 = kernel_fir(u, y, d, grid, kernel=dc_kernel)
    assert best in grid
    err = math.sqrt(sum((a - b) ** 2 for a, b in zip(g_hat, g)))
    assert err < 0.25 * math.sqrt(sum(b * b for b in g))
