# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-projected-polyhedron/. The authors are listed in prov/V244NY.jsonl.

import random
import unittest
from fractions import Fraction as F
from itertools import product
from math import sqrt

from interval_projected_polyhedron import (
    bernstein_tensor, enclose, hull_axis_interval, ipp, project, split, strides,
)
from si1geom import bernstein


def evaluate(poly, x):
    total = F(0)
    for e, c in poly.items():
        term = F(c)
        for xj, k in zip(x, e):
            term *= F(xj) ** k
        total += term
    return total


def bernstein_value(shape, flat, u):
    st = strides(shape)
    bs = [bernstein(d - 1, uj) for d, uj in zip(shape, u)]
    total = F(0)
    for idx in product(*[range(d) for d in shape]):
        w = F(1)
        for j, i in enumerate(idx):
            w *= bs[j][i]
        total += w * flat[sum(i * s for i, s in zip(idx, st))]
    return total


def random_poly(rng, degs):
    return {e: F(rng.randint(-9, 9), rng.randint(1, 5)) for e in product(*[range(d + 1) for d in degs])}


def inside(x, box):
    return all(a <= xj <= b for xj, (a, b) in zip(x, box))


def linear(a, b, c):
    """a x + b y + c."""
    return {(1, 0): a, (0, 1): b, (0, 0): c}


def times(p, q):
    out = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            e = tuple(x + y for x, y in zip(e1, e2))
            out[e] = out.get(e, 0) + F(c1) * F(c2)
    return out


class TestBernsteinForm(unittest.TestCase):
    def test_conversion_is_exact(self):
        rng = random.Random(1)
        for _ in range(20):
            poly = random_poly(rng, (rng.randint(0, 3), rng.randint(0, 3)))
            box = [(F(rng.randint(-5, 0), 2), F(rng.randint(1, 5), 3)) for _ in range(2)]
            shape, flat = bernstein_tensor(poly, box)
            for _ in range(5):
                u = (F(rng.randint(0, 12), 12), F(rng.randint(0, 7), 7))
                x = [a + (b - a) * uj for (a, b), uj in zip(box, u)]
                self.assertEqual(bernstein_value(shape, flat, u), evaluate(poly, x))

    def test_interval_split_encloses_the_exact_pieces(self):
        rng = random.Random(2)
        for _ in range(20):
            poly = random_poly(rng, (3, 2))
            shape, flat = bernstein_tensor(poly, [(0, 1), (0, 1)])
            coefs = [enclose(x) for x in flat]
            axis = rng.randint(0, 1)
            t = rng.random()
            left, right = split(coefs, shape, axis, t)
            for _ in range(4):
                u = [F(rng.randint(0, 10), 10), F(rng.randint(0, 10), 10)]
                for piece, lo_end, width in ((left, F(0), F(t)), (right, F(t), 1 - F(t))):
                    x = list(u)
                    x[axis] = lo_end + width * u[axis]
                    exact = evaluate(poly, x)
                    lo = bernstein_value(shape, [F(a) for a, _ in piece], u)
                    hi = bernstein_value(shape, [F(b) for _, b in piece], u)
                    self.assertLessEqual(lo, exact)
                    self.assertLessEqual(exact, hi)
                    self.assertLess(hi - lo, 1e-12)


class TestProjection(unittest.TestCase):
    def test_hull_interval_of_a_small_set(self):
        pts = [(F(0), F(2)), (F(1, 2), F(-1)), (F(1), F(3))]
        lo, hi = hull_axis_interval(pts)
        # the edges from (1/2, -1) to (0, 2) and to (1, 3) cross f = 0 at 1/3 and 5/8
        self.assertEqual((lo, hi), (F(1, 3), F(5, 8)))
        self.assertIsNone(hull_axis_interval([(F(0), F(1)), (F(1), F(2))]))

    def test_projection_keeps_every_zero(self):
        # g = f - f(u) has the zero u, and the projection must keep u_j
        rng = random.Random(3)
        for _ in range(60):
            poly = random_poly(rng, (rng.randint(1, 3), rng.randint(1, 3)))
            u = (F(rng.randint(0, 20), 20), F(rng.randint(0, 20), 20))
            poly[(0, 0)] = poly[(0, 0)] - evaluate(poly, u)
            shape, flat = bernstein_tensor(poly, [(0, 1), (0, 1)])
            coefs = [enclose(x) for x in flat]
            for j in range(2):
                r = project(coefs, shape, j)
                self.assertIsNotNone(r)
                self.assertLessEqual(r[0], u[j])
                self.assertLessEqual(u[j], r[1])


