# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grisu/. The authors are listed in prov/PHVDFD.jsonl.

"""Tests for Grisu3: certified results are shortest and nearest; failures are rare and caught."""

import math
import random
import struct
from fractions import Fraction

from grisu import CACHED, exact_shortest, grisu3, shortest, to_string

MAX = 1.7976931348623157e308


def from_bits(b: int) -> float:
    return struct.unpack(">d", struct.pack(">Q", b))[0]


def interval(x: float) -> tuple[Fraction, Fraction, bool]:
    up = Fraction(math.nextafter(x, math.inf)) if x < MAX else Fraction(2) ** 1024
    fx = Fraction(x)
    bits = struct.unpack(">Q", struct.pack(">d", x))[0]
    return (fx + Fraction(math.nextafter(x, 0.0))) / 2, (fx + up) / 2, bits % 2 == 0


def check(x: float, digits: str, exp10: int) -> None:
    """Exact check: inside R, no shorter number inside, nearest among equal-length multiples."""
    lo, hi, closed = interval(x)

    def inside(y: Fraction) -> bool:
        return lo <= y <= hi if closed else lo < y < hi

    u = Fraction(10) ** exp10
    y = int(digits) * u
    assert digits[0] != "0" and digits[-1] != "0" and inside(y)
    fx = Fraction(x)
    c = (fx // (10 * u)) * 10 * u
    assert not (c > 0 and inside(c)) and not inside(c + 10 * u)
    for z in (y - u, y + u):
        assert not inside(z) or abs(z - fx) > abs(y - fx) or (abs(z - fx) == abs(y - fx) and int(digits) % 2 == 0)


def test_cached_powers_are_rounded_and_cover_the_range() -> None:
    for k, f, e in CACHED:
        assert 1 << 63 <= f < 1 << 64
        assert abs(Fraction(f) - Fraction(10) ** k / Fraction(2) ** e) <= Fraction(1, 2)
    for a, b in zip(CACHED, CACHED[1:]):
        assert b[0] - a[0] == 8 and 0 < b[2] - a[2] < 28  # 28 = GAMMA - ALPHA


def test_examples() -> None:
    assert grisu3(0.1) == ("1", -1)
    assert grisu3(0.3) == ("3", -1)
    assert grisu3(5e-324) == ("5", -324)
    assert grisu3(MAX) == ("17976931348623157", 292)
    assert grisu3(2.0 ** 63) == ("9223372036854776", 3)


def test_known_failures_fall_back() -> None:
    # 1e23 is exactly the upper end of its rounding interval, and 2^50 + 1/4 is a tie between
    # two shortest strings; Grisu3 cannot decide either with 64-bit approximations.
    assert grisu3(1e23) is None and shortest(1e23) == ("1", 23)
    assert grisu3(2.0 ** 50 + 0.25) is None
    assert to_string(2.0 ** 50 + 0.25) == "1125899906842624.2"


def test_specials() -> None:
    assert to_string(0.0) == "0.0" and to_string(-0.0) == "-0.0"
    assert to_string(math.inf) == "inf" and to_string(math.nan) == "nan"
    assert to_string(-1.5) == "-1.5"
    for e in range(-1074, 1024, 7):
        assert to_string(2.0 ** e) == repr(2.0 ** e)


def test_random_patterns_certified_results_are_exact() -> None:
    rng = random.Random(2010)
    failures = total = 0
    for _ in range(30000):
        x = from_bits(rng.getrandbits(63))
        if x == 0.0 or not math.isfinite(x):
            continue
        total += 1
        r = grisu3(x)
        if r is None:
            failures += 1
            assert exact_shortest(x) == shortest(x)
            continue
        assert to_string(x) == repr(x)
        if total % 20 == 0:
            check(x, *r)
    assert failures / total < 0.01  # about 0.5% in Loitsch's measurements and here


def test_fallback_matches_repr() -> None:
    rng = random.Random(4)
    for _ in range(3000):
        x = from_bits(rng.getrandbits(63))
        if x == 0.0 or not math.isfinite(x):
            continue
        d, e = exact_shortest(x)
        assert float(f"{d}e{e}") == x
        check(x, d, e)
        assert to_string(x) == repr(x)


def test_small_subnormals() -> None:
    for m in range(1, 2000):
        x = m * 5e-324
        assert to_string(x) == repr(x)
