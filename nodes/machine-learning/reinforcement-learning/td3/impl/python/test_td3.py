# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/td3/. The authors are listed in prov/K6H73Z.jsonl.

import math
import random
from fractions import Fraction as F
from itertools import product

from td3 import clipped_double_q_targets, smoothed_target_action, td3, update


class FixedNoise:
    """Stands in for random.Random: gauss returns the given values in turn."""

    def __init__(self, values):
        self.values, self.i = list(values), 0

    def gauss(self, mu, sigma):
        v = self.values[self.i % len(self.values)]
        self.i += 1
        return v


def f(s):
    return [s]


def g(s, a):
    return [s * s, s * a, a * a, 1 + 0 * s]


def dg(s, a):
    return [0 * s, s, 2 * a, 0 * s]


def test_clipped_double_q_target_uses_the_smaller_critic():
    theta_t = [F(-1, 2)]
    w1_t = [F(-1), F(0), F(-1), F(0)]
    w2_t = [F(-2), F(0), F(0), F(1)]
    batch = [(F(0), F(0), F(1), F(2), False), (F(0), F(0), F(1), F(0), False), (F(0), F(0), F(7), F(2), True)]
    ys = clipped_double_q_targets(batch, F(1, 2), theta_t, w1_t, w2_t, f, g, FixedNoise([0]), F(1, 5), F(1, 2))
    # s' = 2, a~ = -1: Q'_1 = -4 - 1 = -5, Q'_2 = -8 + 1 = -7, min = -7, y = 1 - 7/2
    # s' = 0, a~ = 0: Q'_1 = 0, Q'_2 = 1, min = 0, y = 1; the last transition ends the episode
    assert ys == [F(-5, 2), F(1), F(7)]


def test_target_policy_noise_is_clipped():
    theta_t, c = [F(2)], F(1, 2)
    rng = FixedNoise([F(3), F(-3), F(1, 10), F(-1, 2)])
    got = [smoothed_target_action(theta_t, f, F(1), rng, F(1, 5), c) for _ in range(4)]
    assert got == [F(5, 2), F(3, 2), F(21, 10), F(3, 2)]


def test_actor_and_targets_are_delayed():
    batch = [(F(1), F(1, 2), F(-1), F(1), False), (F(-1), F(1), F(-2), F(0), False)]
    params = ([F(-1, 5)], [F(0)] * 4, [F(-1, 10), F(0), F(-1, 10), F(0)], [F(-1, 5)], [F(0)] * 4, [F(-1, 10), F(0), F(-1, 10), F(0)])
    for d in [1, 2, 3]:
        p = params
        for it in range(1, 7):
            new = update(p, batch, it, F(9, 10), f, g, dg, FixedNoise([F(1, 10), F(-1, 10)]), F(1, 10), F(1, 10), F(1, 2), F(1, 5), F(1, 2), d)
            assert new[1] != p[1] and new[2] != p[2]  # both critics move at every update
            moved = [new[i] != p[i] for i in (0, 3, 4, 5)]  # actor and the three targets
            assert moved == [it % d == 0] * 4
            p = new


def test_minimum_of_two_unbiased_estimates_is_biased_down():
    # two independent unbiased estimates q + e1 and q + e2 with e uniform on {-1, 0, 1}
    q = F(5)
    vals = [q + e1 for e1 in (-1, 0, 1)]
    mean_min = sum(min(a, b) for a, b in product(vals, vals)) / 9
    mean_max = sum(max(a, b) for a, b in product(vals, vals)) / 9
    assert mean_min == q - F(4, 9) and mean_max == q + F(4, 9)


def test_td3_learns_the_lqr_gain():
    P = (0.8 + math.sqrt(0.64 + 3.6)) / 1.8
    k_star = -0.9 * P / (1 + 0.9 * P)

    def step(s, a, rng):
        return -(s * s + a * a), s + a, False

    def reset(rng):
        return rng.uniform(-1, 1)

    theta, w1, w2 = td3(step, reset, f, g, dg, [-0.2], [0.0] * 4, [-0.1, 0.0, -0.1, 0.0], 0.9, 6000, random.Random(0),
                        eta_actor=0.03, eta_critic=0.03, tau=0.05, horizon=10, sigma_explore=0.1,
                        sigma_target=0.1, c=0.25, low=-2.0, high=2.0)
    assert abs(theta[0] - k_star) < 0.15
    assert abs(-w1[1] / (2 * w1[2]) - theta[0]) < 0.15
