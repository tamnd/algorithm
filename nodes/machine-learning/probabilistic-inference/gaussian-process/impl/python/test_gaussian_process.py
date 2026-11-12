# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-process/. The authors are listed in prov/6GME91.jsonl.

import math
import random

from gaussian_process import (cholesky, gp_posterior_covariance, gp_regression, gram, rbf,
                              sample_prior)


def inverse_and_logdet(a):
    """Gauss-Jordan elimination with partial pivoting: (a^-1, log |det a|)."""
    n = len(a)
    m = [list(map(float, row)) + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(a)]
    logdet = 0.0
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        logdet += math.log(abs(piv))
        m[c] = [v / piv for v in m[c]]
        for r in range(n):
            if r != c:
                f = m[r][c]
                m[r] = [vr - f * vc for vr, vc in zip(m[r], m[c])]
    return [row[n:] for row in m], logdet


def matvec(a, x):
    return [sum(p * q for p, q in zip(row, x)) for row in a]


def random_problem(rng, n, d):
    xs = [[rng.uniform(-3, 3) for _ in range(d)] for _ in range(n)]
    y = [math.sin(sum(x)) + rng.gauss(0, 0.1) for x in xs]
    xstar = [[rng.uniform(-4, 4) for _ in range(d)] for _ in range(5)]
    length = rng.uniform(0.5, 2.0)
    var = rng.uniform(0.5, 2.0)
    noise = rng.uniform(0.01, 0.5)
    return xs, y, xstar, (lambda a, b: rbf(a, b, length, var)), noise


def test_example_of_the_page():
    m, v, lml = gp_regression([0.0, 1.0, 3.0], [0.5, 1.0, -0.5], rbf, 0.1, [2.0])
    assert abs(m[0] - 0.2649) < 1e-4 and abs(v[0] - 0.3674) < 1e-4 and abs(lml + 3.3473) < 1e-4


def test_cholesky_reconstructs():
    rng = random.Random(1)
    xs = [rng.uniform(-2, 2) for _ in range(8)]
    a = gram(xs, xs, rbf)
    a = [[a[i][j] + (0.1 if i == j else 0) for j in range(8)] for i in range(8)]
    L = cholesky(a)
    for i in range(8):
        for j in range(8):
            assert abs(sum(L[i][t] * L[j][t] for t in range(8)) - a[i][j]) < 1e-12


def test_algorithm_2_1_against_a_direct_solve():
    rng = random.Random(7)
    for _ in range(20):
        n, d = rng.randint(1, 9), rng.randint(1, 3)
        xs, y, xstar, k, noise = random_problem(rng, n, d)
        means, variances, lml = gp_regression(xs, y, k, noise, xstar)
        A = [[k(xs[i], xs[j]) + (noise if i == j else 0.0) for j in range(n)] for i in range(n)]
        Ainv, logdet = inverse_and_logdet(A)
        Ay = matvec(Ainv, y)
        for s, m, v in zip(xstar, means, variances):
            ks = [k(x, s) for x in xs]
            assert abs(m - sum(p * q for p, q in zip(ks, Ay))) < 1e-9
            assert abs(v - (k(s, s) - sum(p * q for p, q in zip(ks, matvec(Ainv, ks))))) < 1e-9
        want = -0.5 * sum(p * q for p, q in zip(y, Ay)) - 0.5 * logdet - 0.5 * n * math.log(2 * math.pi)
        assert abs(lml - want) < 1e-9


def test_mean_equals_kernel_ridge_regression():
    # Kernel ridge: minimize sum (f(x_i) - y_i)^2 + lam ||f||^2, so alpha = (K + lam I)^-1 y.
    rng = random.Random(11)
    for _ in range(20):
        n, d = rng.randint(1, 9), rng.randint(1, 3)
        xs, y, xstar, k, noise = random_problem(rng, n, d)
        lam = noise
        K = gram(xs, xs, k)
        Ainv, _ = inverse_and_logdet([[K[i][j] + (lam if i == j else 0.0) for j in range(n)]
                                      for i in range(n)])
        alpha = matvec(Ainv, y)
        krr = [sum(a * k(x, s) for a, x in zip(alpha, xs)) for s in xstar]
        means, _, _ = gp_regression(xs, y, k, noise, xstar)
        for a, b in zip(means, krr):
            assert abs(a - b) < 1e-9


def test_posterior_variance_at_most_prior_and_free_of_y():
    rng = random.Random(5)
    for _ in range(20):
        n, d = rng.randint(1, 9), rng.randint(1, 3)
        xs, y, xstar, k, noise = random_problem(rng, n, d)
        _, v1, _ = gp_regression(xs, y, k, noise, xstar)
        _, v2, _ = gp_regression(xs, [rng.gauss(0, 5) for _ in y], k, noise, xstar)
        for s, a, b in zip(xstar, v1, v2):
            assert -1e-12 <= a <= k(s, s) + 1e-12
            assert abs(a - b) < 1e-12
        C = gp_posterior_covariance(xs, k, noise, xstar)
        for i in range(len(xstar)):
            assert abs(C[i][i] - v1[i]) < 1e-12


def test_far_from_the_data_the_prior_returns():
    m, v, _ = gp_regression([0.0, 1.0], [1.0, 2.0], rbf, 0.1, [50.0])
    assert abs(m[0]) < 1e-12 and abs(v[0] - 1.0) < 1e-12


def test_small_noise_interpolates():
    xs, y = [0.0, 0.7, 2.0], [1.0, -1.0, 0.5]
    m, v, _ = gp_regression(xs, y, rbf, 1e-10, xs)
    for a, b in zip(m, y):
        assert abs(a - b) < 1e-6
    assert max(v) < 1e-6


def test_prior_samples_have_the_kernel_covariance():
    rng = random.Random(3)
    xs = [0.0, 0.5, 2.0]
    s = 20000
    acc = [[0.0] * 3 for _ in range(3)]
    for _ in range(s):
        f = sample_prior(xs, rbf, rng)
        for i in range(3):
            for j in range(3):
                acc[i][j] += f[i] * f[j] / s
    for i in range(3):
        for j in range(3):
            assert abs(acc[i][j] - rbf(xs[i], xs[j])) < 0.05
