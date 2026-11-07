# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/broyden-method/. The authors are listed in prov/MK4APS.jsonl.

import math
import random
import unittest
from fractions import Fraction

from broyden_method import broyden, difference_jacobian, norm, solve


def F_circle(x):
    return [x[0] + x[1] - 3, x[0] ** 2 + x[1] ** 2 - 9]


def J_circle(x):
    return [[1, 1], [2 * x[0], 2 * x[1]]]


def broyden_tridiagonal(x):
    n = len(x)
    out = []
    for i in range(n):
        left = x[i - 1] if i > 0 else 0.0
        right = x[i + 1] if i < n - 1 else 0.0
        out.append((3 - 2 * x[i]) * x[i] - left - 2 * right + 1)
    return out


class TestBroyden(unittest.TestCase):
    def test_example(self):
        r = broyden(F_circle, [1.0, 5.0], J_circle([1.0, 5.0]), tol=1e-15)
        self.assertIn(r.status, ("converged", "exact"))
        self.assertLess(abs(r.x[0]) + abs(r.x[1] - 3), 1e-15)
        self.assertLessEqual(r.evaluations, 9)

    def test_superlinear_ratios(self):
        errs = []
        for k in range(1, 7):
            r = broyden(F_circle, [1.0, 5.0], J_circle([1.0, 5.0]), tol=0, max_iter=k)
            errs.append(max(abs(r.x[0]), abs(r.x[1] - 3)))
        ratios = [b / a for a, b in zip(errs, errs[1:])]
        self.assertLess(ratios[-1], 1e-3)
        self.assertLess(ratios[-1], ratios[-2])
        self.assertLess(ratios[-2], ratios[-3])

    def test_scalar_case_is_secant(self):
        f = lambda x: [x[0] ** 3 - 2 * x[0] - 5]
        x0, x1 = 2.0, 2.0 - f([2.0])[0] / 10.0  # B0 = 10, first step
        r = broyden(f, [x0], [[10.0]], tol=0, max_iter=5)
        a, b = x0, x1
        xs = []
        for _ in range(4):
            fa, fb = f([a])[0], f([b])[0]
            a, b = b, b - fb * (b - a) / (fb - fa)
            xs.append(b)
        r2 = [broyden(f, [x0], [[10.0]], tol=0, max_iter=k).x[0] for k in range(2, 6)]
        for u, v in zip(xs, r2):
            self.assertAlmostEqual(u, v, delta=1e-12)
        self.assertAlmostEqual(r.x[0], 2.0945514815423265, delta=1e-12)

    def test_linear_problem_finishes_in_2n_steps_exactly(self):
        # Gay (1979): on an affine F with nonsingular A, Broyden's method finds the root in at most 2n steps.
        rng = random.Random(5)
        for n in (2, 3, 4):
            A = [[Fraction(rng.randint(-5, 5)) + (8 if i == j else 0) for j in range(n)] for i in range(n)]
            b = [Fraction(rng.randint(-9, 9)) for _ in range(n)]
            F = lambda x: [sum(A[i][j] * x[j] for j in range(n)) - b[i] for i in range(n)]
            B0 = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
            r = broyden(F, [Fraction(0)] * n, B0, tol=0, max_iter=2 * n + 1)
            self.assertEqual(r.status, "exact")
            self.assertLessEqual(r.iterations, 2 * n)

    def test_tridiagonal_with_difference_jacobian(self):
        for n in (5, 20):
            r = broyden(broyden_tridiagonal, [-1.0] * n)
            self.assertEqual(r.status, "converged")
            self.assertLess(norm(broyden_tridiagonal(r.x)), 1e-10)
            self.assertLessEqual(r.evaluations, n + 1 + 30)

    def test_root_at_start(self):
        r = broyden(F_circle, [0.0, 3.0])
        self.assertEqual((r.status, r.iterations, r.evaluations), ("exact", 0, 1))

    def test_singular_matrix(self):
        r = broyden(F_circle, [1.0, 5.0], [[1.0, 1.0], [1.0, 1.0]])
        self.assertEqual((r.status, r.evaluations), ("singular", 1))
        self.assertIsNone(solve([[0.0, 0.0], [0.0, 0.0]], [1.0, 1.0]))

    def test_zero_derivative_start(self):
        # F = (x^2 - 1, y): the Jacobian at x = 0 is singular
        F = lambda x: [x[0] ** 2 - 1, x[1]]
        r = broyden(F, [0.0, 1.0], [[0.0, 0.0], [0.0, 1.0]])
        self.assertEqual(r.status, "singular")

    def test_max_iter_without_root(self):
        F = lambda x: [x[0] ** 2 + 1, x[1]]
        r = broyden(F, [0.5, 0.0], max_iter=25)
        self.assertIn(r.status, ("max-iter", "singular"))
        self.assertLessEqual(r.iterations, 25)
        self.assertLessEqual(r.evaluations, 1 + 2 + 25)

    def test_non_finite_raises(self):
        with self.assertRaises(ArithmeticError):
            broyden(lambda x: [float("nan")], [1.0])
        with self.assertRaises(ArithmeticError):
            broyden(lambda x: [math.inf if x[0] > 1.5 else x[0] - 2], [1.0], [[1e-3]])

    def test_difference_jacobian(self):
        x = [1.0, 2.0]
        J = difference_jacobian(F_circle, x, F_circle(x))
        for row, exact in zip(J, J_circle(x)):
            for a, b in zip(row, exact):
                self.assertAlmostEqual(a, b, delta=1e-6)

    def test_random_problems(self):
        rng = random.Random(20261108)
        bad = 0
        for _ in range(500):
            n = rng.randint(2, 6)
            xs = [rng.uniform(-3, 3) for _ in range(n)]
            A = [[rng.uniform(-1, 1) + (n + 1 if i == j else 0) for j in range(n)] for i in range(n)]

            def F(x, A=A, xs=xs, n=n):
                d = [x[j] - xs[j] for j in range(n)]
                return [sum(A[i][j] * d[j] for j in range(n)) + 0.5 * d[i] * d[i] for i in range(n)]

            x0 = [t + rng.uniform(-0.3, 0.3) for t in xs]
            r = broyden(F, x0, tol=1e-13, max_iter=60)
            if r.status not in ("converged", "exact"):
                bad += 1
                continue
            self.assertLess(max(abs(a - b) for a, b in zip(r.x, xs)), 1e-9)
            self.assertLessEqual(r.iterations, 30)
        self.assertEqual(bad, 0)


if __name__ == "__main__":
    unittest.main()
