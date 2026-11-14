# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/abc-sequential-monte-carlo/. The authors are listed in prov/HY1FY8.jsonl.
"""Tests for ABC-SMC: the weight identity in exact arithmetic, and the final population
against the exact beta posterior of a binomial model."""

import math
import random
import unittest
from fractions import Fraction as F

from abc_sequential_monte_carlo import abc_smc, smc_weight, weighted_variance


def beta_cdf_int(t, a, b):
    m = a + b - 1
    return math.fsum(math.comb(m, j) * t**j * (1 - t) ** (m - j) for j in range(a, m + 1))


class TestWeightIdentity(unittest.TestCase):
    def test_weights_correct_any_previous_population_exactly(self):
        # Finite parameter set {0..k-1}. Accepted proposals have law q ~ g * a, with
        # g = sum_j W_j K(. | theta_j). Weighting by pi / g must give the eps-posterior
        # pi * a / (sum pi a) exactly, whatever the previous population is.
        rng = random.Random(1)
        for _ in range(500):
            k = rng.randint(1, 6)
            prior = [F(rng.randint(1, 5)) for _ in range(k)]
            prior = [p / sum(prior) for p in prior]
            a = [F(rng.randint(0, 6), 6) for _ in range(k)]
            if sum(p * x for p, x in zip(prior, a)) == 0:
                continue
            rows = [[F(rng.randint(1, 4)) for _ in range(k)] for _ in range(k)]
            kern = [[v / sum(r) for v in r] for r in rows]  # kern[old][new], all positive

            def kernel_pdf(new, old):
                return kern[old][new]

            m = rng.randint(1, 5)
            prev = [rng.randrange(k) for _ in range(m)]
            pw = [F(rng.randint(1, 5)) for _ in range(m)]
            pw = [w / sum(pw) for w in pw]
            g = [sum(w * kernel_pdf(t, p) for p, w in zip(prev, pw)) for t in range(k)]
            q = [g[t] * a[t] for t in range(k)]
            w = [smc_weight(t, lambda u: prior[u], prev, pw, kernel_pdf) for t in range(k)]
            h = [F(rng.randint(-5, 5)) for _ in range(k)]
            lhs = sum(q[t] * w[t] * h[t] for t in range(k)) / sum(q[t] * w[t] for t in range(k))
            rhs = sum(prior[t] * a[t] * h[t] for t in range(k)) / sum(prior[t] * a[t] for t in range(k))
            self.assertEqual(lhs, rhs)

    def test_weighted_variance(self):
        self.assertAlmostEqual(weighted_variance([0.0, 1.0], [0.5, 0.5]), 0.25)


def binomial(n):
    def prior_draw(rng):
        return rng.random()

    def prior_pdf(t):
        return 1.0 if 0.0 < t < 1.0 else 0.0

    def simulate(p, rng):
        return sum(1 for _ in range(n) if rng.random() < p)

    return prior_draw, prior_pdf, simulate


def wstats(res):
    xs, ws = res["particles"], res["weights"]
    m = math.fsum(w * x for x, w in zip(xs, ws))
    return m, weighted_variance(xs, ws)


class TestBinomial(unittest.TestCase):
    def setUp(self):
        # 6 successes in 20 trials, uniform prior: the posterior is Beta(7, 15).
        self.n, self.x = 20, 6
        self.mean, self.var = 7 / 22, 7 * 15 / (22**2 * 23)

    def test_final_population_matches_the_exact_posterior(self):
        pd, pp, sim = binomial(self.n)
        res = abc_smc(pd, pp, sim, lambda y: y, self.x, lambda u, v: abs(u - v), (6, 3, 1, 0), 500, random.Random(2))
        m, v = wstats(res)
        ess = res["ess"]
        self.assertGreater(ess, 400)
        self.assertLess(abs(m - self.mean), 4 * math.sqrt(self.var / ess))
        self.assertLess(abs(v / self.var - 1), 0.2)
        order = sorted(zip(res["particles"], res["weights"]))
        cdf, d = 0.0, 0.0
        for t, w in order:
            f = beta_cdf_int(t, 7, 15)
            d = max(d, abs(cdf - f), abs(cdf + w - f))
            cdf += w
        self.assertLess(d, 2.5 / math.sqrt(ess))
        # Fewer simulations than rejection ABC with eps = 0 (21 per kept value).
        self.assertLess(sum(res["sims"]), 500 * 21)

    def test_dropping_the_weights_gives_too_narrow_an_answer(self):
        pd, pp, sim = binomial(self.n)
        res = abc_smc(pd, pp, sim, lambda y: y, self.x, lambda u, v: abs(u - v), (6, 3, 1, 0), 500, random.Random(3), equal_weights=True)
        _, v = wstats(res)
        self.assertLess(v / self.var, 0.88)


if __name__ == "__main__":
    unittest.main()
