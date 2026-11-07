# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rothstein-trager/. The authors are listed in prov/2HTAE6.jsonl.
"""The Rothstein-Trager algorithm for the logarithmic part of a rational integral.

Polynomials are lists of Fractions from the constant term up (index = degree);
[] is the zero polynomial. Input: A, D in Q[x], D squarefree, deg A < deg D.
Output: the resultant R(z) = res_x(D, A - z D') and a list of pairs (q, S),
q in Q[z] monic squarefree and S in (Q[z]/q)[x] monic in x, such that

    integral of A/D dx = sum over pairs, sum over roots c of q, of c log S(c, x).

Rational roots of R come out as pairs with deg q = 1. The other factors are
handled in Q[z]/(q) by the Euclidean algorithm, splitting q when a leading
coefficient is a zero divisor, so R is never factored. Cost model: operations
in Q, with n = deg D. The resultant takes O(n^4) operations (n + 1 elimination
determinants of order 2n - 1), each gcd attempt over Q[z]/(q) takes O(n^2 k^2)
with k = deg q, and there are at most 2n attempts, so O(n^5) in all. The
rational root search (line L2) is not a field operation: it tries the divisors
of two integer coefficients, which is exponential in their length.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd as igcd

Poly = list  # list of Fraction, low degree first


def norm(p: Poly) -> Poly:
    p = [Fraction(c) for c in p]
    while p and p[-1] == 0:
        p.pop()
    return p


def padd(a: Poly, b: Poly) -> Poly:
    n = max(len(a), len(b))
    return norm([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])


def pscale(a: Poly, c) -> Poly:
    return norm([c * x for x in a])


def pmul(a: Poly, b: Poly) -> Poly:
    if not a or not b:
        return []
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return norm(out)


def pdivmod(a: Poly, b: Poly) -> tuple[Poly, Poly]:
    a, b = norm(a), norm(b)
    q = [Fraction(0)] * max(len(a) - len(b) + 1, 0)
    while a and len(a) >= len(b):
        k, c = len(a) - len(b), a[-1] / b[-1]
        q[k] = c
        a = norm([a[i] - (c * b[i - k] if 0 <= i - k < len(b) else 0) for i in range(len(a))])
    return norm(q), a


def pgcd(a: Poly, b: Poly) -> Poly:
    a, b = norm(a), norm(b)
    while b:
        a, b = b, pdivmod(a, b)[1]
    return pscale(a, 1 / a[-1]) if a else []


def deriv(a: Poly) -> Poly:
    return norm([i * a[i] for i in range(1, len(a))])


def peval(a: Poly, x):
    r = Fraction(0)
    for c in reversed(a):
        r = r * x + c
    return r


def _det(M: list[list[Fraction]]) -> Fraction:
    M = [row[:] for row in M]
    n, d = len(M), Fraction(1)
    for k in range(n):
        p = next((r for r in range(k, n) if M[r][k] != 0), None)
        if p is None:
            return Fraction(0)
        if p != k:
            M[k], M[p] = M[p], M[k]
            d = -d
        d *= M[k][k]
        for i in range(k + 1, n):
            f = M[i][k] / M[k][k]
            if f:
                for j in range(k, n):
                    M[i][j] -= f * M[k][j]
    return d


def resultant_formal(f: Poly, g: Poly, m: int, n: int) -> Fraction:
    """Sylvester determinant for formal degrees m and n (f has degree m)."""
    N = m + n
    if N == 0:
        return Fraction(1)
    fc = [f[m - k] if m - k < len(f) else Fraction(0) for k in range(m + 1)]  # high first
    gc = [g[n - k] if n - k < len(g) else Fraction(0) for k in range(n + 1)]
    M = [[Fraction(0)] * N for _ in range(N)]
    for i in range(n):
        for k in range(m + 1):
            M[i][i + k] = fc[k]
    for j in range(m):
        for k in range(n + 1):
            M[n + j][j + k] = gc[k]
    return _det(M)


def rt_resultant(A: Poly, D: Poly) -> Poly:
    """R(z) = res_x(D, A - z D') with formal degrees (n, n - 1), by interpolation in z."""
    n = len(D) - 1
    Dp = deriv(D)
    pts = list(range(n + 1))
    vals = [resultant_formal(D, padd(A, pscale(Dp, -z)), n, n - 1) for z in pts]
    R: Poly = []
    for i, zi in enumerate(pts):  # Lagrange interpolation
        basis, den = [Fraction(1)], Fraction(1)
        for j, zj in enumerate(pts):
            if j != i:
                basis = pmul(basis, [Fraction(-zj), Fraction(1)])
                den *= zi - zj
        R = padd(R, pscale(basis, vals[i] / den))
    return R


def rational_roots(R: Poly) -> list[Fraction]:
    """All rational roots of R, by the rational root test on the integer form."""
    R = norm(R)
    if not R:
        return []
    L = 1
    for c in R:
        L = L * c.denominator // igcd(L, c.denominator)
    Z = [int(c * L) for c in R]
    while Z and Z[0] == 0:
        Z = Z[1:]
    roots = [Fraction(0)] if len(Z) < len(R) else []
    g = 0
    for c in Z:
        g = igcd(g, c)
    Z = [c // g for c in Z]
    a0, an = abs(Z[0]), abs(Z[-1])

    def divs(v: int) -> list[int]:
        small, d = [], 1
        while d * d <= v:
            if v % d == 0:
                small.append(d)
            d += 1
        return small + [v // d for d in reversed(small) if d * d != v]
    for p in divs(a0):
        for q in divs(an):
            if igcd(p, q) != 1:
                continue
            for s in (1, -1):
                c = Fraction(s * p, q)
                # q^k R(c) in integers, k = deg R, so that the test needs no fractions
                k = len(Z) - 1
                val = sum(z * (s * p) ** i * q ** (k - i) for i, z in enumerate(Z))
                if val == 0 and c not in roots:
                    roots.append(c)
    return roots


# Arithmetic in Q[z]/(q): elements are Polys of length < deg q.
class ZeroDivisor(Exception):
    def __init__(self, factor: Poly):
        self.factor = factor


def amul(a: Poly, b: Poly, q: Poly) -> Poly:
    return pdivmod(pmul(a, b), q)[1]


def ainv(a: Poly, q: Poly) -> Poly:
    """Inverse of a mod q, or raise ZeroDivisor with a proper factor of q."""
    r0, r1, s0, s1 = q, a, [], [Fraction(1)]
    while r1:
        quo, rem = pdivmod(r0, r1)
        r0, r1 = r1, rem
        s0, s1 = s1, padd(s0, pscale(pmul(quo, s1), -1))
    if len(r0) > 1:
        raise ZeroDivisor(pscale(r0, 1 / r0[-1]))
    return pdivmod(pscale(s0, 1 / r0[0]), q)[1]


def xgcd_mod(F: list[Poly], G: list[Poly], q: Poly) -> list[Poly]:
    """Monic gcd in (Q[z]/q)[x]; F, G are lists of algebra elements, low degree in x first."""
    def strip(P):
        P = [pdivmod(c, q)[1] for c in P]
        while P and not P[-1]:
            P.pop()
        return P
    a, b = strip(F), strip(G)
    while b:
        inv = ainv(b[-1], q)
        while a and len(a) >= len(b):
            k, c = len(a) - len(b), amul(a[-1], inv, q)
            a = strip([padd(a[i], pscale(amul(c, b[i - k], q), -1)) if 0 <= i - k < len(b) else a[i]
                       for i in range(len(a))])
        a, b = b, a
    inv = ainv(a[-1], q)
    return [amul(c, inv, q) for c in a]


def rothstein_trager(A: Poly, D: Poly) -> tuple[Poly, list[tuple[Poly, list[Poly]]]]:
    """Return (R, pairs) with integral A/D = sum over pairs (q, S) of sum_{q(c)=0} c log S(c, x)."""
    A, D = norm(A), norm(D)
    if len(D) < 2 or len(A) >= len(D):
        raise ValueError("need deg A < deg D and deg D >= 1")
    Dp = deriv(D)
    R = rt_resultant(A, D)  # @line L1
    pairs: list[tuple[Poly, list[Poly]]] = []
    if not A:
        return R, pairs
    rest = pscale(R, 1 / R[-1])
    sqf = pdivmod(rest, pgcd(rest, deriv(rest)))[0]  # same roots as R, smaller coefficients
    for c in rational_roots(sqf):  # @line L2
        rest = pdivmod(rest, [-c, Fraction(1)])[0]
        while not pdivmod(rest, [-c, Fraction(1)])[1]:
            rest = pdivmod(rest, [-c, Fraction(1)])[0]
        if c != 0:
            v = pgcd(D, padd(A, pscale(Dp, -c)))  # @line L3
            pairs.append(([-c, Fraction(1)], [[x] for x in v]))
    q0 = pdivmod(rest, pgcd(rest, deriv(rest)))[0] if len(rest) > 1 else []  # @line L4
    stack = [pscale(q0, 1 / q0[-1])] if len(q0) > 1 else []
    while stack:  # @line L5
        q = stack.pop()
        Fz = [[c] for c in D]
        Gz = [padd([a], [Fraction(0), -d]) for a, d in
              zip(A + [Fraction(0)] * (len(Dp) - len(A)), Dp + [Fraction(0)] * (len(A) - len(Dp)))]
        try:
            S = xgcd_mod(Fz, Gz, q)  # @line L6
        except ZeroDivisor as zd:  # @line L7
            g = zd.factor
            stack.append(g)
            stack.append(pdivmod(q, g)[0])
            continue
        pairs.append((q, S))  # @line L8
    return R, pairs
