# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplace-approximation/. The authors are listed in prov/M8AVZX.jsonl.
"""Tests for the Laplace approximation: exact Gaussian cases, the O(1/n) error, Stirling, Tierney-Kadane."""

import math
import random
import unittest

from laplace_approximation import (
    beta_binomial_laplace_logit,
    beta_binomial_laplace_p,
    beta_binomial_log_z,
    cholesky,
    cholesky_solve,
    gaussian_log_z,
    laplace,
    log_beta,
    stirling_log,
    tierney_kadane_beta_mean,
)


def simpson_log_z(logf, lo, hi, m=20000):
    """log of the integral of exp(logf) on [lo, hi] by Simpson's rule, scaled by the maximum."""
    h = (hi - lo) / m
    vals = [logf(lo + i * h) for i in range(m + 1)]
    top = max(vals)
    s = 0.0
    for i, v in enumerate(vals):
        w = 1 if i in (0, m) else (4 if i % 2 else 2)
        s += w * math.exp(v - top)
    return top + math.log(s * h / 3.0)


class TestLinearAlgebra(unittest.TestCase):
    def test_cholesky_random(self):
        rng = random.Random(1)
        for _ in range(500):
            d = rng.randint(1, 4)
            b = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(d)]
            a = [[sum(b[i][k] * b[j][k] for k in range(d)) + (1.0 if i == j else 0.0) for j in range(d)] for i in range(d)]
            low = cholesky(a)
            for i in range(d):
                for j in range(d):
                    self.assertAlmostEqual(sum(low[i][k] * low[j][k] for k in range(d)), a[i][j], places=10)
            y = [rng.uniform(-1, 1) for _ in range(d)]
            x = cholesky_solve(low, y)
            for i in range(d):
                self.assertAlmostEqual(sum(a[i][j] * x[j] for j in range(d)), y[i], places=9)

    def test_not_positive_definite(self):
        with self.assertRaises(ValueError):
            cholesky([[1.0, 2.0], [2.0, 1.0]])


class TestExactGaussian(unittest.TestCase):
    def test_normal_normal_is_exact(self):
        # y_i ~ N(theta, s2), theta ~ N(m0, t2). The log posterior is quadratic, so Laplace is exact.
        rng = random.Random(2)
        for _ in range(500):
            n = rng.randint(1, 8)
            s2, t2, m0 = rng.uniform(0.2, 3), rng.uniform(0.2, 3), rng.uniform(-2, 2)
            ys = [rng.gauss(0, 2) for _ in range(n)]

            def lp(v, ys=ys, s2=s2, t2=t2, m0=m0):
                th = v[0]
                return (-0.5 * sum((y - th) ** 2 for y in ys) / s2 - 0.5 * n * math.log(2 * math.pi * s2)
                        - 0.5 * (th - m0) ** 2 / t2 - 0.5 * math.log(2 * math.pi * t2))

            def gr(v, ys=ys, s2=s2, t2=t2, m0=m0):
                return [sum(y - v[0] for y in ys) / s2 - (v[0] - m0) / t2]

            def he(v, s2=s2, t2=t2):
                return [[-n / s2 - 1 / t2]]

            mode, cov, log_z = laplace(lp, gr, he, [0.0])
            # Oracle: y ~ N(m0 1, s2 I + t2 1 1^T); determinant lemma and Sherman-Morrison.
            r = [y - m0 for y in ys]
            sr = sum(r)
            quad = (sum(v * v for v in r) - t2 * sr * sr / (s2 + n * t2)) / s2
            logdet = n * math.log(s2) + math.log(1 + n * t2 / s2)
            exact = -0.5 * (n * math.log(2 * math.pi) + logdet + quad)
            self.assertAlmostEqual(log_z, exact, places=9)
            post_prec = n / s2 + 1 / t2
            self.assertAlmostEqual(cov[0][0], 1 / post_prec, places=12)
            self.assertAlmostEqual(mode[0], (sum(ys) / s2 + m0 / t2) / post_prec, places=9)

    def test_correlated_two_dim_gaussian(self):
        q = [[2.0, 0.7], [0.7, 1.0]]
        mu = [0.3, -1.2]

        def lp(v):
            a, b = v[0] - mu[0], v[1] - mu[1]
            return 1.5 - 0.5 * (q[0][0] * a * a + 2 * q[0][1] * a * b + q[1][1] * b * b)

        def gr(v):
            a, b = v[0] - mu[0], v[1] - mu[1]
            return [-(q[0][0] * a + q[0][1] * b), -(q[0][1] * a + q[1][1] * b)]

        mode, cov, log_z = laplace(lp, gr, lambda v: [[-q[0][0], -q[0][1]], [-q[0][1], -q[1][1]]], [5.0, 5.0])
        self.assertAlmostEqual(log_z, gaussian_log_z(mu, q, 1.5), places=12)
        self.assertAlmostEqual(mode[0], mu[0], places=12)
        det = q[0][0] * q[1][1] - q[0][1] ** 2
        self.assertAlmostEqual(cov[0][1], -q[0][1] / det, places=12)


