# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-cross-validation/. The authors are listed in prov/7S65BE.jsonl.

import math
import random

from imgla import eye, matmul, matvec, norm2, solve, svd, transpose
from generalized_cross_validation import (
    coefficients,
    gcv_function,
    gcv_tikhonov,
    gcv_tikhonov_matrix,
    gcv_tsvd,
    tikhonov_svd,
)


def diag_problem(seed, n=32, sigma=1e-3):
    """A = diag(1/i^2), x_i = 1/i^2, white noise of standard deviation sigma."""
    s = [1.0 / i ** 2 for i in range(1, n + 1)]
    xt = [1.0 / i ** 2 for i in range(1, n + 1)]
    rng = random.Random(seed)
    y = [si * xi + sigma * rng.gauss(0.0, 1.0) for si, xi in zip(s, xt)]
    return s, xt, y


def risk(s, xt, sigma, alpha):
    """(1/m) E ||A x_alpha - A x||^2 for the diagonal problem."""
    tot = 0.0
    for si, xi in zip(s, xt):
        f = si * si / (si * si + alpha)
        tot += ((1.0 - f) * si * xi) ** 2 + sigma * sigma * f * f
    return tot / len(s)


def random_matrix(rng, m, n):
    return [[rng.gauss(0.0, 1.0) / (j + 1) ** 2 for j in range(n)] for _ in range(m)]


def hat_matrix(a, alpha):
    """H = A (A^T A + alpha I)^(-1) A^T, column by column."""
    at = transpose(a)
    ata = matmul(at, a)
    n = len(ata)
    for i in range(n):
        ata[i][i] += alpha
    m = len(a)
    cols = []
    for k in range(m):
        ek = [1.0 if i == k else 0.0 for i in range(m)]
        cols.append(matvec(a, solve(ata, matvec(at, ek))))
    return [[cols[j][i] for j in range(m)] for i in range(m)]


def test_page_example():
    s, xt, y = diag_problem(0)
    eye32 = eye(32)
    alpha, x, v = gcv_tikhonov(eye32, s, eye32, y)
    assert abs(alpha / 7.08667e-4 - 1.0) < 1e-3
    assert abs(v - 1.83444e-6) < 1e-10
    assert abs(math.dist(x, xt) - 0.06056) < 1e-4
    best = min(math.dist(tikhonov_svd(s, eye32, y, 10 ** (k / 100.0)), xt) for k in range(-700, 1))
    assert abs(best - 0.05817) < 1e-4
    assert math.dist(x, xt) <= 1.05 * best


def test_function_matches_dense_hat_matrix():
    rng = random.Random(3)
    a = random_matrix(rng, 9, 6)
    y = [rng.gauss(0.0, 1.0) for _ in range(9)]
    u, s, v = svd(a)
    b, p2 = coefficients(u, s, y)
    for alpha in (1e-4, 1e-2, 0.3):
        h = hat_matrix(a, alpha)
        r = [yi - hy for yi, hy in zip(y, matvec(h, y))]
        tr = 9.0 - sum(h[i][i] for i in range(9))
        direct = (norm2(r) ** 2 / 9.0) / (tr / 9.0) ** 2
        assert abs(gcv_function(s, b, p2, 9, alpha) - direct) <= 1e-9 * direct


def test_invariant_under_rotation_of_the_data_space():
    rng = random.Random(5)
    a = random_matrix(rng, 8, 5)
    y = [rng.gauss(0.0, 1.0) for _ in range(8)]
    q, _, _ = svd([[rng.gauss(0.0, 1.0) for _ in range(8)] for _ in range(8)])
    qa = matmul(q, a)
    qy = matvec(q, y)
    al1, x1, v1 = gcv_tikhonov_matrix(a, y, alpha_min=1e-6, alpha_max=10.0)
    al2, x2, v2 = gcv_tikhonov_matrix(qa, qy, alpha_min=1e-6, alpha_max=10.0)
    assert abs(al1 / al2 - 1.0) < 1e-4
    assert abs(v1 / v2 - 1.0) < 1e-8
    assert math.dist(x1, x2) <= 1e-4 * norm2(x1)


