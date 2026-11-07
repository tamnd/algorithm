# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heuristic-gcd/. The authors are listed in prov/N1KXF6.jsonl.

"""Heuristic gcd of two polynomials in Z[x] (Char, Geddes and Gonnet).

A polynomial is a list of integers [a_0, a_1, ..., a_d], lowest degree first,
with a nonzero last entry. The zero polynomial is []. The gcd is returned with
a positive leading coefficient.
"""

from math import gcd
from typing import List, Optional, Tuple

Poly = List[int]


def trim(f: Poly) -> Poly:
    """Remove zero coefficients at the top."""
    f = list(f)
    while f and f[-1] == 0:
        f.pop()
    return f


def content(f: Poly) -> int:
    """The gcd of the coefficients, 0 for the zero polynomial."""
    c = 0
    for a in f:
        c = gcd(c, a)
    return c


def primitive_part(f: Poly) -> Poly:
    """f divided by its content, with a positive leading coefficient."""
    c = content(f)
    if c == 0:
        return []
    if f[-1] < 0:
        c = -c
    return [a // c for a in f]


def norm(f: Poly) -> int:
    """The max norm |f|_inf."""
    return max((abs(a) for a in f), default=0)


def evaluate(f: Poly, xi: int) -> int:
    """f(xi) by Horner's rule."""
    v = 0
    for a in reversed(f):
        v = v * xi + a
    return v


def genpoly(gamma: int, xi: int) -> Poly:
    """The polynomial whose coefficients are the symmetric xi-adic digits of gamma.

    Each digit lies in (-xi/2, xi/2], and the result h satisfies h(xi) = gamma.
    """
    h: Poly = []
    while gamma != 0:
        r = gamma % xi
        if 2 * r > xi:
            r -= xi
        h.append(r)
        gamma = (gamma - r) // xi
    return h


def divides(h: Poly, f: Poly) -> bool:
    """True when h divides f in Z[x] (h nonzero), by exact long division."""
    r = list(f)
    dh = len(h) - 1
    lc = h[-1]
    while len(r) - 1 >= dh and r:
        q, m = divmod(r[-1], lc)
        if m != 0:
            return False
        shift = len(r) - 1 - dh
        for i, a in enumerate(h):
            r[shift + i] -= q * a
        r = trim(r)
    return not r


def heuristic_gcd(f: Poly, g: Poly, tries: int = 6) -> Optional[Poly]:
    """Return gcd(f, g) in Z[x], or None if every evaluation point fails.

    None means: fall back to another method, such as a modular gcd.
    """
    f, g = trim(f), trim(g)
    if not f or not g:
        h = f or g
        return [-a for a in h] if h and h[-1] < 0 else h
    c = gcd(content(f), content(g))  # @line L1
    f, g = primitive_part(f), primitive_part(g)
    xi = 2 * min(norm(f), norm(g)) + 2  # @line L2
    for _ in range(tries):  # @line L3
        gamma = gcd(evaluate(f, xi), evaluate(g, xi))  # @line L4
        h = genpoly(gamma, xi)  # @line L5
        h = primitive_part(h)  # @line L6
        if divides(h, f) and divides(h, g):  # @line L7
            return [c * a for a in h]
        xi = xi * 73794 // 27011  # @line L8
    return None  # @line L9


def heuristic_gcd_trace(f: Poly, g: Poly, tries: int = 6) -> List[Tuple[int, int, Poly, bool]]:
    """The list of (xi, gamma, h, accepted) for each evaluation point tried."""
    f, g = primitive_part(trim(f)), primitive_part(trim(g))
    xi = 2 * min(norm(f), norm(g)) + 2
    out = []
    for _ in range(tries):
        gamma = gcd(evaluate(f, xi), evaluate(g, xi))
        h = primitive_part(genpoly(gamma, xi))
        ok = divides(h, f) and divides(h, g)
        out.append((xi, gamma, h, ok))
        if ok:
            break
        xi = xi * 73794 // 27011
    return out
