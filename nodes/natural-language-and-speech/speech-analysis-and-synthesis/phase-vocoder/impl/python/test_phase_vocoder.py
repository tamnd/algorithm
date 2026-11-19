# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-vocoder/. The authors are listed in prov/M9RGV0.jsonl.

import cmath
import math
import random
import unittest

from nlsdsp import fft, sine
from phase_vocoder import (
    ifft,
    instantaneous_frequency,
    overlap_add,
    periodic_hann,
    pitch_shift,
    princarg,
    resample_linear,
    stft,
    time_stretch,
)

FS = 8000


def zero_crossing_freq(v, lo, hi):
    """The frequency from the rising zero crossings of v in [lo, hi)."""
    c = [i for i in range(max(lo, 1), hi) if v[i - 1] < 0 <= v[i]]
    return (len(c) - 1) / ((c[-1] - c[0]) / FS)


class TestPrincarg(unittest.TestCase):
    def test_range_and_congruence(self):
        rng = random.Random(1)
        for _ in range(500):
            a = rng.uniform(-100.0, 100.0)
            p = princarg(a)
            self.assertGreaterEqual(p, -math.pi)
            self.assertLess(p, math.pi)
            m = (a - p) / (2.0 * math.pi)
            self.assertAlmostEqual(m, round(m), places=9)

    def test_fixed_points(self):
        for a in (0.0, 1.0, -3.0, 3.1):
            self.assertAlmostEqual(princarg(a), a, places=12)
        self.assertAlmostEqual(princarg(math.pi), -math.pi, places=12)


class TestTransforms(unittest.TestCase):
    def test_ifft_inverts_fft(self):
        rng = random.Random(2)
        x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(64)]
        y = ifft(fft(x))
        self.assertLess(max(abs(a - b) for a, b in zip(x, y)), 1e-12)

    def test_hann_overlap_is_constant(self):
        w = periodic_hann(64)
        for i in range(16):
            self.assertAlmostEqual(sum(w[i + 16 * j] for j in range(4)), 2.0, places=12)


class TestInstantaneousFrequency(unittest.TestCase):
    def test_exact_for_complex_exponential(self):
        # A complex exponential of any frequency: the estimate is exact for the bins near it.
        n, hop = 256, 64
        w = periodic_hann(n)
        for f in (0.1, 0.2345, 0.31, 1.0):
            x = [cmath.exp(1j * f * i) for i in range(n + hop)]
            a = fft([x[i] * w[i] for i in range(n)])
            b = fft([x[hop + i] * w[i] for i in range(n)])
            k = round(f * n / (2.0 * math.pi))
            for kk in (k - 1, k, k + 1):
                self.assertAlmostEqual(instantaneous_frequency(a[kk], b[kk], kk, n, hop), f, places=9)

    def test_page_example(self):
        x = sine(440, FS, 4096, 0.5)
        spectra = stft(x, 1024, 256, periodic_hann(1024))
        om = instantaneous_frequency(spectra[0][56], spectra[1][56], 56, 1024, 256)
        self.assertAlmostEqual(om * FS / (2 * math.pi), 440.0, places=4)
        self.assertAlmostEqual(abs(spectra[1][56]), 119.767, places=2)


class TestStretch(unittest.TestCase):
    def test_identity_when_hops_are_equal(self):
        rng = random.Random(3)
        x = [rng.uniform(-1, 1) for _ in range(3000)]
        y = time_stretch(x, 1.0, 256, 64)
        # Where the window sum is not small, the output equals the input.
        self.assertLess(max(abs(a - b) for a, b in zip(x[256:2700], y[256:2700])), 1e-10)

    def test_overlap_add_of_windowed_frames(self):
        w = periodic_hann(16)
        x = [float(i % 7) for i in range(64)]
        fr = [[x[s + i] * w[i] for i in range(16)] for s in range(0, 49, 4)]
        y = overlap_add(fr, 4, w)
        for i in range(12, 52):
            self.assertAlmostEqual(y[i], x[i], places=10)

    def test_length(self):
        x = sine(440, FS, 4096, 0.5)
        for ratio in (0.75, 1.5, 2.0):
            y = time_stretch(x, ratio)
            hs = round(256 * ratio)
            self.assertEqual(len(y), 12 * hs + 1024)

    def test_stretched_sine_keeps_frequency(self):
        x = sine(440, FS, 4096, 0.5)
        y = time_stretch(x, 1.5)
        self.assertEqual(len(y), 5632)
        f = zero_crossing_freq(y, 1100, 4800)
        self.assertLess(abs(f - 440.0) / 440.0, 0.005)
        peak = max(abs(v) for v in y[1100:4800])
        self.assertLess(abs(peak - 0.5), 0.05)

    def test_pitch_shift(self):
        x = sine(440, FS, 4096, 0.5)
        y = pitch_shift(x, 1.25)
        self.assertLess(abs(len(y) - 4096) / 4096, 0.06)
        f = zero_crossing_freq(y, 1100, 3000)
        self.assertLess(abs(f - 550.0) / 550.0, 0.005)

    def test_resample_linear(self):
        x = [float(i) for i in range(10)]
        self.assertEqual(resample_linear(x, 2.0), [0.0, 2.0, 4.0, 6.0, 8.0])
        self.assertEqual(resample_linear(x, 0.5)[:4], [0.0, 0.5, 1.0, 1.5])

    def test_short_input(self):
        self.assertEqual(time_stretch([0.0] * 100, 2.0), [])


if __name__ == "__main__":
    unittest.main()