def test_result_is_not_above_any_grid_value():
    s, xt, y = diag_problem(1)
    eye32 = eye(32)
    b, p2 = coefficients(eye32, s, y)
    alpha, _, v = gcv_tikhonov(eye32, s, eye32, y)
    lo, hi = math.log(s[-1] ** 2), math.log(s[0] ** 2)
    grid = [gcv_function(s, b, p2, 32, math.exp(lo + (hi - lo) * j / 999)) for j in range(1000)]
    assert v <= min(grid) * (1.0 + 1e-9)
    assert abs(gcv_function(s, b, p2, 32, alpha) - v) <= 1e-15


def test_predictive_risk_close_to_the_best_on_average():
    ratios = []
    for seed in range(20):
        s, xt, y = diag_problem(100 + seed, n=64)
        e = eye(64)
        alpha, _, _ = gcv_tikhonov(e, s, e, y)
        best = min(risk(s, xt, 1e-3, 10 ** (k / 50.0)) for k in range(-500, 1))
        ratios.append(risk(s, xt, 1e-3, alpha) / best)
    ratios.sort()
    assert ratios[10] <= 1.3
    assert sum(1 for r in ratios if r <= 2.0) >= 16


def test_expected_gcv_function_and_the_golub_heath_wahba_bound():
    n, sigma = 32, 1e-3
    s = [1.0 / i ** 2 for i in range(1, n + 1)]
    g = [si / i ** 2 for i, si in enumerate(s, 1)]
    rng = random.Random(12)
    for alpha in (1e-4, 1e-3, 1e-2):
        f = [si * si / (si * si + alpha) for si in s]
        mu1 = sum(f) / n
        mu2 = sum(t * t for t in f) / n
        beta2 = sum(((1.0 - fi) * gi) ** 2 for fi, gi in zip(f, g)) / n
        expected = (beta2 + sigma * sigma * (1.0 - 2.0 * mu1 + mu2)) / (1.0 - mu1) ** 2
        t_risk = beta2 + sigma * sigma * mu2
        assert abs(expected - sigma * sigma - t_risk) <= t_risk * (2 * mu1 + mu1 * mu1 / mu2) / (1.0 - mu1) ** 2
        vals = []
        for _ in range(2000):
            y = [gi + sigma * rng.gauss(0.0, 1.0) for gi in g]
            vals.append(gcv_function(s, y, 0.0, n, alpha))
        mean = sum(vals) / len(vals)
        sd = math.sqrt(sum((t - mean) ** 2 for t in vals) / (len(vals) - 1))
        assert abs(mean - expected) <= 4.0 * sd / math.sqrt(len(vals))


def test_square_system_can_fail_at_the_lower_end():
    s, xt, y = diag_problem(2)
    eye32 = eye(32)
    alpha, x, _ = gcv_tikhonov(eye32, s, eye32, y)
    assert abs(alpha / s[-1] ** 2 - 1.0) < 1e-3
    best = min(math.dist(tikhonov_svd(s, eye32, y, 10 ** (k / 100.0)), xt) for k in range(-700, 1))
    assert math.dist(x, xt) > 10.0 * best


def test_tsvd_rule_matches_direct_projections():
    rng = random.Random(7)
    a = random_matrix(rng, 10, 6)
    y = [rng.gauss(0.0, 1.0) for _ in range(10)]
    u, s, v = svd(a)
    k, vals = gcv_tsvd(u, s, y)
    for kk in range(7):
        proj = [sum(u[i][c] * sum(u[j][c] * y[j] for j in range(10)) for c in range(kk)) for i in range(10)]
        r2 = sum((yi - pi) ** 2 for yi, pi in zip(y, proj))
        assert abs(vals[kk] - 10.0 * r2 / (10 - kk) ** 2) <= 1e-10 * max(1.0, vals[kk])
    assert vals[k] == min(vals)
