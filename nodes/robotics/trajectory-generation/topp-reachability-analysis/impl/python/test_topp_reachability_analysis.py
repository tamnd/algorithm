# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/topp-reachability-analysis/. The authors are listed in prov/HBHW2D.jsonl.
import math
import random
import unittest

from topp_reachability_analysis import (
    INF,
    arm2r_rows,
    max_violation,
    one_step_set,
    single_axis_rows,
    toppra,
    traversal_time,
    uniform_grid,
)


def dp_oracle(grid, rows, levels, x_top):
    """Shortest traversal time over profiles with x_i on the lattice j * x_top / levels.

    A transition x_i -> x_(i+1) is allowed when u = (x_(i+1) - x_i) / (2 delta)
    meets every row at (u, x_i). This does not use the controllable sets.
    """
    n = len(grid) - 1
    xs = [j * x_top / levels for j in range(levels + 1)]
    best = [INF] * (levels + 1)
    best[0] = 0.0
    for i in range(n):
        delta = grid[i + 1] - grid[i]
        new = [INF] * (levels + 1)
        for j, xi in enumerate(xs):
            if best[j] == INF:
                continue
            ok_x = all(
                not (a == 0.0 and not (lo - 1e-12 <= b * xi + c <= hi + 1e-12))
                for a, b, c, lo, hi in rows[i]
            )
            if not ok_x:
                continue
            for k, xk in enumerate(xs):
                u = (xk - xi) / (2.0 * delta)
                if all(lo - 1e-12 <= a * u + b * xi + c <= hi + 1e-12 for a, b, c, lo, hi in rows[i]):
                    den = math.sqrt(xi) + math.sqrt(xk)
                    if den > 0.0:
                        t = best[j] + 2.0 * delta / den
                        if t < new[k]:
                            new[k] = t
        best = new
    return best[0]


class TestWorkedExample(unittest.TestCase):
    def test_single_axis_trapezoid(self):
        # D = 1, V = 1, A = 2: the trapezoid with Ta = 0.5 and T = 1.5.
        g = uniform_grid(4)
        u, x, k = toppra(g, single_axis_rows(g, 1.0, 1.0, 2.0))
        self.assertEqual(x, [0.0, 1.0, 1.0, 1.0, 0.0])
        self.assertEqual(u, [2.0, 0.0, 0.0, -2.0])
        self.assertEqual(k[:4], [(0.0, 1.0)] * 4)
        self.assertEqual(k[4], (0.0, 0.0))
        self.assertAlmostEqual(traversal_time(g, x), 1.5, places=12)

    def test_single_axis_triangle(self):
        # No velocity limit: bang-bang with the switch at s = 1/2, T = sqrt(2).
        for n in (2, 8, 16):
            g = uniform_grid(n)
            u, x, _ = toppra(g, single_axis_rows(g, 1.0, INF, 2.0))
            self.assertAlmostEqual(traversal_time(g, x), math.sqrt(2.0), places=12)
            self.assertAlmostEqual(max(x), 2.0, places=12)

    def test_arm_example(self):
        g = uniform_grid(200)
        rows = arm2r_rows(g, [0.0, 0.0], [2.0, -3.0], [10.0, 4.0])
        u, x, _ = toppra(g, rows)
        self.assertLess(max_violation(rows, u, x), 1e-9)
        self.assertAlmostEqual(traversal_time(g, x), 1.5096, places=3)
        # The profile touches the maximum velocity curve near s = 0.35.
        self.assertAlmostEqual(x[70], 1.1556, places=3)


class TestEdgeCases(unittest.TestCase):
    def test_infeasible_start(self):
        g = uniform_grid(4)
        # Braking from x = 10 at A = 2 needs a distance of 2.5 > 1.
        self.assertIsNone(toppra(g, single_axis_rows(g, 1.0, INF, 2.0), x_start=10.0))
        # Start above the velocity limit.
        self.assertIsNone(toppra(g, single_axis_rows(g, 1.0, 1.0, 2.0), x_start=4.0))

    def test_infeasible_path(self):
        # A row that needs a positive x at s_2 cannot be met.
        g = uniform_grid(4)
        rows = single_axis_rows(g, 1.0, 1.0, 2.0)
        rows[2] = rows[2] + [(0.0, 1.0, 0.0, 5.0, INF)]
        self.assertIsNone(toppra(g, rows))

    def test_nonzero_end_speed(self):
        g = uniform_grid(4)
        u, x, _ = toppra(g, single_axis_rows(g, 1.0, 1.0, 2.0), x_end=1.0)
        self.assertEqual(x, [0.0, 1.0, 1.0, 1.0, 1.0])

    def test_one_step_set_empty(self):
        # x + 2 delta u must reach [10, 10] but u <= 1 and x <= 1.
        rows = [(1.0, 0.0, 0.0, -1.0, 1.0), (0.0, 1.0, 0.0, -INF, 1.0)]
        self.assertIsNone(one_step_set(rows, 0.25, (10.0, 10.0)))
        self.assertEqual(one_step_set(rows, 0.25, (0.0, 1.0)), (0.0, 1.0))

    def test_scaled_profile_breaks_a_limit(self):
        g = uniform_grid(50)
        rows = arm2r_rows(g, [0.0, 0.0], [2.0, -3.0], [10.0, 4.0])
        u, x, _ = toppra(g, rows)
        self.assertGreater(max_violation(rows, [1.01 * v for v in u], [1.01 * v for v in x]), 1e-3)


class TestRandomized(unittest.TestCase):
    def test_against_lattice_dp(self):
        rng = random.Random(20260517)
        for _ in range(3):
            q1 = [rng.uniform(-3.0, 3.0), rng.uniform(-3.0, 3.0)]
            tau = [rng.uniform(4.0, 12.0), rng.uniform(2.0, 6.0)]
            g = uniform_grid(6)
            rows = arm2r_rows(g, [0.0, 0.0], q1, tau)
            res = toppra(g, rows)
            self.assertIsNotNone(res)
            u, x, k = res
            self.assertLess(max_violation(rows, u, x), 1e-9)
            t_ra = traversal_time(g, x)
            x_top = max(hi for _, hi in k) * 1.0001
            t_dp = dp_oracle(g, rows, 120, x_top)
            # The lattice only holds some profiles, so the DP time is an upper
            # bound on the best discrete time; TOPP-RA must not be worse by more
            # than a small margin and the lattice must not beat it.
            self.assertLessEqual(t_ra, t_dp * 1.02)
            self.assertLessEqual(t_dp, t_ra * 1.05)

    def test_dominates_random_admissible_profiles(self):
        # Any admissible profile with the same end points is no faster.
        rng = random.Random(7)
        g = uniform_grid(4)
        rows = single_axis_rows(g, 1.0, 1.0, 2.0)
        t_ra = traversal_time(g, toppra(g, rows)[1])
        for _ in range(300):
            x = [0.0] + [rng.uniform(0.0, 1.0) for _ in range(3)] + [0.0]
            u = [(x[i + 1] - x[i]) * 2.0 for i in range(4)]
            if max_violation(rows, u, x) <= 1e-12:
                self.assertGreaterEqual(traversal_time(g, x), t_ra - 1e-12)


if __name__ == "__main__":
    unittest.main()
