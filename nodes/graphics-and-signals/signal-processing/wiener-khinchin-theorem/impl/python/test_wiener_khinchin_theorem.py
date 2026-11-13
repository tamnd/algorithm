# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wiener-khinchin-theorem/. The authors are listed in prov/QHCYJX.jsonl.

import cmath
import itertools
import math
import random
from fractions import Fraction

import pytest

from wiener_khinchin_theorem import (
    biased_autocorrelation,
    correlogram_at,
    dft,
    expected_periodogram,
    folded_autocorrelation,
    lags_from_periodogram,
    laurent_square,
    periodogram_at,
    periodogram_dft,
)


def test_page_example() -> None:
    # x = (2, 1, -1): r = (2, 1/3, -2/3); P(w) = 2 + (2/3) cos w - (4/3) cos 2w.
    x = [Fraction(2), Fraction(1), Fraction(-1)]
    assert biased_autocorrelation(x) == [2, Fraction(1, 3), Fraction(-2, 3)]
    for w, expect in ((0.0, 4 / 3), (math.pi / 2, 2 + 4 / 3), (math.pi, 0.0), (2 * math.pi / 3, 2 - 1 / 3 + 2 / 3)):
        assert abs(periodogram_at([float(v) for v in x], w) - expect) < 1e-12
        assert abs(correlogram_at([float(v) for v in biased_autocorrelation(x)], w) - expect) < 1e-12


def test_exact_laurent_identity() -> None:
    # X(z) X(1/z) / N has the coefficients r[k]; checked as polynomials and at rational z.
    rng = random.Random(4301)
    for _ in range(500):
        n = rng.randint(1, 9)
        x = [Fraction(rng.randint(-7, 7), rng.randint(1, 3)) for _ in range(n)]
        r = biased_autocorrelation(x)
        coeffs = laurent_square(x)
        assert coeffs == [r[-k] for k in range(-(n - 1), 0)] + r
        z = Fraction(rng.randint(1, 9), rng.randint(1, 9)) * rng.choice((-1, 1))
        left = sum(v * z ** (-k) for k, v in enumerate(x)) * sum(v * z ** k for k, v in enumerate(x)) / n
        right = r[0] + sum(r[k] * (z ** k + z ** (-k)) for k in range(1, n))
        assert left == right


def test_identity_at_any_frequency() -> None:
    rng = random.Random(4302)
    for _ in range(500):
        n = rng.randint(1, 24)
        x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        r = biased_autocorrelation(x)
        energy = sum(abs(v) ** 2 for v in x)
        for _ in range(3):
            w = rng.uniform(-math.pi, math.pi)
            assert abs(periodogram_at(x, w) - correlogram_at(r, w)) <= 1e-12 * energy


def test_dft_of_padded_autocorrelation() -> None:
    # P at w_m = 2 pi m / L equals the DFT of r folded onto L slots, for every L >= N.
    rng = random.Random(4303)
    for _ in range(500):
        n = rng.randint(1, 12)
        x = [rng.uniform(-1, 1) for _ in range(n)]
        energy = sum(v * v for v in x) + 1e-300
        for size in (n, 2 * n - 1, 2 * n + 3):
            lhs = periodogram_dft(x, size)
            rhs = dft(folded_autocorrelation(x, size))
            for a, b in zip(lhs, rhs):
                assert abs(a - b.real) <= 1e-12 * energy and abs(b.imag) <= 1e-12 * energy


def test_inverse_needs_two_n_minus_one() -> None:
    rng = random.Random(4304)
    for _ in range(300):
        n = rng.randint(2, 12)
        x = [rng.uniform(-1, 1) for _ in range(n)]
        r = biased_autocorrelation(x)
        back = lags_from_periodogram(x, 2 * n - 1)
        for k in range(n):
            assert abs(back[k] - r[k]) < 1e-12
            if k > 0:
                assert abs(back[2 * n - 1 - k] - r[k]) < 1e-12
        short = lags_from_periodogram(x, n)
        folded = folded_autocorrelation(x, n)
        assert all(abs(a - b) < 1e-12 for a, b in zip(short, folded))
    # one case where the fold changes lag 1: r[1] + r[1 - 3]
    x = [1.0, 2.0, 4.0]
    r = biased_autocorrelation(x)
    short = lags_from_periodogram(x, 3)
    assert abs(short[1].real - (r[1] + r[2])) < 1e-12 and abs(r[2]) > 0.5


def test_expected_biased_autocorrelation_exact_ma1() -> None:
    # x[n] = w[n] + b w[n - 1] with w = +-1 fair coins; enumerate all 2^(N+1) outcomes.
    b = Fraction(1, 2)
    n = 6
    true_r = {0: 1 + b * b, 1: b}
    total = [Fraction(0)] * n
    count = 0
    for w in itertools.product((-1, 1), repeat=n + 1):
        x = [Fraction(w[i + 1]) + b * w[i] for i in range(n)]
        for k, v in enumerate(biased_autocorrelation(x)):
            total[k] += v
        count += 1
    mean = [v / count for v in total]
    assert mean == [(1 - Fraction(k, n)) * true_r.get(k, 0) for k in range(n)]


def test_fejer_convergence_ar1() -> None:
    # AR(1) with a = 0.6 and unit noise: S(w) = 1 / |1 - a e^(-iw)|^2, r(k) = a^|k| / (1 - a^2).
    a = 0.6

    def r(k: int) -> float:
        return a ** abs(k) / (1 - a * a)

    grid = [math.pi * j / 200 for j in range(201)]
    errors = []
    for n in (8, 32, 128, 512):
        err = max(abs(expected_periodogram(r, n, w) - 1 / abs(1 - a * cmath.exp(-1j * w)) ** 2) for w in grid)
        errors.append(err)
    assert all(e1 > 3.5 * e2 for e1, e2 in zip(errors, errors[1:]))
    # the bias is about (1/N) sum of |k| |r(k)|, which is 2 a / ((1 - a)^2 (1 - a^2)) / N
    bound = 2 * a / ((1 - a) ** 2 * (1 - a * a))
    for n, e in zip((8, 32, 128, 512), errors):
        assert e <= bound / n + 1e-12


def test_tightness_line_spectrum() -> None:
    # A random-phase cosine has r(k) = cos(w0 k) / 2, not summable; E P_N(w0) grows like N / 4.
    w0 = 1.0

    def r(k: int) -> float:
        return math.cos(w0 * k) / 2

    values = [expected_periodogram(r, n, w0) for n in (16, 64, 256, 1024)]
    for n, v in zip((16, 64, 256, 1024), values):
        assert abs(v - n / 4) < 1.0
    assert expected_periodogram(r, 1024, 2.0) < 0.01


def test_errors() -> None:
    with pytest.raises(ValueError):
        periodogram_dft([1, 2, 3], 2)
