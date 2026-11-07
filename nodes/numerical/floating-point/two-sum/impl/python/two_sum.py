# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-sum/. The authors are listed in prov/FP385Q.jsonl.

"""TwoSum (Moller 1965, Knuth): the exact error of a binary64 addition in six operations.

No condition on the order or the size of the operands is needed.
"""

from fractions import Fraction


def two_sum(a: float, b: float) -> tuple[float, float]:
    """Return (s, t) with s = fl(a + b) and s + t = a + b exactly.

    Exact for all finite a, b in binary64 with round to nearest, provided
    no operation overflows. Cost: 6 floating-point operations, no branch.
    """
    s = a + b  # @line L1
    a1 = s - b  # @line L2
    b1 = s - a1  # @line L3
    da = a - a1  # @line L4
    db = b - b1  # @line L5
    t = da + db  # @line L6
    return s, t  # @line L7


def round_to_precision(x: Fraction, p: int, emin: int) -> Fraction:
    """Round the rational x to nearest, ties to even, in binary with precision p.

    The format has subnormals below 2^emin and no overflow. This emulates a
    small floating-point system, for exhaustive checks of the algorithm.
    """
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
    half = quantum / 2
    if r > half or (r == half and q % 2 == 1):
        q += 1
    return sign * q * quantum


def two_sum_emulated(a: Fraction, b: Fraction, p: int, emin: int) -> tuple[Fraction, Fraction]:
    """TwoSum where every operation is rounded by round_to_precision."""

    def rn(v: Fraction) -> Fraction:
        return round_to_precision(v, p, emin)

    s = rn(a + b)
    a1 = rn(s - b)
    b1 = rn(s - a1)
    da = rn(a - a1)
    db = rn(b - b1)
    return s, rn(da + db)
