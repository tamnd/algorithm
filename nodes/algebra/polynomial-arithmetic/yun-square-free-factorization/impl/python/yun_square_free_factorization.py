# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yun-square-free-factorization/. The authors are listed in prov/8QF8S3.jsonl.
"""Yun's square-free factorization over a field of characteristic 0 or p > deg f.

Polynomials are coefficient lists, lowest degree first; the zero polynomial
is []. Coefficients must form a field: Fraction, or a class for Z/pZ with
+, -, *, / and == 0. Integers are accepted and treated as rationals.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Sequence

Poly = list[Any]


def _strip(a: Poly) -> Poly:
    while a and a[-1] == 0:
        a.pop()
    return a


def _field(a: Sequence[Any]) -> Poly:
    return _strip([Fraction(c) if isinstance(c, int) else c for c in a])


def _derivative(a: Poly) -> Poly:
    return _strip([a[k] * k for k in range(1, len(a))])


def _sub(a: Poly, b: Poly) -> Poly:
    n = max(len(a), len(b))
    return _strip([(a[i] if i < len(a) else b[i] * 0) - (b[i] if i < len(b) else a[i] * 0)
                   for i in range(n)])


def _divmod(a: Poly, b: Poly) -> tuple[Poly, Poly]:
    """Schoolbook division over a field; b is not zero."""
    r = list(a)
    n = len(b) - 1
    if len(r) - 1 < n:
        return [], r
    inv = 1 / b[-1]
    q = [b[0] * 0] * (len(r) - n)
    for k in range(len(r) - 1 - n, -1, -1):
        t = r[k + n] * inv
        q[k] = t
        if t != 0:
            for j in range(n + 1):
                r[k + j] = r[k + j] - t * b[j]
    return _strip(q), _strip(r[:n])


def _exact_div(a: Poly, b: Poly) -> Poly:
    q, r = _divmod(a, b)
    if r:
        raise ArithmeticError("division is not exact")
    return q


def _monic(a: Poly) -> Poly:
    inv = 1 / a[-1]
    return [c * inv for c in a]


def _gcd(a: Poly, b: Poly) -> Poly:
    """The monic gcd by the Euclidean algorithm; gcd(0, 0) = 0."""
    while b:
        a, b = b, _divmod(a, b)[1]
    return _monic(a) if a else []


def _is_one(a: Poly) -> bool:
    return len(a) == 1


def yun(f: Sequence[Any]) -> tuple[Any, list[Poly]]:
    """Return (c, [a_1, ..., a_k]) with f = c a_1 a_2^2 ... a_k^k.

    Each a_i is monic and square-free, the a_i are pairwise coprime, and
    a_k is not 1; some a_i with i < k may be 1. A constant f gives (f, []).
    Precondition: the coefficients form a field of characteristic 0, or of
    characteristic p > deg f. Cost: O(n^2) field operations for degree n with
    the Euclidean algorithm used here, O(M(n) log n) with a fast gcd.
    """
    f = _field(f)
    if not f:
        raise ValueError("the zero polynomial has no square-free factorization")
    lc = f[-1]
    if len(f) == 1:
        return lc, []
    f = _monic(f)
    out: list[Poly] = []  # @line L1
    df = _derivative(f)
    b = _gcd(f, df)  # @line L2
    c = _exact_div(f, b)  # @line L3
    d = _sub(_exact_div(df, b), _derivative(c))
    while not _is_one(c):  # @line L4
        a = _gcd(c, d)  # @line L5
        out.append(a)  # @line L6
        c = _exact_div(c, a)  # @line L7
        d = _sub(_exact_div(d, a), _derivative(c))  # @line L8
    return lc, out  # @line L9
