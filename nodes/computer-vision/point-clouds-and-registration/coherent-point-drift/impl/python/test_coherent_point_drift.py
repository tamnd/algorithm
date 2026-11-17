# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coherent-point-drift/. The authors are listed in prov/HWYJKB.jsonl.
import math
import random
import unittest

from cvla import det, mul, transpose
from coherent_point_drift import (cpd_affine, cpd_nonrigid, cpd_rigid, e_step,
                                  gaussian_kernel, initial_sigma2)


def rotation(axis, angle):
    """Rotation by angle (radians) about axis, by the Rodrigues formula."""
    n = math.sqrt(sum(a * a for a in axis))
    x, y, z = (a / n for a in axis)
    c, s = math.cos(angle), math.sin(angle)
    d = 1.0 - c
    return [[c + x * x * d, x * y * d - z * s, x * z * d + y * s],
            [y * x * d + z * s, c + y * y * d, y * z * d - x * s],
            [z * x * d - y * s, z * y * d + x * s, c + z * z * d]]


def rot_angle(R1, R2):
    m = mul(transpose(R1), R2)
    c = (m[0][0] + m[1][1] + m[2][2] - 1.0) / 2.0
    s = 0.5 * math.sqrt((m[2][1] - m[1][2]) ** 2 + (m[0][2] - m[2][0]) ** 2 + (m[1][0] - m[0][1]) ** 2)
    return math.atan2(s, c)


def cloud(rng, n, d=3):
    return [[rng.uniform(-1.0, 1.0) for _ in range(d)] for _ in range(n)]


def move(R, s, t, Y):
    return [[s * sum(R[i][k] * y[k] for k in range(len(y))) + t[i] for i in range(len(t))] for y in Y]


def nonincreasing(hist, rel=1e-9):
    return all(b <= a + rel * max(1.0, abs(a)) for a, b in zip(hist, hist[1:]))


class TestEStep(unittest.TestCase):
    def test_columns_sum_to_one_without_outliers(self):
        rng = random.Random(1)
        X, Y = cloud(rng, 12), cloud(rng, 9)
        P, _ = e_step(X, Y, 0.3, 0.0)
        for n in range(12):
            self.assertAlmostEqual(sum(P[m][n] for m in range(9)), 1.0, places=12)

    def test_matches_direct_formula(self):
        rng = random.Random(2)
        X, Y = cloud(rng, 7), cloud(rng, 5)
        sigma2, w, D = 0.4, 0.25, 3
        P, nll = e_step(X, Y, sigma2, w)
        c = (2 * math.pi * sigma2) ** (D / 2) * w / (1 - w) * 5 / 7
        ref_nll = 0.0
        for n, x in enumerate(X):
            e = [math.exp(-sum((a - b) ** 2 for a, b in zip(x, y)) / (2 * sigma2)) for y in Y]
            for m in range(5):
                self.assertAlmostEqual(P[m][n], e[m] / (sum(e) + c), places=12)
            p = w / 7 + (1 - w) / 5 * (2 * math.pi * sigma2) ** (-D / 2) * sum(e)
            ref_nll -= math.log(p)
        self.assertAlmostEqual(nll, ref_nll, places=9)

    def test_far_point_does_not_underflow(self):
        X = [[0.0, 0.0], [1000.0, 0.0]]
        Y = [[0.0, 0.0], [0.1, 0.0]]
        P, nll = e_step(X, Y, 1e-4, 0.1)
        self.assertTrue(math.isfinite(nll))
        self.assertTrue(all(math.isfinite(v) for row in P for v in row))
        self.assertLess(P[0][1] + P[1][1], 1e-12)


