# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/posterior-predictive-check/. The authors are listed in prov/2TJBEH.jsonl.
"""Tests for posterior predictive checks: the template against closed forms, the pile-up
of p-values near 1/2 when the model is true, Meng's bound P(p <= alpha) <= 2 alpha and
the mean (1 + P(tie)) / 2 in exact arithmetic, the uniform p-value of an ancillary
statistic, and the detection of overdispersed counts."""

import math
import random
import statistics
import unittest
from fractions import Fraction as F

from posterior_predictive_check import (
    dispersion,
    normal_posterior,
    pileup_factor,
    poisson,
    poisson_gamma_check,
    ppc,
    ppp_mean,
    ppp_mean_tail,
    ppp_mean_variance,
    ppp_variance_known_sigma,
)


def mean_stat(y, _theta=None):
    return sum(y) / len(y)


class TestNormalMean(unittest.TestCase):
    def test_template_matches_the_closed_form(self):
        rng = random.Random(1)
        n, sigma, tau = 10, 1.0, 1.0
        xs = [rng.gauss(0.8, sigma) for _ in range(n)]
        m, v = normal_posterior(mean_stat(xs), n, sigma, tau)
        draws = [rng.gauss(m, math.sqrt(v)) for _ in range(20000)]
        p, pairs = ppc(xs, draws, lambda t, r: [r.gauss(t, sigma) for _ in range(n)], mean_stat, rng)
        exact = ppp_mean(mean_stat(xs), n, sigma, tau)
        self.assertEqual(len(pairs), 20000)
        self.assertLess(abs(p - exact), 4 * math.sqrt(exact * (1 - exact) / 20000))

    def test_p_values_pile_up_near_one_half(self):
        n, sigma, tau = 1, 1.0, 1.0
        c = pileup_factor(n, sigma, tau)
        self.assertAlmostEqual(c, 1 / math.sqrt(3), places=12)
        rng = random.Random(2)
        ps = []
        for _ in range(4000):
            th = rng.gauss(0, tau)
            xbar = rng.gauss(th, sigma / math.sqrt(n))
            ps.append(ppp_mean(xbar, n, sigma, tau))
        sd = statistics.pstdev(ps)
        self.assertLess(abs(sd - math.sqrt(ppp_mean_variance(c))), 0.01)
        self.assertLess(sd, 0.25)  # a uniform p-value has sd 0.2887
        mid = sum(0.25 < p < 0.75 for p in ps) / len(ps)
        z = statistics.NormalDist().inv_cdf(0.75) / c
        exact_mid = 2 * statistics.NormalDist().cdf(z) - 1  # 0.757, against 0.5 for uniform
        self.assertLess(abs(mid - exact_mid), 4 * math.sqrt(exact_mid * (1 - exact_mid) / len(ps)))
        self.assertLess(sum(p <= 0.05 for p in ps) / len(ps), 0.01)
        self.assertAlmostEqual(ppp_mean_tail(0.05, c), 0.00219, places=5)

    def test_variance_formula(self):
        nd = statistics.NormalDist()
        self.assertAlmostEqual(ppp_mean_variance(1.0), 1 / 12, places=14)
        for c in (0.1, 0.3, 0.7, 1.0, 2.0):
            # Simpson's rule for E[Phi(cZ)^2] - 1/4 over z in [-10, 10]
            h, k = 0.01, 2000
            vals = [nd.cdf(c * (-10 + h * i)) ** 2 * nd.pdf(-10 + h * i) for i in range(k + 1)]
            integral = h / 3 * (vals[0] + vals[-1] + 4 * sum(vals[1:-1:2]) + 2 * sum(vals[2:-1:2]))
            self.assertAlmostEqual(integral - 0.25, ppp_mean_variance(c), places=8)


