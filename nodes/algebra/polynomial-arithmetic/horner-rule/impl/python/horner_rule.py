# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horner-rule/. The authors are listed in prov/947TVN.jsonl.

"""Horner's rule for evaluating a polynomial, with synthetic division and Taylor shift.

A polynomial a_0 + a_1 x + ... + a_n x^n is the list [a_0, ..., a_n], lowest
degree first, with a_n != 0 (the zero polynomial is []). The coefficients and
the point may be any objects with + and * (int, Fraction, float, Z/pZ, square
matrices for the point). Costs are counted in ring operations.
"""

from __future__ import annotations

from typing import Any, List, Sequence, Tuple


def horner(a: Sequence[Any], u: Any, zero: Any = 0) -> Any:
    """Return a(u) = a_0 + a_1 u + ... + a_n u^n.

    Precondition: a is normalized. Cost: n multiplications and n additions for
    n = len(a) - 1; the empty list gives `zero` with no operation.
    """
    if not a:  # @line L1
        return zero
    n = len(a) - 1
    s = a[n]  # @line L2
    for i in range(n - 1, -1, -1):  # @line L3
        s = s * u + a[i]  # @line L4
    return s  # @line L5


def synthetic_division(a: Sequence[Any], u: Any) -> Tuple[List[Any], Any]:
    """Return (q, r) with a = (x - u) q + r and r = a(u).

    Precondition: len(a) >= 1. Cost: n multiplications and n additions, the
    same as horner(a, u); q is the list of intermediate values of Horner's rule.
    """
    n = len(a) - 1
    if n == 0:
        return [], a[0]
    b: List[Any] = [None] * n
    b[n - 1] = a[n]  # @line S1
    for i in range(n - 1, 0, -1):  # @line S2
        b[i - 1] = b[i] * u + a[i]  # @line S3
    r = b[0] * u + a[0]  # @line S4
    return b, r  # @line S5


def taylor_shift(a: Sequence[Any], u: Any) -> List[Any]:
    """Return c with a(x) = sum c_k (x - u)^k, that is c_k = a^(k)(u) / k!.

    Equivalently, c is the coefficient list of a(x + u). Cost: n (n + 1) / 2
    multiplications and as many additions, by n rounds of synthetic division.
    """
    c = list(a)  # @line T1
    n = len(c) - 1
    for k in range(n):  # @line T2
        for i in range(n - 1, k - 1, -1):  # @line T3
            c[i] = c[i] + u * c[i + 1]  # @line T4
    return c  # @line T5


def horner_with_derivative(a: Sequence[Any], u: Any, zero: Any = 0) -> Tuple[Any, Any]:
    """Return (a(u), a'(u)) in one pass. Cost: 2n - 1 multiplications and additions."""
    if not a:
        return zero, zero
    n = len(a) - 1
    s, d = a[n], zero
    for i in range(n - 1, -1, -1):
        d = d * u + s
        s = s * u + a[i]
    return s, d
