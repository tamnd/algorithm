# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/halley-method/. The authors are listed in prov/4V4H83.jsonl.

import math
import random
import unittest
from fractions import Fraction

from halley_method import halley

ROOT = 1.5213797068045676


def f(x):
    return x ** 3 - x - 2


def df(x):
    return 3 * x * x - 1


def d2f(x):
    return 6 * x


class TestHalley(unittest.TestCase):
    def test_cubic(self):
        r = halley(f, df, d2f, 1.0)
        self.assertTrue(r.converged)
        self.assertLessEqual(abs(r.root - ROOT), 4e-16)
        self.assertEqual(r.iterations, 4)
        self.assertEqual(r.evaluations, 5)
        self.assertAlmostEqual(r.iterates[1], 1.4, places=15)

    def test_exact_cubic_rate_with_fractions(self):
        # e_(k+1)/e_k^3 tends to c2^2 - c3 = 0.4214027...
        x = Fraction(1)
        r = Fraction(ROOT)
        xs = [x]
        for _ in range(4):
            fx, d1, d2 = x ** 3 - x - 2, 3 * x * x - 1, 6 * x
            x = x - 2 * fx * d1 / (2 * d1 * d1 - fx * d2)
            xs.append(x)
        # refine the reference root exactly enough by Newton in Fraction
        for _ in range(6):
            r = r - (r ** 3 - r - 2) / (3 * r * r - 1)
            r = Fraction(round(r * 10 ** 60), 10 ** 60)
        e = [float(v - r) for v in xs]
        ratio = e[4] / e[3] ** 3
        self.assertAlmostEqual(ratio, 0.4214027, places=5)

    def test_observed_order(self):
        r = halley(lambda x: math.exp(x) - 2, math.exp, math.exp, 0.0)
        e = [abs(x - math.log(2)) for x in r.iterates]
        self.assertLess(e[2], 1e-5)
        q = math.log(e[2]) / math.log(e[1])
        self.assertGreater(q, 2.5)

    def test_other_functions(self):
        cases = [(lambda x: math.cos(x) - x, lambda x: -math.sin(x) - 1, lambda x: -math.cos(x), 1.0, 0.7390851332151607),
                 (lambda x: x ** 10 - 1, lambda x: 10 * x ** 9, lambda x: 90 * x ** 8, 1.5, 1.0)]
        for g, dg, d2g, x0, root in cases:
            r = halley(g, dg, d2g, x0)
            self.assertTrue(r.converged)
            self.assertLess(abs(r.root - root), 1e-15)

    def test_atan_from_far(self):
        for x0 in (1.5, 3.0, 10.0, 100.0):
            r = halley(math.atan, lambda x: 1 / (1 + x * x), lambda x: -2 * x / (1 + x * x) ** 2, x0)
            self.assertTrue(r.converged)
            self.assertLess(abs(r.root), 1e-15)

    def test_multiple_root_linear_rate(self):
        r = halley(lambda x: x ** 3, lambda x: 3 * x * x, lambda x: 6 * x, 1.0, max_iter=200)
        self.assertEqual(r.iterates[1:4], [0.5, 0.25, 0.125])
        r = halley(lambda x: (x - 1) ** 2 * (x + 2), lambda x: 3 * x * x - 3, lambda x: 6 * x, 2.0)
        e = [abs(x - 1) for x in r.iterates]
        for k in range(3, 15):
            self.assertAlmostEqual(e[k + 1] / e[k], 1 / 3, delta=0.02)

    def test_exact_zero(self):
        r = halley(lambda x: x - 3, lambda x: 1.0, lambda x: 0.0, 3.0)
        self.assertEqual((r.status, r.iterations, r.root), ("exact", 0, 3.0))

    def test_zero_derivative_stalls(self):
        r = halley(lambda x: x * x - 2, lambda x: 2 * x, lambda x: 2.0, 0.0)
        self.assertEqual(r.status, "stalled")
        self.assertFalse(r.converged)

    def test_zero_denominator(self):
        # f = 1 + x with a supplied f'' = 2: 2 f'^2 - f f'' = 2 - 2 = 0 at x = 0.
        r = halley(lambda x: 1 + x, lambda x: 1.0, lambda x: 2.0, 0.0)
        self.assertEqual(r.status, "zero-denominator")

    def test_no_real_root_hits_max_iter(self):
        r = halley(lambda x: x * x + 1, lambda x: 2 * x, lambda x: 2.0, 0.5, max_iter=50)
        self.assertEqual(r.status, "max-iter")
        self.assertEqual((r.iterations, r.evaluations), (50, 50))

    def test_nan_and_inf(self):
        with self.assertRaises(ArithmeticError):
            halley(lambda x: math.nan, lambda x: 1.0, lambda x: 0.0, 1.0)
        with self.assertRaises(ArithmeticError):
            halley(lambda x: x, lambda x: math.inf, lambda x: 0.0, 1.0)

    def test_random_quadratics(self):
        rng = random.Random(42)
        for _ in range(600):
            a = rng.uniform(0.5, 10)
            g = lambda x, a=a: x * x - a  # root sqrt(a)
            r = halley(g, lambda x: 2 * x, lambda x: 2.0, rng.uniform(0.2, 20) * math.sqrt(a))
            self.assertTrue(r.converged)
            self.assertLess(abs(r.root - math.sqrt(a)), 4e-15 * math.sqrt(a))
            self.assertLessEqual(r.iterations, 12)


if __name__ == "__main__":
    unittest.main()
