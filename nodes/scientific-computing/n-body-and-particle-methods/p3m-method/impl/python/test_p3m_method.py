# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/p3m-method/. The authors are listed in prov/J50KQM.jsonl.
"""Tests for P3M: the FFT, the assignment weights, the short-range sum, and the forces against Ewald summation."""

import cmath
import math
import random
import unittest

from p3m_method import ewald_forces, fft, fft2, p3m_forces, short_range, weights


def rms_err(f, ref):
    num = sum((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 for a, b in zip(f, ref))
    den = sum(b[0] ** 2 + b[1] ** 2 for b in ref)
    return math.sqrt(num / den)


def charges(n, seed):
    rng = random.Random(seed)
    pos = [(rng.random(), rng.random()) for _ in range(n)]
    q = [1.0 if i % 2 == 0 else -1.0 for i in range(n)]
    return q, pos


class TestPieces(unittest.TestCase):
    def test_fft_matches_dft(self):
        rng = random.Random(1)
        a = [complex(rng.random(), rng.random()) for _ in range(16)]
        for inverse, sign in ((False, -1), (True, 1)):
            b = fft(a, inverse)
            for k in range(16):
                d = sum(a[g] * cmath.exp(sign * 2j * math.pi * k * g / 16) for g in range(16))
                self.assertAlmostEqual(abs(b[k] - d), 0.0, places=12)

    def test_fft2_round_trip(self):
        rng = random.Random(2)
        grid = [[complex(rng.random(), 0) for _ in range(8)] for _ in range(8)]
        back = fft2(fft2(grid), inverse=True)
        for i in range(8):
            for j in range(8):
                self.assertAlmostEqual(abs(back[i][j] / 64 - grid[i][j]), 0.0, places=12)

    def test_weights_conserve_charge_and_center(self):
        rng = random.Random(3)
        m = 16
        for order in (2, 3):
            for _ in range(20):
                x = rng.uniform(0.1, 0.9)
                w = weights(x, m, order)
                self.assertAlmostEqual(sum(v for _, v in w), 1.0, places=14)
                u = x * m
                center = sum(v * (g + m * round((u - g) / m)) for g, v in w)
                self.assertAlmostEqual(center, u, places=12)

    def test_short_range_matches_brute_force(self):
        q, pos = charges(120, 4)
        alpha, r_c = 12.0, 0.25
        f, pairs = short_range(q, pos, alpha, r_c)
        count = 0
        for i in range(120):
            fx = fy = 0.0
            for j in range(120):
                if i == j:
                    continue
                rx = pos[i][0] - pos[j][0]
                ry = pos[i][1] - pos[j][1]
                rx -= round(rx)
                ry -= round(ry)
                r2 = rx * rx + ry * ry
                if r2 < r_c * r_c:
                    c = q[i] * q[j] * math.exp(-alpha * alpha * r2) / r2
                    fx += c * rx
                    fy += c * ry
                    count += 1
            self.assertAlmostEqual(f[i][0], fx, places=9)
            self.assertAlmostEqual(f[i][1], fy, places=9)
        self.assertEqual(pairs, count)

    def test_ewald_does_not_depend_on_alpha(self):
        q, pos = charges(60, 5)
        self.assertLess(rms_err(ewald_forces(q, pos, alpha=6.0, kmax=12), ewald_forces(q, pos)), 1e-10)


class TestP3M(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q, cls.pos = charges(200, 21)
        cls.ref = ewald_forces(cls.q, cls.pos)

    def test_accuracy_against_ewald(self):
        cases = ((32, 2, 5e-3), (32, 3, 6e-4), (64, 3, 1e-4))
        for m, order, tol in cases:
            f, st = p3m_forces(self.q, self.pos, m=m, order=order)
            self.assertLess(rms_err(f, self.ref), tol)
        self.assertEqual(st["mesh"], 64 * 64)

    def test_influence_functions(self):
        errs = [rms_err(p3m_forces(self.q, self.pos, m=16, alpha=16.0, r_c=0.1875, kind=k)[0], self.ref)
                for k in ("plain", "deconvolved", "optimal")]
        self.assertLess(errs[1], errs[0] / 1.5)
        self.assertLess(errs[2], errs[1])

    def test_smaller_alpha_moves_work_to_the_pairs(self):
        prev_err, prev_pairs = 0.0, 10 ** 9
        for alpha, r_c in ((8.0, 0.375), (12.0, 0.25), (20.0, 0.15)):
            f, st = p3m_forces(self.q, self.pos, m=32, alpha=alpha, r_c=r_c)
            e = rms_err(f, self.ref)
            self.assertGreater(e, prev_err)
            self.assertLess(st["pairs"], prev_pairs)
            prev_err, prev_pairs = e, st["pairs"]

    def test_total_force_is_zero(self):
        f, _ = p3m_forces(self.q, self.pos, m=32)
        scale = math.sqrt(sum(a * a + b * b for a, b in self.ref) / len(self.ref))
        self.assertLess(abs(sum(a for a, _ in f)), 1e-10 * scale)
        self.assertLess(abs(sum(b for _, b in f)), 1e-10 * scale)
        single, _ = p3m_forces([1.0], [(0.3, 0.6)], m=32)
        self.assertLess(math.hypot(*single[0]), 1e-12)

    def test_pair_force(self):
        for d in (0.05, 0.2, 0.4):
            pos2 = [(0.3, 0.5), (0.3 + d, 0.5)]
            f, _ = p3m_forces([1.0, -1.0], pos2, m=32)
            r = ewald_forces([1.0, -1.0], pos2)
            self.assertLess(abs(f[0][0] - r[0][0]), 0.01 * abs(r[0][0]))
            self.assertGreater(f[0][0], 0.0)


if __name__ == "__main__":
    unittest.main()
