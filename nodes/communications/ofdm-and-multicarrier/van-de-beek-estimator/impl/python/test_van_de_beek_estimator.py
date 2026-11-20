# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/van-de-beek-estimator/. The authors are listed in prov/9K7QSC.jsonl.

import cmath
import math
import random

import cbb
from van_de_beek_estimator import estimate, statistics


def symbol(rng: random.Random, n: int, l: int, ofdm: bool = False) -> list[complex]:
    """One OFDM symbol with a prefix of l samples.

    With CN(0, 1) subcarrier values and the unitary inverse DFT, the N time
    samples are again independent CN(0, 1), so the default draws them directly.
    ofdm=True builds the symbol from 4-QAM subcarrier values instead.
    """
    if ofdm:
        s = 1 / math.sqrt(2)
        x = cbb.uidft([complex(rng.choice((s, -s)), rng.choice((s, -s))) for _ in range(n)])
    else:
        x = [cbb.cn(rng, 1.0) for _ in range(n)]
    return x[n - l:] + x


def apply_cfo(r: list[complex], eps: float, n: int) -> list[complex]:
    return [x * cmath.exp(2j * math.pi * eps * i / n) for i, x in enumerate(r)]


def wrap(d: int, period: int) -> int:
    """d modulo period, in [-period / 2, period / 2)."""
    return (d + period // 2) % period - period // 2


def test_running_sums_match_the_direct_sums() -> None:
    rng = random.Random(1)
    n, l = 32, 8
    r = [cbb.cn(rng, 1.0) for _ in range(120)]
    gs, phis = statistics(r, n, l)
    assert len(gs) == 120 - n - l + 1
    for t in (0, 5, 33, 80):
        g = sum(r[k] * r[k + n].conjugate() for k in range(t, t + l))
        p = 0.5 * sum(abs(r[k]) ** 2 + abs(r[k + n]) ** 2 for k in range(t, t + l))
        assert abs(gs[t] - g) < 1e-9
        assert abs(phis[t] - p) < 1e-9


def test_exact_without_noise() -> None:
    # No noise: Lambda(theta) = |gamma| - Phi is 0 at the prefix start and negative elsewhere.
    rng = random.Random(2)
    n, l = 64, 16
    for eps in (0.0, 0.12, -0.31, 0.45, -0.5):
        for off in (0, 17, 63, 79):
            s = symbol(rng, n, l, True) + symbol(rng, n, l, True) + symbol(rng, n, l, True)
            r = apply_cfo(s, eps, n)[off:off + 2 * (n + l)]
            theta, e = estimate(r, n, l, 1e9)
            assert wrap(theta - (n + l - off), n + l) == 0
            assert abs(e - eps) < 1e-9


def test_offset_range_is_half_a_spacing() -> None:
    # epsilon and epsilon - 1 give the same gamma, so 0.6 is read as -0.4.
    rng = random.Random(3)
    n, l = 64, 16
    s = symbol(rng, n, l) + symbol(rng, n, l)
    _, e = estimate(apply_cfo(s, 0.6, n), n, l, 1e9)
    assert abs(e + 0.4) < 1e-9


def test_timing_at_10_db() -> None:
    # N = 64, L = 16, SNR = 10 dB per sample, epsilon = 0.2, 150 windows of 2(N + L) samples, seed 4.
    # Measurement: about 95 percent of the estimates are within 2 samples of the prefix start.
    rng = random.Random(4)
    n, l, n0, eps = 64, 16, 0.1, 0.2
    near = 0
    trials = 150
    for _ in range(trials):
        s = symbol(rng, n, l) + symbol(rng, n, l) + symbol(rng, n, l)
        off = rng.randrange(n + l)
        r = cbb.awgn(rng, apply_cfo(s, eps, n), n0)[off:off + 2 * (n + l)]
        theta, _ = estimate(r, n, l, 1 / n0)
        near += abs(wrap(theta - (n + l - off), n + l)) <= 2
    assert near >= 0.9 * trials


def test_variance_at_the_true_start() -> None:
    # For a fixed symbol with prefix energy E, var(epsilon_hat) is about
    # (N0 / E) (1 + L N0 / (2 E)) / (4 pi^2). E = L gives (1 / (4 pi^2 L SNR)) (1 + 1 / (2 SNR)).
    rng = random.Random(5)
    n, l, n0, eps = 64, 16, 0.1, 0.2
    x = apply_cfo(symbol(rng, n, l), eps, n)
    e = sum(abs(v) ** 2 for v in x[:l])
    expect = n0 / e * (1 + l * n0 / (2 * e)) / (4 * math.pi ** 2)
    acc = 0.0
    trials = 2000
    for _ in range(trials):
        r = cbb.awgn(rng, x, n0)
        gs, _ = statistics(r, n, l)
        acc += (-cmath.phase(gs[0]) / (2 * math.pi) - eps) ** 2
    assert 0.85 < acc / trials / expect < 1.15
    assert abs((1 + 1 / 20) / (4 * math.pi ** 2 * 16 * 10) - 1.6623e-4) < 1e-8
