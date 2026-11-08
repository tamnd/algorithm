# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radial-basis-function-interpolation/. The authors are listed in prov/QJTKQ6.jsonl.

import math
import random
import unittest
from fractions import Fraction as F

from radial_basis_function_interpolation import KERNELS, rbf_eval, rbf_fit


def natural_spline(xs, ys, t):
    """Independent exact natural cubic spline (second-derivative form)."""
    n = len(xs) - 1
    h = [xs[i + 1] - xs[i] for i in range(n)]
    M = [F(0)] * (n + 1)
    if n >= 2:
        a = [h[i - 1] for i in range(1, n)]
        b = [2 * (h[i - 1] + h[i]) for i in range(1, n)]
        c = [h[i] for i in range(1, n)]
        r = [6 * ((ys[i + 1] - ys[i]) / h[i] - (ys[i] - ys[i - 1]) / h[i - 1])
             for i in range(1, n)]
        m = n - 1
        for i in range(1, m):
            w = a[i] / b[i - 1]
            b[i] -= w * c[i - 1]
            r[i] -= w * r[i - 1]
        sol = [F(0)] * m
        sol[m - 1] = r[m - 1] / b[m - 1]
        for i in range(m - 2, -1, -1):
            sol[i] = (r[i] - c[i] * sol[i + 1]) / b[i]
        M[1:n] = sol
    i = 0
    while i < n - 1 and t > xs[i + 1]:
        i += 1
    if t < xs[0] or t > xs[n]:
        # linear continuation of a natural spline
        k = 0 if t < xs[0] else n
        j = 0 if k == 0 else n - 1
        slope = (ys[j + 1] - ys[j]) / h[j] - h[j] * (2 * M[j] + M[j + 1]) / 6 \
            if k == 0 else (ys[j + 1] - ys[j]) / h[j] + h[j] * (M[j] + 2 * M[j + 1]) / 6
        return ys[k] + slope * (t - xs[k])
    A = (xs[i + 1] - t) / h[i]
    B = (t - xs[i]) / h[i]
    return (A * ys[i] + B * ys[i + 1]
            + ((A ** 3 - A) * M[i] + (B ** 3 - B) * M[i + 1]) * h[i] ** 2 / 6)


def halton(i, b):
    f, r = 1.0, 0.0
    while i > 0:
        f /= b
        r += f * (i % b)
        i //= b
    return r


def franke(x, y):
    return (0.75 * math.exp(-((9 * x - 2) ** 2 + (9 * y - 2) ** 2) / 4)
            + 0.75 * math.exp(-(9 * x + 1) ** 2 / 49 - (9 * y + 1) / 10)
            + 0.5 * math.exp(-((9 * x - 7) ** 2 + (9 * y - 3) ** 2) / 4)
            - 0.2 * math.exp(-(9 * x - 4) ** 2 - (9 * y - 7) ** 2))


