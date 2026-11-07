# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-newton-method/. The authors are listed in prov/MES2VT.jsonl.

import math
import random
import unittest
from fractions import Fraction

from interval_newton_method import Interval, iexp, interval_newton, newton_operator


def sq2(x):
    return x ** 2 - 2


def dsq2(x):
    return 2 * x


class TestIntervalArithmetic(unittest.TestCase):
    def test_outward_rounding_encloses_exact(self):
        rng = random.Random(3)
        for _ in range(500):
            a, b = sorted(rng.uniform(-10, 10) for _ in range(2))
            c, d = sorted(rng.uniform(-10, 10) for _ in range(2))
            X, Y = Interval(a, b), Interval(c, d)
            for op in ("add", "sub", "mul"):
                Z = {"add": X + Y, "sub": X - Y, "mul": X * Y}[op]
                for x in (a, b):
                    for y in (c, d):
                        ex = {"add": Fraction(x) + Fraction(y), "sub": Fraction(x) - Fraction(y),
                              "mul": Fraction(x) * Fraction(y)}[op]
                        self.assertTrue(Fraction(Z.lo) <= ex <= Fraction(Z.hi))

    def test_even_power_and_division(self):
        self.assertEqual((Interval(-2, 1) ** 2).lo, 0.0)
        with self.assertRaises(ZeroDivisionError):
            Interval(1, 2) / Interval(-1, 1)
        with self.assertRaises(ValueError):
            Interval(float("nan"), 1)


class TestIntervalNewton(unittest.TestCase):
    def test_sqrt2_verified(self):
        r = interval_newton(sq2, dsq2, 0, 3)
        self.assertEqual(r.status, "done")
        self.assertEqual(len(r.boxes), 1)
        B = r.boxes[0]
        self.assertEqual(B.status, "unique")
        self.assertTrue(B.lo <= math.sqrt(2) <= B.hi)
        self.assertLess(B.hi - B.lo, 1e-15)
        # exact check: lo^2 < 2 < hi^2
        self.assertTrue(Fraction(B.lo) ** 2 < 2 < Fraction(B.hi) ** 2)

    def test_quadratic_contraction(self):
        X, widths = Interval(1, 2), [1.0]
        for _ in range(4):
            pieces, unique = newton_operator(sq2, dsq2, X)
            self.assertTrue(unique)
            X = pieces[0]
            widths.append(X.width())
        self.assertLess(widths[3], 1e-8)
        for k in range(1, 3):
            self.assertLess(widths[k + 1], 0.1 * widths[k] ** 2)

    def test_zero_derivative_inside_splits(self):
        # f' = 2x vanishes in [-3, 3]: extended division gives two pieces
        pieces, unique = newton_operator(sq2, dsq2, Interval(-3, 3))
        self.assertFalse(unique)
        self.assertEqual(len(pieces), 2)
        r = interval_newton(sq2, dsq2, -3, 3)
        self.assertEqual([B.status for B in r.boxes], ["unique", "unique"])
        self.assertTrue(r.boxes[0].lo <= -math.sqrt(2) <= r.boxes[0].hi)

    def test_three_roots_and_eval_count(self):
        f = lambda x: (x - 1) * (x - 2) * (x - 3)
        df = lambda x: 3 * x ** 2 - 12 * x + 11
        r = interval_newton(f, df, -10, 10)
        self.assertEqual([B.status for B in r.boxes], ["unique"] * 3)
        for B, z in zip(r.boxes, (1, 2, 3)):
            self.assertTrue(B.lo <= z <= B.hi)
        self.assertEqual(r.evals, 101)
        self.assertEqual(r.iterations, 41)

    def test_roots_on_split_points(self):
        # 0, 1 and -1 are midpoints of boxes: each falls on the edge of two boxes
        r = interval_newton(lambda x: x ** 3 - x, lambda x: 3 * x ** 2 - 1, -2, 2)
        self.assertEqual([B.status for B in r.boxes], ["unique"] * 3)
        self.assertTrue(r.boxes[1].lo <= 0 <= r.boxes[1].hi)

    def test_root_at_endpoint(self):
        r = interval_newton(lambda x: (x - 1) * (x - 3), lambda x: 2 * x - 4, 1, 2)
        self.assertEqual(len(r.boxes), 1)
        self.assertEqual(r.boxes[0].status, "unique")
        self.assertTrue(r.boxes[0].lo <= 1 <= r.boxes[0].hi)

    def test_no_root_is_a_proof(self):
        r = interval_newton(lambda x: x ** 2 + 1, lambda x: 2 * x, -5, 5)
        self.assertEqual(r.boxes, [])
        self.assertEqual(r.evals, 1)

    def test_double_root_is_possible_only(self):
        r = interval_newton(lambda x: (x - 1) ** 2, lambda x: 2 * (x - 1), 0, 3)
        self.assertEqual(len(r.boxes), 1)
        B = r.boxes[0]
        self.assertEqual(B.status, "possible")
        self.assertTrue(B.lo <= 1 <= B.hi)
        self.assertLess(B.hi - B.lo, 1e-11)

    def test_exp(self):
        r = interval_newton(lambda x: iexp(x) - 2, iexp, -5, 5)
        B = r.boxes[0]
        self.assertEqual(B.status, "unique")
        self.assertTrue(B.lo <= math.log(2) <= B.hi)

    def test_max_iter_and_bad_input(self):
        r = interval_newton(sq2, dsq2, 0, 3, max_iter=3)
        self.assertEqual(r.status, "max-iter")
        self.assertEqual(r.iterations, 3)
        self.assertTrue(any(B.lo <= math.sqrt(2) <= B.hi for B in r.boxes))
        with self.assertRaises(ValueError):
            interval_newton(sq2, dsq2, 0, math.inf)
        with self.assertRaises(ValueError):
            interval_newton(sq2, dsq2, float("nan"), 1)
        with self.assertRaises(ValueError):
            interval_newton(sq2, dsq2, 2, 1)

    def test_random_cubics(self):
        rng = random.Random(11)
        for _ in range(500):
            while True:
                z = sorted(rng.uniform(-5, 5) for _ in range(3))
                if z[1] - z[0] > 0.05 and z[2] - z[1] > 0.05:
                    break
            f = lambda x, z=z: (x - z[0]) * (x - z[1]) * (x - z[2])
            df = lambda x, z=z: ((x - z[1]) * (x - z[2]) + (x - z[0]) * (x - z[2])
                                 + (x - z[0]) * (x - z[1]))
            r = interval_newton(f, df, -6, 6)
            self.assertEqual(len(r.boxes), 3)
            for B, root in zip(r.boxes, z):
                self.assertEqual(B.status, "unique")
                self.assertTrue(B.lo <= root <= B.hi)
                self.assertLess(B.hi - B.lo, 1e-13)


if __name__ == "__main__":
    unittest.main()
