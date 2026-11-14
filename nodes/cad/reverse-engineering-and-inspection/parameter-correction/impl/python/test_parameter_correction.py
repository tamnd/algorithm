# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parameter-correction/. The authors are listed in prov/RY3SVA.jsonl.

import random
import unittest
from math import cos, pi, sin, sqrt

from parameter_correction import (Curve, basis_row, chord_length_parameters, error, fit_control_points, foot_point,
                                  parameter_correction, sample_table)

CUBIC_U = [0, 0, 0, 0, 0.5, 1, 1, 1, 1]


def cox_de_boor(i, p, U, t):
    """Independent recursive B-spline value, with the right end in the last nonempty span."""
    if p == 0:
        last = max(j for j in range(len(U) - 1) if U[j] < U[j + 1])
        if U[i] <= t < U[i + 1] or (i == last and t == U[i + 1]):
            return 1.0
        return 0.0
    s = 0.0
    if U[i + p] > U[i]:
        s += (t - U[i]) / (U[i + p] - U[i]) * cox_de_boor(i, p - 1, U, t)
    if U[i + p + 1] > U[i + 1]:
        s += (U[i + p + 1] - t) / (U[i + p + 1] - U[i + 1]) * cox_de_boor(i + 1, p - 1, U, t)
    return s


def polyline_distance(curve, q, n=2000):
    """Oracle: the distance from q to a dense polyline through the curve."""
    pts = [curve.point(curve.a + (curve.b - curve.a) * i / n) for i in range(n + 1)]
    best = float("inf")
    for a, b in zip(pts, pts[1:]):
        ab = [y - x for x, y in zip(a, b)]
        aq = [y - x for x, y in zip(a, q)]
        L = sum(v * v for v in ab)
        s = 0.0 if L == 0 else min(1.0, max(0.0, sum(u * v for u, v in zip(ab, aq)) / L))
        best = min(best, sqrt(sum((x + s * u - y) ** 2 for x, u, y in zip(a, ab, q))))
    return best


def orthogonal_error(Q, P, U, p):
    c = Curve(P, U, p)
    return sum(polyline_distance(c, q, 600) ** 2 for q in Q)


def nonincreasing(h, rel=1e-12):
    return all(b <= a + rel * a for a, b in zip(h, h[1:]))


def quarter_circle():
    return [(cos(pi / 2 * (k / 20) ** 2), sin(pi / 2 * (k / 20) ** 2)) for k in range(21)]


class TestWorkedExample(unittest.TestCase):
    def test_quarter_circle_uniform_start(self):
        Q = quarter_circle()
        t0 = [k / 20 for k in range(21)]
        P, t, h = parameter_correction(Q, CUBIC_U, 3, t0, iterations=10, tol=-1)
        self.assertAlmostEqual(h[0], 2.087e-4, delta=1e-7)
        self.assertAlmostEqual(h[1], 6.267e-5, delta=1e-7)
        self.assertTrue(nonincreasing(h))
        self.assertLess(h[-1], 0.2 * h[0])
        # the orthogonal error of the final curve is at most its parametric error
        self.assertLessEqual(orthogonal_error(Q, P, CUBIC_U, 3), h[-1] * (1 + 1e-9))
        self.assertEqual(t[0], 0.0)
        self.assertEqual(t[-1], 1.0)


