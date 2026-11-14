# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/empirical-bayes/. The authors are listed in prov/NGX20X.jsonl.
"""Tests for empirical Bayes: Robbins and Tweedie against exact Bayes rules, gamma-Poisson
and normal type II maximum likelihood, and the undercoverage of plug-in intervals."""

import math
import random
import unittest
from fractions import Fraction as F
from statistics import NormalDist

from empirical_bayes import (
    _normal_marginal_loglik,
    discrete_prior_posterior_mean,
    gamma_poisson_fit,
    gamma_poisson_posterior_mean,
    normal_eb,
    poisson_mixture_marginal,
    poisson_mixture_posterior_mean,
    robbins,
    tweedie_posterior_mean,
)

CLAIMS = [7840, 1317, 239, 42, 14, 4, 4, 1]
SCHOOLS_Y = [28, 8, -3, 7, -1, 1, 18, 12]
SCHOOLS_S = [15, 10, 16, 11, 9, 11, 10, 18]


def poisson(rng, lam):
    """Knuth's multiplication method; fine for small lam."""
    limit, k, p = math.exp(-lam), 0, rng.random()
    while p > limit:
        k += 1
        p *= rng.random()
    return k


class Robbins(unittest.TestCase):
    def test_exact_on_true_marginal(self):
        # w_k = g_k exp(-theta_k) are arbitrary positive rationals: Robbins's formula is
        # an identity, so it holds for every such choice.
        atoms = [F(1, 3), F(1), F(5, 2), F(4)]
        weights = [F(2, 7), F(1, 5), F(3, 11), F(1, 13)]
        counts = [poisson_mixture_marginal(x, atoms, weights) / math.factorial(x) for x in range(9)]
        for x, est in enumerate(robbins(counts)):
            self.assertEqual(est, poisson_mixture_posterior_mean(x, atoms, weights))

    def test_claims_table(self):
        got = robbins(CLAIMS)
        for est, want in zip(got, [0.168, 0.363, 0.527, 1.333, 1.429, 6.0, 1.75]):
            self.assertAlmostEqual(est, want, places=3)

    def test_zero_count(self):
        self.assertIsNone(robbins([3, 0, 1])[1])

    def test_simulated_gamma_prior(self):
        rng = random.Random(4)
        nu, scale = 2.0, 0.5
        counts = [0] * 30
        for _ in range(60000):
            counts[poisson(rng, rng.gammavariate(nu, scale))] += 1
        est = robbins(counts)
        for x in range(3):
            # delta method: the relative error of a ratio of counts is about
            # sqrt(1/c[x] + 1/c[x + 1]); allow four of these
            sd = est[x] * math.sqrt(1 / counts[x] + 1 / counts[x + 1])
            self.assertLess(abs(est[x] - gamma_poisson_posterior_mean(x, nu, scale)), 4 * sd)


class GammaPoisson(unittest.TestCase):
    def test_claims_fit_matches_book_column(self):
        nu, scale = gamma_poisson_fit(CLAIMS)
        book = [0.164, 0.398, 0.633, 0.87, 1.10, 1.34, 1.57]
        for x, want in enumerate(book):
            self.assertLess(abs(gamma_poisson_posterior_mean(x, nu, scale) - want), 0.006)

    def test_mean_is_matched(self):
        nu, scale = gamma_poisson_fit(CLAIMS)
        mean = sum(x * c for x, c in enumerate(CLAIMS)) / sum(CLAIMS)
        self.assertAlmostEqual(nu * scale, mean, places=12)


class Tweedie(unittest.TestCase):
    def test_against_direct_posterior_mean(self):
        atoms = [-2.0, 0.0, 3.0]
        weights = [0.2, 0.5, 0.3]
        for z in (-3.0, -1.0, 0.0, 0.5, 2.0, 4.0):
            for s2 in (1.0, 0.25):
                a = tweedie_posterior_mean(z, atoms, weights, s2)
                b = discrete_prior_posterior_mean(z, atoms, weights, s2)
                self.assertLess(abs(a - b), 1e-12)

    def test_normal_prior_limit(self):
        # many atoms on a fine grid approximate N(0, 1): E[mu | z] -> z/2
        atoms = [i / 50.0 for i in range(-400, 401)]
        weights = [math.exp(-a * a / 2) for a in atoms]
        for z in (-2.0, 0.7, 3.0):
            self.assertAlmostEqual(tweedie_posterior_mean(z, atoms, weights), z / 2, places=6)


class NormalEB(unittest.TestCase):
    def test_eight_schools_tau_zero(self):
        r = normal_eb(SCHOOLS_Y, [s * s for s in SCHOOLS_S])
        self.assertEqual(r["tau2"], 0.0)
        w = [1 / (s * s) for s in SCHOOLS_S]
        pooled = sum(a * b for a, b in zip(w, SCHOOLS_Y)) / sum(w)
        self.assertAlmostEqual(r["mu"], pooled, places=10)
        self.assertAlmostEqual(pooled, 7.6856, places=4)
        for m in r["post_mean"]:
            self.assertAlmostEqual(m, pooled, places=10)

    def test_equal_variances_closed_form_is_the_maximum(self):
        x = [1.83, -0.95, -0.51, 0.57, 0.29, -4.6, 0.78, -1.14, -1.82, -0.58]
        r = normal_eb(x, [1.0] * 10)
        best = r["loglik"]
        for mu in (r["mu"] - 0.1, r["mu"], r["mu"] + 0.1):
            for t2 in (0.0, 0.5, r["tau2"] * 0.95, r["tau2"] * 1.05, 3.0):
                self.assertLessEqual(_normal_marginal_loglik(x, [1.0] * 10, mu, t2), best + 1e-12)
        self.assertAlmostEqual(r["tau2"], 1.787961, places=6)
        self.assertAlmostEqual(r["shrink"][0], 1 / (1 + 1.787961), places=6)

    def test_unequal_variances_search_is_a_maximum(self):
        x = [2.0, -1.0, 4.0, 0.5, 6.0, -3.0]
        s2 = [1.0, 2.0, 0.5, 1.5, 3.0, 1.0]
        r = normal_eb(x, s2)
        self.assertGreater(r["tau2"], 0.0)
        for t2 in (r["tau2"] * 0.98, r["tau2"] * 1.02):
            w = [1 / (v + t2) for v in s2]
            mu = sum(a * b for a, b in zip(w, x)) / sum(w)
            self.assertLess(_normal_marginal_loglik(x, s2, mu, t2), r["loglik"])

    def test_plug_in_intervals_undercover(self):
        z = NormalDist().inv_cdf(0.975)
        rng = random.Random(108)
        cover = total = 0
        for _ in range(1000):
            theta = [rng.gauss(0.0, math.sqrt(0.5)) for _ in range(8)]
            x = [t + rng.gauss(0.0, 1.0) for t in theta]
            r = normal_eb(x, [1.0] * 8)
            for t, m, v in zip(theta, r["post_mean"], r["post_var"]):
                total += 1
                cover += abs(t - m) <= z * math.sqrt(v)
        self.assertLess(cover / total, 0.8)


if __name__ == "__main__":
    unittest.main()
