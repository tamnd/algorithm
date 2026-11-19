# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/likelihood-ratio-vad/. The authors are listed in prov/4HXQ9X.jsonl.

import itertools
import math
import random
import unittest

from likelihood_ratio_vad import decision_directed, hmm_log_odds, log_lr_bin, vad
from nlsdsp import sine, white_noise

FS = 8000


def tone_in_noise(seed, amp, n=8000):
    rng = random.Random(seed)
    x = white_noise(rng, n, 0.01)
    tone = sine(500, FS, 2400, amp)
    for i in range(2400):
        x[2800 + i] += tone[i]
    return x


class TestBinRatio(unittest.TestCase):
    def test_matches_gaussian_densities(self):
        # p(X | H) = exp(-|X|^2 / v) / (pi v) for a complex Gaussian of variance v.
        rng = random.Random(1)
        for _ in range(200):
            lam = rng.uniform(0.1, 5.0)
            xi = rng.uniform(0.0, 20.0)
            x2 = rng.uniform(0.0, 30.0)
            p0 = math.exp(-x2 / lam) / (math.pi * lam)
            v1 = lam * (1.0 + xi)
            p1 = math.exp(-x2 / v1) / (math.pi * v1)
            self.assertAlmostEqual(log_lr_bin(x2 / lam, xi), math.log(p1 / p0), places=9)

    def test_increasing_in_gamma(self):
        for xi in (0.01, 1.0, 10.0):
            vals = [log_lr_bin(g, xi) for g in (0.0, 0.5, 1.0, 2.0, 5.0)]
            self.assertEqual(vals, sorted(vals))
        self.assertEqual(log_lr_bin(3.0, 0.0), 0.0)

    def test_decision_directed(self):
        self.assertAlmostEqual(decision_directed(2.0, 1.0, 5.0, 0.98, 0.001), 0.98 * 2.0 + 0.02 * 4.0)
        self.assertEqual(decision_directed(0.0, 1.0, 0.5, 0.98, 0.001), 0.001)


class TestHmm(unittest.TestCase):
    def test_forward_odds_against_enumeration(self):
        rng = random.Random(2)
        a01, a10 = 0.2, 0.1
        trans = [[1 - a01, a01], [a10, 1 - a10]]
        prior = [a10 / (a01 + a10), a01 / (a01 + a10)]
        for _ in range(20):
            lams = [rng.uniform(-3.0, 3.0) for _ in range(6)]
            got = hmm_log_odds(lams, a01, a10)
            for n in range(1, 7):
                mass = [0.0, 0.0]
                for path in itertools.product((0, 1), repeat=n):
                    p = prior[path[0]]
                    for t in range(1, n):
                        p *= trans[path[t - 1]][path[t]]
                    for t in range(n):
                        if path[t] == 1:
                            p *= math.exp(lams[t])
                    mass[path[-1]] += p
                self.assertAlmostEqual(got[n - 1], math.log(mass[1] / mass[0]), places=9)

    def test_memoryless_chain_gives_frame_ratio(self):
        lams = [0.5, -2.0, 7.0, 1.0]
        for a, b in zip(hmm_log_odds(lams, 0.5, 0.5), lams):
            self.assertAlmostEqual(a, b, places=12)

    def test_vad_uses_the_same_recursion(self):
        x = tone_in_noise(7, 0.01)
        _, ll, lg = vad(x, init_frames=10, log_eta=10.0)
        for a, b in zip(hmm_log_odds(ll, 0.2, 0.1), lg):
            self.assertAlmostEqual(a, b, places=9)


class TestDetection(unittest.TestCase):
    def test_page_example(self):
        x = tone_in_noise(7, 0.01)
        d, ll, lg = vad(x, init_frames=10, log_eta=10.0)
        self.assertEqual(len(d), 61)
        self.assertEqual(d, [0] * 22 + [1] * 18 + [0] * 21)
        self.assertAlmostEqual(ll[22], 17.82, places=2)
        self.assertAlmostEqual(lg[22], 20.02, places=2)
        self.assertAlmostEqual(ll[42], -0.42, places=2)

    def test_noise_only_has_no_detections(self):
        for seed in range(4):
            rng = random.Random(100 + seed)
            d, _, _ = vad(white_noise(rng, 8000, 0.01), init_frames=10, log_eta=10.0)
            self.assertEqual(sum(d), 0)

    def test_errors_only_at_edges(self):
        for seed in range(3):
            d, _, _ = vad(tone_in_noise(seed, 0.02), init_frames=10, log_eta=10.0)
            self.assertEqual(sum(d[:20]) + sum(d[42:]), 0)
            self.assertEqual(sum(d[22:39]), 17)

    def test_short_input(self):
        with self.assertRaises(ValueError):
            vad([0.0] * 300, init_frames=10)


if __name__ == "__main__":
    unittest.main()
