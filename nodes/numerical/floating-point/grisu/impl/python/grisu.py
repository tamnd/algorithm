# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grisu/. The authors are listed in prov/PHVDFD.jsonl.

"""Grisu3 (Loitsch, 2010): shortest float printing with 64-bit integers and a certified result.

All arithmetic in grisu3 stays below 2^64, as it would in C with uint64_t. When grisu3 cannot
prove that its digits are the shortest and nearest, it returns None, and `shortest` falls back
to an exact method with rationals.
"""

import math
import struct
from fractions import Fraction

ALPHA, GAMMA = -60, -32  # target range for the binary exponent of the scaled numbers
MASK64 = (1 << 64) - 1


def _cached_power(k: int) -> tuple[int, int]:
    """10^k as (f, e) with 2^63 <= f < 2^64, f = round(10^k / 2^e). Cost: O(1) big-integer operations."""
    v = Fraction(10) ** k
    e = (v.numerator.bit_length() - v.denominator.bit_length()) - 64
    while v / Fraction(2) ** e >= 1 << 64:
        e += 1
    while v / Fraction(2) ** e < 1 << 63:
        e -= 1
    f = math.floor(v / Fraction(2) ** e + Fraction(1, 2))
    if f == 1 << 64:
        f, e = 1 << 63, e + 1
    return f, e


# Loitsch's table: 10^k for k = -348, -340, ..., 340, each rounded to a 64-bit significand.
CACHED = [(k, *_cached_power(k)) for k in range(-348, 341, 8)]


def _times(a: int, b: int) -> int:
    """The upper 64 bits of the 128-bit product, rounded (half up). Cost: O(1)."""
    return (a * b + (1 << 63)) >> 64


def _normalize(f: int, e: int) -> tuple[int, int]:
    shift = 64 - f.bit_length()
    return f << shift, e - shift


def _round_weed(digits: list[int], dist_high_w: int, unsafe: int, rest: int, ten_kappa: int, unit: int) -> bool:
    """Move the last digit toward w and decide whether the result is certainly shortest and nearest."""
    small, big = dist_high_w - unit, dist_high_w + unit  # w lies strictly between too_high - big and too_high - small
    while (rest < small and unsafe - rest >= ten_kappa  # @line L8
           and (rest + ten_kappa < small or small - rest >= rest + ten_kappa - small)):
        digits[-1] -= 1
        rest += ten_kappa
    if (rest < big and unsafe - rest >= ten_kappa  # @line L9
            and (rest + ten_kappa < big or big - rest > rest + ten_kappa - big)):
        return False  # the nearest candidate depends on where w lies in its error interval
    return 2 * unit <= rest <= unsafe - 4 * unit  # the candidate is inside the safe interval


