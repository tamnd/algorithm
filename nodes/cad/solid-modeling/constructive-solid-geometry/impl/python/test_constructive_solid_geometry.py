# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constructive-solid-geometry/. The authors are listed in prov/QD8QB3.jsonl.

import itertools
import random
import unittest
from fractions import Fraction

from constructive_solid_geometry import ALL, IN, ON, OUT, Box, Move, Op, mat_vec, octant, rotation

HALF = Fraction(1, 2)
QUARTER = Fraction(1, 4)


def det(r):
    return (r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1])
            - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
            + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0]))


def random_tree(rng, depth):
    if depth == 0 or rng.random() < 0.25:
        lo = [rng.randrange(0, 5) for _ in range(3)]
        hi = [a + rng.randrange(1, 4) for a in lo]
        return Box(lo, hi)
    r = rng.random()
    if r < 0.15:
        rot = rotation(rng.randrange(3), rng.randrange(4))
        t = [rng.randrange(-2, 3) for _ in range(3)]
        return Move(random_tree(rng, depth - 1), rot, t)
    kind = "union" if r < 0.55 else "intersection" if r < 0.7 else "difference"
    return Op(kind, random_tree(rng, depth - 1), random_tree(rng, depth - 1))


def cells_of(tree):
    """The brute force: the unit cells whose centres are in the ordinary set.
    Every leaf plane is an integer plane, so no centre is on a plane, and the
    regularized solid is the union of these closed cells."""
    lo, hi = tree.bound()
    out = set()
    for c in itertools.product(*(range(lo[j] - 1, hi[j] + 1) for j in range(3))):
        if tree.raw(tuple(x + HALF for x in c)):
            out.add(c)
    return out


def cell_of(q):
    return tuple(int(x // 1) for x in q)


def brute_classify(cells, p):
    """IN, ON or OUT from the closed cells that contain p."""
    around = [cell_of(tuple(p[j] + s[j] * QUARTER for j in range(3))) for s in map(octant, range(8))]
    n = sum(1 for c in around if c in cells)
    return IN if n == 8 else OUT if n == 0 else ON


class CSGTests(unittest.TestCase):
    def test_rotations(self):
        self.assertEqual(mat_vec(rotation(2, 1), (1, 0, 0)), (0, 1, 0))
        self.assertEqual(mat_vec(rotation(0, 1), (0, 1, 0)), (0, 0, 1))
        self.assertEqual(mat_vec(rotation(1, 1), (0, 0, 1)), (1, 0, 0))
        mats = set()
        for a, k, b, l in itertools.product(range(3), range(4), range(3), range(4)):
            r1, r2 = rotation(a, k), rotation(b, l)
            m = tuple(tuple(sum(r1[i][x] * r2[x][j] for x in range(3)) for j in range(3)) for i in range(3))
            self.assertEqual(det(m), 1)
            mats.add(m)
        self.assertEqual(len(mats), 24)  # the rotation group of the cube

    def test_regularized_difference(self):
        a = Box((0, 0, 0), (2, 2, 2))
        b = Box((1, 0, 0), (3, 2, 2))
        t = a - b
        p = (1, 1, 1)
        self.assertFalse(t.raw(p))  # the ordinary difference loses the face x = 1
        self.assertEqual(t.classify(p), ON)  # the regularized one keeps it
        self.assertEqual(t.classify((HALF, 1, 1)), IN)
        self.assertEqual(t.classify((Fraction(3, 2), 1, 1)), OUT)

    def test_dangling_face(self):
        a = Box((0, 0, 0), (2, 2, 2))
        c = Box((2, 0, 0), (4, 2, 2))
        t = a & c
        self.assertTrue(t.raw((2, 1, 1)))  # the ordinary intersection is the face x = 2
        for p in itertools.product(*(range(0, 5) for _ in range(3))):
            self.assertEqual(t.mask(p), 0)
            self.assertEqual(t.classify(p), OUT)

    def test_not_unique(self):
        a = Box((0, 0, 0), (2, 2, 2))
        b = Box((1, 0, 0), (3, 2, 2))
        trees = [a | b, b | a, (a - b) | b, Box((0, 0, 0), (3, 2, 2)),
                 Move(Box((0, -3, 0), (2, 0, 2)), rotation(2, 1), (0, 0, 0)) | b]
        for p in itertools.product(*(range(-2, 9) for _ in range(3))):
            p = tuple(Fraction(x, 2) for x in p)
            self.assertEqual(len({t.classify(p) for t in trees}), 1, p)

    def test_vertex_neighbourhood(self):
        a = Box((0, 0, 0), (2, 2, 2))
        notch = a - Box((1, 1, 1), (3, 3, 3))  # a cube with one corner cut out
        self.assertEqual(notch.mask((1, 1, 1)), ALL & ~(1 << 7))  # all octants but (+,+,+)
        self.assertEqual(notch.classify((1, 1, 1)), ON)
        self.assertEqual(notch.classify((2, 2, 2)), OUT)
        self.assertEqual(notch.classify((2, 1, 1)), ON)

    def test_random_trees(self):
        rng = random.Random(1980)
        on_seen = in_seen = 0
        for trial in range(40):
            tree = random_tree(rng, 4)
            cells = cells_of(tree)
            lo, hi = tree.bound()
            for _ in range(300):
                p = tuple(Fraction(rng.randrange(2 * (lo[j] - 1), 2 * (hi[j] + 1) + 1), 2) for j in range(3))
                want = brute_classify(cells, p)
                got = tree.classify(p)
                self.assertEqual(got, want, (trial, p))
                mask = tree.mask(p)
                for i in range(8):
                    s = octant(i)
                    c = cell_of(tuple(p[j] + s[j] * QUARTER for j in range(3)))
                    self.assertEqual(bool(mask >> i & 1), c in cells)
                on_seen += got == ON
                in_seen += got == IN
            for _ in range(100):  # points on no plane: CLASSIFY is the ordinary formula
                p = tuple(Fraction(7 * rng.randrange(lo[j] - 1, hi[j] + 1) + rng.randrange(1, 7), 7) for j in range(3))
                got = tree.classify(p)
                self.assertIn(got, (IN, OUT))
                self.assertEqual(got == IN, tree.raw(p))
            for c in cells:
                self.assertTrue(all(lo[j] <= c[j] and c[j] + 1 <= hi[j] for j in range(3)))
        self.assertGreater(on_seen, 500, (on_seen, in_seen))
        self.assertGreater(in_seen, 100, (on_seen, in_seen))


if __name__ == "__main__":
    unittest.main()
