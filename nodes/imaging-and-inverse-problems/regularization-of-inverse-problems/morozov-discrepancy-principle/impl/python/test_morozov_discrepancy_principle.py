# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morozov-discrepancy-principle/. The authors are listed in prov/6BGG92.jsonl.

import math
import random

import pytest

from imgla import matvec, norm2, rmatvec, solve, svd, transpose, matmul
from morozov_discrepancy_principle import (
    DiscrepancyFailure,
    _f_and_slope,
    coefficients,
    discrepancy_index,
    discrepancy_tikhonov,
    discrepancy_tikhonov_matrix,
    residual_norm,
    tikhonov_svd,
)


def integration_matrix(n):
    """(A x)_i = h * sum_{j <= i} x_j with h = 1/n: a mildly ill-posed test operator."""
    h = 1.0 / n
    return [[h if j <= i else 0.0 for j in range(n)] for i in range(n)]


def noise(rng, m, delta):
    e = [rng.gauss(0.0, 1.0) for _ in range(m)]
    c = delta / norm2(e)
    return [c * t for t in e]


def tikhonov_solve(a, y, alpha):
    """x_alpha from the normal equations (A^T A + alpha I) x = A^T y."""
    ata = matmul(transpose(a), a)
    n = len(ata)
    for i in range(n):
        ata[i][i] += alpha
    return solve(ata, rmatvec(a, y))


def residual(a, x, y):
    return norm2([p - q for p, q in zip(matvec(a, x), y)])


def sine_problem(n, rel_noise, seed):
    rng = random.Random(seed)
    a = integration_matrix(n)
    xt = [math.sin(math.pi * (j + 0.5) / n) for j in range(n)]
    y0 = matvec(a, xt)
    delta = rel_noise * norm2(y0)
    y = [p + q for p, q in zip(y0, noise(rng, n, delta))]
    return a, xt, y, delta


def test_page_example():
    u = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    s = [1.0, 0.1, 0.01]
    y = [1.0, 0.13, 0.045]
    alpha, x, steps = discrepancy_tikhonov(u, s, u, y, 0.05, tau=1.2)
    assert abs(alpha - 0.0045272) < 1e-6
    assert steps == 11
    assert max(abs(p - q) for p, q in zip(x, [0.99549, 0.89487, 0.09725])) < 1e-4
    b, p2 = coefficients(u, s, y)
    assert abs(residual_norm(s, b, p2, alpha) - 0.06) < 1e-12
    assert abs(math.dist(x, [1.0, 1.0, 0.5]) - 0.41627) < 1e-4


def test_defining_equality_and_normal_equations():
    for seed in range(3):
        a, xt, y, delta = sine_problem(12, 0.02, seed)
        for tau in (1.0, 1.1, 1.5):
            alpha, x, _ = discrepancy_tikhonov_matrix(a, y, delta, tau)
            assert abs(residual(a, x, y) - tau * delta) <= 1e-8 * tau * delta
            xs = tikhonov_solve(a, y, alpha)
            assert norm2([p - q for p, q in zip(x, xs)]) <= 1e-8 * norm2(xs)


def test_residual_is_increasing_in_alpha():
    a, _, y, _ = sine_problem(10, 0.05, 7)
    u, s, v = svd(a)
    b, p2 = coefficients(u, s, y)
    grid = [10.0 ** (k / 4.0) for k in range(-40, 9)]
    r = [residual_norm(s, b, p2, al) for al in grid]
    assert all(r[i] < r[i + 1] for i in range(len(r) - 1))
    assert r[-1] < norm2(y)


def test_slope_matches_finite_difference():
    a, _, y, delta = sine_problem(8, 0.05, 3)
    u, s, v = svd(a)
    b, p2 = coefficients(u, s, y)
    for t in (-9.0, -5.0, -2.0, 0.5):
        h = 1e-5
        fp, _ = _f_and_slope(s, b, p2, delta * delta, t + h)
        fm, _ = _f_and_slope(s, b, p2, delta * delta, t - h)
        _, d = _f_and_slope(s, b, p2, delta * delta, t)
        assert abs((fp - fm) / (2 * h) - d) <= 1e-6 * abs(d)


def test_failure_when_data_outside_range_is_large():
    a = [[1.0, 0.0], [0.0, 0.5], [0.0, 0.0], [0.0, 0.0]]
    y = [1.0, 1.0, 0.3, 0.4]  # the part outside the range has norm 0.5
    with pytest.raises(DiscrepancyFailure):
        discrepancy_tikhonov_matrix(a, y, 0.4, tau=1.2)
    alpha, x, _ = discrepancy_tikhonov_matrix(a, y, 0.5, tau=1.2)
    assert abs(residual(a, x, y) - 0.6) < 1e-9


