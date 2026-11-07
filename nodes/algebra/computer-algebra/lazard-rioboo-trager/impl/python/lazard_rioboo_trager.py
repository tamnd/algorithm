# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lazard-rioboo-trager/. The authors are listed in prov/J2RB9Z.jsonl.

"""Lazard-Rioboo-Trager: the logarithmic part of the integral of A/D over Q.

Univariate polynomials are lists of Fraction, lowest degree first, with a
nonzero last entry; [] is zero. A polynomial in Q[t][x] is a list indexed by
the x-degree whose entries are polynomials in t.

For a square-free D and deg A < deg D, lazard_rioboo_trager(A, D) returns pairs
(Q_i, S_i) with

    integral of A/D = sum over i of sum over Q_i(alpha) = 0 of alpha log S_i(alpha, x).
"""

from fractions import Fraction
from typing import List, Tuple

Poly = List[Fraction]
BiPoly = List[Poly]


def trim(f: Poly) -> Poly:
    f = [Fraction(a) for a in f]
    while f and f[-1] == 0:
        f.pop()
    return f


def add(f: Poly, g: Poly) -> Poly:
    n = max(len(f), len(g))
    return trim([(f[i] if i < len(f) else 0) + (g[i] if i < len(g) else 0) for i in range(n)])


def scale(c, f: Poly) -> Poly:
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


def pdivmod(f: Poly, g: Poly) -> Tuple[Poly, Poly]:
    r = trim(f)
    q = [Fraction(0)] * max(len(r) - len(g) + 1, 0)
    while len(r) >= len(g) and r:
        c = r[-1] / g[-1]
        s = len(r) - len(g)
        q[s] = c
        for i, b in enumerate(g):
            r[s + i] -= c * b
        r = trim(r)
    return trim(q), r


def monic(f: Poly) -> Poly:
    return scale(1 / f[-1], f) if f else []


def pgcd(f: Poly, g: Poly) -> Poly:
    f, g = trim(f), trim(g)
    while g:
        f, g = g, pdivmod(f, g)[1]
    return monic(f)


def inverse_mod(a: Poly, m: Poly) -> Poly:
    """The inverse of a modulo m, for gcd(a, m) = 1, by the extended Euclidean algorithm."""
    r0, r1 = trim(m), pdivmod(a, m)[1]
    s0, s1 = [], [Fraction(1)]
    while r1:
        q, r = pdivmod(r0, r1)
        r0, r1 = r1, r
        s0, s1 = s1, add(s0, scale(-1, mul(q, s1)))
    if len(r0) != 1:
        raise ValueError("not invertible")
    return pdivmod(scale(1 / r0[0], s0), m)[1]


def square_free(f: Poly) -> List[Poly]:
    """Yun's algorithm: monic [P_1, P_2, ...] with f = lc(f) prod P_i^i."""
    f = trim(f)
    if len(f) <= 1:
        return []
    out = []
    a = pgcd(f, deriv(f))
    b = pdivmod(f, a)[0]
    c = pdivmod(deriv(f), a)[0]
    d = add(c, scale(-1, deriv(b)))
    while len(b) > 1:
        a = pgcd(b, d)
        out.append(a)
        b = pdivmod(b, a)[0]
        c = pdivmod(d, a)[0]
        d = add(c, scale(-1, deriv(b)))
    return out


def det(M: List[List[Fraction]]) -> Fraction:
    M = [list(r) for r in M]
    n = len(M)
    d = Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return Fraction(0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            if M[r][c] != 0:
                q = M[r][c] / M[c][c]
                M[r] = [a - q * b for a, b in zip(M[r], M[c])]
    return d


def subresultant(P: Poly, p: int, Q: Poly, q: int, j: int) -> Poly:
    """The j-th subresultant of P and Q, of formal degrees p >= q > j, by determinants."""
    size = p + q - 2 * j
    rows = []
    for k in range(q - j - 1, -1, -1):
        rows.append(([Fraction(0)] * k + list(P)) + [Fraction(0)] * (p + q - j))
    for k in range(p - j - 1, -1, -1):
        rows.append(([Fraction(0)] * k + list(Q)) + [Fraction(0)] * (p + q - j))
    top = p + q - j - 1  # columns x^top down to x^(j+1), then one column x^i
    res = []
    for i in range(j + 1):
        M = [[r[e] for e in range(top, j, -1)] + [r[i]] for r in rows]
        assert len(M) == size and len(M[0]) == size
        res.append(det(M))
    return trim(res)


def interpolate(xs: List[Fraction], ys: List[Fraction]) -> Poly:
    out: Poly = []
    for i, xi in enumerate(xs):
        basis = [Fraction(1)]
        for j, xj in enumerate(xs):
            if j != i:
                basis = scale(1 / (xi - xj), mul(basis, [-xj, Fraction(1)]))
        out = add(out, scale(ys[i], basis))
    return out


def bivariate_subresultant(A: Poly, D: Poly, j: int) -> BiPoly:
    """The j-th subresultant of D and A - t D' w.r.t. x, as a polynomial in Q[t][x]."""
    n = len(D) - 1
    Dp = deriv(D)
    ts = [Fraction(k) for k in range(n + 1)]  # t-degree is at most n - j
    samples = []
    for t0 in ts:
        B = [(A[k] if k < len(A) else 0) - t0 * (Dp[k] if k < len(Dp) else 0) for k in range(n)]
        s = subresultant(D, n, [Fraction(b) for b in B], n - 1, j)
        samples.append(s + [Fraction(0)] * (j + 1 - len(s)))
    S = [interpolate(ts, [samples[k][e] for k in range(len(ts))]) for e in range(j + 1)]
    while S and not S[-1]:
        S.pop()
    return S


def lazard_rioboo_trager(A: Poly, D: Poly) -> List[Tuple[Poly, BiPoly]]:
    """The pairs (Q_i, S_i) of the logarithmic part of the integral of A/D."""
    A, D = trim(A), trim(D)
    n = len(D) - 1
    if n < 1 or len(A) > n:
        raise ValueError("need deg A < deg D")
    if len(pgcd(D, deriv(D))) > 1:
        raise ValueError("D must be square-free")
    if not A:
        return []
    S0 = bivariate_subresultant(A, D, 0)
    R = S0[0] if S0 else []  # @line L1
    Qs = square_free(R)  # @line L2
    out = []
    for i, Qi in enumerate(Qs, start=1):  # @line L3
        if len(Qi) <= 1:
            continue
        if i == n:
            S = [[c] for c in D]  # @line L4
        else:
            S = bivariate_subresultant(A, D, i)  # @line L5
        for j, Aj in enumerate(square_free(S[-1]), start=1):  # @line L6
            g = pgcd(Aj, Qi)
            for _ in range(j):  # @line L7
                S = [pdivmod(c, g)[0] for c in S]
        S = [pdivmod(c, Qi)[1] for c in S]  # @line L8
        while S and not S[-1]:
            S.pop()
        u = inverse_mod(S[-1], Qi)  # make S monic in x modulo Q_i
        S = [pdivmod(mul(u, c), Qi)[1] for c in S]
        out.append((Qi, S))
    return out  # @line L9
