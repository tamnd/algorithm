# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/veltkamp-splitting/. The authors are listed in prov/Z6SW6X.jsonl.

"""Veltkamp splitting of a binary64 float into a high part and a low part.

With s = 27 the high part has at most 26 significant bits and the low part
at most 26, so products of parts are exact in binary64 (Dekker's product).
"""

from fractions import Fraction

P = 53


def veltkamp_split(a: float, s: int = 27) -> tuple[float, float]:
    """Return (a_hi, a_lo) with a = a_hi + a_lo exactly.

    a_hi is a rounded to a multiple of 2^s ulp(a), so it has at most P - s
    significant bits; |a_lo| <= 2^(s-1) ulp(a). Valid for 1 <= s <= P - 1,
    finite a, and (2^s + 1) * a not overflowing. Cost: 1 multiplication and
    3 additions.
    """
    c = float((1 << s) + 1)  # @line L1
    gamma = c * a  # @line L2
    delta = a - gamma  # @line L3
    hi = gamma + delta  # @line L4
    lo = a - hi  # @line L5
    return hi, lo  # @line L6


def significant_bits(x: float) -> int:
    """The number of bits from the leading to the trailing one bit of |x| (0 for 0)."""
    if x == 0.0:
        return 0
    f = abs(Fraction(x))
    n, d = f.numerator, f.denominator
    # d is a power of two; strip trailing zero bits of n
    while n % 2 == 0:
        n //= 2
    return n.bit_length()


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


def veltkamp_split_emulated(a: Fraction, s: int, p: int, emin: int) -> tuple[Fraction, Fraction]:
    """Veltkamp splitting in a simulated binary format of precision p."""

    def rn(v: Fraction) -> Fraction:
        return round_to_precision(v, p, emin)

    gamma = rn((2**s + 1) * a)
    delta = rn(a - gamma)
    hi = rn(gamma + delta)
    return hi, rn(a - hi)
