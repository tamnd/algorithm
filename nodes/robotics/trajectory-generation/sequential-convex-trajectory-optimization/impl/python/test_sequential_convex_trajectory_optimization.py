# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-convex-trajectory-optimization/. The authors are listed in prov/7KE72T.jsonl.
import random
import unittest

from sequential_convex_trajectory_optimization import (
    add,
    block_tridiag_solve,
    disc_sd,
    inside_circle_sd,
    max_violation,
    merit,
    model_value,
    path_length,
    scp,
    smoothness,
    solve_subproblem,
    straight_line,
)

Q0, Q1 = [-1.0, 0.0], [1.0, 0.0]


def linearize(x, sds):
    return [(t, *sd(x[t])) for t in range(len(x)) for sd in sds]


class TestWorkedExample(unittest.TestCase):
    def test_disc_below_the_line(self):
        sds = [disc_sd(0.0, -0.15, 0.5)]
        log = []
        x, info = scp(Q0, Q1, 9, sds, log=log)
        self.assertAlmostEqual(merit(straight_line(Q0, Q1, 9), Q0, Q1, sds, 0.1, 10.0), 15.356, places=3)
        self.assertEqual((info["mu"], info["accepted"], info["rejected"]), (10.0, 5, 0))
        self.assertAlmostEqual(smoothness(x, Q0, Q1), 0.48781, places=4)
        self.assertAlmostEqual(path_length(x, Q0, Q1), 2.2086, places=3)
        self.assertLessEqual(max_violation(x, sds, 0.1), 1e-4)
        self.assertAlmostEqual(x[4][1], 0.45, places=3)
        values = [m for _, m in info["merits"]]
        self.assertTrue(all(b < a for a, b in zip(values, values[1:])))
        # Convex obstacles: the model is an upper bound, so every ratio is at least 1.
        self.assertTrue(all(r >= 1.0 - 1e-6 for _, _, _, r in log))


class TestEdgeCases(unittest.TestCase):
    def test_no_active_obstacle_keeps_the_line(self):
        sds = [disc_sd(0.0, 3.0, 0.5)]
        x, info = scp(Q0, Q1, 5, sds)
        self.assertEqual(info["accepted"], 0)
        self.assertEqual(x, straight_line(Q0, Q1, 5))

    def test_subproblem_against_grid_search(self):
        # One free waypoint, inside a disc; brute force over the trust region box.
        sds = [disc_sd(0.1, -0.2, 0.4)]
        x = [[0.0, 0.0]]
        lin = linearize(x, sds)
        delta, mu = 0.3, 5.0
        d = solve_subproblem(x, Q0, Q1, lin, 0.1, mu, delta)
        self.assertLessEqual(max(abs(v) for v in d), delta)
        got = model_value(x, Q0, Q1, lin, 0.1, mu, d)
        def m(p):
            return model_value(x, Q0, Q1, lin, 0.1, mu, p)
        h = delta / 30.0
        coarse = min(([delta * (i / 30.0 - 1.0), delta * (j / 30.0 - 1.0)] for i in range(61) for j in range(61)), key=m)
        fine = [[min(delta, max(-delta, coarse[0] + h * (i / 30.0 - 1.0))), min(delta, max(-delta, coarse[1] + h * (j / 30.0 - 1.0)))]
                for i in range(61) for j in range(61)]
        best = min(m(p) for p in fine)
        self.assertLessEqual(got, best + 1e-6)
        self.assertGreater(got, best - 1e-3)

    def test_ratio_test_rejects_and_shrinks(self):
        # A concave constraint (stay inside a circle) makes the model optimistic.
        sds = [inside_circle_sd(0.0, 0.9, 1.0)]
        a, b = [-0.9, 0.0], [0.9, 0.0]
        log = []
        x, info = scp(a, b, 5, sds, delta0=1.0, c=0.98, log=log)
        self.assertGreater(info["rejected"], 0)
        self.assertTrue(any(r < 0.98 for _, _, _, r in log))
        self.assertLessEqual(max_violation(x, sds, 0.1), 1e-4)
        rejected_deltas = [(d0, d1) for (_, d0, _, r), (_, d1, _, _) in zip(log, log[1:]) if r < 0.98]
        self.assertTrue(all(abs(d1 - 0.5 * d0) < 1e-12 for d0, d1 in rejected_deltas))
        values = [m for _, m in info["merits"]]
        self.assertTrue(all(b < a for a, b in zip(values, values[1:])))

    def test_block_tridiagonal_solve(self):
        rng = random.Random(5)
        n, off = 6, -0.7
        diag = []
        for _ in range(n):
            a, b, c = rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3)
            diag.append([[3.0 + a, b], [b, 3.0 + c]])
        rhs = [[rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)] for _ in range(n)]
        x = block_tridiag_solve(diag, off, rhs)
        for t in range(n):
            for i in range(2):
                v = diag[t][i][0] * x[t][0] + diag[t][i][1] * x[t][1]
                if t > 0:
                    v += off * x[t - 1][i]
                if t < n - 1:
                    v += off * x[t + 1][i]
                self.assertAlmostEqual(v, rhs[t][i], places=10)


class TestRandomized(unittest.TestCase):
    def test_random_subproblems_respect_the_box_and_improve_the_model(self):
        rng = random.Random(2013)
        for _ in range(5):
            x = [[rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)] for _ in range(3)]
            sds = [disc_sd(rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5), rng.uniform(0.1, 0.4))]
            lin = linearize(x, sds)
            delta = rng.uniform(0.05, 0.5)
            d = solve_subproblem(x, Q0, Q1, lin, 0.1, 10.0, delta)
            self.assertLessEqual(max(abs(v) for v in d), delta)
            m0 = model_value(x, Q0, Q1, lin, 0.1, 10.0, [0.0] * 6)
            m1 = model_value(x, Q0, Q1, lin, 0.1, 10.0, d)
            self.assertLessEqual(m1, m0 + 1e-7)
            # The true merit is at most the model for convex obstacles.
            self.assertLessEqual(merit(add(x, d), Q0, Q1, sds, 0.1, 10.0), m1 + 1e-9)


if __name__ == "__main__":
    unittest.main()