class TestRBF(unittest.TestCase):
    def test_interpolates_all_kernels(self):
        rng = random.Random(1)
        for trial in range(60):
            n = rng.randint(4, 25)
            pts = [(rng.random(), rng.random()) for _ in range(n)]
            vals = [rng.uniform(-1, 1) for _ in range(n)]
            kernel = rng.choice(sorted(KERNELS))
            m = rbf_fit(pts, vals, kernel, eps=3.0)
            for p, v in zip(pts, vals):
                self.assertAlmostEqual(rbf_eval(m, p), v, delta=1e-8)

    def test_linear_reproduced(self):
        rng = random.Random(2)
        for trial in range(40):
            n = rng.randint(3, 20)
            pts = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
            a, b, c = rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(-2, 2)
            vals = [a + b * x + c * y for x, y in pts]
            for kernel in ("thin_plate", "cubic"):
                m = rbf_fit(pts, vals, kernel)
                for _ in range(5):
                    x, y = rng.uniform(-2, 2), rng.uniform(-2, 2)
                    self.assertAlmostEqual(rbf_eval(m, (x, y)), a + b * x + c * y, delta=1e-8)

    def test_cubic_1d_is_natural_spline_exact(self):
        rng = random.Random(3)
        for trial in range(30):
            n = rng.randint(2, 9)
            xs = sorted(set(F(rng.randint(-40, 40), rng.randint(1, 6)) for _ in range(n)))
            if len(xs) < 2:
                continue
            ys = [F(rng.randint(-9, 9), rng.randint(1, 4)) for _ in xs]
            m = rbf_fit([(x,) for x in xs], ys, "cubic")
            for _ in range(6):
                t = F(rng.randint(-60, 60), rng.randint(1, 7))
                self.assertEqual(rbf_eval(m, (t,)), natural_spline(xs, ys, t))

    def test_linear_kernel_1d_is_broken_line_exact(self):
        xs = [F(0), F(1), F(3), F(4)]
        ys = [F(2), F(-1), F(5), F(5)]
        m = rbf_fit([(x,) for x in xs], ys, "linear")
        self.assertEqual(rbf_eval(m, (F(1, 2),)), F(1, 2))
        self.assertEqual(rbf_eval(m, (F(2),)), F(2))
        self.assertEqual(rbf_eval(m, (F(7, 2),)), F(5))
        for x, y in zip(xs, ys):
            self.assertEqual(rbf_eval(m, (x,)), y)

    def test_single_and_two_nodes(self):
        m = rbf_fit([(0.3, 0.4)], [2.0], "multiquadric", eps=2.0)
        for p in [(0.3, 0.4), (5.0, -1.0)]:
            self.assertAlmostEqual(rbf_eval(m, p), 2.0, places=12)
        m = rbf_fit([(0.0, 0.0)], [3.0], "gaussian", eps=1.0)
        self.assertAlmostEqual(rbf_eval(m, (1.0, 0.0)), 3.0 * math.exp(-1.0), places=12)
        m = rbf_fit([(F(0),), (F(2),)], [F(1), F(5)], "linear")
        self.assertEqual(rbf_eval(m, (F(1, 2),)), F(2))
        with self.assertRaises(ValueError):
            rbf_fit([(0.0, 0.0)], [1.0], "thin_plate")

    def test_repeated_and_collinear(self):
        with self.assertRaises(ValueError):
            rbf_fit([(0.0, 0.0), (1.0, 0.0), (0.0, 0.0)], [1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            rbf_fit([(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)], [1.0, 2.0, 0.0], "thin_plate")

    def test_gaussian_matrix_positive_definite(self):
        rng = random.Random(4)
        for trial in range(30):
            n = rng.randint(1, 15)
            pts = [(rng.random(), rng.random()) for _ in range(n)]
            A = [[math.exp(-(9.0) * ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2))
                  for q in pts] for p in pts]
            L = [[0.0] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1):
                    s = A[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
                    if i == j:
                        self.assertGreater(s, 0.0)
                        L[i][i] = math.sqrt(s)
                    else:
                        L[i][j] = s / L[j][j]

    def test_jump_and_pole_data(self):
        xs = [i / 10 for i in range(-10, 11)]
        jump = [0.0 if x < 0 else 1.0 for x in xs]
        m = rbf_fit([(x,) for x in xs], jump, "cubic")
        for x, y in zip(xs, jump):
            self.assertAlmostEqual(rbf_eval(m, (x,)), y, delta=1e-10)
        over = max(rbf_eval(m, (k / 1000,)) for k in range(-1000, 1001))
        self.assertGreater(over, 1.0)
        pole = [1 / (x - 1.05) for x in xs]
        m = rbf_fit([(x,) for x in xs], pole, "multiquadric", eps=5.0)
        for x, y in zip(xs, pole):
            self.assertAlmostEqual(rbf_eval(m, (x,)), y, delta=1e-7 * abs(y) + 1e-7)

    def test_convergence_franke(self):
        grid = [(0.05 + 0.9 * i / 9, 0.05 + 0.9 * j / 9) for i in range(10) for j in range(10)]
        errs = []
        for n in (25, 100):
            pts = [(halton(i + 1, 2), halton(i + 1, 3)) for i in range(n)]
            m = rbf_fit(pts, [franke(*p) for p in pts], "thin_plate")
            errs.append(max(abs(rbf_eval(m, g) - franke(*g)) for g in grid))
        self.assertLess(errs[1], errs[0] / 4)

    def test_errors(self):
        with self.assertRaises(ValueError):
            rbf_fit([(0.0,)], [1.0], "sinc")
        with self.assertRaises(ValueError):
            rbf_fit([(0.0,), (1.0,)], [1.0])
        with self.assertRaises(ValueError):
            rbf_fit([], [])


if __name__ == "__main__":
    unittest.main()
