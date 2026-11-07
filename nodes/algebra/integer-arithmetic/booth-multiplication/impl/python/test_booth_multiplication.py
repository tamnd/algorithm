# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/booth-multiplication/. The authors are listed in prov/B6TGDA.jsonl.

import random

import pytest

from booth_multiplication import (
    booth2_digits,
    booth4_digits,
    booth4_multiply,
    booth_multiply,
    to_signed,
    to_unsigned,
)


def test_example():
    # x = 3, y = -6 in 4 bits: y = 1010, digits (low first) 0, -1, +1, -1.
    assert booth2_digits(-6, 4) == [0, -1, 1, -1]
    assert booth_multiply(3, -6, 4) == (-18, 3)
    assert booth4_digits(-6, 4) == [-2, -1]
    assert booth4_multiply(3, -6, 4) == (-18, 2)


def test_run_of_ones():
    # 0111 1110 has one run of ones: two operations instead of six.
    assert booth_multiply(5, 0b01111110, 8) == (5 * 126, 2)


def test_digit_values():
    for n in range(1, 9):
        for y in range(-(1 << (n - 1)), 1 << (n - 1)):
            d2 = booth2_digits(y, n)
            assert sum(d << i for i, d in enumerate(d2)) == y
            d4 = booth4_digits(y, n)
            assert all(-2 <= d <= 2 for d in d4)
            assert len(d4) == (n + 1) // 2
            assert sum(d * 4**j for j, d in enumerate(d4)) == y
            # nonzero radix-2 digits alternate in sign
            nz = [d for d in d2 if d]
            assert all(nz[i] == -nz[i + 1] for i in range(len(nz) - 1))


def test_exhaustive_small():
    for n in range(1, 7):
        r = range(-(1 << (n - 1)), 1 << (n - 1))
        for x in r:
            for y in r:
                p, ops = booth_multiply(x, y, n)
                assert p == x * y
                assert ops == sum(1 for d in booth2_digits(y, n) if d)
                p4, nz = booth4_multiply(x, y, n)
                assert p4 == x * y
                assert nz <= (n + 1) // 2


def test_random():
    rng = random.Random(4242)
    for _ in range(800):
        n = rng.randint(1, 64)
        lo, hi = -(1 << (n - 1)), (1 << (n - 1)) - 1
        x, y = rng.randint(lo, hi), rng.randint(lo, hi)
        assert booth_multiply(x, y, n)[0] == x * y
        assert booth4_multiply(x, y, n)[0] == x * y


def test_worst_cases():
    for n in (2, 4, 8, 16, 33):
        lo, hi = -(1 << (n - 1)), (1 << (n - 1)) - 1
        for x, y in ((lo, lo), (lo, hi), (hi, hi), (lo, -1), (-1, -1), (0, lo)):
            assert booth_multiply(x, y, n)[0] == x * y
            assert booth4_multiply(x, y, n)[0] == x * y
        # alternating bits ...0101 give n operations in radix 2
        alt = to_signed(int("01" * n, 2) & ((1 << n) - 1), n)
        assert booth_multiply(1, alt, n)[1] == n


def test_conversions_and_errors():
    assert to_signed(to_unsigned(-5, 8), 8) == -5
    with pytest.raises(ValueError):
        booth_multiply(8, 1, 4)
    with pytest.raises(ValueError):
        booth4_multiply(1, 1, 0)