def test_small_data_gives_zero():
    a = integration_matrix(5)
    y = [0.01, -0.02, 0.0, 0.01, 0.0]
    alpha, x, steps = discrepancy_tikhonov_matrix(a, y, 0.05, tau=1.1)
    assert alpha == math.inf and steps == 0
    assert all(t == 0.0 for t in x)


def test_error_within_factor_of_best_on_grid():
    for seed in range(3):
        a, xt, y, delta = sine_problem(16, 0.01, 10 + seed)
        u, s, v = svd(a)
        b, _ = coefficients(u, s, y)
        alpha, x, _ = discrepancy_tikhonov(u, s, v, y, delta, tau=1.1)
        err = math.dist(x, xt)
        best = min(math.dist(tikhonov_svd(s, v, b, 10.0 ** (k / 8.0)), xt) for k in range(-80, 9))
        assert err <= 3.0 * best


def test_rate_under_source_condition():
    n, tau = 12, 1.1
    a = integration_matrix(n)
    w = [math.cos(math.pi * (j + 0.5) / n) for j in range(n)]
    xt = rmatvec(a, w)  # x_dagger = A^T w
    y0 = matvec(a, xt)
    u, s, v = svd(a)
    rng = random.Random(5)
    deltas, errs = [], []
    for k in range(1, 5):
        delta = 10.0 ** (-k) * norm2(y0)
        y = [p + q for p, q in zip(y0, noise(rng, n, delta))]
        _, x, _ = discrepancy_tikhonov(u, s, v, y, delta, tau)
        err = math.dist(x, xt)
        assert err <= math.sqrt(2.0 * (1.0 + tau) * norm2(w) * delta) * (1 + 1e-9)
        deltas.append(math.log(delta))
        errs.append(math.log(err))
    slope = (errs[-1] - errs[0]) / (deltas[-1] - deltas[0])
    assert slope >= 0.5 - 0.15


def plain_bisection(a, y, target):
    lo, hi = -40.0, 20.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if residual(a, tikhonov_solve(a, y, math.exp(mid)), y) > target:
            hi = mid
        else:
            lo = mid
    return math.exp((lo + hi) / 2)


def test_random_matrices_against_plain_bisection():
    rng = random.Random(2024)
    for _ in range(6):
        a = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(6)]
        y = [rng.uniform(-1, 1) for _ in range(6)]
        u, s, v = svd(a)
        b, p2 = coefficients(u, s, y)
        target = math.sqrt(p2) + 0.5 * (norm2(y) - math.sqrt(p2))
        alpha, x, _ = discrepancy_tikhonov(u, s, v, y, target / 1.1, tau=1.1)
        ref = plain_bisection(a, y, target)
        assert abs(math.log(alpha / ref)) < 1e-6
        assert abs(residual(a, x, y) - target) < 1e-9


def test_bracket_and_iteration_bound():
    rng = random.Random(99)
    eps = 1e-10
    for trial in range(10):
        a, _, y, delta = sine_problem(8, 10.0 ** (-1 - trial % 4), 200 + trial)
        u, s, v = svd(a)
        b, p2 = coefficients(u, s, y)
        tau = 1.0 + rng.random()
        target = tau * delta
        yn = norm2(y)
        q = (1.0 + target / yn) / 2.0
        hi = math.log(s[0] ** 2 * q / (1.0 - q))
        lo = math.log(s[-1] ** 2 * math.sqrt((target * target - p2) / 2.0) / yn)
        assert residual_norm(s, b, p2, math.exp(lo)) < target < residual_norm(s, b, p2, math.exp(hi))
        _, _, steps = discrepancy_tikhonov(u, s, v, y, delta, tau, eps)
        assert steps <= 2 * math.ceil(math.log2((hi - lo) / eps))


def test_discrete_rule():
    assert discrepancy_index([5.0, 3.0, 1.2, 1.0, 0.9], 1.0, tau=1.1) == 3
    assert discrepancy_index([5.0, 3.0], 1.0) is None
    a, xt, y, delta = sine_problem(10, 0.02, 4)
    u, s, v = svd(a)
    b, p2 = coefficients(u, s, y)
    # residual norms of truncated SVD with k = 0, 1, ..., n terms
    res = [math.sqrt(p2 + sum(t * t for t in b[k:])) for k in range(len(b) + 1)]
    k = discrepancy_index(res, delta, 1.1)
    assert k is not None and res[k] <= 1.1 * delta and (k == 0 or res[k - 1] > 1.1 * delta)
