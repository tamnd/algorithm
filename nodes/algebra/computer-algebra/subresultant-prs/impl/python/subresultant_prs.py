# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subresultant-prs/. The authors are listed in prov/ESA0T9.jsonl.
"""The subresultant PRS and the full subresultant chain S_0, ..., S_(n-1).

Polynomials are lists of coefficients from the highest degree down, with no
leading zeros; [] is the zero polynomial. Coefficients lie in an integral
domain with exact division (int here). S_j is the j-th subresultant of f and g
for the Sylvester matrix whose rows are x^(n-1) f, ..., f, x^(m-1) g, ..., g;
S_0 = Res(f, g).

Cost: O(m n) ring operations for deg f = m >= deg g = n >= 1, plus the
powers in the gap formula. Every member of the chain is a subresultant, so
over Z its coefficients are at most ||f||_2^n ||g||_2^m in absolute value.
"""

from __future__ import annotations

from math import gcd


def _strip(p: list[int]) -> list[int]:
    i = 0
    while i < len(p) and p[i] == 0:
        i += 1
    return p[i:]


def _exact(a: int, b: int) -> int:
    q, r = divmod(a, b)
    if r:
        raise ArithmeticError("division is not exact")
    return q


def prem(a: list[int], b: list[int]) -> list[int]:
    """Pseudo-remainder LC(b)^(deg a - deg b + 1) a mod b, for deg a >= deg b >= 0."""
    a = list(a)
    lb, e = b[0], len(a) - len(b) + 1
    while a and len(a) >= len(b):
        q = a[0]
        a = [lb * x for x in a]
        for k in range(len(b)):
            a[k] -= q * b[k]
        a = _strip(a)
        e -= 1
    return [lb ** e * x for x in a]


def subresultant_chain(f: list[int], g: list[int]) -> tuple[list[list[int]], list[int]]:
    """Return ([S_0, ..., S_(n-1)], the last nonzero member of the subresultant PRS).

    Requires deg f >= deg g >= 1. S_j is [] when the j-th subresultant is zero.
    """
    f, g = _strip(list(f)), _strip(list(g))
    m, n = len(f) - 1, len(g) - 1
    if n < 1 or m < n:
        raise ValueError("need deg f >= deg g >= 1")
    S: list[list[int]] = [[] for _ in range(n)]  # @line L1
    A, B = f, g  # @line L2
    delta = m - n
    s = g[0] ** delta  # @line L3
    beta = (-1) ** (delta + 1)  # @line L4
    while True:  # @line L5
        C = [_exact(x, beta) for x in prem(A, B)]  # @line L6
        if not C:  # @line L7
            return S, B
        b, c = len(B) - 1, len(C) - 1
        S[b - 1] = C  # @line L8
        e = b - c
        if e >= 2:  # @line L9
            S[c] = [_exact(x * C[0] ** (e - 1), s ** (e - 1)) for x in C]
        if c == 0:  # @line L10
            return S, C
        beta = -B[0] * (-s) ** e  # @line L11
        s = S[c][0]  # @line L12
        A, B = B, C  # @line L13


def subresultant_gcd(f: list[int], g: list[int]) -> list[int]:
    """gcd(f, g) in Z[x] with positive leading coefficient, from the subresultant PRS."""
    f, g = _strip(list(f)), _strip(list(g))
    if len(f) < len(g):
        f, g = g, f
    if not g:
        return f if not f or f[0] > 0 else [-x for x in f]

    def cont(p: list[int]) -> int:
        c = 0
        for x in p:
            c = gcd(c, x)
        return c

    c = gcd(cont(f), cont(g))
    if len(g) == 1:
        return [c]
    _, last = subresultant_chain(f, g)
    if len(last) == 1:
        return [c]
    k = cont(last) * (1 if last[0] > 0 else -1)
    return [c * (x // k) for x in last]
