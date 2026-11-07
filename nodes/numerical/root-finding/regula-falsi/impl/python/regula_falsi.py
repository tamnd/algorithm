# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regula-falsi/. The authors are listed in prov/2GQVTS.jsonl.

"""Regula falsi: keep a sign-change bracket and cut it at the zero of the chord."""

import math
from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass
class RegulaFalsiResult:
    """The returned point, why the loop ended, the work done and the last bracket."""

    root: Any
    reason: str  # "root", "bracket", "converged", "no bracket", "failure", "kmax reached"
    iterations: int
    evaluations: int
    a: Any
    b: Any

    @property
    def converged(self) -> bool:
        return self.reason in ("root", "bracket", "converged")


def _finite(v: Any) -> bool:
    return math.isfinite(float(v))


def regula_falsi(
    f: Callable[[Any], Any],
    a: Any,
    b: Any,
    tol: Any = 0.0,
    max_iter: int = 10000,
) -> RegulaFalsiResult:
    """Find a zero of f in [a, b] by the method of false position.

    Precondition: a < b, f is real valued on [a, b], and tol >= 0. If
    f(a) and f(b) are finite with opposite signs, every bracket that the
    function keeps has the same property. Works with float, Fraction and
    Decimal; tol must have a type that compares with b - a.

    Stops when f is exactly zero at a point ("root"), when b - a <= 2 tol
    (returns the midpoint, error at most tol: "bracket"), when two
    successive points differ by at most tol ("converged", not certified),
    or after max_iter passes. Cost: 2 evaluations of f, plus 1 per pass.
    """
    fa = f(a)  # @line L1
    fb = f(b)
    n = 2
    if fa == 0:  # @line L2
        return RegulaFalsiResult(a, "root", 0, n, a, b)
    if fb == 0:
        return RegulaFalsiResult(b, "root", 0, n, a, b)
    if not (_finite(fa) and _finite(fb)) or (fa > 0) == (fb > 0):  # @line L3
        return RegulaFalsiResult(a, "no bracket", 0, n, a, b)
    c_prev: Optional[Any] = None  # @line L4
    c = a
    for k in range(1, max_iter + 1):  # @line L5
        c = b - fb * (b - a) / (fb - fa)  # @line L6
        if not (a < c < b):
            c = a + (b - a) / 2
        fc = f(c)  # @line L7
        n += 1
        if fc == 0:
            return RegulaFalsiResult(c, "root", k, n, a, b)
        if not _finite(fc):
            return RegulaFalsiResult(c, "failure", k, n, a, b)
        if (fc > 0) == (fa > 0):  # @line L8
            a, fa = c, fc
        else:
            b, fb = c, fc
        if b - a <= 2 * tol:  # @line L9
            return RegulaFalsiResult(a + (b - a) / 2, "bracket", k, n, a, b)
        if c_prev is not None and abs(c - c_prev) <= tol:  # @line L10
            return RegulaFalsiResult(c, "converged", k, n, a, b)
        c_prev = c  # @line L11
    return RegulaFalsiResult(c, "kmax reached", max_iter, n, a, b)  # @line L12
