# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/primitive-prs/. The authors are listed in prov/1021Z1.jsonl.
"""The primitive polynomial remainder sequence and the gcd in Z[x].

A polynomial is a list of integers from the highest degree down, with no
leading zeros; the zero polynomial is []. The content cont(f) is the gcd of
the coefficients with the sign of the leading coefficient, so the primitive
part pp(f) = f / cont(f) has a positive leading coefficient.

Cost: O(m^2) integer operations for the pseudo-divisions and O(m^2) integer
gcds for the contents, m = max(deg f, deg g). Every member of the sequence is,
up to sign, the primitive part of a subresultant, so its coefficients are at
most ||f||_2^n ||g||_2^m in absolute value (Hadamard bound).
"""

from __future__ import annotations

from math import gcd


def _strip(p: list[int]) -> list[int]:
    i = 0
    while i < len(p) and p[i] == 0:
        i += 1
    return p[i:]


def content(p: list[int]) -> int:
    """gcd of the coefficients, with the sign of the leading coefficient; 0 for []."""
    c = 0
    for a in p:
        c = gcd(c, a)
    return -c if p and p[0] < 0 else c


def primitive_part(p: list[int]) -> list[int]:
    """p / content(p); [] for []."""
    c = content(p)
    return [a // c for a in p] if c else []


def prem(a: list[int], b: list[int]) -> list[int]:
    """Pseudo-remainder: LC(b)^(deg a - deg b + 1) a mod b, exact in Z[x]."""
    a = list(a)
    db, lb = len(b) - 1, b[0]
    e = len(a) - len(b) + 1
    while len(a) - 1 >= db and a:
        q = a[0]
        a = [lb * x for x in a]
        for k in range(len(b)):
            a[k] -= q * b[k]
        a = _strip(a[1:]) if a[0] == 0 else _strip(a)
        e -= 1
    return [lb ** e * x for x in a] if e > 0 else a


def primitive_prs(f: list[int], g: list[int]) -> tuple[list[int], list[list[int]]]:
    """Return (gcd(f, g) in Z[x] with positive leading coefficient, the primitive PRS)."""
    f, g = _strip(list(f)), _strip(list(g))
    if not f and not g:  # @line L1
        return [], []
    if len(f) < len(g):  # @line L2
        f, g = g, f
    if not g:  # @line L3
        return (f if f[0] > 0 else [-x for x in f]), [primitive_part(f)]
    c = gcd(content(f), content(g))  # @line L4
    A, B = primitive_part(f), primitive_part(g)
    seq = [A, B]
    while len(B) > 1:  # @line L5
        R = prem(A, B)  # @line L6
        if not R:  # @line L7
            return [c * x for x in B], seq
        A, B = B, primitive_part(R)  # @line L8
        seq.append(B)
    return [c], seq  # @line L9
