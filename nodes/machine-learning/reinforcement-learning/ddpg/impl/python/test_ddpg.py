# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ddpg/. The authors are listed in prov/CP12JX.jsonl.

import math
import random
from fractions import Fraction as F

from ddpg import actor_gradient, critic_gradient, critic_targets, ddpg, dot, ou_step, soft_update


def f(s):
    return [s]


def g(s, a):
    return [s * s, s * a, a * a]


def dg(s, a):
    return [0 * s, s, 2 * a]


def test_soft_update_closed_form():
    # with the online weights fixed, theta'_k = theta + (1 - tau)^k (theta'_0 - theta)
    online, target0, tau = [F(3), F(-1, 2)], [F(0), F(5)], F(1, 10)
    target = list(target0)
    for k in range(1, 30):
        target = soft_update(target, online, tau)
        assert target == [o + (1 - tau) ** k * (t - o) for o, t in zip(online, target0)]
    # tau = 1 copies the online weights, as in DQN's hard update
    assert soft_update(target0, online, F(1)) == online


def test_ou_noise_without_diffusion_decays_geometrically():
    x, rng = F(2), random.Random(0)
    for t in range(1, 20):
        x = ou_step(x, rng, theta=F(3, 20), sigma=0, mean=F(1, 2))
        assert x == F(1, 2) + (1 - F(3, 20)) ** t * (2 - F(1, 2))


def test_ou_noise_is_correlated_with_the_right_variance():
    rng = random.Random(1)
    xs, x = [], 0.0
    for _ in range(40000):
        x = ou_step(x, rng, theta=0.15, sigma=0.2)
        xs.append(x)
    m = sum(xs) / len(xs)
    var = sum((v - m) ** 2 for v in xs) / len(xs)
    lag1 = sum((xs[i] - m) * (xs[i + 1] - m) for i in range(len(xs) - 1)) / (len(xs) - 1) / var
    # x' = 0.85 x + 0.2 e has stationary variance 0.04 / (1 - 0.85^2) and lag-one correlation 0.85
    assert abs(var - 0.04 / (1 - 0.85 ** 2)) < 0.02
    assert abs(lag1 - 0.85) < 0.02


def test_targets_use_target_networks():
    batch = [(F(1), F(2), F(-3), F(2), False), (F(0), F(1), F(5), F(-1), True)]
    theta_t, w_t = [F(-1, 2)], [F(1), F(2), F(3)]
    ys = critic_targets(batch, F(1, 2), theta_t, w_t, f, g)
    # s' = 2, mu'(2) = -1, Q'(2, -1) = 4 - 4 + 3 = 3, so y = -3 + 3/2; the second ends the episode
    assert ys == [F(-3, 2), F(5)]
    # the online weights do not enter
    assert critic_targets(batch, F(1, 2), theta_t, w_t, f, g) == critic_targets(batch, F(1, 2), theta_t, list(w_t), f, g)


def test_critic_and_actor_gradients_are_exact_derivatives():
    rng = random.Random(2)
    for _ in range(20):
        batch = [(F(rng.randint(-3, 3)), F(rng.randint(-3, 3)), F(rng.randint(-3, 3)), F(0), False) for _ in range(5)]
        ys = [F(rng.randint(-9, 9)) for _ in batch]
        w = [F(rng.randint(-3, 3), 2) for _ in range(3)]
        theta = [F(rng.randint(-3, 3), 4)]

        def loss(w):
            return sum((dot(w, g(s, a)) - y) ** 2 for (s, a, _, _, _), y in zip(batch, ys)) / len(batch)

        def objective(theta):
            return sum(dot(w, g(s, dot(theta, f(s)))) for s, _, _, _, _ in batch) / len(batch)

        # both functions are quadratic, so the central difference with h = 1 is exact
        gw = critic_gradient(w, batch, ys, g)
        for i in range(3):
            e = [F(1) if j == i else F(0) for j in range(3)]
            up = [x + y for x, y in zip(w, e)]
            dn = [x - y for x, y in zip(w, e)]
            assert (loss(up) - loss(dn)) / 2 == gw[i]
        ga = actor_gradient(theta, w, batch, f, dg)
        assert (objective([theta[0] + 1]) - objective([theta[0] - 1])) / 2 == ga[0]


def test_ddpg_learns_the_lqr_gain():
    # s' = s + a, r = -(s^2 + a^2), gamma = 0.9: V*(s) = -P s^2 with 0.9 P^2 - 0.8 P - 1 = 0
    P = (0.8 + math.sqrt(0.64 + 3.6)) / 1.8
    k_star = -0.9 * P / (1 + 0.9 * P)

    def step(s, a, rng):
        return -(s * s + a * a), s + a, False

    def reset(rng):
        return rng.uniform(-1, 1)

    theta, w = ddpg(step, reset, f, g, lambda s, a: [0.0, s, 2 * a], [-0.2], [0.0, 0.0, 0.0], 0.9, 6000,
                    random.Random(0), eta_actor=0.02, eta_critic=0.02, tau=0.05, horizon=10, ou_sigma=0.1)
    assert abs(theta[0] - k_star) < 0.15
    # the critic's greedy action -w1 s / (2 w2) agrees with the actor
    assert abs(-w[1] / (2 * w[2]) - theta[0]) < 0.1
