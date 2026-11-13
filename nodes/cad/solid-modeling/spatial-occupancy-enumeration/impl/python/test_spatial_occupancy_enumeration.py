# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spatial-occupancy-enumeration/. The authors are listed in prov/F2JK2W.jsonl.

import itertools
import random
import unittest
from fractions import Fraction

from spatial_occupancy_enumeration import (
    DIFFERENCE, EMPTY, FULL, IN, INTERSECTION, ON, OUT, UNION, VoxelSet,
    from_octree, octree_boolean, octree_size, to_octree,
)

QUARTER = Fraction(1, 4)
OCTANTS = list(itertools.product((-1, 1), repeat=3))
OPS = {"union": UNION, "intersection": INTERSECTION, "difference": DIFFERENCE}


def contains(cells, p, scale=1):
    """Ordinary point membership of p / scale in the closed union of the cells,
    by a scan. With integer p and scale the test is integer arithmetic."""
    return any(all(scale * c[j] <= p[j] <= scale * (c[j] + 1) for j in range(3)) for c in cells)


def brute_classify(a, b, op, p):
    """The class of p against the regularized result of op on the solids a and b,
    from ordinary point membership in a and b only. p is on the half-integer grid,
    so each point p + s/4 is on no grid plane: it is interior to one cell, and the
    ordinary result there agrees with its interior (and so with the regularized
    result) near p. p is in the closure of each of the eight open octants. The
    points are scaled by 4 so that the scan uses integers."""
    k = 0
    for s in OCTANTS:
        q = tuple(int(4 * p[j]) + s[j] for j in range(3))
        k += bool(op(contains(a, q, 4), contains(b, q, 4)))
    return OUT if k == 0 else IN if k == 8 else ON


def random_set(rng, n, density):
    return VoxelSet(c for c in itertools.product(range(n), repeat=3) if rng.random() < density)


def box(lo, hi):
    return VoxelSet(itertools.product(*(range(lo[j], hi[j]) for j in range(3))))


