# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chandrupatla-method/. The authors are listed in prov/WGGEP1.jsonl.

import math
import random
import unittest
from fractions import Fraction

from chandrupatla_method import chandrupatla

U = 2.0 ** -53


def cubic(x):
    return x ** 3 - x - 2


CUBIC_ROOT = 1.5213797068045676


def accept(a, b, c, fa, fb, fc):
    xi = (a - b) / (c - b)
    phi = (fa - fb) / (fc - fb)
    return phi * phi < xi and (1 - phi) * (1 - phi) < 1 - xi


class TestChandrupatla(unittest.TestCase):
    def check_root(self, f, a, b, root, tol=1e-12):
        r = chandrupatla(f, a, b, tol)
        self.assertTrue(r.converged)
        self.assertLessEqual(abs(r.root - root), tol + 8 * U * abs(r.root) + 1e-300)
        self.assertLessEqual(r.a, r.root)
        self.assertLessEqual(r.root, r.b)
        self.assertEqual(r.evaluations, r.iterations + 2)
        return r

    def test_smooth_functions(self):
        self.check_root(cubic, 1.0, 2.0, CUBIC_ROOT)
        self.check_root(lambda x: math.cos(x) - x, 0.0, 1.0, 0.7390851332151607)
        self.check_root(lambda x: math.exp(x) - 2, 0.0, 1.0, math.log(2))
        self.check_root(lambda x: x ** 10 - 1, 0.0, 1.3, 1.0)

    def test_cubic_counts_and_steps(self):
        r = self.check_root(cubic, 1.0, 2.0, CUBIC_ROOT)
        self.assertEqual(r.iterations, 6)
        self.assertEqual(r.evaluations, 8)
        self.assertEqual(r.steps, ["bisect"] + ["iqi"] * 5)

    def test_observed_order(self):
        r = chandrupatla(cubic, 1.0, 2.0, 1e-12)
        e = [abs(x - CUBIC_ROOT) for x in r.iterates[1:5]]
        for k in (1, 2):
            q = math.log(e[k + 1]) / math.log(e[k])
            self.assertGreater(q, 1.6)
            self.assertLess(q, 2.2)

    def test_multiple_roots_stay_near_bisection(self):
        for f, a, b, root in ((lambda x: x ** 9, -1.0, 1.1, 0.0), (lambda x: (x - 1) ** 3, 0.0, 3.3, 1.0), (lambda x: (x - 0.3) ** 19, 0.0, 1.0, 0.3)):
            r = self.check_root(f, a, b, root)
            self.assertLess(r.evaluations, 60)

    def test_discontinuous_and_pole(self):
        r = chandrupatla(lambda x: -1.0 if x < 0.3 else 1.0, 0.0, 1.0, 1e-12)
        self.assertTrue(r.a <= 0.3 <= r.b and r.b - r.a <= 1e-12 + 1e-15)
        r = chandrupatla(lambda x: 1 / (x - 1 / 3), 0.0, 1.0, 1e-12)
        self.assertTrue(r.a <= 1 / 3 <= r.b)

    def test_bracket_kept_every_step(self):
        seen = []

        def f(x):
            seen.append(x)
            return cubic(x)

        r = chandrupatla(f, 1.0, 2.0, 1e-14)
        lo, hi = 1.0, 2.0
        for x in seen[2:]:
            self.assertTrue(lo < x < hi)
            if cubic(x) < 0:
                lo = x
            else:
                hi = x
        self.assertTrue(lo <= r.root <= hi)

    def test_acceptance_means_monotone_inverse_quadratic(self):
        rng = random.Random(11)
        for _ in range(500):
            a, b, c = 0.0, 1.0, rng.uniform(-3.0, -0.01)
            fa, fb, fc = rng.uniform(-2, -0.01), rng.uniform(0.01, 2), rng.uniform(-3, -0.01)
            if not accept(a, b, c, fa, fb, fc):
                continue
            def P(y):
                return (a * (y - fb) * (y - fc) / ((fa - fb) * (fa - fc)) + b * (y - fa) * (y - fc) / ((fb - fa) * (fb - fc))
                        + c * (y - fa) * (y - fb) / ((fc - fa) * (fc - fb)))
            ys = [fc + (fb - fc) * i / 100 for i in range(101)]
            xs = [P(y) for y in ys]
            self.assertTrue(all(xs[i] <= xs[i + 1] + 1e-12 for i in range(100)))
            self.assertTrue(a < P(0.0) < b)

    def test_root_at_endpoint(self):
        r = chandrupatla(lambda x: x - 1, 1.0, 2.0)
        self.assertEqual((r.root, r.evaluations, r.iterations), (1.0, 2, 0))
        r = chandrupatla(lambda x: x - 2, 1.0, 2.0)
        self.assertEqual((r.root, r.evaluations), (2.0, 2))

    def test_exact_zero_at_iterate(self):
        r = chandrupatla(lambda x: x - 0.5, 0.0, 1.0)
        self.assertEqual(r.root, 0.5)
        self.assertEqual(r.evaluations, 3)
        self.assertTrue(r.converged)

    def test_zero_slope_at_iterate(self):
        # f'(1.5) = 0: the first midpoint sits at a stationary point; the bracket logic does not care.
        f = lambda x: (x - 1.5) ** 2 - 0.01 if x < 1.5 else -0.01 + 0.0 * x - (x - 1.5) ** 3
        r = chandrupatla(f, 1.0, 2.0, 1e-12)
        self.assertTrue(r.converged)
        self.assertLess(abs(f(r.root)), 1e-10)

    def test_no_sign_change(self):
        with self.assertRaises(ValueError):
            chandrupatla(lambda x: x * x + 1, -1.0, 1.0)

    def test_max_iter(self):
        r = chandrupatla(cubic, 1.0, 2.0, 1e-14, max_iter=2)
        self.assertFalse(r.converged)
        self.assertEqual(r.iterations, 2)
        self.assertEqual(r.evaluations, 4)
        self.assertTrue(r.a <= CUBIC_ROOT <= r.b)

    def test_zero_tolerance_terminates(self):
        r = chandrupatla(lambda x: x ** 3, -1.0, 1.1, 0.0, max_iter=5000)
        self.assertTrue(abs(r.root) < 1e-100)

    def test_nan_and_inf(self):
        with self.assertRaises(ArithmeticError):
            chandrupatla(lambda x: math.nan, 0.0, 1.0)
        with self.assertRaises(ArithmeticError):
            chandrupatla(lambda x: math.inf if 0.4 < x < 0.6 else x - 0.7, 0.0, 1.0)

    def test_step_bound_from_tolerance(self):
        for tol in (1e-2, 1e-4, 1e-6):
            r = chandrupatla(lambda x: (x - 0.3) ** 19, 0.0, 1.0, tol)
            self.assertLessEqual(r.iterations, math.ceil(2 * 1.0 / tol))

    def test_exact_fraction_reference(self):
        # Root of x^3 - x - 2 to 30 digits by Fraction bisection.
        lo, hi = Fraction(3, 2), Fraction(2)
        for _ in range(110):
            mid = (lo + hi) / 2
            if mid ** 3 - mid - 2 < 0:
                lo = mid
            else:
                hi = mid
        r = chandrupatla(cubic, 1.0, 2.0, 0.0)
        self.assertLess(abs(Fraction(r.root) - lo), Fraction(1, 10 ** 15))

    def test_random_cubics(self):
        rng = random.Random(2024)
        total_c = total_b = 0
        for _ in range(600):
            roots = sorted(rng.uniform(-10, 10) for _ in range(3))
            k = rng.randrange(3)
            r0 = roots[k]
            lo = (roots[k - 1] + r0) / 2 if k > 0 else r0 - 5
            hi = (roots[k + 1] + r0) / 2 if k < 2 else r0 + 5
            f = lambda x, rs=roots: (x - rs[0]) * (x - rs[1]) * (x - rs[2])
            tol = 1e-10
            r = chandrupatla(f, lo, hi, tol)
            self.assertTrue(r.converged)
            self.assertLessEqual(abs(r.root - r0), tol + 8 * U * abs(r0) + 1e-12 * abs(r0) + 1e-13)
            self.assertLessEqual(r.iterations, math.ceil(2 * (hi - lo) / tol))
            total_c += r.evaluations
            total_b += math.ceil(math.log2((hi - lo) / tol)) + 2
        self.assertLess(total_c, total_b / 2)


if __name__ == "__main__":
    unittest.main()
