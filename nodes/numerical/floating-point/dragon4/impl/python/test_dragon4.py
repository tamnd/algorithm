# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dragon4/. The authors are listed in prov/17AMFE.jsonl.

"""Tests for Dragon4: shortest, nearest, round trip, checked with exact rationals and with repr."""

import math
import random
import struct
from fractions import Fraction

import pytest

from dragon4 import decompose, dragon4, to_string

MAX = 1.7976931348623157e308


def from_bits(b: int) -> float:
    return struct.unpack(">d", struct.pack(">Q", b))[0]


def interval(x: float) -> tuple[Fraction, Fraction, bool]:
    """The rounding interval of x > 0 under ties-to-even reading: (low, high, closed)."""
    m, _ = decompose(x)
    up = Fraction(math.nextafter(x, math.inf)) if x < MAX else Fraction(2) ** 1024
    down = Fraction(math.nextafter(x, 0.0))
    fx = Fraction(x)
    return (fx + down) / 2, (fx + up) / 2, m % 2 == 0


def inside(y: Fraction, lo: Fraction, hi: Fraction, closed: bool) -> bool:
    return lo <= y <= hi if closed else lo < y < hi


def check_shortest_and_nearest(x: float) -> None:
    digits, k = dragon4(x)
    n = len(digits)
    assert digits[0] != "0" and digits[-1] != "0"
    unit = Fraction(10) ** (k - n)
    y = int(digits) * unit
    lo, hi, closed = interval(x)
    assert inside(y, lo, hi, closed)
    fx = Fraction(x)
    # No number with n - 1 significant digits is inside: such numbers below 10^k are multiples
    # of 10 * unit, and it is enough to test the two that bracket x.
    coarse = unit * 10
    below = (fx // coarse) * coarse
    assert not (below > 0 and inside(below, lo, hi, closed))
    assert not inside(below + coarse, lo, hi, closed)
    # Nearest among the n-digit candidates, ties to an even last digit.
    for other in (y - unit, y + unit):
        if other > 0 and inside(other, lo, hi, closed):
            assert abs(other - fx) > abs(y - fx) or (abs(other - fx) == abs(y - fx) and int(digits) % 2 == 0)


def test_examples() -> None:
    assert dragon4(0.1) == ("1", 0)
    assert dragon4(0.3) == ("3", 0)
    assert dragon4(0.1 + 0.2) == ("30000000000000004", 0)
    assert dragon4(1e23) == ("1", 24)
    assert dragon4(2.0 ** 63) == ("9223372036854776", 19)
    assert dragon4(5e-324) == ("5", -323)
    assert dragon4(MAX) == ("17976931348623157", 309)
    assert dragon4(1.0) == ("1", 1)


def test_tie_between_two_shortest_candidates() -> None:
    # 2^50 + 1/4 lies exactly halfway between ...624.2 and ...624.3; the even digit wins.
    assert to_string(2.0 ** 50 + 0.25) == "1125899906842624.2"
    assert to_string(2.0 ** 50 + 0.75) == "1125899906842624.8"


def test_power_of_two_boundary() -> None:
    # Below a power of two the gap is half as wide; the interval is asymmetric.
    for e in (-1022, -1000, -1, 0, 1, 52, 53, 100, 1023):
        x = 2.0 ** e
        check_shortest_and_nearest(x)
        assert float(to_string(x)) == x


def test_extremes_and_specials() -> None:
    for x in (5e-324, 2.0 ** -1022, math.nextafter(2.0 ** -1022, 0.0), MAX, 1e-300, 1e300):
        check_shortest_and_nearest(x)
        assert to_string(x) == repr(x)
    assert to_string(0.0) == "0.0" and to_string(-0.0) == "-0.0"
    assert to_string(math.inf) == "inf" and to_string(-math.inf) == "-inf"
    assert to_string(math.nan) == "nan"
    with pytest.raises(ValueError):
        dragon4(0.0)


def test_random_bit_patterns_match_repr() -> None:
    rng = random.Random(1990)
    count = 0
    while count < 20000:
        x = from_bits(rng.getrandbits(64))
        if math.isnan(x) or math.isinf(x):
            continue
        assert to_string(x) == repr(x)
        count += 1


def test_small_subnormals() -> None:
    # Here the rounding interval is wide (up to a factor 3 between its ends), so it can
    # straddle a power of ten; compare with repr and also with every one-digit candidate.
    for m in range(1, 3000):
        x = m * 5e-324
        assert to_string(x) == repr(x)
        check_shortest_and_nearest(x)
        digits, k = dragon4(x)
        if len(digits) == 1:
            lo, hi, closed = interval(x)
            y, fx = int(digits) * Fraction(10) ** (k - 1), Fraction(x)
            for z in [d * Fraction(10) ** (k - 2) for d in range(1, 10)]:
                assert not inside(z, lo, hi, closed) or abs(z - fx) > abs(y - fx)


def test_random_shortest_nearest_exact() -> None:
    rng = random.Random(7)
    for _ in range(2000):
        x = from_bits(rng.getrandbits(63))
        if x == 0.0 or math.isinf(x) or math.isnan(x):
            continue
        check_shortest_and_nearest(x)


def test_short_decimals_print_back() -> None:
    # Two decimals with at most 15 digits are farther apart than the width of a rounding
    # interval of a normal binary64 number, so the shortest output is the decimal itself.
    rng = random.Random(3)
    for _ in range(3000):
        n = rng.randint(1, 15)
        f, e = rng.randrange(10 ** (n - 1), 10 ** n), rng.randint(-290, 290)
        digits, k = dragon4(float(f"{f}e{e}"))
        assert int(digits) * Fraction(10) ** (k - len(digits)) == f * Fraction(10) ** e