def discrete_ppp_law(prior, like):
    """Exact posterior predictive p-values of T(y) = y for every y, and the prior predictive m(y)."""
    k, ys = len(prior), range(len(like[0]))
    m = [sum(prior[t] * like[t][y] for t in range(k)) for y in ys]
    tail = [[sum(like[t][z] for z in ys if z >= y) for y in ys] for t in range(k)]
    p = [sum(prior[t] * like[t][y] * tail[t][y] for t in range(k)) / m[y] for y in ys]
    return p, m


class TestExactDiscrete(unittest.TestCase):
    def test_meng_bound_and_the_mean(self):
        rng = random.Random(3)
        for _ in range(300):
            k = rng.randint(1, 4)
            n = rng.randint(1, 8)
            raw = [rng.randint(1, 9) for _ in range(k)]
            prior = [F(v, sum(raw)) for v in raw]
            ps = [F(rng.randint(1, 9), 10) for _ in range(k)]
            like = [[math.comb(n, y) * q**y * (1 - q) ** (n - y) for y in range(n + 1)] for q in ps]
            p, m = discrete_ppp_law(prior, like)
            # Meng (1994): P(p <= alpha) <= 2 alpha; it suffices to check at the attained values
            for a in p:
                self.assertLessEqual(sum(mm for pp, mm in zip(p, m) if pp <= a), 2 * a)
            # E[p] = (1 + P(Y = Y')) / 2 for Y, Y' independent given theta
            tie = sum(prior[t] * sum(v * v for v in like[t]) for t in range(k))
            self.assertEqual(sum(pp * mm for pp, mm in zip(p, m)), (1 + tie) / 2)


class TestAncillaryStatistic(unittest.TestCase):
    def test_sample_variance_with_known_sigma_is_uniform(self):
        rng = random.Random(4)
        n, sigma, tau = 5, 1.0, 2.0
        ps = []
        for _ in range(3000):
            th = rng.gauss(0, tau)
            xs = [rng.gauss(th, sigma) for _ in range(n)]
            ps.append(ppp_variance_known_sigma(xs, sigma))
        ps.sort()
        ks = max(max((i + 1) / len(ps) - v, v - i / len(ps)) for i, v in enumerate(ps))
        self.assertLess(ks, 1.63 / math.sqrt(len(ps)))
        # the template gives the same value on one data set
        xs = [rng.gauss(0.5, sigma) for _ in range(n)]
        m, v = normal_posterior(sum(xs) / n, n, sigma, tau)
        draws = [rng.gauss(m, math.sqrt(v)) for _ in range(20000)]

        def s2(y, _t=None):
            mu = sum(y) / len(y)
            return sum((a - mu) ** 2 for a in y) / (len(y) - 1)

        p, _ = ppc(xs, draws, lambda t, r: [r.gauss(t, sigma) for _ in range(n)], s2, rng)
        exact = ppp_variance_known_sigma(xs, sigma)
        self.assertLess(abs(p - exact), 4 * math.sqrt(exact * (1 - exact) / 20000) + 1e-9)


class TestCounts(unittest.TestCase):
    def test_overdispersion_is_detected(self):
        rng = random.Random(8)
        xa = [poisson(4.0, rng) for _ in range(20)]
        xb = [poisson(rng.gammavariate(2.0, 2.0), rng) for _ in range(20)]
        pa = poisson_gamma_check(xa, 1.0, 0.25, 4000, random.Random(9))
        pb = poisson_gamma_check(xb, 1.0, 0.25, 4000, random.Random(9))
        self.assertGreater(pa, 0.05)
        self.assertLess(pb, 0.01)
        self.assertGreater(dispersion(xb), 5)
        # the sample mean is sufficient for lambda, so its p-value is near 1/2 for both
        for xs in (xa, xb):
            pm = poisson_gamma_check(xs, 1.0, 0.25, 4000, random.Random(9), mean_stat)
            self.assertLess(abs(pm - 0.5), 0.05)


if __name__ == "__main__":
    unittest.main()
