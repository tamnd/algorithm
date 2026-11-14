# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-point-inversion/. The authors are listed in prov/BYMVEB.jsonl.

import random
import unittest

from newton_point_inversion import newton_point_inversion
from si1geom import bernstein, dot, norm, patch_derivs, patch_point, sub

Z = [[0, 0, 0, 0], [0, 3, 3, 0], [0, 3, 3, 0], [0, 0, 0, 0]]
BUMP = [[(i, j, Z[i][j]) for j in range(4)] for i in range(4)]


def dense_min(P, p, n):
    """Brute force: the least distance from p over an (n + 1) x (n + 1) grid."""
    m = len(P) - 1
    B = [bernstein(m, i / n) for i in range(n + 1)]
    best = float("inf")
    for i in range(n + 1):
        bu = B[i]
        rows = [tuple(sum(bu[a] * P[a][b][k] for a in range(m + 1)) for k in range(3)) for b in range(m + 1)]
        for j in range(n + 1):
            bv = B[j]
            x = sum(bv[b] * rows[b][0] for b in range(m + 1)) - p[0]
            y = sum(bv[b] * rows[b][1] for b in range(m + 1)) - p[1]
            z = sum(bv[b] * rows[b][2] for b in range(m + 1)) - p[2]
            best = min(best, x * x + y * y + z * z)
    return best ** 0.5


def kkt_holds(P, p, u, v, tol=1e-7):
    r, ru, rv = patch_derivs(P, u, v)[:3]
    w = sub(r, p)
    f, g = dot(w, ru), dot(w, rv)
    scale_ = 1 + norm(w)
    ok_u = abs(f) <= tol * scale_ * norm(ru) or (u == 0.0 and f > 0) or (u == 1.0 and f < 0)
    ok_v = abs(g) <= tol * scale_ * norm(rv) or (v == 0.0 and g > 0) or (v == 1.0 and g < 0)
    return ok_u and ok_v


class TestNewtonPointInversion(unittest.TestCase):
    def test_example_trace(self):
        tr = []
        u, v = newton_point_inversion(BUMP, (1.0, 2.0, 2.5), n_grid=4, trace=tr)
        self.assertEqual(tr[0][:2], (0.5, 0.5))
        self.assertAlmostEqual(tr[1][0], 0.4248826291, places=9)
        self.assertAlmostEqual(u, 0.4274223333, places=9)
        self.assertAlmostEqual(v, 0.5725776667, places=9)
        self.assertAlmostEqual(norm(sub(patch_point(BUMP, u, v), (1.0, 2.0, 2.5))), 0.9689144476, places=9)
        self.assertEqual(len(tr), 5)

    def test_quadratic_convergence(self):
        tr = []
        newton_point_inversion(BUMP, (0.5, 2.0, 2.0), n_grid=4, trace=tr)
        e = [max(abs(t[3]), abs(t[4])) for t in tr]
        for k in range(1, len(e) - 1):
            if e[k] > 1e-10:
                self.assertLessEqual(e[k + 1], 0.2 * e[k] ** 2)

    def test_inversion_of_points_on_the_patch(self):
        rng = random.Random(3)
        for _ in range(40):
            u0, v0 = rng.uniform(0.02, 0.98), rng.uniform(0.02, 0.98)
            u, v = newton_point_inversion(BUMP, patch_point(BUMP, u0, v0))
            self.assertAlmostEqual(u, u0, places=9)
            self.assertAlmostEqual(v, v0, places=9)

    def test_edges_and_corners(self):
        flat = [[(i / 3, j / 3, 0) for j in range(4)] for i in range(4)]
        self.assertEqual(newton_point_inversion(flat, (2.0, 0.5, 1.0)), (1.0, 0.5))
        self.assertEqual(newton_point_inversion(flat, (2.0, 2.0, 1.0)), (1.0, 1.0))
        u, v = newton_point_inversion(flat, (-1.0, 0.3, -1.0))
        self.assertEqual(u, 0.0)
        self.assertAlmostEqual(v, 0.3, places=12)

    def test_stationary_start_is_a_pitfall(self):
        p = (1.5, 1.5, 1.0)
        self.assertEqual(newton_point_inversion(BUMP, p, n_grid=2), (0.5, 0.5))
        u, v = newton_point_inversion(BUMP, p, n_grid=3)
        self.assertAlmostEqual(norm(sub(patch_point(BUMP, u, v), p)), 0.6872365853, places=8)

    def test_against_dense_sampling(self):
        rng = random.Random(7)
        for _ in range(60):
            P = [[(i + rng.uniform(-0.3, 0.3), j + rng.uniform(-0.3, 0.3), rng.uniform(-1.5, 1.5))
                  for j in range(4)] for i in range(4)]
            p = (rng.uniform(-0.5, 3.5), rng.uniform(-0.5, 3.5), rng.uniform(-2.0, 2.0))
            u, v = newton_point_inversion(P, p, n_grid=10)
            d = norm(sub(patch_point(P, u, v), p))
            self.assertLessEqual(d, dense_min(P, p, 100) + 1e-9)
            self.assertLessEqual(d, dense_min(P, p, 10) + 1e-9)
            self.assertTrue(kkt_holds(P, p, u, v))


if __name__ == "__main__":
    unittest.main()
