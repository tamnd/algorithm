# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-product/. The authors are listed in prov/Q0TV83.jsonl.

"""Dekker's TwoProduct: x = fl(a*b) and the exact error y = a*b - x.

Exact in binary64 with round to nearest when no operation overflows and
e_a + e_b >= e_min + p - 1 = -970 (so the error is representable).
"""

import math
from fractions import Fraction

SPLITTER = 134217729.0  # 2^27 + 1 for binary64


def split(a: float) -> tuple[float, float]:
    """Veltkamp splitting: a = hi + lo with 26-bit parts."""
    gamma = SPLITTER * a
    delta = a - gamma
    hi = gamma + delta
    return hi, a - hi


def two_product(a: float, b: float) -> tuple[float, float]:
    """Dekker's product in 17 floating-point operations, no FMA needed."""
    x = a * b  # @line L1
    ah, al = split(a)  # @line L2
    bh, bl = split(b)  # @line L3
    t1 = ah * bh - x  # @line L4
    t2 = t1 + ah * bl  # @line L5
    t3 = t2 + al * bh  # @line L6
    y = t3 + al * bl  # @line L7
    return x, y  # @line L8


def _fma_fallback(a: float, b: float, c: float) -> float:
    """Correctly rounded a*b + c for finite inputs, via exact rationals."""
    return float(Fraction(a) * Fraction(b) + Fraction(c))


fma = getattr(math, "fma", _fma_fallback)


def two_product_fma(a: float, b: float) -> tuple[float, float]:
    """The FMA variant (2MultFMA): two operations."""
    x = a * b
    return x, fma(a, b, -x)


def round_to_precision(x: Fraction, p: int, emin: int) -> Fraction:
    """Round x to nearest, ties to even, in binary with precision p, subnormals below 2^emin."""
    if x == 0:
        return Fraction(0)
    sign = -1 if x < 0 else 1
    m = abs(x)
    e = m.numerator.bit_length() - m.denominator.bit_length()
    if Fraction(2) ** e > m:
        e -= 1
    e = max(e, emin)
    quantum = Fraction(2) ** (e - p + 1)
    q, r = divmod(m, quantum)
    q = int(q)
    if r > quantum / 2 or (r == quantum / 2 and q % 2 == 1):
        q += 1
    return sign * q * quantum


def two_product_emulated(a: Fraction, b: Fraction, p: int, emin: int) -> tuple[Fraction, Fraction]:
    """Dekker's product in a simulated binary format of precision p."""

    def rn(v: Fraction) -> Fraction:
        return round_to_precision(v, p, emin)

    c = 2 ** ((p + 1) // 2) + 1

    def sp(v: Fraction) -> tuple[Fraction, Fraction]:
        g = rn(c * v)
        h = rn(g + rn(v - g))
        return h, rn(v - h)

    x = rn(a * b)
    ah, al = sp(a)
    bh, bl = sp(b)
    t1 = rn(rn(ah * bh) - x)
    t2 = rn(t1 + rn(ah * bl))
    t3 = rn(t2 + rn(al * bh))
    return x, rn(t3 + rn(al * bl))
