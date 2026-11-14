# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-zone-flatness/. The authors are listed in prov/5ZWKK1.jsonl.

import math
import random
import unittest
from fractions import Fraction
from itertools import combinations

from minimum_zone_flatness import (
    convex_hull_3d,
    minimum_zone_flatness,
    minimum_zone_straightness,
)


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def extent(points, n):
    v = [dot(n, p) for p in points]
    return max(v) - min(v)


def brute_width2(points):
    """Minimum over every plane through three points and every direction
    normal to two segments of the extent of the set, with exact arithmetic.
    This candidate set holds every face-vertex and edge-edge normal, and every
    candidate gives a zone that holds all points, so the minimum is the width.
    """
    best = None
    cands = []
    for a, b, c in combinations(points, 3):
        cands.append(cross(sub(b, a), sub(c, a)))
    segs = list(combinations(points, 2))
    for (a, b), (c, d) in combinations(segs, 2):
        cands.append(cross(sub(b, a), sub(d, c)))
    for n in cands:
        if n == (0, 0, 0):
            continue
        w2 = Fraction(extent(points, n) ** 2, dot(n, n))
        if best is None or w2 < best:
            best = w2
    return best


def random_set(rng, n, lo=-5, hi=5):
    return [tuple(rng.randint(lo, hi) for _ in range(3)) for _ in range(n)]


class TestHull(unittest.TestCase):
    def test_hull_is_closed_and_convex(self):
        rng = random.Random(1)
        for _ in range(30):
            pts = list(dict.fromkeys(random_set(rng, 25)))
            fp = [tuple(Fraction(x) for x in p) for p in pts]
            faces = convex_hull_3d(fp)
            self.assertIsNotNone(faces)
            edges = set()
            for a, b, c in faces:
                for e in ((a, b), (b, c), (c, a)):
                    self.assertNotIn(e, edges)
                    edges.add(e)
            for a, b in edges:
                self.assertIn((b, a), edges)
            verts = {i for f in faces for i in f}
            self.assertEqual(len(verts) - len(edges) // 2 + len(faces), 2)
            for a, b, c in faces:
                nrm = cross(sub(fp[b], fp[a]), sub(fp[c], fp[a]))
                self.assertNotEqual(nrm, (0, 0, 0))
                for p in fp:
                    self.assertLessEqual(dot(nrm, sub(p, fp[a])), 0)


class TestFlatness(unittest.TestCase):
    def test_against_brute_force(self):
        rng = random.Random(7)
        for trial in range(40):
            n = rng.randint(4, 10)
            pts = random_set(rng, n)
            z = minimum_zone_flatness(pts)
            self.assertEqual(z.width2, brute_width2(pts), pts)
            for p in pts:
                v = dot(z.normal, p)
                self.assertTrue(z.lo <= v <= z.hi)

    def test_near_planar_sets(self):
        rng = random.Random(11)
        for trial in range(30):
            pts = []
            for _ in range(rng.randint(5, 10)):
                x, y = rng.randint(-6, 6), rng.randint(-6, 6)
                pts.append((x, y, 2 * x - y + rng.randint(0, 2)))
            self.assertEqual(minimum_zone_flatness(pts).width2, brute_width2(pts), pts)

    def test_against_grid_of_normals(self):
        rng = random.Random(5)
        step = math.radians(1.0)
        grid = []
        for i in range(91):
            th = i * step
            for j in range(360):
                ph = j * step
                grid.append((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)))
        for trial in range(4):
            pts = random_set(rng, 9)
            z = minimum_zone_flatness(pts)
            nn = math.sqrt(float(dot(z.normal, z.normal)))
            ustar = tuple(float(c) / nn for c in z.normal)
            if ustar[2] < 0:
                ustar = tuple(-c for c in ustar)
            diam = max(math.dist(p, q) for p, q in combinations(pts, 2))
            gap = min(math.dist(g, ustar) for g in grid)
            best = min(extent(pts, g) for g in grid)
            # Every direction gives a zone at least as wide as the optimum.
            self.assertGreaterEqual(best, z.width - 1e-9)
            # The extent is Lipschitz in the normal with constant diam.
            self.assertLessEqual(best, z.width + diam * gap + 1e-9)

    def test_regular_tetrahedron_needs_edge_edge(self):
        z = minimum_zone_flatness([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)])
        self.assertEqual(z.width2, 1)
        self.assertEqual(z.kind, "edge-edge")

    def test_cube(self):
        cube = [(x, y, z) for x in (0, 2) for y in (0, 2) for z in (0, 2)]
        self.assertEqual(minimum_zone_flatness(cube + [(1, 1, 1)]).width2, 4)

    def test_degenerate(self):
        self.assertEqual(minimum_zone_flatness([(1, 2, 3)]).width2, 0)
        self.assertEqual(minimum_zone_flatness([(0, 0, 0), (1, 1, 1), (2, 2, 2)]).width2, 0)
        z = minimum_zone_flatness([(0, 0, 1), (1, 0, 3), (0, 1, 2), (5, 7, 18)])
        self.assertEqual(z.width2, 0)
        for p in [(0, 0, 1), (5, 7, 18)]:
            self.assertEqual(dot(z.normal, p), z.lo)

    def test_float_input(self):
        z = minimum_zone_flatness([(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 0.5)])
        # The origin is at distance 1/sqrt(6) from the face x + y + 2z = 1.
        self.assertEqual(z.width2, Fraction(1, 6))
        self.assertEqual(z.kind, "face-vertex")


