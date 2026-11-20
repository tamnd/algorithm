# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/max-log-demapping/. The authors are listed in prov/BTM11T.jsonl.

import math
import random
import unittest

import constel
from max_log_demapping import max_log_16qam_closed_form, max_log_demap, max_log_extrinsic, max_log_square_qam


def brute_max(y, points, n0, h=1, la=None):
    """The max form by brute force: the best metric with bit 0 minus the best with bit 1."""
    m = len(points).bit_length() - 1
    d = []
    for i, a in enumerate(points):
        v = -abs(y - h * a) ** 2 / n0
        if la is not None:
            v += sum((1 - 2 * constel.bits(i, m)[k]) * la[k] / 2.0 for k in range(m))
        d.append(v)
    out = []
    for k in range(m):
        b0 = max(d[i] for i in range(len(points)) if constel.bits(i, m)[k] == 0)
        b1 = max(d[i] for i in range(len(points)) if constel.bits(i, m)[k] == 1)
        out.append(b0 - b1)
    return out


def min_distance_form(y, points, n0, h=1):
    """(min over bit 1 of |y - h a|^2 - min over bit 0 of |y - h a|^2) / N0."""
    m = len(points).bit_length() - 1
    out = []
    for k in range(m):
        d0 = min(abs(y - h * a) ** 2 for i, a in enumerate(points) if constel.bits(i, m)[k] == 0)
        d1 = min(abs(y - h * a) ** 2 for i, a in enumerate(points) if constel.bits(i, m)[k] == 1)
        out.append((d1 - d0) / n0)
    return out


def exact_llr(y, points, n0, h=1):
    """The exact LLRs as a log-sum-exp over all points."""
    m = len(points).bit_length() - 1
    d = [-abs(y - h * a) ** 2 / n0 for a in points]
    out = []
    for k in range(m):
        acc = []
        for b in (0, 1):
            vals = [d[i] for i in range(len(points)) if constel.bits(i, m)[k] == b]
            top = max(vals)
            acc.append(top + math.log(sum(math.exp(v - top) for v in vals)))
        out.append(acc[0] - acc[1])
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


def sample(rng, pts):
    h = complex(rng.gauss(0, 1), rng.gauss(0, 1))
    n0 = 10 ** rng.uniform(-2.5, 0.5)
    x = pts[rng.randrange(len(pts))]
    y = h * x + complex(rng.gauss(0, 1), rng.gauss(0, 1)) * math.sqrt(n0 / 2)
    return y, n0, h


class TestMaxLogDemapping(unittest.TestCase):
    def test_equals_max_form_exactly(self):
        rng = random.Random(20261120)
        for name, pts in CONSTELLATIONS.items():
            for _ in range(60):
                y, n0, h = sample(rng, pts)
                self.assertEqual(max_log_demap(y, pts, n0, h), brute_max(y, pts, n0, h), name)

    def test_min_distance_form(self):
        rng = random.Random(3)
        for name, pts in CONSTELLATIONS.items():
            for _ in range(40):
                y, n0, h = sample(rng, pts)
                for g, r in zip(max_log_demap(y, pts, n0, h), min_distance_form(y, pts, n0, h)):
                    self.assertLess(abs(g - r), 1e-9 * max(1.0, abs(r)), name)

    def test_bound_against_exact(self):
        rng = random.Random(5)
        for name, pts in CONSTELLATIONS.items():
            bound = math.log(len(pts) / 2)
            for _ in range(60):
                y, n0, h = sample(rng, pts)
                for g, r in zip(max_log_demap(y, pts, n0, h), exact_llr(y, pts, n0, h)):
                    self.assertLessEqual(abs(g - r), bound + 1e-9, name)

    def test_equal_to_exact_for_bpsk_and_qpsk(self):
        rng = random.Random(6)
        for name in ("bpsk", "qpsk"):
            pts = CONSTELLATIONS[name]
            for _ in range(100):
                y, n0, h = sample(rng, pts)
                for g, r in zip(max_log_demap(y, pts, n0, h), exact_llr(y, pts, n0, h)):
                    self.assertLess(abs(g - r), 1e-9 * max(1.0, abs(r)), name)

    def test_scales_with_one_over_n0(self):
        rng = random.Random(8)
        pts = CONSTELLATIONS["16qam"]
        for _ in range(50):
            y = complex(rng.gauss(0, 1), rng.gauss(0, 1))
            a = max_log_demap(y, pts, 1.0)
            b = max_log_demap(y, pts, 0.01)
            for u, v in zip(a, b):
                self.assertLess(abs(100.0 * u - v), 1e-9 * max(1.0, abs(v)))

    def test_signs_give_ml_bits(self):
        rng = random.Random(9)
        for name, pts in CONSTELLATIONS.items():
            m = len(pts).bit_length() - 1
            for _ in range(60):
                y, n0, h = sample(rng, pts)
                ml = constel.bits(constel.ml_detect(y, pts, h), m)
                llr = max_log_demap(y, pts, n0, h)
                self.assertEqual([1 if v < 0 else 0 for v in llr], ml, name)

    def test_square_qam_per_axis(self):
        rng = random.Random(10)
        for big_m in (4, 16, 64, 256):
            pts = constel.qam(big_m)
            for _ in range(40):
                y, n0, h = sample(rng, pts)
                for g, r in zip(max_log_square_qam(y, big_m, n0, h), max_log_demap(y, pts, n0, h)):
                    self.assertLess(abs(g - r), 1e-9 * max(1.0, abs(r)), big_m)

    def test_16qam_closed_form(self):
        rng = random.Random(11)
        pts = constel.qam(16)
        for _ in range(300):
            y, n0, h = sample(rng, pts)
            for g, r in zip(max_log_16qam_closed_form(y, n0, h), max_log_demap(y, pts, n0, h)):
                self.assertLess(abs(g - r), 1e-9 * max(1.0, abs(r)))

    def test_page_example(self):
        pts = constel.qam(16)
        y = 0.5 - 0.2j
        for g, r in zip(max_log_demap(y, pts, 0.1), [6.3246, -1.6754, -2.5298, -5.4702]):
            self.assertAlmostEqual(g, r, delta=1e-4)
        for g, r in zip(exact_llr(y, pts, 0.1), [6.4962, -1.6772, -2.5340, -5.5463]):
            self.assertAlmostEqual(g, r, delta=1e-4)
        for g, r in zip(max_log_demap(y, pts, 1.0), [0.6325, -0.1675, -0.2530, -0.5470]):
            self.assertAlmostEqual(g, r, delta=1e-4)

    def test_priors_and_extrinsic(self):
        rng = random.Random(12)
        for name in ("8psk", "16qam", "64qam"):
            pts = CONSTELLATIONS[name]
            m = len(pts).bit_length() - 1
            for _ in range(40):
                la = [rng.uniform(-6, 6) for _ in range(m)]
                y, n0, h = sample(rng, pts)
                got = max_log_demap(y, pts, n0, h, la)
                self.assertEqual(got, brute_max(y, pts, n0, h, la), name)
                ext = max_log_extrinsic(y, pts, n0, h, la)
                for e, g, a in zip(ext, got, la):
                    self.assertAlmostEqual(e, g - a, delta=1e-12)

    def test_errors(self):
        pts = constel.qam(16)
        with self.assertRaises(ValueError):
            max_log_demap(0.1, pts[:3], 0.3)
        with self.assertRaises(ValueError):
            max_log_demap(0.1, pts, 0.0)
        with self.assertRaises(ValueError):
            max_log_square_qam(0.1, 8, 0.3)


if __name__ == "__main__":
    unittest.main()
