# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-bayesian-computation/. The authors are listed in prov/5HMWEW.jsonl.
"""Tests for the ABC template: exact Bayes factors of the Poisson and geometric models,
ABC model choice with a summary that is or is not sufficient for the model index, and
the regression adjustment."""

import itertools
import math
import random
import unittest
from fractions import Fraction as F

from approximate_bayesian_computation import (
    abc,
    abc_model_choice,
    evidence_geometric,
    evidence_geometric_sum,
    evidence_poisson,
    evidence_poisson_sum,
    regression_adjust,
    weighted_mean_var,
)


class TestExactBayesFactors(unittest.TestCase):
    def test_page_values(self):
        self.assertEqual(evidence_poisson((0, 0, 3)) / evidence_geometric((0, 0, 3)), F(35, 64))
        self.assertEqual(evidence_poisson((1, 1, 1)) / evidence_geometric((1, 1, 1)), F(105, 32))
        self.assertEqual(evidence_poisson_sum(3, 3) / evidence_geometric_sum(3, 3), F(189, 128))

    def test_sum_evidences_add_up_over_data_sets(self):
        # m(S = s) is the sum of m(x) over all x with sum s.
        for n in range(1, 4):
            for s in range(0, 6):
                xs_all = [x for x in itertools.product(range(s + 1), repeat=n) if sum(x) == s]
                self.assertEqual(sum(evidence_poisson(x) for x in xs_all), evidence_poisson_sum(n, s))
                self.assertEqual(sum(evidence_geometric(x) for x in xs_all), evidence_geometric_sum(n, s))

    def test_true_bayes_factor_is_the_summary_one_times_a_data_factor(self):
        # B(x) = B_S(s) * h_P(x) / h_G(x), with h_P(x) = s! / (n^s prod x_i!) the multinomial
        # probability of x given s, and h_G(x) = 1 / C(n + s - 1, s), uniform on compositions.
        rng = random.Random(1)
        for _ in range(500):
            n = rng.randint(1, 6)
            xs = [rng.randint(0, 5) for _ in range(n)]
            s = sum(xs)
            b = evidence_poisson(xs) / evidence_geometric(xs)
            bs = evidence_poisson_sum(n, s) / evidence_geometric_sum(n, s)
            hp = F(math.factorial(s), n**s * math.prod(math.factorial(v) for v in xs))
            hg = F(1, math.comb(n + s - 1, s))
            self.assertEqual(b, bs * hp / hg)


class TestModelChoice(unittest.TestCase):
    def test_sum_is_not_sufficient_for_the_model_but_the_sorted_data_are(self):
        rng = random.Random(4)
        xs = (0, 0, 3)
        target_s = F(189, 128) / (1 + F(189, 128))  # 0.5962 for any data with S = 3
        target = F(35, 64) / (1 + F(35, 64))  # 0.3535, the true posterior probability
        a, b = abc_model_choice(xs, sum, 100000, rng)
        p = a / (a + b)
        self.assertLess(abs(p - float(target_s)), 4 * math.sqrt(p * (1 - p) / (a + b)))
        c, d = abc_model_choice(xs, lambda y: tuple(sorted(y)), 100000, rng)
        q = c / (c + d)
        self.assertLess(abs(q - float(target)), 4 * math.sqrt(q * (1 - q) / (c + d)))
        self.assertGreater(p - q, 0.15)


class TestRegressionAdjustment(unittest.TestCase):
    def test_exact_linear_relation_is_removed(self):
        rng = random.Random(2)
        for _ in range(500):
            a, b = rng.uniform(-5, 5), rng.uniform(-5, 5)
            s_obs = rng.uniform(-1, 1)
            ss = [s_obs + rng.uniform(-1, 1) for _ in range(rng.randint(2, 20))]
            kept = [(a + b * (s - s_obs), s, 1.0) for s in ss]
            out = regression_adjust(kept, s_obs, 1.0)
            for t, _, _ in out:
                self.assertAlmostEqual(t, a, places=8)

    def test_normal_mean_with_a_large_tolerance(self):
        # x_i ~ N(theta, 1), n = 5, theta ~ N(0, 3^2); exact posterior sd 0.4423.
        rng = random.Random(11)
        xs = [round(rng.gauss(1.0, 1.0), 2) for _ in range(5)]
        n, tau = 5, 3.0
        v = 1 / (n + 1 / tau**2)
        m = v * sum(xs)

        def prior_draw(r):
            return r.gauss(0, tau)

        def simulate(t, r):
            return [r.gauss(t, 1) for _ in range(n)]

        def summary(y):
            return sum(y) / len(y)

        plain = abc(xs, prior_draw, simulate, summary, lambda u, w: abs(u - w), 2.0, 20000, random.Random(30))
        adj = abc(xs, prior_draw, simulate, summary, lambda u, w: abs(u - w), 2.0, 20000, random.Random(30), adjust=True)
        _, vp = weighted_mean_var(plain)
        ma, va = weighted_mean_var(adj)
        self.assertGreater(math.sqrt(vp), 1.0)
        self.assertLess(abs(math.sqrt(va) - math.sqrt(v)), 0.03)
        self.assertLess(abs(ma - m), 0.05)


if __name__ == "__main__":
    unittest.main()
