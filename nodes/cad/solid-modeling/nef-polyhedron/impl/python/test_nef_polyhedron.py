# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nef-polyhedron/. The authors are listed in prov/Q616YB.jsonl.

import random
import unittest
from fractions import Fraction as Fr
from math import atan2, gcd

from nef_polyhedron import NefPolygon

# Directions for the neighbourhood oracle: every primitive vector with
# entries in [-3, 3], which contains the direction of every line with such
# coefficients, and the sum of each pair of neighbours in angular order,
# which lies strictly inside every wedge between two such lines.
S3 = sorted({(x, y) for x in range(-3, 4) for y in range(-3, 4) if (x, y) != (0, 0) and gcd(x, y) == 1},
            key=lambda d: atan2(d[1], d[0]))
DIRS = [(0, 0)] + S3 + [(S3[i][0] + S3[(i + 1) % len(S3)][0], S3[i][1] + S3[(i + 1) % len(S3)][1])
                        for i in range(len(S3))]
EPS0 = Fr(1, 1000)


def ev(node, p, eps=EPS0):
    """Evaluate a formula at p straight from its definition. A topological
    operator looks at p and at p + eps d for every d in DIRS; eps is small
    enough that these points see every face around p and no other."""
    k = node[0]
    if k == "h":
        _, a, b, c, closed = node
        v = a * p[0] + b * p[1] + c
        return v >= 0 if closed else v > 0
    if k == "not":
        return not ev(node[1], p, eps)
    if k in ("and", "or", "minus", "xor"):
        x, y = ev(node[1], p, eps), ev(node[2], p, eps)
        return {"and": x and y, "or": x or y, "minus": x and not y, "xor": x != y}[k]
    near = [ev(node[1], (p[0] + eps * d[0], p[1] + eps * d[1]), eps / 100) for d in DIRS]
    if k == "int":
        return all(near)
    if k == "cl":
        return any(near)
    if k == "bd":
        return any(near) and not all(near)
    raise ValueError(k)


def build(node):
    k = node[0]
    if k == "h":
        return NefPolygon.halfplane(*node[1:])
    if k == "not":
        return build(node[1]).complement()
    if k in ("and", "or", "minus", "xor"):
        a, b = build(node[1]), build(node[2])
        return {"and": a & b, "or": a | b, "minus": a - b, "xor": a ^ b}[k]
    a = build(node[1])
    return {"int": a.interior(), "cl": a.closure(), "bd": a.boundary()}[k]


def random_halfplane(rng):
    while True:
        a, b = rng.randint(-3, 3), rng.randint(-3, 3)
        if (a, b) != (0, 0):
            return ("h", a, b, rng.randint(-3, 3), rng.random() < 0.5)


def random_formula(rng, depth, topo):
    if depth == 0 or rng.random() < 0.25:
        return random_halfplane(rng)
    r = rng.random()
    if topo and r < 0.3:
        return (rng.choice(["int", "cl", "bd"]), random_formula(rng, depth - 1, False))
    if r < 0.4:
        return ("not", random_formula(rng, depth - 1, topo))
    return (rng.choice(["and", "or", "minus", "xor"]), random_formula(rng, depth - 1, topo),
            random_formula(rng, depth - 1, topo))


def halfplanes(node, out):
    if node[0] == "h":
        out.append(node)
    else:
        for c in node[1:]:
            halfplanes(c, out)
    return out


def sample_points(node):
    """Grid points with denominator 2 and every crossing of two lines."""
    pts = [(Fr(x, 2), Fr(y, 2)) for x in range(-6, 7) for y in range(-6, 7)]
    hs = halfplanes(node, [])
    for i in range(len(hs)):
        for j in range(i + 1, len(hs)):
            a1, b1, c1 = hs[i][1:4]
            a2, b2, c2 = hs[j][1:4]
            det = a1 * b2 - a2 * b1
            if det != 0:
                pts.append((Fr(b1 * c2 - c1 * b2, det), Fr(c1 * a2 - a1 * c2, det)))
    return pts


