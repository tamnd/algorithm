# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/welch-method/. The authors are listed in prov/N8KZKA.jsonl.

import cmath
import math
import random

import pytest

from welch_method import bartlett, fft, hann, overlap_correlation, segment_count, variance_factor, welch


def brute_welch(x, m, d, w, size):
    """Average of the modified periodograms, each bin by its defining sum."""
    k = (len(x) - m) // d + 1
    u = sum(v * v for v in w) / m
    out = []
    for b in range(size):
        total = 0.0
        for i in range(k):
            s = sum(w[t] * x[i * d + t] * cmath.exp(-2j * math.pi * b * t / size) for t in range(m))
            total += abs(s) ** 2 / (m * u)
        out.append(total / k)
    return out


def test_page_example() -> None:
    # N = 8, M = 4, D = 2: K = 3 segments starting at 0, 2 and 4.
    x = [1, 0, -1, 0, 1, 0, -1, 0]
    assert segment_count(8, 4, 2) == 3
    s = welch(x, 4, 2)
    # every segment is (+-1, 0, -+1, 0): |DFT|^2 / 4 = (0, 1, 0, 1)
    assert all(abs(a - b) < 1e-12 for a, b in zip(s, [0, 1, 0, 1]))
    y = [2, 1, 0, -1, 1, 3, -2, 0]
    expect = brute_welch(y, 4, 2, [1.0] * 4, 4)
    assert all(abs(a - b) < 1e-12 for a, b in zip(welch(y, 4, 2), expect))
    # segment periodograms (1, 2, 1, 2), (9/4, 17/4, 1/4, 17/4) and (1, 9/2, 4, 9/2)
    assert all(abs(a - b) < 1e-12 for a, b in zip(expect, (17 / 12, 43 / 12, 7 / 4, 43 / 12)))


def test_edges() -> None:
    assert segment_count(10, 10, 3) == 1
    assert welch([2.0, 0.0], 2, 1) == pytest.approx([2.0, 2.0])
    with pytest.raises(ValueError):
        segment_count(4, 5, 1)
    with pytest.raises(ValueError):
        segment_count(4, 2, 0)
    with pytest.raises(ValueError):
        welch([1, 2, 3, 4], 4, 1, [1.0] * 3)
    with pytest.raises(ValueError):
        welch([1, 2, 3, 4], 4, 1, None, 2)
    with pytest.raises(ValueError):
        welch([1, 2, 3, 4], 4, 1, [0.0] * 4)


def test_against_brute_force() -> None:
    rng = random.Random(4501)
    for _ in range(500):
        m = rng.choice((1, 2, 4, 8))
        n = m + rng.randint(0, 20)
        d = rng.randint(1, m)
        size = m * rng.choice((1, 2))
        x = [rng.gauss(0, 1) for _ in range(n)]
        w = hann(m) if m > 1 and rng.random() < 0.5 else [1.0] * m
        got = welch(x, m, d, w, size)
        exp = brute_welch(x, m, d, w, size)
        scale = sum(v * v for v in x) + 1
        assert all(abs(a - b) <= 1e-11 * scale for a, b in zip(got, exp))


def test_one_segment_is_the_periodogram() -> None:
    rng = random.Random(4502)
    for _ in range(200):
        x = [rng.uniform(-1, 1) for _ in range(16)]
        p = [abs(v) ** 2 / 16 for v in fft(x)]
        assert all(abs(a - b) < 1e-12 for a, b in zip(welch(x, 16, 5), p))


def test_overlap_correlation_of_hann() -> None:
    w = hann(64)
    # the normalized overlap at 50 percent is 1/6, so rho_1 = 1/36; at 75 percent it is about 0.65
    assert abs(overlap_correlation(w, 32, 1) - 1 / 36) < 1e-12
    assert overlap_correlation(w, 32, 2) == 0
    assert overlap_correlation([1.0] * 8, 8, 1) == 0
    assert abs(variance_factor([1.0] * 8, 8, 5) - 1 / 5) < 1e-15


def _stats(vals):
    mean = sum(vals) / len(vals)
    return mean, sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)


def test_variance_shrinks_unlike_periodogram() -> None:
    # White Gaussian noise of variance 1, one record per seed 6000 to 6199, bin at w = pi/2.
    w = hann(64)
    results = {}
    for n in (256, 1024):
        vw, vb, vr = [], [], []
        for seed in range(6000, 6200):
            rng = random.Random(seed)
            x = [rng.gauss(0, 1) for _ in range(n)]
            vw.append(welch(x, 64, 32, w)[16])
            vb.append(bartlett(x, 64)[16])
            vr.append(abs(fft(x)[n // 4]) ** 2 / n)
        results[n] = (_stats(vw), _stats(vb), _stats(vr))
        (mw, varw), (mb, varb), (mr, varr) = results[n]
        assert abs(mw - 1) < 0.1 and abs(mb - 1) < 0.1
        assert 0.6 < varw / variance_factor(w, 32, segment_count(n, 64, 32)) < 1.4
        assert 0.6 < varb * segment_count(n, 64, 64) < 1.4
        assert 0.6 < varr < 1.6
    # Welch and Bartlett shrink about 4 times from N = 256 to N = 1024; the raw periodogram does not
    assert results[1024][0][1] < results[256][0][1] / 2.5
    assert results[1024][1][1] < results[256][1][1] / 2.5
    assert results[1024][2][1] > results[256][2][1] / 2.5
