# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ephraim-malah-estimator/. The authors are listed in prov/EV1Q5W.jsonl.

import math
import random
import unittest

from ephraim_malah_estimator import bessel_ie, enhance, mmse_stsa_gain
from nlsdsp import sine, white_noise

FS = 8000


def bessel_ie_integral(nu, x, m=2000):
    """exp(-x) I_nu(x) = (1 / pi) int_0^pi exp(x (cos t - 1)) cos(nu t) dt, by Simpson's rule."""
    h = math.pi / m
    f = [math.exp(x * (math.cos(i * h) - 1.0)) * math.cos(nu * i * h) for i in range(m + 1)]
    return h / 3.0 * (f[0] + f[-1] + 4.0 * sum(f[1:-1:2]) + 2.0 * sum(f[2:-1:2])) / math.pi


def posterior_mean_gain(xi, gamma, m=3000):
    """E[A | Y] / |Y| by Simpson's rule on the posterior density of the amplitude, with lambda_d = 1."""
    lx, r = xi, math.sqrt(gamma)
    c = 1.0 / lx + 1.0
    top = r + 12.0 / math.sqrt(c) + 5.0
    h = top / m
    num = den = 0.0
    for i in range(1, m + 1):
        a = i * h
        z = 2.0 * a * r
        # p(a | Y) is proportional to a exp(-c a^2) I0(2 a r) = a exp(-c a^2 + z) bessel_ie(0, z)
        w = a * math.exp(-c * a * a + z) * bessel_ie(0, z)
        wt = 1.0 if i == m else (4.0 if i % 2 else 2.0)
        num += wt * w * a
        den += wt * w
    return num / den / r


def tone_in_noise(seed):
    rng = random.Random(seed)
    clean = [0.0] * 1600 + sine(500, FS, 6400, 0.1)
    noisy = [c + v for c, v in zip(clean, white_noise(rng, 8000, 0.05))]
    return clean, noisy


def snr_db(ref, sig, lo, hi):
    s = sum(ref[i] ** 2 for i in range(lo, hi))
    e = sum((ref[i] - sig[i]) ** 2 for i in range(lo, hi))
    return 10.0 * math.log10(s / e)


class TestBessel(unittest.TestCase):
    def test_against_integral(self):
        for x in (0.0, 0.1, 1.0, 10.0, 49.9, 50.0, 120.0, 1000.0):
            for nu in (0, 1):
                ref = bessel_ie_integral(nu, x)
                self.assertLess(abs(bessel_ie(nu, x) - ref), 1e-9 * max(ref, 1e-3))

    def test_negative(self):
        with self.assertRaises(ValueError):
            bessel_ie(0, -1.0)


class TestGain(unittest.TestCase):
    def test_gain_is_the_posterior_mean(self):
        for xi, gamma in [(1.0, 1.0), (1.0, 4.0), (0.1, 2.0), (10.0, 10.0), (3.16, 0.5), (0.01, 30.0)]:
            self.assertAlmostEqual(mmse_stsa_gain(xi, gamma), posterior_mean_gain(xi, gamma), places=7)

    def test_page_table(self):
        self.assertAlmostEqual(mmse_stsa_gain(1.0, 1.0), 0.7743, places=4)
        self.assertAlmostEqual(mmse_stsa_gain(1.0, 4.0), 0.5681, places=4)
        self.assertAlmostEqual(mmse_stsa_gain(0.1, 1.0), 0.2792, places=4)
        self.assertAlmostEqual(mmse_stsa_gain(10.0, 0.5), 1.4522, places=4)

    def test_limit_is_wiener(self):
        # G -> xi / (1 + xi) + 1 / (4 gamma) + O(1 / gamma^2) as gamma grows with xi fixed.
        for xi in (0.5, 1.0, 4.0):
            for gamma in (1e4, 1e6):
                self.assertAlmostEqual(mmse_stsa_gain(xi, gamma), xi / (1 + xi) + 0.25 / gamma, delta=2.0 / gamma**2 * (1 + 1 / xi) ** 2)

    def test_monotone_in_xi(self):
        for gamma in (0.5, 2.0, 20.0):
            vals = [mmse_stsa_gain(xi, gamma) for xi in (0.01, 0.1, 1.0, 10.0, 100.0)]
            self.assertEqual(vals, sorted(vals))

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            mmse_stsa_gain(0.0, 1.0)


class TestEnhance(unittest.TestCase):
    def test_unit_gain_gives_identity(self):
        _, noisy = tone_in_noise(3)
        out = enhance(noisy, gain=lambda xi, gamma: 1.0)
        self.assertLess(max(abs(a - b) for a, b in zip(noisy[128:7800], out[128:7800])), 1e-12)

    def test_page_example(self):
        clean, noisy = tone_in_noise(3)
        out = enhance(noisy)
        self.assertAlmostEqual(snr_db(clean, noisy, 2400, 7600), 2.89, places=2)
        self.assertAlmostEqual(snr_db(clean, out, 2400, 7600), 15.00, places=2)
        p_in = sum(v * v for v in noisy[200:1400]) / 1200
        p_out = sum(v * v for v in out[200:1400]) / 1200
        self.assertGreater(10 * math.log10(p_in / p_out), 16.0)


if __name__ == "__main__":
    unittest.main()
