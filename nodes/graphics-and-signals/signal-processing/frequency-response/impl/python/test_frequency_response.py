# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frequency-response/. The authors are listed in prov/7WHC1B.jsonl.

import cmath
import math
import random
from fractions import Fraction

from frequency_response import dtft, freq_response, group_delay, impulse_response, lfilter


def poly_mul(p, q):
    out = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, u in enumerate(p):
        for j, v in enumerate(q):
            out[i + j] += u * v
    return out


def random_stable_denominator(rng):
    """A(z) as a product of factors whose roots have modulus at most 9/10."""
    a = [Fraction(1)]
    for _ in range(rng.randint(1, 3)):
        if rng.random() < 0.5:
            r = Fraction(rng.randint(-9, 9), 10)
            a = poly_mul(a, [Fraction(1), -r])
        else:  # a complex pair r e^(+-i theta) with r^2 = s, 2 r cos(theta) = t
            s = Fraction(rng.randint(1, 81), 100)
            bound = 2 * math.sqrt(s)
            t = Fraction(rng.randint(-int(bound * 10), int(bound * 10)), 10)
            if t * t >= 4 * s:
                t = Fraction(0)
            a = poly_mul(a, [Fraction(1), -t, s])
    return a


def test_examples() -> None:
    third = [1 / 3, 1 / 3, 1 / 3]
    assert abs(freq_response(third, [1], 2 * math.pi / 3)) < 1e-15
    assert abs(freq_response(third, [1], 0) - 1) < 1e-15
    b, a = [1], [1, -0.5]
    assert abs(freq_response(b, a, 0) - 2) < 1e-15
    assert abs(freq_response(b, a, math.pi / 2) - (0.8 - 0.4j)) < 1e-15
    assert abs(freq_response(b, a, math.pi) - 2 / 3) < 1e-15


def test_fir_equals_direct_dtft() -> None:
    rng = random.Random(7501)
    for _ in range(100):
        h = [rng.uniform(-1, 1) for _ in range(rng.randint(1, 12))]
        for _ in range(10):
            w = rng.uniform(-math.pi, math.pi)
            assert abs(freq_response(h, [1], w) - dtft(h, w)) < 1e-12


def test_iir_equals_dtft_of_impulse_response() -> None:
    # the poles have modulus <= 0.9, so |h[n]| <= C n^2 0.9^n and 600 terms leave a tail far below 1e-9
    rng = random.Random(7502)
    for _ in range(30):
        a = random_stable_denominator(rng)
        b = [Fraction(rng.randint(-5, 5), rng.randint(1, 3)) for _ in range(rng.randint(1, 4))]
        h = impulse_response([float(v) for v in b], [float(v) for v in a], 600)
        for _ in range(8):
            w = rng.uniform(-math.pi, math.pi)
            assert abs(freq_response(b, a, w) - dtft(h, w)) < 1e-9


def test_partial_sums_converge_exactly_at_dc() -> None:
    # H(1) = sum(b) / sum(a), a rational number; the partial sums of h tend to it
    b = [Fraction(1), Fraction(2)]
    a = [Fraction(1), Fraction(-1, 2), Fraction(1, 4)]
    h = impulse_response(b, a, 120)
    target = sum(b) / sum(a)
    assert target == 4
    errs = [abs(sum(h[:k]) - target) for k in (20, 40, 80, 120)]
    assert errs[0] > errs[1] > errs[2] > errs[3]
    assert errs[3] < Fraction(1, 10**15)


def test_steady_state_sinusoid() -> None:
    b, a = [0.2, 0.3], [1, -0.6, 0.25]
    w0 = 0.7
    n = 400
    x = [math.cos(w0 * t) for t in range(n)]
    y = lfilter(b, a, x)
    g = freq_response(b, a, w0)
    for t in range(300, n):
        assert abs(y[t] - abs(g) * math.cos(w0 * t + cmath.phase(g))) < 1e-9


def test_group_delay() -> None:
    rng = random.Random(7503)
    # a symmetric FIR filter of length M has group delay (M - 1) / 2
    for m in range(2, 9):
        half = [rng.uniform(0.1, 1) for _ in range((m + 1) // 2)]
        h = half + half[::-1][m % 2:]
        for w in (0.1, 0.5, 1.0):
            if abs(freq_response(h, [1], w)) > 1e-3:
                assert abs(group_delay(h, [1], w) - (m - 1) / 2) < 1e-9
    # against a numerical derivative of the phase
    b, a = [1, 0.5], [1, -0.6, 0.25]
    for w in (0.2, 1.1, 2.5):
        e = 1e-6
        d = cmath.phase(freq_response(b, a, w + e) / freq_response(b, a, w - e))
        assert abs(group_delay(b, a, w) - (-d / (2 * e))) < 1e-5


def test_unstable_has_no_dtft() -> None:
    h = impulse_response([1], [1, -2], 40)
    assert h[:5] == [1, 2, 4, 8, 16]
    # the partial sums of the DTFT at w = 0 grow without bound, though B/A is finite there
    assert abs(sum(h)) > 1e11 and abs(freq_response([1], [1, -2], 0) - (-1)) < 1e-15
