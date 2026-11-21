# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lepskii-balancing-principle/. The authors are listed in prov/WKH6V6.jsonl.

import math
import random

from imgla import eye, matmul, matvec, norm2, solve, svd, transpose
from lepskii_balancing_principle import (
    balancing,
    balancing_matrix,
    bias_norms,
    coefficients,
    geometric_grid,
    noise_bound,
    tikhonov_coeffs,
    tikhonov_svd,
)

EYE = eye(32)


def diag_problem(seed, sigma=1e-3, power=2.0, n=32):
    """A = diag(1/i^2), x_i = 1/i^power, white noise of standard deviation sigma."""
    s = [1.0 / i ** 2 for i in range(1, n + 1)]
    xt = [1.0 / i ** power for i in range(1, n + 1)]
    rng = random.Random(seed)
    e = [sigma * rng.gauss(0.0, 1.0) for _ in range(n)]
    y = [si * xi + ei for si, xi, ei in zip(s, xt, e)]
    return s, xt, y, norm2(e)


def test_page_example():
    s, xt, y, delta = diag_problem(0)
    assert abs(delta - 0.0065079) < 1e-6
    alphas = [1e-6 * 2 ** j for j in range(21)]
    alpha, x, j = balancing(EYE, s, EYE, y, delta, alphas=alphas)
    assert j == 16 and alpha == alphas[16]
    assert abs(math.dist(x, xt) - 0.19141) < 1e-5
    phi = bias_norms(s, EYE, xt, alphas)
    psi = [noise_bound(delta, a) for a in alphas]
    jstar = max(k for k in range(21) if phi[k] <= psi[k])
    assert jstar == 11
    assert math.dist(x, xt) <= 6.0 * psi[jstar]


def test_noise_bound_holds_and_is_attained():
    rng = random.Random(1)
    a = [[rng.gauss(0.0, 1.0) / (j + 1) for j in range(5)] for _ in range(7)]
    u, s, v = svd(a)
    at = transpose(a)
    for alpha in (1e-4, 1e-2, 1.0):
        ata = matmul(at, a)
        for i in range(5):
            ata[i][i] += alpha
        for _ in range(20):
            e = [rng.gauss(0.0, 1.0) for _ in range(7)]
            d = norm2(e)
            assert norm2(solve(ata, matvec(at, e))) <= noise_bound(d, alpha) * (1.0 + 1e-12)
    s1 = [1.0, 0.5]
    alpha = 0.25
    coeff = tikhonov_coeffs(s1, [0.0, 1.0], alpha)
    assert abs(norm2(coeff) - noise_bound(1.0, alpha)) < 1e-15


def test_oracle_inequality_over_noise_levels_and_seeds():
    for power in (1.5, 2.0, 3.0):
        for sigma in (1e-2, 1e-3, 1e-4, 1e-5):
            for seed in range(3):
                s, xt, y, delta = diag_problem(seed, sigma, power)
                alphas = geometric_grid(1e-9, 1.0, 2.0)
                alpha, x, j = balancing(EYE, s, EYE, y, delta, alphas=alphas)
                phi = bias_norms(s, EYE, xt, alphas)
                psi = [noise_bound(delta, a) for a in alphas]
                assert phi[0] <= psi[0]
                jstar = max(k for k in range(len(alphas)) if phi[k] <= psi[k])
                err = math.dist(x, xt)
                assert j >= jstar
                assert err <= 6.0 * psi[jstar] * (1.0 + 1e-12)
                oracle = min(p + q for p, q in zip(phi, psi))
                assert err <= 6.0 * math.sqrt(2.0) * oracle * (1.0 + 1e-12)


def test_result_is_the_largest_admissible_index():
    s, xt, y, delta = diag_problem(5)
    alphas = geometric_grid(1e-8, 1.0, 1.7)
    alpha, x, j = balancing(EYE, s, EYE, y, delta, alphas=alphas, kappa=1.3)
    co = [tikhonov_coeffs(s, y, a) for a in alphas]

    def admissible(k):
        return all(math.dist(co[k], co[i]) <= 4 * 1.3 * noise_bound(delta, alphas[i]) for i in range(k))

    assert admissible(j)
    assert not any(admissible(k) for k in range(j + 1, len(alphas)))
    assert all(admissible(k) for k in range(j))


def test_bias_is_nondecreasing_in_alpha():
    s, xt, y, delta = diag_problem(0)
    alphas = geometric_grid(1e-9, 10.0, 1.3)
    phi = bias_norms(s, EYE, xt, alphas)
    assert all(phi[k] <= phi[k + 1] for k in range(len(phi) - 1))


def test_dense_matrix_path():
    rng = random.Random(9)
    a = [[rng.gauss(0.0, 1.0) / (j + 1) ** 2 for j in range(6)] for _ in range(9)]
    xt = [1.0, -0.5, 0.25, 0.1, -0.05, 0.02]
    e = [1e-3 * rng.gauss(0.0, 1.0) for _ in range(9)]
    y = [p + q for p, q in zip(matvec(a, xt), e)]
    al1, x1, j1 = balancing_matrix(a, y, norm2(e))
    u, s, v = svd(a)
    b = coefficients(u, s, y)
    assert math.dist(x1, tikhonov_svd(s, v, b, al1)) <= 1e-12 * norm2(x1)
    at = transpose(a)
    ata = matmul(at, a)
    for i in range(6):
        ata[i][i] += al1
    assert math.dist(x1, solve(ata, matvec(at, y))) <= 1e-8 * norm2(x1)
