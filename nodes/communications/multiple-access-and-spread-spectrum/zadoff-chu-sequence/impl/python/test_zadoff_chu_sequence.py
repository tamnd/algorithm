# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zadoff-chu-sequence/. The authors are listed in prov/MHXFB8.jsonl.

import cmath
import math

from zadoff_chu_sequence import corr_all, corr_exact_odd, periodic_corr, zadoff_chu, zc_exponents

TOL = 1e-9


def test_check_values_length_seven() -> None:
    x = zadoff_chu(1, 7)
    y = zadoff_chu(3, 7)
    auto = corr_all(x, x)
    assert abs(auto[0] - 7) < TOL
    assert all(abs(c) < TOL for c in auto[1:])
    assert all(abs(abs(c) - math.sqrt(7)) < TOL for c in corr_all(x, y))
    assert abs(math.sqrt(7) - 2.6458) < 5e-5


def test_exponent_form() -> None:
    assert zc_exponents(1, 7) == [0, 1, 3, 6, 3, 1, 0]
    x = zadoff_chu(1, 7)
    for k, m in enumerate(zc_exponents(1, 7)):
        assert abs(x[k] - cmath.exp(-2j * math.pi * m / 7)) < TOL


def test_constant_amplitude_and_periodic_extension() -> None:
    for n, u in ((7, 1), (13, 5), (63, 2), (8, 3), (64, 5)):
        x = zadoff_chu(u, n)
        assert all(abs(abs(v) - 1) < TOL for v in x)
        c = n % 2
        for k in range(n):
            nxt = cmath.exp(-1j * math.pi * u * (k + n) * (k + n + c) / n)
            assert abs(nxt - x[k]) < TOL


def test_zero_autocorrelation_for_coprime_roots() -> None:
    for n in (7, 13, 31, 63, 8, 16, 30):
        for u in range(1, n):
            if math.gcd(u, n) != 1:
                continue
            x = zadoff_chu(u, n)
            auto = corr_all(x, x)
            assert abs(auto[0] - n) < 1e-8
            assert all(abs(c) < 1e-8 for c in auto[1:])


def test_exact_zero_autocorrelation_in_integers() -> None:
    # For odd prime n, every shift t != 0 hits each n-th root of unity once,
    # and the sum of all n-th roots of unity is 0.
    for n in (7, 11, 13):
        for u in range(1, n):
            for t in range(1, n):
                _, counts = corr_exact_odd(u, u, n, t)
                assert counts == [1] * n


def test_cross_correlation_prime_length() -> None:
    for n in (7, 13, 31):
        for u1 in range(1, n):
            for u2 in (1, 2, n - 1):
                if u2 == u1:
                    continue
                vals = corr_all(zadoff_chu(u1, n), zadoff_chu(u2, n))
                assert all(abs(abs(c) - math.sqrt(n)) < 1e-8 for c in vals)


def test_cross_correlation_composite_length() -> None:
    a = zadoff_chu(1, 63)
    # u2 - u1 = 1 is coprime to 63: constant magnitude sqrt(63)
    assert all(abs(abs(c) - math.sqrt(63)) < 1e-8 for c in corr_all(a, zadoff_chu(2, 63)))
    # u2 - u1 = 3 shares the factor 3: magnitudes 0 and sqrt(3 * 63)
    mags = {round(abs(c), 6) for c in corr_all(a, zadoff_chu(4, 63))}
    assert mags == {0.0, round(math.sqrt(189), 6)}


def test_dft_has_constant_magnitude() -> None:
    for n, u in ((7, 1), (13, 4), (16, 3)):
        x = zadoff_chu(u, n)
        for k in range(n):
            xk = sum(x[m] * cmath.exp(-2j * math.pi * k * m / n) for m in range(n))
            assert abs(abs(xk) - math.sqrt(n)) < 1e-8


def test_frequency_offset_moves_the_peak() -> None:
    for n, u in ((7, 1), (7, 3), (13, 5), (31, 7)):
        x = zadoff_chu(u, n)
        y = [x[k] * cmath.exp(2j * math.pi * k / n) for k in range(n)]
        c = corr_all(y, x)
        peak = max(range(n), key=lambda t: abs(c[t]))
        assert peak == (-pow(u, -1, n)) % n
        assert abs(abs(c[peak]) - n) < 1e-8


def test_periodic_corr_definition() -> None:
    x = zadoff_chu(2, 11)
    y = zadoff_chu(3, 11)
    for t in range(11):
        direct = sum(x[k] * y[(k + t) % 11].conjugate() for k in range(11))
        assert abs(periodic_corr(x, y, t) - direct) < TOL
