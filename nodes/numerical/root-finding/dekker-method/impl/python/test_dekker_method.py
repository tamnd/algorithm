# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dekker-method/. The authors are listed in prov/GD9DJV.jsonl.

import math
import random
import unittest
from fractions import Fraction

from dekker_method import dekker

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


class TestDekker(unittest.TestCase):
    def test_cubic(self):
        f = Counter(lambda x: x ** 3 - x - 2)
        res = dekker(f, 1.0, 2.0, 1e-12)
        self.assertTrue(res.converged)
        self.assertLessEqual(abs(res.root - CUBIC_ROOT), 1e-12)
        self.assertEqual(res.evaluations, f.n)
        self.assertEqual(res.evaluations, res.iterations + 2)
        self.assertEqual(res.iterations, 8)
        self.assertAlmostEqual(res.iterates[1], 1.642857142857143, places=12)

    def test_observed_secant_order(self):
        f = lambda x: x ** 3 - x - 2
        res = dekker(f, 1.0, 2.0, 1e-15)
        r = Fraction(CUBIC_ROOT)
        es = [abs(float(Fraction(x) - r)) for x in res.iterates]
        logs = [math.log(es[i + 1]) / math.log(es[i]) for i in range(len(es) - 1)
                if es[i] < 2e-2 and es[i + 1] > 1e-14]
        self.assertGreaterEqual(len(logs), 3)
        for q in logs:
            self.assertAlmostEqual(q, 1.618, delta=0.12)

    def test_known_functions(self):
        for f, a, b, r in ((lambda x: math.cos(x) - x, 0.0, 1.0, 0.7390851332151607),
                           (lambda x: math.exp(x) - 2, 0.0, 1.0, math.log(2)),
                           (lambda x: x ** 10 - 1, 0.0, 1.3, 1.0)):
            for tol in (1e-6, 1e-12):
                res = dekker(f, a, b, tol)
                self.assertTrue(res.converged)
                self.assertLessEqual(abs(res.root - r), tol + 4 * math.ulp(r))
                self.assertTrue(bracket_ok(f, res))
                self.assertLess(res.evaluations, 15)

    def test_slow_case_and_bound(self):
        f = lambda x: x ** 9
        res = dekker(f, -1.0, 1.1, 1e-12)
        self.assertTrue(res.converged)
        self.assertLessEqual(abs(res.root), 1e-12)
        self.assertGreater(res.evaluations, 300)  # bisection needs about 42
        self.assertLessEqual(res.iterations, math.ceil(2 * 2.1 / 1e-12))

    def test_width_bound_small_tol(self):
        # the proved bound: at most ceil(2 (b - a) / tol) steps
        f = lambda x: (x - 0.3) ** 19
        res = dekker(f, 0.0, 1.0, 1e-3)
        self.assertTrue(res.converged)
        self.assertLessEqual(res.iterations, 2000)
        self.assertLessEqual(abs(res.root - 0.3), 1e-3 + 1e-15)

    def test_step_function(self):
        res = dekker(lambda x: -1.0 if x < 0.3 else 1.0, 0.0, 1.0, 1e-12)
        self.assertTrue(res.converged)
        self.assertLessEqual(abs(res.root - 0.3), 1e-12 + 1e-15)
        self.assertEqual(set(res.steps), {"bisect"})

    def test_multiple_root(self):
        res = dekker(lambda x: (x - 1) ** 3, 0.0, 3.3, 1e-12)
        self.assertTrue(res.converged)
        self.assertLessEqual(abs(res.root - 1.0), 1e-12 + 1e-15)

    def test_root_at_endpoint(self):
        res = dekker(lambda x: x - 1.0, 1.0, 2.0)
        self.assertEqual((res.root, res.evaluations), (1.0, 2))
        res = dekker(lambda x: x - 2.0, 1.0, 2.0)
        self.assertEqual(res.root, 2.0)

    def test_exact_zero_at_iterate(self):
        res = dekker(lambda x: 2 * x - 1, 0.0, 1.0)
        self.assertEqual(res.root, 0.5)
        self.assertEqual(res.iterations, 1)

    def test_no_sign_change(self):
        with self.assertRaises(ValueError):
            dekker(lambda x: x * x + 1, -1.0, 1.0)

    def test_nan(self):
        with self.assertRaises(ArithmeticError):
            dekker(lambda x: math.nan, 0.0, 1.0)
        with self.assertRaises(ArithmeticError):
            dekker(lambda x: -1.0 if x < 0.2 else (math.inf if x < 0.9 else 1.0), 0.0, 1.0)

    def test_max_iter(self):
        res = dekker(lambda x: x ** 9, -1.0, 1.1, 1e-12, max_iter=10)
        self.assertFalse(res.converged)
        self.assertEqual(res.evaluations, 12)
        self.assertTrue(bracket_ok(lambda x: x ** 9, res))

    def test_zero_tolerance(self):
        exact = lambda x: float(Fraction(x) ** 2 - 2)
        res = dekker(exact, 1.0, 2.0, 0.0)
        self.assertTrue(res.converged)
        self.assertLessEqual(abs(res.root - math.sqrt(2)), 4 * math.ulp(1.5))

    def test_pole(self):
        res = dekker(lambda x: 1.0 / (x - 1.0 / 3.0), 0.0, 1.0, 1e-10)
        self.assertTrue(res.converged)
        self.assertLess(abs(res.root - 1.0 / 3.0), 1e-9)

    def test_random(self):
        rng = random.Random(1969)
        for _ in range(600):
            r = rng.uniform(-5, 5)
            o1, o2 = rng.uniform(6, 9), rng.uniform(-9, -6)
            f = lambda x, r=r, o1=o1, o2=o2: (x - r) * (x - o1) * (x - o2)
            a, b = r - rng.uniform(0.1, 1.0), r + rng.uniform(0.1, 1.0)
            res = dekker(f, a, b, 1e-10)
            self.assertTrue(res.converged)
            self.assertLessEqual(abs(res.root - r), 1e-10 + 4 * math.ulp(abs(r) + 1))
            self.assertTrue(bracket_ok(f, res))
            self.assertLess(res.evaluations, 30)


if __name__ == "__main__":
    unittest.main()
