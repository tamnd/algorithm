# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/abc-rejection-sampling/. The authors are listed in prov/1PE36P.jsonl.
"""Tests for the ABC rejection algorithm.

Discrete models: every random path of one proposal is enumerated with exact Fraction
probabilities, so the law of the kept values is compared exactly with Bayes' rule.
Continuous prior: Kolmogorov-Smirnov distance to the exact beta posterior.
"""

import math
import random
import statistics
import unittest
from fractions import Fraction as F

from abc_rejection_sampling import abc_rejection, abc_step, exact_accept_law


def comb(n, k):
    return math.comb(n, k)


def discrete_model(thetas, weights, den):
    """Prior on thetas (numerators of p = a/den) with integer weights; Bernoulli trials
    drawn by randrange(den) < a, so every path is enumerable."""
    total = sum(weights)

    def prior_draw(rng):
        r = rng.randrange(total)
        for a, w in zip(thetas, weights):
            if r < w:
                return a
            r -= w
        raise AssertionError

    def make_sim(n):
        def simulate(a, rng):
            return tuple(1 if rng.randrange(den) < a else 0 for _ in range(n))
        return simulate

    return prior_draw, make_sim


def normalize(law):
    z = sum(law.values())
    return {k: v / z for k, v in law.items()}, z


def hamming(a, b):
    return sum(u != v for u, v in zip(a, b))


class TestExactLaw(unittest.TestCase):
    def test_tolerance_zero_sufficient_summary_gives_the_posterior(self):
        rng = random.Random(1)
        cases = 0
        while cases < 500:
            den = rng.choice([2, 3, 4])
            k = rng.randint(1, min(3, den - 1))
            thetas = rng.sample(range(1, den), k)
            weights = [rng.randint(1, 3) for _ in thetas]
            n = rng.randint(1, 3)
            x = tuple(rng.randint(0, 1) for _ in range(n))
            s = sum(x)
            prior_draw, make_sim = discrete_model(thetas, weights, den)
            sim = make_sim(n)
            prior = {a: F(w, sum(weights)) for a, w in zip(thetas, weights)}
            lik = {a: F(a, den) ** s * (1 - F(a, den)) ** (n - s) for a in thetas}
            post, _ = normalize({a: prior[a] * lik[a] for a in thetas})

            # S = number of successes (sufficient), eps = 0.
            law = exact_accept_law(lambda r: abc_step(prior_draw, sim, sum, s, lambda u, v: abs(u - v), 0, r))
            got, acc = normalize(law)
            self.assertEqual(got, post)
            self.assertEqual(acc, sum(prior[a] * comb(n, s) * lik[a] for a in thetas))  # m_S(s_obs)

            # S = the whole data set (also sufficient), eps = 0, Hamming distance.
            law = exact_accept_law(lambda r: abc_step(prior_draw, sim, lambda y: y, x, hamming, 0, r))
            got, acc = normalize(law)
            self.assertEqual(got, post)
            self.assertEqual(acc, sum(prior[a] * lik[a] for a in thetas))  # m(x)

            # eps = 1 on the count: the eps-posterior pi(a) P_a(|S - s| <= 1).
            def window(a):
                p = F(a, den)
                return sum(comb(n, j) * p**j * (1 - p) ** (n - j) for j in range(max(0, s - 1), min(n, s + 1) + 1))

            law = exact_accept_law(lambda r: abc_step(prior_draw, sim, sum, s, lambda u, v: abs(u - v), 1, r))
            got, _ = normalize(law)
            self.assertEqual(got, normalize({a: prior[a] * window(a) for a in thetas})[0])

            # Insufficient summary (the first trial only): the posterior given x_1 alone.
            law = exact_accept_law(lambda r: abc_step(prior_draw, sim, lambda y: y[0], x[0], lambda u, v: abs(u - v), 0, r))
            got, _ = normalize(law)
            p1 = {a: F(a, den) if x[0] == 1 else 1 - F(a, den) for a in thetas}
            self.assertEqual(got, normalize({a: prior[a] * p1[a] for a in thetas})[0])
            cases += 1

    def test_insufficient_summary_differs_from_the_posterior(self):
        prior_draw, make_sim = discrete_model([1, 3], [1, 1], 4)
        sim = make_sim(3)
        x = (1, 1, 1)
        full, _ = normalize(exact_accept_law(lambda r: abc_step(prior_draw, sim, sum, 3, lambda u, v: abs(u - v), 0, r)))
        first, _ = normalize(exact_accept_law(lambda r: abc_step(prior_draw, sim, lambda y: y[0], 1, lambda u, v: abs(u - v), 0, r)))
        self.assertEqual(full, {1: F(1, 28), 3: F(27, 28)})
        self.assertEqual(first, {1: F(1, 4), 3: F(3, 4)})


def beta_cdf_int(t, a, b):
    """Beta(a, b) CDF for integer a, b: P(Binomial(a + b - 1, t) >= a)."""
    m = a + b - 1
    return math.fsum(comb(m, j) * t**j * (1 - t) ** (m - j) for j in range(a, m + 1))


def binomial_setup(n):
    def prior_draw(rng):
        return rng.random()

    def simulate(p, rng):
        return sum(1 for _ in range(n) if rng.random() < p)

    return prior_draw, simulate


class TestContinuousPrior(unittest.TestCase):
    def test_kolmogorov_smirnov_against_the_beta_posterior(self):
        # Uniform prior, 3 successes in 10 trials: the posterior is Beta(4, 8).
        rng = random.Random(7)
        prior_draw, simulate = binomial_setup(10)
        n_acc = 2000
        acc, sims = abc_rejection(prior_draw, simulate, lambda y: y, 3, lambda u, v: abs(u - v), 0, n_acc, rng)
        acc.sort()
        d = max(max((i + 1) / n_acc - beta_cdf_int(t, 4, 8), beta_cdf_int(t, 4, 8) - i / n_acc) for i, t in enumerate(acc))
        self.assertLess(d, 1.95 / math.sqrt(n_acc))
        # Acceptance probability m_S(3) = 1/11.
        rate = n_acc / sims
        self.assertLess(abs(rate - 1 / 11), 4 * math.sqrt((1 / 11) * (10 / 11) / sims))

    def test_positive_tolerance_inflates_the_variance(self):
        # eps = 1: pi_eps(p) is proportional to sum_{k=2}^{4} C(10,k) p^k (1-p)^(10-k).
        # Mean 1/3 (as the posterior), variance 0.021368 against 0.017094 for eps = 0.
        exact_var = F(62, 468) - F(1, 9)
        rng = random.Random(8)
        prior_draw, simulate = binomial_setup(10)
        acc, sims = abc_rejection(prior_draw, simulate, lambda y: y, 3, lambda u, v: abs(u - v), 1, 4000, rng)
        self.assertLess(abs(statistics.mean(acc) - 1 / 3), 4 * math.sqrt(float(exact_var) / 4000))
        self.assertLess(abs(statistics.variance(acc) - float(exact_var)), 0.0015)
        self.assertGreater(statistics.variance(acc), 32 / 1872 + 0.002)
        self.assertLess(abs(4000 / sims - 3 / 11), 4 * math.sqrt((3 / 11) * (8 / 11) / sims))

    def test_max_sims_limits_the_work(self):
        rng = random.Random(9)
        prior_draw, simulate = binomial_setup(10)
        acc, sims = abc_rejection(prior_draw, simulate, lambda y: y, 3, lambda u, v: abs(u - v), 0, 10**6, rng, max_sims=500)
        self.assertEqual(sims, 500)
        self.assertLess(len(acc), 500)


if __name__ == "__main__":
    unittest.main()
