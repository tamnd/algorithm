# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/squared-distance-minimization/. The authors are listed in prov/YVZM72.jsonl.

import random
import unittest
from math import cos, pi, sin, sqrt

from re1lin import solve
from squared_distance_minimization import (Curve, basis_row, energy, frame, sdm_step, sdm_weight,
                                           squared_distance_minimization, squared_distance_model)

CUBIC_U = [0, 0, 0, 0, 0.5, 1, 1, 1, 1]


def lsq_fit(X, t, U, p):
    """Independent least-squares fit for fixed parameters, for the starting curves."""
    rows = [basis_row(U, p, s) for s in t]
    n = len(rows[0])
    A = [[sum(r[i] * r[j] for r in rows) for j in range(n)] for i in range(n)]
    cols = [solve(A, [sum(r[i] * x[c] for r, x in zip(rows, X)) for i in range(n)]) for c in range(2)]
    return [(cols[0][i], cols[1][i]) for i in range(n)]


def chord(X):
    acc = [0.0]
    for a, b in zip(X, X[1:]):
        acc.append(acc[-1] + sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2))
    return [s / acc[-1] for s in acc]


def polyline_distance(curve, q, n=3000):
    """Oracle: nearest sample of a dense polyline, refined by golden section on the true curve."""
    ts = [curve.a + (curve.b - curve.a) * i / n for i in range(n + 1)]

    def dist(t):
        c = curve.point(t)
        return sqrt((c[0] - q[0]) ** 2 + (c[1] - q[1]) ** 2)

    i = min(range(n + 1), key=lambda j: dist(ts[j]))
    lo, hi = ts[max(0, i - 1)], ts[min(n, i + 1)]
    g = (sqrt(5) - 1) / 2
    for _ in range(80):
        a, b = hi - g * (hi - lo), lo + g * (hi - lo)
        if dist(a) <= dist(b):
            hi = b
        else:
            lo = a
    return min(dist(ts[i]), dist((lo + hi) / 2))


def quarter_circle():
    return [(cos(pi / 2 * (k / 20) ** 2), sin(pi / 2 * (k / 20) ** 2)) for k in range(21)]


def nonincreasing(h):
    return all(b <= a for a, b in zip(h, h[1:]))


class TestWorkedExample(unittest.TestCase):
    def test_quarter_circle_from_chord_length(self):
        X = quarter_circle()
        P0 = lsq_fit(X, chord(X), CUBIC_U, 3)
        P, h, steps = squared_distance_minimization(X, P0, CUBIC_U, 3, mu=0.0, iterations=6, tol=0)
        self.assertAlmostEqual(h[0], 6.634e-7, delta=1e-10)
        self.assertLess(h[1], 5e-9)
        self.assertLess(h[-1], 1.6e-9)
        self.assertTrue(nonincreasing(h))
        self.assertEqual(steps, [1.0] * len(steps))
        # the energy agrees with an independent distance computation
        c = Curve(P, CUBIC_U, 3)
        oracle = sum(polyline_distance(c, x) ** 2 for x in X)
        self.assertAlmostEqual(oracle, h[-1], delta=1e-10)


class TestLocalModel(unittest.TestCase):
    def circle_case(self, r, theta, d):
        M = (0.3, -0.2)
        K = (M[0] + r * cos(theta), M[1] + r * sin(theta))
        T = (-sin(theta), cos(theta))
        N = (-cos(theta), -sin(theta))          # T turned left points to the center
        X = (K[0] + d * N[0], K[1] + d * N[1])
        return M, K, T, N, X

    def test_second_order_against_the_circle(self):
        rng = random.Random(1)
        for _ in range(40):
            r = rng.uniform(0.5, 3)
            theta = rng.uniform(0, 2 * pi)
            d = rng.uniform(-3 * r, 0.9 * r)
            M, K, T, N, X = self.circle_case(r, theta, d)
            v = (rng.gauss(0, 1), rng.gauss(0, 1))
            errs = []
            for eps in (1e-2, 5e-3, 2.5e-3):
                y = (X[0] + eps * v[0], X[1] + eps * v[1])
                true = (sqrt((y[0] - M[0]) ** 2 + (y[1] - M[1]) ** 2) - r) ** 2
                errs.append(abs(squared_distance_model(K, T, N, 1 / r, y) - true))
            # third-order error: halving eps divides the error by about 8
            for a, b in zip(errs, errs[1:]):
                self.assertLess(b, a / 5 + 1e-11)
            self.assertLess(errs[0], 1e-4)

    def test_model_is_exact_at_the_point_and_on_the_normal(self):
        M, K, T, N, X = self.circle_case(2.0, 0.7, -0.5)
        self.assertAlmostEqual(squared_distance_model(K, T, N, 0.5, X), 0.25, places=14)
        for s in (-0.3, 0.2, 1.0):
            y = (X[0] + s * N[0], X[1] + s * N[1])
            self.assertAlmostEqual(squared_distance_model(K, T, N, 0.5, y), (0.5 - s) ** 2, places=14)

    def test_weight_and_limits(self):
        self.assertEqual(sdm_weight(0.0, 5.0), 0.0)        # straight curve: tangent distance
        self.assertEqual(sdm_weight(3.0, 0.0), 0.0)        # point on the curve: tangent distance
        self.assertEqual(sdm_weight(1.0, 0.5), 0.0)        # between curve and center: clamped to 0
        self.assertAlmostEqual(sdm_weight(1.0, -1.0), 0.5, places=15)   # d / (d - rho) = -1 / (-1 - 1)
        self.assertGreater(sdm_weight(1.0, -1e9), 1 - 1e-8)            # far away: point distance
        rng = random.Random(2)
        for _ in range(100):
            w = sdm_weight(rng.uniform(-5, 5), rng.uniform(-5, 5))
            self.assertTrue(0.0 <= w < 1.0)

    def test_curvature_of_a_parabola(self):
        c = Curve([(-1, 1), (0, -1), (1, 1)], [0, 0, 0, 1, 1, 1], 2)   # (2t - 1, (2t - 1)^2), y = x^2
        T, N, kappa = frame(c, 0.5)
        self.assertAlmostEqual(kappa, 2.0, places=12)
        self.assertAlmostEqual(T[0], 1.0, places=12)
        self.assertAlmostEqual(N[1], 1.0, places=12)
        T, N, kappa = frame(c, 0.75)                                    # x = 1/2: kappa = 2 / (1 + 1)^(3/2)
        self.assertAlmostEqual(kappa, 2 / 2 ** 1.5, places=12)


