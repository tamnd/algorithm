# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clinger-decimal-conversion/. The authors are listed in prov/FZCTBB.jsonl.

"""Tests for Clinger's decimal input: compare with an exact rational oracle and with float()."""

import math
import random
import struct
from fractions import Fraction

from clinger_decimal_conversion import algorithm_m, clinger_read, parse_decimal, read_float

MAX = struct.unpack(">d", bytes.fromhex("7fefffffffffffff"))[0]


def oracle(f: int, e: int) -> float:
    """RN(f * 10^e) through Fraction; CPython's int true division is correctly rounded."""
    q = Fraction(f) * Fraction(10) ** e
    try:
        return q.numerator / q.denominator
    except OverflowError:
        return math.inf


def test_examples() -> None:
    cases = {
        "0.1": "0x1.999999999999ap-4",
        "3.14159": "0x1.921f9f01b866ep+1",
        "1e23": "0x1.52d02c7e14af6p+76",
        "123456789012345678901234567890": "0x1.8ee90ff6c373ep+96",
        "8.98846567431158e307": "0x1.0000000000000p+1023",
    }
    for s, h in cases.items():
        assert read_float(s) == float.fromhex(h)


def test_ties_to_even() -> None:
    assert read_float("9007199254740993") == 2.0 ** 53  # 2^53 + 1, a tie, goes down to even
    assert read_float("9007199254740995") == 2.0 ** 53 + 4  # 2^53 + 3, a tie, goes up to even
    assert read_float("9007199254740993.0000000000000001") == 2.0 ** 53 + 2  # just above the tie


def test_extremes() -> None:
    assert read_float("1.7976931348623157e308") == MAX
    assert read_float("1.7976931348623158e308") == MAX
    assert read_float("1.7976931348623159e308") == math.inf
    assert read_float("1e400") == math.inf
    assert read_float("2.2250738585072014e-308") == 2.0 ** -1022
    assert read_float("2.2250738585072011e-308") == math.nextafter(2.0 ** -1022, 0.0)
    assert read_float("4.9406564584124654e-324") == 2.0 ** -1074
    assert read_float("2.4703282292062327e-324") == 0.0  # below half the smallest subnormal
    assert read_float("2.4703282292062328e-324") == 2.0 ** -1074  # above it
    assert read_float("1e-400") == 0.0


def test_zero_and_sign() -> None:
    assert read_float("0") == 0.0
    assert math.copysign(1.0, read_float("-0.0")) == -1.0
    assert read_float("-2.5") == -2.5
    assert read_float("+1e2") == 100.0


def test_parse() -> None:
    assert parse_decimal("12.50e-3") == (1250, -5, False)
    assert parse_decimal("-7") == (7, 0, True)
    assert parse_decimal(".5") == (5, -1, False)


def test_fast_path_matches_algorithm_m() -> None:
    rng = random.Random(1)
    for _ in range(3000):
        f = rng.randrange(1, 1 << 53)
        e = rng.randint(-22, 22)
        x = clinger_read(f, e)
        slow = algorithm_m(f * 10 ** e, 1) if e >= 0 else algorithm_m(f, 10 ** -e)
        assert x == slow == oracle(f, e)


def test_naive_fast_path_beyond_22_is_wrong() -> None:
    # Multiplying by an inexact power of ten rounds twice.
    assert 3.0 * 1e23 != oracle(3, 23)  # 1e23 is already rounded
    assert clinger_read(3, 23) == oracle(3, 23) == 3e23


def test_random_against_oracle_and_float() -> None:
    rng = random.Random(20240612)
    for _ in range(4000):
        digits = rng.randint(1, 40)
        f = rng.randrange(10 ** (digits - 1), 10 ** digits)
        e = rng.randint(-360, 300)
        x = clinger_read(f, e)
        assert x == oracle(f, e)
        assert x == float(f"{f}e{e}")


def test_halfway_cases_from_floats() -> None:
    # Exact decimal expansions of midpoints between neighbors, and values just off them.
    rng = random.Random(5)
    for _ in range(400):
        bits = rng.getrandbits(63)
        x = struct.unpack(">d", struct.pack(">Q", bits))[0]
        if not math.isfinite(x) or x == 0.0 or x == MAX:
            continue
        y = math.nextafter(x, math.inf)
        mid = (Fraction(x) + Fraction(y)) / 2
        den = mid.denominator  # a power of two, so mid has a finite decimal expansion
        k = den.bit_length() - 1
        f, e = mid.numerator * 5 ** k, -k
        expected = x if struct.unpack(">Q", struct.pack(">d", x))[0] % 2 == 0 else y
        assert clinger_read(f, e) == expected
        assert clinger_read(f * 10 + 1, e - 1) == y
        assert clinger_read(f * 10 - 1, e - 1) == x
