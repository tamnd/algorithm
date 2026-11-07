# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/petkovsek-hyper-algorithm/. The authors are listed in prov/M8QSZ7.jsonl.
"""Petkovsek's algorithm Hyper over Q, with exact rational arithmetic.

A polynomial in n is a list of Fractions, lowest degree first, with no
trailing zeros; [] is the zero polynomial. A recurrence operator
L = sum p_i(n) S^i is the list [p_0, ..., p_r], and it acts on a sequence by
(L t)(n) = sum p_i(n) t(n + i).

hyper(L) returns every ratio t(n+1)/t(n), as a pair (numerator, denominator)
of polynomials in lowest terms with monic denominator, of the hypergeometric
solutions t of L t = 0 whose ratio lies in Q(n). It needs p_0 and p_r to split
into linear factors over Q, which it checks; then the list is complete in the
sense of the theorem in the proof file: every such solution is a linear
combination of solutions whose ratios are returned.
"""
from fractions import Fraction
from itertools import product
from math import comb


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def add(p, q):
    n = max(len(p), len(q))
    return trim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)])


def scale(p, c):
    return trim([c * a for a in p])


def mul(p, q):
    if not p or not q:
        return []
    r = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                r[i + j] += a * b
    return trim(r)


def shift(p, h):
    """p(n + h), by the binomial expansion of each (n + h)^j."""
    if h == 0 or not p:
        return list(p)
    r = [0] * len(p)
    for j, c in enumerate(p):
        if c:
            hp = 1
            for k in range(j, -1, -1):
                r[k] += c * comb(j, k) * hp
                hp *= h
    return trim(r)


def evaluate(p, x):
    v = Fraction(0)
    for c in reversed(p):
        v = v * x + c
    return v


def divmod_poly(p, q):
    p = trim(p)
    quo = [Fraction(0)] * max(len(p) - len(q) + 1, 0)
    while p and len(p) >= len(q):
        c = Fraction(p[-1]) / q[-1]
        k = len(p) - len(q)
        quo[k] = c
        p = add(p, scale([Fraction(0)] * k + q, -c))
    return trim(quo), p


def gcd_poly(p, q):
    p, q = trim(p), trim(q)
    while q:
        p, q = q, divmod_poly(p, q)[1]
    return scale(p, Fraction(1) / p[-1]) if p else []


