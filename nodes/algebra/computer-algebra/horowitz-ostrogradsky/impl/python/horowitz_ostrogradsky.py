# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horowitz-ostrogradsky/. The authors are listed in prov/KX6NMH.jsonl.

"""Horowitz-Ostrogradsky method: the rational part of the integral of A/D.

Polynomials over Q are lists of Fraction, lowest degree first, with a nonzero
last entry; the zero polynomial is []. For deg A < deg D the function returns
B, Dm, C, Ds with

    integral of A/D = B/Dm + integral of C/Ds,

where Dm = gcd(D, D'), Ds = D/Dm is square-free, deg B < deg Dm, deg C < deg Ds.
"""

from fractions import Fraction
from typing import List, Tuple

Poly = List[Fraction]


def trim(f: Poly) -> Poly:
    f = [Fraction(a) for a in f]
    while f and f[-1] == 0:
        f.pop()
    return f


def add(f: Poly, g: Poly) -> Poly:
    n = max(len(f), len(g))
    return trim([(f[i] if i < len(f) else 0) + (g[i] if i < len(g) else 0) for i in range(n)])


def scale(c: Fraction, f: Poly) -> Poly:
    return trim([c * a for a in f])


def mul(f: Poly, g: Poly) -> Poly:
    if not f or not g:
        return []
    r = [Fraction(0)] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            r[i + j] += a * b
    return trim(r)


def deriv(f: Poly) -> Poly:
    return trim([i * f[i] for i in range(1, len(f))])


def divmod_poly(f: Poly, g: Poly) -> Tuple[Poly, Poly]:
    """Quotient and remainder of f by a nonzero g."""
    r = list(trim(f))
    q = [Fraction(0)] * max(len(r) - len(g) + 1, 0)
    while len(r) >= len(g) and r:
        c = r[-1] / g[-1]
        s = len(r) - len(g)
        q[s] = c
        for i, b in enumerate(g):
            r[s + i] -= c * b
        r = trim(r)
    return trim(q), r


def gcd_poly(f: Poly, g: Poly) -> Poly:
    """Monic gcd by the Euclidean algorithm."""
    f, g = trim(f), trim(g)
    while g:
        f, g = g, divmod_poly(f, g)[1]
    return scale(1 / f[-1], f) if f else []


def solve(M: List[List[Fraction]], rhs: List[Fraction]) -> List[Fraction]:
    """Solve the square nonsingular system M y = rhs by Gaussian elimination."""
    n = len(M)
    A = [list(M[i]) + [rhs[i]] for i in range(n)]
    for col in range(n):
        piv = next(r for r in range(col, n) if A[r][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        inv = 1 / A[col][col]
        A[col] = [inv * a for a in A[col]]
        for r in range(n):
            if r != col and A[r][col] != 0:
                c = A[r][col]
                A[r] = [a - c * b for a, b in zip(A[r], A[col])]
    return [A[i][n] for i in range(n)]


def horowitz_ostrogradsky(A: Poly, D: Poly) -> Tuple[Poly, Poly, Poly, Poly]:
    """Return (B, Dm, C, Ds) with integral A/D = B/Dm + integral C/Ds."""
    A, D = trim(A), trim(D)
    if not D:
        raise ValueError("D must be nonzero")
    if len(A) >= len(D):
        raise ValueError("need deg A < deg D")
    Dm = gcd_poly(D, deriv(D))  # @line L1
    Ds = divmod_poly(D, Dm)[0]  # @line L2
    n, m = len(Dm) - 1, len(Ds) - 1  # @line L3
    # L4: B = sum b_i x^i (i < n) and C = sum c_j x^j (j < m) are the unknowns.
    E = divmod_poly(mul(Ds, deriv(Dm)), Dm)[0]  # Ds * Dm' / Dm, a polynomial
    columns: List[Poly] = []  # @line L4
    for i in range(n):  # the image of x^i as B: (x^i)' Ds - x^i E
        xi = [Fraction(0)] * i + [Fraction(1)]
        columns.append(add(mul(deriv(xi), Ds), scale(Fraction(-1), mul(xi, E))))
    for j in range(m):  # the image of x^j as C: x^j Dm
        xj = [Fraction(0)] * j + [Fraction(1)]
        columns.append(mul(xj, Dm))
    size = n + m  # = deg D
    M = [[col[r] if r < len(col) else Fraction(0) for col in columns] for r in range(size)]  # @line L5
    rhs = [A[r] if r < len(A) else Fraction(0) for r in range(size)]
    y = solve(M, rhs)  # @line L6
    B = trim(y[:n])
    C = trim(y[n:])
    return B, Dm, C, Ds  # @line L7
