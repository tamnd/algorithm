# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bostan-mori-algorithm/. The authors are listed in prov/8WEKFW.jsonl.

"""The Bostan-Mori algorithm: the N-th coefficient of a rational power series.

A polynomial a_0 + a_1 x + ... + a_n x^n is the list [a_0, ..., a_n], lowest
degree first; the zero polynomial is []. Coefficients may be int, Fraction, or
any ring element type with + - * and unary minus (and `/` for the inverse of a
unit). The constant term of the denominator must be a unit.

One step multiplies the numerator and the denominator by Q(-x). The new
denominator Q(x) Q(-x) has only even powers, so it is W(x^2), and the
coefficient of x^N comes only from the even or only from the odd part of the
new numerator. N is halved, so there are about log2 N steps, each with two
polynomial products. All loops are iterative.
"""

from __future__ import annotations

from typing import Any, Callable, List, Sequence

Poly = List[Any]
MulFn = Callable[[Sequence[Any], Sequence[Any]], Poly]

KARATSUBA_CUTOFF = 32


def schoolbook_mul(a: Sequence[Any], b: Sequence[Any]) -> Poly:
    """Return the full product of two coefficient lists, len(a) + len(b) - 1 entries."""
    if not a or not b:
        return []
    c: Poly = [a[0] - a[0]] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] = c[i + j] + x * y
    return c


def _add(a: Sequence[Any], b: Sequence[Any]) -> Poly:
    """Return the coefficientwise sum of two lists of possibly different lengths."""
    if len(a) < len(b):
        a, b = b, a
    return [x + y for x, y in zip(a, b)] + list(a[len(b):])


def karatsuba_mul(a: Sequence[Any], b: Sequence[Any]) -> Poly:
    """Return the full product of two coefficient lists by Karatsuba's method.

    Works over every commutative ring. The recursion splits the longer operand
    in halves, so its depth is O(log(len(a) + len(b))).
    """
    if not a or not b:
        return []
    if len(a) < len(b):
        a, b = b, a
    if len(b) <= KARATSUBA_CUTOFF:
        return schoolbook_mul(a, b)
    zero = a[0] - a[0]
    h = len(a) // 2
    a0, a1 = list(a[:h]), list(a[h:])
    if len(b) <= h:
        # Unbalanced: b fits in the low half; multiply each half of a by b.
        lo = karatsuba_mul(a0, b)
        hi = karatsuba_mul(a1, b)
        c = [zero] * (len(a) + len(b) - 1)
        for i, v in enumerate(lo):
            c[i] = c[i] + v
        for i, v in enumerate(hi):
            c[i + h] = c[i + h] + v
        return c
    b0, b1 = list(b[:h]), list(b[h:])
    z0 = karatsuba_mul(a0, b0)
    z2 = karatsuba_mul(a1, b1)
    sa = _add(a0, a1)
    sb = _add(b0, b1)
    z1 = karatsuba_mul(sa, sb)
    for i, v in enumerate(z0):
        z1[i] = z1[i] - v
    for i, v in enumerate(z2):
        z1[i] = z1[i] - v
    c = [zero] * (len(a) + len(b) - 1)
    for i, v in enumerate(z0):
        c[i] = c[i] + v
    for i, v in enumerate(z1):
        if i + h < len(c):
            c[i + h] = c[i + h] + v
    for i, v in enumerate(z2):
        c[i + 2 * h] = c[i + 2 * h] + v
    return c


def _unit_inverse(c: Any) -> Any:
    """Return c^(-1), or raise ValueError if c is not a unit."""
    if isinstance(c, bool):
        raise TypeError("bool is not a ring element here")
    if isinstance(c, int):
        if c in (1, -1):
            return c
        raise ValueError("not a unit of Z")
    if c == 0:
        raise ValueError("zero is not a unit")
    one = c - c + 1
    try:
        return one / c
    except ZeroDivisionError as exc:
        raise ValueError("not a unit") from exc


def normalize(a: Sequence[Any]) -> Poly:
    """Return a copy of a without zero entries at the top."""
    out = list(a)
    while out and out[-1] == 0:
        out.pop()
    return out


def bostan_mori(p: Sequence[Any], q: Sequence[Any], n: int, mul: MulFn = karatsuba_mul, steps: list = None) -> Any:
    """Return the coefficient of x^n in the power series p / q.

    Precondition: q(0) is a unit. Any degrees are allowed. Cost: two products
    of polynomials with at most deg q + 1 coefficients per halving of n, once
    deg p < deg q.
    """
    p = normalize(p)
    q = normalize(q)
    if not q:
        raise ZeroDivisionError("the denominator is zero")
    zero = q[0] - q[0]
    if n < 0 or not p:
        return zero
    _unit_inverse(q[0])  # fail early if q(0) is not a unit
    while n >= 1:  # @line L1
        qm = [c if i % 2 == 0 else -c for i, c in enumerate(q)]  # @line L2
        u = mul(p, qm)  # @line L3
        v = mul(q, qm)  # @line L4
        p = u[n % 2 :: 2]  # @line L5
        q = v[0::2]  # @line L6
        n //= 2  # @line L7
        p = normalize(p)
        q = normalize(q)
        if steps is not None:
            steps.append((n, list(p), list(q)))
        if not p:
            return zero
    c0 = p[0] if p else zero  # @line L8
    return c0 * _unit_inverse(q[0])


def nth_term(c: Sequence[Any], a: Sequence[Any], n: int, mul: MulFn = karatsuba_mul) -> Any:
    """Return a_n for a_i = c_1 a_(i-1) + ... + c_d a_(i-d), given a_0, ..., a_(d-1).

    c = [c_1, ..., c_d] and a = [a_0, ..., a_(d-1)] must have the same length d.
    """
    d = len(c)
    if len(a) != d:
        raise ValueError("need exactly d initial values")
    if n < 0:
        raise ValueError("n must be nonnegative")
    if d == 0:
        return 0
    if n < d:
        return a[n]
    one = c[0] - c[0] + 1
    q = [one] + [-x for x in c]
    p = mul(list(a), q)[:d]
    return bostan_mori(p, q, n, mul)


def series_coefficient_naive(p: Sequence[Any], q: Sequence[Any], n: int) -> Any:
    """Reference: the first n + 1 coefficients of p / q by long division of series."""
    q = normalize(q)
    inv = _unit_inverse(q[0])
    zero = q[0] - q[0]
    s: Poly = []
    for i in range(n + 1):
        t = p[i] if i < len(p) else zero
        for j in range(1, min(i, len(q) - 1) + 1):
            t = t - q[j] * s[i - j]
        s.append(t * inv)
    return s[n]


if __name__ == "__main__":
    st = []
    print(bostan_mori([0, 1], [1, -1, -1], 10, steps=st))
    for row in st:
        print(row)
    print(nth_term([1, 1], [0, 1], 90))
