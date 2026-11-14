# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/levin-quadric-intersection/. The authors are listed in prov/NA927X.jsonl.

import random
import unittest
from math import sqrt

from levin_quadric_intersection import (
    _normalized, _upper, levin_intersection, pencil_candidates, pencil_cubic,
    quadric_value, ruled_sheets, ruling_roots, _combo,
)
from si1geom import add, dot, jacobi_eigen, norm, scale, solve, sub

SPHERE2 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -4]]
US = [i / 20 for i in range(-60, 61)]


def residual(Q, p):
    return abs(quadric_value(_normalized(Q), p)) / (1 + dot(p, p))


def gradient(Q, x):
    return tuple(2 * (sum(Q[i][j] * x[j] for j in range(3)) + Q[i][3]) for i in range(3))


def point_on_both(S, T, x, steps=60):
    """A point of S = T = 0 near x, by minimum norm Newton steps, or None."""
    for _ in range(steps):
        F = (quadric_value(S, x), quadric_value(T, x))
        if max(abs(F[0]), abs(F[1])) < 1e-14:
            return x
        gs, gt = gradient(S, x), gradient(T, x)
        try:
            y = solve([[dot(gs, gs), dot(gs, gt)], [dot(gt, gs), dot(gt, gt)]], list(F))
        except ZeroDivisionError:
            return None
        x = sub(x, add(scale(y[0], gs), scale(y[1], gt)))
        if norm(x) > 50:
            return None
    return None


def covered(res, x):
    """True when x lies on a sheet of the member and the quadratic of its
    ruling has a root at x, or the whole ruling is in both quadrics."""
    G = res["partner"]
    for sh in res["sheets"]:
        u = sh.param(x)
        if sh.kind == "hyperbolic cylinder" and abs(u) < 1e-12:
            continue
        p, d = sh.point(u), sh.direction(u)
        v = dot(sub(x, p), d) / dot(d, d)
        if norm(sub(add(p, scale(v, d)), x)) > 1e-7 * (1 + norm(x)):
            continue
        roots = ruling_roots(G, p, d)
        if roots is None or any(abs(r - v) <= 1e-6 * (1 + abs(v)) for r in roots):
            return True
    return False


def random_pair(rng):
    """Two random quadrics through a common random point."""
    A = [[0.0] * 4 for _ in range(4)]
    B = [[0.0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(i, 4):
            A[i][j] = A[j][i] = rng.uniform(-1, 1)
            B[i][j] = B[j][i] = rng.uniform(-1, 1)
    x0 = (rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))
    A[3][3] -= quadric_value(A, x0)
    B[3][3] -= quadric_value(B, x0)
    return A, B, x0


class TestLevin(unittest.TestCase):
    def test_example_viviani(self):
        T = [[1, 0, 0, -1], [0, 1, 0, 0], [0, 0, 0, 0], [-1, 0, 0, 0]]
        res = levin_intersection(SPHERE2, T, [-2, -1, 0, 1, 2])
        self.assertEqual(res["kind"], "parabolic cylinder")
        # the member is a multiple of S - T = z^2 + 2x - 4
        R = res["member"]
        k = R[0][3]
        self.assertGreater(abs(k), 0.1)
        self.assertAlmostEqual(R[2][2] / k, 1.0)
        self.assertAlmostEqual(R[3][3] / k, -4.0)
        self.assertAlmostEqual(R[0][0] / k, 0.0)
        for p in res["points"]:
            self.assertLess(residual(SPHERE2, p), 1e-12)
            self.assertLess(residual(T, p), 1e-12)
        h = sqrt(3) / 2
        for want in ((1.5, h, 1.0), (1.5, -h, 1.0), (1.5, h, -1.0), (1.5, -h, -1.0), (2.0, 0.0, 0.0), (0.0, 0.0, 2.0)):
            self.assertLess(min(norm(sub(p, want)) for p in res["points"]), 1e-5)

    def test_disjoint_spheres(self):
        # radius 1 about (3, 0, 0), against radius 2 about the origin
        T = [[1, 0, 0, -3], [0, 1, 0, 0], [0, 0, 1, 0], [-3, 0, 0, 8]]
        res = levin_intersection(SPHERE2, T, US)
        self.assertEqual(res["kind"], "plane")
        self.assertEqual(res["points"], [])

    def test_parallel_cylinders_vanishing_cubic(self):
        S = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, -1]]
        T = [[1, 0, 0, -1], [0, 1, 0, 0], [0, 0, 0, 0], [-1, 0, 0, 0]]
        self.assertLess(max(abs(c) for c in pencil_cubic(_normalized(S), _normalized(T))), 1e-12)
        res = levin_intersection(S, T, [-1, 0, 1])
        self.assertEqual(res["kind"], "plane")
        self.assertEqual(len(res["points"]), 6)
        for p in res["points"]:
            self.assertAlmostEqual(p[0], 0.5)
            self.assertAlmostEqual(abs(p[1]), sqrt(3) / 2)

    def test_each_kind_of_member(self):
        cases = {
            "hyperbolic cylinder": [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, 0], [0, 0, 0, -1]],
            "intersecting planes": [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            "parallel planes": [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, -1]],
            "double plane": [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            "hyperbolic paraboloid": [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, -0.5], [0, 0, -0.5, 0]],
        }
        rng = random.Random(3)
        for kind, S in cases.items():
            res = levin_intersection(S, SPHERE2, US)
            self.assertEqual(res["kind"], kind)
            self.assertTrue(res["points"])
            for p in res["points"]:
                self.assertLess(residual(S, p), 1e-11)
                self.assertLess(residual(SPHERE2, p), 1e-11)
            for _ in range(20):
                x = (rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(-2, 2))
                y = point_on_both(_normalized(S), _normalized(SPHERE2), x)
                if y is not None:
                    self.assertTrue(covered(res, y), (kind, y))

    def test_pencil_has_a_simple_ruled_root(self):
        # the theorem: some real root of the cubic gives a member that is not
        # semidefinite of rank 2, without the safeguard
        rng = random.Random(11)
        for _ in range(300):
            A, B, _x0 = random_pair(rng)
            S, T = _normalized(A), _normalized(B)
            cands = pencil_candidates(S, T, pencil_cubic(S, T))
            self.assertTrue(cands)
            good = 0
            for a, b in cands:
                R = _combo(a, S, b, T)
                vals = jacobi_eigen(_upper(R))[0]
                self.assertLess(min(abs(v) for v in vals), 1e-8)
                good += ruled_sheets(R, S) is not None
            self.assertGreater(good, 0)

    def test_random_points_satisfy_both_and_all_are_found(self):
        rng = random.Random(7)
        found = 0
        for _ in range(60):
            A, B, x0 = random_pair(rng)
            res = levin_intersection(A, B, US)
            for p in res["points"]:
                self.assertLess(residual(A, p), 1e-9)
                self.assertLess(residual(B, p), 1e-9)
            self.assertTrue(covered(res, x0))
            S, T = _normalized(A), _normalized(B)
            for _ in range(4):
                x = add(x0, (rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)))
                y = point_on_both(S, T, x)
                if y is not None:
                    found += 1
                    self.assertTrue(covered(res, y))
        self.assertGreater(found, 100)


if __name__ == "__main__":
    unittest.main()
