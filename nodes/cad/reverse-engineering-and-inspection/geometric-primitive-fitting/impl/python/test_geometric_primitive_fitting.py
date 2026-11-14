# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometric-primitive-fitting/. The authors are listed in prov/8FSGZT.jsonl.

import random
import unittest
from fractions import Fraction as F
from math import cos, pi, sin, sqrt

from geometric_primitive_fitting import (algebraic_sphere, cylinder_distance, fit_cylinder, fit_sphere,
                                         sphere_distance)
from re1lin import solve


def rational_unit_vector(a, b):
    """Inverse stereographic projection of the rational point (a, b): a rational point of the unit sphere."""
    a, b = F(a), F(b)
    s = a * a + b * b + 1
    return (2 * a / s, 2 * b / s, (a * a + b * b - 1) / s)


def rational_frame(q):
    """The rotation matrix of the integer quaternion q, with rational entries; its columns are orthonormal."""
    a, b, c, d = q
    s = F(a * a + b * b + c * c + d * d)
    R = [[a * a + b * b - c * c - d * d, 2 * (b * c - a * d), 2 * (b * d + a * c)],
         [2 * (b * c + a * d), a * a - b * b + c * c - d * d, 2 * (c * d - a * b)],
         [2 * (b * d - a * c), 2 * (c * d + a * b), a * a - b * b - c * c + d * d]]
    cols = [tuple(R[i][j] / s for i in range(3)) for j in range(3)]
    return cols


def unit_circle(s):
    s = F(s)
    return (1 - s * s) / (1 + s * s), 2 * s / (1 + s * s)


def dist2_to_axis(x, p, u):
    w = [a - b for a, b in zip(x, p)]
    h = sum(a * b for a, b in zip(w, u))
    return sum(a * a for a in w) - h * h


def strictly_decreasing(h):
    return all(b < a for a, b in zip(h, h[1:]))


class TestWorkedExamples(unittest.TestCase):
    def test_noise_free_sphere_start_is_exact(self):
        c, r = (F(1), F(-2), F(1, 2)), F(3)
        pts = [tuple(ci + r * vi for ci, vi in zip(c, rational_unit_vector(a, b)))
               for a, b in [(0, 0), (F(1, 2), 0), (0, F(1, 3)), (F(-1, 4), F(1, 5)), (F(2, 7), F(-1, 3)), (1, 1)]]
        for x in pts:
            self.assertEqual(sum((a - b) ** 2 for a, b in zip(x, c)), r * r)
        # the algebraic system, solved exactly with fractions, gives the true sphere (Theorem 2)
        rows = [tuple(x) + (1,) for x in pts]
        A = [[sum(u[i] * u[j] for u in rows) for j in range(4)] for i in range(4)]
        rhs = [-sum(u[i] * sum(v * v for v in x) for u, x in zip(rows, pts)) for i in range(4)]
        s = solve(A, rhs)
        self.assertEqual([-v / 2 for v in s[:3]], list(c))
        self.assertEqual(sum(v * v for v in c) - s[3], r * r)
        gc, gr, hist = fit_sphere(pts)
        for a, b in zip(gc, c):
            self.assertAlmostEqual(a, float(b), places=10)
        self.assertAlmostEqual(gr, 3, places=10)
        self.assertLess(hist[-1], 1e-24)

    def test_circle_in_the_plane(self):
        pts = [(5 + 2 * x, -1 + 2 * y) for x, y in map(unit_circle, [0, F(1, 4), F(1, 3), F(1, 2)])]
        c, r, _ = fit_sphere(pts)
        self.assertAlmostEqual(c[0], 5, places=10)
        self.assertAlmostEqual(c[1], -1, places=10)
        self.assertAlmostEqual(r, 2, places=10)


class TestNoiseFree(unittest.TestCase):
    def test_random_sphere_caps(self):
        rng = random.Random(1)
        for _ in range(30):
            c = tuple(F(rng.randint(-20, 20), rng.randint(1, 4)) for _ in range(3))
            r = F(rng.randint(1, 30), rng.randint(1, 3))
            pts = [tuple(ci + r * vi for ci, vi in zip(c, rational_unit_vector(F(rng.randint(-20, 20), 50),
                                                                              F(rng.randint(-20, 20), 50))))
                   for _ in range(12)]
            gc, gr, hist = fit_sphere(pts)
            self.assertTrue(strictly_decreasing(hist))
            for a, b in zip(gc, c):
                self.assertAlmostEqual(a, float(b), delta=1e-8 * float(r))
            self.assertAlmostEqual(gr, float(r), delta=1e-8 * float(r))

    def test_random_cylinders(self):
        rng = random.Random(2)
        quats = [(1, 2, 3, 4), (2, -1, 0, 3), (5, 1, -2, 1), (1, 0, 0, 0), (3, 3, -1, 2), (0, 1, 2, -2)]
        for trial in range(12):
            u, e1, e2 = rational_frame(quats[trial % len(quats)] if trial < 6 else
                                       tuple(rng.randint(-5, 5) or 1 for _ in range(4)))
            p = tuple(F(rng.randint(-10, 10)) for _ in range(3))
            r = F(rng.randint(2, 20), rng.randint(1, 4))
            pts = []
            for _ in range(30):
                cs, sn = unit_circle(F(rng.randint(-30, 30), 20))
                t = F(rng.randint(-40, 40), 10)
                pts.append(tuple(pi_ + r * (cs * a + sn * b) + t * c for pi_, a, b, c in zip(p, e1, e2, u)))
            for x in pts:
                self.assertEqual(dist2_to_axis(x, p, u), r * r)
            normals = None if trial % 2 == 0 else [
                tuple(float(v) for v in [(xi - pi_) - sum((xj - pj) * uj for xj, pj, uj in zip(x, p, u)) * ui
                                         for xi, pi_, ui in zip(x, p, u)]) for x in pts]
            gp, gu, gr, hist = fit_cylinder(pts, normals)
            self.assertTrue(strictly_decreasing(hist))
            fu = [float(v) for v in u]
            self.assertGreater(abs(sum(a * b for a, b in zip(gu, fu))), 1 - 1e-12)
            self.assertAlmostEqual(gr, float(r), delta=1e-8 * float(r))
            self.assertLess(sqrt(max(0.0, dist2_to_axis(gp, [float(v) for v in p], fu))), 1e-8 * float(r))