class TestSolver(unittest.TestCase):
    def check(self, clusters, raw, roots, eps=1e-8):
        """Each root is in a raw box, each cluster holds exactly one root."""
        for x in roots:
            self.assertTrue(any(inside([F(v) for v in x], X) for X in raw), x)
        self.assertEqual(len(clusters), len(roots))
        for C in clusters:
            self.assertEqual(sum(inside(x, C) for x in roots), 1, C)
            self.assertLess(max(b - a for a, b in C), eps)

    def test_example_circle_and_line(self):
        circle = {(2, 0): 1, (0, 2): 1, (0, 0): -1}
        clusters, raw = ipp([circle, linear(1, -1, 0)], [(-2, 2), (-2, 2)])
        h = sqrt(0.5)
        self.assertEqual(len(clusters), 2)
        for C, s in zip(clusters, (-1, 1)):
            for a, b in C:
                self.assertLess(abs(a - s * h), 1e-9)
                self.assertLess(abs(b - s * h), 1e-9)

    def test_products_of_linear_factors(self):
        f1 = times(linear(1, 0, -F(2, 10)), linear(1, 0, -F(7, 10)))
        f2 = times(times(linear(0, 1, -F(3, 10)), linear(0, 1, -F(6, 10))), linear(0, 1, -F(9, 10)))
        clusters, raw = ipp([f1, f2], [(0, 1), (0, 1)])
        roots = [(F(a, 10), F(b, 10)) for a in (2, 7) for b in (3, 6, 9)]
        self.check(clusters, raw, roots)

    def test_three_variables(self):
        sphere = {(2, 0, 0): 1, (0, 2, 0): 1, (0, 0, 2): 1, (0, 0, 0): -1}
        p1 = {(1, 0, 0): 1, (0, 1, 0): -1}
        p2 = {(0, 1, 0): 1, (0, 0, 1): -1}
        clusters, raw = ipp([sphere, p1, p2], [(-1, 1)] * 3)
        self.assertEqual(len(clusters), 2)
        r = 1 / sqrt(3)
        for C, s in zip(clusters, (-1, 1)):
            for a, b in C:
                self.assertLessEqual(a, s * r + 1e-15)
                self.assertLessEqual(s * r - 1e-15, b)

    def test_one_variable_degree_five(self):
        p = {(0,): 1}
        for k in range(1, 6):
            p = times(p, {(1,): 1, (0,): -F(k, 10)})
        clusters, raw = ipp([p], [(0, 1)])
        self.check(clusters, raw, [(F(k, 10),) for k in range(1, 6)])

    def test_close_roots_of_the_book_example(self):
        # (x - 0.1)(x - 0.6)(x - 0.7), where plain floats can lose 0.7
        p = {(0,): 1}
        for r in (F(1, 10), F(6, 10), F(7, 10)):
            p = times(p, {(1,): 1, (0,): -r})
        clusters, raw = ipp([p], [(0, 1)], eps=1e-12)
        self.check(clusters, raw, [(F(1, 10),), (F(6, 10),), (F(7, 10),)], eps=1e-11)

    def test_no_roots(self):
        positive = {(2, 0): 1, (0, 2): 1, (0, 0): 1}
        self.assertEqual(ipp([positive, linear(1, -1, 0)], [(-2, 2), (-2, 2)]), ([], []))
        small = {(2, 0): 1, (0, 2): 1, (0, 0): -F(1, 4)}
        self.assertEqual(ipp([small, linear(1, -1, 0)], [(1, 2), (1, 2)]), ([], []))

    def test_double_root_is_enclosed(self):
        tangent = {(2, 0): 1, (1, 0): -1, (0, 0): F(1, 4)}  # (x - 1/2)^2
        clusters, raw = ipp([tangent, linear(0, 1, -F(1, 2))], [(0, 1), (0, 1)])
        self.assertTrue(any(inside((F(1, 2), F(1, 2)), X) for X in raw))
        self.assertEqual(len(clusters), 1)

    def test_random_pairs_of_line_pairs(self):
        # f1 = L1 L2 and f2 = L3 L4 have the four roots Li = Lj = 0, i < 3 <= j
        rng = random.Random(5)
        total = 0
        for _ in range(30):
            lines = [(F(rng.randint(-9, 9)), F(rng.randint(-9, 9)), F(rng.randint(-9, 9), 3)) for _ in range(4)]
            if any(a == 0 and b == 0 for a, b, _ in lines):
                continue
            f1 = times(linear(*lines[0]), linear(*lines[1]))
            f2 = times(linear(*lines[2]), linear(*lines[3]))
            roots = []
            for a1, b1, c1 in lines[:2]:
                for a2, b2, c2 in lines[2:]:
                    d = a1 * b2 - a2 * b1
                    if d != 0:
                        x = ((-c1) * b2 - (-c2) * b1) / d
                        y = (a1 * (-c2) - a2 * (-c1)) / d
                        if -1 <= x <= 1 and -1 <= y <= 1:
                            roots.append((x, y))
            if any(a1 * b2 == a2 * b1 for a1, b1, _ in lines[:2] for a2, b2, _ in lines[2:]):
                continue  # a parallel pair may share a whole line
            clusters, raw = ipp([f1, f2], [(-1, 1), (-1, 1)])
            for x in roots:
                self.assertTrue(any(inside(x, X) for X in raw), x)
            distinct = set(roots)
            total += len(distinct)
            # measured: every group holds a root, and distinct roots give distinct groups
            for C in clusters:
                self.assertTrue(any(inside(x, C) for x in distinct), C)
            self.assertEqual(len(clusters), len(distinct))
        self.assertGreater(total, 20)


if __name__ == "__main__":
    unittest.main()
