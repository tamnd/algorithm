# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tone-reservation/. The authors are listed in prov/N335YA.jsonl.

import cmath
import math
import random

import pytest

from tone_reservation import fft, kernel, papr, to_bins, to_time, tone_reservation

QPSK = [complex(a, b) / math.sqrt(2) for a in (1, -1) for b in (1, -1)]
R8 = [10, 28, 30, 31, 34, 37, 39, 41]


def direct_time(X, L):
    n = len(X)
    freqs = list(range(n // 2)) + list(range(-(n // 2), 0))
    size = L * n
    return [sum(X[k] * cmath.exp(2j * math.pi * freqs[k] * t / size) for k in range(n)) * math.sqrt(L) / math.sqrt(size) for t in range(size)]


def block(rng, n, reserved):
    X = [rng.choice(QPSK) for _ in range(n)]
    for k in reserved:
        X[k] = 0j
    return X


def opt_one_tone(x, q1):
    """min over complex C of max_t |x[t] + C q1[t]|, a convex problem, by nested ternary search."""

    def f(a, b):
        c = complex(a, b)
        return max(abs(u + c * w) for u, w in zip(x, q1))

    def g(a):
        lo, hi = -3.0, 3.0
        for _ in range(70):
            m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
            if f(a, m1) < f(a, m2):
                hi = m2
            else:
                lo = m1
        return f(a, (lo + hi) / 2)

    lo, hi = -3.0, 3.0
    for _ in range(70):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if g(m1) < g(m2):
            hi = m2
        else:
            lo = m1
    return g((lo + hi) / 2)


def test_transforms():
    rng = random.Random(11)
    X = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(16)]
    x = to_time(X, 4)
    ref = direct_time(X, 4)
    assert max(abs(u - v) for u, v in zip(x, ref)) < 1e-9
    assert max(abs(u - v) for u, v in zip(to_bins(x, 4), X)) < 1e-9
    a = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(32)]
    back = [v / 32 for v in fft(fft(a), inverse=True)]
    assert max(abs(u - v) for u, v in zip(a, back)) < 1e-9


def test_kernel():
    p = kernel(64, R8, 4)
    assert abs(p[0] - 1) < 1e-12
    assert max(abs(v) for v in p) <= 1 + 1e-12
    P = to_bins(p, 4)
    assert max(abs(P[k]) for k in range(64) if k not in R8) < 1e-9
    # a circular shift of the kernel is a modulation: its spectrum stays on R
    m = 37
    shifted = [p[(t - m) % 256] for t in range(256)]
    S = to_bins(shifted, 4)
    assert max(abs(S[k]) for k in range(64) if k not in R8) < 1e-9


def test_data_untouched_and_spectrum_on_reserved_set():
    rng = random.Random(3)
    for _ in range(5):
        X = block(rng, 64, R8)
        a = math.sqrt(10 ** 0.5 * 56 / 64)
        y, C = tone_reservation(X, R8, 4, a, 20)
        Y = to_bins(y, 4)
        assert max(abs(Y[k] - X[k]) for k in range(64) if k not in R8) < 1e-9
        assert max(abs(C[k]) for k in range(64) if k not in R8) < 1e-9
        assert max(abs(Y[k] - C[k]) for k in R8) < 1e-9


def test_one_step_clips_the_peak_exactly():
    rng = random.Random(5)
    X = block(rng, 64, R8)
    x = to_time(X, 4)
    m = max(range(256), key=lambda t: abs(x[t]))
    a = 0.8 * abs(x[m])
    y, _ = tone_reservation(X, R8, 4, a, 1)
    assert abs(abs(y[m]) - a) < 1e-9
    assert abs(cmath.phase(y[m] / x[m])) < 1e-9


def test_stops_below_target():
    rng = random.Random(6)
    X = block(rng, 64, R8)
    x = to_time(X, 4)
    a = max(abs(v) for v in x) + 0.01
    y, C = tone_reservation(X, R8, 4, a, 50)
    assert y == x
    assert max(abs(v) for v in C) < 1e-12


def test_reaches_convex_optimum_with_one_tone():
    rng = random.Random(1)
    for _ in range(3):
        X = block(rng, 8, [3])
        x = to_time(X, 2)
        q1 = to_time([1 if k == 3 else 0 for k in range(8)], 2)
        opt = opt_one_tone(x, q1)
        y, _ = tone_reservation(X, [3], 2, opt, 200)
        peak = max(abs(v) for v in y)
        assert peak >= opt - 1e-6
        assert peak <= opt * (1 + 2e-3)


def test_papr_drops():
    rng = random.Random(2)
    before, after = [], []
    for _ in range(60):
        X = block(rng, 64, R8)
        a = math.sqrt(10 ** 0.5 * 56 / 64)
        y, _ = tone_reservation(X, R8, 4, a, 10)
        before.append(papr(to_time(X, 4)))
        after.append(papr(y))
    gain = 10 * math.log10(sum(before) / len(before)) - 10 * math.log10(sum(after) / len(after))
    assert gain > 1.5


def test_rejects_data_on_reserved_tones():
    X = [1 + 0j] * 16
    with pytest.raises(ValueError):
        tone_reservation(X, [2, 5], 4, 1.0, 5)
