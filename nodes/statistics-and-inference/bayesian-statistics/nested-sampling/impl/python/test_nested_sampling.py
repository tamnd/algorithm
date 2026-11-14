# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nested-sampling/. The authors are listed in prov/G4YCZZ.jsonl.
"""Tests for nested sampling: the layer-cake identity, the shrinkage law, and log Z of conjugate models.

All constrained draws are exact: the set {L > L*} is an interval in these models, so a
draw from the prior restricted to it comes from the inverse CDF.
"""

import math
import random
import statistics
import unittest
from fractions import Fraction as F

from nested_sampling import layer_cake, nested_sampling, posterior_mean

ND = statistics.NormalDist()


def normal_model(xs, sigma, tau):
    """x_j ~ N(theta, sigma^2), theta ~ N(0, tau^2). Returns the model and exact log Z, H, mean."""
    n = len(xs)
    xb = sum(xs) / n
    s2 = sum((x - xb) ** 2 for x in xs)
    c = -0.5 * n * math.log(2 * math.pi * sigma**2) - 0.5 * s2 / sigma**2

    def log_lik(t):
        return c - 0.5 * n * (t - xb) ** 2 / sigma**2

    def prior_draw(rng):
        return rng.gauss(0.0, tau)

    def constrained_draw(rng, log_l_star):
        r = math.sqrt(max((c - log_l_star) * 2 * sigma**2 / n, 0.0))
        lo, hi = ND.cdf((xb - r) / tau), ND.cdf((xb + r) / tau)
        u = lo + (hi - lo) * rng.random()
        return tau * ND.inv_cdf(min(max(u, 1e-300), 1 - 1e-16))

    v = 1 / (n / sigma**2 + 1 / tau**2)
    m = v * n * xb / sigma**2
    log_z = c + 0.5 * math.log(v / tau**2) - 0.5 * xb**2 / (tau**2 + sigma**2 / n)
    h = 0.5 * math.log(tau**2 / v) - 0.5 + 0.5 * (v + m * m) / tau**2
    return log_lik, prior_draw, constrained_draw, log_z, h, m


def binomial_model(n, x):
    """x successes in n trials, uniform prior on p. Exact Z = 1/(n+1)."""
    log_c = math.lgamma(n + 1) - math.lgamma(x + 1) - math.lgamma(n - x + 1)
    mode = x / n

    def log_lik(p):
        if p <= 0.0 or p >= 1.0:
            return -math.inf
        return log_c + x * math.log(p) + (n - x) * math.log1p(-p)

    def prior_draw(rng):
        return rng.random()

    def edge(lo, hi, log_l_star, rising):
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if (log_lik(mid) > log_l_star) == rising:
                hi = mid
            else:
                lo = mid
        return 0.5 * (lo + hi)

    def constrained_draw(rng, log_l_star):
        a = edge(0.0, mode, log_l_star, True)
        b = edge(mode, 1.0, log_l_star, False)
        return a + (b - a) * rng.random()

    return log_lik, prior_draw, constrained_draw, -math.log(n + 1)


class TestIdentities(unittest.TestCase):
    def test_layer_cake_is_exact_on_discrete_priors(self):
        rng = random.Random(1)
        for _ in range(500):
            m = rng.randint(1, 8)
            vals = [F(rng.randint(0, 6), rng.randint(1, 4)) for _ in range(m)]  # ties happen
            w = [rng.randint(1, 9) for _ in range(m)]
            probs = [F(k, sum(w)) for k in w]
            self.assertEqual(layer_cake(vals, probs), sum(p * v for p, v in zip(probs, vals)))

    def test_shrinkage_law_beta_n_1(self):
        # L(theta) = theta on a uniform prior, so X(lambda) = 1 - lambda exactly and the
        # true prior mass X_i above the i-th dead point is known. Theory: log X_i is a sum of
        # i iid log t, t ~ Beta(N, 1): mean -i/N, variance i/N^2; E t = N/(N+1).
        rng = random.Random(2)
        n_live, steps, reps = 10, 30, 2000
        logs, ratios = [], []
        for _ in range(reps):
            res = nested_sampling(
                math.log,
                lambda r: 1.0 - r.random(),
                lambda r, ls: 1.0 - (1.0 - math.exp(ls)) * r.random(),
                n_live, rng, max_iter=steps,
            )
            xs = [1.0 - th for th, _, _ in res["dead"][:steps]]
            logs.append(math.log(xs[-1]))
            ratios.append(xs[1] / xs[0])
        se = math.sqrt(steps / n_live**2 / reps)
        self.assertLess(abs(statistics.mean(logs) + steps / n_live), 4 * se)
        self.assertLess(abs(statistics.variance(logs) / (steps / n_live**2) - 1), 0.12)
        self.assertLess(abs(statistics.mean(ratios) - n_live / (n_live + 1)), 4 * math.sqrt(0.0069 / reps))


class TestConjugateModels(unittest.TestCase):
    def test_normal_normal_log_z_and_error_bar(self):
        rng = random.Random(1)
        xs = [round(rng.gauss(1.0, 1.0), 2) for _ in range(20)]
        log_lik, prior_draw, cdraw, exact, h, m = normal_model(xs, 1.0, 10.0)
        self.assertAlmostEqual(exact, -31.327583, places=5)
        self.assertAlmostEqual(h, 3.306072, places=5)
        n_live, reps = 100, 60
        errs, hs, inside = [], [], 0
        for _ in range(reps):
            res = nested_sampling(log_lik, prior_draw, cdraw, n_live, rng, eps=1e-6)
            e = res["log_z"] - exact
            errs.append(e)
            hs.append(res["h"])
            inside += abs(e) <= 2 * res["error"]
            self.assertLess(abs(posterior_mean(res, lambda t: t) - m), 0.05)
        self.assertLess(abs(statistics.mean(hs) - h), 0.1)
        sd = statistics.stdev(errs)
        self.assertLess(abs(statistics.mean(errs)), 4 * sd / math.sqrt(reps))
        self.assertTrue(0.7 < sd / math.sqrt(h / n_live) < 1.4)
        self.assertGreaterEqual(inside, int(0.85 * reps))

    def test_beta_binomial_uniform_prior(self):
        rng = random.Random(3)
        log_lik, prior_draw, cdraw, exact = binomial_model(10, 3)
        errs = []
        for _ in range(20):
            res = nested_sampling(log_lik, prior_draw, cdraw, 50, rng, eps=1e-6)
            errs.append(res["log_z"] - exact)
            self.assertLess(abs(res["log_z"] - exact), 4 * res["error"])
            self.assertLess(abs(posterior_mean(res, lambda p: p) - 4 / 12), 0.03)
        self.assertLess(abs(statistics.mean(errs)), 0.1)


if __name__ == "__main__":
    unittest.main()
