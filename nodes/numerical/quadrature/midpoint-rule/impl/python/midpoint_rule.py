# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/midpoint-rule/. The authors are listed in prov/YFXF32.jsonl.

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


def midpoint_rule(f: Callable[[Num], Num], a: Num, b: Num, m: int) -> Num:
    """Composite midpoint rule M_m(f) for the integral of f from a to b.

    Precondition: m >= 1 is the number of subintervals; f is defined at the
    m midpoints a + (i - 1/2) h, and need not be defined at a or b.
    If b < a the result is minus the rule on [b, a]. With Fraction
    arguments and a Fraction-valued f the result is exact.
    Cost: exactly m evaluations of f and O(m) arithmetic operations.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    h = (b - a) / m  # @line L1
    s = _sum(  # @line L2
        f(a + (2 * i - 1) * h / 2) for i in range(1, m + 1)  # @line L3 @line L4
    )
    return h * s  # @line L5
