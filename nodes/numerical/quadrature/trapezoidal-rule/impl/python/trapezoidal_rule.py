# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trapezoidal-rule/. The authors are listed in prov/K7MAWR.jsonl.

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


def trapezoidal_rule(f: Callable[[Num], Num], a: Num, b: Num, m: int) -> Num:
    """Composite trapezoidal rule T_m(f) for the integral of f from a to b.

    Precondition: m >= 1 is the number of subintervals; f is defined at the
    m + 1 nodes a + i*h. If b < a the result is minus the rule on [b, a].
    With Fraction arguments and a Fraction-valued f the result is exact.
    Cost: exactly m + 1 evaluations of f and O(m) arithmetic operations.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    h = (b - a) / m  # @line L1
    s = (f(a) + f(b)) / 2  # @line L2
    inner = _sum(f(a + i * h) for i in range(1, m))  # @line L3 @line L4
    return h * (s + inner)  # @line L5
