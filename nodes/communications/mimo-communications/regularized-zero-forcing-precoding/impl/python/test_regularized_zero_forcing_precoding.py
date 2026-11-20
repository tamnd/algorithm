# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regularized-zero-forcing-precoding/. The authors are listed in prov/E77HBP.jsonl.

import math
import random

import cbb
from regularized_zero_forcing_precoding import rzf_precoder, sinr, sum_mse, sum_rate


def rand_h(rng: random.Random, k: int, m: int) -> list[list[complex]]:
    return [[cbb.cn(rng, 1.0) for _ in range(m)] for _ in range(k)]


def max_abs(a: list[list[complex]]) -> float:
    return max(abs(x) for row in a for x in row)


def test_example() -> None:
    h = [[2, 1], [1, 1]]
    w, beta, f = rzf_precoder(h, 10.0, 1.0)
    want_f = [[1.4 / 2.44, -0.8 / 2.44], [-0.8 / 2.44, 2.2 / 2.44]]
    assert max_abs(cbb.sub(f, want_f)) < 1e-12
    assert abs(beta - math.sqrt(10 / (8.08 / 2.44**2))) < 1e-12
    s = sinr(h, w, 1.0)
    assert abs(s[0] - 3.4247) < 5e-5 and abs(s[1] - 1.6781) < 5e-5
    assert abs(sum_rate(h, w, 1.0) - 3.5668) < 5e-5
    assert abs(sum_mse(h, f, 10.0, 1.0) - 0.2 * 7.4 / 2.44) < 1e-12


def test_power_constraint() -> None:
    rng = random.Random(1)
    for k, m in [(1, 1), (2, 2), (3, 5), (4, 4), (8, 8)]:
        h = rand_h(rng, k, m)
        pt = rng.uniform(0.1, 100.0)
        w, _, _ = rzf_precoder(h, pt, rng.uniform(0.1, 2.0))
        assert abs(cbb.norm2(w) - pt) < 1e-9 * pt


def test_stationarity_kkt() -> None:
    # The gradient of ||I - H F||^2 + alpha ||F||^2 is H^H (H F - I) + alpha F; it vanishes at the optimum.
    rng = random.Random(2)
    for k, m in [(2, 2), (3, 4), (4, 8)]:
        h = rand_h(rng, k, m)
        pt, n0 = 5.0, 0.7
        alpha = k * n0 / pt
        _, _, f = rzf_precoder(h, pt, n0)
        grad = cbb.add(cbb.matmul(cbb.herm(h), cbb.sub(cbb.matmul(h, f), cbb.eye(k))), cbb.scale(alpha, f))
        assert max_abs(grad) < 1e-9


def test_perturbations_increase_the_mse() -> None:
    rng = random.Random(3)
    h = rand_h(rng, 3, 4)
    pt, n0 = 4.0, 1.0
    _, _, f = rzf_precoder(h, pt, n0)
    best = sum_mse(h, f, pt, n0)
    for _ in range(200):
        d = [[cbb.cn(rng, 1e-2) for _ in range(3)] for _ in range(4)]
        assert sum_mse(h, cbb.add(f, d), pt, n0) >= best - 1e-12


def test_grid_search_real_two_users() -> None:
    # The sum MSE separates over the columns of F. For a real 2 by 2 channel,
    # a grid over each real column finds no better value than the closed form.
    rng = random.Random(4)
    for _ in range(3):
        h = [[rng.gauss(0, 1) for _ in range(2)] for _ in range(2)]
        pt, n0 = 3.0, 1.0
        alpha = 2 * n0 / pt
        _, _, f = rzf_precoder(h, pt, n0)
        best = sum_mse(h, f, pt, n0)
        grid_total = 0.0
        for k in range(2):
            fk = [f[0][k].real, f[1][k].real]
            col_best = math.inf
            for i in range(-60, 61):
                for j in range(-60, 61):
                    a, b = fk[0] + i * 0.02, fk[1] + j * 0.02
                    e0 = (1 if k == 0 else 0) - (h[0][0] * a + h[0][1] * b)
                    e1 = (1 if k == 1 else 0) - (h[1][0] * a + h[1][1] * b)
                    col_best = min(col_best, e0 * e0 + e1 * e1 + alpha * (a * a + b * b))
            grid_total += col_best
        assert best <= grid_total + 1e-12
        assert grid_total - best < 1e-3


def test_minimum_mse_closed_form() -> None:
    # The minimum is alpha tr((H H^H + alpha I)^(-1)).
    rng = random.Random(5)
    for k, m in [(2, 2), (3, 6), (5, 5)]:
        h = rand_h(rng, k, m)
        pt, n0 = 8.0, 1.0
        alpha = k * n0 / pt
        _, _, f = rzf_precoder(h, pt, n0)
        g = cbb.matmul(h, cbb.herm(h))
        for i in range(k):
            g[i][i] += alpha
        gi = cbb.inv(g)
        want = alpha * sum(gi[i][i].real for i in range(k))
        assert abs(sum_mse(h, f, pt, n0) - want) < 1e-10


def test_limits_zero_forcing_and_matched_beams() -> None:
    rng = random.Random(6)
    h = rand_h(rng, 3, 4)
    hh = cbb.herm(h)
    # alpha -> 0: H W is diagonal (zero forcing with a common scale).
    w, _, _ = rzf_precoder(h, 1.0, 1.0, alpha=1e-10)
    e = cbb.matmul(h, w)
    assert max(abs(e[i][j]) for i in range(3) for j in range(3) if i != j) < 1e-8
    assert max(abs(e[i][i] - e[0][0]) for i in range(3)) < 1e-8
    # alpha -> infinity: W is proportional to H^H.
    w, _, _ = rzf_precoder(h, 1.0, 1.0, alpha=1e10)
    s = math.sqrt(1.0 / cbb.norm2(hh))
    assert max_abs(cbb.sub(w, cbb.scale(s, hh))) < 1e-8


def test_beats_channel_inversion_on_average() -> None:
    # With K = M = 4 in Rayleigh fading, channel inversion has a poor average SNR, and RZF is much better.
    rng = random.Random(7)
    t, pt, n0 = 100, 10.0, 1.0
    rzf = zf = 0.0
    for _ in range(t):
        h = rand_h(rng, 4, 4)
        w, _, _ = rzf_precoder(h, pt, n0)
        rzf += sum_rate(h, w, n0)
        w, _, _ = rzf_precoder(h, pt, n0, alpha=1e-12)
        zf += sum_rate(h, w, n0)
    assert rzf / t > zf / t + 1.0
