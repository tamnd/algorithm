# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/illinois-method/. The authors are listed in prov/C2H8P5.jsonl.

import math
import random
import unittest
from fractions import Fraction

from illinois_method import illinois

CUBIC_ROOT = 1.5213797068045676


def poly(roots):
    def f(x):
        p = 1.0
        for r in roots:
            p *= x - r
        return p
    return f


class Counter:
    def __init__(self, f):
        self.f, self.n = f, 0

    def __call__(self, x):
        self.n += 1
        return self.f(x)


class TestIllinois(unittest.TestCase):
    def test_cubic_table(self):
        res = illinois(lambda x: x ** 3 - x - 2, 1.0, 2.0, 1e-14)
        self.assertTrue(res.converged)
        self.assertAlmostEqual(res.root, CUBIC_ROOT, delta=1e-14)
        self.assertAlmostEqual(res.iterates[0], 1.3333333333333333, places=12)
        self.assertAlmostEqual(res.iterates[5], 1.5213908211, places=9)
        self.assertEqual(res.iterations, 9)

    def test_evaluation_count(self):
        f = Counter(lambda x: x ** 3 - x - 2)
        res = illinois(f, 1.0, 2.0, 1e-6)
        self.assertEqual(f.n, res.evaluations)
        self.assertEqual(res.evaluations, res.iterations + 2)
        self.assertEqual(res.evaluations, 11)

    def test_known_functions(self):
        cases = [
            (lambda x: math.cos(x) - x, 0.0, 1.0, 0.7390851332151607),
            (lambda x: math.exp(x) - 2, 0.0, 1.0, math.log(2)),
            (lambda x: x ** 10 - 1, 0.0, 1.3, 1.0),
        ]
        for f, a, b, r in cases:
            res = illinois(f, a, b, 1e-12)
            self.assertTrue(res.converged)
            self.assertLessEqual(abs(res.root - r), 1e-12)
            self.assertLessEqual(res.a, r)
            self.assertLessEqual(r, res.b)

    def test_beats_regula_falsi(self):
        res = illinois(lambda x: x ** 10 - 1, 0.0, 1.3, 1e-10)
        self.assertEqual(res.iterations, 15)

    def test_bracket_kept(self):
        f = lambda x: x ** 3 - x - 2
        res = illinois(f, 1.0, 2.0, 1e-14)
        for x in res.iterates:
            self.assertTrue(1.0 < x < 2.0)
        self.assertTrue(f(res.a) <= 0 <= f(res.b) or f(res.b) <= 0 <= f(res.a))

    def test_observed_order(self):
        # log|e_{k+3}| / log|e_k| near 3 in the asymptotic cycle
        cases = [
            (lambda x: x ** 3 - x - 2, 1.0, 2.0, Fraction(CUBIC_ROOT)),
            (lambda x: math.exp(x) - 2, 0.0, 1.0, Fraction(math.log(2))),
        ]
        for f, a, b, r in cases:
            res = illinois(f, a, b, 0.0, max_iter=60)
            es = [abs(float(Fraction(x) - r)) for x in res.iterates]
            ratios = [math.log(es[i + 3]) / math.log(es[i]) for i in range(len(es) - 3)
                      if 1e-13 < es[i + 3] and es[i] < 1e-2]
            self.assertTrue(ratios)
            for q in ratios:
                self.assertGreater(q, 2.5)
                self.assertLess(q, 3.8)

    def test_multiple_roots(self):
        for f, r in ((poly([1.0, 1.0, 1.0]), 1.0), (lambda x: (x - 2.0) ** 3 * (x + 1), 2.0)):
            res = illinois(f, 0.3, 2.9 if r == 2.0 else 1.6, 1e-10, max_iter=2000)
            self.assertTrue(res.converged)
            self.assertLess(abs(res.root - r), 1e-3)

    def test_root_at_endpoint(self):
        res = illinois(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual(res.root, 1.0)
        self.assertEqual(res.evaluations, 2)
        res = illinois(lambda x: x - 3.0, 1.0, 3.0)
        self.assertEqual(res.root, 3.0)

    def test_exact_zero_at_iterate(self):
        res = illinois(lambda x: x - 0.5, 0.0, 1.0)
        self.assertEqual(res.root, 0.5)
        self.assertEqual(res.iterations, 1)

    def test_no_sign_change(self):
        with self.assertRaises(ValueError):
            illinois(lambda x: x * x + 1, -1.0, 1.0)

    def test_nan(self):
        with self.assertRaises(ArithmeticError):
            illinois(lambda x: float("nan"), 0.0, 1.0)
        with self.assertRaises(ArithmeticError):
            illinois(lambda x: math.inf if x > 0.3 else -1.0, 0.0, 1.0)

    def test_max_iter(self):
        res = illinois(lambda x: x ** 3 - x - 2, 1.0, 2.0, 0.0, max_iter=3)
        self.assertFalse(res.converged)
        self.assertEqual(res.iterations, 3)
        self.assertEqual(res.evaluations, 5)

    def test_zero_tolerance_terminates(self):
        exact = lambda x: float(Fraction(x) ** 2 - 2)
        res = illinois(exact, 1.0, 2.0, 0.0, max_iter=200)
        self.assertTrue(res.converged)
        self.assertLessEqual(res.b - res.a, 4 * math.ulp(2.0))

    def test_pole(self):
        res = illinois(lambda x: 1.0 / (x - 1.0 / 3.0), 0.0, 1.0, 1e-12, max_iter=500)
        self.assertLess(abs(res.root - 1.0 / 3.0), 1e-9)
        self.assertGreater(abs(1.0 / (res.root - 1.0 / 3.0)), 1e6)

    def test_random(self):
        rng = random.Random(1971)
        for _ in range(600):
            r = rng.uniform(-5, 5)
            others = [rng.uniform(6, 9), rng.uniform(-9, -6)]
            f = poly([r] + others)
            a, b = r - rng.uniform(0.1, 1.0), r + rng.uniform(0.1, 1.0)
            res = illinois(f, a, b, 1e-10)
            self.assertTrue(res.converged)
            self.assertLessEqual(abs(res.root - r), 1e-10 + 1e-14)
            self.assertLess(res.evaluations, 40)


if __name__ == "__main__":
    unittest.main()
