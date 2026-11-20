# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dft-based-channel-estimation/. The authors are listed in prov/Q4YZBD.jsonl.

import cmath
import math
import random

import cbb
from dft_based_channel_estimation import estimate, estimate_comb

S = 1 / math.sqrt(2)


def qpsk(rng: random.Random, n: int) -> list[complex]:
    return [complex(rng.choice((S, -S)), rng.choice((S, -S))) for _ in range(n)]


def response(h: list[complex], n: int) -> list[complex]:
    return cbb.dft(list(h) + [0j] * (n - len(h)))


def mse(a: list[complex], b: list[complex]) -> float:
    return sum(abs(u - v) ** 2 for u, v in zip(a, b)) / len(a)


def test_exact_without_noise() -> None:
    rng = random.Random(1)
    n = 32
    for length, taps in ((1, 1), (3, 3), (4, 8), (8, 8)):
        h = [cbb.cn(rng, 1 / length) for _ in range(length)]
        hf = response(h, n)
        x = qpsk(rng, n)
        y = [a * b for a, b in zip(hf, x)]
        assert mse(estimate(y, x, taps), hf) < 1e-24


def test_projection_is_idempotent_and_keeps_the_taps() -> None:
    # The steps L2 to L4 form an orthogonal projection: applying them twice changes nothing.
    rng = random.Random(2)
    n, taps = 16, 5
    y = [cbb.cn(rng, 1.0) for _ in range(n)]
    ones = [1 + 0j] * n
    once = estimate(y, ones, taps)
    assert mse(estimate(once, ones, taps), once) < 1e-24
    g = cbb.idft(once)
    assert max(abs(v) for v in g[taps:]) < 1e-12
    assert cbb.norm2(once) <= cbb.norm2(y) + 1e-9


def test_noise_drops_to_taps_over_n() -> None:
    # Closed form with |X[k]| = 1: least squares MSE = N0, DFT-based MSE = L_t N0 / N.
    # N = 64, L_t = 8, N0 = 0.1, 200 symbols, seed 3.
    rng = random.Random(3)
    n, taps, n0 = 64, 8, 0.1
    h = [cbb.cn(rng, p) for p in (0.4, 0.3, 0.2, 0.1)]
    hf = response(h, n)
    e_ls = e_dft = 0.0
    trials = 200
    for _ in range(trials):
        x = qpsk(rng, n)
        y = cbb.awgn(rng, [a * b for a, b in zip(hf, x)], n0)
        e_ls += mse([a / b for a, b in zip(y, x)], hf)
        e_dft += mse(estimate(y, x, taps), hf)
    assert 0.95 < e_ls / trials / n0 < 1.05
    assert 0.9 < e_dft / trials / (taps * n0 / n) < 1.1


def test_comb_version_is_exact_and_has_the_predicted_noise() -> None:
    rng = random.Random(4)
    n, d = 64, 4
    p = n // d
    h = [cbb.cn(rng, q) for q in (0.4, 0.3, 0.2, 0.1)]
    hf = response(h, n)
    for k0 in (0, 1, 3):
        xp = qpsk(rng, p)
        y = [0j] * n
        for i in range(p):
            y[k0 + i * d] = hf[k0 + i * d] * xp[i]
        assert mse(estimate_comb(y, xp, d, 4, k0), hf) < 1e-24
        assert mse(estimate_comb(y, xp, d, p, k0), hf) < 1e-24
    # Closed form: each kept tap has noise variance N0 / P, so the MSE is L_t N0 / P.
    n0, taps, k0 = 0.1, 6, 2
    acc = 0.0
    trials = 300
    for _ in range(trials):
        xp = qpsk(rng, p)
        y = [0j] * n
        for i in range(p):
            y[k0 + i * d] = hf[k0 + i * d] * xp[i] + cbb.cn(rng, n0)
        acc += mse(estimate_comb(y, xp, d, taps, k0), hf)
    assert 0.9 < acc / trials / (taps * n0 / p) < 1.1


def test_a_delay_between_samples_leaks_into_all_taps() -> None:
    # A path at delay 2.5 samples: H[k] = e^(-j 2 pi k 2.5 / N) for k < N / 2, a smooth phase ramp
    # (taken on the symmetric index range). Its inverse DFT spreads over all N taps, so cutting at
    # L_t leaves an error floor even with no noise. A measurement: the floor falls as L_t grows.
    n = 64
    hf = [cmath.exp(-2j * math.pi * (k if k < n // 2 else k - n) * 2.5 / n) for k in range(n)]
    ones = [1 + 0j] * n
    floors = [mse(estimate(hf, ones, t), hf) for t in (4, 8, 16)]
    assert floors[0] > 1e-2
    assert floors[0] > floors[1] > floors[2] > 0
