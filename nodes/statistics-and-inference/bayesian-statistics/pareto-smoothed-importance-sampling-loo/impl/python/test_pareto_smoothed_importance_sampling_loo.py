# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pareto-smoothed-importance-sampling-loo/. The authors are listed in prov/NR2Y7A.jsonl.
"""Tests for PSIS-LOO: exact identities, a conjugate normal model with exact LOO, and the GPD fit."""

import math
import random
import unittest
from fractions import Fraction as F

from pareto_smoothed_importance_sampling_loo import (
    gpd_fit,
    gpd_quantile,
    is_loo_raw,
    khat_threshold,
    psis_loo,
    psis_smooth,
    tail_length,
    waic,
)

LOG2PI = math.log(2.0 * math.pi)


def lnorm(x, m, v):
    return -0.5 * (LOG2PI + math.log(v) + (x - m) ** 2 / v)


def posterior(ys, sig2=1.0, mu0=0.0, t02=100.0):
    prec = 1.0 / t02 + len(ys) / sig2
    return (mu0 / t02 + sum(ys) / sig2) / prec, 1.0 / prec


def exact_loo(ys, sig2=1.0):
    out = []
    for i in range(len(ys)):
        m, v = posterior(ys[:i] + ys[i + 1:], sig2)
        out.append(lnorm(ys[i], m, v + sig2))
    return out


def exact_waic(ys, sig2=1.0):
    m, v = posterior(ys, sig2)
    lppd = sum(lnorm(y, m, v + sig2) for y in ys)
    p = sum((2 * v * v + 4 * (y - m) ** 2 * v) / (4 * sig2 * sig2) for y in ys)
    return lppd, p, lppd - p


def draws_matrix(ys, s, seed, sig2=1.0):
    rng = random.Random(seed)
    m, v = posterior(ys, sig2)
    th = [rng.gauss(m, math.sqrt(v)) for _ in range(s)]
    return [[lnorm(y, t, sig2) for t in th] for y in ys]


def outlier_data(last):
    rng = random.Random(7)
    base = [round(rng.gauss(0.0, 1.0), 2) for _ in range(19)]
    return base + [last]


class HarmonicIdentity(unittest.TestCase):
    """p(y_i | y_-i) = 1 / E_post[1 / p(y_i | theta)], checked exactly on a discrete model."""

    def setUp(self):
        self.thetas = [F(1, 4), F(1, 2), F(3, 4)]
        self.post = [F(1, 4), F(1, 2), F(1, 4)]
        self.ys = [1, 0, 1]

        def lik(t, y):
            return t if y == 1 else 1 - t

        self.lik = lik
        full = [math.prod(lik(t, y) for y in self.ys) for t in self.thetas]
        prior = [p / L for p, L in zip(self.post, full)]
        total = sum(prior)
        self.prior = [p / total for p in prior]

    def exact(self, i):
        rest = self.ys[:i] + self.ys[i + 1:]
        w = [p * math.prod(self.lik(t, y) for y in rest) for p, t in zip(self.prior, self.thetas)]
        return sum(a * self.lik(t, self.ys[i]) for a, t in zip(w, self.thetas)) / sum(w)

    def test_identity_in_fractions(self):
        for i, y in enumerate(self.ys):
            harmonic = 1 / sum(p / self.lik(t, y) for p, t in zip(self.post, self.thetas))
            self.assertEqual(harmonic, self.exact(i))

    def test_raw_is_exact_on_weighted_draws(self):
        draws = [F(1, 4)] + [F(1, 2)] * 2 + [F(3, 4)]
        ll = [[math.log(self.lik(t, y)) for t in draws] for y in self.ys]
        for i, got in enumerate(is_loo_raw(ll)):
            self.assertAlmostEqual(got, math.log(self.exact(i)), places=12)


