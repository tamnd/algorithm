# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thiele-continued-fraction-interpolation/. The authors are listed in prov/D0H64Z.jsonl.

import math
import random
import unittest
from fractions import Fraction as F

from thiele_continued_fraction_interpolation import (
    INF, thiele_eval, thiele_fit, thiele_type)


def rat(num, den, t):
    p = sum(c * t ** i for i, c in enumerate(num))
    q = sum(c * t ** i for i, c in enumerate(den))
    return p / q


class TestThiele(unittest.TestCase):
    def test_hand_example(self):
        # f = 1/(1+x) at 0, 1, 2: inverse differences 1, -2, -1
        m = thiele_fit([F(0), F(1), F(2)], [F(1), F(1, 2), F(1, 3)])
        self.assertEqual(m[1], [F(1), F(-2), F(-1)])
        self.assertEqual(thiele_type(m), (1, 1))
        for t in range(10):
            self.assertEqual(thiele_eval(m, F(t)), F(1, 1 + t))

    def test_interpolates_random_data(self):
        rng = random.Random(11)
        for n in range(1, 12):
            xs = rng.sample(range(-30, 30), n)
            xs = [F(v, 3) for v in xs]
            ys = [F(rng.randint(-50, 50), rng.randint(1, 9)) for _ in xs]
            m = thiele_fit(xs, ys)
            for x, y in zip(xs, ys):
                self.assertEqual(thiele_eval(m, x), y)

    def test_reproduces_rational_functions(self):
        rng = random.Random(5)
        checked = 0
        for k in range(0, 5):
            for _ in range(5):
                num = [rng.randint(-9, 9) for _ in range(k + 1)]
                den = [rng.randint(1, 9)] + [rng.randint(-9, 9) for _ in range(k)]
                xs = [F(i, 2) for i in range(2 * k + 4)]
                if any(sum(c * x ** i for i, c in enumerate(den)) == 0
                       for x in xs):
                    continue
                checked += 1
                ys = [rat(num, den, x) for x in xs]
                m = thiele_fit(xs, ys)
                self.assertLessEqual(len(m[1]), 2 * k + 1)  # early stop
                for t in [F(-7, 3), F(13, 5), F(40)]:
                    if sum(c * t ** i for i, c in enumerate(den)) != 0:
                        self.assertEqual(thiele_eval(m, t), rat(num, den, t))
        self.assertGreater(checked, 20)

    def test_runge_function_found_with_five_coefficients(self):
        for n in (5, 9, 17):
            xs = [F(-1) + F(2 * i, n - 1) for i in range(n)]
            m = thiele_fit(xs, [1 / (1 + 25 * x * x) for x in xs])
            self.assertEqual(len(m[1]), 5)
            self.assertEqual(thiele_eval(m, F(3, 10)), 1 / (1 + 25 * F(9, 100)))

    def test_polynomials(self):
        m = thiele_fit([F(i) for i in range(4)], [F(i * i) for i in range(4)])
        self.assertEqual(m[1], [F(0), F(1), F(-2), F(-1)])
        for t in range(-5, 9):
            self.assertEqual(thiele_eval(m, F(t)), F(t * t))

    def test_single_and_two_nodes(self):
        m = thiele_fit([F(3)], [F(7)])
        self.assertEqual(thiele_eval(m, F(100)), F(7))
        m = thiele_fit([F(0), F(2)], [F(1), F(5)])
        self.assertEqual(thiele_eval(m, F(1)), F(3))   # the line 1 + 2x
        m = thiele_fit([F(0), F(2)], [F(4), F(4)])
        self.assertEqual(len(m[1]), 1)                 # constant, early stop
        self.assertEqual(thiele_eval(m, F(-9)), F(4))

    def test_reordering_on_infinite_inverse_difference(self):
        # f = x(x-1)/(x+1) + 1 has f(0) = f(1), so phi_1(x_1) is infinite
        f = lambda x: x * (x - 1) / (x + 1) + 1
        xs = [F(0), F(1), F(2), F(3)]
        m = thiele_fit(xs, [f(x) for x in xs])
        self.assertTrue(all(b is not INF for b in m[1]))
        self.assertEqual(m[0][1], F(2))
        for t in [F(-3), F(1, 2), F(7)]:
            self.assertEqual(thiele_eval(m, t), f(t))

    def test_unattainable_point(self):
        # no rational function of type (1,1) takes 1, 2, 2 at 0, 1, 2
        m = thiele_fit([F(0), F(1), F(2)], [F(1), F(2), F(2)])
        with self.assertRaises(ValueError):
            thiele_eval(m, F(0))
        self.assertEqual(thiele_eval(m, F(1)), F(2))
        self.assertEqual(thiele_eval(m, F(5)), F(2))

    def test_pole(self):
        f = lambda x: 1 / (x - F(1, 2))
        xs = [F(0), F(1), F(2), F(3)]
        m = thiele_fit(xs, [f(x) for x in xs])
        self.assertIs(thiele_eval(m, F(1, 2)), INF)
        self.assertEqual(thiele_eval(m, F(5)), f(F(5)))

    def test_float_accuracy_beats_polynomial_near_pole(self):
        n = 17
        xs = [1.5 * (-1 + 2 * i / (n - 1)) for i in range(n)]
        m = thiele_fit(xs, [math.tan(x) for x in xs])
        err = max(abs(thiele_eval(m, t) - math.tan(t))
                  for t in [1.5 * (-1 + 2 * (i + 0.5) / 200) for i in range(200)])
        self.assertLess(err, 1e-9)
        m = thiele_fit([i / 8 for i in range(9)], [math.exp(i / 8) for i in range(9)])
        self.assertLess(abs(thiele_eval(m, 0.3) - math.exp(0.3)), 1e-12)

    def test_errors(self):
        with self.assertRaises(ValueError):
            thiele_fit([], [])
        with self.assertRaises(ValueError):
            thiele_fit([1, 2], [1])
        with self.assertRaises(ValueError):
            thiele_fit([1, 1], [2, 3])


if __name__ == "__main__":
    unittest.main()