class TestHandCases(unittest.TestCase):
    def test_touching_halfplanes_meet_in_a_line(self):
        a = NefPolygon.halfplane(1, 0, 0, True)    # x >= 0
        b = NefPolygon.halfplane(-1, 0, 0, True)   # x <= 0
        s = a & b
        self.assertEqual(s.count_by_dimension(), (0, 1, 0))
        self.assertTrue(s.contains((0, 5)))
        self.assertTrue(s.regularization().is_empty())

    def test_square_with_a_dangling_edge_and_a_point(self):
        sq = (NefPolygon.halfplane(1, 0, 0, True) & NefPolygon.halfplane(-1, 0, 2, True)
              & NefPolygon.halfplane(0, 1, 0, True) & NefPolygon.halfplane(0, -1, 2, True))
        # the segment y = 1, 2 <= x <= 3
        seg = (NefPolygon.halfplane(0, 1, -1, True) & NefPolygon.halfplane(0, -1, 1, True)
               & NefPolygon.halfplane(1, 0, -2, True) & NefPolygon.halfplane(-1, 0, 3, True))
        # the point (4, 4)
        pt = (NefPolygon.halfplane(1, 0, -4, True) & NefPolygon.halfplane(-1, 0, 4, True)
              & NefPolygon.halfplane(0, 1, -4, True) & NefPolygon.halfplane(0, -1, 4, True))
        s = sq | seg | pt
        for q, want in [((1, 1), True), ((Fr(5, 2), 1), True), ((4, 4), True), ((3, 2), False)]:
            self.assertEqual(s.contains(q), want)
        r = s.regularization()
        self.assertFalse(r.contains((Fr(5, 2), 1)))
        self.assertFalse(r.contains((4, 4)))
        self.assertTrue(r.contains((2, 2)))
        self.assertTrue(s.boundary().contains((Fr(5, 2), 1)))
        # all 8 lines x = 0, 2, 3, 4 and y = 0, 1, 2, 4 carry some boundary
        self.assertEqual(len(s.simplify().arr.lines), 8)
        # the regularized set needs only the 4 lines of the square
        self.assertEqual(len(r.simplify().arr.lines), 4)

    def test_open_square_minus_its_diagonal(self):
        sq = (NefPolygon.halfplane(1, 0, 0, False) & NefPolygon.halfplane(-1, 0, 1, False)
              & NefPolygon.halfplane(0, 1, 0, False) & NefPolygon.halfplane(0, -1, 1, False))
        diag = NefPolygon.halfplane(1, -1, 0, True) & NefPolygon.halfplane(-1, 1, 0, True)
        s = sq - diag
        self.assertEqual(s.count_by_dimension(), (0, 0, 2))
        self.assertFalse(s.contains((Fr(1, 2), Fr(1, 2))))
        self.assertTrue(s.closure().contains((Fr(1, 2), Fr(1, 2))))
        self.assertTrue((s.regularization() ^ sq.closure()).is_empty())


class TestAgainstFormula(unittest.TestCase):
    def test_boolean_formulas(self):
        rng = random.Random(1)
        checked = 0
        for _ in range(80):
            f = random_formula(rng, 4, False)
            s = build(f)
            for p in sample_points(f):
                self.assertEqual(s.contains(p), ev(f, p), (f, p))
                checked += 1
        self.assertGreater(checked, 500)

    def test_topological_operators(self):
        rng = random.Random(2)
        checked = 0
        for _ in range(40):
            f = (rng.choice(["int", "cl", "bd"]), random_formula(rng, 3, False))
            s = build(f)
            pts = sample_points(f)
            for p in rng.sample(pts, min(25, len(pts))):
                self.assertEqual(s.contains(p), ev(f, p), (f, p))
                checked += 1
        self.assertGreater(checked, 500)

    def test_nested_formulas(self):
        rng = random.Random(3)
        for _ in range(25):
            f = random_formula(rng, 4, True)
            s = build(f)
            pts = sample_points(f)
            for p in rng.sample(pts, min(15, len(pts))):
                self.assertEqual(s.contains(p), ev(f, p), (f, p))


class TestIdentities(unittest.TestCase):
    def test_closure_identities(self):
        rng = random.Random(4)
        for _ in range(60):
            s = build(random_formula(rng, 4, False))
            c, i = s.closure(), s.interior()
            self.assertTrue((c.closure() ^ c).is_empty())
            self.assertTrue((i.interior() ^ i).is_empty())
            self.assertTrue((s.complement().closure() ^ i.complement()).is_empty())
            self.assertTrue((s.boundary() ^ (c & s.complement().closure())).is_empty())
            self.assertTrue((s - c).is_empty() and (i - s).is_empty())
            r = s.regularization()
            self.assertTrue((r.regularization() ^ r).is_empty())

    def test_simplify_keeps_the_set(self):
        rng = random.Random(5)
        for _ in range(60):
            f = random_formula(rng, 4, False)
            s = build(f)
            t = s.simplify()
            self.assertLessEqual(len(t.arr.lines), len(s.arr.lines))
            self.assertTrue((s ^ t).is_empty())
            for p in sample_points(f)[::7]:
                self.assertEqual(t.contains(p), ev(f, p))


if __name__ == "__main__":
    unittest.main()
