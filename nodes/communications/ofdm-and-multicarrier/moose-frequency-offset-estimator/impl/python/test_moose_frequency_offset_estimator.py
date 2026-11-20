# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moose-frequency-offset-estimator/. The authors are listed in prov/6JQ8CA.jsonl.

import cmath
import math
import random

import cbb
from moose_frequency_offset_estimator import correlation, estimate, estimate_time_domain

S = 1 / math.sqrt(2)


def qpsk(rng: random.Random, n: int) -> list[complex]:
    return [complex(rng.choice((S, -S)), rng.choice((S, -S))) for _ in range(n)]


def apply_cfo(r: list[complex], eps: float, n: int) -> list[complex]:
    return [x * cmath.exp(2j * math.pi * eps * i / n) for i, x in enumerate(r)]


def two_copies(rng: random.Random, n: int, ncp: int, each_prefix: bool) -> tuple[list[complex], int, int]:
    """The repeated symbol: one prefix then two copies (G = 0), or a prefix before each copy (G = ncp).

    Returns the samples, the start of the first copy and G.
    """
    x = cbb.uidft(qpsk(rng, n))
    pre = x[n - ncp:]
    if each_prefix:
        return pre + x + pre + x, ncp, ncp
    return pre + x + x, ncp, 0


def test_plancherel_gives_the_same_correlation() -> None:
    rng = random.Random(1)
    a = [cbb.cn(rng, 1.0) for _ in range(32)]
    b = [cbb.cn(rng, 1.0) for _ in range(32)]
    c = sum(x.conjugate() * y for x, y in zip(a, b))
    assert abs(correlation(a, b) - c) < 1e-9
    assert abs(estimate(a, b, 5) - estimate_time_domain(a, b, 5)) < 1e-12


def test_exact_without_noise_through_a_multipath_channel() -> None:
    rng = random.Random(2)
    n, ncp, h = 32, 4, [0.8, -0.4j, 0.3, 0.2 + 0.1j]
    for each_prefix in (False, True):
        for eps in (0.0, 0.07, -0.33, 0.39):
            s, start, gap = two_copies(rng, n, ncp, each_prefix)
            r = apply_cfo(cbb.conv(s, h), eps, n)
            y1 = r[start:start + n]
            y2 = r[start + n + gap:start + 2 * n + gap]
            assert abs(estimate(y1, y2, gap) - eps) < 1e-9


def test_range_shrinks_with_the_gap() -> None:
    # G = 0: range 1/2, so 0.6 reads as -0.4. G = N / 4: range N / (2 (N + G)) = 0.4, so 0.45 reads as -0.35.
    rng = random.Random(3)
    n = 32
    for gap, eps, seen in ((0, 0.6, -0.4), (8, 0.45, -0.35)):
        x = cbb.uidft(qpsk(rng, n))
        r = apply_cfo(x + [0j] * gap + x, eps, n)
        assert abs(estimate(r[:n], r[n + gap:], gap) - seen) < 1e-9


def test_matches_a_grid_search_of_the_likelihood() -> None:
    # Two copies Y2 = e^(j 2 pi eps) Y1 in white Gaussian noise: the ML estimate maximizes
    # Re(e^(-j 2 pi eps) C). A grid of 20001 points on [-1/2, 1/2] finds the same value.
    rng = random.Random(4)
    n = 16
    x = cbb.uidft(qpsk(rng, n))
    r = cbb.awgn(rng, apply_cfo(x + x, 0.21, n), 0.3)
    y1, y2 = r[:n], r[n:]
    c = correlation(y1, y2)
    grid = [-0.5 + i / 20000 for i in range(20001)]
    best = max(grid, key=lambda e: (cmath.exp(-2j * math.pi * e) * c).real)
    assert abs(best - estimate(y1, y2)) <= 1 / 40000 + 1e-12


def test_variance_at_10_db() -> None:
    # Unit-energy 4-QAM on N = 16 subcarriers, so each copy has energy N. With SNR = 10 dB per sample,
    # var(eps_hat) is about (1 / (4 pi^2 N SNR)) (1 + 1 / (2 SNR)) = 1.6623e-4. 2000 trials, seed 5.
    rng = random.Random(5)
    n, n0, eps = 16, 0.1, 0.1
    expect = (1 + n0 / 2) * n0 / (4 * math.pi ** 2 * n)
    assert abs(expect - 1.6623e-4) < 1e-8
    x = cbb.uidft(qpsk(rng, n))
    s = apply_cfo(x + x, eps, n)
    acc = 0.0
    trials = 2000
    for _ in range(trials):
        r = cbb.awgn(rng, s, n0)
        acc += (estimate(r[:n], r[n:]) - eps) ** 2
    assert 0.85 < acc / trials / expect < 1.15
