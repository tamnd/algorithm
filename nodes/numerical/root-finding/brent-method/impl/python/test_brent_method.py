# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brent-method/. The authors are listed in prov/E222GS.jsonl.

import math
import random
import unittest
from fractions import Fraction

from brent_method import brent

CUBIC_ROOT = 1.5213797068045676


class Counter:
    def __init__(self, f):
        self.f, self.n = f, 0

    def __call__(self, x):
        self.n += 1
        return self.f(x)


def bracket_ok(f, res):
    fa, fb = f(res.a), f(res.b)
    return fa == 0 or fb == 0 or (fa > 0) != (fb > 0)


def bound(a, b, tol):
    k = math.ceil(math.log2((b - a) / tol))
    return 2 * (k + 2) ** 2 + 2


class TestBrent(unittest.TestCase):
    def test_cubic(self):
        f = Counter(lambda x: x ** 3 - x - 2)
        res = brent(f, 1.0, 2.0, 1e-12)
        self.assertTrue(res.converged)
        self.assertLessEqual(abs(res.root - CUBIC_ROOT), 1e-12)
        self.assertEqual(f.n, res.evaluations)
        self.assertEqual(res.evaluations, res.iterations + 2)
        self.assertEqual(res.evaluations, 9)
        self.assertEqual(res.steps[:2], ["secant", "iqi"])
        self.assertAlmostEqual(res.iterates[1], 1.582800284293, places=11)

    def test_known_functions(self):
        for f, a, b, r, n in ((lambda x: math.cos(x) - x, 0.0, 1.0, 0.7390851332151607, 8),
                              (lambda x: math.exp(x) - 2, 0.0, 1.0, math.log(2), 8),
                              (lambda x: x ** 10 - 1, 0.0, 1.3, 1.0, 10)):
            res = brent(f, a, b, 1e-12)
            self.assertTrue(res.converged)
            self.assertLessEqual(abs(res.root - r), 1e-12 + 8 * 2 ** -53 * abs(r))
            self.assertTrue(bracket_ok(f, res))
            self.assertEqual(res.evaluations, n)

    def test_superlinear_near_simple_root(self):
        f = lambda x: x ** 3 - x - 2
        res = brent(f, 1.0, 2.0, 1e-15)
        r = Fraction(CUBIC_ROOT)
        es = [abs(float(Fraction(x) - r)) for x in res.iterates]
        logs = [math.log(es[i + 1]) / math.log(es[i]) for i in range(len(es) - 1)
                if es[i] < 1e-2 and es[i + 1] > 1e-15]
        self.assertTrue(logs)
        self.assertGreater(min(logs), 1.4)

    def test_bound_on_hard_functions(self):
        cases = [(lambda x: x ** 9, -1.0, 1.1, 0.0), (lambda x: (x - 0.3) ** 19, 0.0, 1.0, 0.3),
                 (lambda x: (x - 1) ** 3, 0.0, 3.3, 1.0), (lambda x: -1.0 if x < 0.3 else 1.0, 0.0, 1.0, 0.3)]
        for f, a, b, r in cases:
            for tol in (1e-6, 1e-12):
                res = brent(f, a, b, tol)
                self.assertTrue(res.converged)
                self.assertLessEqual(abs(res.root - r), tol + 1e-15)
                self.assertLessEqual(res.evaluations, bound(a, b, tol))
        res = brent(lambda x: x ** 9, -1.0, 1.1, 1e-12)
        self.assertLess(res.evaluations, 150)  # Dekker's method needs 321

    def test_root_at_endpoint(self):
        self.assertEqual(brent(lambda x: x - 1.0, 1.0, 2.0).root, 1.0)
        self.assertEqual(brent(lambda x: x - 2.0, 1.0, 2.0).evaluations, 2)

    def test_exact_zero_at_iterate(self):
        res = brent(lambda x: 2 * x - 1, 0.0, 1.0)
        self.assertEqual(res.root, 0.5)
        self.assertEqual(res.evaluations, 3)

    def test_no_sign_change(self):
        with self.assertRaises(ValueError):
            brent(lambda x: x * x + 1, -1.0, 1.0)

    def test_nan(self):
        with self.assertRaises(ArithmeticError):
            brent(lambda x: math.nan, 0.0, 1.0)
        with self.assertRaises(ArithmeticError):
            brent(lambda x: -1.0 if x < 0.1 else (math.inf if x < 0.95 else 1.0), 0.0, 1.0)

    def test_max_iter(self):
        res = brent(lambda x: x ** 9, -1.0, 1.1, 1e-12, max_iter=5)
        self.assertFalse(res.converged)
        self.assertEqual(res.evaluations, 7)
        self.assertTrue(bracket_ok(lambda x: x ** 9, res))

    def test_zero_tolerance(self):
        exact = lambda x: float(Fraction(x) ** 2 - 2)
        res = brent(exact, 1.0, 2.0, 0.0)
        self.assertTrue(res.converged)
        self.assertLessEqual(abs(res.root - math.sqrt(2)), 4 * math.ulp(1.5))

    def test_pole(self):
        res = brent(lambda x: 1.0 / (x - 1.0 / 3.0), 0.0, 1.0, 1e-10)
        self.assertTrue(res.converged)
        self.assertLess(abs(res.root - 1.0 / 3.0), 1e-9)

    def test_random(self):
        rng = random.Random(1973)
        for _ in range(600):
            r = rng.uniform(-5, 5)
            o1, o2 = rng.uniform(6, 9), rng.uniform(-9, -6)
            mult = rng.choice((1, 1, 1, 2, 3))
            f = lambda x, r=r, o1=o1, o2=o2, m=mult: (x - r) ** m * (x - o1) * (x - o2) if m != 2 else (x - r) ** 3 * (x - o1)
            a, b = r - rng.uniform(0.1, 1.0), r + rng.uniform(0.1, 1.0)
            res = brent(f, a, b, 1e-10)
            self.assertTrue(res.converged)
            self.assertLessEqual(abs(res.root - r), 1e-10 + 1e-14)
            self.assertTrue(bracket_ok(f, res))
            self.assertLessEqual(res.evaluations, bound(a, b, 1e-10))


if __name__ == "__main__":
    unittest.main()
