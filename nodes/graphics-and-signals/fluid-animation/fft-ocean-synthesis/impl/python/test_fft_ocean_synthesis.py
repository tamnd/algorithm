# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fft-ocean-synthesis/. The authors are listed in prov/6YE8FD.jsonl.
import cmath
import math
import random
import unittest

import fft_ocean_synthesis as fo

SIZE = 16
LENGTH = 100.0
WIND = (1.0, 0.5)
SPEED = 10.0
AMP = 1e-3


def direct_dft(a, inverse=False):
    n = len(a)
    s = 1.0 if inverse else -1.0
    return [sum(a[j] * cmath.exp(s * 2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]


def direct_height(spec, size, length, x, y):
    total = 0j
    for n in range(size):
        for m in range(size):
            kx, ky = fo.wave_vector(n, m, size, length)
            total += spec[n][m] * cmath.exp(1j * (kx * x + ky * y))
    return total


class TestFFT(unittest.TestCase):
    def test_fft_equals_direct_dft(self):
        rng = random.Random(1)
        for n in (1, 2, 4, 8, 32):
            a = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
            for inverse in (False, True):
                fast = fo.fft(a, inverse)
                slow = direct_dft(a, inverse)
                self.assertLess(max(abs(p - q) for p, q in zip(fast, slow)), 1e-12)
        self.assertEqual([abs(z) for z in fo.fft([1, 0, 0, 0])], [1.0] * 4)

    def test_fft_round_trip(self):
        rng = random.Random(2)
        a = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(64)]
        back = [z / 64 for z in fo.fft(fo.fft(a), inverse=True)]
        self.assertLess(max(abs(p - q) for p, q in zip(a, back)), 1e-12)

    def test_bad_length(self):
        with self.assertRaises(ValueError):
            fo.fft([0j] * 6)


class TestOcean(unittest.TestCase):
    def setUp(self):
        self.h0 = fo.initial_amplitudes(random.Random(7), SIZE, LENGTH, AMP, WIND, SPEED)

    def test_dispersion_check_values(self):
        k = 2 * math.pi / 10.0
        w = fo.dispersion(k, 9.81)
        self.assertAlmostEqual(k, 0.628319, places=6)
        self.assertAlmostEqual(w, 2.482701, places=6)
        self.assertAlmostEqual(2 * math.pi / w, 2.530786, places=6)
        self.assertAlmostEqual(w / k, 3.951342, places=6)
        self.assertAlmostEqual(fo.dispersion(k, 9.81, depth=1000.0), w, places=12)
        self.assertLess(fo.dispersion(k, 9.81, depth=1.0), w)

    def test_spectrum_is_hermitian(self):
        for t in (0.0, 1.3, 17.0):
            spec = fo.spectrum_at(self.h0, SIZE, LENGTH, t)
            for n in range(SIZE):
                for m in range(SIZE):
                    other = spec[(-n) % SIZE][(-m) % SIZE].conjugate()
                    self.assertLess(abs(spec[n][m] - other), 1e-15 + 1e-12 * abs(spec[n][m]))

    def test_height_is_real_and_equals_direct_sum(self):
        for t in (0.0, 2.5):
            spec = fo.spectrum_at(self.h0, SIZE, LENGTH, t)
            h = fo.height_field(self.h0, SIZE, LENGTH, t)
            self.assertGreater(max(abs(z.real) for row in h for z in row), 0.05)
            self.assertLess(max(abs(z.imag) for row in h for z in row), 1e-12)
            for a in range(SIZE):
                for b in range(SIZE):
                    x, y = a * LENGTH / SIZE, b * LENGTH / SIZE
                    self.assertLess(abs(h[a][b] - direct_height(spec, SIZE, LENGTH, x, y)), 1e-12)

    def test_choppy_displacement_is_real(self):
        dx, dy = fo.choppy_displacement(self.h0, SIZE, LENGTH, 3.0, lam=0.8)
        self.assertLess(max(abs(z.imag) for g in (dx, dy) for row in g for z in row), 1e-12)
        self.assertGreater(max(abs(z.real) for row in dx for z in row), 0.01)

    def test_single_mode_is_a_moving_cosine(self):
        n, m = 3, 1
        a = complex(0.2, -0.1)
        h0 = [[0j] * SIZE for _ in range(SIZE)]
        h0[n][m] = a
        kx, ky = fo.wave_vector(n, m, SIZE, LENGTH)
        w = fo.dispersion(math.hypot(kx, ky))
        for t in (0.0, 0.7, 4.0):
            h = fo.height_field(h0, SIZE, LENGTH, t)
            for i in range(SIZE):
                for j in range(SIZE):
                    x, y = i * LENGTH / SIZE, j * LENGTH / SIZE
                    want = 2 * (a * cmath.exp(1j * (kx * x + ky * y + w * t))).real
                    self.assertAlmostEqual(h[i][j].real, want, places=12)

    def test_phillips(self):
        self.assertEqual(fo.phillips(0.0, 0.0, 1.0, WIND, SPEED), 0.0)
        self.assertAlmostEqual(fo.phillips(-0.5, 1.0, 1.0, WIND, SPEED), 0.0, places=15)
        p = fo.phillips(0.3, 0.1, 1.0, WIND, SPEED)
        self.assertAlmostEqual(p, fo.phillips(-0.3, -0.1, 1.0, WIND, SPEED), places=15)
        self.assertLess(fo.phillips(0.3, 0.1, 1.0, WIND, SPEED, small=1.0), p)

    def test_seed_and_frames(self):
        f1 = fo.synthesize(random.Random(5), 8, 50.0, AMP, WIND, SPEED, [0.0, 1.0])
        f2 = fo.synthesize(random.Random(5), 8, 50.0, AMP, WIND, SPEED, [0.0, 1.0])
        self.assertEqual(f1, f2)
        self.assertEqual(len(f1), 2)
        mean = sum(sum(row) for row in f1[1][0]) / 64
        self.assertLess(abs(mean), 1e-12)


if __name__ == "__main__":
    unittest.main()
