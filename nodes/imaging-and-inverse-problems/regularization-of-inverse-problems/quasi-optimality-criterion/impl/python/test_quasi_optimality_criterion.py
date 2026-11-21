# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quasi-optimality-criterion/. The authors are listed in prov/4809JZ.jsonl.

import math
import random

from imgla import eye, matmul, matvec, norm2, solve, svd, transpose
from quasi_optimality_criterion import (
    coefficients,
    continuous_measure,
    quasi_optimality,
    quasi_optimality_matrix,
    step_norm,
    tikhonov_svd,
)


def diag_problem(seed, n=32, sigma=1e-3):
    """A = diag(1/i^2), x_i = 1/i^2, white noise of standard deviation sigma."""
    s = [1.0 / i ** 2 for i in range(1, n + 1)]
    xt = [1.0 / i ** 2 for i in range(1, n + 1)]
    rng = random.Random(seed)
    y = [si * xi + sigma * rng.gauss(0.0, 1.0) for si, xi in zip(s, xt)]
    return s, xt, y


def random_matrix(rng, m, n):
    return [[rng.gauss(0.0, 1.0) / (j + 1) ** 2 for j in range(n)] for _ in range(m)]


def tikhonov_solve(a, y, alpha):
    at = transpose(a)
    ata = matmul(at, a)
    for i in range(len(ata)):
        ata[i][i] += alpha
    return solve(ata, matvec(at, y))


def test_page_example():
    s, xt, y = diag_problem(0)
    e = eye(32)
    alpha, x, j, d = quasi_optimality(e, s, e, y)
    assert len(d) == 20
    assert j == 9 and alpha == 0.5 ** 9
    assert abs(d[9] - 0.017480) < 1e-6
    assert abs(d[8] - 0.018896) < 1e-6 and abs(d[10] - 0.022928) < 1e-6
    assert abs(math.dist(x, xt) - 0.06146) < 1e-5
    best = min(math.dist(tikhonov_svd(s, e, y, 10 ** (k / 100.0)), xt) for k in range(-700, 1))
    assert math.dist(x, xt) <= 1.06 * best


def test_step_norm_matches_dense_solves():
    rng = random.Random(2)
    a = random_matrix(rng, 8, 6)
    y = [rng.gauss(0.0, 1.0) for _ in range(8)]
    u, s, v = svd(a)
    b = coefficients(u, s, y)
    for a1, a2 in ((0.1, 0.05), (1e-3, 5e-4), (1e-5, 1e-6)):
        x1, x2 = tikhonov_solve(a, y, a1), tikhonov_solve(a, y, a2)
        assert abs(step_norm(s, b, a1, a2) - math.dist(x1, x2)) <= 1e-8 * max(1.0, norm2(x1))
        assert math.dist(tikhonov_svd(s, v, b, a1), x1) <= 1e-8 * max(1.0, norm2(x1))


def test_derivative_formula_and_continuous_limit():
    rng = random.Random(4)
    a = random_matrix(rng, 7, 5)
    y = [rng.gauss(0.0, 1.0) for _ in range(7)]
    u, s, v = svd(a)
    b = coefficients(u, s, y)
    alpha = 2e-3
    x = tikhonov_solve(a, y, alpha)
    at = transpose(a)
    ata = matmul(at, a)
    for i in range(5):
        ata[i][i] += alpha
    dx = [-t for t in solve(ata, x)]
    h = 1e-6 * alpha
    fd = [(p - q) / (2 * h) for p, q in zip(tikhonov_solve(a, y, alpha + h), tikhonov_solve(a, y, alpha - h))]
    assert math.dist(dx, fd) <= 1e-5 * norm2(dx)
    assert abs(continuous_measure(s, b, alpha) - alpha * norm2(dx)) <= 1e-8 * alpha * norm2(dx)
    q = 0.999
    ratio = step_norm(s, b, alpha, q * alpha) / ((1.0 - q) * continuous_measure(s, b, alpha))
    assert abs(ratio - 1.0) < 2e-3


def test_error_close_to_best_over_seeds():
    e = eye(32)
    for seed in range(5):
        s, xt, y = diag_problem(seed)
        alpha, x, _, _ = quasi_optimality(e, s, e, y)
        best = min(math.dist(tikhonov_svd(s, e, y, 10 ** (k / 100.0)), xt) for k in range(-700, 1))
        assert math.dist(x, xt) <= 1.5 * best


def test_chosen_index_is_the_minimum_and_matrix_path_agrees():
    rng = random.Random(6)
    a = random_matrix(rng, 9, 6)
    xt = [1.0, -0.5, 0.25, 0.1, -0.05, 0.02]
    y = [p + 1e-3 * rng.gauss(0.0, 1.0) for p in matvec(a, xt)]
    u, s, v = svd(a)
    al1, x1, j1, d1 = quasi_optimality(u, s, v, y, q=0.7)
    al2, x2, j2, d2 = quasi_optimality_matrix(a, y, q=0.7)
    assert j1 == j2 and d1[j1] == min(d1)
    assert math.dist(x1, x2) <= 1e-12 * norm2(x1)
    assert math.dist(x1, tikhonov_solve(a, y, al1)) <= 1e-8 * norm2(x1)


def test_scaling_multiplies_alpha_by_c_squared():
    s, xt, y = diag_problem(1)
    e = eye(32)
    c = 3.0
    al1, x1, j1, _ = quasi_optimality(e, s, e, y)
    al2, x2, j2, _ = quasi_optimality(e, [c * t for t in s], e, [c * t for t in y])
    assert j1 == j2 and abs(al2 / (c * c * al1) - 1.0) < 1e-12
    assert math.dist(x1, x2) <= 1e-12 * norm2(x1)
