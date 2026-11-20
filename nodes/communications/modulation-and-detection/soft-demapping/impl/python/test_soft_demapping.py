# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/soft-demapping/. The authors are listed in prov/N96EQ7.jsonl.

import math
import random
import unittest

import constel
from soft_demapping import extrinsic, max_star, soft_demap, soft_demap_block


def lse(values):
    """ln sum exp(v), shifted by the maximum."""
    top = max(values)
    return top + math.log(sum(math.exp(v - top) for v in values))


def brute_llr(y, points, n0, h=1, la=None):
    """The LLRs as a log-sum-exp over all points, with the priors as bit probabilities."""
    m = len(points).bit_length() - 1
    logp = []
    for i, a in enumerate(points):
        v = -abs(y - h * a) ** 2 / n0
        if la is not None:
            for k, b in enumerate(constel.bits(i, m)):
                p0 = 1.0 / (1.0 + math.exp(-la[k]))
                v += math.log(p0 if b == 0 else 1.0 - p0)
        logp.append(v)
    out = []
    for k in range(m):
        s0 = [logp[i] for i in range(len(points)) if constel.bits(i, m)[k] == 0]
        s1 = [logp[i] for i in range(len(points)) if constel.bits(i, m)[k] == 1]
        out.append(lse(s0) - lse(s1))
    return out


def prob_llr(y, points, n0, h=1):
    """The LLRs from plain probabilities, for N0 large enough that nothing underflows."""
    m = len(points).bit_length() - 1
    out = []
    for k in range(m):
        p = [0.0, 0.0]
        for i, a in enumerate(points):
            p[constel.bits(i, m)[k]] += math.exp(-abs(y - h * a) ** 2 / n0) / (math.pi * n0)
        out.append(math.log(p[0] / p[1]))
    return out


CONSTELLATIONS = {
    "bpsk": constel.pam(2),
    "4pam": constel.pam(4),
    "8pam": constel.pam(8),
    "qpsk": constel.qam(4),
    "8psk": constel.psk(8),
    "16psk": constel.psk(16, math.pi / 16),
    "16qam": constel.qam(16),
    "64qam": constel.qam(64),
}


class TestSoftDemapping(unittest.TestCase):
    def test_max_star(self):
        for a, b in [(0.0, 0.0), (3.0, -2.0), (-700.0, -701.5), (800.0, 799.0)]:
            ref = max(a, b) + math.log(math.exp(a - max(a, b)) + math.exp(b - max(a, b)))
            self.assertAlmostEqual(max_star(a, b), ref, delta=1e-12)
        self.assertEqual(max_star(-math.inf, 2.5), 2.5)
        self.assertEqual(max_star(2.5, -math.inf), 2.5)

    def test_matches_log_sum_exp(self):
        rng = random.Random(20261120)
        for name, pts in CONSTELLATIONS.items():
            for _ in range(60):
                h = complex(rng.gauss(0, 1), rng.gauss(0, 1))
                n0 = 10 ** rng.uniform(-2.5, 0.5)
                x = pts[rng.randrange(len(pts))]
                y = h * x + complex(rng.gauss(0, 1), rng.gauss(0, 1)) * math.sqrt(n0 / 2)
                got = soft_demap(y, pts, n0, h)
                ref = brute_llr(y, pts, n0, h)
                for g, r in zip(got, ref):
                    self.assertLess(abs(g - r), 1e-9, name)

    def test_matches_probabilities(self):
        rng = random.Random(7)
        for name, pts in CONSTELLATIONS.items():
            for _ in range(30):
                n0 = rng.uniform(0.2, 2.0)
                y = complex(rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5))
                for g, r in zip(soft_demap(y, pts, n0), prob_llr(y, pts, n0)):
                    self.assertLess(abs(g - r), 1e-9, name)

    def test_bpsk_closed_form(self):
        rng = random.Random(11)
        pts = constel.pam(2)
        for _ in range(200):
            h = complex(rng.gauss(0, 1), rng.gauss(0, 1))
            y = complex(rng.gauss(0, 2), rng.gauss(0, 2))
            n0 = rng.uniform(0.05, 3.0)
            (llr,) = soft_demap(y, pts, n0, h)
            self.assertAlmostEqual(llr, 4.0 * (y * h.conjugate()).real / n0, delta=1e-9)

    def test_qpsk_closed_form(self):
        rng = random.Random(12)
        pts = constel.qam(4)
        for _ in range(200):
            y = complex(rng.gauss(0, 1), rng.gauss(0, 1))
            n0 = rng.uniform(0.05, 3.0)
            l0, l1 = soft_demap(y, pts, n0)
            self.assertAlmostEqual(l0, 2.0 * math.sqrt(2.0) * y.real / n0, delta=1e-9)
            self.assertAlmostEqual(l1, 2.0 * math.sqrt(2.0) * y.imag / n0, delta=1e-9)

    def test_page_example(self):
        got = soft_demap(0.5 - 0.2j, constel.qam(16), 0.1)
        for g, r in zip(got, [6.4962, -1.6772, -2.5340, -5.5463]):
            self.assertAlmostEqual(g, r, delta=1e-4)

    def test_priors(self):
        rng = random.Random(13)
        for name in ("8psk", "16qam", "64qam"):
            pts = CONSTELLATIONS[name]
            m = len(pts).bit_length() - 1
            for _ in range(40):
                la = [rng.uniform(-6, 6) for _ in range(m)]
                n0 = 10 ** rng.uniform(-1.5, 0.3)
                y = complex(rng.gauss(0, 1), rng.gauss(0, 1))
                got = soft_demap(y, pts, n0, 1, la)
                for g, r in zip(got, brute_llr(y, pts, n0, 1, la)):
                    self.assertLess(abs(g - r), 1e-9, name)
                ext = extrinsic(y, pts, n0, 1, la)
                for e, g, a in zip(ext, got, la):
                    self.assertAlmostEqual(e, g - a, delta=1e-12)

    def test_extrinsic_of_bpsk_ignores_prior(self):
        pts = constel.pam(2)
        for la in (-3.0, 0.0, 2.5):
            (e,) = extrinsic(0.3 - 0.1j, pts, 0.5, 1, [la])
            self.assertAlmostEqual(e, 4.0 * 0.3 / 0.5, delta=1e-12)

    def test_extreme_noise_levels(self):
        pts = constel.qam(64)
        y = 0.71 - 0.33j
        tiny = soft_demap(y, pts, 1e-7)
        for g, r in zip(tiny, brute_llr(y, pts, 1e-7)):
            self.assertTrue(math.isfinite(g))
            self.assertLess(abs(g - r), 1e-9 * max(1.0, abs(r)))
        huge = soft_demap(y, pts, 1e6)
        for g in huge:
            self.assertLess(abs(g), 1e-5)

    def test_block_and_errors(self):
        pts = constel.qam(16)
        got = soft_demap_block([0.5 - 0.2j, -0.1 + 0.9j], pts, 0.3)
        self.assertEqual(len(got), 8)
        self.assertEqual(got[:4], soft_demap(0.5 - 0.2j, pts, 0.3))
        with self.assertRaises(ValueError):
            soft_demap(0.1, pts[:3], 0.3)
        with self.assertRaises(ValueError):
            soft_demap(0.1, pts, 0.0)


if __name__ == "__main__":
    unittest.main()
