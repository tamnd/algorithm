# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/periodogram/. The authors are listed in prov/6S1Y6B.jsonl.

import cmath
import math
import random

import pytest

from periodogram import dft, fft, frequencies, hann, periodogram


def brute(x, w, m, size):
    """The defining sum at w_m = 2 pi m / size, one term at a time."""
    n = len(x)
    u = sum(v * v for v in w) / n
    s = 0j
    for k in range(n):
        s += w[k] * x[k] * cmath.exp(-2j * math.pi * m * k / size)
    return abs(s) ** 2 / (n * u)


def test_page_example() -> None:
    x = [1, 1, 1, 1, -1, -1, -1, -1]
    p = periodogram(x)
    r2 = math.sqrt(2)
    expect = [0, 2 + r2, 0, 2 - r2, 0, 2 - r2, 0, 2 + r2]
    assert all(abs(a - b) < 1e-12 for a, b in zip(p, expect))
    # the mean of P over the grid is the sample power (1/N) sum of x^2 = 1
    assert abs(sum(p) / len(p) - 1) < 1e-12
    padded = periodogram(x, 16)
    assert all(abs(padded[2 * m] - p[m]) < 1e-12 for m in range(8))
    # X(w) = (1 - e^(-4iw)) sum_{n<4} e^(-iwn), so P(pi/8) = (2 sin^2(pi/4) / sin(pi/16))^2 / 8 = 1 / (8 sin^2(pi/16))
    assert abs(padded[1] - 1 / (8 * math.sin(math.pi / 16) ** 2)) < 1e-12


def test_edges() -> None:
    assert periodogram([3.0]) == [9.0]
    assert periodogram([0, 0, 0, 0]) == [0, 0, 0, 0]
    with pytest.raises(ValueError):
        periodogram([])
    with pytest.raises(ValueError):
        periodogram([1, 2, 3], 2)
    with pytest.raises(ValueError):
        periodogram([1, 2], window=[1.0])
    with pytest.raises(ValueError):
        periodogram([1, 2], window=[0.0, 0.0])
    with pytest.raises(ValueError):
        fft([1, 2, 3])
    f = frequencies(4)
    assert f == [0, math.pi / 2, -math.pi, -math.pi / 2]


def test_against_defining_sum() -> None:
    rng = random.Random(4401)
    for _ in range(500):
        n = rng.randint(1, 20)
        size = rng.choice((n, n + rng.randint(0, 7), 1 << max(0, (n - 1).bit_length())))
        x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        w = hann(n) if rng.random() < 0.5 and n > 1 else [1.0] * n
        p = periodogram(x, size, w)
        energy = sum(abs(v) ** 2 for v in x) + 1e-300
        for m in range(size):
            assert abs(p[m] - brute(x, w, m, size)) <= 1e-11 * energy


def test_fft_matches_direct_dft() -> None:
    rng = random.Random(4402)
    for size in (1, 2, 4, 8, 16, 32, 64):
        a = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(size)]
        assert all(abs(u - v) < 1e-10 for u, v in zip(fft(a), dft(a)))


def test_parseval_mean_over_grid() -> None:
    rng = random.Random(4403)
    for _ in range(500):
        n = rng.randint(1, 16)
        x = [rng.uniform(-2, 2) for _ in range(n)]
        size = n + rng.randint(0, 9)
        p = periodogram(x, size)
        assert abs(sum(p) / size - sum(v * v for v in x) / n) < 1e-10


def _bin_variance(n: int, seeds: range) -> tuple[float, float]:
    """Mean and variance of P at the bin m = N/4 over one white Gaussian record per seed."""
    vals = []
    for seed in seeds:
        rng = random.Random(seed)
        x = [rng.gauss(0, 1) for _ in range(n)]
        vals.append(periodogram(x)[n // 4])
    mean = sum(vals) / len(vals)
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, var


def test_not_consistent_on_white_noise() -> None:
    # sigma = 1, so the exact law at an interior bin is Exp(1): mean 1, variance 1, for every N.
    # The sample variance of 300 Exp(1) values has standard error about sqrt(8 / 300) = 0.16.
    seeds = range(5000, 5300)
    results = {n: _bin_variance(n, seeds) for n in (64, 256, 1024)}
    for n, (mean, var) in results.items():
        assert abs(mean - 1) < 0.2
        assert 0.55 < var < 1.6
    # the variance does not shrink by the factor 16 that a consistent estimator of rate 1/N would show
    assert results[1024][1] > results[64][1] / 4


def test_exponential_law_at_a_bin() -> None:
    # P(P > t) = e^(-t) for Exp(1); measure at t = 1 over 2000 records of N = 32 (seed 4404).
    rng = random.Random(4404)
    above = 0
    trials = 2000
    for _ in range(trials):
        x = [rng.gauss(0, 1) for _ in range(32)]
        above += periodogram(x)[5] > 1
    expect = math.exp(-1)
    sd = math.sqrt(expect * (1 - expect) / trials)
    assert abs(above / trials - expect) < 4 * sd


def test_sinusoid_peak_and_leakage() -> None:
    n = 64
    on_bin = [math.cos(2 * math.pi * 8 * k / n) for k in range(n)]
    p = periodogram(on_bin)
    assert abs(p[8] - n / 4) < 1e-9 and abs(p[56] - n / 4) < 1e-9
    assert all(p[m] < 1e-18 for m in range(n) if m not in (8, 56))
    off_bin = [math.cos(2 * math.pi * 8.5 * k / n) for k in range(n)]
    q = periodogram(off_bin)
    rect_far = q[20]
    h = periodogram(off_bin, window=hann(n))
    # the Hann window cuts the leakage 12 bins away by a large factor
    assert h[20] < rect_far / 1000
