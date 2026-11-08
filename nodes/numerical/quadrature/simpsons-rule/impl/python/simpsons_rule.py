# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simpsons-rule/. The authors are listed in prov/CWAN1Z.jsonl.

import math
from fractions import Fraction
from typing import Callable, Iterable, TypeVar

Num = TypeVar("Num", float, Fraction)


def _sum(values: Iterable[Num]) -> Num:
    """Sum floats with math.fsum (one rounding), and Fractions exactly."""
    vals = list(values)
    if any(isinstance(v, Fraction) for v in vals) or not vals:
        return sum(vals)
    return math.fsum(vals)


def simpsons_rule(f: Callable[[Num], Num], a: Num, b: Num, m: int) -> Num:
    """Composite Simpson rule S_m(f) for the integral of f from a to b.

    Precondition: m >= 2 is even (the number of subintervals of width
    h = (b - a)/m); f is defined at the m + 1 nodes a + i*h.
    If b < a the result is minus the rule on [b, a]. With Fraction
    arguments and a Fraction-valued f the result is exact.
    Cost: exactly m + 1 evaluations of f and O(m) arithmetic operations.
    """
    if m < 2 or m % 2:
        raise ValueError("m must be even and at least 2")
    h = (b - a) / m  # @line L1
    ends = f(a) + f(b)  # @line L2
    terms = []
    for i in range(1, m):  # @line L3
        if i % 2 == 1:
            terms.append(4 * f(a + i * h))  # @line L4
        else:
            terms.append(2 * f(a + i * h))  # @line L5
    return h * (ends + _sum(terms)) / 3  # @line L6
