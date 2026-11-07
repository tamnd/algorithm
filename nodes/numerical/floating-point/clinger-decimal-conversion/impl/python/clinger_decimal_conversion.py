# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clinger-decimal-conversion/. The authors are listed in prov/FZCTBB.jsonl.

"""Clinger's correct decimal input (1990): a floating-point fast path and AlgorithmM with big integers."""

import math

P = 53  # precision of binary64
K_MIN = -1074  # exponent of the least significant bit of the smallest subnormal
K_MAX = 1024 - P  # exponent of the last bit of the largest finite number
FAST_EXP = 22  # 10^22 is the largest power of ten that is a binary64 number
POW10 = [10.0 ** i for i in range(FAST_EXP + 1)]  # exact: 5^22 < 2^53


def algorithm_m(u: int, v: int) -> float:
    """RN(u / v) in binary64, ties to even, for integers u >= 0 and v > 0, by exact integer division.

    Finds the scale k with 2^52 <= u / (v 2^k) < 2^53 (or k = K_MIN for subnormal
    results), divides, and rounds by the remainder. Returns math.inf on overflow.
    Cost: O(1) big-integer operations on integers of O(log u + log v) bits.
    """
    if u == 0:
        return 0.0
    k = u.bit_length() - v.bit_length() - P  # @line L5
    if _scaled(u, v, k) >= 1 << P:  # @line L6
        k += 1  # now 2^52 <= floor(u / (v 2^k)) < 2^53
    k = max(k, K_MIN)  # @line L7
    num, den = (u, v << k) if k >= 0 else (u << -k, v)
    q, r = divmod(num, den)  # @line L8
    if 2 * r > den or (2 * r == den and q & 1):  # @line L9
        q += 1
    if q == 1 << P:  # rounding carried into the next binade
        q, k = q >> 1, k + 1
    if k > K_MAX:  # @line L10
        return math.inf
    return math.ldexp(q, k)


def _scaled(u: int, v: int, k: int) -> int:
    """floor(u / (v 2^k)) for integers u >= 0, v > 0 and any integer k. Cost: one big-integer division."""
    return (u // (v << k)) if k >= 0 else ((u << -k) // v)


def clinger_read(f: int, e: int) -> float:
    """The binary64 number nearest to f * 10^e (ties to even), for integers f >= 0 and e.

    Uses the fast path when f < 2^53 and |e| <= 22, where both operands are exact
    binary64 numbers and one IEEE operation rounds correctly; otherwise AlgorithmM.
    Cost: O(1) for the fast path; O(1) big-integer operations on numbers of
    O(log f + |e|) bits otherwise.
    """
    if f < 0:
        raise ValueError("f must be nonnegative; apply the sign afterwards")
    if f == 0:  # @line L1
        return 0.0
    if f < 1 << P and -FAST_EXP <= e <= FAST_EXP:  # @line L2
        x = float(f)  # exact
        return x * POW10[e] if e >= 0 else x / POW10[-e]  # @line L3
    if e >= 0:  # @line L4
        return algorithm_m(f * 10 ** e, 1)
    return algorithm_m(f, 10 ** -e)


def parse_decimal(s: str) -> tuple[int, int, bool]:
    """Split a decimal string such as '-12.5e-3' into (f, e, negative) with value f * 10^e. Cost: O(len(s))."""
    s = s.strip().lower()
    negative = s.startswith("-")
    s = s.lstrip("+-")
    mantissa, _, exponent = s.partition("e")
    whole, _, frac = mantissa.partition(".")
    digits = (whole + frac) or "0"
    if not digits.isdigit():
        raise ValueError(f"not a decimal number: {s!r}")
    return int(digits), (int(exponent) if exponent else 0) - len(frac), negative


def read_float(s: str) -> float:
    """Correctly rounded conversion of a decimal string to binary64. Cost: as clinger_read."""
    f, e, negative = parse_decimal(s)
    x = clinger_read(f, e)
    return -x if negative else x
