# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ryu/. The authors are listed in prov/JH77DH.jsonl.

import math
import random
import struct
from decimal import Decimal
from fractions import Fraction

from ryu import BIAS, MANTISSA_BITS, decode, pow5_inv_split, pow5_split, pow5bits, ryu, ryu_str


def from_bits(b: int) -> float:
    return struct.unpack("<d", struct.pack("<Q", b))[0]


def reference(x: float) -> tuple[int, int]:
    """Shortest, then closest (ties to even digits), decimal in the rounding interval, in exact rationals."""
    v = Fraction(x)
    lo = (v + Fraction(math.nextafter(x, 0.0))) / 2
    hi = (v + Fraction(math.nextafter(x, math.inf))) / 2
    inclusive = decode(x)[1] % 2 == 0

    def inside(y: Fraction) -> bool:
        return lo <= y <= hi if inclusive else lo < y < hi

    k = len(str(int(hi))) + 1 if hi >= 1 else 1
    while True:
        unit = Fraction(10) ** k
        d0 = math.floor(v / unit)
        cands = [d for d in (d0 - 1, d0, d0 + 1, d0 + 2) if d > 0 and inside(d * unit)]
        if cands:
            best = min(cands, key=lambda d: (abs(d * unit - v), d % 2))
            while best % 10 == 0:
                best //= 10
                k += 1
            return best, k
        k -= 1


def from_repr(x: float) -> tuple[int, int]:
    t = Decimal(repr(x)).normalize().as_tuple()
    return int("".join(map(str, t.digits))), t.exponent


def test_examples():
    assert ryu(0.3) == (3, -1)
    assert ryu(1.0) == (1, 0)
    assert ryu(5e-324) == (5, -324)
    assert ryu(1.7976931348623157e308) == (17976931348623157, 292)
    assert ryu(2.0**-1017) == (7120236347223045, -322)
    assert ryu(1e23) == (1, 23)
    assert ryu(2.0**60) == (1152921504606847, 3)
    assert ryu_str(0.1) == "1e-1" and ryu_str(-2.5) == "-2.5e0" and ryu_str(-0.0) == "-0.0"


def test_against_exact_reference():
    rng = random.Random(2018)
    for _ in range(800):
        x = from_bits(rng.getrandbits(63))
        if math.isfinite(x) and x > 0:
            assert ryu(x) == reference(x), x


def test_round_trip_and_repr():
    rng = random.Random(1)
    for _ in range(25000):
        x = from_bits(rng.getrandbits(63))
        if not (math.isfinite(x) and x > 0):
            continue
        d, e = ryu(x)
        assert float(f"{d}e{e}") == x
        assert (d, e) == from_repr(x)


def test_edge_values():
    vals = [5e-324, 1e-323, 2.2250738585072014e-308, 2.225073858507201e-308, 1.0, 2.0, 0.5]
    vals += [2.0**k for k in range(-1074, 1024, 7)]
    vals += [math.nextafter(2.0**k, 0.0) for k in range(-1020, 1024, 11)]
    vals += [float(10**k) for k in range(0, 23)] + [10.0**-k for k in range(1, 30)]
    vals += [float(n) for n in range(1, 400)] + [9007199254740993.0, 2.0**53 + 2.0]
    for x in vals:
        assert ryu(x) == reference(x), x


def test_multiplier_floors_are_exact():
    # the 125-bit table entries give the exact floor of v * 2^e2 / 10^e10
    rng = random.Random(3)
    for _ in range(1500):
        x = from_bits(rng.getrandbits(63))
        if not (math.isfinite(x) and x > 0):
            continue
        _, m, e = decode(x)
        e2 = (1 if e == 0 else e) - BIAS - MANTISSA_BITS - 2
        mv = 4 * ((1 << MANTISSA_BITS) | m if e else m)
        if e2 >= 0:
            q = max(0, ((e2 * 78913) >> 18) - (e2 > 3))
            j = -e2 + q + 125 + pow5bits(q) - 1
            got, e10 = (mv * pow5_inv_split(q)) >> j, q
        else:
            q = max(0, ((-e2 * 732923) >> 20) - (-e2 > 1))
            i = -e2 - q
            j = q - (pow5bits(i) - 125)
            got, e10 = (mv * pow5_split(i)) >> j, q + e2
        assert got == math.floor(Fraction(mv) * Fraction(2) ** e2 / Fraction(10) ** e10)


def test_rejects_non_positive():
    for bad in (0.0, -1.0, math.inf, math.nan):
        try:
            ryu(bad)
        except ValueError:
            continue
        raise AssertionError(bad)
