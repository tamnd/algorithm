# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smolyak-sparse-grids/. The authors are listed in prov/Y27RRZ.jsonl.

import math
import random
import unittest
from fractions import Fraction as F

from smolyak_sparse_grids import smolyak_eval, smolyak_fit, sparse_grid_points


def rand_point(rng, d):
    return [F(rng.randint(-99, 99), 100) for _ in range(d)]


class TestSmolyak(unittest.TestCase):
    def test_point_counts(self):
        zero = lambda *x: 0
        self.assertEqual([len(sparse_grid_points(smolyak_fit(zero, 2, L)))
                          for L in range(5)], [1, 5, 13, 29, 65])
        self.assertEqual([len(sparse_grid_points(smolyak_fit(zero, 3, L)))
                          for L in range(4)], [1, 7, 25, 69])
        self.assertEqual(len(sparse_grid_points(smolyak_fit(zero, 10, 2))), 221)

    def test_interpolates_at_grid_points(self):
        for d, L in ((1, 3), (2, 3), (3, 2)):
            f = lambda *x: 1 / (7 + sum((j + 1) * v for j, v in enumerate(x)))
            m = smolyak_fit(f, d, L, family="equispaced")
            for p in sparse_grid_points(m):
                self.assertEqual(smolyak_eval(m, p), f(*p))

    def test_polynomial_exactness(self):
        rng = random.Random(4)
        # d = 2, L = 3: exact on x^a y^b with (a, b) <= (0, 8), (2, 4), (4, 2), (8, 0)
        for a, b in ((0, 8), (2, 4), (4, 2), (8, 0), (1, 3), (3, 1)):
            f = lambda x, y: x ** a * y ** b + 3 * x * y - 2
            m = smolyak_fit(f, 2, 3, family="equispaced")
            for _ in range(5):
                t = rand_point(rng, 2)
                self.assertEqual(smolyak_eval(m, t), f(*t))
        f = lambda x, y: x ** 4 * y ** 4
        m = smolyak_fit(f, 2, 3, family="equispaced")
        t = [F(1, 3), F(2, 7)]
        self.assertNotEqual(smolyak_eval(m, t), f(*t))  # not in the space

    def test_total_degree_three_dimensions(self):
        rng = random.Random(9)
        # L = 2: exact on total degree <= 2, and on x^4, x^2 y, not on x y z
        f = lambda x, y, z: x ** 4 + x * x * y - 3 * z ** 2 + y * z + 7
        m = smolyak_fit(f, 3, 2, family="equispaced")
        for _ in range(5):
            t = rand_point(rng, 3)
            self.assertEqual(smolyak_eval(m, t), f(*t))
        g = lambda x, y, z: x * y * z
        m = smolyak_fit(g, 3, 2, family="equispaced")
        t = [F(1, 2), F(1, 3), F(1, 5)]
        self.assertNotEqual(smolyak_eval(m, t), g(*t))

    def test_level_zero_and_one_dimension(self):
        m = smolyak_fit(lambda x, y: x + y + 4, 2, 0, family="equispaced")
        self.assertEqual(smolyak_eval(m, [F(1, 2), F(-1, 3)]), 4)
        # d = 1 is Lagrange interpolation on 2^L + 1 equispaced points
        g = lambda x: 1 / (2 + x)
        m = smolyak_fit(g, 1, 2, family="equispaced")
        nodes = [F(-1), F(-1, 2), F(0), F(1, 2), F(1)]
        t = F(3, 10)
        ref = 0
        for a in nodes:
            w = 1
            for b in nodes:
                if b != a:
                    w *= (t - b) / (a - b)
            ref += w * g(a)
        self.assertEqual(smolyak_eval(m, [t]), ref)

    def test_chebyshev_accuracy_in_four_dimensions(self):
        f = lambda *x: math.exp(-sum(v * v for v in x) / 2)
        m = smolyak_fit(f, 4, 4)
        self.assertEqual(len(sparse_grid_points(m)), 401)
        rng = random.Random(3)
        err = max(abs(smolyak_eval(m, t) - f(*t))
                  for t in ([rng.uniform(-1, 1) for _ in range(4)]
                            for _ in range(20)))
        self.assertLess(err, 5e-3)

    def test_errors(self):
        f = lambda *x: 0
        with self.assertRaises(ValueError):
            smolyak_fit(f, 0, 1)
        with self.assertRaises(ValueError):
            smolyak_fit(f, 2, -1)
        with self.assertRaises(ValueError):
            smolyak_fit(f, 2, 1, family="halton")
        with self.assertRaises(ValueError):
            smolyak_eval(smolyak_fit(f, 2, 1), [0.0])


if __name__ == "__main__":
    unittest.main()