class Helpers(unittest.TestCase):
    def test_tail_length(self):
        self.assertEqual(tail_length(100), 20)
        self.assertEqual(tail_length(1000), 94)
        self.assertEqual(tail_length(4000), 189)

    def test_threshold(self):
        self.assertAlmostEqual(khat_threshold(100), 0.5)
        self.assertAlmostEqual(khat_threshold(1000), 2.0 / 3.0)
        self.assertEqual(khat_threshold(4000), 0.7)

    def test_gpd_quantile_inverts_cdf(self):
        for k in (0.0, 0.4, -0.3):
            for p in (0.1, 0.5, 0.9):
                x = gpd_quantile(p, k, 2.0)
                cdf = 1 - math.exp(-x / 2.0) if k == 0 else 1 - (1 + k * x / 2.0) ** (-1 / k)
                self.assertAlmostEqual(cdf, p, places=12)

    def test_gpd_fit_recovers_shape(self):
        rng = random.Random(3)
        for k in (0.0, 0.3, 0.5, 0.8):
            xs = []
            for _ in range(2000):
                u = rng.random()
                xs.append(-math.log(u) if k == 0 else (u ** (-k) - 1) / k)
            khat, sigma = gpd_fit(xs)
            self.assertLess(abs(khat - k), 0.1)
            self.assertLess(abs(sigma - 1.0), 0.15)


class Smoothing(unittest.TestCase):
    def test_only_tail_changes_and_cap_holds(self):
        rng = random.Random(5)
        s = 1000
        raw = [rng.gauss(0.0, 1.5) for _ in range(s)]
        lw, k = psis_smooth(raw)
        top = max(raw)
        m = tail_length(s)
        order = sorted(range(s), key=lambda j: raw[j])
        for j in order[: s - m]:
            self.assertEqual(lw[j], raw[j] - top)
        threshold = raw[order[s - m - 1]] - top
        for j in order[s - m:]:
            self.assertGreaterEqual(lw[j], threshold)
            self.assertLessEqual(lw[j], 0.0)
        self.assertTrue(math.isfinite(k))

    def test_short_input_is_not_smoothed(self):
        lw, k = psis_smooth([0.0, 1.0, 2.0])
        self.assertEqual(lw, [-2.0, -1.0, 0.0])
        self.assertEqual(k, math.inf)


class ConjugateNormal(unittest.TestCase):
    """y_i ~ N(theta, 1), theta ~ N(0, 100): leave-one-out has a closed form."""

    def test_five_points(self):
        ys = [0.5, 1.0, 2.0, 2.5, 4.0]
        res = psis_loo(draws_matrix(ys, 4000, 1))
        ex = exact_loo(ys)
        for got, want in zip(res["pointwise"], ex):
            self.assertLess(abs(got - want), 0.06)
        self.assertLess(abs(res["elpd_loo"] - sum(ex)), 0.15)
        self.assertEqual(res["flagged"], [])
        self.assertAlmostEqual(res["looic"], -2 * res["elpd_loo"])

    def test_no_outlier_no_flag(self):
        rng = random.Random(7)
        base = [round(rng.gauss(0.0, 1.0), 2) for _ in range(19)]
        ys = base + [round(rng.gauss(0.0, 1.0), 2)]
        res = psis_loo(draws_matrix(ys, 4000, 11))
        self.assertEqual(res["flagged"], [])
        self.assertLess(abs(res["elpd_loo"] - sum(exact_loo(ys))), 0.05)

    def test_outlier_is_flagged(self):
        ys = outlier_data(9.0)
        res = psis_loo(draws_matrix(ys, 4000, 11))
        self.assertIn(19, res["flagged"])
        self.assertGreater(res["k_hat"][19], 0.7)
        self.assertEqual(max(res["k_hat"][:19]) < 0.7, True)

    def test_waic_against_closed_form(self):
        ys = [0.5, 1.0, 2.0, 2.5, 4.0]
        w = waic(draws_matrix(ys, 4000, 1))
        lppd, p, elpd = exact_waic(ys)
        self.assertLess(abs(w["lppd"] - lppd), 0.01)
        self.assertLess(abs(w["p_waic"] - p), 0.1)
        self.assertLess(abs(w["elpd_waic"] - elpd), 0.1)
        self.assertAlmostEqual(w["waic"], -2 * w["elpd_waic"])

    def test_waic_matches_its_definition(self):
        ll = [[-1.0, -2.0, -3.0], [0.0, 0.0, 0.0]]
        w = waic(ll)
        lppd0 = math.log((math.exp(-1) + math.exp(-2) + math.exp(-3)) / 3)
        self.assertAlmostEqual(w["lppd"], lppd0, places=12)
        self.assertAlmostEqual(w["p_waic"], 1.0, places=12)

    def test_unequal_rows_raise(self):
        with self.assertRaises(ValueError):
            psis_loo([[0.0] * 10, [0.0] * 9])


if __name__ == "__main__":
    unittest.main()