class TestPageExamples(unittest.TestCase):
    def test_tilted_face(self):
        pts = [(0, 0, 0), (2, 0, 2), (0, 2, 0), (2, 2, 2), (1, 1, 2)]
        z = minimum_zone_flatness(pts)
        self.assertEqual(z.width2, Fraction(1, 2))

    def test_vertical_chebyshev_differs(self):
        pts = [(1, 2, 2), (0, 0, 1), (4, 3, 10), (3, 3, 7), (1, 3, 4)]
        z = minimum_zone_flatness(pts)
        self.assertEqual(z.width2, Fraction(81, 170))

        def vertical(a, b):
            r = [p[2] - a * p[0] - b * p[1] for p in pts]
            return max(r) - min(r)

        # The vertical thickness V(a, b) is convex and piecewise linear, so its
        # minimum is at a vertex, where the zone touches the points in a
        # triple or in two pairs. Those planes are among the candidates below.
        vals = {}
        for a3, b3, c3 in combinations(pts, 3):
            n = cross(sub(b3, a3), sub(c3, a3))
            if n[2] != 0:
                vals[(Fraction(-n[0], n[2]), Fraction(-n[1], n[2]))] = None
        for (a2, b2), (c2, d2) in combinations(list(combinations(pts, 2)), 2):
            n = cross(sub(b2, a2), sub(d2, c2))
            if n[2] != 0:
                vals[(Fraction(-n[0], n[2]), Fraction(-n[1], n[2]))] = None
        for ab in vals:
            vals[ab] = vertical(*ab)
        vstar = min(vals.values())
        argmin = [ab for ab, v in vals.items() if v == vstar]
        self.assertEqual(vstar, Fraction(5, 3))
        self.assertEqual(argmin, [(2, Fraction(1, 3))])
        a, b = argmin[0]
        orth = float(vstar) / math.sqrt(1 + a * a + b * b)
        self.assertAlmostEqual(orth, 0.7372, places=4)
        self.assertAlmostEqual(z.width, 0.6903, places=4)
        self.assertGreater(orth, z.width)


class TestStraightness(unittest.TestCase):
    def test_against_brute_force(self):
        rng = random.Random(3)
        for trial in range(60):
            pts = [(rng.randint(-8, 8), rng.randint(-8, 8)) for _ in range(rng.randint(3, 12))]
            w2, nrm, lo, hi = minimum_zone_straightness(pts)
            best = None
            for (ax, ay), (bx, by) in combinations(set(pts), 2):
                n = (ay - by, bx - ax)
                v = [n[0] * x + n[1] * y for x, y in pts]
                c = Fraction((max(v) - min(v)) ** 2, n[0] ** 2 + n[1] ** 2)
                best = c if best is None or c < best else best
            self.assertEqual(w2, best if best is not None else 0, pts)
            for x, y in pts:
                self.assertTrue(lo <= nrm[0] * x + nrm[1] * y <= hi)

    def test_collinear(self):
        self.assertEqual(minimum_zone_straightness([(0, 0), (1, 2), (3, 6)])[0], 0)


class TestScale(unittest.TestCase):
    def test_many_points_on_a_plate(self):
        rng = random.Random(9)
        pts = [(rng.randint(0, 1000), rng.randint(0, 1000), rng.randint(0, 3)) for _ in range(300)]
        z = minimum_zone_flatness(pts)
        self.assertLessEqual(z.width2, 9)
        for p in pts:
            self.assertTrue(z.lo <= dot(z.normal, p) <= z.hi)


if __name__ == "__main__":
    unittest.main()
