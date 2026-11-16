# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chomp/. The authors are listed in prov/ZMPYZV.jsonl.
import random
import unittest

from chomp import (
    chomp,
    cost_c,
    cost_dc,
    min_clearance,
    obstacle_grad,
    objective,
    path_length,
    smoothness_grad,
    solve_a,
    straight_line,
)

Q0, Q1 = [-1.0, 0.0], [1.0, 0.0]


def nonincreasing(h, tol=1e-12):
    return all(h[i + 1] <= h[i] + tol for i in range(len(h) - 1))


class TestWorkedExample(unittest.TestCase):
    def test_disc_below_the_line(self):
        disc = (0.0, -0.15, 0.5)
        xi, hist, iters = chomp(Q0, Q1, 19, [disc], lam=0.02, eps=0.2)
        self.assertLess(iters, 3000)
        self.assertTrue(nonincreasing(hist))
        self.assertAlmostEqual(hist[0], 3.85586, delta=1e-5)
        self.assertAlmostEqual(hist[-1], 1.06162, delta=1e-5)
        self.assertAlmostEqual(xi[9][1], 0.5195, delta=1e-3)
        self.assertAlmostEqual(min_clearance(xi, [disc]), 0.1695, delta=1e-3)
        self.assertAlmostEqual(path_length(xi, Q0, Q1), 2.2883, delta=1e-3)

    def test_first_steps(self):
        disc = (0.0, -0.15, 0.5)
        xi, hist, _ = chomp(Q0, Q1, 19, [disc], iters=5)
        self.assertGreater(min_clearance(xi, [disc]), 0.13)
        self.assertAlmostEqual(hist[1], 2.96117, delta=1e-5)


class TestEdgeCases(unittest.TestCase):
    def test_one_covariant_step_reaches_the_line(self):
        # Without obstacles and with eta = lam, one step solves the quadratic exactly.
        rng = random.Random(7)
        xi0 = [[p[0] + rng.uniform(-0.3, 0.3), p[1] + rng.uniform(-0.3, 0.3)]
               for p in straight_line(Q0, Q1, 9)]
        xi, _, _ = chomp(Q0, Q1, 9, [], lam=0.5, eta=0.5, iters=1, xi0=xi0)
        for got, want in zip(xi, straight_line(Q0, Q1, 9)):
            self.assertAlmostEqual(got[0], want[0], places=12)
            self.assertAlmostEqual(got[1], want[1], places=12)

    def test_symmetric_start_is_a_stationary_trap(self):
        # The straight line through the center of the disc never leaves the axis.
        disc = (0.0, 0.0, 0.5)
        xi, hist, _ = chomp(Q0, Q1, 19, [disc], iters=2000)
        self.assertTrue(all(p[1] == 0.0 for p in xi))
        self.assertLess(min_clearance(xi, [disc]), -0.3)
        # A push of 0.001 to one side is enough to escape.
        xi0 = [[p[0], p[1] + 1e-3] for p in straight_line(Q0, Q1, 19)]
        xi, _, _ = chomp(Q0, Q1, 19, [disc], iters=2000, xi0=xi0)
        self.assertGreater(min_clearance(xi, [disc]), 0.15)

    def test_cost_is_continuously_differentiable(self):
        eps = 0.2
        for d in (0.0, eps):
            self.assertAlmostEqual(cost_c(d - 1e-9, eps), cost_c(d + 1e-9, eps), places=7)
            self.assertAlmostEqual(cost_dc(d - 1e-9, eps), cost_dc(d + 1e-9, eps), places=7)

    def test_gradient_against_finite_differences(self):
        rng = random.Random(3)
        discs = [(0.1, 0.05, 0.4), (-0.4, -0.2, 0.3)]
        lam, eps, n = 0.05, 0.2, 7
        dt = 1.0 / (n + 1)
        xi = [[p[0] + rng.uniform(-0.2, 0.2), p[1] + rng.uniform(-0.2, 0.2)]
              for p in straight_line(Q0, Q1, n)]
        go = obstacle_grad(xi, discs, eps)
        gs = smoothness_grad(xi, Q0, Q1, dt)
        h = 1e-6
        for t in range(n):
            for d in range(2):
                xp = [list(p) for p in xi]
                xm = [list(p) for p in xi]
                xp[t][d] += h
                xm[t][d] -= h
                num = (objective(xp, Q0, Q1, dt, discs, lam, eps)
                       - objective(xm, Q0, Q1, dt, discs, lam, eps)) / (2 * h)
                self.assertAlmostEqual(num, go[t][d] + lam * gs[t][d], delta=1e-5)

    def test_tridiagonal_solve(self):
        rng = random.Random(11)
        n, dt = 8, 0.1
        rhs = [rng.uniform(-1.0, 1.0) for _ in range(n)]
        x = solve_a(rhs, dt)
        for i in range(n):
            v = 2.0 * x[i] - (x[i - 1] if i > 0 else 0.0) - (x[i + 1] if i < n - 1 else 0.0)
            self.assertAlmostEqual(v / (dt * dt), rhs[i], places=9)


class TestRandomized(unittest.TestCase):
    def test_cost_never_increases(self):
        rng = random.Random(2013)
        for _ in range(3):
            discs = [(rng.uniform(-0.6, 0.6), rng.uniform(-0.4, 0.4), rng.uniform(0.1, 0.35))
                     for _ in range(3)]
            lam = rng.uniform(0.01, 0.1)
            xi, hist, _ = chomp(Q0, Q1, 15, discs, lam=lam, iters=400)
            self.assertTrue(nonincreasing(hist))
            self.assertLessEqual(hist[-1], hist[0])


if __name__ == "__main__":
    unittest.main()
