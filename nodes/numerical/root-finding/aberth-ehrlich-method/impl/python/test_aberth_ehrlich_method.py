# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aberth-ehrlich-method/. The authors are listed in prov/4VYZ43.jsonl.

import cmath
import math
import random
import unittest
from fractions import Fraction

from aberth_ehrlich_method import aberth, horner2, start_points

CUBIC_ROOTS = [1.5213797068045676, complex(-0.7606898534022838, 0.8578736265951786),
               complex(-0.7606898534022838, -0.8578736265951786)]


def poly(roots):
    c = [1 + 0j]
    for r in roots:
        c = c + [0j]
        for i in range(len(c) - 1, 0, -1):
            c[i] -= r * c[i - 1]
    return c


def max_err(z, roots):
    return max(max(min(abs(a - b) for a in z) for b in roots), max(min(abs(a - b) for b in roots) for a in z))


class TestAberth(unittest.TestCase):
    def test_integer_roots(self):
        r = aberth(poly([1, 2, 3, 4, 5]))
        self.assertTrue(r.converged)
        self.assertEqual(r.iterations, 6)
        self.assertEqual(r.evaluations, 30)
        self.assertLess(max_err(r.roots, [1, 2, 3, 4, 5]), 1e-12)

    def test_cubic_with_kerner_start_is_cubically_convergent(self):
        r = aberth([1, 0, -1, -2], start=[(0.4 + 0.9j) ** k for k in range(3)], keep_history=True)
        self.assertTrue(r.converged)
        e = [max_err(h, CUBIC_ROOTS) for h in r.history]
        c1 = e[3] / e[2] ** 3
        c2 = e[4] / e[3] ** 3
        self.assertLess(e[4], 1e-12)
        self.assertLess(max(c1, c2) / min(c1, c2), 3)

    def test_roots_of_unity_and_complex(self):
        for n in (2, 5, 8, 15):
            roots = [cmath.exp(2j * math.pi * k / n) for k in range(n)]
            r = aberth(poly(roots))
            self.assertTrue(r.converged)
            self.assertLess(max_err(r.roots, roots), 1e-12)
        roots = [1 + 2j, 1 - 2j, -3, 0.5j]
        self.assertLess(max_err(aberth(poly(roots)).roots, roots), 1e-12)

    def test_widely_spread_roots(self):
        roots = [1e-3, 1, 1e3]
        r = aberth(poly(roots))
        for x in roots:
            self.assertLess(min(abs(z - x) for z in r.roots), 1e-12 * x)

    def test_multiple_root_ratio(self):
        roots = [1, 1, 1, -2]
        r = aberth(poly(roots), keep_history=True)
        self.assertTrue(r.converged)
        self.assertLess(max_err(r.roots, roots), 1e-4)
        e = [max_err(h, roots) for h in r.history]
        for k in range(5, 15):
            self.assertAlmostEqual(e[k + 1] / e[k], 0.5, delta=0.05)

    def test_exact_coefficients_from_fractions(self):
        roots = [Fraction(1, 3), Fraction(-5, 7), Fraction(9, 4)]
        c = [Fraction(1)]
        for x in roots:
            c = c + [Fraction(0)]
            for i in range(len(c) - 1, 0, -1):
                c[i] -= x * c[i - 1]
        r = aberth([float(a) for a in c])
        self.assertLess(max_err(r.roots, [float(x) for x in roots]), 1e-14)

    def test_horner_derivative(self):
        p, dp, _ = horner2([1, 0, -1, -2], 2.0)
        self.assertEqual((p, dp), (4, 11))

    def test_zero_derivative_at_iterate(self):
        # p'(0) = 0 for z^2 - 1; the Newton step is undefined but p/(p' - pS) is not.
        r = aberth([1, 0, -1], start=[0.0, 3.0])
        self.assertTrue(r.converged)
        self.assertLess(max_err(r.roots, [1, -1]), 1e-14)

    def test_exact_root_in_start(self):
        r = aberth([1, -3, 2], start=[1.0, 5.0])
        self.assertEqual(r.roots[0], 1.0)
        self.assertLess(abs(r.roots[1] - 2), 1e-14)

    def test_degree_one(self):
        r = aberth([2, -3])
        self.assertAlmostEqual(r.roots[0], 1.5)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            aberth([0, 1, 2])
        with self.assertRaises(ValueError):
            aberth([5])
        with self.assertRaises(ValueError):
            aberth([1, 0, -1], start=[1.0, 1.0])
        with self.assertRaises(ArithmeticError):
            aberth([1, math.nan, 2])
        with self.assertRaises(ArithmeticError):
            aberth([1, 2, math.inf])

    def test_max_iter(self):
        r = aberth(poly(list(range(1, 11))), max_iter=2)
        self.assertFalse(r.converged)
        self.assertEqual((r.iterations, r.evaluations), (2, 20))

    def test_wilkinson_20_backward_floor(self):
        c = poly(list(range(1, 21)))
        r = aberth(c)
        self.assertTrue(r.converged)
        self.assertLess(max_err(r.roots, list(range(1, 21))), 0.5)

    def test_start_points_distinct(self):
        self.assertEqual(len(set(start_points(poly([1, 2, 3])))), 3)

    def test_random_polynomials(self):
        rng = random.Random(7)
        for _ in range(500):
            n = rng.randrange(2, 9)
            roots = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
            r = aberth(poly(roots))
            self.assertTrue(r.converged)
            self.assertLessEqual(r.evaluations, n * r.iterations)
            sep = min(abs(a - b) for i, a in enumerate(roots) for b in roots[i + 1:])
            if sep > 0.1:
                self.assertLess(max_err(r.roots, roots), 1e-8)


if __name__ == "__main__":
    unittest.main()
