# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algebraic-surface-intersection/. The authors are listed in prov/38DDQS.jsonl.

import random
import unittest
from fractions import Fraction

from algebraic_surface_intersection import algebraic_surface_intersection, substitute
from si1geom import bernstein, patch_point

Z = [[0, 0, 0, 0], [0, 3, 3, 0], [0, 3, 3, 0], [0, 0, 0, 0]]
BUMP = [[(i, j, Z[i][j]) for j in range(4)] for i in range(4)]
SADDLE = [[(i, j, (i - 1.5) * (j - 1.5)) for j in range(4)] for i in range(4)]


def eval_f(f, q):
    return sum(c * q[0] ** a * q[1] ** b * q[2] ** e for (a, b, e), c in f.items())


def random_case(rng):
    P = [[(i + rng.randint(-3, 3) / 8, j + rng.randint(-3, 3) / 8, rng.randint(-24, 24) / 8)
          for j in range(4)] for i in range(4)]
    if rng.random() < 0.5:
        f = {(1, 0, 0): rng.randint(-8, 8) / 8, (0, 1, 0): rng.randint(-8, 8) / 8, (0, 0, 1): 1,
             (0, 0, 0): rng.randint(-8, 8) / 8}
    else:
        cx, cy, cz, R = rng.randint(0, 12) / 4, rng.randint(0, 12) / 4, rng.randint(-4, 4) / 4, rng.randint(4, 8) / 4
        f = {(2, 0, 0): 1, (0, 2, 0): 1, (0, 0, 2): 1, (1, 0, 0): -2 * cx, (0, 1, 0): -2 * cy,
             (0, 0, 1): -2 * cz, (0, 0, 0): cx * cx + cy * cy + cz * cz - R * R}
    return P, f


def crossings(curves, along_v, c):
    """Number of times the polylines cross the line u = c (along_v) or v = c."""
    k = 0 if along_v else 1
    return sum(1 for line in curves for a, b in zip(line, line[1:]) if (a[k] - c) * (b[k] - c) < 0)


def sign_changes(P, f, along_v, c, samples):
    vals = [eval_f(f, patch_point(P, c, t / samples) if along_v else patch_point(P, t / samples, c))
            for t in range(samples + 1)]
    return sum(1 for a, b in zip(vals, vals[1:]) if a * b < 0)


class TestAlgebraicSurfaceIntersection(unittest.TestCase):
    def test_substitution_is_exact(self):
        rng = random.Random(1)
        for _ in range(5):
            P, f = random_case(rng)
            G = substitute(P, f)
            for _ in range(4):
                u, v = Fraction(rng.randint(0, 64), 64), Fraction(rng.randint(0, 64), 64)
                bu, bv = bernstein(len(G) - 1, u), bernstein(len(G[0]) - 1, v)
                g = sum(bu[i] * bv[j] * G[i][j] for i in range(len(bu)) for j in range(len(bv)))
                q = patch_point([[tuple(Fraction(x) for x in p) for p in row] for row in P], u, v)
                self.assertEqual(g, eval_f({e: Fraction(c) for e, c in f.items()}, q))

    def test_example_plane_and_bump(self):
        G = substitute(BUMP, {(0, 0, 1): 1, (0, 0, 0): -1})
        self.assertEqual(G, [[-1, -1, -1, -1], [-1, 2, 2, -1], [-1, 2, 2, -1], [-1, -1, -1, -1]])
        stats = {}
        curves, singular = algebraic_surface_intersection(BUMP, {(0, 0, 1): 1, (0, 0, 0): -1}, stats=stats)
        self.assertEqual(stats["boxes"], 37)
        self.assertEqual(singular, [])
        self.assertEqual(len(curves), 1)
        self.assertEqual(curves[0][0], curves[0][-1])
        for u, v in curves[0]:
            self.assertAlmostEqual(27 * u * (1 - u) * v * (1 - v), 1.0, places=12)

    def test_small_loop_is_found(self):
        curves, singular = algebraic_surface_intersection(BUMP, {(0, 0, 1): 1, (0, 0, 0): -1.68})
        self.assertEqual((len(curves), singular), (1, []))
        self.assertEqual(curves[0][0], curves[0][-1])
        us = [u for u, v in curves[0]]
        self.assertAlmostEqual(max(us) - min(us), 1 / 15, places=6)

    def test_singular_point_is_boxed(self):
        curves, singular = algebraic_surface_intersection(SADDLE, {(0, 0, 1): 1}, max_depth=6)
        self.assertEqual(len(singular), 4)
        for u0, u1, v0, v1 in singular:
            self.assertTrue(u0 <= 0.5 <= u1 and v0 <= 0.5 <= v1)
        self.assertEqual(len(curves), 4)

    def test_against_grid_sign_changes(self):
        rng = random.Random(23)
        lines = [k / 10 + 0.0123 for k in range(10)]
        total = 0
        for _ in range(16):
            P, f = random_case(rng)
            curves, singular = algebraic_surface_intersection(P, f, samples=12)
            self.assertEqual(singular, [])
            for line in curves:
                for u, v in line:
                    self.assertLess(abs(eval_f(f, patch_point(P, u, v))), 1e-9)
            for c in lines:
                for along_v in (True, False):
                    want = sign_changes(P, f, along_v, c, 2000)
                    self.assertEqual(crossings(curves, along_v, c), want)
                    total += want
        self.assertGreater(total, 100)


if __name__ == "__main__":
    unittest.main()
