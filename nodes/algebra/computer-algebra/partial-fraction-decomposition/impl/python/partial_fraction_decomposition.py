# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-fraction-decomposition/. The authors are listed in prov/P053GE.jsonl.

"""Partial fraction decomposition of a rational function a / b over a field K.

A polynomial is a list of coefficients, lowest degree first, with no trailing
zero; the zero polynomial is []. Coefficients are Fraction, or any field type
with +, -, *, / and == 0.
"""

from typing import Dict, List, Sequence, Tuple

Poly = List[object]


def trim(f: Poly) -> Poly:
    f = list(f)
    while f and f[-1] == 0:
        f.pop()
    return f


def p_add(f: Poly, g: Poly) -> Poly:
    n = max(len(f), len(g))
    return trim([(f[i] if i < len(f) else 0) + (g[i] if i < len(g) else 0) for i in range(n)])


def p_sub(f: Poly, g: Poly) -> Poly:
    return p_add(f, [-c for c in g])


def p_mul(f: Poly, g: Poly) -> Poly:
    if not f or not g:
        return []
    h = [f[0] * 0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            h[i + j] = h[i + j] + a * b
    return trim(h)


def p_divmod(f: Poly, g: Poly) -> Tuple[Poly, Poly]:
    """Quotient and remainder of f by a nonzero g (long division)."""
    if not g:
        raise ZeroDivisionError("division by the zero polynomial")
    r = list(f)
    q = [g[-1] * 0] * max(0, len(f) - len(g) + 1)
    for k in range(len(f) - len(g), -1, -1):
        c = r[k + len(g) - 1] / g[-1]
        q[k] = c
        for j, b in enumerate(g):
            r[k + j] = r[k + j] - c * b
    return trim(q), trim(r[: len(g) - 1])


def p_pow(f: Poly, e: int) -> Poly:
    out: Poly = [f[-1] / f[-1]] if f else []
    for _ in range(e):
        out = p_mul(out, f)
    return out


def ext_gcd(f: Poly, g: Poly) -> Tuple[Poly, Poly, Poly]:
    """Monic gcd h and s, t with s f + t g = h (extended Euclidean algorithm)."""
    r0, r1 = trim(f), trim(g)
    one = (r0 or r1)[-1] / (r0 or r1)[-1]
    s0, s1, t0, t1 = [one], [], [], [one]
    while r1:
        q, r = p_divmod(r0, r1)
        r0, r1 = r1, r
        s0, s1 = s1, p_sub(s0, p_mul(q, s1))
        t0, t1 = t1, p_sub(t0, p_mul(q, t1))
    lc = r0[-1]
    return [c / lc for c in r0], [c / lc for c in s0], [c / lc for c in t0]


def partial_fractions(a: Poly, factors: Sequence[Tuple[Poly, int]]) -> Tuple[Poly, Dict[Tuple[int, int], Poly]]:
    """Decompose a / b with b = prod b_i^e_i given as factors = [(b_i, e_i), ...].

    Precondition: each b_i has degree >= 1, each e_i >= 1, and the b_i are
    pairwise coprime. Returns the polynomial part q and a dict that maps (i, j)
    to a_ij with deg a_ij < deg b_i, such that
    a / b = q + sum over i and 1 <= j <= e_i of a_ij / b_i^j.
    Cost: O(d^2 + deg(a) d) field operations with classical arithmetic, d = deg b.
    """
    b: Poly = [1]
    powers = []
    for bi, ei in factors:
        if len(trim(bi)) < 2 or ei < 1:
            raise ValueError("each factor needs degree >= 1 and multiplicity >= 1")
        powers.append(p_pow(trim(bi), ei))
    one = powers[0][-1] / powers[0][-1] if powers else 1
    b = [one]
    for pw in powers:
        b = p_mul(b, pw)  # @line L1
    q, a = p_divmod(trim(a), b)  # @line L2
    parts: Dict[Tuple[int, int], Poly] = {}
    for i, (bi, ei) in enumerate(factors):  # @line L3
        ci, rem = p_divmod(b, powers[i])  # @line L4
        g, s, _ = ext_gcd(ci, powers[i])  # @line L5
        if len(g) != 1:
            raise ValueError("the factors must be pairwise coprime")
        r = p_divmod(p_mul(a, s), powers[i])[1]  # @line L6
        for j in range(ei, 0, -1):  # @line L7
            r, parts[(i, j)] = p_divmod(r, trim(bi))  # @line L8
    return q, parts  # @line L9
