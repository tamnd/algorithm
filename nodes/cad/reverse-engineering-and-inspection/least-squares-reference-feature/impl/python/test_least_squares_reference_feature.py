# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-squares-reference-feature/. The authors are listed in prov/5ETC50.jsonl.

import math
import random
import unittest
from fractions import Fraction
from itertools import combinations

from least_squares_reference_feature import (
    kasa_start,
    ls_circle,
    ls_line,
    ls_plane,
    zone_width,
)


def unit(v):
    n = math.sqrt(sum(x * x for x in v))
    return tuple(x / n for x in v)


def smallest_eigenvalue_3x3(m):
    """Closed form of the smallest eigenvalue of a symmetric 3x3 matrix
    (the trigonometric solution of the characteristic cubic)."""
    p1 = m[0][1] ** 2 + m[0][2] ** 2 + m[1][2] ** 2
    q = (m[0][0] + m[1][1] + m[2][2]) / 3.0
    p2 = sum((m[i][i] - q) ** 2 for i in range(3)) + 2 * p1
    p = math.sqrt(p2 / 6.0)
    b = [[(m[i][j] - (q if i == j else 0.0)) / p for j in range(3)] for i in range(3)]
    detb = (
        b[0][0] * (b[1][1] * b[2][2] - b[1][2] * b[2][1])
        - b[0][1] * (b[1][0] * b[2][2] - b[1][2] * b[2][0])
        + b[0][2] * (b[1][0] * b[2][1] - b[1][1] * b[2][0])
    )
    r = max(-1.0, min(1.0, detb / 2.0))
    phi = math.acos(r) / 3.0
    return q + 2 * p * math.cos(phi + 2 * math.pi / 3)


def plane_cost(points, n):
    c = [sum(p[k] for p in points) / len(points) for k in range(3)]
    return sum(sum(n[k] * (p[k] - c[k]) for k in range(3)) ** 2 for p in points)


def circle_cost(points, a, b, r):
    return sum((math.hypot(x - a, y - b) - r) ** 2 for x, y in points)


def brute_flatness2(points):
    def sub(a, b):
        return tuple(x - y for x, y in zip(a, b))

    def cross(a, b):
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

    best = None
    cands = [cross(sub(b, a), sub(c, a)) for a, b, c in combinations(points, 3)]
    segs = list(combinations(points, 2))
    cands += [cross(sub(b, a), sub(d, c)) for (a, b), (c, d) in combinations(segs, 2)]
    for n in cands:
        if n == (0, 0, 0):
            continue
        v = [sum(x * y for x, y in zip(n, p)) for p in points]
        w2 = Fraction((max(v) - min(v)) ** 2, sum(x * x for x in n))
        best = w2 if best is None or w2 < best else best
    return best


def brute_roundness(points):
    """Minimum width annulus: the best center is equidistant from two pairs of
    points (a vertex of the nearest or farthest point Voronoi diagram, or a
    crossing of their edges), so it is a crossing of two bisectors."""
    best = math.inf
    pairs = list(combinations(points, 2))
    for (p, q), (r, s) in combinations(pairs, 2):
        # Bisector of p, q: 2 (q - p) . c = |q|^2 - |p|^2.
        a1, b1 = 2 * (q[0] - p[0]), 2 * (q[1] - p[1])
        c1 = q[0] ** 2 + q[1] ** 2 - p[0] ** 2 - p[1] ** 2
        a2, b2 = 2 * (s[0] - r[0]), 2 * (s[1] - r[1])
        c2 = s[0] ** 2 + s[1] ** 2 - r[0] ** 2 - r[1] ** 2
        det = a1 * b2 - a2 * b1
        if det == 0:
            continue
        cx = Fraction(c1 * b2 - c2 * b1, det)
        cy = Fraction(a1 * c2 - a2 * c1, det)
        d = [math.hypot(x - cx, y - cy) for x, y in points]
        best = min(best, max(d) - min(d))
    return best


class TestPlane(unittest.TestCase):
    def test_noise_free_plane(self):
        rng = random.Random(1)
        for _ in range(50):
            n = unit((rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)))
            off = rng.uniform(-5, 5)
            pts = []
            for _ in range(rng.randint(3, 30)):
                p = [rng.uniform(-10, 10) for _ in range(3)]
                t = sum(n[k] * p[k] for k in range(3)) - off
                pts.append(tuple(p[k] - t * n[k] for k in range(3)))
            if len(pts) == 3:
                pts.append(tuple((pts[0][k] + pts[1][k]) / 2 for k in range(3)))
            c, m, dev, ss = ls_plane(pts)
            self.assertAlmostEqual(abs(sum(m[k] * n[k] for k in range(3))), 1.0, places=9)
            self.assertLess(max(abs(e) for e in dev), 1e-9)

    def test_smallest_eigenvalue_closed_form(self):
        rng = random.Random(2)
        for _ in range(50):
            pts = [tuple(rng.gauss(0, s) for s in (3.0, 2.0, 0.3)) for _ in range(40)]
            c, n, dev, ss = ls_plane(pts)
            cov = [[sum((p[i] - c[i]) * (p[j] - c[j]) for p in pts) for j in range(3)] for i in range(3)]
            self.assertAlmostEqual(ss, smallest_eigenvalue_3x3(cov), delta=1e-9 * (1 + ss))
            # No other normal does better.
            for _ in range(20):
                other = unit(tuple(n[k] + rng.gauss(0, 0.05) for k in range(3)))
                self.assertGreaterEqual(plane_cost(pts, other), ss - 1e-9)

    def test_zone_never_narrower_than_minimum_zone(self):
        rng = random.Random(3)
        for _ in range(40):
            pts = [(rng.randint(-5, 5), rng.randint(-5, 5), rng.randint(-1, 1)) for _ in range(8)]
            w2 = brute_flatness2(pts)
            if w2 is None:
                continue
            c, n, dev, ss = ls_plane([tuple(map(float, p)) for p in pts])
            self.assertGreaterEqual(zone_width(dev), math.sqrt(w2) - 1e-9)


