# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bobrow-time-optimal-algorithm/. The authors are listed in prov/BWJG6T.jsonl.
import math
import random
import unittest

from bobrow_time_optimal_algorithm import (
    accel_bounds,
    arm2r,
    bobrow,
    mvc,
    profile_value,
    single_axis,
    traversal_time,
)


def grid_oracle(rows_fn, n):
    """Independent check: backward braking limit and forward greedy pass on a grid.

    y_i is the largest x <= MVC with x + 2 h L(s_i, x) <= y_(i+1), found by
    bisection; then x_(i+1) = min(x_i + 2 h U(s_i, x_i), y_(i+1)). Explicit
    Euler on the phase plane, error O(1 / n).
    """
    h = 1.0 / n
    s = [i * h for i in range(n + 1)]
    y = [0.0] * (n + 1)
    for i in range(n - 1, -1, -1):
        rows = rows_fn(s[i])
        top = min(mvc(rows), 1e6)
        ok = lambda x: x + 2.0 * h * accel_bounds(rows, x)[0] <= y[i + 1]
        if ok(top):
            y[i] = top
            continue
        lo, hi = 0.0, top
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if ok(mid):
                lo = mid
            else:
                hi = mid
        y[i] = lo
    x = [0.0] * (n + 1)
    for i in range(n):
        x[i + 1] = min(x[i] + 2.0 * h * accel_bounds(rows_fn(s[i]), x[i])[1], y[i + 1])
    return sum(2.0 * h / (math.sqrt(x[i]) + math.sqrt(x[i + 1])) for i in range(n))


def below_mvc(rows_fn, profile, rel):
    return all(x <= mvc(rows_fn(s)) * (1.0 + rel) + 1e-9 for s, x in profile)


class TestWorkedExample(unittest.TestCase):
    def test_single_axis_triangle(self):
        # q = s, |q''| <= 2: accelerate to s = 1/2, brake to s = 1, T = sqrt(2).
        prof, switches = bobrow(single_axis(1.0, 2.0), h=0.01)
        self.assertAlmostEqual(traversal_time(prof), math.sqrt(2.0), places=9)
        self.assertEqual(len(switches), 1)
        self.assertAlmostEqual(switches[0][0], 0.5, places=9)
        self.assertAlmostEqual(profile_value(prof, 0.5), 2.0, places=9)

    def test_arm_example(self):
        rows_fn = arm2r([0.0, 0.0], [2.0, -3.0], [10.0, 4.0])
        prof, switches = bobrow(rows_fn, h=0.004)
        kinds = [k for _, k in switches]
        self.assertEqual(kinds, ["UL", "LU", "UL"])
        self.assertAlmostEqual(switches[0][0], 0.2385, delta=2e-3)
        # The tangent point is found on the integration grid: within one step h.
        self.assertAlmostEqual(switches[1][0], 0.35, delta=0.0041)
        self.assertAlmostEqual(switches[2][0], 0.731, delta=2e-3)
        self.assertEqual(prof[0], (0.0, 0.0))
        self.assertEqual(prof[-1][1], 0.0)
        self.assertAlmostEqual(prof[-1][0], 1.0, places=12)
        self.assertTrue(all(b[0] > a[0] for a, b in zip(prof, prof[1:])))
        self.assertTrue(below_mvc(rows_fn, prof, 1e-6))
        t = traversal_time(prof)
        self.assertAlmostEqual(t, grid_oracle(rows_fn, 2000), delta=3e-3 * t)
        # The profile touches the MVC, so a profile 1% faster is above it.
        self.assertFalse(below_mvc(rows_fn, [(s, 1.01 * x) for s, x in prof], 0.0))


class TestEdgeCases(unittest.TestCase):
    def test_cannot_start(self):
        # u + 5 <= 1 forces u <= -4 at rest: the robot cannot start.
        rows_fn = lambda s: [(1.0, 0.0, 5.0, -INF_LIMIT, 1.0)]
        self.assertIsNone(bobrow(rows_fn, h=0.05))

    def test_mvc_of_rows(self):
        # |u + x| <= 1 and |u - x| <= 1 meet only for x <= 1.
        rows = [(1.0, 1.0, 0.0, -1.0, 1.0), (1.0, -1.0, 0.0, -1.0, 1.0)]
        self.assertAlmostEqual(mvc(rows), 1.0, places=15)
        self.assertEqual(accel_bounds(rows, 0.5), (-0.5, 0.5))
        self.assertEqual(mvc([(1.0, 0.0, 0.0, -2.0, 2.0)]), math.inf)
        # A pure velocity row: 4 x <= 1.
        self.assertAlmostEqual(mvc([(1.0, 0.0, 0.0, -2.0, 2.0), (0.0, 4.0, 0.0, -math.inf, 1.0)]), 0.25)

    def test_asymmetric_limits(self):
        # Accelerate at 1, brake at 3: switch where s / 1 = (1 - s) / 3, s = 3/4.
        rows_fn = lambda s: [(1.0, 0.0, 0.0, -3.0, 1.0)]
        prof, switches = bobrow(rows_fn, h=0.01)
        self.assertAlmostEqual(switches[0][0], 0.75, places=9)
        t = math.sqrt(2.0 * 0.75 / 1.0) + math.sqrt(2.0 * 0.25 / 3.0)
        self.assertAlmostEqual(traversal_time(prof), t, places=9)


INF_LIMIT = math.inf


class TestRandomized(unittest.TestCase):
    def test_against_grid_oracle(self):
        rng = random.Random(1985)
        done = 0
        while done < 3:
            q1 = [rng.uniform(-3.0, 3.0), rng.uniform(-3.0, 3.0)]
            tau = [rng.uniform(4.0, 12.0), rng.uniform(2.0, 6.0)]
            rows_fn = arm2r([0.0, 0.0], q1, tau)
            res = bobrow(rows_fn, h=0.005)
            self.assertIsNotNone(res)
            prof, _ = res
            self.assertTrue(below_mvc(rows_fn, prof, 1e-6))
            t = traversal_time(prof)
            self.assertAlmostEqual(t, grid_oracle(rows_fn, 1000), delta=5e-3 * t)
            done += 1


if __name__ == "__main__":
    unittest.main()
