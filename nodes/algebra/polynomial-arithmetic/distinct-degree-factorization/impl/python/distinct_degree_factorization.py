# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distinct-degree-factorization/. The authors are listed in prov/9GANAE.jsonl.

"""Distinct-degree factorization of a square-free polynomial over Z/pZ.

A polynomial a_0 + a_1 x + ... + a_n x^n is the list [a_0, ..., a_n] of ints
in 0 .. p - 1, lowest degree first; the zero polynomial is []. p must be a
prime.

For i = 1, 2, ..., the polynomial x^(p^i) - x is the product of all monic
irreducible polynomials whose degree divides i. So after the factors of
degree less than i have been removed, gcd(x^(p^i) - x, f) is the product of
the irreducible factors of degree exactly i. All loops are iterative.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

Poly = List[int]


def trim(a: Sequence[int]) -> Poly:
    """Return a copy of a without trailing zero coefficients."""
    out = list(a)
    while out and out[-1] == 0:
        out.pop()
    return out


def reduce_p(a: Sequence[int], p: int) -> Poly:
    """Reduce every coefficient into 0 .. p - 1 and strip leading zeros."""
    return trim([x % p for x in a])


def add(a: Sequence[int], b: Sequence[int], p: int) -> Poly:
    n = max(len(a), len(b))
    return trim([((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p for i in range(n)])


def sub(a: Sequence[int], b: Sequence[int], p: int) -> Poly:
    n = max(len(a), len(b))
    return trim([((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p for i in range(n)])


def mul(a: Sequence[int], b: Sequence[int], p: int) -> Poly:
    """Schoolbook product in (Z/pZ)[x]."""
    if not a or not b:
        return []
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                c[i + j] += x * y
    return reduce_p(c, p)


def divmod_p(a: Sequence[int], b: Sequence[int], p: int) -> Tuple[Poly, Poly]:
    """Quotient and remainder of a by the nonzero b in (Z/pZ)[x]."""
    b = reduce_p(b, p)
    if not b:
        raise ZeroDivisionError("division by the zero polynomial")
    r = reduce_p(a, p)
    inv = pow(b[-1], -1, p)
    db = len(b) - 1
    if len(r) <= db:
        return [], r
    q = [0] * (len(r) - db)
    for i in range(len(r) - 1, db - 1, -1):
        c = r[i] * inv % p
        if c:
            q[i - db] = c
            for j in range(db + 1):
                r[i - db + j] = (r[i - db + j] - c * b[j]) % p
    return trim(q), trim(r[:db])


def rem(a: Sequence[int], b: Sequence[int], p: int) -> Poly:
    return divmod_p(a, b, p)[1]


def monic(a: Sequence[int], p: int) -> Poly:
    """a divided by its leading coefficient; the zero polynomial stays zero."""
    a = reduce_p(a, p)
    if not a:
        return []
    inv = pow(a[-1], -1, p)
    return [x * inv % p for x in a]


def gcd_p(a: Sequence[int], b: Sequence[int], p: int) -> Poly:
    """The monic gcd in (Z/pZ)[x], by the Euclidean algorithm."""
    a, b = reduce_p(a, p), reduce_p(b, p)
    while b:
        a, b = b, rem(a, b, p)
    return monic(a, p)


def powmod(a: Sequence[int], e: int, f: Sequence[int], p: int) -> Poly:
    """a^e mod f in (Z/pZ)[x], by binary exponentiation (a loop)."""
    result = rem([1], f, p)
    base = rem(a, f, p)
    while e > 0:
        if e & 1:
            result = rem(mul(result, base, p), f, p)
        base = rem(mul(base, base, p), f, p)
        e >>= 1
    return result


def derivative(a: Sequence[int], p: int) -> Poly:
    return reduce_p([i * a[i] for i in range(1, len(a))], p)


def distinct_degree_factorization(f: Sequence[int], p: int, log: list | None = None) -> List[Tuple[Poly, int]]:
    """Split a monic square-free f into (g_i, i), g_i the product of its irreducible factors of degree i.

    Only the pairs with g_i != 1 are returned, in increasing order of i. If
    log is a list, (i, h, g) is appended for every gcd taken, where h is
    x^(p^i) mod the remaining part.
    """
    f = reduce_p(f, p)
    if not f or f[-1] != 1:
        raise ValueError("f must be monic")
    out: List[Tuple[Poly, int]] = []
    h = rem([0, 1], f, p)  # @line L1
    r, i = f, 0  # @line L1
    while len(r) - 1 >= 2 * (i + 1):  # @line L2
        i += 1  # @line L3
        h = powmod(h, p, r, p)  # @line L4
        g = gcd_p(sub(h, [0, 1], p), r, p)  # @line L5
        if log is not None:
            log.append((i, list(h), list(g)))
        if len(g) > 1:  # @line L6
            out.append((g, i))  # @line L6
            r = divmod_p(r, g, p)[0]  # @line L6
            h = rem(h, r, p)  # @line L6
    if len(r) > 1:  # @line L7
        out.append((r, len(r) - 1))  # @line L7
    return out  # @line L8
