# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hammersley-sampling-for-cmm/. The authors are listed in prov/9X9MZP.jsonl.

import random
import unittest
from fractions import Fraction

from hammersley_sampling_for_cmm import (
    PRIMES,
    hammersley,
    net_bound,
    niederreiter_bound,
    probe_points_on_patch,
    probe_points_on_rectangle,
    radical_inverse,
    star_discrepancy_2d,
)


def digits(i, base):
    """Base-b digits of i, least significant first."""
    out = []
    while i > 0:
        i, d = divmod(i, base)
        out.append(d)
    return out


def radical_inverse_by_definition(i, base):
    """phi_b(i) = sum_j a_j b^-(j+1) for i = sum_j a_j b^j."""
    return sum((Fraction(a, base ** (j + 1)) for j, a in enumerate(digits(i, base))), Fraction(0))


def star_discrepancy_3d(points):
    """Exact star discrepancy in [0, 1)^3 by the same corner argument as in
    two dimensions; time O(N^4)."""
    pts = [tuple(Fraction(c) for c in p) for p in points]
    n = len(pts)
    axes = [sorted({p[k] for p in pts} | {Fraction(1)}) for k in range(3)]
    best = Fraction(0)
    for x in axes[0]:
        for y in axes[1]:
            for z in axes[2]:
                vol = x * y * z
                op = sum(1 for p in pts if p[0] < x and p[1] < y and p[2] < z)
                cl = sum(1 for p in pts if p[0] <= x and p[1] <= y and p[2] <= z)
                best = max(best, vol - Fraction(op, n), Fraction(cl, n) - vol)
    return best


def local_discrepancy(points, x, y):
    n = len(points)
    count = sum(1 for p, q in points if p < x and q < y)
    return abs(Fraction(count, n) - x * y)


class TestDefinition(unittest.TestCase):
    def test_radical_inverse_matches_definition(self):
        for base in (2, 3, 5, 7):
            for i in range(500):
                self.assertEqual(radical_inverse(i, base), radical_inverse_by_definition(i, base))

    def test_small_values(self):
        self.assertEqual([radical_inverse(i) for i in range(8)],
                         [Fraction(k, 8) for k in (0, 4, 2, 6, 1, 5, 3, 7)])
        self.assertEqual([radical_inverse(i, 3) for i in range(4)],
                         [Fraction(0), Fraction(1, 3), Fraction(2, 3), Fraction(1, 9)])

    def test_points_match_definition(self):
        for n in (1, 2, 7, 16, 50):
            for dim in (1, 2, 3, 4):
                pts = hammersley(n, dim)
                self.assertEqual(len(pts), n)
                for i, p in enumerate(pts):
                    self.assertEqual(p[0], Fraction(i, n))
                    for k in range(1, dim):
                        self.assertEqual(p[k], radical_inverse_by_definition(i, PRIMES[k - 1]))
                    self.assertTrue(all(0 <= c < 1 for c in p))

    def test_van_der_corput_permutation(self):
        # The first b^m values of phi_b are the multiples of b^-m in some order.
        for base, m in ((2, 6), (3, 4), (5, 3)):
            n = base ** m
            got = sorted(radical_inverse(i, base) for i in range(n))
            self.assertEqual(got, [Fraction(k, n) for k in range(n)])

    def test_net_property(self):
        # For N = 2^m, every box of the form
        # [a 2^-j, (a+1) 2^-j) x [c 2^-(m-j), (c+1) 2^-(m-j)) holds one point.
        for m in range(0, 8):
            n = 2 ** m
            pts = hammersley(n, 2)
            for j in range(m + 1):
                counts = {}
                for u, v in pts:
                    key = (int(u * 2 ** j), int(v * 2 ** (m - j)))
                    counts[key] = counts.get(key, 0) + 1
                self.assertEqual(len(counts), n)
                self.assertTrue(all(c == 1 for c in counts.values()))


