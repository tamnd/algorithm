# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bridge-sampling/. The authors are listed in prov/TC3WDX.jsonl.
"""Tests for bridge sampling: the exact identity, the iteration, and log Z of conjugate models."""

import math
import random
import statistics
import unittest
from fractions import Fraction as F

from bridge_sampling import (
    bisection_bridge,
    bridge_from_densities,
    estimating_function,
    general_bridge,
    harmonic_mean,
    importance_sampling,
    optimal_bridge,
)


def lbeta(a, b):
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


class TestIdentityExact(unittest.TestCase):
    def test_bridge_identity_on_finite_sets(self):
        # p_k = q_k / c_k on a finite set; expectations are exact sums in Fractions.
        rng = random.Random(10)
        for _ in range(500):
            m = rng.randint(1, 6)
            q1 = [F(rng.randint(0, 9)) for _ in range(m)]
            q2 = [F(rng.randint(0, 9)) for _ in range(m)]
            alpha = [F(rng.randint(1, 9), rng.randint(1, 9)) for _ in range(m)]
            if sum(q1) == 0 or sum(q2) == 0:
                continue
            c1, c2 = sum(q1), sum(q2)
            overlap = sum(a * u * v for a, u, v in zip(alpha, q1, q2))
            if overlap == 0:
                continue
            e2 = sum(u * a * v / c2 for u, a, v in zip(q1, alpha, q2))  # E_2[q1 alpha]
            e1 = sum(v * a * u / c1 for u, a, v in zip(q1, alpha, q2))  # E_1[q2 alpha]
            self.assertEqual(e2 / e1, c1 / c2)

    def test_importance_sampling_is_the_bridge_with_alpha_one_over_q2(self):
        rng = random.Random(11)
        for _ in range(200):
            n1, n2 = rng.randint(1, 6), rng.randint(1, 6)
            a1 = [rng.uniform(-5, 5) for _ in range(n1)]
            b1 = [rng.uniform(-5, 5) for _ in range(n1)]
            a2 = [rng.uniform(-5, 5) for _ in range(n2)]
            b2 = [rng.uniform(-5, 5) for _ in range(n2)]
            g = general_bridge(a1, b1, a2, b2, lambda a, b: -b)
            self.assertAlmostEqual(g, importance_sampling(a2, b2), places=12)

    def test_harmonic_mean_is_the_bridge_with_prior_and_alpha_one_over_q1(self):
        rng = random.Random(12)
        for _ in range(200):
            n1, n2 = rng.randint(1, 6), rng.randint(1, 6)
            loglik1 = [rng.uniform(-5, 0) for _ in range(n1)]
            logprior1 = [rng.uniform(-3, 0) for _ in range(n1)]
            loglik2 = [rng.uniform(-5, 0) for _ in range(n2)]
            logprior2 = [rng.uniform(-3, 0) for _ in range(n2)]
            # q1 = lik * prior, q2 = prior. With alpha = 1/q1 the numerator is the mean of 1
            # over the prior draws, so only the posterior draws matter.
            a1 = [u + v for u, v in zip(loglik1, logprior1)]
            a2 = [u + v for u, v in zip(loglik2, logprior2)]
            g = general_bridge(a1, logprior1, a2, logprior2, lambda a, b: -a)
            self.assertAlmostEqual(g, harmonic_mean(loglik1), places=12)


class TestIteration(unittest.TestCase):
    def test_estimating_function_is_increasing_with_the_right_limits(self):
        rng = random.Random(20)
        l1 = [rng.uniform(-3, 3) for _ in range(5)]
        l2 = [rng.uniform(-3, 3) for _ in range(7)]
        s1, s2 = 5 / 12, 7 / 12
        vals = [estimating_function(u / 4, l1, l2) for u in range(-60, 61)]
        self.assertTrue(all(vals[i] < vals[i + 1] for i in range(len(vals) - 1)))
        self.assertAlmostEqual(estimating_function(-60, l1, l2), -1 / s1, places=6)
        self.assertAlmostEqual(estimating_function(60, l1, l2), 1 / s2, places=6)

    def test_iteration_equals_the_bisection_root(self):
        rng = random.Random(21)
        for _ in range(500):
            n1, n2 = rng.randint(1, 8), rng.randint(1, 8)
            shift = rng.uniform(-50, 50)
            l1 = [shift + rng.gauss(0, 2) for _ in range(n1)]
            l2 = [shift + rng.gauss(0, 2) for _ in range(n2)]
            start = rng.uniform(-100, 100)
            got, its = optimal_bridge(l1, l2, log_r0=start)
            self.assertLess(its, 10000)
            self.assertAlmostEqual(got, bisection_bridge(l1, l2), places=8)

    def test_constant_ratio_gives_the_exact_answer(self):
        # If q1 / q2 = c everywhere, every bridge returns c in one step.
        got, _ = optimal_bridge([2.5] * 4, [2.5] * 9)
        self.assertAlmostEqual(got, 2.5, places=12)


