# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/teaser-registration/. The authors are listed in prov/E0TQ57.jsonl.
import itertools
import math
import random
import unittest

from cvla import det, mul, transpose
from teaser_registration import (adaptive_voting, gnc_tls_rotation, max_clique,
                                 teaser, tls_cost, weighted_wahba)


def rotation(axis, angle):
    n = math.sqrt(sum(a * a for a in axis))
    x, y, z = (a / n for a in axis)
    c, s = math.cos(angle), math.sin(angle)
    d = 1.0 - c
    return [[c + x * x * d, x * y * d - z * s, x * z * d + y * s],
            [y * x * d + z * s, c + y * y * d, y * z * d - x * s],
            [z * x * d - y * s, z * y * d + x * s, c + z * z * d]]


def random_rotation(rng):
    q = [rng.gauss(0.0, 1.0) for _ in range(4)]
    n = math.sqrt(sum(v * v for v in q))
    w, x, y, z = (v / n for v in q)
    return [[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]]


def rot_angle(R1, R2):
    m = mul(transpose(R1), R2)
    c = (m[0][0] + m[1][1] + m[2][2] - 1.0) / 2.0
    s = 0.5 * math.sqrt((m[2][1] - m[1][2]) ** 2 + (m[0][2] - m[2][0]) ** 2 + (m[1][0] - m[0][1]) ** 2)
    return math.atan2(s, c)


def make_problem(rng, m, n_out, noise, s=1.0):
    R = random_rotation(rng)
    t = [rng.uniform(-1.0, 1.0) for _ in range(3)]
    A = [[rng.uniform(-1.0, 1.0) for _ in range(3)] for _ in range(m)]
    B = []
    for a in A:
        Ra = [sum(R[i][k] * a[k] for k in range(3)) for i in range(3)]
        B.append([s * Ra[i] + t[i] + rng.gauss(0.0, noise) for i in range(3)])
    out = rng.sample(range(m), n_out)
    for i in out:
        B[i] = [rng.uniform(-2.0, 2.0) for _ in range(3)]
    return R, t, A, B, set(range(m)) - set(out)


class TestAdaptiveVoting(unittest.TestCase):
    def brute(self, values, bounds, cbar):
        best = math.inf
        for r in range(1, len(values) + 1):
            for S in itertools.combinations(range(len(values)), r):
                w = [1.0 / bounds[k] ** 2 for k in S]
                x = sum(wk * values[k] for wk, k in zip(w, S)) / sum(w)
                best = min(best, tls_cost(x, values, bounds, cbar))
        return best

    def test_against_all_subsets(self):
        rng = random.Random(1)
        for _ in range(40):
            K = rng.randint(1, 8)
            values = [rng.uniform(-3.0, 3.0) for _ in range(K)]
            bounds = [rng.uniform(0.1, 1.0) for _ in range(K)]
            cbar = rng.choice([0.5, 1.0, 2.0])
            x, S = adaptive_voting(values, bounds, cbar)
            self.assertAlmostEqual(tls_cost(x, values, bounds, cbar), self.brute(values, bounds, cbar), places=9)

    def test_no_grid_point_is_better(self):
        rng = random.Random(2)
        for _ in range(20):
            K = rng.randint(2, 12)
            values = [rng.uniform(-3.0, 3.0) for _ in range(K)]
            bounds = [rng.uniform(0.1, 1.0) for _ in range(K)]
            x, _ = adaptive_voting(values, bounds)
            f = tls_cost(x, values, bounds)
            grid = min(tls_cost(-5.0 + 10.0 * g / 4000, values, bounds) for g in range(4001))
            self.assertLessEqual(f, grid + 1e-12)

    def test_example_from_page(self):
        x, S = adaptive_voting([1.0, 1.1, 0.9, 3.0, 5.0], [0.2] * 5)
        self.assertAlmostEqual(x, 1.0, places=12)
        self.assertEqual(S, [0, 1, 2])

    def test_single_value(self):
        self.assertEqual(adaptive_voting([2.5], [0.1]), (2.5, [0]))


class TestMaxClique(unittest.TestCase):
    def test_against_brute_force(self):
        rng = random.Random(3)
        for _ in range(30):
            n = rng.randint(1, 11)
            p = rng.uniform(0.2, 0.8)
            adj = [set() for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    if rng.random() < p:
                        adj[i].add(j)
                        adj[j].add(i)
            C = max_clique(n, adj)
            for i, j in itertools.combinations(C, 2):
                self.assertIn(j, adj[i])
            best = 1
            for r in range(2, n + 1):
                if any(all(j in adj[i] for i, j in itertools.combinations(S, 2))
                       for S in itertools.combinations(range(n), r)):
                    best = r
            self.assertEqual(len(C), best)


class TestRotation(unittest.TestCase):
    def test_wahba_exact(self):
        rng = random.Random(4)
        R = random_rotation(rng)
        U = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(6)]
        V = [[sum(R[i][k] * u[k] for k in range(3)) for i in range(3)] for u in U]
        Rh = weighted_wahba(U, V, [1.0] * 6)
        self.assertLess(rot_angle(R, Rh), 1e-9)
        self.assertAlmostEqual(det(Rh), 1.0, places=12)

    def test_gnc_rejects_outliers(self):
        rng = random.Random(5)
        R = random_rotation(rng)
        U = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(40)]
        V = [[sum(R[i][k] * u[k] for k in range(3)) + rng.gauss(0, 0.005) for i in range(3)] for u in U]
        for k in range(16):
            V[k] = [rng.uniform(-1.5, 1.5) for _ in range(3)]
        Rh, w = gnc_tls_rotation(U, V, [0.05] * 40)
        self.assertLess(rot_angle(R, Rh), math.radians(1.0))
        self.assertEqual(sum(1 for x in w[16:] if x > 0.5), 24)


class TestTeaser(unittest.TestCase):
    def test_inliers_form_a_clique(self):
        rng = random.Random(6)
        R, t, A, B, inl = make_problem(rng, 40, 20, 0.005)
        out = teaser(A, B, beta=0.03, scale=1.0)
        self.assertGreaterEqual(len(out["clique"]), len(inl))

    def test_known_scale_high_outlier_rate(self):
        rng = random.Random(7)
        R, t, A, B, inl = make_problem(rng, 60, 51, 0.005)
        out = teaser(A, B, beta=0.03, scale=1.0)
        self.assertLess(rot_angle(R, out["R"]), math.radians(2.0))
        for a, b in zip(out["t"], t):
            self.assertLess(abs(a - b), 0.03)
        self.assertTrue(inl <= set(out["inliers"]))

    def test_unknown_scale(self):
        rng = random.Random(8)
        R, t, A, B, inl = make_problem(rng, 40, 24, 0.002, s=1.7)
        out = teaser(A, B, beta=0.01)
        self.assertLess(abs(out["s"] - 1.7), 0.02)
        self.assertLess(rot_angle(R, out["R"]), math.radians(1.0))

    def test_exact_data(self):
        rng = random.Random(9)
        R, t, A, B, _ = make_problem(rng, 12, 0, 0.0)
        out = teaser(A, B, beta=1e-6, scale=1.0)
        self.assertLess(rot_angle(R, out["R"]), 1e-6)
        self.assertEqual(out["clique"], list(range(12)))


if __name__ == "__main__":
    unittest.main()