class TestBSplineParts(unittest.TestCase):
    def test_basis_against_recursion(self):
        rng = random.Random(1)
        for U, p in ((CUBIC_U, 3), ([0, 0, 0, 0.2, 0.7, 1, 1, 1], 2), ([0, 0, 0.3, 0.6, 1, 1], 1)):
            n = len(U) - p - 2
            for t in [rng.random() for _ in range(20)] + [0.0, 1.0, 0.5]:
                row = basis_row(U, p, t)
                for i in range(n + 1):
                    self.assertAlmostEqual(row[i], cox_de_boor(i, p, U, t), places=12)
                self.assertAlmostEqual(sum(row), 1.0, places=12)

    def test_derivative_against_differences(self):
        rng = random.Random(2)
        P = [(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(5)]
        c = Curve(P, CUBIC_U, 3)
        for t in (0.1, 0.3, 0.7, 0.9):
            h = 1e-6
            fd = [(a - b) / (2 * h) for a, b in zip(c.point(t + h), c.point(t - h))]
            sd = [(a - b) / (2 * h) for a, b in zip(c.first(t + h), c.first(t - h))]
            for x, y in zip(fd, c.first(t)):
                self.assertAlmostEqual(x, y, places=6)
            for x, y in zip(sd, c.second(t)):
                self.assertAlmostEqual(x, y, places=5)

    def test_foot_point_is_normal_and_nearest(self):
        rng = random.Random(3)
        for _ in range(20):
            P = [(i + rng.uniform(-0.3, 0.3), rng.uniform(-1, 1)) for i in range(5)]
            c = Curve(P, CUBIC_U, 3)
            q = (rng.uniform(0.5, 3.5), rng.uniform(-1.5, 1.5))
            t = foot_point(c, q, 0.0, sample_table(c, 64))
            e = [a - b for a, b in zip(q, c.point(t))]
            d = sqrt(sum(v * v for v in e))
            self.assertAlmostEqual(d, polyline_distance(c, q), delta=1e-5)
            if 1e-9 < t < 1 - 1e-9:
                tang = c.first(t)
                cosang = sum(a * b for a, b in zip(e, tang)) / (d * sqrt(sum(v * v for v in tang)))
                self.assertLess(abs(cosang), 1e-8)


class TestNoiseFree(unittest.TestCase):
    def test_true_parameters_give_the_true_curve_and_stay(self):
        rng = random.Random(4)
        for _ in range(10):
            P0 = [(i + rng.uniform(-0.3, 0.3), rng.uniform(-1, 1), rng.uniform(-1, 1)) for i in range(5)]
            c0 = Curve(P0, CUBIC_U, 3)
            tau = sorted([0.0, 1.0] + [rng.random() for _ in range(18)])
            Q = [c0.point(x) for x in tau]
            P, t, h = parameter_correction(Q, CUBIC_U, 3, tau, iterations=5, tol=-1)
            for a, b in zip(P, P0):
                for x, y in zip(a, b):
                    self.assertAlmostEqual(x, y, places=9)
            self.assertLess(max(h), 1e-20)
            for x, y in zip(t, tau):
                self.assertAlmostEqual(x, y, places=9)

    def test_chord_start_moves_towards_the_true_curve(self):
        # measured, not proved: from chord-length parameters the error and the
        # distance to the true curve both fall in every trial
        rng = random.Random(5)
        better = 0
        trials = 3
        for _ in range(trials):
            P0 = [(i + rng.uniform(-0.2, 0.2), rng.uniform(-0.5, 0.5)) for i in range(5)]
            c0 = Curve(P0, CUBIC_U, 3)
            tau = sorted([0.0, 1.0] + [rng.random() for _ in range(18)])
            Q = [c0.point(x) for x in tau]
            far = [c0.point(i / 100) for i in range(101)]
            _, _, h0 = parameter_correction(Q, CUBIC_U, 3, None, iterations=0)
            P0fit = fit_control_points(Q, chord_length_parameters(Q), CUBIC_U, 3)
            P, _, h = parameter_correction(Q, CUBIC_U, 3, None, iterations=25, tol=-1)
            self.assertTrue(nonincreasing(h))
            d_start = max(polyline_distance(Curve(P0fit, CUBIC_U, 3), x, 300) for x in far)
            d_end = max(polyline_distance(Curve(P, CUBIC_U, 3), x, 300) for x in far)
            better += h[-1] < h0[0] and d_end < d_start
        self.assertEqual(better, trials)


class TestEdgeCases(unittest.TestCase):
    def test_too_few_points(self):
        with self.assertRaises(ValueError):
            parameter_correction([(0, 0), (1, 1), (2, 0), (3, 1)], CUBIC_U, 3)

    def test_points_in_one_span_only(self):
        with self.assertRaises(ValueError):
            fit_control_points([(k, k * k) for k in range(10)], [k / 30 for k in range(10)], CUBIC_U, 3)

    def test_degree_one_and_exact_data(self):
        U = [0, 0, 0.5, 1, 1]
        Q = [(0, 0), (1, 2), (2, 2), (3, 1), (4, 0)]
        P, t, h = parameter_correction(Q, U, 1, [0, 0.25, 0.5, 0.75, 1], iterations=20)
        self.assertTrue(nonincreasing(h))
        self.assertLessEqual(h[-1], 24 / 35 + 1e-12)
        self.assertAlmostEqual(h[0], 24 / 35, places=12)


class TestRandomizedNoisy(unittest.TestCase):
    def test_error_never_increases_and_bounds_the_orthogonal_error(self):
        rng = random.Random(2026)
        ok_mono = ok_bound = ok_ortho = 0
        trials = 6
        for trial in range(trials):
            m = 25
            Q = []
            for k in range(m):
                s = k / (m - 1)
                Q.append((3 * s + rng.gauss(0, 0.01), sin(3 * s) + 0.3 * s * s + rng.gauss(0, 0.01),
                          0.5 * cos(2 * s) + rng.gauss(0, 0.01)))
            P, t, h = parameter_correction(Q, CUBIC_U, 3, None, iterations=8, tol=-1,
                                           fix_ends=(trial % 2 == 0))
            ok_mono += nonincreasing(h)
            D = orthogonal_error(Q, P, CUBIC_U, 3)
            ok_bound += D <= h[-1] * (1 + 1e-9)
            ok_ortho += error(Q, Curve(P, CUBIC_U, 3), t) == h[-1]
        self.assertEqual(ok_mono, trials)
        self.assertEqual(ok_bound, trials)
        self.assertEqual(ok_ortho, trials)


if __name__ == "__main__":
    unittest.main()
