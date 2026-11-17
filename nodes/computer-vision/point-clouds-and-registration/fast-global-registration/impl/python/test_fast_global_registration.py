# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-global-registration/. The authors are listed in prov/MFA6WR.jsonl.
import math
import random
import unittest

from cvgeom import axis_angle_to_R, random_rotation
from cvla import mul, transpose
from fast_global_registration import (compose, fgr, fgr_cost, gauss_newton_step,
                                      geman_mcclure, line_process_weight, match_features)


def rot_angle(R1, R2):
    m = mul(transpose(R1), R2)
    c = max(-1.0, min(1.0, (m[0][0] + m[1][1] + m[2][2] - 1.0) / 2.0))
    return math.acos(c)


def make_problem(rng, m, n_out, noise, R=None):
    R = R or random_rotation(rng)
    t = [rng.uniform(-1.0, 1.0) for _ in range(3)]
    P = [[rng.uniform(-1.0, 1.0) for _ in range(3)] for _ in range(m)]
    Q = [[sum(R[i][k] * p[k] for k in range(3)) + t[i] + rng.gauss(0.0, noise) for i in range(3)] for p in P]
    for k in rng.sample(range(m), n_out):
        Q[k] = [rng.uniform(-2.0, 2.0) for _ in range(3)]
    return R, t, P, Q


class TestLineProcess(unittest.TestCase):
    def test_weight_minimizes_and_gives_rho(self):
        for mu in [0.01, 1.0, 25.0]:
            for r2 in [0.0, 0.003, 0.5, 4.0, 100.0]:
                l = line_process_weight(r2, mu)
                best = min(L * r2 + mu * (math.sqrt(L) - 1.0) ** 2 for L in (g / 20000.0 for g in range(20001)))
                val = l * r2 + mu * (math.sqrt(l) - 1.0) ** 2
                self.assertLessEqual(val, best + 1e-9)
                self.assertAlmostEqual(val, geman_mcclure(r2, mu), places=12)

    def test_rho_is_bounded(self):
        self.assertAlmostEqual(geman_mcclure(1e12, 2.0), 2.0, places=9)
        self.assertEqual(geman_mcclure(0.0, 2.0), 0.0)


class TestStep(unittest.TestCase):
    def test_g_is_half_the_gradient(self):
        rng = random.Random(1)
        _, _, P, Q = make_problem(rng, 15, 5, 0.01)
        R, t, mu = axis_angle_to_R([0.2, -0.1, 0.3]), [0.1, 0.0, -0.2], 0.5
        _, _, _, g = gauss_newton_step(P, Q, R, t, mu)
        h = 1e-6
        for a in range(6):
            e = [0.0] * 6
            e[a] = h
            Rp, tp = compose(e, R, t)
            e[a] = -h
            Rm, tm = compose(e, R, t)
            fd = (fgr_cost(P, Q, Rp, tp, mu) - fgr_cost(P, Q, Rm, tm, mu)) / (2 * h)
            self.assertAlmostEqual(fd, 2.0 * g[a], places=5)

    def test_step_is_a_descent_direction(self):
        rng = random.Random(2)
        for _ in range(10):
            _, _, P, Q = make_problem(rng, 20, 8, 0.01)
            R, t = random_rotation(rng), [rng.uniform(-1, 1) for _ in range(3)]
            mu = rng.choice([0.1, 1.0, 10.0])
            xi, _, _, g = gauss_newton_step(P, Q, R, t, mu)
            self.assertLess(sum(a * b for a, b in zip(xi, g)), 0.0)
            e0 = fgr_cost(P, Q, R, t, mu)
            R1, t1 = compose([1e-4 * v for v in xi], R, t)
            self.assertLess(fgr_cost(P, Q, R1, t1, mu), e0)


class TestFGR(unittest.TestCase):
    def test_exact_data_large_rotation(self):
        rng = random.Random(3)
        R = axis_angle_to_R([1.0, 2.0, -1.0], math.radians(150.0))
        R, t, P, Q = make_problem(rng, 30, 0, 0.0, R)
        out = fgr(P, Q, delta=1e-4, max_iter=120)
        self.assertLess(rot_angle(R, out["R"]), 1e-6)
        for a, b in zip(out["t"], t):
            self.assertAlmostEqual(a, b, places=6)

    def test_many_outliers(self):
        for seed in (4, 5):
            rng = random.Random(seed)
            R, t, P, Q = make_problem(rng, 60, 42, 0.005)
            out = fgr(P, Q)
            self.assertLess(rot_angle(R, out["R"]), math.radians(1.0))
            for a, b in zip(out["t"], t):
                self.assertLess(abs(a - b), 0.02)

    def test_weights_separate_inliers(self):
        rng = random.Random(6)
        R, t, P, Q = make_problem(rng, 40, 0, 0.002)
        bad = rng.sample(range(40), 12)
        for k in bad:
            Q[k] = [rng.uniform(-2.0, 2.0) for _ in range(3)]
        out = fgr(P, Q)
        for k, l in enumerate(out["l"]):
            if k in bad:
                self.assertLess(l, 0.1)
            else:
                self.assertGreater(l, 0.9)


class TestMatching(unittest.TestCase):
    def test_reciprocity_and_tuples(self):
        rng = random.Random(7)
        R, t, P, Q = make_problem(rng, 40, 0, 0.0)
        FP = [[rng.uniform(0.0, 10.0) for _ in range(4)] for _ in range(40)]
        FQ = [[f + rng.gauss(0.0, 0.01) for f in fp] for fp in FP]
        swap = rng.sample(range(40), 10)
        for a, b in zip(swap[::2], swap[1::2]):  # five pairs of points trade features
            FQ[a], FQ[b] = FQ[b], FQ[a]
        # All 40 pairs pass the reciprocity test, 10 of them wrong. With few
        # tuples, the tuple test keeps every right pair and drops most wrong ones.
        pairs = match_features(P, Q, FP, FQ, n_tuples=2000, tau=1e-9, rng=random.Random(8))
        self.assertEqual(len(pairs), 40)
        pairs = match_features(P, Q, FP, FQ, n_tuples=200, rng=random.Random(8))
        good = [(i, j) for i, j in pairs if i == j]
        self.assertEqual(len(good), 30)
        self.assertLessEqual(len(pairs) - len(good), 5)


if __name__ == "__main__":
    unittest.main()
