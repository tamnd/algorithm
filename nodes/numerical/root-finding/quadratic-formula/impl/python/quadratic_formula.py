# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadratic-formula/. The authors are listed in prov/CQ88BP.jsonl.

"""The quadratic formula in the form that avoids cancellation."""

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Tuple, Union

Number = Union[float, complex]


@dataclass
class QuadraticResult:
    """The two roots (with multiplicity) and their kind."""

    roots: Tuple[Number, ...]
    kind: str  # "real", "complex", "not quadratic" or "invalid"


def _discriminant(h: float, a: float, c: float) -> float:
    """h*h - a*c computed exactly and rounded once."""
    return float(Fraction(h) * Fraction(h) - Fraction(a) * Fraction(c))


def quadratic_roots(a: float, b: float, c: float) -> QuadraticResult:
    """Roots of a x^2 + b x + c with real float coefficients.

    Precondition: a, b, c finite floats; for full accuracy every nonzero
    coefficient should be at least 2^-1000 times the largest one, so that
    the scaling below does not make it subnormal. Real roots are returned
    in increasing order; complex roots as a conjugate pair, positive
    imaginary part first. Each computed root has relative error below
    about 3.5 u (u = 2^-53) with respect to the roots of the stored
    coefficients. Cost: a fixed number of operations and one square root.
    """
    if not (math.isfinite(a) and math.isfinite(b) and math.isfinite(c)):  # @line L1
        return QuadraticResult((), "invalid")
    if a == 0:
        return QuadraticResult((), "not quadratic")
    e = math.frexp(max(abs(a), abs(b), abs(c)))[1]  # @line L2
    a, b, c = math.ldexp(a, -e), math.ldexp(b, -e), math.ldexp(c, -e)
    h = b / 2  # @line L3
    d = _discriminant(h, a, c)
    if d < 0:  # @line L4
        re = -h / a  # @line L5
        im = math.sqrt(-d) / a
        return QuadraticResult((complex(re, abs(im)), complex(re, -abs(im))), "complex")  # @line L6
    s = math.sqrt(d)  # @line L7
    q = -(h + s) if h >= 0 else s - h
    if q == 0:  # @line L8
        return QuadraticResult((0.0, 0.0), "real")
    x1, x2 = q / a, c / q  # @line L9
    return QuadraticResult((min(x1, x2), max(x1, x2)), "real")


def quadratic_roots_naive(a: float, b: float, c: float) -> Tuple[Number, Number]:
    """The textbook formula (-b +- sqrt(b^2 - 4ac)) / (2a), for comparison only."""
    d = b * b - 4 * a * c
    if d < 0:
        s = complex(0.0, math.sqrt(-d))
    else:
        s = math.sqrt(d)
    return ((-b - s) / (2 * a), (-b + s) / (2 * a))
