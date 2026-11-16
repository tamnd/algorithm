# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stomp/. The authors are listed in prov/2F4S7V.jsonl.
import math
import random
import unittest

from stomp import (
    disc_hinge,
    min_clearance,
    r_inverse,
    sample_noise,
    smoothing_matrix,
    solve_second_difference,
    stomp,
    total_cost,
    weights,
)

Q0, Q1 = [-1.0, 0.0], [1.0, 0.0]
DISC = (0.0, -0.15, 0.5)


class TestWorkedExample(unittest.TestCase):
    def test_disc_below_the_line(self):
        cost = disc_hinge([DISC], 0.1)
        theta, best_q, hist = stomp(Q0, Q1, 19, cost, lam=0.05, sigma=0.02, w=10.0, iters=12, seed=2011)
        self.assertAlmostEqual(hist[0], 3.0202, delta=1e-4)
        self.assertAlmostEqual(best_q, 0.0075, delta=1e-4)
        self.assertEqual(hist.index(min(hist)), 7)
        self.assertGreater(min_clearance(theta, [DISC]), 0.1)
        # The iterates do not decrease monotonically.
        self.assertTrue(any(hist[i + 1] > hist[i] for i in range(len(hist) - 1)))

    def test_cost_without_gradient(self):
        # A step cost: 1 for each waypoint closer than 0.1 to the disc, else 0.
        def step(p):
            return 1.0 if math.hypot(p[0] - DISC[0], p[1] - DISC[1]) < DISC[2] + 0.1 else 0.0
        theta, best_q, hist = stomp(Q0, Q1, 19, step, lam=0.05, sigma=0.02, w=10.0, iters=60, seed=7)
        self.assertEqual(hist[0], 11.0)
        self.assertLess(best_q, 0.01)
        self.assertGreater(min_clearance(theta, [DISC]), 0.1)


class TestEdgeCases(unittest.TestCase):
    def test_noise_covariance_is_r_inverse(self):
        rng = random.Random(1)
        n, sigma, count = 6, 1.0, 6000
        rinv = r_inverse(n)
        acc = [[0.0] * n for _ in range(n)]
        for _ in range(count):
            e = sample_noise(rng, n, sigma)
            for i in range(n):
                for j in range(n):
                    acc[i][j] += e[i][0] * e[j][0]
        for i in range(n):
            for j in range(n):
                self.assertAlmostEqual(acc[i][j] / count, rinv[i][j], delta=0.08 * rinv[2][2])

    def test_second_difference_solve(self):
        rng = random.Random(4)
        rhs = [rng.uniform(-1.0, 1.0) for _ in range(7)]
        x = solve_second_difference(rhs)
        for i in range(7):
            v = -2.0 * x[i] + (x[i - 1] if i > 0 else 0.0) + (x[i + 1] if i < 6 else 0.0)
            self.assertAlmostEqual(v, rhs[i], places=12)

    def test_smoothing_matrix_columns(self):
        n = 9
        m = smoothing_matrix(n)
        for j in range(n):
            self.assertAlmostEqual(max(m[i][j] for i in range(n)), 1.0 / n, places=12)
            self.assertTrue(all(m[i][j] > 0.0 for i in range(n)))

    def test_weights(self):
        s = [3.0, 1.0, 2.0, 1.5]
        p = weights(s, 0.5)
        self.assertAlmostEqual(sum(p), 1.0, places=12)
        q = weights([v + 7.0 for v in s], 0.5)
        for a, b in zip(p, q):
            self.assertAlmostEqual(a, b, places=12)
        self.assertEqual(max(range(4), key=lambda i: p[i]), 1)
        sharp = weights(s, 1e-6)
        self.assertAlmostEqual(sharp[1], 1.0, places=9)
        flat = weights([2.0] * 4, 0.5)
        self.assertTrue(all(abs(v - 0.25) < 1e-12 for v in flat))

    def test_free_space_keeps_best(self):
        # No obstacles: the straight line has cost 0 and stays the best.
        theta, best_q, hist = stomp(Q0, Q1, 9, lambda p: 0.0, iters=5, seed=3)
        self.assertLess(best_q, 1e-20)
        self.assertEqual(best_q, hist[0])
        self.assertGreater(max(hist), 1e-6)  # the iterates themselves drift


class TestRandomized(unittest.TestCase):
    def test_best_is_never_worse_than_start(self):
        rng = random.Random(2011)
        for _ in range(3):
            discs = [(rng.uniform(-0.5, 0.5), rng.uniform(-0.3, 0.3), rng.uniform(0.1, 0.3)) for _ in range(2)]
            cost = disc_hinge(discs, 0.1)
            theta, best_q, hist = stomp(Q0, Q1, 11, cost, k=10, iters=15, seed=rng.randrange(1000))
            self.assertLessEqual(best_q, hist[0])
            self.assertAlmostEqual(best_q, total_cost(theta, Q0, Q1, cost, 100.0), places=12)
            self.assertEqual(best_q, min(hist))


if __name__ == "__main__":
    unittest.main()
