# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ironing/. The authors are listed in prov/Y8ZAS3.jsonl.

import random
import unittest
from fractions import Fraction as F

from ironing import concave_hull, iron, revenue_curve, virtual_values

IRREGULAR = [(2, F(1, 2)), (3, F(1, 6)), (5, F(1, 3))]


def random_dist(rng, k, denom=12):
    values = sorted(rng.sample(range(1, 20), k))
    cuts = sorted(rng.sample(range(1, denom), k - 1))
    parts = [b - a for a, b in zip([0] + cuts, cuts + [denom])]
    return [(v, F(p, denom)) for v, p in zip(values, parts)]


def hull_height(pts, hull, q):
    """The value at q of the piecewise linear function through the hull vertices."""
    for a, b in zip(hull, hull[1:]):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        if x1 <= q <= x2:
            return y1 + (y2 - y1) * (q - x1) / (x2 - x1)
    raise AssertionError("q outside [0, 1]")


class TestIroning(unittest.TestCase):
    def test_example(self):
        self.assertEqual(virtual_values(IRREGULAR), [1, -1, 5])
        self.assertEqual(iron(IRREGULAR), ([F(1, 2), F(1, 2), 5], [(0, 1)]))

    def test_regular_is_unchanged(self):
        d = [(1, F(1, 4)), (2, F(1, 4)), (3, F(1, 4)), (4, F(1, 4))]
        self.assertEqual(iron(d), (virtual_values(d), []))
        self.assertEqual(iron([(7, 1)]), ([7], []))

    def test_long_ironed_interval(self):
        d = [(1, F(3, 10)), (2, F(1, 10)), (3, F(1, 10)), (4, F(1, 10)), (6, F(2, 5))]
        bar, intervals = iron(d)
        self.assertEqual(bar, [F(-7, 3)] * 4 + [6])
        self.assertEqual(intervals, [(0, 3)])

    def test_hull_properties(self):
        rng = random.Random(1)
        for _ in range(300):
            d = random_dist(rng, rng.randint(1, 7))
            probs = [p for _, p in sorted(d)]
            phi = virtual_values(d)
            bar, intervals = iron(d)
            pts = revenue_curve(d)
            hull = concave_hull(pts)
            # the hull lies on or above every point and touches the two end points
            for q, r in pts:
                self.assertGreaterEqual(hull_height(pts, hull, q), r)
            self.assertEqual(hull[0], 0)
            self.assertEqual(hull[-1], len(pts) - 1)
            # ironed values are nondecreasing and equal the raw ones outside ironed intervals
            self.assertTrue(all(a <= b for a, b in zip(bar, bar[1:])))
            inside = {k for lo, hi in intervals for k in range(lo, hi + 1)}
            for k in range(len(d)):
                if k not in inside:
                    self.assertEqual(bar[k], phi[k])
            # on each ironed interval the mean of phi equals the ironed value
            for lo, hi in intervals:
                mass = sum(probs[lo:hi + 1])
                mean = sum(phi[k] * probs[k] for k in range(lo, hi + 1)) / mass
                self.assertEqual(mean, bar[lo])
            # both have mean equal to the lowest value
            low = min(v for v, _ in d)
            self.assertEqual(sum(f * x for f, x in zip(probs, phi)), low)
            self.assertEqual(sum(f * x for f, x in zip(probs, bar)), low)

    def test_virtual_surplus_inequality(self):
        rng = random.Random(2)
        for _ in range(300):
            d = random_dist(rng, rng.randint(1, 6))
            probs = [p for _, p in sorted(d)]
            phi = virtual_values(d)
            bar, intervals = iron(d)
            # a random nondecreasing allocation x in [0, 1]
            x = sorted(F(rng.randint(0, 6), 6) for _ in d)
            self.assertGreaterEqual(sum(f * a * b for f, a, b in zip(probs, x, bar)),
                                    sum(f * a * b for f, a, b in zip(probs, x, phi)))
            # constant on ironed intervals gives equality
            for lo, hi in intervals:
                for k in range(lo, hi + 1):
                    x[k] = x[lo]
            self.assertEqual(sum(f * a * b for f, a, b in zip(probs, x, bar)),
                             sum(f * a * b for f, a, b in zip(probs, x, phi)))

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            iron([])
        with self.assertRaises(ValueError):
            iron([(1, F(1, 3)), (2, F(1, 3))])


if __name__ == "__main__":
    unittest.main()
