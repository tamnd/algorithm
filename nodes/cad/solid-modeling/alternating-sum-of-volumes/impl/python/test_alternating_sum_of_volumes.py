# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alternating-sum-of-volumes/. The authors are listed in prov/7SFHP7.jsonl.

import random
import unittest
from bisect import bisect_left
from fractions import Fraction
from itertools import combinations

from alternating_sum_of_volumes import asv, contains, depth, series_area, series_value, signed_hulls


# ---------- random simple polygons and an independent oracle ----------

def random_orthogonal(rng, size=7):
    """A hole-free polyomino with no pinch points, traced into a
    counterclockwise rectilinear polygon on random integer coordinates."""
    while True:
        target = rng.randint(4, 22)
        cells = {(rng.randrange(size), rng.randrange(size))}
        while len(cells) < target:
            i, j = rng.choice(sorted(cells))
            di, dj = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            if 0 <= i + di < size and 0 <= j + dj < size:
                cells.add((i + di, j + dj))
        if ok_polyomino(cells, size):
            break
    W = max(i for i, _ in cells) + 1
    H = max(j for _, j in cells) + 1
    X = sorted(rng.sample(range(-20, 60), W + 1))
    Y = sorted(rng.sample(range(-20, 60), H + 1))
    poly = [(X[i], Y[j]) for i, j in trace(cells)]

    def oracle(x, y):
        i, j = bisect_left(X, x) - 1, bisect_left(Y, y) - 1
        return (i, j) in cells
    return poly, oracle


def ok_polyomino(cells, size):
    empty = {(i, j) for i in range(-1, size + 1) for j in range(-1, size + 1)} - cells
    seen, stack = {(-1, -1)}, [(-1, -1)]
    while stack:
        i, j = stack.pop()
        for c in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if c in empty and c not in seen:
                seen.add(c)
                stack.append(c)
    if seen != empty:
        return False
    for i in range(-1, size):
        for j in range(-1, size):
            a, b = (i, j) in cells, (i + 1, j + 1) in cells
            c, d = (i + 1, j) in cells, (i, j + 1) in cells
            if a == b and c == d and a != c:
                return False
    return True


def trace(cells):
    nxt = {}
    for i, j in cells:
        if (i, j - 1) not in cells: nxt[(i, j)] = (i + 1, j)
        if (i + 1, j) not in cells: nxt[(i + 1, j)] = (i + 1, j + 1)
        if (i, j + 1) not in cells: nxt[(i + 1, j + 1)] = (i, j + 1)
        if (i - 1, j) not in cells: nxt[(i, j + 1)] = (i, j)
    start = min(nxt)
    cyc, p = [start], nxt[start]
    while p != start:
        cyc.append(p)
        p = nxt[p]
    return [b for k, b in enumerate(cyc)
            if orient(cyc[k - 1], b, cyc[(k + 1) % len(cyc)]) != 0]


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def random_star(rng):
    """A star-shaped simple polygon: integer points at distinct angles around
    the origin, sorted by angle, with every angular gap below a half turn."""
    while True:
        k = rng.randint(4, 14)
        pts = set()
        while len(pts) < k:
            p = (rng.randint(-30, 30), rng.randint(-30, 30))
            if p != (0, 0):
                pts.add(p)
        pts = sorted(pts, key=angle_key)
        ok = all(orient((0, 0), pts[t], pts[(t + 1) % k]) > 0 for t in range(k))
        ok = ok and all(orient(pts[t - 1], pts[t], pts[(t + 1) % k]) != 0 for t in range(k))
        if ok:
            return pts, lambda x, y, P=pts: crossing_number(P, x, y)


def angle_key(p):
    # exact angular order: half plane first, then by cross product
    half = 0 if (p[1] > 0 or (p[1] == 0 and p[0] > 0)) else 1
    return (half, Fraction(-p[0], abs(p[0]) + abs(p[1])) if half == 0 else Fraction(p[0], abs(p[0]) + abs(p[1])))


def crossing_number(poly, x, y):
    inside = False
    for k in range(len(poly)):
        (x0, y0), (x1, y1) = poly[k], poly[(k + 1) % len(poly)]
        if (y0 > y) != (y1 > y) and x0 + Fraction(x1 - x0) * (y - y0) / (y1 - y0) > x:
            inside = not inside
    return inside


