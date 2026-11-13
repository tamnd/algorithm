# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marching-surface-intersection/. The authors are listed in prov/ZVWZT1.jsonl.

import math
import random
import unittest

from marching_surface_intersection import cylinder, dot, march, norm, plane, scale, sphere, sub

BOX = ((-3.0, -3.0, -3.0), (3.0, 3.0, 3.0))


def dist_to_polyline(x, pts, closed):
    best = math.inf
    n = len(pts)
    for i in range(n if closed else n - 1):
        a, b = pts[i], pts[(i + 1) % n]
        ab = sub(b, a)
        L = dot(ab, ab)
        t = 0.0 if L == 0 else max(0.0, min(1.0, dot(sub(x, a), ab) / L))
        best = min(best, norm(sub(x, (a[0] + t * ab[0], a[1] + t * ab[1], a[2] + t * ab[2]))))
    return best


def sign_change_points(f, g, R, n_theta, n_phi):
    """Brute force: walk a (theta, phi) grid on a sphere f of radius R about the origin
    and return the linear interpolants of the grid edges on which g changes sign."""

    def P(i, j):
        th = 2 * math.pi * i / n_theta
        ph = math.pi * j / n_phi
        return (R * math.sin(ph) * math.cos(th), R * math.sin(ph) * math.sin(th), R * math.cos(ph))

    out = []
    for i in range(n_theta):
        for j in range(n_phi):
            a = P(i, j)
            for b in (P(i + 1, j), P(i, j + 1)):
                ga, gb = g.value(a), g.value(b)
                if (ga < 0) != (gb < 0):
                    s = ga / (ga - gb)
                    out.append(tuple(a[k] + s * (b[k] - a[k]) for k in range(3)))
    return out