class TestNoiseFree(unittest.TestCase):
    def test_the_true_curve_is_a_fixed_point(self):
        rng = random.Random(3)
        U = [0, 0, 0, 0, 1 / 3, 2 / 3, 1, 1, 1, 1]
        for _ in range(5):
            P = [(i + rng.uniform(-0.3, 0.3), rng.uniform(-1, 1)) for i in range(6)]
            c = Curve(P, U, 3)
            X = [c.point(k / 39) for k in range(40)]
            Q = sdm_step(X, P, U, 3, 0.0, 64)
            for a, b in zip(P, Q):
                self.assertAlmostEqual(a[0], b[0], places=8)
                self.assertAlmostEqual(a[1], b[1], places=8)
            self.assertLess(energy(X, P, U, 3), 1e-24)


class TestEdgeCases(unittest.TestCase):
    def test_degree_one_is_rejected(self):
        with self.assertRaises(ValueError):
            Curve([(0, 0), (1, 0)], [0, 0, 1, 1], 1)

    def test_straight_data_needs_damping(self):
        # on a straight curve every weight is 0, so sliding along the line costs nothing
        X = [(0.2 + 0.6 * k / 9, 0.01 * (-1) ** k) for k in range(10)]
        P = [(i / 4, 0.0) for i in range(5)]
        with self.assertRaises(ValueError):
            sdm_step(X, P, CUBIC_U, 3, 0.0, 64)
        with self.assertRaises(ValueError):
            sdm_step(X, P, CUBIC_U, 3, 1e-4, 64)       # second differences do not see the slide
        Q, h, _ = squared_distance_minimization(X, P, CUBIC_U, 3, mu=0.0, iterations=10)
        self.assertTrue(nonincreasing(h))
        self.assertAlmostEqual(h[0], 10 * 1e-4, delta=1e-12)
        self.assertLess(h[-1], h[0])


class TestRandomizedNoisy(unittest.TestCase):
    def test_energy_decreases_every_step(self):
        rng = random.Random(11)
        U = [0, 0, 0, 0, 0.2, 0.4, 0.6, 0.8, 1, 1, 1, 1]
        full = total = 0
        for _ in range(3):
            X = [(cos(1.5 * pi * k / 39) * (1 + 0.3 * cos(3 * pi * k / 39)) + rng.gauss(0, 0.005),
                  sin(1.5 * pi * k / 39) * (1 + 0.3 * cos(3 * pi * k / 39)) + rng.gauss(0, 0.005)) for k in range(40)]
            P0 = lsq_fit(X, [k / 39 for k in range(40)], U, 3)
            P, h, steps = squared_distance_minimization(X, P0, U, 3, mu=1e-6, iterations=8, tol=1e-10)
            self.assertTrue(nonincreasing(h))
            self.assertLess(h[-1], 0.2 * h[0])
            full += sum(1 for a in steps if a == 1.0)
            total += len(steps)
            # the reported energy is the independent squared distance plus the roughness term
            c = Curve(P, U, 3)
            oracle = sum(polyline_distance(c, x, 1500) ** 2 for x in X)
            self.assertAlmostEqual(oracle, energy(X, P, U, 3, 0.0), delta=1e-7)
        # measured: most steps are full steps
        self.assertGreaterEqual(full / total, 0.6)


if __name__ == "__main__":
    unittest.main()
