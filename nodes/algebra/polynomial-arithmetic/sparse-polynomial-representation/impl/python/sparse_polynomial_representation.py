# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-polynomial-representation/. The authors are listed in prov/3AC783.jsonl.
"""Sparse univariate polynomials as sorted lists of (exponent, coefficient) pairs.

A value is a list of pairs (e, c) with exponents strictly increasing and every
coefficient nonzero. The zero polynomial is the empty list. Coefficients may be
of any type with +, -, * and == 0 that models a commutative ring, for example
int, Fraction or a class for Z/pZ. Costs count ring operations on coefficients
and comparisons and additions of exponents, each at unit cost.
"""

from __future__ import annotations

from typing import Any, Sequence

Term = tuple[int, Any]
Sparse = list[Term]


def is_normalized(a: Sequence[Term]) -> bool:
    """True when the exponents are nonnegative, strictly increasing, and no coefficient is 0."""
    for k, (e, c) in enumerate(a):
        if e < 0 or c == 0:
            return False
        if k > 0 and a[k - 1][0] >= e:
            return False
    return True


def from_dense(coeffs: Sequence[Any]) -> Sparse:
    """The sparse form of a dense list, lowest degree first. Cost: n zero tests."""
    return [(i, c) for i, c in enumerate(coeffs) if c != 0]


def to_dense(a: Sequence[Term], zero: Any = 0) -> list[Any]:
    """The dense list of a sparse polynomial. Cost: deg + 1 writes."""
    if not a:
        return []
    out = [zero] * (a[-1][0] + 1)
    for e, c in a:
        out[e] = c
    return out


def degree(a: Sequence[Term]) -> int:
    """The degree, with -1 for the zero polynomial. Cost O(1)."""
    return a[-1][0] if a else -1


def add(a: Sequence[Term], b: Sequence[Term]) -> Sparse:
    """The sum of two normalized sparse polynomials, by merging.

    Precondition: a and b are normalized. Cost: at most s + t exponent
    comparisons and min(s, t) ring additions and zero tests, for s = len(a)
    and t = len(b).
    """
    i, j, c = 0, 0, []  # @line L1
    s, t = len(a), len(b)
    while i < s and j < t:  # @line L2
        if a[i][0] < b[j][0]:  # @line L3
            c.append(a[i])
            i += 1
        elif a[i][0] > b[j][0]:  # @line L4
            c.append(b[j])
            j += 1
        else:  # @line L5
            u = a[i][1] + b[j][1]  # @line L6
            if u != 0:  # @line L7
                c.append((a[i][0], u))
            i += 1  # @line L8
            j += 1
    c.extend(a[i:])  # @line L9
    c.extend(b[j:])
    return c  # @line L10


def neg(a: Sequence[Term]) -> Sparse:
    """The negative. Cost: len(a) negations."""
    return [(e, -c) for e, c in a]


def sub(a: Sequence[Term], b: Sequence[Term]) -> Sparse:
    """a - b for normalized a and b. Cost as for add."""
    return add(a, neg(b))


def scale(a: Sequence[Term], u: Any) -> Sparse:
    """u * a. Over a ring with zero divisors some terms can vanish. Cost: len(a) products."""
    out = []
    for e, c in a:
        v = u * c
        if v != 0:
            out.append((e, v))
    return out


def mul(a: Sequence[Term], b: Sequence[Term]) -> Sparse:
    """The product, by collecting the s t term products in a dictionary.

    Precondition: a and b are normalized. Cost: s t ring multiplications, at
    most s t ring additions, s t dictionary updates (expected O(1) each), and
    a sort of the k <= s t distinct exponents, O(k log k) comparisons.
    """
    acc: dict[int, Any] = {}
    for e, u in a:
        for d, v in b:
            k = e + d
            if k in acc:
                acc[k] = acc[k] + u * v
            else:
                acc[k] = u * v
    return [(k, acc[k]) for k in sorted(acc) if acc[k] != 0]


def _power(x: Any, g: int, one: Any) -> Any:
    """x^g by binary powering, a loop. Cost at most 2 floor(log2 g) products for g >= 1."""
    if g == 0:
        return one
    result = None
    base = x
    while True:
        if g & 1:
            result = base if result is None else result * base
        g >>= 1
        if g == 0:
            return result
        base = base * base


def evaluate(a: Sequence[Term], x: Any, one: Any = 1) -> Any:
    """The value a(x), by powering across the exponent gaps.

    Precondition: a is normalized. Cost: at most 2 sum(log2 g_i) + 2 t ring
    multiplications and t additions, where g_i are the gaps between exponents;
    O(t log n) for t terms and degree n.
    """
    y = one * 0
    p = one
    prev = 0
    for e, u in a:
        if e > prev:
            p = p * _power(x, e - prev, one)
        prev = e
        y = y + u * p
    return y


def derivative(a: Sequence[Term]) -> Sparse:
    """The formal derivative. Terms with e * c = 0 are dropped. Cost: len(a) products."""
    out = []
    for e, c in a:
        if e > 0:
            v = c * e
            if v != 0:
                out.append((e - 1, v))
    return out