class VoxelTests(unittest.TestCase):
    def test_box_measures(self):
        b = box((0, 0, 0), (3, 4, 5))
        self.assertEqual(b.volume(), 60)
        self.assertEqual(b.area(), 2 * (12 + 20 + 15))
        self.assertEqual(b.classify((0, 0, 0)), ON)
        self.assertEqual(b.classify((1, 1, 1)), IN)
        self.assertEqual(b.classify((3, 2, 2)), ON)
        self.assertEqual(b.classify((Fraction(7, 2), 2, 2)), OUT)

    def test_regularized_on_shared_faces(self):
        a = box((0, 0, 0), (2, 2, 2))
        b = box((2, 0, 0), (4, 2, 2))
        self.assertTrue(contains(a.cells, (2, 1, 1)) and contains(b.cells, (2, 1, 1)))
        self.assertEqual(len(a.intersection(b)), 0)  # no dangling face
        d = a.difference(box((1, 0, 0), (3, 2, 2)))
        self.assertEqual(d.classify((1, 1, 1)), ON)  # the face x = 1 is kept
        u = a.union(b)
        self.assertEqual(u.classify((2, 1, 1)), IN)  # the shared face is now interior
        self.assertEqual(u.area(), a.area() + b.area() - 2 * 4)

    def test_operations_against_point_membership(self):
        rng = random.Random(1982)
        on_seen = 0
        for trial in range(12):
            a = random_set(rng, 4, 0.45)
            b = random_set(rng, 4, 0.45)
            for name, op in OPS.items():
                r = a.boolean(b, op)
                self.assertEqual(r, getattr(a, name)(b))
                for _ in range(300):
                    p = tuple(Fraction(rng.randrange(-1, 10), 2) for _ in range(3))
                    got = r.classify(p)
                    self.assertEqual(got, brute_classify(a.cells, b.cells, op, p), (trial, name, p))
                    on_seen += got == ON
                for _ in range(40):  # points on no grid plane: the ordinary formula
                    p = tuple(Fraction(rng.randrange(0, 35), 7) for _ in range(3))
                    if any(x.denominator == 1 for x in p):
                        continue
                    want = op(contains(a.cells, p), contains(b.cells, p))
                    self.assertEqual(r.classify(p) == IN, want)
                    self.assertNotEqual(r.classify(p), ON)
        self.assertGreater(on_seen, 1000)

    def test_area_and_volume(self):
        rng = random.Random(7)
        for _ in range(30):
            a = random_set(rng, 4, 0.5)
            b = random_set(rng, 4, 0.5)
            self.assertEqual(a.union(b).volume() + a.intersection(b).volume(), a.volume() + b.volume())
            # brute force area: the unit squares of the grid whose centre is ON
            squares = 0
            for axis in range(3):
                for c in itertools.product(range(-1, 6), repeat=3):
                    centre = tuple(Fraction(c[j]) if j == axis else c[j] + Fraction(1, 2) for j in range(3))
                    squares += a.classify(centre) == ON
            self.assertEqual(a.area(), squares)

    def test_sampling_a_solid(self):
        r = 6
        ball = VoxelSet.from_membership(lambda p: sum((x - r) ** 2 for x in p) <= r * r, (0, 0, 0), (2 * r, 2 * r, 2 * r))
        self.assertEqual(ball.classify((r, r, r)), IN)
        self.assertEqual(ball.volume(), len([c for c in itertools.product(range(2 * r), repeat=3)
                                             if sum((x + Fraction(1, 2) - r) ** 2 for x in c) <= r * r]))
        # The error is only in cells that meet the boundary sphere: a cell wholly
        # inside the ball is kept and a cell wholly outside it is dropped.
        for c in itertools.product(range(-1, 2 * r + 1), repeat=3):
            far = sum(max((x - r) ** 2, (x + 1 - r) ** 2) for x in c)
            near = sum((max(x, min(r, x + 1)) - r) ** 2 for x in c)  # the nearest point of the cell
            if far <= r * r:
                self.assertIn(c, ball.cells)
            if near > r * r:
                self.assertNotIn(c, ball.cells)
        self.assertEqual(from_octree(to_octree(ball, 4), 4), ball)
        # The ball is convex, so each grid line meets the sample in one run of
        # cells, and the area is twice the number of lines that meet it.
        lines = {(a, tuple(c[j] for j in range(3) if j != a)) for c in ball.cells for a in range(3)}
        self.assertEqual(ball.area(), 2 * len(lines))

    def test_octree_round_trip_and_booleans(self):
        rng = random.Random(1980)
        self.assertEqual(to_octree(box((0, 0, 0), (8, 8, 8)), 3), FULL)
        self.assertEqual(to_octree(VoxelSet(), 3), EMPTY)
        with self.assertRaises(ValueError):
            to_octree(VoxelSet([(8, 0, 0)]), 3)
        for _ in range(40):
            lo = [rng.randrange(0, 8) for _ in range(3)]
            hi = [rng.randrange(x + 1, 9) for x in lo]
            a = box(lo, hi).union(random_set(rng, 8, 0.05))
            b = random_set(rng, 8, rng.choice((0.1, 0.5, 0.9)))
            ta, tb = to_octree(a, 3), to_octree(b, 3)
            self.assertEqual(from_octree(ta, 3), a)
            self.assertEqual(from_octree(tb, 3), b)
            for op in OPS.values():
                t = octree_boolean(ta, tb, op)
                self.assertEqual(from_octree(t, 3), a.boolean(b, op))
                self.assertEqual(t, to_octree(a.boolean(b, op), 3))  # the result is reduced
            self.assertLessEqual(octree_size(ta), 1 + 8 + 64 + 512)


if __name__ == "__main__":
    unittest.main()
