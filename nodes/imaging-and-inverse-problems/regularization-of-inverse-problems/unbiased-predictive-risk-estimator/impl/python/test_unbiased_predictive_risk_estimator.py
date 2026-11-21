# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unbiased-predictive-risk-estimator/. The authors are listed in prov/FEKTYX.jsonl.

import math
import random

from imgla import eye, matmul, matvec, norm2, solve, svd, transpose
from unbiased_predictive_risk_estimator import (
    coefficients,
    predictive_risk,
    tikhonov_svd,
    upre_function,
    upre_tikhonov,
    upre_tikhonov_matrix,
    upre_tsvd,
)

SIGMA = 1e-3


def diag_problem(seed, n=32, sigma=SIGMA):
    """A = diag(1/i^2), x_i = 1/i^2, white noise of standard deviation sigma."""
    s = [1.0 / i ** 2 for i in range(1, n + 1)]
    xt = [1.0 / i ** 2 for i in range(1, n + 1)]
    rng = random.Random(seed)
    y = [si * xi + sigma * rng.gauss(0.0, 1.0) for si, xi in zip(s, xt)]
    return s, xt, y


def random_matrix(rng, m, n):
    return [[rng.gauss(0.0, 1.0) / (j + 1) ** 2 for j in range(n)] for _ in range(m)]


def test_page_example():
    s, xt, y = diag_problem(0)
    e = eye(32)
    alpha, x, val = upre_tikhonov(e, s, e, y, SIGMA)
    assert abs(alpha / 5.04162e-4 - 1.0) < 1e-3
    assert abs(val - 5.69561e-7) < 1e-11
    assert abs(math.dist(x, xt) - 0.06641) < 1e-4
    c0 = [si * xi for si, xi in zip(s, xt)]
    grid = [10 ** (k / 100.0) for k in range(-700, 1)]
    rmin = min(predictive_risk(s, c0, 32, SIGMA, a) for a in grid)
    assert abs(rmin - 1.954e-7) < 1e-10
    assert predictive_risk(s, c0, 32, SIGMA, alpha) <= 1.02 * rmin


def test_function_matches_dense_formula():
    rng = random.Random(3)
    m, n = 9, 6
    a = random_matrix(rng, m, n)
    y = [rng.gauss(0.0, 1.0) for _ in range(m)]
    u, s, v = svd(a)
    b, p2 = coefficients(u, s, y)
    at = transpose(a)
    for alpha in (1e-4, 1e-2, 0.3):
        ata = matmul(at, a)
        for i in range(n):
            ata[i][i] += alpha
        x = solve(ata, matvec(at, y))
        r = [yi - ax for yi, ax in zip(y, matvec(a, x))]
        tr = 0.0
        for k in range(m):
            ek = [1.0 if i == k else 0.0 for i in range(m)]
            tr += matvec(a, solve(ata, matvec(at, ek)))[k]
        sig = 0.2
        direct = norm2(r) ** 2 / m + 2.0 * sig * sig * tr / m - sig * sig
        assert abs(upre_function(s, b, p2, m, sig, alpha) - direct) <= 1e-9 * max(1.0, abs(direct))


def test_unbiased_by_monte_carlo():
    s = [1.0 / i ** 2 for i in range(1, 33)]
    xt = [1.0 / i ** 2 for i in range(1, 33)]
    c0 = [si * xi for si, xi in zip(s, xt)]
    rng = random.Random(11)
    for alpha in (1e-5, 1e-3, 1e-1):
        vals = []
        for _ in range(3000):
            y = [ci + SIGMA * rng.gauss(0.0, 1.0) for ci in c0]
            vals.append(upre_function(s, y, 0.0, 32, SIGMA, alpha))
        mean = sum(vals) / len(vals)
        sd = math.sqrt(sum((t - mean) ** 2 for t in vals) / (len(vals) - 1))
        true = predictive_risk(s, c0, 32, SIGMA, alpha)
        assert abs(mean - true) <= 4.0 * sd / math.sqrt(len(vals))


def test_predictive_risk_close_to_the_best():
    ratios = []
    for seed in range(20):
        s, xt, y = diag_problem(100 + seed, n=64)
        e = eye(64)
        c0 = [si * xi for si, xi in zip(s, xt)]
        alpha, _, _ = upre_tikhonov(e, s, e, y, SIGMA)
        best = min(predictive_risk(s, c0, 64, SIGMA, 10 ** (k / 50.0)) for k in range(-500, 1))
        ratios.append(predictive_risk(s, c0, 64, SIGMA, alpha) / best)
    ratios.sort()
    assert ratios[10] <= 1.3
    assert ratios[-1] <= 3.0


def test_dense_and_svd_paths_agree():
    rng = random.Random(4)
    a = random_matrix(rng, 10, 6)
    y = [rng.gauss(0.0, 1.0) for _ in range(10)]
    u, s, v = svd(a)
    al1, x1, v1 = upre_tikhonov(u, s, v, y, 0.1, alpha_min=1e-6, alpha_max=10.0)
    al2, x2, v2 = upre_tikhonov_matrix(a, y, 0.1, alpha_min=1e-6, alpha_max=10.0)
    assert abs(al1 / al2 - 1.0) < 1e-9
    assert math.dist(x1, x2) <= 1e-12 * max(1.0, norm2(x1))
    b, p2 = coefficients(u, s, y)
    assert abs(upre_function(s, b, p2, 10, 0.1, al1) - v1) <= 1e-15


def test_tsvd_rule_matches_direct_projections():
    rng = random.Random(7)
    a = random_matrix(rng, 10, 6)
    y = [rng.gauss(0.0, 1.0) for _ in range(10)]
    u, s, v = svd(a)
    k, vals = upre_tsvd(u, s, y, 0.3)
    for kk in range(7):
        proj = [sum(u[i][c] * sum(u[j][c] * y[j] for j in range(10)) for c in range(kk)) for i in range(10)]
        r2 = sum((yi - pi) ** 2 for yi, pi in zip(y, proj))
        assert abs(vals[kk] - (r2 / 10 + 2 * 0.09 * kk / 10 - 0.09)) <= 1e-10
    assert vals[k] == min(vals)


def test_tikhonov_svd_solves_the_normal_equations():
    rng = random.Random(8)
    a = random_matrix(rng, 7, 5)
    y = [rng.gauss(0.0, 1.0) for _ in range(7)]
    u, s, v = svd(a)
    b, _ = coefficients(u, s, y)
    at = transpose(a)
    ata = matmul(at, a)
    for i in range(5):
        ata[i][i] += 0.01
    x = solve(ata, matvec(at, y))
    assert math.dist(tikhonov_svd(s, v, b, 0.01), x) <= 1e-9 * norm2(x)
