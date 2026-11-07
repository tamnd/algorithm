# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-quadratic-interpolation/. The authors are listed in prov/6ZVEEE.jsonl.

import math
import random
import unittest
from decimal import Decimal, getcontext

from inverse_quadratic_interpolation import inverse_quadratic_interpolation, iqi_step

CUBIC_ROOT = 1.5213797068045676
Q = 1.839286755214161  # real root of q^3 = q^2 + q + 1


class Counter:
    def __init__(self, f):
        self.f, self.n = f, 0

    def __call__(self, x):
        self.n += 1
        return self.f(x)


class TestIQI(unittest.TestCase):
    def test_cubic_table(self):
        res = inverse_quadratic_interpolation(lambda x: x ** 3 - x - 2, 1.0, 1.5, 2.0, 1e-14)
        self.assertTrue(res.converged)
        self.assertAlmostEqual(res.iterates[0], 1.5272727272727273, places=14)
        self.assertAlmostEqual(res.iterates[1], 1.521336540179002, places=12)
        self.assertLess(abs(res.root - CUBIC_ROOT), 1e-14)

    def test_step_is_exact_on_inverse_quadratic(self):
        # f is the inverse of x = 2 + 3y + y^2 near y = 0, so one step is exact
        g = lambda y: 2 + 3 * y + y * y
        ys = [0.1, -0.2, 0.3]
        x = iqi_step(g(ys[0]), ys[0], g(ys[1]), ys[1], g(ys[2]), ys[2])
        self.assertAlmostEqual(x, 2.0, places=14)

    def test_evaluation_count(self):
        f = Counter(lambda x: math.cos(x) - x)
        res = inverse_quadratic_interpolation(f, 0.0, 0.5, 1.0, 1e-12)
        self.assertEqual(f.n, res.evaluations)
        self.assertEqual(res.evaluations, res.iterations + 3)
        self.assertLess(abs(res.root - 0.7390851332151607), 1e-15)

    def test_error_constant_and_order(self):
        getcontext().prec = 120
        f = lambda x: x ** 3 - x - 2
        r = Decimal("1.5")
        for _ in range(20):
            r = r - f(r) / (3 * r * r - 1)
        fp, fpp = 3 * r * r - 1, 6 * r
        C = (3 * fpp ** 2 - fp * 6) / (6 * fp ** 2)
        xs = [Decimal(1), Decimal("1.5"), Decimal(2)]
        fs = [f(x) for x in xs]
        for _ in range(6):
            x0, x1, x2 = xs[-3:]
            f0, f1, f2 = fs[-3:]
            x3 = iqi_step(x0, f0, x1, f1, x2, f2)
            xs.append(x3)
            fs.append(f(x3))
        es = [abs(x - r) for x in xs]
        self.assertAlmostEqual(float(es[8] / (es[7] * es[6] * es[5])), float(C), places=3)
        logs = [float(es[i].ln() / es[i - 1].ln()) for i in range(6, 9)]
        self.assertAlmostEqual(sum(logs) / len(logs), Q, delta=0.08)

    def test_known_functions(self):
        for f, s, r in ((lambda x: math.exp(x) - 2, (0.0, 0.5, 1.0), math.log(2)),
                        (lambda x: (x - 0.25) * (x - 3) * (x + 4), (0.0, 0.2, 0.5), 0.25)):
            res = inverse_quadratic_interpolation(f, *s, 1e-13)
            self.assertTrue(res.converged)
            self.assertLess(abs(res.root - r), 1e-13)
            self.assertLess(res.evaluations, 15)

    def test_double_root_is_slow(self):
        res = inverse_quadratic_interpolation(lambda x: (x - 1) ** 2 * (x + 2), 0.0, 0.5, 0.8, 1e-8, 200)
        self.assertLess(abs(res.root - 1.0), 1e-4)
        self.assertGreater(res.iterations, 15)

    def test_divergence_far_from_root(self):
        res = inverse_quadratic_interpolation(math.atan, 2.0, 3.0, 4.0, 1e-12, 6)
        self.assertFalse(res.converged)
        self.assertGreater(abs(res.iterates[-1]), 1e9)

    def test_equal_values(self):
        res = inverse_quadratic_interpolation(lambda x: x * x - 1, -2.0, 2.0, 0.5)
        self.assertEqual(res.status, "equal-values")
        self.assertEqual(res.evaluations, 3)

    def test_zero_at_start_and_iterate(self):
        res = inverse_quadratic_interpolation(lambda x: x - 1.0, 1.0, 2.0, 3.0)
        self.assertEqual((res.root, res.status), (1.0, "zero"))
        res = inverse_quadratic_interpolation(lambda x: 2 * x - 1, 0.0, 0.25, 1.0)
        self.assertEqual((res.root, res.status), (0.5, "zero"))

    def test_nan(self):
        with self.assertRaises(ArithmeticError):
            inverse_quadratic_interpolation(lambda x: 1.0 if x < 0.5 else math.nan, 0.0, 0.2, 0.7)
        with self.assertRaises(ArithmeticError):
            inverse_quadratic_interpolation(lambda x: math.inf if x > 2.5 else x - 3, 0.0, 1.0, 2.0)

    def test_max_iter(self):
        res = inverse_quadratic_interpolation(lambda x: x ** 3 - x - 2, 1.0, 1.5, 2.0, 0.0, 2)
        self.assertEqual(res.status, "max-iter")
        self.assertEqual(res.evaluations, 5)

    def test_random(self):
        rng = random.Random(1839)
        for _ in range(600):
            r = rng.uniform(-3, 3)
            o1, o2 = r + rng.uniform(3, 6), r - rng.uniform(3, 6)
            f = lambda x, r=r, o1=o1, o2=o2: (x - r) * (x - o1) * (x - o2)
            h = rng.uniform(0.05, 0.3)
            res = inverse_quadratic_interpolation(f, r - h, r + h / 3, r + h, 1e-12)
            self.assertTrue(res.converged, msg=str((r, o1, o2, h, res.status)))
            self.assertLess(abs(res.root - r), 1e-10)
            self.assertLess(res.evaluations, 20)


if __name__ == "__main__":
    unittest.main()
