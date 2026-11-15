# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-pole-placement/. The authors are listed in prov/G5MEWV.jsonl.

"""Tests for adaptive pole placement."""

import random
import unittest
from fractions import Fraction as F

from adaptive_pole_placement import app_simulate, design, diophantine, sylvester_matrix
from ctlmat import det, polyadd, polymul, polyroots, polyval

A_TRUE = [-1.5, 0.7]  # A = q^2 - 1.5 q + 0.7
B_TRUE = [1.0, 0.5]   # B = q + 0.5
AC = [1, -1, 0.25]    # (q - 0.5)^2
AO = [1, 0]           # q


def square(t):
    return 1.0 if (t // 25) % 2 == 0 else -1.0


class TestDiophantine(unittest.TestCase):
    def test_page_example_exact(self):
        A, B, Ac = [1, F(-3, 2), F(7, 10)], [1, F(1, 2)], [1, -1, F(1, 4)]
        R, S, T = design(A, B, Ac, [1, 0])
        self.assertEqual(R, [1, F(7, 34)])
        self.assertEqual(S, [F(5, 17), F(-49, 170)])
        self.assertEqual(T, [F(1, 6), 0])
        self.assertEqual(polyadd(polymul(A, R), polymul(B, S)), polymul(Ac, [1, 0]))
        self.assertEqual(det(sylvester_matrix(A, B)), F(17, 10))

    def test_random_exact_and_resultant(self):
        rng = random.Random(11)
        for n in (2, 3):
            for _ in range(5):
                A = [1] + [F(rng.randint(-9, 9), 4) for _ in range(n)]
                B = [F(rng.randint(1, 9), 4)] + [F(rng.randint(-9, 9), 4) for _ in range(n - 1)]
                Acl = [1] + [F(rng.randint(-9, 9), 8) for _ in range(2 * n - 1)]
                R, S = diophantine(A, B, Acl)
                self.assertEqual(len(R), n)
                self.assertEqual(len(S), n)
                self.assertEqual(polyadd(polymul(A, R), polymul(B, S)), Acl)
                # reference: |det| = |resultant| = |prod of B at the roots of A|
                res = 1
                for z in polyroots([float(c) for c in A]):
                    res *= polyval([float(c) for c in B], z)
                self.assertAlmostEqual(abs(float(det(sylvester_matrix(A, B)))), abs(res), places=6)

    def test_common_factor_is_rejected(self):
        A = polymul([1, F(-1, 2)], [1, F(-1, 3)])
        B = [1, F(-1, 2)]
        self.assertEqual(det(sylvester_matrix(A, B)), 0)
        with self.assertRaises(ValueError):
            diophantine(A, B, [1, 0, 0, 0])


class TestAdaptiveLoop(unittest.TestCase):
    def test_converges_to_known_plant_design(self):
        # reference: the same design with the true plant, no adaptation
        _, y_ref, _ = app_simulate(A_TRUE, B_TRUE, AC, AO, square, 200, A_TRUE + B_TRUE, adapt=False)
        self.assertAlmostEqual(y_ref[1], 1 / 6, places=12)
        th, ys, _ = app_simulate(A_TRUE, B_TRUE, AC, AO, square, 200, [0.0, 0.0, 1.0, 0.1])
        self.assertLess(max(abs(a - b) for a, b in zip(ys[100:], y_ref[100:])), 0.02)
        self.assertLess(max(abs(a - b) for a, b in zip(th[-1], A_TRUE + B_TRUE)), 0.01)

    def test_with_noise(self):
        th, _, _ = app_simulate(A_TRUE, B_TRUE, AC, AO, square, 1000, [0.0, 0.0, 1.0, 0.1],
                                sigma=0.05, seed=0)
        self.assertLess(max(abs(a - b) for a, b in zip(th[-1], A_TRUE + B_TRUE)), 0.15)

    def test_projection_keeps_b0_above_minimum(self):
        th, ys, _ = app_simulate(A_TRUE, B_TRUE, AC, AO, square, 200, [0.0, 0.0, 0.1, 0.3], b_min=0.1)
        self.assertTrue(all(v[2] >= 0.1 for v in th))
        self.assertLess(max(abs(v) for v in ys), 1e3)


if __name__ == "__main__":
    unittest.main()