def generic_points(rng, poly, count):
    """Rational points on no line through two vertices of the polygon. Every
    edge of every hull and region in the tree joins two such vertices."""
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    # the line through a and b, scaled by 97: u * X + v * Y = w at X = 97 x, Y = 97 y
    lines = [(b[1] - a[1], a[0] - b[0], 97 * ((b[1] - a[1]) * a[0] + (a[0] - b[0]) * a[1]))
             for a, b in combinations(poly, 2)]
    out = []
    while len(out) < count:
        X = rng.randint(97 * min(xs) - 50, 97 * max(xs) + 50)
        Y = rng.randint(97 * min(ys) - 50, 97 * max(ys) + 50)
        if all(u * X + v * Y != w for u, v, w in lines):
            out.append((Fraction(X, 97), Fraction(Y, 97)))
    return out


def twice_area(poly):
    return sum(poly[k][0] * poly[(k + 1) % len(poly)][1] - poly[(k + 1) % len(poly)][0] * poly[k][1]
               for k in range(len(poly)))


# ---------- tests ----------

class TestHandCases(unittest.TestCase):
    def test_convex_input_ends_in_one_step(self):
        sq = [(0, 0), (4, 0), (4, 3), (0, 3)]
        t = asv(sq)
        self.assertEqual(t.children, [])
        self.assertEqual(t.hull, sq)

    def test_l_shape(self):
        L = [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]
        t = asv(L)
        self.assertEqual(t.hull, [(0, 0), (4, 0), (4, 2), (2, 4), (0, 4)])
        self.assertEqual([c.region for c in t.children], [[(2, 4), (2, 2), (4, 2)]])
        self.assertEqual(depth(t), 2)
        self.assertEqual(series_area(t), 12)

    def test_stepped_slot_has_three_levels(self):
        P = [(0, 0), (8, 0), (8, 6), (6, 6), (6, 4), (5, 4), (5, 2), (3, 2),
             (3, 4), (2, 4), (2, 6), (0, 6)]
        t = asv(P)
        self.assertEqual(t.hull, [(0, 0), (8, 0), (8, 6), (0, 6)])
        (slot,) = t.children
        self.assertEqual(slot.hull, [(2, 4), (3, 2), (5, 2), (6, 4), (6, 6), (2, 6)])
        self.assertEqual(sorted(c.region for c in slot.children),
                         [[(3, 2), (3, 4), (2, 4)], [(6, 4), (5, 4), (5, 2)]])
        self.assertEqual([(s, len(h)) for s, h in signed_hulls(t)], [(1, 4), (-1, 6), (1, 3), (1, 3)])
        self.assertEqual(series_area(t), 48 - 12)

    def test_random_convex_inputs_end_in_one_step(self):
        rng = random.Random(21)
        from alternating_sum_of_volumes import convex_hull
        for _ in range(300):
            pts = [(rng.randint(-50, 50), rng.randint(-50, 50)) for _ in range(rng.randint(3, 30))]
            h = convex_hull(pts)
            if len(h) < 3:
                continue
            t = asv(h)
            self.assertEqual(t.children, [])
            self.assertEqual(t.hull, convex_hull(h))


class TestAgainstOracle(unittest.TestCase):
    def check(self, poly, oracle, rng, npts):
        t = asv(poly)
        self.assertEqual(series_area(t), Fraction(twice_area(poly), 2))
        # each pocket has fewer vertices than its parent, which bounds the depth
        stack = [t]
        while stack:
            node = stack.pop()
            for c in node.children:
                self.assertLess(len(c.region), len(node.region))
                stack.append(c)
        n = 0
        for x, y in generic_points(rng, poly, npts):
            inside = oracle(x, y)
            self.assertEqual(contains(t, x, y), inside)
            self.assertEqual(series_value(t, x, y), int(inside))
            n += 1
        return n, depth(t)

    def test_orthogonal_polygons(self):
        rng = random.Random(22)
        total, deepest = 0, 0
        for _ in range(250):
            poly, oracle = random_orthogonal(rng)
            n, d = self.check(poly, oracle, rng, 25)
            total += n
            deepest = max(deepest, d)
        self.assertGreater(total, 500)
        self.assertGreaterEqual(deepest, 3)

    def test_star_shaped_polygons(self):
        rng = random.Random(23)
        total = 0
        for _ in range(200):
            poly, oracle = random_star(rng)
            n, _ = self.check(poly, oracle, rng, 20)
            total += n
        self.assertGreater(total, 500)


