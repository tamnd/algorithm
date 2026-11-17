# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/four-points-congruent-sets/. The authors are listed in prov/2MMXJS.jsonl.
import itertools
import math
import random
import unittest

from cvla import det, mul, transpose
from four_points_congruent_sets import (Grid, apply, base_invariants, congruent_sets, four_pcs,
                                        kabsch, lcp_score, pairs_at_distance, select_base)


def random_rotation(rng):
    q = [rng.gauss(0.0, 1.0) for _ in range(4)]
    n = math.sqrt(sum(v * v for v in q))
    w, x, y, z = (v / n for v in q)
    return [[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]]


def rot_angle(R1, R2):
    m = mul(transpose(R1), R2)
    c = max(-1.0, min(1.0, (m[0][0] + m[1][1] + m[2][2] - 1.0) / 2.0))
    return math.acos(c)


def surface(rng, n, x0=-1.0, x1=1.0):
    pts = []
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(-1.0, 1.0)
        pts.append([x, y, 0.3 * x * y + 0.2 * x * x - 0.1 * y])
    return pts


EXAMPLE_P = [[0.0, 0.0, 0.0], [4.0, 2.0, 0.0], [0.0, 3.0, 0.0], [3.0, 0.0, 0.0],
             [1.0, 1.0, 2.0], [3.0, 3.0, 1.0], [-1.0, 2.0, 1.0], [2.0, -1.0, 2.0]]


class TestInvariants(unittest.TestCase):
    def test_example_base(self):
        r1, r2, d1, d2, gap = base_invariants(*EXAMPLE_P[:4])
        self.assertAlmostEqual(r1, 0.5)
        self.assertAlmostEqual(r2, 2.0 / 3.0)
        self.assertAlmostEqual(d1, math.sqrt(20.0))
        self.assertAlmostEqual(d2, math.sqrt(18.0))
        self.assertAlmostEqual(gap, 0.0)

    def test_ratios_are_affine_invariant(self):
        rng = random.Random(1)
        for _ in range(50):
            a, b = [rng.uniform(-1, 1) for _ in range(3)], [rng.uniform(-1, 1) for _ in range(3)]
            c = [rng.uniform(-1, 1) for _ in range(3)]
            s, u = rng.uniform(0.1, 0.9), rng.uniform(0.1, 0.9)
            e = [a[i] + s * (b[i] - a[i]) for i in range(3)]
            d = [c[i] + (e[i] - c[i]) / u for i in range(3)]  # so that e = c + u (d - c)
            M = [[rng.uniform(-2, 2) for _ in range(3)] for _ in range(3)]
            if abs(det(M)) < 0.1:
                continue
            tt = [rng.uniform(-1, 1) for _ in range(3)]
            img = [apply(M, tt, p) for p in (a, b, c, d)]
            for pts in ((a, b, c, d), img):
                inv = base_invariants(*pts)
                self.assertIsNotNone(inv)
                self.assertAlmostEqual(inv[0], s, places=8)
                self.assertAlmostEqual(inv[1], u, places=8)
                self.assertLess(inv[4], 1e-8)

    def test_segments_that_miss(self):
        self.assertIsNone(base_invariants([0, 0, 0], [1, 0, 0], [2, 1, 0], [2, -1, 0]))
        self.assertIsNone(base_invariants([0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]))


class TestSearch(unittest.TestCase):
    def test_pairs_at_distance(self):
        rng = random.Random(2)
        Q = [[rng.uniform(0, 1) for _ in range(3)] for _ in range(30)]
        got = set(pairs_at_distance(Q, 0.5, 0.05))
        want = {(i, j) for i, j in itertools.permutations(range(30), 2)
                if abs(math.dist(Q[i], Q[j]) - 0.5) <= 0.05}
        self.assertEqual(got, want)

    def test_example_congruent_sets(self):
        R = [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
        Q = [apply(R, [5.0, 0.0, 1.0], p) for p in EXAMPLE_P] + [[0.0, 0.0, 0.0], [6.0, 4.0, 1.0]]
        cands = congruent_sets(Q, 0.5, 2.0 / 3.0, math.sqrt(20.0), math.sqrt(18.0), 0.01)
        self.assertEqual(sorted(cands), [(0, 1, 2, 3), (1, 0, 2, 3)])
        Rk, tk = kabsch(EXAMPLE_P[:4], [Q[i] for i in (0, 1, 2, 3)])
        self.assertLess(rot_angle(R, Rk), 1e-9)
        self.assertEqual(lcp_score(EXAMPLE_P, Grid(Q, 0.01), Rk, tk, 0.01), 8)
        Rk, tk = kabsch(EXAMPLE_P[:4], [Q[i] for i in (1, 0, 2, 3)])
        self.assertEqual(lcp_score(EXAMPLE_P, Grid(Q, 0.01), Rk, tk, 0.01), 0)

    def test_true_image_of_base_is_found(self):
        rng = random.Random(3)
        P = surface(rng, 80)
        R, t = random_rotation(rng), [rng.uniform(-1, 1) for _ in range(3)]
        Q = [apply(R, t, p) for p in P]
        found = select_base(P, rng, 0.02)
        self.assertIsNotNone(found)
        base, (r1, r2, d1, d2) = found
        self.assertIn(base, congruent_sets(Q, r1, r2, d1, d2, 0.02))

    def test_grid_matches_brute_force(self):
        rng = random.Random(4)
        pts = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(200)]
        g = Grid(pts, 0.2)
        for _ in range(30):
            x = [rng.uniform(-1, 1) for _ in range(3)]
            want = sorted(i for i, p in enumerate(pts) if math.dist(p, x) <= 0.15)
            self.assertEqual(sorted(g.near(x, 0.15)), want)


class TestKabsch(unittest.TestCase):
    def test_exact_and_proper(self):
        rng = random.Random(5)
        R, t = random_rotation(rng), [1.0, -2.0, 0.5]
        A = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(4)]
        Rk, tk = kabsch(A, [apply(R, t, a) for a in A])
        self.assertLess(rot_angle(R, Rk), 1e-9)
        self.assertAlmostEqual(det(Rk), 1.0, places=12)
        for x, y in zip(tk, t):
            self.assertAlmostEqual(x, y, places=9)


class TestFourPCS(unittest.TestCase):
    def test_full_overlap_with_noise_and_outliers(self):
        rng = random.Random(6)
        P = surface(rng, 80)
        R, t = random_rotation(rng), [rng.uniform(-1, 1) for _ in range(3)]
        Q = [[v + rng.gauss(0.0, 0.003) for v in apply(R, t, p)] for p in P]
        Q += [[rng.uniform(-2, 2) for _ in range(3)] for _ in range(20)]
        rng.shuffle(Q)
        out = four_pcs(P, Q, 0.03, n_trials=3, rng=random.Random(7))
        self.assertLess(rot_angle(R, out["R"]), math.radians(2.0))
        self.assertGreaterEqual(out["score"], 76)

    def test_partial_overlap(self):
        rng = random.Random(8)
        S = surface(rng, 90)
        P = [p for p in S if p[0] < 0.4]
        R, t = random_rotation(rng), [rng.uniform(-1, 1) for _ in range(3)]
        Q = [[v + rng.gauss(0.0, 0.003) for v in apply(R, t, p)] for p in S if p[0] > -0.4]
        out = four_pcs(P, Q, 0.03, n_trials=40, rng=random.Random(9), tries=5, max_width=0.8)
        self.assertLess(rot_angle(R, out["R"]), math.radians(3.0))


if __name__ == "__main__":
    unittest.main()
