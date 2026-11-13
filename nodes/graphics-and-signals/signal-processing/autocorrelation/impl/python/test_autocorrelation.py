# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/autocorrelation/. The authors are listed in prov/CHSTEW.jsonl.

import random
from fractions import Fraction

import pytest

from autocorrelation import autocorrelation, autocorrelation_fft, autocovariance, fft, toeplitz


def brute_pairs(x, k, scale):
    """The defining sum, written as a scan over all pairs (m, n) with m - n = k."""
    n = len(x)
    s = Fraction(0)
    for m in range(n):
        for j in range(n):
            if m - j == k:
                s += Fraction(x[m]) * Fraction(x[j])
    if scale == "biased":
        return s / n
    if scale == "unbiased":
        return s / (n - k)
    return s


def test_page_example() -> None:
    x = [3, -1, 2, 1, -2]
    assert autocorrelation(x, scale="none") == [19, -5, 1, 5, -6]
    assert autocorrelation([Fraction(v) for v in x]) == [Fraction(19, 5), -1, Fraction(1, 5), 1, Fraction(-6, 5)]
    assert autocorrelation([Fraction(v) for v in x], scale="unbiased") == [Fraction(19, 5), Fraction(-5, 4), Fraction(1, 3), Fraction(5, 2), -6]


def test_edges() -> None:
    assert autocorrelation([]) == []
    assert autocorrelation([Fraction(5)]) == [25]
    assert autocorrelation([0, 0, 0], scale="none") == [0, 0, 0]
    assert autocorrelation([Fraction(2)] * 4) == [4, 3, 2, 1]
    with pytest.raises(ValueError):
        autocorrelation([1, 2], max_lag=2)
    with pytest.raises(ValueError):
        autocorrelation([1, 2], scale="other")


def test_against_defining_sum_exact() -> None:
    rng = random.Random(4101)
    for _ in range(500):
        n = rng.randint(1, 12)
        x = [Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(n)]
        for scale in ("biased", "unbiased", "none"):
            r = autocorrelation(x, scale=scale)
            assert r == [brute_pairs(x, k, scale) for k in range(n)]


def test_fft_against_direct() -> None:
    rng = random.Random(4102)
    for _ in range(500):
        n = rng.randint(1, 40)
        x = [rng.randint(-20, 20) for _ in range(n)]
        exact = autocorrelation([Fraction(v) for v in x])
        fast = autocorrelation_fft(x)
        energy = sum(v * v for v in x) + 1
        for a, b in zip(exact, fast):
            assert abs(float(a) - b) <= 1e-12 * energy


def test_complex_hermitian_and_bound() -> None:
    rng = random.Random(4103)
    for _ in range(500):
        n = rng.randint(1, 15)
        x = [complex(rng.randint(-5, 5), rng.randint(-5, 5)) for _ in range(n)]
        r = autocorrelation(x, scale="none")
        fast = autocorrelation_fft(x, scale="none")
        for a, b in zip(r, fast):
            assert abs(a - b) <= 1e-9 * (abs(r[0]) + 1)
        # r[0] is real and bounds every lag
        assert r[0].imag == 0
        for v in r:
            assert abs(v) <= r[0].real + 1e-12
        # r[-k] = conj(r[k]): the lag -k sum computed directly
        for k in range(n):
            neg = sum(x[j - k] * x[j].conjugate() for j in range(k, n))
            assert neg == r[k].conjugate()


def test_biased_estimate_is_positive_semidefinite() -> None:
    # c^T R c = (1/N) * sum over n of (sum over k of c[k] x[n - k])^2, exactly.
    rng = random.Random(4104)
    for _ in range(500):
        n = rng.randint(1, 10)
        p = rng.randint(1, n)
        x = [Fraction(rng.randint(-6, 6)) for _ in range(n)]
        r = autocorrelation(x, max_lag=p - 1)
        big_r = toeplitz(r)
        c = [Fraction(rng.randint(-5, 5)) for _ in range(p)]
        quad = sum(c[i] * big_r[i][j] * c[j] for i in range(p) for j in range(p))
        conv = [sum(c[k] * x[t - k] for k in range(p) if 0 <= t - k < n) for t in range(n + p - 1)]
        assert quad == sum(v * v for v in conv) / n
        assert quad >= 0


def test_unbiased_estimate_can_fail() -> None:
    x = [Fraction(1), Fraction(0), Fraction(-1)]
    r = autocorrelation(x, scale="unbiased")
    assert r == [Fraction(2, 3), 0, -1]
    assert abs(r[2]) > r[0]
    big_r = toeplitz(r)
    c = [1, 0, 1]
    assert sum(c[i] * big_r[i][j] * c[j] for i in range(3) for j in range(3)) == Fraction(-2, 3)


def test_autocovariance_removes_mean() -> None:
    x = [Fraction(v) for v in (4, 6, 5, 7)]
    assert autocovariance(x, scale="none") == autocorrelation([v - Fraction(11, 2) for v in x], scale="none")
    assert autocovariance([Fraction(3)] * 5) == [0] * 5


def test_fft_roundtrip() -> None:
    rng = random.Random(4105)
    for size in (1, 2, 4, 8, 64):
        a = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(size)]
        back = fft(fft(a), inverse=True)
        assert all(abs(u - v) < 1e-12 for u, v in zip(a, back))
    with pytest.raises(ValueError):
        fft([1, 2, 3])