class TestMarching(unittest.TestCase):
    def assert_on_both(self, f, g, pts):
        for p in pts:
            self.assertLess(abs(f.value(p)), 1e-10)
            self.assertLess(abs(g.value(p)), 1e-10)

    def test_viviani_curve(self):
        f = sphere((0.0, 0.0, 0.0), 2.0)
        g = cylinder((1.0, 0.0, 0.0), (0.0, 0.0, 1.0), 1.0)
        h = 0.02
        pts, closed = march(f, g, (0.1, 0.0, 1.9), h, BOX)
        self.assertTrue(closed)
        self.assert_on_both(f, g, pts)
        # Closed form: (1 + cos t, sin t, 2 sin(t / 2)) for t in [0, 4 pi).
        for j in range(800):
            t = 4 * math.pi * j / 800
            x = (1 + math.cos(t), math.sin(t), 2 * math.sin(t / 2))
            self.assertLess(dist_to_polyline(x, pts, True), 1e-3)
        # Brute force: every sign change of g on a grid of the sphere is near the trace.
        for x in sign_change_points(f, g, 2.0, 120, 60):
            self.assertLess(dist_to_polyline(x, pts, True), 0.03)
        # The trace passes the double point (2, 0, 0) twice.
        near = [i for i, p in enumerate(pts) if norm(sub(p, (2.0, 0.0, 0.0))) < 2 * h]
        self.assertTrue(near)
        self.assertGreater(max(near) - min(near), len(pts) // 4)

    def test_one_start_point_finds_one_loop(self):
        f = sphere((0.0, 0.0, 0.0), 2.0)
        g = cylinder((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), 1.0)
        pts, closed = march(f, g, (1.0, 0.1, 1.6), 0.05, BOX)
        self.assertTrue(closed)
        self.assert_on_both(f, g, pts)
        for p in pts:
            self.assertAlmostEqual(p[2], math.sqrt(3.0), delta=1e-9)
        # The second loop, at z = -sqrt(3), is far from everything that was traced.
        for j in range(60):
            th = 2 * math.pi * j / 60
            x = (math.cos(th), math.sin(th), -math.sqrt(3.0))
            self.assertGreater(dist_to_polyline(x, pts, True), 3.0)
        # The brute force grid sees both loops.
        found = sign_change_points(f, g, 2.0, 60, 40)
        self.assertTrue(any(x[2] > 1 for x in found))
        self.assertTrue(any(x[2] < -1 for x in found))

    def test_random_sphere_pairs(self):
        rng = random.Random(3)
        for _ in range(15):
            c1 = tuple(rng.uniform(-0.5, 0.5) for _ in range(3))
            u = tuple(rng.gauss(0, 1) for _ in range(3))
            u = scale(1 / norm(u), u)
            r1, r2 = rng.uniform(1.0, 1.5), rng.uniform(0.6, 1.2)
            d = rng.uniform(abs(r1 - r2) + 0.2, r1 + r2 - 0.2)
            c2 = tuple(c1[k] + d * u[k] for k in range(3))
            f, g = sphere(c1, r1), sphere(c2, r2)
            a = (d * d + r1 * r1 - r2 * r2) / (2 * d)
            rho = math.sqrt(r1 * r1 - a * a)
            center = tuple(c1[k] + a * u[k] for k in range(3))
            v = (u[1], -u[0], 0.0) if abs(u[2]) < 0.9 else (0.0, u[2], -u[1])
            v = scale(1 / norm(v), v)
            w = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
            start = tuple(center[k] + rho * v[k] + rng.uniform(-0.03, 0.03) for k in range(3))
            h = 0.03
            pts, closed = march(f, g, start, h, BOX)
            self.assertTrue(closed)
            self.assert_on_both(f, g, pts)
            length = sum(norm(sub(pts[i], pts[i - 1])) for i in range(len(pts)))
            self.assertAlmostEqual(length, 2 * math.pi * rho, delta=2 * h)
            for j in range(100):
                th = 2 * math.pi * j / 100
                x = tuple(center[k] + rho * (math.cos(th) * v[k] + math.sin(th) * w[k]) for k in range(3))
                # A chord of length at most 2h of a circle of radius rho is within (2h)^2 / (8 rho).
                self.assertLess(dist_to_polyline(x, pts, True), h * h / (2 * rho) + 1e-9)

    def test_open_branch_stops_at_the_box(self):
        f = plane((0.0, 0.0, 1.0), 0.0)
        g = cylinder((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), 1.0)
        box = ((-2.0, -2.0, -2.0), (2.0, 2.0, 2.0))
        pts, closed = march(f, g, (0.3, 1.1, 0.1), 0.1, box)
        self.assertFalse(closed)
        self.assert_on_both(f, g, pts)
        xs = sorted(p[0] for p in pts)
        self.assertLess(xs[0], -1.89)
        self.assertGreater(xs[-1], 1.89)
        for p in pts:
            self.assertAlmostEqual(p[1], 1.0, delta=1e-9)

    def test_crossing_of_two_ellipses(self):
        f = cylinder((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), 1.0)
        g = cylinder((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), 1.0)
        pts, closed = march(f, g, (0.05, 1.0, 1.0), 0.05, BOX)
        self.assertTrue(closed)
        self.assert_on_both(f, g, pts)
        # The trace passes the singular points (1, 0, 0) and (-1, 0, 0) on its own ellipse y = z.
        for p in pts:
            self.assertLess(abs(p[1] - p[2]), 1e-9)
        self.assertLess(min(norm(sub(p, (1.0, 0.0, 0.0))) for p in pts), 0.05)
        self.assertLess(min(norm(sub(p, (-1.0, 0.0, 0.0))) for p in pts), 0.05)

    def test_singular_start_is_rejected(self):
        f = sphere((0.0, 0.0, 0.0), 2.0)
        g = cylinder((1.0, 0.0, 0.0), (0.0, 0.0, 1.0), 1.0)
        with self.assertRaises(ValueError):
            march(f, g, (2.0, 0.0, 0.0), 0.02, BOX)


if __name__ == "__main__":
    unittest.main()