class TestDistances(unittest.TestCase):
    def test_cylinder_distance_against_brute_force(self):
        rng = random.Random(3)
        for _ in range(30):
            x = tuple(rng.uniform(-3, 3) for _ in range(3))
            # cylinder: axis z through (1, 0, 0), radius 1; brute force over a fine grid of the surface near x
            best = min(sqrt((x[0] - 1 - cos(t)) ** 2 + (x[1] - sin(t)) ** 2)
                       for t in (2 * pi * k / 20000 for k in range(20000)))
            self.assertAlmostEqual(abs(cylinder_distance((1, 0, 0), (0, 0, 1), 1, x)), best, places=6)

    def test_sphere_distance(self):
        self.assertEqual(sphere_distance((0, 0, 0), 1, (0, 0, 3)), 2)
        self.assertEqual(sphere_distance((0, 0, 0), 2, (0, 1, 0)), -1)


class TestEdgeCases(unittest.TestCase):
    def test_too_few_points(self):
        with self.assertRaises(ValueError):
            fit_sphere([(0, 0, 0), (1, 0, 0), (0, 1, 0)])
        with self.assertRaises(ValueError):
            fit_cylinder([(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)])

    def test_coplanar_points_have_no_sphere(self):
        with self.assertRaises(ValueError):
            algebraic_sphere([(1, 0, 0), (0, 1, 0), (-1, 0, 0), (0, -1, 0), (F(3, 5), F(4, 5), 0)])


class TestRandomizedNoisy(unittest.TestCase):
    def cost_sphere(self, pts, c, r):
        return sum((sqrt(sum((a - b) ** 2 for a, b in zip(x, c))) - r) ** 2 for x in pts)

    def test_sphere_local_minimum_and_better_than_truth(self):
        rng = random.Random(2026)
        for _ in range(20):
            pts = []
            for _ in range(40):
                z = rng.uniform(0.5, 1)
                ph = rng.uniform(0, 2 * pi)
                s = sqrt(1 - z * z)
                pts.append((s * cos(ph) + rng.gauss(0, 0.02), s * sin(ph) + rng.gauss(0, 0.02),
                            z + rng.gauss(0, 0.02)))
            c, r, hist = fit_sphere(pts)
            self.assertTrue(strictly_decreasing(hist))
            best = self.cost_sphere(pts, c, r)
            self.assertAlmostEqual(best, hist[-1], delta=1e-12)
            self.assertLessEqual(best, self.cost_sphere(pts, (0, 0, 0), 1) + 1e-15)
            ac, ar = algebraic_sphere(pts)
            self.assertLessEqual(best, self.cost_sphere(pts, ac, ar) + 1e-15)
            for _ in range(100):
                dc = tuple(v + rng.gauss(0, 1e-3) for v in c)
                self.assertLessEqual(best, self.cost_sphere(pts, dc, r + rng.gauss(0, 1e-3)) + 1e-15)
            # the gradient of the independent cost function vanishes (central differences)
            for k in range(4):
                th = list(c) + [r]
                hi, lo = list(th), list(th)
                hi[k] += 1e-6
                lo[k] -= 1e-6
                g = (self.cost_sphere(pts, hi[:3], hi[3]) - self.cost_sphere(pts, lo[:3], lo[3])) / 2e-6
                self.assertLess(abs(g), 1e-6)

    def test_cylinder_noisy_close_to_truth(self):
        rng = random.Random(5)
        for _ in range(6):
            pts = []
            for _ in range(60):
                t, h = rng.uniform(0, pi), rng.uniform(0, 3)
                pts.append((2 * cos(t) + rng.gauss(0, 0.01), 2 * sin(t) + rng.gauss(0, 0.01), h + rng.gauss(0, 0.01)))
            p, u, r, hist = fit_cylinder(pts)
            self.assertTrue(strictly_decreasing(hist))
            self.assertGreater(abs(u[2]), cos(pi / 180))
            self.assertAlmostEqual(r, 2, delta=0.02)
            cost = sum(cylinder_distance(p, u, r, x) ** 2 for x in pts)
            truth = sum(cylinder_distance((0, 0, 0), (0, 0, 1), 2, x) ** 2 for x in pts)
            self.assertLessEqual(cost, truth + 1e-15)


if __name__ == "__main__":
    unittest.main()
