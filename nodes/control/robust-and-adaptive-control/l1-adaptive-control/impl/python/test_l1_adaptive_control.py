# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/l1-adaptive-control/. The authors are listed in prov/S1SMGT.jsonl.

"""Tests for the L1 adaptive controller. RK4 with a fixed step; tolerances are stated."""

import math
import unittest

from l1_adaptive_control import l1_norm_g, l1_simulate, prediction_bound, proj

THETA, THETA_B, EPS, OMEGA_C = 1.5, 2.0, 0.1, 10.0


def step(t):
    return 1.0


def run(gamma, thetah0=0.0):
    # 10 s with dt = 0.002: 5000 steps
    return l1_simulate(THETA, THETA_B, EPS, gamma, OMEGA_C, step, 10.0, 0.002, thetah0=thetah0)


class TestL1Norm(unittest.TestCase):
    def test_formula_against_quadrature(self):
        # reference: trapezoid rule for the integral of |g| on [0, 40]
        for w in (2.0, 5.0, 10.0, 20.0):
            n, T = 20000, 40.0
            h = T / n
            g = [abs((w * math.exp(-w * k * h) - math.exp(-k * h)) / (w - 1.0)) for k in range(n + 1)]
            quad = h * (sum(g) - (g[0] + g[-1]) / 2)
            self.assertLess(abs(quad - l1_norm_g(w)), 1e-4)

    def test_small_gain_condition(self):
        # L = theta_b = 2; the condition ||G||_L1 L < 1 holds for omega_c = 5, 10, 20
        self.assertAlmostEqual(l1_norm_g(2.0), 0.5, places=12)
        self.assertFalse(l1_norm_g(2.0) * THETA_B < 1.0)
        for w in (5.0, 10.0, 20.0):
            self.assertLess(l1_norm_g(w) * THETA_B, 1.0)


class TestProjection(unittest.TestCase):
    def test_operator(self):
        self.assertEqual(proj(1.0, 3.0, 2.0, 0.1), 3.0)    # inside the ball
        self.assertEqual(proj(2.09, -1.0, 2.0, 0.1), -1.0)  # pointing inward
        f = (2.09 ** 2 - 4.0) / 0.4
        self.assertAlmostEqual(proj(2.09, 1.0, 2.0, 0.1), 1.0 - f, places=12)
        # on the outer boundary f = 1 and the outward part is removed
        self.assertAlmostEqual(proj(2.0 * math.sqrt(1.1), 1.0, 2.0, 0.1), 0.0, places=12)


class TestClosedLoop(unittest.TestCase):
    def test_prediction_error_bound_low_gains(self):
        for gamma in (10.0, 100.0):
            _, xs, xhs, ths, _ = run(gamma)
            err = max(abs(a - b) for a, b in zip(xs, xhs))
            self.assertLess(err, prediction_bound(0.0, THETA, gamma))
            self.assertLessEqual(max(abs(v) for v in ths), THETA_B * math.sqrt(1 + EPS) + 1e-9)
            self.assertLess(abs(xs[-1] - 1.0), 0.01)

    def test_high_gain_approaches_reference_system(self):
        # reference: the same loop with the true theta and no adaptation
        _, x_ref, _, _, _ = run(0.0, thetah0=THETA)
        self.assertLess(abs(x_ref[-1] - 1.0), 1e-4)
        _, xs, xhs, _, _ = run(1000.0)
        self.assertLess(max(abs(a - b) for a, b in zip(xs, xhs)), prediction_bound(0.0, THETA, 1000.0))
        self.assertLess(max(abs(a - b) for a, b in zip(xs, x_ref)), 0.07)

    def test_dt_must_divide_t1(self):
        with self.assertRaises(AssertionError):
            l1_simulate(THETA, THETA_B, EPS, 10.0, OMEGA_C, step, 1.0, 0.3)


if __name__ == "__main__":
    unittest.main()