class TestErrorRate(unittest.TestCase):
    def test_beta_binomial_values_of_the_page(self):
        self.assertAlmostEqual(beta_binomial_log_z(30, 100, 2, 2), -63.028491, places=5)
        self.assertAlmostEqual(beta_binomial_log_z(30, 100, 2, 2) - beta_binomial_laplace_p(30, 100, 2, 2), -0.006711, places=5)
        self.assertAlmostEqual(beta_binomial_log_z(30, 100, 2, 2) - beta_binomial_laplace_logit(30, 100, 2, 2), 0.002960, places=5)

    def test_relative_error_falls_like_one_over_n(self):
        # x = 0.3 n, prior Beta(2, 2). n times the log error must settle to a constant.
        for fn, limit in ((beta_binomial_laplace_p, -0.6865), (beta_binomial_laplace_logit, 0.3133)):
            scaled = []
            for n in (10, 100, 1000, 10000):
                x = 3 * n // 10
                scaled.append(n * (beta_binomial_log_z(x, n, 2, 2) - fn(x, n, 2, 2)))
            self.assertAlmostEqual(scaled[-1], limit, delta=0.002)
            gaps = [abs(s - limit) for s in scaled]
            self.assertTrue(all(gaps[i + 1] < gaps[i] for i in range(len(gaps) - 1)))

    def test_independent_oracle_by_quadrature(self):
        # Simpson's rule in the p scale gives the exact value to 1e-8, independent of lgamma.
        rng = random.Random(3)
        for _ in range(30):
            n = rng.randint(5, 60)
            x = rng.randint(1, n - 1)
            a, b = rng.uniform(1, 4), rng.uniform(1, 4)
            lb = log_beta(a, b)
            exact = simpson_log_z(lambda p: (a + x - 1) * math.log(p) + (b + n - x - 1) * math.log1p(-p) - lb if 0 < p < 1 else -1e300, 0.0, 1.0)
            self.assertAlmostEqual(exact, beta_binomial_log_z(x, n, a, b), places=6)
            err = abs(exact - beta_binomial_laplace_logit(x, n, a, b))
            # In the logit scale the error is mu(al) + mu(be) - mu(al + be) with
            # 0 < mu(z) < 1/(12 z), the error of Stirling's formula for Gamma(z).
            al, be = a + x, b + n - x
            self.assertLess(err, 1.0 / (12 * al) + 1.0 / (12 * be))

    def test_error_adds_over_independent_blocks(self):
        # d independent copies: the log error is d times the error of one copy.
        x, n, a, b = 3, 10, 2.0, 2.0
        one = beta_binomial_log_z(x, n, a, b) - beta_binomial_laplace_logit(x, n, a, b)
        for d in (1, 2, 3, 5):
            al, be = a + x, b + n - x

            def lp(v):
                return sum(-al * math.log1p(math.exp(-t)) - be * math.log1p(math.exp(t)) - log_beta(a, b) for t in v)

            def gr(v):
                return [al - (al + be) / (1 + math.exp(-t)) for t in v]

            def he(v):
                out = [[0.0] * d for _ in range(d)]
                for i, t in enumerate(v):
                    p = 1 / (1 + math.exp(-t))
                    out[i][i] = -(al + be) * p * (1 - p)
                return out

            log_z = laplace(lp, gr, he, [0.1 * i for i in range(d)])[2]
            self.assertAlmostEqual(d * beta_binomial_log_z(x, n, a, b) - log_z, d * one, places=9)


class TestStirlingAndTierneyKadane(unittest.TestCase):
    def test_stirling(self):
        for n, val in ((1, 0.081061), (10, 0.0083306), (1000, 8.33333e-5)):
            self.assertAlmostEqual(math.lgamma(n + 1) - stirling_log(n), val, delta=val * 1e-4)
        self.assertAlmostEqual(1000 * (math.lgamma(1001) - stirling_log(1000)), 1 / 12, places=6)

    def test_tierney_kadane_error_is_order_n_minus_two(self):
        scaled = []
        for n in (10, 100, 1000):
            x = 3 * n // 10
            al, be = 2 + x, 2 + n - x
            exact = al / (al + be)
            scaled.append(n * n * (tierney_kadane_beta_mean(al, be) - exact) / exact)
        self.assertAlmostEqual(scaled[0], 0.2375, places=3)
        self.assertAlmostEqual(scaled[2], 0.8281, places=3)
        self.assertTrue(all(0 < s < 1 for s in scaled))


if __name__ == "__main__":
    unittest.main()
