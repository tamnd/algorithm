# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subdivision-surface-intersection/. The authors are listed in prov/V3H0YK.jsonl.

import random
import unittest
from fractions import Fraction as F

from subdivision_surface_intersection import dot, evaluate, intersect, patch, quarters

SADDLE = [[(0, 0, 0), (0, 1, 0)], [(1, 0, 0), (1, 1, 1)]]  # z = u v
LEVEL = [[(0, 0, F(1, 4)), (0, 1, F(1, 4))], [(1, 0, F(1, 4)), (1, 1, F(1, 4))]]  # z = 1/4


def in_rect(rect, u, v) -> bool:
    u0, u1, v0, v1 = rect
    return u0 <= u <= u1 and v0 <= v <= v1


def crossings(g, n, bits=24):
    """Brute force: the grid edges of [0, 1]^2 with n cells a side on which g changes
    sign, each narrowed by exact bisection to a segment of length 2^-bits."""
    out = []
    for i in range(n + 1):
        for j in range(n + 1):
            a = (F(i, n), F(j, n))
            for b in ((F(i + 1, n), F(j, n)), (F(i, n), F(j + 1, n))):
                if b[0] > 1 or b[1] > 1:
                    continue
                ga, gb = g(*a), g(*b)
                if ga == 0:
                    out.append((a, a))
                    continue
                if gb == 0 or (ga > 0) == (gb > 0):
                    continue
                lo, hi = a, b
                for _ in range(bits):
                    mid = ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2)
                    gm = g(*mid)
                    if gm == 0:
                        lo = hi = mid
                        break
                    if (gm > 0) == (ga > 0):
                        lo = mid
                    else:
                        hi = mid
                out.append((lo, hi))
    return out


def hits(rect, seg) -> bool:
    """True when the closed rectangle meets the short axis-parallel segment."""
    (a, b) = seg
    u0, u1, v0, v1 = rect
    return min(a[0], b[0]) <= u1 and max(a[0], b[0]) >= u0 and min(a[1], b[1]) <= v1 and max(a[1], b[1]) >= v0


class TestSubdivision(unittest.TestCase):
    def test_quarters_reproduce_the_patch(self):
        rng = random.Random(11)
        net = [[(F(i, 3), F(j, 3), F(rng.randint(-8, 8), 8)) for j in range(4)] for i in range(3)]
        P = patch(net)
        for Pk in quarters(quarters(P)[2]):
            u0, u1, v0, v1 = Pk[1]
            for a in (F(0), F(1, 3), F(1)):
                for b in (F(0), F(2, 5), F(1)):
                    self.assertEqual(evaluate(Pk[0], a, b), evaluate(net, u0 + a * (u1 - u0), v0 + b * (v1 - v0)))

    def test_saddle_and_level_plane(self):
        P, Q = patch(SADDLE), patch(LEVEL)
        for eps in (F(1, 16), F(1, 64)):
            leaves = intersect(P, Q, eps)
            self.assertTrue(leaves)
            for leaf in leaves:
                self.assertTrue(leaf["flat"])
                u0, u1, v0, v1 = leaf["rects"][0]
                # The z range of the piece is [u0 v0, u1 v1]: every kept piece meets the curve.
                self.assertTrue(u0 * v0 <= F(1, 4) <= u1 * v1)
                for seg in leaf["segments"]:
                    for x in seg:
                        self.assertEqual(x[2], F(1, 4))
                        self.assertLessEqual(abs(x[0] * x[1] - F(1, 4)), eps)
            # Completeness against the brute force grid of sign changes of u v - 1/4.
            for seg in crossings(lambda u, v: u * v - F(1, 4), 16):
                self.assertTrue(any(hits(leaf["rects"][0], seg) and hits(leaf["rects"][1], seg) for leaf in leaves))

    def test_two_curved_patches(self):
        # Q is the height field z = 1/4 + (s - 1/2)^2 over the unit square, of degree (2, 1).
        Q = patch([[(0, 0, F(1, 2)), (0, 1, F(1, 2))], [(F(1, 2), 0, 0), (F(1, 2), 1, 0)], [(1, 0, F(1, 2)), (1, 1, F(1, 2))]])
        P = patch(SADDLE)
        eps = F(1, 32)
        leaves = intersect(P, Q, eps)
        g = lambda u, v: u * v - F(1, 4) - (u - F(1, 2)) ** 2  # noqa: E731
        # A point (x, y) of both surfaces has parameters (x, y) in P and in Q.
        for seg in crossings(g, 16):
            self.assertTrue(any(hits(leaf["rects"][0], seg) and hits(leaf["rects"][1], seg) for leaf in leaves))
        for leaf in leaves:
            for seg in leaf["segments"]:
                for x in seg:
                    self.assertLessEqual(abs(g(x[0], x[1])), 4 * eps)

    def test_random_bicubic_against_planes(self):
        rng = random.Random(5)
        for _ in range(6):
            net = [[(F(i, 3) + F(rng.randint(-1, 1), 16), F(j, 3) + F(rng.randint(-1, 1), 16), F(rng.randint(-8, 8), 8)) for j in range(4)] for i in range(4)]
            P = patch(net)
            n = (F(rng.randint(-2, 2), 4), F(rng.randint(-2, 2), 4), F(1))
            # The plane n . x = d passes through a point of P, so the curve is not empty.
            d = dot(n, evaluate(net, F(rng.randint(1, 5), 6), F(rng.randint(1, 5), 6)))
            # A planar quadrilateral on n . x = d that covers the box of P.
            corner = lambda x, y: (F(x), F(y), d - n[0] * x - n[1] * y)  # noqa: E731
            Q = patch([[corner(-1, -1), corner(-1, 2)], [corner(2, -1), corner(2, 2)]])
            leaves = intersect(P, Q, F(1, 16))
            for leaf in leaves:
                self.assertTrue(leaf["flat"])
                self.assertEqual(leaf["rects"][1], Q[1])  # a flat patch is never split
            g = lambda u, v: dot(n, evaluate(P[0], u, v)) - d  # noqa: E731
            segs = crossings(g, 12, bits=16)
            self.assertTrue(segs)
            self.assertTrue(any(leaf["segments"] for leaf in leaves))
            for seg in segs:
                self.assertTrue(any(hits(leaf["rects"][0], seg) for leaf in leaves))
            for leaf in leaves:
                for seg in leaf["segments"]:
                    for x in seg:
                        self.assertEqual(dot(n, x), d)

    def test_near_miss_keeps_nothing(self):
        # z = u v stays below 1/16 where x, y <= 1/4, so it misses the small square at z = 1/4,
        # although the boxes of the whole patches overlap.
        Q = patch([[(0, 0, F(1, 4)), (0, F(1, 4), F(1, 4))], [(F(1, 4), 0, F(1, 4)), (F(1, 4), F(1, 4), F(1, 4))]])
        self.assertEqual(intersect(patch(SADDLE), Q, F(1, 64)), [])
        far = patch([[(5, 5, 0), (5, 6, 0)], [(6, 5, 0), (6, 6, 1)]])
        self.assertEqual(intersect(patch(SADDLE), far, F(1, 64)), [])

    def test_coincident_patches_are_flagged(self):
        leaves = intersect(patch(LEVEL), patch(LEVEL), F(1, 64))
        self.assertEqual(len(leaves), 1)
        self.assertTrue(leaves[0]["coplanar"])


if __name__ == "__main__":
    unittest.main()
