# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/psola/. The authors are listed in prov/Z76XPX.jsonl.

import cmath
import math
import random
import unittest

from nlsdsp import pulse_train
from psola import local_periods, psola, segment, synthesis_marks

FS = 8000


def vowel(n):
    """A 100 Hz pulse train through one resonator at 500 Hz with a 60 Hz bandwidth, and its pulse positions."""
    r = math.exp(-math.pi * 60 / FS)
    b1, c = 2 * r * math.cos(2 * math.pi * 500 / FS), -r * r
    p = pulse_train(100, FS, n)
    x, y1, y2 = [], 0.0, 0.0
    for v in p:
        y = v + b1 * y1 + c * y2
        x.append(y)
        y2, y1 = y1, y
    return x, [i for i, v in enumerate(p) if v > 0]


def harmonic(sig, f, lo, hi):
    s = sum(sig[n] * cmath.exp(-2j * math.pi * f * n / FS) for n in range(lo, hi))
    return abs(s) / (hi - lo)


class TestParts(unittest.TestCase):
    def test_local_periods(self):
        self.assertEqual(local_periods([10, 20, 32, 40]), [10, 11, 10, 8])
        with self.assertRaises(ValueError):
            local_periods([5])
        with self.assertRaises(ValueError):
            local_periods([5, 5, 9])

    def test_segment_window(self):
        x = [1.0] * 30
        seg = segment(x, 10, 4)
        self.assertEqual(len(seg), 9)
        self.assertAlmostEqual(seg[0], 0.0)
        self.assertAlmostEqual(seg[4], 1.0)
        self.assertAlmostEqual(seg[2], 0.5)
        # Samples outside x count as 0.
        self.assertEqual(segment(x, 1, 4)[:3], [0.0, 0.0, 0.0])

    def test_synthesis_mark_spacing(self):
        marks = list(range(50, 1001, 50))
        sm = synthesis_marks(marks, 1.25, 1.0)
        pos = [p for p, _ in sm]
        self.assertTrue(all(b - a == 40 for a, b in zip(pos, pos[1:])))
        self.assertEqual(pos[0], 50)
        self.assertLessEqual(pos[-1], 1000)
        sm2 = synthesis_marks(marks, 1.0, 2.0)
        self.assertEqual([i for _, i in sm2][:7], [0, 1, 1, 2, 2, 3, 3])


class TestTheorems(unittest.TestCase):
    def test_identity(self):
        # alpha = beta = 1 with marks at a constant spacing gives back x between the first and last mark.
        rng = random.Random(4)
        x = [rng.uniform(-1, 1) for _ in range(900)]
        marks = list(range(30, 871, 60))
        y = psola(x, marks)
        self.assertEqual(len(y), len(x))
        self.assertLess(max(abs(a - b) for a, b in zip(x[30:841], y[30:841])), 1e-12)

    def test_periodic_input_gives_periodized_segment(self):
        rng = random.Random(5)
        p, q = 50, 40
        base = [rng.uniform(-1, 1) for _ in range(p)]
        x = [base[n % p] for n in range(1000)]
        marks = list(range(50, 901, 50))
        y = psola(x, marks, beta=p / q)
        # The output is periodic with period q away from the ends.
        for n in range(100, 800):
            self.assertAlmostEqual(y[n + q], y[n], places=12)
        # Its Fourier coefficients over one period are G(2 pi k / q) / q, with G the DTFT of one segment.
        g = segment(x, marks[0], p)
        for k in range(q):
            c = sum(y[n] * cmath.exp(-2j * math.pi * k * n / q) for n in range(100, 100 + q)) / q
            gk = sum(v * cmath.exp(-2j * math.pi * k * j / q) for j, v in enumerate(g))
            self.assertAlmostEqual(abs(c), abs(gk) / q, places=10)


class TestExample(unittest.TestCase):
    def test_pitch_up_keeps_formant(self):
        x, marks = vowel(1600)
        self.assertEqual(len(marks), 20)
        y = psola(x, marks, beta=1.25)
        self.assertEqual(len(y), 1600)
        self.assertEqual(len(synthesis_marks(marks, 1.25, 1.0)), 24)
        out = [harmonic(y, 125 * k, 200, 200 + 8 * 64) for k in range(1, 9)]
        self.assertEqual(out.index(max(out)), 3)  # 500 Hz, the formant
        self.assertAlmostEqual(out[3], 0.88629, places=4)
        inp = [harmonic(x, 100 * k, 200, 1000) for k in range(1, 9)]
        self.assertEqual(inp.index(max(inp)), 4)  # 500 Hz
        self.assertAlmostEqual(inp[4], 0.70921, places=4)

    def test_pitch_down(self):
        x, marks = vowel(1600)
        y = psola(x, marks, beta=0.8)
        out = [harmonic(y, 80 * k, 200, 1000) for k in range(1, 9)]
        self.assertEqual(out.index(max(out)), 5)  # 480 Hz, the harmonic nearest the formant

    def test_time_stretch_keeps_period(self):
        x, marks = vowel(1600)
        y = psola(x, marks, alpha=2.0)
        self.assertEqual(len(y), 3200)
        sm = synthesis_marks(marks, 1.0, 2.0)
        pos = [p for p, _ in sm]
        self.assertTrue(all(b - a == 80 for a, b in zip(pos, pos[1:])))
        self.assertEqual(len(sm), 39)


if __name__ == "__main__":
    unittest.main()
