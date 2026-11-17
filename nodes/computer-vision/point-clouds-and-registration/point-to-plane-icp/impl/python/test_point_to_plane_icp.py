# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-to-plane-icp/. The authors are listed in prov/FSJANG.jsonl.
import math
import random
import unittest

from cvgeom import add_noise, axis_angle_to_R
from cvla import det, mul, transpose
from point_to_plane_icp import (closest_points, linearized_step, plane_error,
                                point_to_plane_icp, transform)

TOL_ICP = 1e-6


def rot_angle(R1, R2):
    """The angle of R1^T R2: arccos((tr - 1) / 2), computed with atan2."""
    m = mul(transpose(R1), R2)
    c = (m[0][0] + m[1][1] + m[2][2] - 1.0) / 2.0
    s = 0.5 * math.sqrt((m[2][1] - m[1][2]) ** 2 + (m[0][2] - m[2][0]) ** 2 + (m[1][0] - m[0][1]) ** 2)
    return math.atan2(s, c)


def surface(k=15):
    """Grid points on z = 0.3 sin(2x) cos(1.5y) + 0.1 x^2 over [-1, 1]^2,
    with their exact unit normals."""
    g = [-1.0 + 2.0 * i / (k - 1) for i in range(k)]
    Q, N = [], []
    for x in g:
        for y in g:
            Q.append([x, y, 0.3 * math.sin(2 * x) * math.cos(1.5 * y) + 0.1 * x * x])
            fx = 0.6 * math.cos(2 * x) * math.cos(1.5 * y) + 0.2 * x
            fy = -0.45 * math.sin(2 * x) * math.sin(1.5 * y)
            s = math.sqrt(fx * fx + fy * fy + 1.0)
            N.append([-fx / s, -fy / s, 1.0 / s])
    return Q, N


def source_from(Q, sel, R, t):
    """Points p with R p + t = q for the selected target points q."""
    Rt = transpose(R)
    return [[sum(Rt[i][k] * (Q[j][k] - t[k]) for k in range(3)) for i in range(3)] for j in sel]


class TestPointToPlane(unittest.TestCase):
    def setUp(self):
        self.Q, self.N = surface()
        self.rng = random.Random(1)
        self.sel = self.rng.sample(range(len(self.Q)), 60)
        self.R = axis_angle_to_R([1.0, 2.0, 3.0], math.radians(10.0))
        self.t = [0.05, -0.03, 0.04]
        self.P = source_from(self.Q, self.sel, self.R, self.t)

    def test_exact_recovery_without_noise(self):
        Rf, tf, costs = point_to_plane_icp(self.P, self.Q, self.N)
        self.assertLess(rot_angle(self.R, Rf), TOL_ICP)
        self.assertLess(max(abs(a - b) for a, b in zip(self.t, tf)), TOL_ICP)
        self.assertAlmostEqual(det(Rf), 1.0, places=12)
        self.assertLess(costs[-1], 1e-20)

    def test_fast_final_convergence(self):
        # Zero residual and a near start: each error is at most the square of
        # the one before (a check of this scene, not a general bound).
        _, _, costs = point_to_plane_icp(self.P, self.Q, self.N)
        for a, b in zip(costs, costs[1:]):
            if a > 1e-12:
                self.assertLessEqual(b, a * a)

    def test_linear_step_is_the_least_squares_minimum(self):
        # Brute force: random changes of the step never lower the linear cost.
        moved = transform(axis_angle_to_R([0.0, 1.0, 0.0], 0.05), [0.02, 0.0, 0.0], self.P)
        idx = closest_points(moved, self.Q)
        tg, nm = [self.Q[j] for j in idx], [self.N[j] for j in idx]
        x = linearized_step(moved, tg, nm)

        def lin_cost(v):
            total = 0.0
            for p, q, n in zip(moved, tg, nm):
                c = [p[1] * n[2] - p[2] * n[1], p[2] * n[0] - p[0] * n[2], p[0] * n[1] - p[1] * n[0]]
                r = sum(n[k] * (p[k] - q[k]) for k in range(3))
                total += (r + sum(c[k] * v[k] for k in range(3)) + sum(n[k] * v[3 + k] for k in range(3))) ** 2
            return total

        best = lin_cost(x)
        rng = random.Random(2)
        for _ in range(300):
            y = [v + rng.gauss(0.0, 1e-3) for v in x]
            self.assertGreaterEqual(lin_cost(y), best - 1e-15)

    def test_plane_is_degenerate(self):
        g = [i / 4.0 for i in range(5)]
        Q = [[x, y, 0.0] for x in g for y in g]
        N = [[0.0, 0.0, 1.0]] * len(Q)
        P = [[x + 0.01, y, 0.02] for x, y, _ in Q]
        with self.assertRaises(ValueError):
            point_to_plane_icp(P, Q, N)

    def test_noisy_source(self):
        P = add_noise(self.rng, self.P, 0.005)
        Rf, tf, costs = point_to_plane_icp(P, self.Q, self.N)
        self.assertLess(rot_angle(self.R, Rf), math.radians(1.0))
        self.assertLess(max(abs(a - b) for a, b in zip(self.t, tf)), 0.02)
        self.assertLess(costs[-1], costs[0])
        moved = transform(Rf, tf, P)
        idx = closest_points(moved, self.Q)
        e = plane_error(moved, [self.Q[j] for j in idx], [self.N[j] for j in idx])
        self.assertLessEqual(e, costs[0])


if __name__ == "__main__":
    unittest.main()
