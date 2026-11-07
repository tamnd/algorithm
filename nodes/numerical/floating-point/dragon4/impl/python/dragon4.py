# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dragon4/. The authors are listed in prov/17AMFE.jsonl.

"""Dragon4 free-format printing (Steele and White, 1990), in the formulation of Burger and Dybvig (1996).

Every quantity is an exact Python integer: no floating-point operation is used after the input
is decomposed, so the digits are the shortest that read back to x, and the nearest such digits.
"""

import math
import struct

P = 53  # precision of binary64
Q_MIN = -1074  # exponent of the least significant bit of a subnormal


def decompose(x: float) -> tuple[int, int]:
    """Return (m, q) with x = m * 2^q exactly, for finite x > 0, m < 2^53 and q >= -1074. Cost: O(1)."""
    bits = struct.unpack(">Q", struct.pack(">d", x))[0]
    biased, frac = (bits >> 52) & 0x7FF, bits & ((1 << 52) - 1)
    if biased == 0:
        return frac, Q_MIN
    return frac | (1 << 52), biased - 1075


def dragon4(x: float) -> tuple[str, int]:
    """Shortest decimal digits of x: returns (digits, k) with x printed as 0.digits * 10^k.

    Precondition: x is finite and x > 0. The digits are the fewest that lie in the rounding
    interval of x (so float() reads them back to x, ties to even), and among those the nearest
    to x, ties to an even last digit. Cost: O(n) big-integer operations on integers of
    O(1100) binary digits for binary64, where n <= 17 is the number of digits produced.
    """
    if not (math.isfinite(x) and x > 0):
        raise ValueError("dragon4 needs a finite positive float")
    m, q = decompose(x)  # @line L1
    inclusive = m % 2 == 0  # ties-to-even readers map the gap midpoints to x when m is even
    if q >= 0:  # @line L2
        if m != 1 << (P - 1):
            r, s, m_plus, m_minus = 2 * m << q, 2, 1 << q, 1 << q
        else:  # the gap below a power of two is half the gap above
            r, s, m_plus, m_minus = 4 * m << q, 4, 2 << q, 1 << q
    elif q == Q_MIN or m != 1 << (P - 1):
        r, s, m_plus, m_minus = 2 * m, 2 << -q, 1, 1
    else:
        r, s, m_plus, m_minus = 4 * m, 4 << -q, 2, 1
    # Now x = r/s, and the gaps to the midpoints with the neighbors are m_plus/s and m_minus/s.
    e2 = q + m.bit_length() - 1  # 2^e2 <= x < 2^(e2 + 1)
    k = (e2 * 30103) // 100000 - 1  # @line L3, k < log10(x), and k is at most 3 below the answer
    if k >= 0:
        s *= 10 ** k
    else:
        scale = 10 ** -k
        r, m_plus, m_minus = r * scale, m_plus * scale, m_minus * scale
    while r + m_plus > s or (inclusive and r + m_plus == s):  # @line L4
        s, k = s * 10, k + 1  # now every number in the rounding interval is below 10^k
    digits = []
    while True:
        r, m_plus, m_minus = r * 10, m_plus * 10, m_minus * 10  # @line L5
        d, r = divmod(r, s)  # @line L6
        low = r < m_minus or (inclusive and r == m_minus)  # @line L7
        high = r + m_plus > s or (inclusive and r + m_plus == s)
        if not low and not high:  # @line L8
            digits.append(d)
            continue
        if low and high:  # @line L9
            if 2 * r > s or (2 * r == s and d % 2 == 1):
                d += 1
        elif high:
            d += 1
        digits.append(d)
        return "".join(map(str, digits)), k  # @line L10


def to_string(x: float) -> str:
    """Format x in the style of Python's repr, using dragon4 for the digits. Cost: as dragon4."""
    if math.isnan(x):
        return "nan"
    if math.isinf(x):
        return "inf" if x > 0 else "-inf"
    if x == 0.0:
        return "-0.0" if math.copysign(1.0, x) < 0 else "0.0"
    sign = "-" if x < 0 else ""
    digits, k = dragon4(abs(x))
    n, point = len(digits), k  # value = 0.digits * 10^k
    if -4 < point <= 16:
        if point <= 0:
            return sign + "0." + "0" * -point + digits
        if point >= n:
            return sign + digits + "0" * (point - n) + ".0"
        return sign + digits[:point] + "." + digits[point:]
    exp = point - 1
    mant = digits[0] + ("." + digits[1:] if n > 1 else "")
    return f"{sign}{mant}e{'+' if exp >= 0 else '-'}{abs(exp):02d}"
