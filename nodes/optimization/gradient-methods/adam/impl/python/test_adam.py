# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adam/. The authors are listed in prov/F3F4VF.jsonl.

import math
import random

from adam import adam


def test_example_trace_ill_conditioned_quadratic() -> None:
    # F = (100 x1^2 + x2^2) / 2, alpha = 0.1, default betas, eps = 0: the first step is exactly alpha per coordinate.
    xs = adam(lambda t, x: [100 * x[0], x[1]], [1.0, 1.0], 0.1, 0.9, 0.999, 8, eps=0.0)
    want = [1.0, 0.9, 0.80041, 0.70159, 0.60394, 0.50796, 0.41424, 0.32342, 0.23626]
    for x, w in zip(xs, want):
        assert abs(x[0] - w) <= 5e-6 and abs(x[1] - w) <= 5e-6


def test_constant_gradient_steps_are_exactly_alpha() -> None:
    # Bias correction: with g_t = c, m_hat_t = c and v_hat_t = c^2 for every t, so each step is alpha sign(c).
    for c in (-7.0, 0.003, 250.0):
        xs = adam(lambda t, x: [c], [0.0], 0.01, 0.9, 0.999, 50, eps=0.0)
        for t in range(50):
            assert abs((xs[t][0] - xs[t + 1][0]) - 0.01 * math.copysign(1.0, c)) <= 1e-14


def test_corrected_moments_are_weighted_averages() -> None:
    # The bias-corrected weights add up to 1, so m_hat lies in [min g, max g] and v_hat in [min g^2, max g^2].
    for seed in range(20):
        r = random.Random(seed)
        lo, hi = sorted([r.uniform(-3, 3), r.uniform(-3, 3)])
        gs = [r.uniform(lo, hi) for _ in range(200)]
        seen: list[tuple[float, float]] = []
        adam(lambda t, x: [gs[t]], [0.0], 0.1, 0.9, 0.999, 200, observer=lambda t, m, v: seen.append((m[0], v[0])))
        sq = [g * g for g in gs]
        for t, (m, v) in enumerate(seen, start=1):
            assert lo - 1e-12 <= m <= hi + 1e-12
            assert min(sq[:t]) * (1 - 1e-12) <= v <= max(sq[:t]) * (1 + 1e-12)


def test_step_bound_every_step() -> None:
    # If gamma = beta1^2 / beta2 < 1, then
    # |dx_t| <= alpha (1 - b1) / (1 - b1^t) * sqrt((1 - b2^t) / (1 - b2)) * sqrt((1 - gamma^t) / (1 - gamma)).
    for seed in range(20):
        r = random.Random(100 + seed)
        b1, b2 = r.choice([(0.9, 0.999), (0.5, 0.3), (0.0, 0.9), (0.9, 0.82)])
        alpha, gamma = r.uniform(0.01, 1.0), b1 * b1 / b2
        gs = [[r.gauss(0, 1) * 10 ** r.randint(-3, 3), 2.0**t if t < 40 else 0.0] for t in range(300)]
        xs = adam(lambda t, x: gs[t], [0.0, 0.0], alpha, b1, b2, 300, eps=0.0)
        for t in range(1, 301):
            bound = alpha * (1 - b1) / (1 - b1**t) * math.sqrt((1 - b2**t) / (1 - b2) * (1 - gamma**t) / (1 - gamma))
            assert all(abs(p - q) <= bound * (1 + 1e-9) for p, q in zip(xs[t - 1], xs[t]))


def test_bias_correction_is_unbiased_monte_carlo() -> None:
    # i.i.d. gradients g = mu + sigma Z: E m_hat_t = mu and E v_hat_t = mu^2 + sigma^2 for every t.
    # 4000 seeds; tolerance 5 standard errors, computed from the exact weights.
    mu, sigma, b1, b2, steps, seeds = 0.5, 2.0, 0.9, 0.999, 10, 4000
    sum_m, sum_v = [0.0] * steps, [0.0] * steps
    for seed in range(seeds):
        r = random.Random(seed)
        gs = [mu + sigma * r.gauss(0, 1) for _ in range(steps)]

        def record(t: int, m: list[float], v: list[float]) -> None:
            sum_m[t - 1] += m[0]
            sum_v[t - 1] += v[0]

        adam(lambda t, x: [gs[t]], [0.0], 0.1, b1, b2, steps, observer=record)
    var_g, var_g2 = sigma**2, 4 * mu**2 * sigma**2 + 2 * sigma**4
    for t in range(1, steps + 1):
        w1 = [(1 - b1) * b1 ** (t - s) / (1 - b1**t) for s in range(1, t + 1)]
        w2 = [(1 - b2) * b2 ** (t - s) / (1 - b2**t) for s in range(1, t + 1)]
        assert abs(sum(w1) - 1) <= 1e-12 and abs(sum(w2) - 1) <= 1e-12
        se_m = math.sqrt(var_g * sum(w * w for w in w1) / seeds)
        se_v = math.sqrt(var_g2 * sum(w * w for w in w2) / seeds)
        assert abs(sum_m[t - 1] / seeds - mu) <= 5 * se_m
        assert abs(sum_v[t - 1] / seeds - (mu**2 + sigma**2)) <= 5 * se_v


def test_reddi_kale_kumar_counterexample_with_bias_correction() -> None:
    # f_t(x) = C x if t = 1 mod 3, else -x, on [-1, 1]; beta1 = 0, beta2 = 1 / (1 + C^2), alpha_t = alpha / sqrt(t).
    # These settings meet the assumptions of Kingma and Ba's Theorem 4.1, yet the average regret stays >= 2 (C - 2) / 3.
    big_c, rounds = 3.0, 3000
    gs = [[big_c if t % 3 == 0 else -1.0] for t in range(rounds)]
    for alpha in (0.1, 0.5, 2.0):
        xs = adam(
            lambda t, x: gs[t], [1.0], lambda t: alpha / math.sqrt(t), 0.0, 1 / (1 + big_c**2), rounds,
            eps=0.0, lower=[-1.0], upper=[1.0],
        )
        assert all(xs[t][0] == 1.0 for t in range(0, rounds, 3))  # x = 1 at the start of every period
        played = sum(g[0] * x[0] for g, x in zip(gs, xs))
        best = -abs(sum(g[0] for g in gs))
        assert (played - best) / rounds >= 2 * (big_c - 2) / 3 - 1e-12


def test_zero_iterations() -> None:
    assert adam(lambda t, x: x, [1.0], 0.1, 0.9, 0.999, 0) == [[1.0]]
