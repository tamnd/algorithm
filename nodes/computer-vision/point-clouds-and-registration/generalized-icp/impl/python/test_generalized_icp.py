# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-icp/. The authors are listed in prov/W2QK6S.jsonl.
import math
import random
import unittest

from cvgeom import add_noise, axis_angle_to_R, random_rotation
from cvla import det, matvec, mul, svd, transpose
from generalized_icp import (generalized_icp, minimize_fixed_weights,
                             plane_covariances, transform, weighted_cost,
                             weights)

TOL_ICP = 1e-6
ZERO = [[0.0] * 3 for _ in range(3)]
EYE = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


def rot_angle(R1, R2):
    """The angle of R1^T R2: arccos((tr - 1) / 2), computed with atan2."""
    m = mul(transpose(R1), R2)
    c = (m[0][0] + m[1][1] + m[2][2] - 1.0) / 2.0
    s = 0.5 * math.sqrt((m[2][1] - m[1][2]) ** 2 + (m[0][2] - m[2][0]) ** 2 + (m[1][0] - m[0][1]) ** 2)
    return math.atan2(s, c)


def kabsch(P, Y):
    """Reference closed form for point-to-point pairs, with the sign fix."""
    n = len(P)
    pc = [sum(p[k] for p in P) / n for k in range(3)]
    yc = [sum(y[k] for y in Y) / n for k in range(3)]
    H = [[sum((p[i] - pc[i]) * (y[j] - yc[j]) for p, y in zip(P, Y)) for j in range(3)] for i in range(3)]
    U, _, V = svd(H)
    d = 1.0 if det(mul(V, transpose(U))) >= 0 else -1.0
    R = mul(mul(V, [[1, 0, 0], [0, 1, 0], [0, 0, d]]), transpose(U))
    return R, [yc[i] - sum(R[i][k] * pc[k] for k in range(3)) for i in range(3)]


def surface_scene(k=12, n=70, seed=1):
    g = [-1.0 + 2.0 * i / (k - 1) for i in range(k)]
    B = [[x, y, 0.3 * math.sin(2 * x) * math.cos(1.5 * y) + 0.1 * x * x] for x in g for y in g]
    rng = random.Random(seed)
    sel = rng.sample(range(len(B)), n)
    R = axis_angle_to_R([1.0, 2.0, 3.0], math.radians(10.0))
    t = [0.05, -0.03, 0.04]
    Rt = transpose(R)
    A = [[sum(Rt[i][c] * (B[j][c] - t[c]) for c in range(3)) for i in range(3)] for j in sel]
    return A, B, R, t


class TestGeneralizedICP(unittest.TestCase):
    def test_plane_to_plane_exact_recovery(self):
        A, B, R, t = surface_scene()
        Rf, tf, costs = generalized_icp(A, B, plane_covariances(A), plane_covariances(B))
        self.assertLess(rot_angle(R, Rf), TOL_ICP)
        self.assertLess(max(abs(a - b) for a, b in zip(t, tf)), TOL_ICP)
        self.assertLess(costs[-1], 1e-12)
        self.assertAlmostEqual(det(Rf), 1.0, places=12)

    def test_point_to_point_case_matches_kabsch(self):
        # C^A = 0 and C^B = I: the fixed-pair minimum is the Kabsch solution.
        rng = random.Random(2)
        A = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(15)]
        B = add_noise(rng, transform(axis_angle_to_R([0, 0, 1], 0.4), [0.2, -0.1, 0.0], A), 0.05)
        pairs = [(i, i) for i in range(len(A))]
        Ms = weights(EYE, [ZERO] * 15, [EYE] * 15, pairs)
        R, t = minimize_fixed_weights(EYE, [0.0, 0.0, 0.0], A, B, pairs, Ms)
        Rk, tk = kabsch(A, B)
        self.assertLess(rot_angle(R, Rk), 1e-8)
        self.assertLess(max(abs(a - b) for a, b in zip(t, tk)), 1e-8)

    def test_fixed_pair_minimum_against_random_motions(self):
        # Brute force: no random small change of the result has a lower cost.
        A, B, _, _ = surface_scene(k=8, n=25, seed=3)
        rng = random.Random(3)
        B = add_noise(rng, B, 0.01)
        CA, CB = plane_covariances(A, k=8), plane_covariances(B, k=8)
        pairs = [(i, i) for i in range(10)]
        Bp = [B[i] for i in range(10)]
        CBp = [CB[i] for i in range(10)]
        Ms = weights(axis_angle_to_R([0.0, 0.0, 0.1]), CA, CBp, pairs)
        R, t = minimize_fixed_weights(EYE, [0.0, 0.0, 0.0], A, Bp, pairs, Ms, steps=50)
        best = weighted_cost(R, t, A, Bp, pairs, Ms)
        for _ in range(200):
            dR = axis_angle_to_R([rng.gauss(0, 1e-3) for _ in range(3)])
            R2 = mul(dR, R)
            t2 = [v + rng.gauss(0, 1e-3) for v in t]
            self.assertGreaterEqual(weighted_cost(R2, t2, A, Bp, pairs, Ms), best - 1e-12)

    def test_plane_covariance_shape(self):
        rng = random.Random(4)
        R = random_rotation(rng)
        pts = transform(R, [0.0, 0.0, 0.0], [[rng.uniform(-1, 1), rng.uniform(-1, 1), 0.0] for _ in range(30)])
        normal = [R[0][2], R[1][2], R[2][2]]
        tangent = [R[0][0], R[1][0], R[2][0]]
        for C in plane_covariances(pts, k=8, eps=1e-3):
            cn, ct = matvec(C, normal), matvec(C, tangent)
            for c in range(3):
                self.assertAlmostEqual(cn[c], 1e-3 * normal[c], places=9)
                self.assertAlmostEqual(ct[c], tangent[c], places=9)

    def test_d_max_too_small(self):
        A, B, _, _ = surface_scene(k=6, n=10)
        with self.assertRaises(ValueError):
            generalized_icp(A, B, [ZERO] * len(A), [EYE] * len(B), d_max=1e-6)


if __name__ == "__main__":
    unittest.main()
