# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asymmetric-numeral-systems/. The authors are listed in prov/4JH8SV.jsonl.

"""Uniform binary ANS (uABS) of Duda, in exact arithmetic.

The state is one natural number x. The probability of a 1 is a Fraction p
with 0 < p < 1. The states y with symbol 1 are the y where
ceil((y + 1) p) - ceil(y p) = 1, so they are spread as evenly as possible
with density p. C(s, x) is the x-th state (from 0) of symbol s, and D(y) is
the symbol of y and its rank among the states of that symbol. The coder has
no renormalization: x is a Python int that grows to about the information
content of the message, so this is the exact form of the method, not a
streaming coder. See rANS and tANS for the streaming forms.

Cost: O(n) state operations; each one works on an int of O(n) bits.
"""

import math
from fractions import Fraction


def _ceil(q: Fraction) -> int:
    return -((-q.numerator) // q.denominator)


def _floor(q: Fraction) -> int:
    return q.numerator // q.denominator


def check_probability(p: Fraction) -> Fraction:
    p = Fraction(p)
    if not 0 < p < 1:
        raise ValueError("p must lie strictly between 0 and 1")
    return p


def coding_function(s: int, x: int, p: Fraction) -> int:
    """C(s, x): the next state after coding the bit s from the state x."""
    if s == 1:
        return _floor(x / p)  # @line L1
    return _ceil((x + 1) / (1 - p)) - 1  # @line L2


def decoding_function(y: int, p: Fraction) -> tuple[int, int]:
    """D(y): the bit that the state y holds, and the state before it."""
    c = _ceil(y * p)
    s = _ceil((y + 1) * p) - c  # @line L3
    if s == 1:
        return 1, c  # @line L4
    return 0, y - c  # @line L5


def encode(bits: list[int], p: Fraction, x0: int = 1) -> int:
    """Encode bits so that decoding returns them in order: code them last first."""
    p = check_probability(p)
    x = x0  # @line L6
    for s in reversed(bits):  # @line L7
        x = coding_function(s, x, p)
    return x  # @line L8


def decode(x: int, n: int, p: Fraction, x0: int = 1) -> list[int]:
    p = check_probability(p)
    out = []
    for _ in range(n):  # @line L9
        s, x = decoding_function(x, p)
        out.append(s)
    if x != x0:  # @line L10
        raise ValueError("the final state is not the initial state")
    return out


def code_length(x: int) -> int:
    """The number of bits that write the final state in binary."""
    return x.bit_length()


def information(bits: list[int], p: Fraction) -> float:
    """The sum of lg(1/p_s) over the message: its ideal code length."""
    lg1, lg0 = -math.log2(p), -math.log2(1 - p)
    ones = sum(bits)
    return ones * lg1 + (len(bits) - ones) * lg0


def length_bound(bits: list[int], p: Fraction, x0: int = 1) -> float:
    """The bound of the proof on lg(X + 1) for the final state X."""
    q = 1 - p
    return math.log2(x0 + 1) + information(bits, p) + float(q / p) / ((x0 + 1) * math.log(2))