class TestRigid(unittest.TestCase):
    def test_exact_recovery(self):
        rng = random.Random(3)
        Y = cloud(rng, 30)
        R0 = rotation([1.0, 2.0, -0.5], math.radians(50))
        s0, t0 = 1.3, [0.4, -0.2, 0.3]
        X = move(R0, s0, t0, Y)
        rng.shuffle(X)
        out = cpd_rigid(X, Y)
        self.assertLess(rot_angle(out["R"], R0), 1e-5)
        self.assertAlmostEqual(out["s"], s0, places=5)
        for a, b in zip(out["t"], t0):
            self.assertAlmostEqual(a, b, places=5)
        self.assertAlmostEqual(det(out["R"]), 1.0, places=12)

    def test_without_scale(self):
        rng = random.Random(4)
        Y = cloud(rng, 25)
        R0 = rotation([0.0, 0.0, 1.0], math.radians(35))
        X = move(R0, 1.0, [0.1, 0.2, 0.0], Y)
        out = cpd_rigid(X, Y, scale=False)
        self.assertEqual(out["s"], 1.0)
        self.assertLess(rot_angle(out["R"], R0), 1e-5)

    def test_noise_and_outliers(self):
        rng = random.Random(5)
        Y = cloud(rng, 40)
        R0 = rotation([0.3, -1.0, 0.4], math.radians(40))
        t0 = [0.2, 0.1, -0.3]
        X = [[v + rng.gauss(0.0, 0.01) for v in p] for p in move(R0, 1.0, t0, Y)]
        X += [[rng.uniform(-2.0, 2.0) for _ in range(3)] for _ in range(15)]
        out = cpd_rigid(X, Y, w=0.3, scale=False)
        self.assertLess(rot_angle(out["R"], R0), math.radians(1.0))
        self.assertTrue(nonincreasing(out["nll"]))

    def test_likelihood_never_rises(self):
        rng = random.Random(6)
        Y = cloud(rng, 20)
        X = [[v + rng.gauss(0.0, 0.05) for v in p]
             for p in move(rotation([1.0, 1.0, 1.0], 0.6), 0.9, [0.3, 0.0, 0.1], Y)]
        out = cpd_rigid(X, Y, w=0.1)
        self.assertGreater(len(out["nll"]), 5)
        self.assertTrue(nonincreasing(out["nll"]))

    def test_two_dimensions(self):
        rng = random.Random(7)
        Y = cloud(rng, 20, 2)
        a = math.radians(30)
        R0 = [[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]]
        X = move(R0, 1.0, [0.5, -0.5], Y)
        out = cpd_rigid(X, Y)
        self.assertAlmostEqual(out["R"][1][0], math.sin(a), places=5)
        self.assertAlmostEqual(out["s"], 1.0, places=5)

    def test_initial_sigma2(self):
        X = [[0.0, 0.0], [2.0, 0.0]]
        Y = [[0.0, 1.0]]
        self.assertAlmostEqual(initial_sigma2(X, Y), (1.0 + 5.0) / (2 * 2 * 1))


class TestAffine(unittest.TestCase):
    def test_exact_recovery(self):
        rng = random.Random(8)
        Y = cloud(rng, 30)
        B0 = [[1.1, 0.2, 0.0], [-0.1, 0.9, 0.15], [0.05, 0.0, 1.2]]
        t0 = [0.1, -0.1, 0.2]
        X = move(B0, 1.0, t0, Y)
        out = cpd_affine(X, Y)
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(out["B"][i][j], B0[i][j], places=4)
        self.assertTrue(nonincreasing(out["nll"]))


class TestNonRigid(unittest.TestCase):
    def test_kernel(self):
        G = gaussian_kernel([[0.0], [1.0]], 1.0)
        self.assertAlmostEqual(G[0][1], math.exp(-0.5))
        self.assertEqual(G[0][0], 1.0)

    def test_objective_never_rises_and_fit_improves(self):
        rng = random.Random(9)
        Y = [[math.cos(2 * math.pi * k / 20), math.sin(2 * math.pi * k / 20)] for k in range(20)]
        X = [[y[0] + 0.15 * math.sin(3 * y[1]), y[1] + 0.1 * y[0] * y[0]] for y in Y]
        X = [[v + rng.gauss(0.0, 0.005) for v in p] for p in X]
        out = cpd_nonrigid(X, Y, beta=1.0, lam=1.0)
        self.assertTrue(nonincreasing(out["nll"]))
        before = sum(min(sum((a - b) ** 2 for a, b in zip(x, y)) for y in Y) for x in X)
        after = sum(min(sum((a - b) ** 2 for a, b in zip(x, y)) for y in out["TY"]) for x in X)
        self.assertLess(after, 0.1 * before)


if __name__ == "__main__":
    unittest.main()
