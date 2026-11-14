# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simulation-based-calibration/. The authors are listed in prov/GB2WNE.jsonl.
"""Tests for simulation-based calibration: the exact law of the rank in a discrete model
(uniform with random tie breaking, not uniform without it), uniform ranks for a correct
sampler, the characteristic shapes for wrong ones, and thinning of a Markov chain."""

import itertools
import math
import random
import unittest
from fractions import Fraction as F

from simulation_based_calibration import (
    ar1_sampler,
    bin_counts,
    chi2_sf,
    chi2_uniformity,
    gaussian_sampler,
    normal_model,
    sbc,
)


def exact_rank_law(prior, like, post_of, n_draws, randomize=True):
    """The exact law of the rank of theta~ among n_draws draws from post_of(y), for a model
    with finitely many parameter values and data values. prior[t] and like[t][y] are Fractions."""
    k = len(prior)
    ys = range(len(like[0]))
    law = [F(0)] * (n_draws + 1)
    for y in ys:
        q = post_of(y)
        for t in range(k):
            joint = prior[t] * like[t][y]
            if joint == 0:
                continue
            for draws in itertools.product(range(k), repeat=n_draws):
                pd = math.prod((q[d] for d in draws), start=F(1))
                below = sum(1 for d in draws if d < t)
                ties = sum(1 for d in draws if d == t)
                if randomize:
                    for r in range(below, below + ties + 1):
                        law[r] += joint * pd / (ties + 1)
                else:
                    law[below] += joint * pd
    return law


class TestExactRankLaw(unittest.TestCase):
    def test_uniform_with_random_ties_and_also_for_the_prior(self):
        rng = random.Random(1)
        for _ in range(500):
            k = rng.randint(2, 4)
            m = rng.randint(1, 3)
            raw = [rng.randint(1, 9) for _ in range(k)]
            prior = [F(v, sum(raw)) for v in raw]
            ps = sorted(rng.sample([F(1, 5), F(2, 5), F(3, 5), F(4, 5), F(1, 2)], k))
            like = [[math.comb(m, y) * p**y * (1 - p) ** (m - y) for y in range(m + 1)] for p in ps]

            def post_of(y):
                joint = [prior[t] * like[t][y] for t in range(k)]
                s = sum(joint)
                return [j / s for j in joint]

            n_draws = rng.randint(1, 3)
            law = exact_rank_law(prior, like, post_of, n_draws)
            self.assertEqual(law, [F(1, n_draws + 1)] * (n_draws + 1))
            # without random tie breaking, rank 0 is too likely
            plain = exact_rank_law(prior, like, post_of, n_draws, randomize=False)
            self.assertEqual(sum(plain), 1)
            self.assertGreater(plain[0], F(1, n_draws + 1))
            # a sampler that ignores the data and returns the prior also passes
            law_prior = exact_rank_law(prior, like, lambda y: prior, n_draws)
            self.assertEqual(law_prior, [F(1, n_draws + 1)] * (n_draws + 1))


class TestNormalModel(unittest.TestCase):
    L = 20

    def run_sbc(self, sampler):
        prior_draw, simulate, _ = normal_model(5)
        return sbc(prior_draw, simulate, sampler, lambda t: t, 1000, self.L, random.Random(7))

    def test_correct_sampler_gives_uniform_ranks(self):
        _, _, post = normal_model(5)
        c = self.run_sbc(gaussian_sampler(post))
        self.assertEqual(sum(c), 1000)
        self.assertGreater(chi2_uniformity(c)[1], 0.01)
        self.assertGreater(chi2_uniformity(bin_counts(c, 7))[1], 0.01)

    def test_wrong_samplers_give_their_shapes(self):
        _, _, post = normal_model(5)
        expected_ends = 2 * 1000 / (self.L + 1)
        narrow = self.run_sbc(gaussian_sampler(post, scale=0.6))
        self.assertLess(chi2_uniformity(narrow)[1], 1e-10)
        self.assertGreater(narrow[0] + narrow[-1], 2 * expected_ends)  # U shape
        wide = self.run_sbc(gaussian_sampler(post, scale=1.5))
        self.assertLess(chi2_uniformity(wide)[1], 1e-10)
        self.assertLess(wide[0] + wide[-1], expected_ends / 2)  # hump
        shifted = self.run_sbc(gaussian_sampler(post, shift=0.5))
        self.assertLess(chi2_uniformity(shifted)[1], 1e-10)
        mean_rank = sum(r * c for r, c in enumerate(shifted)) / 1000
        self.assertLess(mean_rank, self.L / 2 - 2)  # draws too high, so the truth ranks low

    def test_prior_sampler_is_not_detected(self):
        c = self.run_sbc(lambda y, n, rng: [rng.gauss(0.0, 1.0) for _ in range(n)])
        self.assertGreater(chi2_uniformity(c)[1], 0.01)

    def test_autocorrelated_chain_fails_and_thinning_fixes_it(self):
        _, _, post = normal_model(5)
        raw = self.run_sbc(ar1_sampler(post, 0.9))
        self.assertLess(chi2_uniformity(raw)[1], 1e-10)
        self.assertGreater(raw[0] + raw[-1], 3 * 2 * 1000 / (self.L + 1))
        # effective sample size of an AR(1) chain: n (1 - rho) / (1 + rho), so thin by 19
        thinned = self.run_sbc(ar1_sampler(post, 0.9, 19))
        self.assertGreater(chi2_uniformity(thinned)[1], 0.01)


class TestChiSquared(unittest.TestCase):
    def test_closed_forms(self):
        # upper 5 percent points from standard tables
        for x, k in ((3.841, 1), (5.991, 2), (7.815, 3), (30.144, 19), (31.410, 20)):
            self.assertAlmostEqual(chi2_sf(x, k), 0.05, places=3)
        for x in (0.1, 1.0, 4.0, 20.0):
            self.assertAlmostEqual(chi2_sf(x, 1), math.erfc(math.sqrt(x / 2)), places=12)
            self.assertAlmostEqual(chi2_sf(x, 2), math.exp(-x / 2), places=12)
            # P(chi2_{k+2} >= x) = P(chi2_k >= x) + (x/2)^(k/2) e^(-x/2) / Gamma(k/2 + 1)
            for k in range(1, 12):
                h = x / 2
                self.assertAlmostEqual(chi2_sf(x, k + 2), chi2_sf(x, k) + h ** (k / 2) * math.exp(-h) / math.gamma(k / 2 + 1), places=12)


if __name__ == "__main__":
    unittest.main()
