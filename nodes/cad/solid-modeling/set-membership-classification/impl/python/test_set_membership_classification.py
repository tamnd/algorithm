# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/set-membership-classification/. The authors are listed in prov/E1CR69.jsonl.

import random
import unittest
from fractions import Fraction
from math import gcd

from set_membership_classification import (
    IN, ON, OUT, classify_neighborhood, classify_point, classify_segment, cross, segment_class_at,
)

DIRS = [(x, y) for x in range(-8, 9) for y in range(-8, 9) if gcd(x, y) == 1]


def is_tree_node(t):
    return isinstance(t, tuple) and t and isinstance(t[0], str)


def strictly_inside(p, poly):
    k = len(poly)
    return all(cross((poly[(i + 1) % k][0] - poly[i][0], poly[(i + 1) % k][1] - poly[i][1]),
                     (p[0] - poly[i][0], p[1] - poly[i][1])) > 0 for i in range(k))


def formula(p, tree):
    """The plain set formula, valid at a point that lies on no leaf boundary."""
    if not is_tree_node(tree):
        return strictly_inside(p, tree)
    op, l, r = tree
    a, b = formula(p, l), formula(p, r)
    return {"union": a or b, "intersection": a and b, "difference": a and not b}[op]


def edge_dirs_through(p, tree):
    if is_tree_node(tree):
        return edge_dirs_through(p, tree[1]) + edge_dirs_through(p, tree[2])
    out = []
    k = len(tree)
    for i in range(k):
        a, b = tree[i], tree[(i + 1) % k]
        e = (b[0] - a[0], b[1] - a[1])
        if cross(e, (p[0] - a[0], p[1] - a[1])) == 0:
            out.append(e)
    return out


def scale(tree, s):
    if is_tree_node(tree):
        return (tree[0], scale(tree[1], s), scale(tree[2], s))
    return [(int(x * s), int(y * s)) for x, y in tree]


def brute_classify(p, tree):
    """Sample points at distance about 1/10^6 in many directions and evaluate the plain formula.

    All edge vectors have coordinates of at most 8 in absolute value, so every
    open sector between two edge lines through p contains one of DIRS. The work
    is done in integers, scaled by s.
    """
    lines = edge_dirs_through(p, tree)
    if not lines:
        return IN if formula(p, tree) else OUT
    s = Fraction(p[0]).denominator * Fraction(p[1]).denominator * 10 ** 6
    big = scale(tree, s)
    q = (int(p[0] * s), int(p[1] * s))
    seen = set()
    for w in DIRS:
        if any(cross(e, w) == 0 for e in lines):
            continue
        seen.add(formula((q[0] + w[0], q[1] + w[1]), big))
        if len(seen) == 2:
            return ON
    return IN if seen == {True} else OUT


def hull(points):
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross((lower[-1][0] - lower[-2][0], lower[-1][1] - lower[-2][1]),
                                        (p[0] - lower[-2][0], p[1] - lower[-2][1])) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross((upper[-1][0] - upper[-2][0], upper[-1][1] - upper[-2][1]),
                                        (p[0] - upper[-2][0], p[1] - upper[-2][1])) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def random_convex(rng):
    while True:
        if rng.random() < 0.4:
            x0, y0 = rng.randint(0, 3), rng.randint(0, 3)
            x1, y1 = x0 + rng.randint(1, 2), y0 + rng.randint(1, 2)
            return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        h = hull([(rng.randint(0, 4), rng.randint(0, 4)) for _ in range(rng.randint(3, 6))])
        if len(h) >= 3:
            return h


def random_tree(rng, depth):
    if depth == 0 or rng.random() < 0.3:
        return random_convex(rng)
    op = rng.choice(["union", "union", "intersection", "difference"])
    return (op, random_tree(rng, depth - 1), random_tree(rng, depth - 1))


def half_point(rng):
    return (Fraction(rng.randint(0, 9), 2), Fraction(rng.randint(0, 9), 2))


SQ1 = [(0, 0), (2, 0), (2, 2), (0, 2)]
SQ2 = [(2, 0), (4, 0), (4, 2), (2, 2)]
TRI = [(1, 1), (3, 1), (2, 3)]


class TestSetMembership(unittest.TestCase):
    def test_worked_example(self):
        tree = ("difference", ("union", SQ1, SQ2), TRI)
        self.assertEqual(classify_point((2, 1), ("union", SQ1, SQ2)), IN)
        self.assertEqual(classify_point((2, 0), ("union", SQ1, SQ2)), ON)
        self.assertEqual(classify_point((2, 1), ("intersection", SQ1, SQ2)), OUT)
        self.assertEqual(classify_point((2, 1), tree), ON)
        self.assertEqual(classify_point((2, 2), tree), OUT)
        self.assertEqual(classify_point((2, Fraction(1, 2)), tree), IN)
        self.assertEqual(classify_point((Fraction(1, 2), Fraction(1, 2)), tree), IN)
        self.assertEqual(classify_point((2, 3), tree), OUT)
        nb = classify_neighborhood((2, 1), tree)
        self.assertEqual(nb, ([(2, 0), (-2, 0)], [False, True]))

    def test_touching_squares(self):
        self.assertEqual(classify_point((2, 1), ("intersection", SQ1, SQ2)), OUT)
        self.assertEqual(classify_point((2, 1), ("difference", SQ1, SQ2)), ON)
        self.assertEqual(classify_point((1, 1), ("difference", SQ1, SQ1)), OUT)

    def test_segment_example(self):
        tree = ("difference", ("union", SQ1, SQ2), TRI)
        pieces = classify_segment((0, 1), (4, 1), tree)
        q, h = Fraction(1, 4), Fraction(3, 4)
        self.assertEqual(pieces, [(0, 0, ON), (0, q, IN), (q, q, ON), (q, h, ON), (h, h, ON),
                                  (h, 1, IN), (1, 1, ON)])

    def test_random_points(self):
        rng = random.Random(1980)
        count = 0
        for _ in range(300):
            tree = random_tree(rng, 3)
            for _ in range(4):
                p = half_point(rng)
                self.assertEqual(classify_point(p, tree), brute_classify(p, tree), (p, tree))
                count += 1
        self.assertGreaterEqual(count, 1000)

    def test_random_segments(self):
        rng = random.Random(874)
        for _ in range(120):
            tree = random_tree(rng, 2)
            a, b = half_point(rng), half_point(rng)
            if a == b:
                continue
            pieces = classify_segment(a, b, tree)
            for k in range(17):
                t = Fraction(k, 16)
                p = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
                self.assertEqual(segment_class_at(pieces, t), brute_classify(p, tree))
            for t0, t1, c in pieces:
                if t0 < t1:
                    m = (t0 + t1) / 2
                    p = (a[0] + m * (b[0] - a[0]), a[1] + m * (b[1] - a[1]))
                    self.assertEqual(c, brute_classify(p, tree))


if __name__ == "__main__":
    unittest.main()