def divisors(m):
    m = abs(m)
    out, d = [], 1
    while d * d <= m:
        if m % d == 0:
            out.append(d)
            out.append(m // d)
        d += 1
    return sorted(set(out))


def rational_roots(p):
    """The distinct rational roots of p, by the rational root theorem."""
    p = trim(p)
    roots = []
    if not p:
        raise ValueError("zero polynomial")
    while p and p[0] == 0:
        if 0 not in roots:
            roots.append(Fraction(0))
        p = p[1:]
    if len(p) <= 1:
        return roots
    den = 1
    for c in p:
        den = den * c.denominator // _gcd(den, c.denominator)
    z = [int(c * den) for c in p]
    g = 0
    for c in z:
        g = _gcd(g, c)
    z = [c // g for c in z]
    deg = len(z) - 1
    for u in divisors(z[0]):
        for v in divisors(z[-1]):
            if _gcd(u, v) != 1:
                continue
            for su in (u, -u):
                # v^deg p(su / v), in integers
                acc, up, vp = 0, 1, v ** deg
                for c in z:
                    acc += c * up * vp
                    up *= su
                    vp //= v
                if acc == 0:
                    roots.append(Fraction(su, v))
    return roots


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def linear_factors(p):
    """Roots of p with multiplicities, or ValueError if p does not split over Q."""
    p = trim(p)
    out = []
    for x in rational_roots(p):
        lin = [-x, Fraction(1)]
        while True:
            q, rem = divmod_poly(p, lin)
            if rem:
                break
            out.append(x)
            p = q
    if len(p) != 1:
        raise ValueError("coefficient does not split into linear factors over Q")
    return out


def monic_factors(p):
    """All monic divisors of p, which must split over Q."""
    roots = linear_factors(p)
    distinct = sorted(set(roots))
    mult = [roots.count(x) for x in distinct]
    out = []
    for es in product(*[range(e + 1) for e in mult]):
        f = [Fraction(1)]
        for x, e in zip(distinct, es):
            for _ in range(e):
                f = mul(f, [-x, Fraction(1)])
        out.append(f)
    return out


def nullspace(rows, ncols):
    """A basis of the solutions v of rows * v = 0, by Gauss-Jordan elimination."""
    rows = [list(r) for r in rows if any(r)]
    pivots, rank = [], 0
    for col in range(ncols):
        piv = next((i for i in range(rank, len(rows)) if rows[i][col] != 0), None)
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        inv = Fraction(1) / rows[rank][col]
        rows[rank] = [a * inv for a in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[rank])]
        pivots.append(col)
        rank += 1
    basis = []
    for free in range(ncols):
        if free in pivots:
            continue
        v = [Fraction(0)] * ncols
        v[free] = Fraction(1)
        for i, pc in enumerate(pivots):
            v[pc] = -rows[i][free]
        basis.append(v)
    return basis


def degree_bound(Q):
    """Largest possible degree of a nonzero polynomial solution of sum Q_i(n) c(n+i) = 0, or -1.

    Write sum Q_i E^i = sum R_k Delta^k with R_k = sum_(i >= k) C(i, k) Q_i. With
    b = max(deg R_k - k), the coefficient of n^(b + d) for deg c = d is
    lc(c) * phi(d) with phi(d) = sum over k with deg R_k - k = b of
    lc(R_k) d(d-1)...(d-k+1), so d is a root of phi.
    """
    r = len(Q) - 1
    R = [[] for _ in range(r + 1)]
    for k in range(r + 1):
        for i in range(k, r + 1):
            R[k] = add(R[k], scale(Q[i], comb(i, k)))
    b = max(len(R[k]) - 1 - k for k in range(r + 1) if R[k])
    phi = []
    for k in range(r + 1):
        if R[k] and len(R[k]) - 1 - k == b:
            ff = [Fraction(1)]
            for j in range(k):
                ff = mul(ff, [Fraction(-j), Fraction(1)])
            phi = add(phi, scale(ff, R[k][-1]))
    roots = [x for x in rational_roots(phi) if x.denominator == 1 and x >= 0]
    return int(max(roots)) if roots else -1


def polynomial_solutions(Q):
    """A basis of the polynomial solutions c of sum Q_i(n) c(n + i) = 0."""
    Q = [trim(q) for q in Q]
    D = degree_bound(Q)
    if D < 0:
        return []
    cols = []
    for j in range(D + 1):
        col = []
        for i, q in enumerate(Q):
            col = add(col, mul(q, shift([Fraction(0)] * j + [Fraction(1)], i)))
        cols.append(col)
    height = max((len(c) for c in cols), default=0)
    rows = [[c[e] if e < len(c) else Fraction(0) for c in cols] for e in range(height)]
    return [trim(v) for v in nullspace(rows, D + 1)]


def normalize_ratio(num, den):
    g = gcd_poly(num, den)
    num, den = divmod_poly(num, g)[0], divmod_poly(den, g)[0]
    c = den[-1]
    return (tuple(Fraction(x) for x in scale(num, Fraction(1) / c)),
            tuple(Fraction(x) for x in scale(den, Fraction(1) / c)))


def hyper(L, trace=None):
    """Ratios of the hypergeometric solutions of L t = 0 with ratio in Q(n)."""
    L = [trim([Fraction(c) for c in p]) for p in L]
    while L and not L[-1]:
        L.pop()
    r = len(L) - 1
    if r < 1 or not L[0]:
        raise ValueError("need an operator of order at least 1 with p_0 and p_r nonzero")
    found = []  # @line L1
    A = monic_factors(L[0])
    B = monic_factors(shift(L[r], -(r - 1)))
    for a in A:  # @line L2
        for b in B:
            P = []
            for i in range(r + 1):  # @line L3
                f = L[i]
                for j in range(i):
                    f = mul(f, shift(a, j))
                for j in range(i, r):
                    f = mul(f, shift(b, j))
                P.append(f)
            m = max(len(p) - 1 for p in P)  # @line L4
            alpha = [p[m] if len(p) - 1 == m else Fraction(0) for p in P]
            Zs = rational_roots(alpha)
            for Z in Zs:  # @line L5
                if Z == 0:
                    continue
                Q = [scale(P[i], Z ** i) for i in range(r + 1)]
                C = polynomial_solutions(Q)  # @line L6
                if trace is not None:
                    trace.append((tuple(a), tuple(b), Z, [tuple(c) for c in C]))
                for c in C:  # @line L7
                    ratio = normalize_ratio(mul(scale(a, Z), shift(c, 1)), mul(b, c))
                    if ratio not in found:
                        found.append(ratio)
            if trace is not None and not any(Z != 0 for Z in Zs):
                trace.append((tuple(a), tuple(b), None, []))
    return [(list(n), list(d)) for n, d in found]  # @line L8


def is_solution_ratio(L, num, den):
    """Exact check that t(n+1)/t(n) = num/den solves L t = 0 as a rational identity."""
    r = len(L) - 1
    total = []
    for i in range(r + 1):
        f = trim(L[i])
        for k in range(i):
            f = mul(f, shift(num, k))
        for k in range(i, r):
            f = mul(f, shift(den, k))
        total = add(total, f)
    return not total


def op_mul(M, F):
    """Product M F of shift operators, using S a(n) = a(n + 1) S."""
    out = []
    for i, m in enumerate(M):
        for j, f in enumerate(F):
            term = mul(m, shift(f, i))
            k = i + j
            while len(out) <= k:
                out.append([])
            out[k] = add(out[k], term)
    return out
