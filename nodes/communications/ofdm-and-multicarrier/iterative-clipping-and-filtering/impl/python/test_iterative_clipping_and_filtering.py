# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-clipping-and-filtering/. The authors are listed in prov/CVZ52Y.jsonl.

import cmath
import math
import random

from iterative_clipping_and_filtering import (
    clip,
    clipped_energy,
    fft,
    in_band,
    iterative_clipping_and_filtering,
    to_bins,
    to_time,
)

QPSK = [complex(a, b) / math.sqrt(2) for a in (1, -1) for b in (1, -1)]


def block(rng, n=64):
    return [rng.choice(QPSK) for _ in range(n)]


def papr(x):
    p = [abs(v) ** 2 for v in x]
    return max(p) / (sum(p) / len(p))


def direct_time(X, L):
    """The oversampled symbol from its definition, x(t) at t = m / (L N) of a symbol."""
    n = len(X)
    freqs = list(range(n // 2)) + list(range(-(n // 2), 0))
    return [sum(X[i] * cmath.exp(2j * math.pi * f * m / (L * n)) for i, f in enumerate(freqs)) / math.sqrt(n) for m in range(L * n)]


def test_fft_and_the_oversampled_symbol():
    rng = random.Random(1)
    X = block(rng, 8)
    assert max(abs(a - b) for a, b in zip(to_time(X, 4), direct_time(X, 4))) < 1e-9
    assert max(abs(a - b) for a, b in zip(fft(fft(X), inverse=True), [8 * v for v in X])) < 1e-9
    assert max(abs(a - b) for a, b in zip(in_band(to_bins(to_time(X, 4), 4), 8), X)) < 1e-9


def test_output_is_band_limited():
    rng = random.Random(2)
    for _ in range(5):
        x, Xo, _ = iterative_clipping_and_filtering(block(rng), 4, 1.2, 3)
        bins = to_bins(x, 4)
        assert max(abs(v) for v in bins[32:256 - 32]) < 1e-12
        assert max(abs(a - b) for a, b in zip(to_time(Xo, 4), x)) < 1e-9


def test_clipped_off_energy_never_grows():
    rng = random.Random(3)
    for _ in range(10):
        X = block(rng)
        x = to_time(X, 4)
        a = 1.3 * math.sqrt(sum(abs(v) ** 2 for v in x) / len(x))
        _, _, e = iterative_clipping_and_filtering(X, 4, 1.3, 6)
        for k in range(6):
            assert abs(e[k] - clipped_energy(x, a)) < 1e-9
            c = clip(x, a)
            filt = to_time(in_band(to_bins(c, 4), 64), 4)
            removed = sum(abs(p - q) ** 2 for p, q in zip(c, filt))
            assert removed <= e[k] + 1e-12
            x = filt
            assert clipped_energy(x, a) <= removed + 1e-12
        assert all(e[k + 1] <= e[k] + 1e-12 for k in range(5))


def test_no_clipping_returns_the_input():
    rng = random.Random(4)
    X = block(rng)
    x, Xo, e = iterative_clipping_and_filtering(X, 4, 10.0, 3)
    assert e == [0.0, 0.0, 0.0]
    assert max(abs(a - b) for a, b in zip(Xo, X)) < 1e-9


def test_clip_is_the_nearest_point_of_the_disc():
    rng = random.Random(5)
    for _ in range(200):
        v = complex(rng.uniform(-3, 3), rng.uniform(-3, 3))
        c = clip([v], 1.0)[0]
        assert abs(c) <= 1.0 + 1e-15
        for _ in range(20):
            r, t = math.sqrt(rng.random()), rng.uniform(0, 2 * math.pi)
            assert abs(c - v) <= abs(r * cmath.exp(1j * t) - v) + 1e-12


def test_papr_drops():
    rng = random.Random(6)
    before, after = [], []
    for _ in range(40):
        X = block(rng)
        before.append(papr(to_time(X, 4)))
        after.append(papr(iterative_clipping_and_filtering(X, 4, 1.4, 4)[0]))
    assert 10 * math.log10(sum(before) / 40) > 6.5
    assert 10 * math.log10(sum(after) / 40) < 5.0
    assert 10 * math.log10(max(after)) < 6.0
