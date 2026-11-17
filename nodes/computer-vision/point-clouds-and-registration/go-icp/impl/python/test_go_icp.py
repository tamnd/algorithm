# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/go-icp/. The authors are listed in prov/AT1CTF.jsonl.
import math
import random
import unittest

from cvgeom import axis_angle_to_R, random_rotation
from cvla import det, mul, transpose
from go_icp import (cost, go_icp, inner_bnb, local_icp, residuals,
                    rotation_uncertainty, transform)

EYE = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
ZERO3 = [0.0, 0.0, 0.0]


def rot_angle(R1, R2):
    """The angle of R1^T R2: arccos((tr - 1) / 2), computed with atan2."""
    m = mul(transpose(R1), R2)
    c = (m[0][0] + m[1][1] + m[2][2] - 1.0) / 2.0
    s = 0.5 * math.sqrt((m[2][1] - m[1][2]) ** 2 + (m[0][2] - m[2][0]) ** 2 + (m[1][0] - m[0][1]) ** 2)
    return math.atan2(s, c)


def scene(n, m, seed, noise=0.0):
    """m target points in [-0.6, 0.6]^3. The source is n of them, moved by
    the inverse of a 150 degree rotation and a translation, plus noise.
    Returns (P, Q, R, t, r) with r the angle-axis vector of R."""
    rng = random.Random(seed)
    Q = [[rng.uniform(-0.6, 0.6) for _ in range(3)] for _ in range(m)]
    sel = rng.sample(range(m), n)
    axis = [1.0, -1.0, 2.0]
    angle = math.radians(150.0)
    R = axis_angle_to_R(axis, angle)
    t = [0.1, -0.05, 0.08]
    P = [[sum(R[k][i] * (Q[s][k] - t[k]) for k in range(3)) + rng.gauss(0.0, noise) for i in range(3)]
         for s in sel]
    na = math.sqrt(sum(a * a for a in axis))
    return P, Q, R, t, [angle * a / na for a in axis]


class TestGoICP(unittest.TestCase):
    def test_global_where_icp_fails(self):
        P, Q, R, t, _ = scene(10, 20, 5)
        self.assertGreater(local_icp(P, Q, EYE, ZERO3)[2], 0.1)
        Rg, tg, E = go_icp(P, Q, 0.01, t_half=0.5)
        self.assertLess(E, 1e-12)
        self.assertLess(rot_angle(R, Rg), 1e-6)
        self.assertLess(max(abs(a - b) for a, b in zip(t, tg)), 1e-6)
        self.assertAlmostEqual(det(Rg), 1.0, places=12)
        self.assertAlmostEqual(cost(Rg, tg, P, Q), E, places=12)

    def test_eps_optimal_against_many_icp_starts(self):
        # Noisy data, so the optimum is above eps and the bounds must prune.
        P, Q, _, _, r = scene(6, 10, 5, noise=0.03)
        eps = 0.014
        rc = [r[0] + 0.2, r[1] - 0.1, r[2] + 0.15]
        Rg, tg, E = go_icp(P, Q, eps, t_half=0.2, r_center=rc, r_half=0.3)
        self.assertGreater(E, eps)
        rng = random.Random(8)
        starts = [random_rotation(rng) for _ in range(60)] + [axis_angle_to_R(r)]
        best = min(local_icp(P, Q, R0, ZERO3)[2] for R0 in starts)
        self.assertLessEqual(E, best + eps)
        self.assertGreaterEqual(best, E - eps)
        self.assertAlmostEqual(cost(Rg, tg, P, Q), E, places=12)

    def test_rotation_uncertainty(self):
        # Theorem 1: ||R_r x - R_r0 x|| <= gamma_r for r in the cube.
        rng = random.Random(3)
        for _ in range(400):
            sigma = rng.choice([0.05, 0.3, 1.0, 2.0])
            r0 = [rng.uniform(-2.0, 2.0) for _ in range(3)]
            r = [c + rng.uniform(-sigma, sigma) for c in r0]
            x = [rng.uniform(-1.0, 1.0) for _ in range(3)]
            nx = math.sqrt(sum(v * v for v in x))
            a = transform(axis_angle_to_R(r), ZERO3, [x])[0]
            b = transform(axis_angle_to_R(r0), ZERO3, [x])[0]
            dist = math.sqrt(sum((p - q) ** 2 for p, q in zip(a, b)))
            self.assertLessEqual(dist, rotation_uncertainty(nx, sigma) + 1e-12)

    def test_residual_lower_bound(self):
        # Theorem 2: e_i(R_r, t) >= e_i(R_r0, t0) - gamma_ri - gamma_t.
        P, Q, _, _, _ = scene(6, 10, 2)
        rng = random.Random(4)
        for _ in range(100):
            sr, st = rng.uniform(0.01, 0.5), rng.uniform(0.01, 0.3)
            r0 = [rng.uniform(-1.5, 1.5) for _ in range(3)]
            t0 = [rng.uniform(-0.3, 0.3) for _ in range(3)]
            r = [c + rng.uniform(-sr, sr) for c in r0]
            t = [c + rng.uniform(-st, st) for c in t0]
            e0 = residuals(transform(axis_angle_to_R(r0), ZERO3, P), t0, Q)
            e = residuals(transform(axis_angle_to_R(r), ZERO3, P), t, Q)
            for p, a, b in zip(P, e, e0):
                g = rotation_uncertainty(math.sqrt(sum(v * v for v in p)), sr) + math.sqrt(3.0) * st
                self.assertGreaterEqual(a, b - g - 1e-12)

    def test_inner_search_against_grid(self):
        # Brute force over a grid of translations: L is below every value
        # and the best value found is within delta of the grid minimum.
        P, Q, _, _, _ = scene(6, 10, 2)
        moved = transform(axis_angle_to_R([0.3, -0.2, 0.5]), ZERO3, P)
        delta = 0.02
        for gam in (0.0, 0.05):
            gammas = [gam] * len(P)
            Et, tb, L = inner_bnb(moved, gammas, Q, ZERO3, 0.4, float("inf"), delta)
            grid = [-0.4 + 0.8 * k / 12 for k in range(13)]
            vals = [sum(max(e - gam, 0.0) ** 2 for e in residuals(moved, [x, y, z], Q))
                    for x in grid for y in grid for z in grid]
            self.assertLessEqual(L, min(vals) + 1e-12)
            self.assertLessEqual(Et, min(vals) + delta)
            self.assertAlmostEqual(sum(max(e - gam, 0.0) ** 2 for e in residuals(moved, tb, Q)), Et, places=12)

    def test_bad_eps(self):
        P, Q, _, _, _ = scene(4, 6, 1)
        with self.assertRaises(ValueError):
            go_icp(P, Q, 0.0)


if __name__ == "__main__":
    unittest.main()
