# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cross-correlation/. The authors are listed in prov/ST8WA2.jsonl.

import random
from fractions import Fraction

import pytest

from cross_correlation import correlation_coefficient, cross_correlation, cross_correlation_fft, estimate_delay, fft


def brute(x, y, k):
    """The defining sum as a scan over every index pair (m, n) with m - n = k."""
    s = 0
    for m in range(len(x)):
        for j in range(len(y)):
            if m - j == k:
                yv = y[j].conjugate() if isinstance(y[j], complex) else y[j]
                s += x[m] * yv
    return s


def test_page_example() -> None:
    x = [0, 0, 1, 2, -1]
    y = [1, 2, -1]
    lags, r = cross_correlation(x, y)
    assert lags == [-2, -1, 0, 1, 2, 3, 4]
    assert r == [0, 0, -1, 0, 6, 0, -1]
    assert estimate_delay(x, y) == 2


def test_edges() -> None:
    assert cross_correlation([], [1]) == ([], [])
    assert cross_correlation([1], []) == ([], [])
    assert cross_correlation([3], [4]) == ([0], [12])
    assert cross_correlation_fft([], [1]) == ([], [])
    with pytest.raises(ValueError):
        estimate_delay([], [1])
    with pytest.raises(ValueError):
        correlation_coefficient([0, 0], [1])


def test_against_defining_sum_exact() -> None:
    rng = random.Random(4201)
    for _ in range(500):
        x = [Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(rng.randint(1, 10))]
        y = [Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(rng.randint(1, 10))]
        lags, r = cross_correlation(x, y)
        assert r == [brute(x, y, k) for k in lags]
        # every lag outside the range gives an empty sum
        assert brute(x, y, lags[0] - 1) == 0
        assert brute(x, y, lags[-1] + 1) == 0


def test_identities_exact() -> None:
    rng = random.Random(4202)
    for _ in range(500):
        x = [complex(rng.randint(-4, 4), rng.randint(-4, 4)) for _ in range(rng.randint(1, 8))]
        y = [complex(rng.randint(-4, 4), rng.randint(-4, 4)) for _ in range(rng.randint(1, 8))]
        lxy, rxy = cross_correlation(x, y)
        lyx, ryx = cross_correlation(y, x)
        table = dict(zip(lyx, ryx))
        # r_xy[-k] = conj(r_yx[k])
        for k, v in zip(lxy, rxy):
            assert v == table[-k].conjugate()
        # r_xy[k] is the convolution of x with the reversed conjugate of y, at index k + len(y) - 1
        rev = [v.conjugate() for v in reversed(y)]
        conv = [sum(x[i] * rev[t - i] for i in range(len(x)) if 0 <= t - i < len(rev)) for t in range(len(x) + len(y) - 1)]
        assert conv == rxy
        # Cauchy-Schwarz: |r_xy[k]|^2 <= r_xx[0] r_yy[0]
        ex = sum(abs(v) ** 2 for v in x)
        ey = sum(abs(v) ** 2 for v in y)
        for v in rxy:
            assert abs(v) ** 2 <= ex * ey + 1e-9


def test_fft_against_direct() -> None:
    rng = random.Random(4203)
    for _ in range(500):
        x = [rng.randint(-20, 20) for _ in range(rng.randint(1, 30))]
        y = [rng.randint(-20, 20) for _ in range(rng.randint(1, 30))]
        lags, exact = cross_correlation(x, y)
        lags2, fast = cross_correlation_fft(x, y)
        assert lags == lags2
        scale = (sum(v * v for v in x) * sum(v * v for v in y)) ** 0.5 + 1
        for a, b in zip(exact, fast):
            assert abs(a - b) <= 1e-12 * scale


def test_delay_recovery_in_noise() -> None:
    # y is a random +-1 pulse of length 32; x is y delayed by d plus Gaussian noise of sigma 0.5.
    rng = random.Random(4204)
    hits = 0
    trials = 500
    for _ in range(trials):
        y = [rng.choice((-1.0, 1.0)) for _ in range(32)]
        d = rng.randint(0, 40)
        x = [rng.gauss(0, 0.5) for _ in range(80)]
        for i, v in enumerate(y):
            x[i + d] += v
        hits += estimate_delay(x, y) == d
    assert hits == trials


def test_cyclic_wrap_without_padding() -> None:
    # With length-L DFTs and no padding, the lags k and k - L add up.
    x = [1, 2, 3, 4]
    y = [1, 0, 0, 5]
    size = 4
    raw = fft([a * b.conjugate() for a, b in zip(fft(x), fft(y))], inverse=True)
    lags, r = cross_correlation(x, y)
    table = dict(zip(lags, r))
    for k in range(size):
        folded = table.get(k, 0) + table.get(k - size, 0)
        assert abs(raw[k].real - folded) < 1e-12
    # the fold changes the answer here
    assert table[1] == 2 and table[-3] == 5
    assert round(raw[1].real) == 7


def test_correlation_coefficient_bound() -> None:
    rng = random.Random(4205)
    for _ in range(500):
        x = [rng.uniform(-1, 1) for _ in range(rng.randint(1, 12))]
        y = [rng.uniform(-1, 1) for _ in range(rng.randint(1, 12))]
        _, rho = correlation_coefficient(x, y)
        assert all(abs(v) <= 1 + 1e-12 for v in rho)
    _, rho = correlation_coefficient([1.0, 2.0, 3.0], [2.0, 4.0, 6.0])
    assert abs(rho[2] - 1) < 1e-12
