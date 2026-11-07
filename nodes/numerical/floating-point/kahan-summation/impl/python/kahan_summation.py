# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kahan-summation/. The authors are listed in prov/7H2DE0.jsonl.

"""Kahan's compensated summation of binary64 floats (Kahan, 1965).

A correction c holds the negated low-order part that the last addition
lost; it is subtracted from the next term before that term is added.
"""

from collections.abc import Iterable


def kahan_sum(xs: Iterable[float]) -> float:
    """Compensated sum of xs. Cost: 4 floating-point operations per term, O(1) space."""
    s = 0.0  # @line L1
    c = 0.0  # @line L2
    for x in xs:  # @line L3
        y = x - c  # @line L4
        t = s + y  # @line L5
        c = (t - s) - y  # @line L6
        s = t  # @line L7
    return s  # @line L8


def kahan_steps(xs: Iterable[float]) -> list[tuple[float, float, float, float]]:
    """The values (y, t, c, s) after each iteration, for inspection and tests."""
    s = 0.0
    c = 0.0
    out = []
    for x in xs:
        y = x - c
        t = s + y
        c = (t - s) - y
        s = t
        out.append((y, t, c, s))
    return out


def kahan_sum_corrected(xs: Iterable[float]) -> float:
    """Kahan summation followed by one final correction, s - c."""
    s = 0.0
    c = 0.0
    for x in xs:
        y = x - c
        t = s + y
        c = (t - s) - y
        s = t
    return s - c
