# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/granlund-montgomery-division/. The authors are listed in prov/N5CE12.jsonl.

"""Division by an invariant integer with a precomputed multiplier.

Words have w bits and beta = 2^w. Every operation below is one that a w-bit
machine provides: the high word of a w x w product, addition and subtraction
modulo beta, shifts and comparisons. Python ints model the words and every
intermediate result is checked to fit in one word.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Divisor:
    """The precomputed data for dividing w-bit words by d."""

    d: int
    w: int
    m: int
    s1: int
    s2: int


def _word(x: int, w: int) -> int:
    if not 0 <= x < (1 << w):
        raise AssertionError("intermediate value does not fit in a word")
    return x


def precompute(d: int, w: int) -> Divisor:
    """Granlund-Montgomery data for 1 <= d < 2^w (their Figure 4.1)."""
    if w < 1 or not 1 <= d < (1 << w):
        raise ValueError("need 1 <= d < 2^w")
    ell = (d - 1).bit_length()  # @line L1
    m = ((1 << w) * ((1 << ell) - d)) // d + 1  # @line L2
    s1, s2 = min(ell, 1), max(ell - 1, 0)  # @line L3
    return Divisor(d, w, _word(m, w), s1, s2)


def divide(n: int, dv: Divisor) -> tuple[int, int]:
    """Return (n // d, n % d) for 0 <= n < 2^w with one multiply-high."""
    w = dv.w
    _word(n, w)
    t = (dv.m * n) >> w  # @line L4
    if t > n:
        raise AssertionError("t must not exceed n")
    q = _word(t + ((n - t) >> dv.s1), w) >> dv.s2  # @line L5
    return q, _word(n - q * dv.d, w)  # @line L6


def reciprocal(d: int, w: int) -> int:
    """The Moller-Granlund reciprocal v = floor((beta^2 - 1) / d) - beta.

    Precondition: d is normalized, 2^(w-1) <= d < 2^w.
    """
    if w < 1 or not (1 << (w - 1)) <= d < (1 << w):
        raise ValueError("d must be normalized")
    return _word(((1 << (2 * w)) - 1) // d - (1 << w), w)


def div_2by1(u1: int, u0: int, d: int, v: int, w: int) -> tuple[int, int]:
    """Divide the two-word number (u1, u0) by a normalized d with u1 < d.

    Moller and Granlund, Algorithm 4: one full product, one low product,
    and at most two corrections. Returns (q, r) with u1 beta + u0 = q d + r.
    """
    beta = 1 << w
    mask = beta - 1
    if not (0 <= u1 < d and 0 <= u0 < beta):
        raise ValueError("need u1 < d and u0 < beta")
    prod = v * u1 + (u1 << w) + u0  # @line L7
    q1, q0 = prod >> w, prod & mask
    _word(q1, w)
    q1 = (q1 + 1) & mask  # @line L8
    r = (u0 - q1 * d) & mask
    if r > q0:  # @line L9
        q1 = (q1 - 1) & mask
        r = (r + d) & mask
    if r >= d:  # @line L10
        q1 += 1
        r -= d
    return q1, r  # @line L11