def grisu3(x: float) -> tuple[str, int] | None:
    """Shortest digits of x as (digits, exponent), value = int(digits) * 10^exponent, or None.

    Precondition: x finite and x > 0. When the result is not None it is the shortest decimal in
    the rounding interval of x and the nearest to x among those. Cost: O(1) operations on
    64-bit integers (at most 17 digit steps and one table lookup).
    """
    bits = struct.unpack(">Q", struct.pack(">d", x))[0]
    biased, frac = bits >> 52, bits & ((1 << 52) - 1)
    f, e = (frac, -1074) if biased == 0 else (frac | (1 << 52), biased - 1075)  # @line L1
    plus_f, plus_e = _normalize(2 * f + 1, e - 1)  # @line L2, x + g+, exactly
    if frac == 0 and biased > 1:
        minus_f, minus_e = 4 * f - 1, e - 2  # x - g-, where the lower gap is half as wide
    else:
        minus_f, minus_e = 2 * f - 1, e - 1
    minus_f <<= minus_e - plus_e
    w_f, w_e = _normalize(f, e)
    # @line L3: a cached power 10^K with ALPHA <= w_e + c_e + 64 <= GAMMA
    K, c_f, c_e = next(t for t in CACHED if ALPHA <= w_e + t[2] + 64 <= GAMMA)
    w = _times(w_f, c_f)  # @line L4, each within one unit of the exact scaled value
    high = _times(plus_f, c_f)
    low = _times(minus_f, c_f)
    e2 = w_e + c_e + 64  # the three products share this binary exponent; it is in [ALPHA, GAMMA]
    too_low, too_high = low - 1, high + 1  # @line L5, an interval that surely contains R(x)
    unsafe = too_high - too_low
    one_shift = -e2
    one = 1 << one_shift
    integrals, fractionals = too_high >> one_shift, too_high & (one - 1)
    kappa = len(str(integrals))
    divisor = 10 ** (kappa - 1)
    digits: list[int] = []
    while kappa > 0:  # @line L6, digits of the integer part of too_high
        digits.append(integrals // divisor)
        integrals %= divisor
        kappa -= 1
        rest = (integrals << one_shift) + fractionals
        if rest < unsafe:  # @line L7, the truncation lies above too_low
            ok = _round_weed(digits, too_high - w, unsafe, rest, divisor << one_shift, 1)
            return ("".join(map(str, digits)), kappa - K) if ok else None
        divisor //= 10
    unit = 1
    while True:  # digits of the fractional part
        fractionals *= 10
        unit *= 10
        unsafe *= 10
        digits.append(fractionals >> one_shift)
        fractionals &= one - 1
        kappa -= 1
        if fractionals < unsafe:
            ok = _round_weed(digits, (too_high - w) * unit, unsafe, fractionals, one, unit)
            return ("".join(map(str, digits)), kappa - K) if ok else None  # @line L10


def exact_shortest(x: float) -> tuple[str, int]:
    """The fallback: shortest and nearest digits by exact rational arithmetic. Cost: O(17) Fraction operations."""
    bits = struct.unpack(">Q", struct.pack(">d", x))[0]
    fx = Fraction(x)
    up = Fraction(math.nextafter(x, math.inf)) if bits != 0x7FEFFFFFFFFFFFFF else Fraction(2) ** 1024
    lo, hi = (fx + Fraction(math.nextafter(x, 0.0))) / 2, (fx + up) / 2
    closed = bits % 2 == 0

    def inside(y: Fraction) -> bool:
        return lo <= y <= hi if closed else lo < y < hi

    t = len(str(math.floor(hi))) if hi >= 1 else -len(str(math.floor(1 / hi)))
    while True:  # the coarsest power of ten with a multiple inside R
        u = Fraction(10) ** t
        c0 = math.floor(fx / u)
        cands = [c for c in (c0, c0 + 1) if c > 0 and inside(c * u)]
        if cands:
            best = min(cands, key=lambda c: (abs(c * u - fx), c % 2))
            s = str(best).rstrip("0")
            return s, t + len(str(best)) - len(s)
        t -= 1


def shortest(x: float) -> tuple[str, int]:
    """Grisu3 with the exact fallback, so always correct. Precondition: x finite, x > 0. Cost: O(1) usually."""
    r = grisu3(x)
    return r if r is not None else exact_shortest(x)


def to_string(x: float) -> str:
    """Format x in the style of Python's repr. Cost: as shortest."""
    if math.isnan(x):
        return "nan"
    if math.isinf(x):
        return "inf" if x > 0 else "-inf"
    if x == 0.0:
        return "-0.0" if math.copysign(1.0, x) < 0 else "0.0"
    sign = "-" if x < 0 else ""
    digits, exp10 = shortest(abs(x))
    n = len(digits)
    point = n + exp10  # value = 0.digits * 10^point
    if -4 < point <= 16:
        if point <= 0:
            return sign + "0." + "0" * -point + digits
        if point >= n:
            return sign + digits + "0" * (point - n) + ".0"
        return sign + digits[:point] + "." + digits[point:]
    exp = point - 1
    mant = digits[0] + ("." + digits[1:] if n > 1 else "")
    return f"{sign}{mant}e{'+' if exp >= 0 else '-'}{abs(exp):02d}"
