# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mit-rule/. The authors are listed in prov/B6VAKD.jsonl.

"""Tests for the MIT rule. RK4 with a fixed step; tolerances are stated."""

import random
import unittest

from ctlsim import rk4_step
from mit_rule import (
    cubic_is_hurwitz, feedforward_theta_poly, mit_feedforward_gain, mit_first_order,
)

# G(s) = 1 / (s^2 + s + 1), plant gain k = 1, model gain k0 = 2.
A = [[0.0, 1.0], [-1.0, -1.0]]
B = [0.0, 1.0]
C = [1.0, 0.0]


def run_ff(gamma, u0, t1, dt=0.02, theta0=1.0):
    # plant and model start at rest for their gains, so y_m is constant
    return mit_feedforward_gain(
        A, B, C, 1.0, 2.0, gamma, lambda t: u0, t1, dt, theta0=theta0,
        x0=[theta0 * u0, 0.0], xm0=[2.0 * u0, 0.0], every=50)


class TestFeedforward(unittest.TestCase):
    def test_converges_for_small_gain(self):
        # gamma u0^2 = 0.25 < 1/2: theta -> k0 / k = 2
        _, th, err = run_ff(0.25, 1.0, 60.0)
        self.assertLess(abs(th[-1] - 2.0), 1e-3)
        self.assertLess(abs(err[-1]), 1e-3)

    def test_diverges_for_large_gain_or_amplitude(self):
        # gamma u0^2 = 1 > 1/2 in both runs: the same gain with a larger
        # command amplitude is unstable too
        for gamma, u0 in ((1.0, 1.0), (0.25, 2.0)):
            _, th, _ = run_ff(gamma, u0, 40.0)
            self.assertGreater(max(abs(v - 2.0) for v in th), 50.0)

    def test_routh_verdict_matches_simulation(self):
        for gamma, stable in ((0.3, True), (0.8, False)):
            p = feedforward_theta_poly(1.0, 1.0, 1.0, 2.0, gamma, 1.0)
            self.assertEqual(cubic_is_hurwitz(p), stable)
            _, th, _ = run_ff(gamma, 1.0, 80.0)
            early = max(abs(v - 2.0) for v in th[:10])
            late = max(abs(v - 2.0) for v in th[-10:])
            self.assertEqual(late < early, stable)

    def test_against_linear_theta_equation(self):
        # reference method: integrate the third order equation of theta
        gamma, u0, theta0 = 0.2, 1.0, 1.0
        p = feedforward_theta_poly(1.0, 1.0, 1.0, 2.0, gamma, u0)
        ym0, e0 = 2.0 * u0, (theta0 - 2.0) * u0
        z = [theta0, -gamma * ym0 * e0, 0.0]

        def g(t, w, _u):
            return [w[1], w[2], -p[1] * w[2] - p[2] * w[1] - p[3] * (w[0] - 2.0)]

        dt = 0.02
        for i in range(1000):
            z = rk4_step(g, i * dt, z, None, dt)
        _, th, _ = run_ff(gamma, u0, 20.0, dt=dt, theta0=theta0)
        self.assertLess(abs(th[-1] - z[0]), 1e-6)

    def test_routh_threshold_formula(self):
        rng = random.Random(7)
        for _ in range(50):
            a1, a2 = rng.uniform(0.2, 3), rng.uniform(0.2, 3)
            k, k0, u0 = rng.uniform(0.2, 3), rng.uniform(0.2, 3), rng.uniform(0.2, 3)
            limit = a1 * a2 * a2 / (k * k0 * u0 * u0)
            for gamma in (0.9 * limit, 1.1 * limit):
                p = feedforward_theta_poly(a1, a2, k, k0, gamma, u0)
                self.assertEqual(cubic_is_hurwitz(p), gamma < limit)


class TestFirstOrder(unittest.TestCase):
    def test_two_parameters_converge(self):
        # y' = -y + 0.5 u, model 2 / (s + 2), square wave command of period 20 s
        def sq(t):
            return 1.0 if (t % 20.0) < 10.0 else -1.0
        # gamma = 5: the ideal values are theta_1 = 4 and theta_2 = 2
        _, th1, th2, err = mit_first_order(1.0, 0.5, 2.0, 2.0, 5.0, sq, 100.0, 0.01, every=100)
        self.assertLess(abs(th1[-1] - 4.0), 0.05)
        self.assertLess(abs(th2[-1] - 2.0), 0.05)
        self.assertLess(max(abs(v) for v in err[-10:]), 0.01)

    def test_dt_must_divide_t1(self):
        with self.assertRaises(AssertionError):
            mit_first_order(1.0, 0.5, 2.0, 2.0, 1.0, lambda t: 1.0, 1.0, 0.3)


if __name__ == "__main__":
    unittest.main()
