# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goldschmidt-division/. The authors are listed in prov/CRTBFS.jsonl.

"""Goldschmidt division of binary64 numbers in W-bit fixed point, with a final exact rounding step."""

import math

P = 53  # precision of binary64
W = 64  # fractional bits of the fixed-point datapath
TABLE_BITS = 7  # the seed table is indexed by the 7 leading fraction bits of the divisor
SEED_BITS = 10  # fractional bits of each table entry
ONE = 1 << W


def seed(big_b: int) -> int:
    """The table entry f0 ~ 1/B for a divisor B in [1, 2) given as an integer scaled by 2^W.

    Entry i is 1/(1 + (i + 1/2)/2^7) rounded to SEED_BITS fractional bits, so that
    |1 - B*f0| < 2^(-7). Returned scaled by 2^W. Cost: O(1).
    """
    i = (big_b - ONE) >> (W - TABLE_BITS)
    num = 1 << (SEED_BITS + TABLE_BITS + 1)  # 2^(SEED_BITS) * 2^(TABLE_BITS + 1)
    den = (1 << (TABLE_BITS + 1)) + 2 * i + 1  # 2^(TABLE_BITS + 1) * (1 + (i + 1/2)/2^7)
    f = (2 * num + den) // (2 * den)  # nearest integer to num/den
    return f << (W - SEED_BITS)


def split(x: float) -> tuple[int, int]:
    """For a positive normal float x, the integer M with x = M * 2^(e - 52), 2^52 <= M < 2^53, and e. Cost: O(1)."""
    m, e = math.frexp(x)  # x = m * 2^e with 1/2 <= m < 1
    return int(m * (1 << P)), e - 1


def goldschmidt_divide(a: float, b: float, iterations: int = 3, trace: list | None = None) -> float:
    """The correctly rounded (to nearest) binary64 quotient a / b by Goldschmidt's iteration.

    Precondition: a and b are finite, nonzero and normal, the quotient is a normal
    binary64 number (no underflow or overflow), and 3 <= iterations <= 64. The iteration runs
    in W-bit fixed point with truncation; after 3 iterations the approximation is within
    2^(-54) of A/B, and lines L8 and L9 fix the last bit with exact integer comparisons.
    With fewer iterations the result can be wrong. Cost: O(iterations) multiplications
    of (W+2)-bit integers, O(1) for fixed W.
    If trace is a list, the tuples (f, n, d) of each step are appended to it.
    """
    if not (math.isfinite(a) and math.isfinite(b)) or a == 0.0 or b == 0.0:
        raise ValueError("a and b must be finite and nonzero")
    sign = -1.0 if (a < 0.0) != (b < 0.0) else 1.0
    ma, ea = split(abs(a))  # @line L1
    mb, eb = split(abs(b))
    big_a = ma << (W - P + 1)  # A in [1, 2), scaled by 2^W
    big_b = mb << (W - P + 1)
    f = seed(big_b)  # @line L2
    n = (big_a * f) >> W  # @line L3
    d = (big_b * f) >> W
    if trace is not None:
        trace.append((f, n, d))
    for _ in range(iterations):  # @line L4
        f = 2 * ONE - d  # @line L5
        n, d = (n * f) >> W, (d * f) >> W  # @line L6
        if trace is not None:
            trace.append((f, n, d))
    # The quotient A/B lies in (1/2, 2); its unit in the last place is 2^(-52) or 2^(-53).
    shift = P - 1 if ma >= mb else P  # unit = 2^(-shift)
    q = (n + (1 << (W - shift - 1))) >> (W - shift)  # @line L7
    # Exact tests: A/B < (q - 1/2) * unit  <=>  2 * ma * 2^shift < (2q - 1) * mb.
    if 2 * ma * (1 << shift) < (2 * q - 1) * mb:  # @line L8
        q -= 1
    if 2 * ma * (1 << shift) > (2 * q + 1) * mb:  # @line L9
        q += 1
    return sign * math.ldexp(q, ea - eb - shift)  # @line L10
