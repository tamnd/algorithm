# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convex-time-optimal-path-parameterization/. The authors are listed in prov/KKZDAS.jsonl.
import math
import random
import unittest

from convex_time_optimal_path_parameterization import (
    INF,
    arm2r_rows,
    convex_topp,
    max_violation,
    single_axis_rows,
    thomas,
    traversal_time,
    uniform_grid,
)


def admissible(grid, rows, b, tol=1e-12):
    n = len(grid) - 1
    a = [(b[k + 1] - b[k]) / (2.0 * (grid[k + 1] - grid[k])) for k in range(n)]
    return min(b) >= 0.0 and max_violation(rows, a, b) <= tol


def brute_force_3(grid, rows, top, steps):
    """Best time over a square lattice of (b_1, b_2) for a grid with N = 3."""
    best = INF
    for i in range(1, steps + 1):
        for j in range(1, steps + 1):
            b = [0.0, top * i / steps, top * j / steps, 0.0]
            if admissible(grid, rows, b):
                best = min(best, traversal_time(grid, b))
    return best


class TestWorkedExample(unittest.TestCase):
    def test_single_axis_trapezoid(self):
        g = uniform_grid(4)
        b, a, info = convex_topp(g, single_axis_rows(g, 1.0, 1.0, 2.0))
        for got, want in zip(b, [0.0, 1.0, 1.0, 1.0, 0.0]):
            self.assertAlmostEqual(got, want, delta=1e-6)
        self.assertAlmostEqual(traversal_time(g, b), 1.5, delta=1e-8)
        self.assertLess(info["gap"], 1e-9)

    def test_single_axis_triangle(self):
        g = uniform_grid(8)
        b, a, _ = convex_topp(g, single_axis_rows(g, 1.0, INF, 2.0))
        self.assertAlmostEqual(traversal_time(g, b), math.sqrt(2.0), delta=1e-8)

    def test_arm_example(self):
        g = uniform_grid(50)
        rows = arm2r_rows(g, [0.0, 0.0], [2.0, -3.0], [10.0, 4.0])
        b, a, _ = convex_topp(g, rows)
        self.assertLessEqual(max_violation(rows, a, b), 0.0)
        self.assertAlmostEqual(traversal_time(g, b), 1.50555, delta=1e-5)
        # The optimum is on the boundary: a profile 1% faster breaks a limit.
        self.assertGreater(max_violation(rows, [1.01 * v for v in a], [1.01 * v for v in b]), 1e-3)


class TestEdgeCases(unittest.TestCase):
    def test_no_strictly_feasible_start(self):
        # u >= 0 everywhere: the robot can never brake to rest.
        g = uniform_grid(4)
        rows = [[(1.0, 0.0, 0.0, 0.0, 2.0)] for _ in g]
        self.assertIsNone(convex_topp(g, rows))

    def test_thomas_against_dense(self):
        rng = random.Random(11)
        n = 6
        diag = [rng.uniform(3.0, 5.0) for _ in range(n)]
        off = [rng.uniform(-1.0, 1.0) for _ in range(n - 1)]
        rhs = [rng.uniform(-1.0, 1.0) for _ in range(n)]
        x = thomas(diag, off, rhs)
        for i in range(n):
            v = diag[i] * x[i]
            if i > 0:
                v += off[i - 1] * x[i - 1]
            if i < n - 1:
                v += off[i] * x[i + 1]
            self.assertAlmostEqual(v, rhs[i], places=12)

    def test_two_grid_intervals(self):
        # N = 2: one free variable; the optimum is b_1 = min(vmax^2, 2 a Delta * 2 / 2).
        g = uniform_grid(2)
        b, _, _ = convex_topp(g, single_axis_rows(g, 1.0, INF, 2.0))
        self.assertAlmostEqual(b[1], 2.0, delta=1e-6)


class TestRandomized(unittest.TestCase):
    def test_against_brute_force(self):
        rng = random.Random(2009)
        g = uniform_grid(3)
        for _ in range(3):
            q1 = [rng.uniform(-3.0, 3.0), rng.uniform(-3.0, 3.0)]
            tau = [rng.uniform(4.0, 12.0), rng.uniform(2.0, 6.0)]
            rows = arm2r_rows(g, [0.0, 0.0], q1, tau)
            b, a, _ = convex_topp(g, rows)
            self.assertLessEqual(max_violation(rows, a, b), 0.0)
            t = traversal_time(g, b)
            top = 1.2 * max(b)
            t_bf = brute_force_3(g, rows, top, 150)
            self.assertLessEqual(t, t_bf + 1e-9)
            self.assertLessEqual(t_bf, t * 1.02)

    def test_random_admissible_profiles_are_slower(self):
        # Random lattice profiles on a coarse grid: none beats the optimum.
        rng = random.Random(5)
        g = uniform_grid(4)
        rows = arm2r_rows(g, [0.0, 0.0], [1.5, 2.5], [10.0, 4.0])
        b, _, _ = convex_topp(g, rows)
        t = traversal_time(g, b)
        tried = 0
        for _ in range(3000):
            c = [0.0] + [rng.uniform(0.0, 1.2 * max(b)) for _ in range(3)] + [0.0]
            if admissible(g, rows, c):
                tried += 1
                self.assertGreaterEqual(traversal_time(g, c), t - 1e-9)
        self.assertGreater(tried, 10)


if __name__ == "__main__":
    unittest.main()