class TestNonConvergenceIn3D(unittest.TestCase):
    """The 3D example of the page: two of the four cones from the centre of a
    regular tetrahedron. The solid and its deficiency both have all four
    corners, so the hull never shrinks, and cutting along z = x fixes it."""

    # A = (0,0,0), B = (1,1,0), C = (1,0,1), D = (0,1,1), O = (1/2,1/2,1/2),
    # all scaled by S = 202, so that the sample points p / S are exact integers
    S = 202
    A, B, C, D = (0, 0, 0), (S, S, 0), (S, 0, S), (0, S, S)
    O = (S // 2,) * 3

    @staticmethod
    def det3(u, v, w):
        return (u[0] * (v[1] * w[2] - v[2] * w[1]) - u[1] * (v[0] * w[2] - v[2] * w[0])
                + u[2] * (v[0] * w[1] - v[1] * w[0]))

    def in_tet(self, p, a, b, c, d):
        sub = lambda u, v: tuple(x - y for x, y in zip(u, v))
        s = self.det3(sub(b, a), sub(c, a), sub(d, a))
        signs = [self.det3(sub(b, p), sub(c, p), sub(d, p)),
                 self.det3(sub(p, a), sub(c, a), sub(d, a)),
                 self.det3(sub(b, a), sub(p, a), sub(d, a)),
                 self.det3(sub(b, a), sub(c, a), sub(p, a))]
        return all(x * s > 0 for x in signs)

    def test_cycle_and_partition(self):
        A, B, C, D, O = self.A, self.B, self.C, self.D, self.O
        H = lambda p: self.in_tet(p, A, B, C, D)
        P = lambda p: self.in_tet(p, O, A, B, C) or self.in_tet(p, O, A, C, D)
        deficiency = lambda p: self.in_tet(p, O, A, B, D) or self.in_tet(p, O, B, C, D)
        # both P and its deficiency contain all four corners, so both hulls are H
        for corner in (A, B, C, D):
            self.assertTrue(corner in (O, A, B, C) or corner in (O, A, C, D))
            self.assertTrue(corner in (O, A, B, D) or corner in (O, B, C, D))
        rng = random.Random(24)
        checked = 0
        while checked < 1000:
            p = tuple(rng.randint(-20, self.S + 20) for _ in range(3))
            if p[2] == p[0]:
                continue
            cones = [self.in_tet(p, O, *f) for f in ((A, B, C), (A, B, D), (A, C, D), (B, C, D))]
            if not H(p):
                self.assertEqual(sum(cones), 0)
                continue
            if sum(cones) != 1:          # on a shared face of two cones
                continue
            checked += 1
            # ASV step 1: H minus P is the deficiency, step 2: H minus that is P again
            self.assertEqual(H(p) and not P(p), deficiency(p))
            self.assertEqual(H(p) and not deficiency(p), P(p))
            # ASVP: the plane z = x through O, A and C splits P into two tetrahedra
            if p[2] < p[0]:
                self.assertEqual(P(p), self.in_tet(p, O, A, B, C))
            else:
                self.assertEqual(P(p), self.in_tet(p, O, A, C, D))
        # volumes: each cone is a quarter of the tetrahedron, which has volume 1/3
        vol = lambda a, b, c, d: abs(self.det3(*[tuple(x - y for x, y in zip(v, a)) for v in (b, c, d)])) * Fraction(1, 6 * self.S ** 3)
        self.assertEqual(vol(A, B, C, D), Fraction(1, 3))
        self.assertEqual(vol(O, A, B, C) + vol(O, A, C, D), Fraction(1, 6))
        self.assertEqual(vol(O, A, B, D) + vol(O, B, C, D), Fraction(1, 6))


if __name__ == "__main__":
    unittest.main()
