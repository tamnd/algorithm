# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kraft-inequality/. The authors are listed in prov/AMFER4.jsonl.
"""The Kraft sum, and the construction of a D-ary prefix code from feasible lengths."""

from fractions import Fraction
from typing import Sequence

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def kraft_sum(lengths: Sequence[int], D: int = 2) -> Fraction:
    """sum D^(-l_i), exactly."""
    if D < 2:
        raise ValueError("D must be at least 2")
    if any(l < 0 for l in lengths):
        raise ValueError("a length is negative")
    return sum((Fraction(1, D ** l) for l in lengths), Fraction(0))


def satisfies_kraft(lengths: Sequence[int], D: int = 2) -> bool:
    return kraft_sum(lengths, D) <= 1


def to_digits(value: int, length: int, D: int) -> str:
    out = []
    for _ in range(length):
        value, d = divmod(value, D)
        out.append(DIGITS[d])
    if value:
        raise ValueError("value does not fit")
    return "".join(reversed(out))


def prefix_code_from_lengths(lengths: Sequence[int], D: int = 2) -> list[str]:
    """A D-ary prefix code with the given codeword lengths, or ValueError if the Kraft sum exceeds 1.

    Take the lengths in non-decreasing order. Codeword i is the first l_i digits of
    the D-ary expansion of S_i = sum over earlier j of D^(-l_j). The result is in
    the order of the input.
    """
    if D > len(DIGITS):
        raise ValueError("D is too large for the digit table")
    if not satisfies_kraft(lengths, D):
        raise ValueError("the lengths violate the Kraft inequality")
    order = sorted(range(len(lengths)), key=lambda i: lengths[i])
    code = [""] * len(lengths)
    S = Fraction(0)
    for i in order:
        l = lengths[i]
        v = S * D ** l  # an integer: every earlier length is at most l
        assert v.denominator == 1
        code[i] = to_digits(int(v), l, D)
        S += Fraction(1, D ** l)
    return code


def is_prefix_free(code: Sequence[str]) -> bool:
    """True when no codeword is a prefix of another (and no two are equal)."""
    words = sorted(code)
    return all(not words[i + 1].startswith(words[i]) for i in range(len(words) - 1))