class TestDiscrepancy(unittest.TestCase):
    def test_brute_force_is_a_supremum(self):
        # No sampled box beats the computed value, and the value is attained
        # in the limit, so random boxes come close on small sets.
        rng = random.Random(11)
        for n in (3, 5, 8, 13):
            pts = [(Fraction(rng.randint(0, 99), 100), Fraction(rng.randint(0, 99), 100)) for _ in range(n)]
            d = star_discrepancy_2d(pts)
            for _ in range(2000):
                x, y = Fraction(rng.randint(0, 1000), 1000), Fraction(rng.randint(0, 1000), 1000)
                self.assertLessEqual(local_discrepancy(pts, x, y), d)
            near = max(
                local_discrepancy(pts, Fraction(a, 1000), Fraction(b, 1000))
                for a in range(0, 1001, 1)
                for b in (0, 1000)
            )
            self.assertLessEqual(near, d)

    def test_known_values(self):
        self.assertEqual(star_discrepancy_2d(hammersley(1)), 1)
        self.assertEqual(star_discrepancy_2d(hammersley(2)), Fraction(3, 4))
        self.assertEqual(star_discrepancy_2d(hammersley(4)), Fraction(1, 2))
        # One point at the center of the square: the worst box is [0,1)^2
        # minus the closed quadrant at the point, or the open quadrant.
        self.assertEqual(star_discrepancy_2d([(Fraction(1, 2), Fraction(1, 2))]), Fraction(3, 4))

    def test_niederreiter_bound_2d(self):
        for n in range(1, 49):
            d = star_discrepancy_2d(hammersley(n, 2))
            self.assertLessEqual(float(d), niederreiter_bound(n, 2))

    def test_net_bound(self):
        for m in range(0, 7):
            n = 2 ** m
            d = star_discrepancy_2d(hammersley(n, 2))
            self.assertLessEqual(d, net_bound(m))

    def test_niederreiter_bound_3d(self):
        for n in (1, 2, 3, 5, 8, 12, 16):
            d = star_discrepancy_3d(hammersley(n, 3))
            self.assertLessEqual(float(d), niederreiter_bound(n, 3))

    def test_empty_disk_bound(self):
        # Lemma 5 of the proof page: an empty disk inside the square has a
        # radius of at most sqrt(2 D*). Centers on a fine grid.
        for n in (16, 64):
            pts = [(float(u), float(v)) for u, v in hammersley(n)]
            bound = (2 * float(star_discrepancy_2d(hammersley(n)))) ** 0.5
            worst = 0.0
            steps = 100
            for a in range(steps + 1):
                for b in range(steps + 1):
                    cx, cy = a / steps, b / steps
                    r = min(((cx - x) ** 2 + (cy - y) ** 2) ** 0.5 for x, y in pts)
                    if min(cx, cy, 1 - cx, 1 - cy) >= r:
                        worst = max(worst, r)
            self.assertGreater(worst, 0.0)
            self.assertLessEqual(worst, bound)

    def test_better_than_random_on_average(self):
        # Measured, not a theorem for each seed: 64 Hammersley points against
        # the mean of ten sets of 64 uniform random points.
        rng = random.Random(12)
        d_h = star_discrepancy_2d(hammersley(64))
        rand = []
        for _ in range(10):
            pts = [(Fraction(rng.randint(0, 9999), 10000), Fraction(rng.randint(0, 9999), 10000)) for _ in range(64)]
            rand.append(star_discrepancy_2d(pts))
        self.assertLess(d_h, sum(rand) / len(rand))


class TestProbePoints(unittest.TestCase):
    def test_rectangle(self):
        pts = probe_points_on_rectangle(8, 10, 20, 40, 16)
        self.assertEqual(pts[0], (10, 20))
        self.assertEqual(pts[1], (15, 28))
        self.assertTrue(all(10 <= x < 50 and 20 <= y < 36 for x, y in pts))

    def test_patch(self):
        def cylinder(u, v):
            # A quarter of a cylinder of radius 5 and height 30: the map from
            # (u, v) scales area by a constant, so the points stay even.
            import math

            t = float(u) * math.pi / 2
            return (5 * math.cos(t), 5 * math.sin(t), 30 * float(v))

        pts = probe_points_on_patch(16, cylinder)
        self.assertEqual(len(pts), 16)
        for x, y, z in pts:
            self.assertAlmostEqual(x * x + y * y, 25.0, places=9)
            self.assertTrue(0 <= z < 30)


if __name__ == "__main__":
    unittest.main()
