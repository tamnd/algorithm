# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extremum-seeking-control/. The authors are listed in prov/Y83ZRN.jsonl.

"""Tests for extremum seeking. RK4 with a fixed step; tolerances are stated."""

import math
import random
import unittest

from extremum_seeking_control import demodulated_average, esc_simulate

DT, T1 = 0.005, 30.0  # 6000 steps per run


def quad(th):
    return (th[0] - 2.0) ** 2 + 1.0


class TestDemodulation(unittest.TestCase):
    def test_quadratic_gives_exact_half_gradient(self):
        rng = random.Random(1)
        for _ in range(5):
            th, a, w = rng.uniform(-3, 3), rng.uniform(0.05, 0.5), rng.uniform(5, 50)
            got = demodulated_average(lambda x: (x - 2.0) ** 2 + 1.0, th, a, w)
            self.assertAlmostEqual(got, (a / 2) * 2 * (th - 2.0), places=10)

    def test_quartic_has_third_order_bias(self):
        # (theta + a s)^4 s averages to 4 theta^3 a / 2 + 4 theta a^3 (3 / 8)
        th, a = 1.0, 0.1
        got = demodulated_average(lambda x: x ** 4, th, a, 10.0)
        self.assertAlmostEqual(got, 2 * th ** 3 * a + 1.5 * th * a ** 3, places=10)


class TestClosedLoop(unittest.TestCase):
    def test_tracks_averaged_gradient_flow(self):
        # averaged system: thetah' = -k a (thetah - 2), so thetah = 2 - 2 exp(-k a t)
        a, k = 0.2, 1.0
        ts, ths, _ = esc_simulate(quad, [a], [50.0], [k], 5.0, [0.0], T1, DT)
        dev = max(abs(v[0] - (2.0 - 2.0 * math.exp(-k * a * t))) for t, v in zip(ts, ths))
        self.assertLess(dev, 0.02)

    def test_maximum_with_negative_gain(self):
        ts, ths, _ = esc_simulate(lambda th: 1.0 - (th[0] - 2.0) ** 2, [0.2], [50.0], [-1.0], 5.0, [0.0], T1, DT)
        self.assertLess(max(abs(v[0] - 2.0) for t, v in zip(ts, ths) if t >= 25.0), 0.02)

    def test_against_grid_search(self):
        # reference: brute force minimum of exp(theta) - 2 theta on a grid of step 0.001
        def J(th):
            return math.exp(th[0]) - 2.0 * th[0]
        best = min((J([i / 1000.0]), i / 1000.0) for i in range(-3000, 3001))[1]
        self.assertAlmostEqual(best, math.log(2.0), places=3)
        ts, ths, _ = esc_simulate(J, [0.2], [50.0], [1.0], 5.0, [0.0], T1, DT)
        self.assertLess(max(abs(v[0] - best) for t, v in zip(ts, ths) if t >= 25.0), 0.02)

    def test_two_parameters_distinct_frequencies(self):
        def J(th):
            return (th[0] - 1.0) ** 2 + 2.0 * (th[1] + 1.0) ** 2 + 3.0
        ts, ths, _ = esc_simulate(J, [0.2, 0.2], [50.0, 70.0], [1.0, 1.0], 5.0, [0.0, 0.0], T1, DT)
        # averaged system: theta1 = 1 - exp(-0.2 t), theta2 = -1 + exp(-0.4 t)
        dev = max(max(abs(v[0] - (1 - math.exp(-0.2 * t))), abs(v[1] - (-1 + math.exp(-0.4 * t))))
                  for t, v in zip(ts, ths))
        self.assertLess(dev, 0.03)
        self.assertLess(max(abs(ths[-1][0] - 1.0), abs(ths[-1][1] + 1.0)), 0.01)

    def test_poor_time_scale_separation(self):
        # k = 5, omega = 10, washout h = 1: it still converges, but far from the averaged flow
        ts, ths, _ = esc_simulate(quad, [0.1], [10.0], [5.0], 1.0, [0.0], T1, DT)
        dev = max(abs(v[0] - (2.0 - 2.0 * math.exp(-0.5 * t))) for t, v in zip(ts, ths))
        self.assertGreater(dev, 1.0)
        self.assertLess(abs(ths[-1][0] - 2.0), 0.01)

    def test_dt_must_divide_t1(self):
        with self.assertRaises(AssertionError):
            esc_simulate(quad, [0.1], [10.0], [1.0], 1.0, [0.0], 1.0, 0.3)


if __name__ == "__main__":
    unittest.main()
