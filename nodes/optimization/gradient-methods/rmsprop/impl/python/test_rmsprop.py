# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rmsprop/. The authors are listed in prov/DDRZ14.jsonl.

import math
import random

from rmsprop import rmsprop

TOL = 1e-12


def test_example_trace_ill_conditioned_quadratic() -> None:
    # F = (100 x1^2 + x2^2) / 2: both coordinates follow the same path, whatever the curvature.
    xs = rmsprop(lambda t, x: [100 * x[0], x[1]], [1.0, 1.0], 0.1, 0.9, 6)
    want = [1.0, 0.68377, 0.49887, 0.36918, 0.27282, 0.1998, 0.1443]
    for x, w in zip(xs, want):
        assert abs(x[0] - w) <= 5e-6 and abs(x[1] - w) <= 5e-6


def test_step_is_bounded_by_eta_over_root_one_minus_beta() -> None:
    # v_t >= (1 - beta) g_t^2, so |x_(t+1),i - x_t,i| <= eta / sqrt(1 - beta) at every step, for any gradients.
    for seed in range(20):
        r = random.Random(seed)
        beta, eta = r.choice([0.5, 0.9, 0.99]), r.uniform(0.01, 1.0)
        gs = [[r.choice([0.0, r.gauss(0, 10 ** r.randint(-3, 3))]) for _ in range(3)] for _ in range(200)]
        xs = rmsprop(lambda t, x: gs[t], [0.0, 0.0, 0.0], eta, beta, 200)
        for a, b in zip(xs, xs[1:]):
            assert all(abs(p - q) <= eta / math.sqrt(1 - beta) * (1 + 1e-12) for p, q in zip(a, b))


def test_constant_gradient_gives_the_bias_formula() -> None:
    # With g_t = c and v_0 = 0, v_t = (1 - beta^t) c^2 exactly, so the step is eta / sqrt(1 - beta^t).
    beta, eta, c = 0.9, 0.05, 3.0
    xs = rmsprop(lambda t, x: [c], [0.0], eta, beta, 40)
    for t in range(1, 41):
        assert abs((xs[t - 1][0] - xs[t][0]) - eta / math.sqrt(1 - beta**t)) <= 1e-12


def test_beta_one_minus_one_over_t_is_adagrad() -> None:
    # beta_t = 1 - 1/t makes v_t the mean of g_1^2, ..., g_t^2; with eta_t = eta / sqrt(t) this is AdaGrad.
    r = random.Random(3)
    gs = [[r.gauss(0, 1), r.choice([0.0, r.gauss(0, 5)])] for _ in range(100)]
    eta = 0.3
    xs = rmsprop(lambda t, x: gs[t], [0.5, -0.5], lambda t: eta / math.sqrt(t), lambda t: 1 - 1 / t, 100)
    x, s = [0.5, -0.5], [0.0, 0.0]
    for t in range(100):
        s = [a + b * b for a, b in zip(s, gs[t])]
        x = [xi - eta * gi / math.sqrt(si) if si > 0 else xi for xi, gi, si in zip(x, gs[t], s)]
        assert max(abs(p - q) for p, q in zip(x, xs[t + 1])) <= 1e-9


def test_reddi_kale_kumar_online_counterexample() -> None:
    # f_t(x) = C x if t = 1 mod 3, else -x, on [-1, 1]; the best fixed point is -1.
    # With beta = 1 / (1 + C^2) and eta_t = alpha / sqrt(t), RMSProp stays at +1 and the average regret stays
    # at 2 (C - 2) / 3 per round instead of going to 0.
    big_c, alpha, rounds = 3.0, 0.5, 3000
    gs = [[big_c if t % 3 == 0 else -1.0] for t in range(rounds)]
    xs = rmsprop(lambda t, x: gs[t], [1.0], lambda t: alpha / math.sqrt(t), 1 / (1 + big_c**2), rounds, lower=[-1.0], upper=[1.0])
    assert xs[3][0] == 1.0  # x_4 = 1, the condition of the proof
    for t in range(3, rounds, 3):
        assert xs[t][0] == 1.0  # it stays at +1 at the start of every later period
    played = sum(g[0] * x[0] for g, x in zip(gs, xs))
    best = -abs(sum(g[0] for g in gs))
    assert (played - best) / rounds >= 2 * (big_c - 2) / 3 - 2 * (big_c - 2) * 1 / rounds


def test_zero_iterations() -> None:
    assert rmsprop(lambda t, x: x, [1.0], 0.1, 0.9, 0) == [[1.0]]