class TestConjugateModels(unittest.TestCase):
    def test_beta_binomial_trace_of_the_page(self):
        # 3 successes in 10 trials, prior Beta(2, 2), logit scale; proposal = the Laplace normal.
        m, s = -0.587787, 0.557773
        exact = lbeta(5, 9) - lbeta(2, 2)

        def lq1(t):
            return -5 * math.log1p(math.exp(-t)) - 9 * math.log1p(math.exp(t)) - lbeta(2, 2)

        def lq2(t):
            return -0.5 * math.log(2 * math.pi * s * s) - 0.5 * (t - m) ** 2 / (s * s)

        rng = random.Random(5)
        th = []
        for _ in range(8):
            p = rng.betavariate(5, 9)
            th.append(math.log(p / (1 - p)))
        ph = [rng.gauss(m, s) for _ in range(8)]
        got, its = optimal_bridge([lq1(t) - lq2(t) for t in th], [lq1(t) - lq2(t) for t in ph])
        self.assertAlmostEqual(got, -7.024985, places=5)
        self.assertLessEqual(its, 8)
        self.assertAlmostEqual(bridge_from_densities(lq1, lq2, th, ph), got, places=12)
        self.assertAlmostEqual(exact, -6.977748, places=6)

        # 1000 + 1000 draws, 40 repetitions: every optimal bridge estimate within 0.02 nats.
        errs = []
        for _ in range(40):
            th = []
            for _ in range(1000):
                p = rng.betavariate(5, 9)
                th.append(math.log(p / (1 - p)))
            ph = [rng.gauss(m, s) for _ in range(1000)]
            got, _ = optimal_bridge([lq1(t) - lq2(t) for t in th], [lq1(t) - lq2(t) for t in ph])
            errs.append(got - exact)
        self.assertLess(max(abs(e) for e in errs), 0.02)
        self.assertLess(abs(statistics.mean(errs)), 0.003)

    def test_normal_normal_bridge_beats_harmonic_mean(self):
        # x_i ~ N(theta, 1), theta ~ N(0, 10^2), n = 20: n tau^2 >= sigma^2, so the
        # harmonic mean has infinite variance. Exact log Z is in closed form.
        rng = random.Random(1)
        n, tau = 20, 10.0
        xs = [round(rng.gauss(1.0, 1.0), 2) for _ in range(n)]
        xb = sum(xs) / n
        s2 = sum((x - xb) ** 2 for x in xs)
        v = 1 / (n + 1 / tau**2)
        m = v * sum(xs)
        exact = (-0.5 * n * math.log(2 * math.pi) - 0.5 * s2 - 0.5 * math.log(1 + n * tau**2)
                 - 0.5 * n * xb**2 / (1 + n * tau**2))
        self.assertAlmostEqual(exact, -31.327583, places=5)

        def llik(t):
            return -0.5 * n * math.log(2 * math.pi) - 0.5 * (s2 + n * (t - xb) ** 2)

        def lprior(t):
            return -0.5 * math.log(2 * math.pi * tau**2) - 0.5 * t * t / tau**2

        sd2 = math.sqrt(2 * v)

        def lq2(t):
            return -0.5 * math.log(2 * math.pi * sd2 * sd2) - 0.5 * (t - m) ** 2 / sd2**2

        hm_errs, br_errs = [], []
        for _ in range(20):
            th = [rng.gauss(m, math.sqrt(v)) for _ in range(2000)]
            ph = [rng.gauss(m, sd2) for _ in range(2000)]
            hm_errs.append(harmonic_mean([llik(t) for t in th]) - exact)
            br = optimal_bridge([llik(t) + lprior(t) - lq2(t) for t in th], [llik(t) + lprior(t) - lq2(t) for t in ph])[0]
            br_errs.append(br - exact)
        self.assertLess(max(abs(e) for e in br_errs), 0.03)
        # The harmonic mean overestimates Z by more than one nat in every run.
        self.assertGreater(min(hm_errs), 1.0)


if __name__ == "__main__":
    unittest.main()
