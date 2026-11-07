# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dense-polynomial-representation/. The authors are listed in prov/YEET6X.jsonl.

"""Dense univariate polynomials as coefficient lists, lowest degree first.

A polynomial a_0 + a_1 x + ... + a_(n-1) x^(n-1) is the list [a_0, ..., a_(n-1)].
Invariant (N): the list is empty (the zero polynomial) or its last entry is
nonzero. The coefficients may be any objects with +, -, * and a test "== 0":
int, fractions.Fraction, or a class for Z/pZ. Costs are counted in ring
operations on the coefficients.
"""

from __future__ import annotations

from typing import Any, List, Sequence, Tuple

Poly = List[Any]


def normalize(c: Poly) -> Poly:
    """Remove zero entries at the top of c, in place, and return c.

    Cost: O(k) zero tests, where k is the number of entries removed.
    """
    while c and c[-1] == 0:  # @line L1
        c.pop()  # @line L2
    return c  # @line L3


def degree(a: Sequence[Any]) -> int:
    """The degree of a normalized polynomial; -1 stands for the zero polynomial."""
    return len(a) - 1


def add(a: Sequence[Any], b: Sequence[Any]) -> Poly:
    """The sum a + b of two normalized polynomials, normalized.

    Cost: max(m, n) ring additions for m = len(a), n = len(b).
    """
    m, n = len(a), len(b)
    c: Poly = [0] * max(m, n)  # @line L4
    for i in range(max(m, n)):  # @line L5
        c[i] = (a[i] if i < m else 0) + (b[i] if i < n else 0)  # @line L6
    return normalize(c)  # @line L7


def neg(a: Sequence[Any]) -> Poly:
    """The negative -a. Cost: len(a) negations."""
    return [-x for x in a]


def sub(a: Sequence[Any], b: Sequence[Any]) -> Poly:
    """The difference a - b, normalized. Cost: max(m, n) ring operations."""
    return add(a, neg(b))


def scale(s: Any, a: Sequence[Any]) -> Poly:
    """The product s * a for a ring element s, normalized. Cost: len(a) products."""
    return normalize([s * x for x in a])


def mul(a: Sequence[Any], b: Sequence[Any]) -> Poly:
    """The product a * b by the schoolbook method, normalized.

    Cost: m n ring multiplications and at most (m - 1)(n - 1) ring additions
    for m = len(a), n = len(b).
    """
    m, n = len(a), len(b)
    if m == 0 or n == 0:  # @line L8
        return []
    c: Poly = [0] * (m + n - 1)  # @line L9
    for i in range(m):  # @line L10
        ai = a[i]
        for j in range(n):  # @line L11
            c[i + j] = c[i + j] + ai * b[j]  # @line L12
    return normalize(c)  # @line L13


def evaluate(a: Sequence[Any], u: Any) -> Any:
    """The value a(u), by Horner's rule. Cost: len(a) products and additions."""
    s: Any = 0  # @line L14
    for i in range(len(a) - 1, -1, -1):  # @line L15
        s = s * u + a[i]  # @line L16
    return s  # @line L17


def _unit_inverse(c: Any) -> Any:
    """The inverse of a unit c: 1 and -1 over int, 1 / c for field elements."""
    if isinstance(c, int):
        if c in (1, -1):
            return c
        raise ValueError("the leading coefficient of the divisor must be a unit")
    return 1 / c


def divmod_poly(a: Sequence[Any], b: Sequence[Any]) -> Tuple[Poly, Poly]:
    """Return (q, r) with a = q b + r and deg r < deg b.

    Precondition: b is normalized, nonzero, and its leading coefficient is a
    unit of the coefficient ring (always true over a field; over int it must be
    1 or -1). Cost: one inversion, (m - n + 1) n multiplications and as many
    subtractions, for m = len(a) >= n = len(b).
    """
    m, n = len(a), len(b)
    if n == 0:
        raise ZeroDivisionError("division by the zero polynomial")
    r: Poly = list(a)  # @line L18
    q: Poly = [0] * max(m - n + 1, 0)
    v = _unit_inverse(b[-1])  # @line L19
    for k in range(m - n, -1, -1):  # @line L20
        t = r[k + n - 1] * v  # @line L21
        q[k] = t  # @line L22
        for j in range(n):  # @line L23
            r[k + j] = r[k + j] - t * b[j]  # @line L24
    return normalize(q), normalize(r[: n - 1])  # @line L25


def derivative(a: Sequence[Any]) -> Poly:
    """The formal derivative a', normalized. Cost: len(a) - 1 products by integers."""
    return normalize([i * a[i] for i in range(1, len(a))])
