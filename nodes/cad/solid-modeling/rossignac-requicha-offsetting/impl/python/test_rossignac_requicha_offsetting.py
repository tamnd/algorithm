# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rossignac-requicha-offsetting/. The authors are listed in prov/B7AHTM.jsonl.

import random
import unittest
from fractions import Fraction as F

from rossignac_requicha_offsetting import Solid, box, diff, grow, inter, shrink_classify, union


def d2_rect(c, x):
    dx = max(c[0] - x[0], F(0), x[0] - c[1])
    dy = max(c[2] - x[1], F(0), x[1] - c[3])
    return dx * dx + dy * dy


def d2_to_solid(S: Solid, x):
    """Brute force: the squared distance to the union of the closed inside cells."""
    return min((d2_rect(c, x) for c in S.cells), default=None)


def d2_to_complement(S: Solid, x):
    """Brute force: the squared distance to the closure of the complement, for x in the grid."""
    xs, ys = S.xs, S.ys
    best = min(x[0] - xs[0], xs[-1] - x[0], x[1] - ys[0], ys[-1] - x[1]) ** 2
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            if not S.cell[i][j]:
                best = min(best, d2_rect((xs[i], xs[i + 1], ys[j], ys[j + 1]), x))
    return best


def random_tree(rng, n):
    def rb():
        x0, y0 = rng.randint(0, 5), rng.randint(0, 5)
        return box(x0, x0 + rng.randint(1, 3), y0, y0 + rng.randint(1, 3))

    t = rb()
    for _ in range(n - 1):
        t = rng.choice([union, union, inter, diff])(t, rb())
    return t


def points(rng, k, lo=-2, hi=10, den=4):
    return [(F(rng.randint(lo * den, hi * den), den), F(rng.randint(lo * den, hi * den), den)) for _ in range(k)]


def near(rng, S: Solid, k, den=4):
    """Random points of the grid of step 1/den in the box of S, widened by 1."""
    if not S.cells:
        return points(rng, k)
    x0, x1 = min(c[0] for c in S.cells) - 1, max(c[1] for c in S.cells) + 1
    y0, y1 = min(c[2] for c in S.cells) - 1, max(c[3] for c in S.cells) + 1
    return [(F(rng.randint(int(x0 * den), int(x1 * den)), den), F(rng.randint(int(y0 * den), int(y1 * den)), den)) for _ in range(k)]


def ring(x, K=40, N=1000):
    """The points x + (i, j) / N with max(|i|, |j|) = K."""
    out = []
    for i in range(-K, K + 1):
        out += [(x[0] + F(i, N), x[1] + F(K, N)), (x[0] + F(i, N), x[1] - F(K, N))]
        out += [(x[0] + F(K, N), x[1] + F(i, N)), (x[0] - F(K, N), x[1] + F(i, N))]
    return out


