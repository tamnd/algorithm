# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selective-geometric-complex/. The authors are listed in prov/TH7Q2X.jsonl.

import random
import unittest
from fractions import Fraction as Fr
from math import atan2, gcd

from selective_geometric_complex import SGC

# Directions for the neighbourhood oracle: the primitive vectors with entries
# in [-4, 4] contain the direction of every segment between grid points of
# [0, 4]^2, and the sum of two neighbours in angular order lies strictly
# inside every wedge between two such directions.
S4 = sorted({(x, y) for x in range(-4, 5) for y in range(-4, 5) if (x, y) != (0, 0) and gcd(x, y) == 1},
            key=lambda d: atan2(d[1], d[0]))
DIRS = [(0, 0)] + S4 + [(S4[i][0] + S4[(i + 1) % len(S4)][0], S4[i][1] + S4[(i + 1) % len(S4)][1])
                        for i in range(len(S4))]
EPS0 = Fr(1, 10000)


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def in_closed_segment(p, a, b):
    if orient(a, b, p) != 0:
        return False
    t = ((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1]))
    return 0 <= t <= (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2


def prim_contains(prim, p):
    """Membership in a primitive, straight from its definition."""
    kind = prim[0]
    if kind == "tri":
        _, a, b, c, closed = prim
        s = [orient(a, b, p), orient(b, c, p), orient(c, a, p)]
        if orient(a, b, c) < 0:
            s = [-x for x in s]
        if all(x > 0 for x in s):
            return True
        return closed and all(x >= 0 for x in s)
    if kind == "seg":
        _, a, b, closed = prim
        return in_closed_segment(p, a, b) and (closed or p not in (a, b))
    return p == prim[1]


def ev(node, p, eps=EPS0):
    k = node[0]
    if k in ("tri", "seg", "pt"):
        return prim_contains(node, p)
    if k == "not":
        return not ev(node[1], p, eps)
    if k in ("and", "or", "minus", "xor"):
        x, y = ev(node[1], p, eps), ev(node[2], p, eps)
        return {"and": x and y, "or": x or y, "minus": x and not y, "xor": x != y}[k]
    near = [ev(node[1], (p[0] + eps * d[0], p[1] + eps * d[1]), eps / 100) for d in DIRS]
    return {"int": all(near), "cl": any(near), "bd": any(near) and not all(near)}[k]


def build(node):
    k = node[0]
    if k == "tri":
        return SGC.polygon(node[1:4], node[4])
    if k == "seg":
        return SGC.segment(node[1], node[2], node[3])
    if k == "pt":
        return SGC.point(node[1])
    if k == "not":
        return build(node[1]).complement()
    if k in ("and", "or", "minus", "xor"):
        a, b = build(node[1]), build(node[2])
        return {"and": a & b, "or": a | b, "minus": a - b, "xor": a ^ b}[k]
    a = build(node[1])
    return {"int": a.interior(), "cl": a.closure(), "bd": a.boundary()}[k]


def rpt(rng):
    return (rng.randint(0, 4), rng.randint(0, 4))


def random_primitive(rng):
    r = rng.random()
    if r < 0.6:
        while True:
            a, b, c = rpt(rng), rpt(rng), rpt(rng)
            if orient(a, b, c) != 0:
                return ("tri", a, b, c, rng.random() < 0.5)
    if r < 0.85:
        while True:
            a, b = rpt(rng), rpt(rng)
            if a != b:
                return ("seg", a, b, rng.random() < 0.5)
    return ("pt", rpt(rng))


def random_formula(rng, depth, topo):
    if depth == 0 or rng.random() < 0.25:
        return random_primitive(rng)
    r = rng.random()
    if topo and r < 0.3:
        return (rng.choice(["int", "cl", "bd"]), random_formula(rng, depth - 1, False))
    if r < 0.35:
        return ("not", random_formula(rng, depth - 1, topo))
    return (rng.choice(["and", "or", "minus", "xor"]), random_formula(rng, depth - 1, topo),
            random_formula(rng, depth - 1, topo))


def sample_points(s):
    pts = [(Fr(x, 2), Fr(y, 2)) for x in range(-1, 10) for y in range(-1, 10)]
    return pts + list(s.cx.vertices)


class TestHandCases(unittest.TestCase):
    def test_square_with_a_crack(self):
        sq = SGC.polygon([(0, 0), (4, 0), (4, 4), (0, 4)], True)
        crack = SGC.segment((1, 2), (3, 2), False)
        s = sq - crack
        self.assertEqual(s.size(), (6, 5, 2))                 # 1 bounded face, plus the outside
        self.assertEqual(s.count_by_dimension(), (6, 4, 1))
        self.assertFalse(s.contains((2, 2)))
        self.assertTrue(s.contains((1, 2)))
        r = s.regularization()
        self.assertEqual(r.size(), (4, 4, 2))
        self.assertTrue(r.contains((2, 2)))

    def test_shared_edge(self):
        a = SGC.polygon([(0, 0), (2, 0), (2, 2), (0, 2)], True)
        b = SGC.polygon([(2, 0), (4, 0), (4, 2), (2, 2)], True)
        self.assertEqual((a & b).count_by_dimension(), (2, 1, 0))
        self.assertTrue((a & b).regularization().is_empty())
        u = a | b
        self.assertEqual(u.size(), (4, 4, 2))                 # the inner edge is simplified away
        self.assertEqual(u.count_by_dimension(), (4, 4, 1))

    def test_dangling_edge_and_point(self):
        sq = SGC.polygon([(0, 0), (2, 0), (2, 2), (0, 2)], True)
        s = sq | SGC.segment((2, 1), (3, 1), True) | SGC.point((4, 4))
        self.assertEqual(s.count_by_dimension(), (7, 6, 1))
        self.assertEqual(s.boundary().count_by_dimension(), (7, 6, 0))
        self.assertEqual(s.interior().count_by_dimension(), (0, 0, 1))


class TestAgainstFormula(unittest.TestCase):
    def test_boolean_formulas(self):
        rng = random.Random(1)
        checked = 0
        for _ in range(30):
            f = random_formula(rng, 3, False)
            s = build(f)
            for p in sample_points(s):
                self.assertEqual(s.contains(p), ev(f, p), (f, p))
                checked += 1
        self.assertGreater(checked, 500)

    def test_topological_operators(self):
        rng = random.Random(2)
        checked = 0
        for _ in range(15):
            f = (rng.choice(["int", "cl", "bd"]), random_formula(rng, 2, False))
            s = build(f)
            pts = sample_points(s)
            for p in rng.sample(pts, 35):
                self.assertEqual(s.contains(p), ev(f, p), (f, p))
                checked += 1
        self.assertGreater(checked, 500)


class TestSimplification(unittest.TestCase):
    def test_minimal_and_stable(self):
        """After simplification no edge or vertex separates cells with equal
        marks, and simplifying again changes nothing."""
        rng = random.Random(3)
        for _ in range(20):
            s = build(random_formula(rng, 3, False))
            cx, m = s.cx, s.marks
            for e in cx.edges:
                self.assertTrue(any((("f", f) in m) != (("e", e) in m) for f in cx.side[e]))
            for v in cx.vertices:
                star = cx.star[("v", v)]
                needed = any((c in m) != (("v", v) in m) for c in star)
                edges = [c for c in star if c[0] == "e"]
                bend = len(edges) != 2 or orient(*[x for c in edges for x in c[1] if x != v][:2], v) != 0
                self.assertTrue(needed or bend)
            t = s.simplify()
            self.assertEqual(t.size(), s.size())
            self.assertEqual(t.count_by_dimension(), s.count_by_dimension())


if __name__ == "__main__":
    unittest.main()
