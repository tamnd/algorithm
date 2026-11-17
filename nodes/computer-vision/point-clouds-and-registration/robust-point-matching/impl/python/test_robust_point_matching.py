# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robust-point-matching/. The authors are listed in prov/P020QC.jsonl.
import math
import random
import unittest

from robust_point_matching import (apply, energy, pose_step, rpm, sinkhorn, softassign,
                                   sq_dists)


def cloud(rng, n):
    return [[rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)] for _ in range(n)]


def objective(X, Y, M, A, t, lam):
    D = sq_dists(X, Y, A, t)
    e = lam * sum((A[i][k] - (1.0 if i == k else 0.0)) ** 2 for i in range(2) for k in range(2))
    return e + sum(M[j][k] * D[j][k] for j in range(len(X)) for k in range(len(Y)))


class TestSoftassign(unittest.TestCase):
    def test_sinkhorn_sums(self):
        rng = random.Random(1)
        M = [[rng.uniform(0.1, 2.0) for _ in range(5)] for _ in range(4)]
        sc = [rng.uniform(0.1, 1.0) for _ in range(4)]
        sr = [rng.uniform(0.1, 1.0) for _ in range(5)]
        sinkhorn(M, sc, sr, 500, 1e-12)
        for j in range(4):
            self.assertAlmostEqual(sum(M[j]) + sc[j], 1.0, places=9)
        for k in range(5):
            self.assertAlmostEqual(sum(M[j][k] for j in range(4)) + sr[k], 1.0, places=9)

    def test_scaling_form(self):
        # M_jk / (slack_j * slack_k) = exp(beta (alpha - d_jk)) after any number
        # of sweeps: Sinkhorn only scales rows and columns.
        rng = random.Random(2)
        X, Y = cloud(rng, 6), cloud(rng, 5)
        A, t = [[1.1, 0.2], [-0.1, 0.9]], [0.1, -0.2]
        beta, alpha = 3.0, 0.2
        D = sq_dists(X, Y, A, t)
        for iters in (1, 3, 50):
            M, sc, sr = softassign(X, Y, A, t, beta, alpha, iters)
            for j in range(6):
                for k in range(5):
                    self.assertAlmostEqual(math.log(M[j][k] / (sc[j] * sr[k])),
                                           beta * (alpha - D[j][k]), places=9)


class TestPoseStep(unittest.TestCase):
    def test_exact_with_hard_matches(self):
        rng = random.Random(3)
        Y = cloud(rng, 6)
        A0, t0 = [[1.2, 0.3], [-0.4, 0.8]], [0.5, -0.7]
        X = [apply(A0, t0, y) for y in Y]
        M = [[1.0 if j == k else 0.0 for k in range(6)] for j in range(6)]
        A, t = pose_step(X, Y, M, 0.0)
        for i in range(2):
            self.assertAlmostEqual(t[i], t0[i], places=9)
            for k in range(2):
                self.assertAlmostEqual(A[i][k], A0[i][k], places=9)

    def test_minimizes_the_penalized_cost(self):
        rng = random.Random(4)
        X, Y = cloud(rng, 5), cloud(rng, 4)
        M = [[rng.random() for _ in range(4)] for _ in range(5)]
        lam = 0.7
        A, t = pose_step(X, Y, M, lam)
        best = objective(X, Y, M, A, t, lam)
        for _ in range(40):
            B = [[A[i][k] + rng.uniform(-0.05, 0.05) for k in range(2)] for i in range(2)]
            u = [t[i] + rng.uniform(-0.05, 0.05) for i in range(2)]
            self.assertGreater(objective(X, Y, M, B, u, lam), best)


class TestAnnealing(unittest.TestCase):
    def test_energy_never_rises_at_fixed_beta(self):
        rng = random.Random(5)
        Y = cloud(rng, 8)
        X = [apply([[0.9, -0.3], [0.3, 0.9]], [0.2, 0.1], y) for y in Y] + cloud(rng, 2)
        A, t = [[1.0, 0.0], [0.0, 1.0]], [0.0, 0.0]
        beta, alpha, lam = 4.0, 0.05, 1.0
        last = None
        for _ in range(15):
            M, sc, sr = softassign(X, Y, A, t, beta, alpha, 2000, 1e-13)
            e1 = energy(X, Y, M, sc, sr, A, t, alpha, lam, beta)
            if last is not None:
                self.assertLessEqual(e1, last + 1e-9)
            A, t = pose_step(X, Y, M, lam)
            last = energy(X, Y, M, sc, sr, A, t, alpha, lam, beta)
            self.assertLessEqual(last, e1 + 1e-9)

    def test_recovers_affine_map_with_outliers(self):
        for seed in (6, 7, 10):
            rng = random.Random(seed)
            Y = cloud(rng, 15)
            A0, t0 = [[0.95, -0.35], [0.25, 1.1]], [0.3, -0.2]
            # X: images of the first 13 points of Y with noise, plus 3 outliers, shuffled.
            # Y[13] and Y[14] have no partner.
            X = [[v + rng.gauss(0.0, 0.01) for v in apply(A0, t0, y)] for y in Y[:13]]
            X += cloud(rng, 3)
            order = list(range(16))
            rng.shuffle(order)
            X = [X[i] for i in order]
            out = rpm(X, Y, alpha=0.04)
            for i in range(2):
                self.assertLess(abs(out["t"][i] - t0[i]), 0.03)
                for k in range(2):
                    self.assertLess(abs(out["A"][i][k] - A0[i][k]), 0.03)
            truth = {(order.index(k), k) for k in range(13)}
            self.assertEqual(set(out["matches"]), truth)

    def test_fixed_small_penalty_can_fail(self):
        # A fixed small penalty from the start lets the affine part collapse:
        # this is why the penalty is annealed.
        rng = random.Random(7)
        Y = cloud(rng, 15)
        A0, t0 = [[0.95, -0.35], [0.25, 1.1]], [0.3, -0.2]
        X = [[v + rng.gauss(0.0, 0.01) for v in apply(A0, t0, y)] for y in Y[:13]]
        X += cloud(rng, 3)
        out = rpm(X, Y, alpha=0.04, lam0=0.01, lam_final=0.01)
        err = max(abs(out["A"][i][k] - A0[i][k]) for i in range(2) for k in range(2))
        self.assertGreater(err, 0.1)


if __name__ == "__main__":
    unittest.main()