class TestGrow(unittest.TestCase):
    def test_box_grows_to_a_rounded_box(self):
        r = F(1, 2)
        G = grow(box(0, 3, 0, 2), r)
        rng = random.Random(1)
        pts = points(rng, 600, -1, 4, 10) + [(F(3) + F(3, 10), F(2) + F(4, 10)), (F(-1, 2), F(1)), (F(1), F(5, 2))]
        for x in pts:
            d2 = d2_rect((F(0), F(3), F(0), F(2)), x)
            expect = "in" if d2 < r * r else ("on" if d2 == r * r else "out")
            self.assertEqual(G.classify(x), expect, x)

    def test_random_trees_against_brute_force(self):
        rng = random.Random(2)
        for _ in range(25):
            tree = random_tree(rng, rng.randint(1, 4))
            r = rng.choice([F(1, 2), F(3, 4), F(1, 3)])
            G = grow(tree, r)
            for x in near(rng, G.S, 60):
                d2 = d2_to_solid(G.S, x)
                if d2 is None:
                    self.assertEqual(G.classify(x), "out")
                    continue
                self.assertEqual(G.contains(x), d2 <= r * r)
                if d2 != r * r:
                    self.assertEqual(G.classify(x), "in" if d2 < r * r else "out")
                else:
                    # At distance exactly r, x is on the boundary when points nearby are farther.
                    outside = any(d2_to_solid(G.S, y) > r * r for y in ring(x))
                    self.assertEqual(G.classify(x), "on" if outside else "in", x)

    def test_union_identity_and_intersection_inclusion(self):
        rng = random.Random(3)
        for _ in range(12):
            A, B = random_tree(rng, 2), random_tree(rng, 2)
            r = F(1, 2)
            GA, GB, GU, GI = grow(A, r), grow(B, r), grow(union(A, B), r), grow(inter(A, B), r)
            for x in points(rng, 50):
                self.assertEqual(GU.contains(x), GA.contains(x) or GB.contains(x))
                if GI.contains(x):
                    self.assertTrue(GA.contains(x) and GB.contains(x))
        # The inclusion is strict: two disjoint squares at distance 1.
        A, B, r = box(0, 1, 0, 1), box(2, 3, 0, 1), F(3, 4)
        x = (F(3, 2), F(1, 2))
        self.assertTrue(grow(A, r).contains(x) and grow(B, r).contains(x))
        self.assertFalse(grow(inter(A, B), r).contains(x))

    def test_degenerate_contacts(self):
        r = F(1, 2)
        # A square hole of half side r closes exactly: its center is an interior point.
        G = grow(diff(box(0, 3, 0, 3), box(1, 2, 1, 2)), r)
        self.assertEqual(G.classify((F(3, 2), F(3, 2))), "in")
        # Two squares at distance 2r merge along a segment, which is interior except at its ends.
        G = grow(union(box(0, 1, 0, 1), box(2, 3, 0, 1)), r)
        self.assertEqual(G.classify((F(3, 2), F(1, 2))), "in")
        self.assertEqual(G.classify((F(3, 2), F(0))), "on")
        self.assertEqual(G.classify((F(3, 2), F(-1, 100))), "out")


class TestShrink(unittest.TestCase):
    def test_box_shrinks_to_a_box(self):
        r = F(1, 2)
        G = grow(box(0, 4, 0, 2), r)
        rng = random.Random(4)
        for x in points(rng, 500, -1, 5, 8):
            inner = (F(1, 2), F(7, 2), F(1, 2), F(3, 2))
            inside = inner[0] < x[0] < inner[1] and inner[2] < x[1] < inner[3]
            closed = inner[0] <= x[0] <= inner[1] and inner[2] <= x[1] <= inner[3]
            self.assertEqual(shrink_classify(G, r, x), "in" if inside else ("on" if closed else "out"), x)

    def test_random_trees_against_brute_force(self):
        rng = random.Random(5)
        for _ in range(25):
            tree = random_tree(rng, rng.randint(1, 4))
            r = rng.choice([F(1, 2), F(1, 3)])
            G = grow(tree, r)
            for x in near(rng, G.S, 60):
                if not G.S.contains(x):
                    self.assertEqual(shrink_classify(G, r, x), "out")
                    continue
                d2 = d2_to_complement(G.S, x)
                if d2 != r * r:
                    self.assertEqual(shrink_classify(G, r, x), "in" if d2 > r * r else "out")
                else:
                    deeper = any(G.S.contains(y) and d2_to_complement(G.S, y) > r * r for y in ring(x))
                    self.assertEqual(shrink_classify(G, r, x), "on" if deeper else "out", x)

    def test_regularization(self):
        r = F(1, 2)
        # A slab of width exactly 2r shrinks to a segment, which regularization removes.
        self.assertEqual(shrink_classify(box(0, 1, 0, 3), r, (F(1, 2), F(1))), "out")
        # A square of side 2r shrinks to its center, which regularization removes.
        self.assertEqual(shrink_classify(box(0, 1, 0, 1), r, (F(1, 2), F(1, 2))), "out")
        # In an L shape the shrunk left arm touches the line y = r at a point below the reflex corner.
        L = diff(box(-2, 2, 0, 3), box(0, 2, 1, 3))
        self.assertEqual(shrink_classify(L, r, (F(0), F(1, 2))), "on")
        self.assertEqual(shrink_classify(L, r, (F(-1), F(1, 2))), "on")
        self.assertEqual(shrink_classify(L, r, (F(1), F(1, 2))), "out")
        self.assertEqual(shrink_classify(L, r, (F(-1, 5), F(51, 100))), "in")
        self.assertEqual(shrink_classify(L, r, (F(-1, 20), F(51, 100))), "out")

    def test_nonpositive_distance_is_rejected(self):
        with self.assertRaises(ValueError):
            grow(box(0, 1, 0, 1), 0)


if __name__ == "__main__":
    unittest.main()
