# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/durand-kerner-method/. The authors are listed in prov/VNB2F0.jsonl.

import cmath
import math
import random
import unittest
from fractions import Fraction

from durand_kerner_method import durand_kerner, horner, start_points


def poly(roots):
    c = [1 + 0j]
    for r in roots:
        c = c + [0j]
        for i in range(len(c) - 1, 0, -1):
            c[i] -= r * c[i - 1]
    return c


def max_err(z, roots):
    """Largest distance from a true root to the nearest computed one, and the reverse."""
    return max(max(min(abs(a - b) for a in z) for b in roots), max(min(abs(a - b) for b in roots) for a in z))


class TestDurandKerner(unittest.TestCase):
    def test_integer_roots(self):
        r = durand_kerner(poly([1, 2, 3, 4, 5]))
        self.assertTrue(r.converged)
        self.assertLess(max_err(r.roots, [1, 2, 3, 4, 5]), 1e-11)
        self.assertLessEqual(r.evaluations, 5 * r.iterations)

    def test_cubic_with_kerner_start(self):
        r = durand_kerner([1, 0, -1, -2], start=[(0.4 + 0.9j) ** k for k in range(3)])
        self.assertTrue(r.converged)
        self.assertEqual(r.iterations, 7)
        real = [z for z in r.roots if abs(z.imag) < 1e-12]
        self.assertEqual(len(real), 1)
        self.assertAlmostEqual(real[0].real, 1.5213797068045676, places=14)

    def test_roots_of_unity_and_complex(self):
        for n in (2, 5, 8, 15):
            roots = [cmath.exp(2j * math.pi * k / n) for k in range(n)]
            r = durand_kerner(poly(roots))
            self.assertTrue(r.converged)
            self.assertLess(max_err(r.roots, roots), 1e-12)
        roots = [1 + 2j, 1 - 2j, -3, 0.5j]
        r = durand_kerner(poly(roots))
        self.assertLess(max_err(r.roots, roots), 1e-12)

    def test_observed_quadratic_order(self):
        roots = [1, 2, 3, 4, 5]
        r = durand_kerner(poly(roots), keep_history=True)
        e = [max_err(h, roots) for h in r.history]
        qs = [math.log(e[k + 1]) / math.log(e[k]) for k in range(len(e) - 1) if 1e-10 < e[k + 1] < e[k] < 1e-2]
        self.assertTrue(qs)
        for q in qs:
            self.assertGreater(q, 1.8)
            self.assertLess(q, 2.3)

    def test_sum_of_roots_after_one_sweep(self):
        r = durand_kerner(poly([1, 2, 3, 4, 5]), max_iter=1, keep_history=True)
        self.assertAlmostEqual(sum(r.history[1]), 15, places=10)

    def test_multiple_root_is_linear(self):
        roots = [1, 1, 1, -2]
        r = durand_kerner(poly(roots), keep_history=True)
        self.assertTrue(r.converged)
        self.assertLess(max_err(r.roots, roots), 1e-4)
        e = [max_err(h, roots) for h in r.history]
        ratios = [e[k + 1] / e[k] for k in range(5, 20)]
        for q in ratios:
            self.assertAlmostEqual(q, 2 / 3, delta=0.05)

    def test_exact_coefficients_from_fractions(self):
        roots = [Fraction(1, 3), Fraction(-5, 7), Fraction(9, 4)]
        c = [Fraction(1)]
        for x in roots:
            c = c + [Fraction(0)]
            for i in range(len(c) - 1, 0, -1):
                c[i] -= x * c[i - 1]
        r = durand_kerner([float(a) for a in c])
        self.assertLess(max_err(r.roots, [float(x) for x in roots]), 1e-14)

    def test_degree_one(self):
        r = durand_kerner([2, -3])
        self.assertTrue(r.converged)
        self.assertAlmostEqual(r.roots[0], 1.5)

    def test_exact_root_in_start(self):
        r = durand_kerner([1, -3, 2], start=[1.0, 5.0])
        self.assertTrue(r.converged)
        self.assertEqual(r.roots[0], 1.0)
        self.assertLess(abs(r.roots[1] - 2), 1e-14)

    def test_coinciding_approximations(self):
        with self.assertRaises(ArithmeticError):
            durand_kerner([1, -4, 2], start=[0.0, 1.0])

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            durand_kerner([0, 1, 2])
        with self.assertRaises(ValueError):
            durand_kerner([5])
        with self.assertRaises(ValueError):
            durand_kerner([1, 0, -1], start=[1.0, 1.0])
        with self.assertRaises(ArithmeticError):
            durand_kerner([1, math.nan, 2])
        with self.assertRaises(ArithmeticError):
            durand_kerner([1, math.inf, 2])

    def test_max_iter(self):
        r = durand_kerner(poly(list(range(1, 11))), max_iter=2)
        self.assertFalse(r.converged)
        self.assertEqual(r.iterations, 2)
        self.assertEqual(r.evaluations, 20)

    def test_residual_floor_holds_at_return(self):
        r = durand_kerner(poly(list(range(1, 21))))
        self.assertTrue(r.converged)
        c = poly(list(range(1, 21)))
        for z in r.roots:
            p, floor = horner(c, z)
            self.assertLessEqual(abs(p), floor)
        self.assertLess(max_err(r.roots, list(range(1, 21))), 0.5)

    def test_start_points_distinct(self):
        z = start_points(poly([1, 2, 3]))
        self.assertEqual(len(set(z)), 3)

    def test_random_polynomials(self):
        rng = random.Random(7)
        for _ in range(500):
            n = rng.randrange(2, 9)
            roots = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
            r = durand_kerner(poly(roots))
            self.assertTrue(r.converged)
            sep = min(abs(a - b) for i, a in enumerate(roots) for b in roots[i + 1:])
            if sep > 0.1:
                self.assertLess(max_err(r.roots, roots), 1e-8)


if __name__ == "__main__":
    unittest.main()
