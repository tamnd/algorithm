# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rolling-ball-blend/. The authors are listed in prov/DRVDD3.jsonl.

import math
import random
import unittest
from fractions import Fraction

from rolling_ball_blend import Cylinder, Plane, cross, dot, norm, rolling_ball_blend, scale, sub, unit

F = Fraction
TOL = 1e-9


def solve3(rows, rhs):
    """Exact Cramer's rule for a 3 by 3 system with Fraction entries."""

    def det(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

    d = det(rows)
    out = []
    for j in range(3):
        m = [[rhs[i] if c == j else rows[i][c] for c in range(3)] for i in range(3)]
        out.append(det(m) / d)
    return out


def plane_plane_spine(n1, d1, s1, n2, d2, s2, r, t, along):
    """Closed form: the point c with n_i . c = d_i + s_i r and t . c = along, exactly."""
    return solve3([list(n1), list(n2), list(t)], [d1 + s1 * r, d2 + s2 * r, along])


class Checks:
    def check_sections(self, s1, s2, r, sides, spine, sections):
        for c, (p1, p2, arc) in zip(spine, sections):
            self.assertAlmostEqual(s1.sd(c), sides[0] * r, delta=1e-12)
            self.assertAlmostEqual(s2.sd(c), sides[1] * r, delta=1e-12)
            t = unit(cross(s1.normal(c), s2.normal(c)))
            for surface, p, s in ((s1, p1, sides[0]), (s2, p2, sides[1])):
                self.assertLess(abs(surface.sd(p)), TOL)  # the contact is on the surface
                g = scale(1.0 / r, sub(c, p))
                n = scale(s, surface.normal(p))
                self.assertLess(norm(sub(g, n)), TOL)  # the same tangent plane, G1
            total = math.acos(max(-1.0, min(1.0, dot(sub(p1, c), sub(p2, c)) / r ** 2)))
            self.assertLess(total, math.pi)  # the shorter arc
            for x in arc:
                self.assertAlmostEqual(norm(sub(x, c)), r, delta=TOL)
                self.assertLess(abs(dot(sub(x, c), t)), TOL)  # in the normal plane of the spine
                a1 = math.acos(max(-1.0, min(1.0, dot(sub(x, c), sub(p1, c)) / r ** 2)))
                a2 = math.acos(max(-1.0, min(1.0, dot(sub(x, c), sub(p2, c)) / r ** 2)))
                self.assertAlmostEqual(a1 + a2, total, delta=1e-7)


class TestRollingBallBlend(unittest.TestCase, Checks):
    def test_two_planes_against_closed_form(self):
        r = F(1, 2)
        n1, d1 = (F(0), F(0), F(1)), F(0)
        n2, d2 = (F(3, 5), F(0), F(-4, 5)), F(0)
        p1 = Plane(tuple(map(float, n1)), float(d1))
        p2 = Plane(tuple(map(float, n2)), float(d2))
        spine, sections, closed = rolling_ball_blend(p1, p2, float(r), (1, 1), (2.0, 0.0, 1.0), 0.1, 30)
        self.assertFalse(closed)
        t = (F(0), F(1), F(0))
        for c in spine:
            exact = plane_plane_spine(n1, d1, 1, n2, d2, 1, r, t, F(c[1]))
            self.assertLess(norm(sub(c, tuple(map(float, exact)))), 1e-12)
            self.assertEqual(exact[0], F(3, 2))
            self.assertEqual(exact[2], F(1, 2))
        self.check_sections(p1, p2, float(r), (1, 1), spine, sections)
        q1, q2, _ = sections[0]
        self.assertAlmostEqual(q2[0], 1.2, delta=1e-12)
        self.assertAlmostEqual(q2[2], 0.9, delta=1e-12)

    def test_round_of_a_convex_edge(self):
        # Solid x >= 0, y >= 0 with outward normals (-1, 0, 0) and (0, -1, 0); the ball is inside.
        r = 0.25
        a, b = Plane((-1, 0, 0), 0.0), Plane((0, -1, 0), 0.0)
        spine, sections, _ = rolling_ball_blend(a, b, r, (-1, -1), (0.3, 0.2, 0.0), 0.05, 20)
        for c, (p1, p2, arc) in zip(spine, sections):
            self.assertAlmostEqual(c[0], r, delta=1e-12)
            self.assertAlmostEqual(c[1], r, delta=1e-12)
            for x in arc:
                self.assertLessEqual(x[0], r + 1e-12)
                self.assertLessEqual(x[1], r + 1e-12)
        self.check_sections(a, b, r, (-1, -1), spine, sections)

    def test_random_plane_pairs(self):
        rng = random.Random(7)
        triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]
        for _ in range(40):
            p, q, h = rng.choice(triples)
            ang = rng.choice([(p, q), (q, p), (-p, q), (p, -q)])
            n1 = (F(0), F(0), F(1))
            n2 = (F(ang[0], h), F(0), F(ang[1], h))
            if abs(n2[2]) == 1 or n2[0] == 0:
                continue
            d1, d2 = F(rng.randint(-3, 3), 2), F(rng.randint(-3, 3), 2)
            r = F(rng.randint(1, 4), 4)
            sides = (rng.choice((1, -1)), rng.choice((1, -1)))
            t = (F(0), F(1), F(0))
            exact = plane_plane_spine(n1, d1, sides[0], n2, d2, sides[1], r, t, F(0))
            start = tuple(float(v) + rng.uniform(-0.2, 0.2) for v in exact)
            pl1 = Plane(tuple(map(float, n1)), float(d1))
            pl2 = Plane(tuple(map(float, n2)), float(d2))
            spine, sections, _ = rolling_ball_blend(pl1, pl2, float(r), sides, start, 0.1, 10)
            for c in spine:
                e = plane_plane_spine(n1, d1, sides[0], n2, d2, sides[1], r, t, F(c[1]))
                self.assertLess(norm(sub(c, tuple(map(float, e)))), 1e-11)
            self.check_sections(pl1, pl2, float(r), sides, spine, sections)

    def test_plane_and_cylinder_gives_a_torus(self):
        R, r = 1.0, 0.5
        floor = Plane((0, 0, 1), 0.0)
        shaft = Cylinder((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), R)
        spine, sections, closed = rolling_ball_blend(floor, shaft, r, (1, 1), (1.7, 0.1, 0.6), 0.05, 1000)
        self.assertTrue(closed)
        self.assertAlmostEqual(len(spine) * 0.05, 2 * math.pi * (R + r), delta=0.1)
        for c in spine:
            self.assertAlmostEqual(math.hypot(c[0], c[1]), R + r, delta=1e-12)
            self.assertAlmostEqual(c[2], r, delta=1e-12)
        for _, _, arc in sections:
            for x in arc:
                rho = math.hypot(x[0], x[1])
                self.assertAlmostEqual((rho - (R + r)) ** 2 + (x[2] - r) ** 2, r * r, delta=1e-9)
                self.assertLessEqual(rho, R + r + 1e-12)  # the quarter of the tube in the corner
                self.assertLessEqual(x[2], r + 1e-12)
        self.check_sections(floor, shaft, r, (1, 1), spine, sections)

        # Brute force: sample the two faces densely; no sample is closer than r to a ball center.
        samples = []
        for i in range(90):
            th = 2 * math.pi * i / 90
            for j in range(15):
                z = 0.1 * j
                samples.append((R * math.cos(th), R * math.sin(th), z))
                rho = R + 0.1 * j
                samples.append((rho * math.cos(th), rho * math.sin(th), 0.0))
        for c in spine[::10]:
            dmin = min(norm(sub(c, s)) for s in samples)
            self.assertGreaterEqual(dmin, r - 1e-12)
            self.assertLess(dmin, r + 0.05)

        # Brute force envelope test: no arc point lies inside the ball at another spine point.
        for _, _, arc in sections[::7]:
            for x in arc:
                self.assertGreaterEqual(min(norm(sub(x, c)) for c in spine), r - 1e-9)

    def test_two_parallel_cylinders(self):
        r = 0.5
        big = Cylinder((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), 1.0)
        small = Cylinder((1.2, 0.0, 0.0), (0.0, 0.0, 1.0), 0.5)
        # Closed form: the center is at distance 1.5 from the first axis and 1.0 from the second.
        d, ra, rb = 1.2, 1.5, 1.0
        x0 = (d * d + ra * ra - rb * rb) / (2 * d)
        y0 = math.sqrt(ra * ra - x0 * x0)
        for sign in (1, -1):
            spine, sections, closed = rolling_ball_blend(big, small, r, (1, 1), (1.0, sign * 1.2, 0.0), 0.1, 15)
            self.assertFalse(closed)
            for c in spine:
                self.assertAlmostEqual(c[0], x0, delta=1e-12)
                self.assertAlmostEqual(c[1], sign * y0, delta=1e-12)
            self.check_sections(big, small, r, (1, 1), spine, sections)
            for _, _, arc in sections:
                for x in arc:
                    self.assertGreaterEqual(big.sd(x), -1e-12)
                    self.assertGreaterEqual(small.sd(x), -1e-12)

    def test_parallel_planes_are_rejected(self):
        a, b = Plane((0, 0, 1), 0.0), Plane((0, 0, 1), 1.0)
        with self.assertRaises(ValueError):
            rolling_ball_blend(a, b, 0.5, (1, -1), (0.0, 0.0, 0.5), 0.1, 5)


if __name__ == "__main__":
    unittest.main()