class TestLine(unittest.TestCase):
    def test_closed_form_angle(self):
        rng = random.Random(4)
        for _ in range(50):
            pts = [(rng.gauss(0, 3), rng.gauss(0, 1)) for _ in range(20)]
            c, u, dev = ls_line(pts)
            sxx = sum((x - c[0]) ** 2 for x, y in pts)
            syy = sum((y - c[1]) ** 2 for x, y in pts)
            sxy = sum((x - c[0]) * (y - c[1]) for x, y in pts)
            th = 0.5 * math.atan2(2 * sxy, sxx - syy)
            self.assertAlmostEqual(abs(u[0] * math.cos(th) + u[1] * math.sin(th)), 1.0, places=9)

    def test_page_example(self):
        pts = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 1)]
        c, u, dev = ls_line(pts)
        self.assertAlmostEqual(zone_width(dev), 0.7754, places=4)
        self.assertAlmostEqual(u[1] / u[0], 0.2080, places=4)
        self.assertGreater(zone_width(dev), 3 / math.sqrt(17))

    def test_line_in_space(self):
        pts = [(1 + 2 * t, -1 + t, 3 - 2 * t) for t in (-2, -0.5, 0, 1.5, 4)]
        c, u, dev = ls_line(pts)
        self.assertLess(max(dev), 1e-9)
        self.assertAlmostEqual(abs(u[0] * 2 + u[1] - u[2] * 2) / 3, 1.0, places=9)


class TestCircle(unittest.TestCase):
    def test_noise_free_circles_and_arcs(self):
        rng = random.Random(5)
        for _ in range(60):
            a, b, r = rng.uniform(-5, 5), rng.uniform(-5, 5), rng.uniform(0.5, 10)
            t0, span = rng.uniform(0, 2 * math.pi), rng.choice([0.3, 1.0, 3.0, 2 * math.pi])
            pts = [(a + r * math.cos(t0 + span * i / 9), b + r * math.sin(t0 + span * i / 9)) for i in range(10)]
            (ka, kb), kr = kasa_start(pts)
            (ca, cb), cr, dev, ss = ls_circle(pts)
            for got in ((ka, kb, kr), (ca, cb, cr)):
                self.assertAlmostEqual(got[0], a, delta=1e-6 * (1 + r))
                self.assertAlmostEqual(got[1], b, delta=1e-6 * (1 + r))
                self.assertAlmostEqual(got[2], r, delta=1e-6 * (1 + r))

    def test_noisy_arc_is_a_minimum(self):
        rng = random.Random(6)
        for _ in range(30):
            pts = []
            for i in range(30):
                t = 0.8 * i / 29
                rho = 1 + rng.gauss(0, 0.01)
                pts.append((rho * math.cos(t), rho * math.sin(t)))
            (ka, kb), kr = kasa_start(pts)
            (a, b), r, dev, ss = ls_circle(pts)
            self.assertLessEqual(ss, circle_cost(pts, ka, kb, kr) + 1e-15)
            for _ in range(20):
                da, db, dr = (rng.gauss(0, 1e-3) for _ in range(3))
                self.assertGreaterEqual(circle_cost(pts, a + da, b + db, r + dr), ss - 1e-12)
            # At a minimum the mean deviation is zero (the derivative in r).
            self.assertAlmostEqual(sum(dev), 0.0, delta=1e-8)

    def test_short_arc_example(self):
        # The example of the circle fitting page: seven points every 10
        # degrees on a 60 degree arc of the unit circle, moved radially by
        # -0.02 and +0.02 in turn.
        pts = []
        for k in range(7):
            t = math.radians(10 * k)
            rho = 1 + (0.02 if k % 2 else -0.02)
            pts.append((rho * math.cos(t), rho * math.sin(t)))
        (ka, kb), kr = kasa_start(pts)
        (a, b), r, dev, ss = ls_circle(pts)
        self.assertAlmostEqual(kr, 0.8141, places=4)
        self.assertAlmostEqual(r, 0.8909, places=4)
        self.assertLess(ss, circle_cost(pts, ka, kb, kr))
        self.assertLess(ss, circle_cost(pts, 0.0, 0.0, 1.0))

    def test_zone_never_narrower_than_minimum_zone(self):
        rng = random.Random(7)
        for _ in range(30):
            pts = []
            for i in range(7):
                t = 2 * math.pi * i / 7
                rho = 20 + rng.randint(-2, 2)
                pts.append((round(rho * math.cos(t)), round(rho * math.sin(t))))
            pts = list(dict.fromkeys(pts))
            (a, b), r, dev, ss = ls_circle([tuple(map(float, p)) for p in pts])
            self.assertGreaterEqual(zone_width(dev), brute_roundness(pts) - 1e-9)


if __name__ == "__main__":
    unittest.main()
