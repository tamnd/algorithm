# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rational-univariate-representation/. The authors are listed in prov/KJ9098.jsonl.
"""Rational univariate representation (RUR) of a zero-dimensional ideal over Q.

Multivariate polynomials are dicts {exponent tuple: Fraction}; univariate
polynomials are lists of Fractions from the constant term up, [] is zero.
Input: generators F of an ideal I in Q[x_1, ..., x_n] with finitely many
complex zeros. Output: (lam, fbar, g1, gs) with u = sum lam[i] x_{i+1} a
separating linear form, fbar the monic squarefree polynomial whose roots are
the values u(alpha) at the zeros alpha, and polynomials g1, gs[i] of degree
below deg fbar, such that the zeros are exactly

    alpha = (gs[0](t) / g1(t), ..., gs[n-1](t) / g1(t))  for fbar(t) = 0.

Cost model: operations in Q, with D = dim_Q Q[x]/I. Given the Groebner basis
and the multiplication matrices (n D normal forms, whose cost depends on the
basis), the Hermite rank takes O(D^4), each trial of lam O(D^4) for the
powers of M_u, and the g polynomials O(n D^3). At most
(n - 1) D (D - 1) / 2 + 1 trials are needed, so O(n D^6) in the worst case;
in practice the first or second trial succeeds. The Groebner basis step
(line L1) is Buchberger's algorithm, which has no polynomial bound.
"""

from __future__ import annotations

from fractions import Fraction

Mono = tuple
MPoly = dict  # {Mono: Fraction}
UPoly = list  # [Fraction], low degree first


# ---------- multivariate arithmetic, grevlex order ----------

def _key(m: Mono) -> tuple:
    return (sum(m), tuple(-e for e in reversed(m)))


def _lm(f: MPoly) -> Mono:
    return max(f, key=_key)


def _divides(a: Mono, b: Mono) -> bool:
    return all(x <= y for x, y in zip(a, b))


def _addmul(f: MPoly, g: MPoly, mono: Mono, c: Fraction) -> MPoly:
    """Return f + c * mono * g."""
    r = dict(f)
    for e, v in g.items():
        k = tuple(x + y for x, y in zip(e, mono))
        w = r.get(k, Fraction(0)) + c * v
        if w:
            r[k] = w
        else:
            r.pop(k, None)
    return r


def _reduce(f: MPoly, G: list) -> MPoly:
    """Full normal form of f modulo the list G (a Groebner basis after L1)."""
    rem: MPoly = {}
    p = {e: Fraction(c) for e, c in f.items() if c}
    while p:
        m = _lm(p)
        c = p[m]
        for g in G:
            lg = _lm(g)
            if _divides(lg, m):
                q = tuple(x - y for x, y in zip(m, lg))
                p = _addmul(p, g, q, -c / g[lg])
                break
        else:
            rem[m] = c
            del p[m]
    return rem


def groebner(F: list, n: int) -> list:
    """Reduced Groebner basis for grevlex.

    Buchberger's algorithm with the normal selection strategy (least lcm
    first) and Buchberger's coprime and chain criteria.
    """
    G = [{e: Fraction(c) for e, c in f.items() if c} for f in F]
    G = [g for g in G if g]
    pending = {(j, i) for i in range(len(G)) for j in range(i)}

    def lcm_of(p: tuple) -> Mono:
        return tuple(max(x, y) for x, y in zip(_lm(G[p[0]]), _lm(G[p[1]])))

    while pending:
        i, j = min(pending, key=lambda p: _key(lcm_of(p)))
        pending.discard((i, j))
        a, b = _lm(G[i]), _lm(G[j])
        if all(x == 0 or y == 0 for x, y in zip(a, b)):
            continue  # coprime criterion: the S-polynomial reduces to 0
        L = lcm_of((i, j))
        if any(k not in (i, j) and _divides(_lm(G[k]), L)
               and (min(i, k), max(i, k)) not in pending
               and (min(j, k), max(j, k)) not in pending for k in range(len(G))):
            continue  # chain criterion
        s = _addmul({}, G[i], tuple(x - y for x, y in zip(L, a)), 1 / G[i][a])
        s = _addmul(s, G[j], tuple(x - y for x, y in zip(L, b)), -1 / G[j][b])
        r = _reduce(s, G)
        if r:
            lc = r[_lm(r)]
            G.append({e: c / lc for e, c in r.items()})
            pending.update((k, len(G) - 1) for k in range(len(G) - 1))
    # minimal, then reduced and monic
    G.sort(key=lambda g: _key(_lm(g)))
    M: list = []
    for g in G:
        if not any(_divides(_lm(h), _lm(g)) for h in M):
            M.append(g)
    out = []
    for k, g in enumerate(M):
        r = _reduce(g, M[:k] + M[k + 1:]) if len(M) > 1 else g
        lc = r[_lm(r)]
        out.append({e: c / lc for e, c in r.items()})
    return out


def normal_set(G: list, n: int) -> list:
    """Monomials outside LM(I), or ValueError if I is not zero-dimensional."""
    if any(all(e == 0 for e in _lm(g)) for g in G):
        return []  # unit ideal
    for i in range(n):
        if not any(_lm(g)[i] > 0 and sum(_lm(g)) == _lm(g)[i] for g in G):
            raise ValueError("the ideal is not zero-dimensional")
    lms = [_lm(g) for g in G]
    start = tuple([0] * n)
    seen = {start}
    stack = [start]
    while stack:
        m = stack.pop()
        for i in range(n):
            nm = m[:i] + (m[i] + 1,) + m[i + 1:]
            if nm not in seen and not any(_divides(l, nm) for l in lms):
                seen.add(nm)
                stack.append(nm)
    return sorted(seen, key=_key)


# ---------- linear algebra over Q ----------

def _matmul(A: list, B: list) -> list:
    n = len(A)
    Bt = list(zip(*B)) if B else []
    return [[sum((a * b for a, b in zip(A[r], Bt[c]) if a and b), Fraction(0))
             for c in range(n)] for r in range(n)]


def _trace_prod(A: list, B: list) -> Fraction:
    n = len(A)
    return sum((A[r][c] * B[c][r] for r in range(n) for c in range(n)
                if A[r][c] and B[c][r]), Fraction(0))


def _rank(A: list) -> int:
    M = [row[:] for row in A]
    rank, rows = 0, len(M)
    cols = len(M[0]) if M else 0
    for c in range(cols):
        piv = next((r for r in range(rank, rows) if M[r][c]), None)
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        for r in range(rows):
            if r != rank and M[r][c]:
                f = M[r][c] / M[rank][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[rank])]
        rank += 1
    return rank


# ---------- univariate arithmetic ----------

def _trim(p: UPoly) -> UPoly:
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def _udivmod(a: UPoly, b: UPoly) -> tuple:
    a, b = _trim(a), _trim(b)
    q = [Fraction(0)] * max(len(a) - len(b) + 1, 0)
    while len(a) >= len(b) and a:
        c = a[-1] / b[-1]
        k = len(a) - len(b)
        q[k] = c
        for i, v in enumerate(b):
            a[i + k] -= c * v
        a = _trim(a)
    return _trim(q), a


def _ugcd(a: UPoly, b: UPoly) -> UPoly:
    a, b = _trim(a), _trim(b)
    while b:
        a, b = b, _udivmod(a, b)[1]
    return [c / a[-1] for c in a] if a else []


def _deriv(p: UPoly) -> UPoly:
    return _trim([i * p[i] for i in range(1, len(p))])


def _charpoly_newton(s: list, D: int) -> UPoly:
    """Monic polynomial of degree D with power sums s[1..D] (characteristic 0)."""
    e = [Fraction(1)] + [Fraction(0)] * D
    for k in range(1, D + 1):
        e[k] = sum(((-1) ** (i - 1) * e[k - i] * s[i] for i in range(1, k + 1)),
                   Fraction(0)) / k
    return [(-1) ** (D - i) * e[D - i] for i in range(D + 1)]  # low degree first


# ---------- the algorithm ----------

def rur(F: list, n: int) -> tuple:
    """Rational univariate representation of the ideal generated by F."""
    G = groebner(F, n)                                    # @line L1
    B = normal_set(G, n)
    D = len(B)
    if D == 0:
        return [Fraction(1)] + [Fraction(0)] * (n - 1), [Fraction(1)], [], [[] for _ in range(n)]
    index = {b: k for k, b in enumerate(B)}
    Mx = []                                               # @line L2
    for i in range(n):
        M = [[Fraction(0)] * D for _ in range(D)]
        for col, b in enumerate(B):
            xb = b[:i] + (b[i] + 1,) + b[i + 1:]
            for e, c in _reduce({xb: Fraction(1)}, G).items():
                M[index[e]][col] = c
        Mx.append(M)
    Mb = {B[0]: [[Fraction(int(r == c)) for c in range(D)] for r in range(D)]}
    for b in B[1:]:                                       # @line L3
        i = next(k for k in range(n) if b[k] > 0)
        prev = b[:i] + (b[i] - 1,) + b[i + 1:]
        Mb[b] = _matmul(Mx[i], Mb[prev])
    herm = [[_trace_prod(Mb[b], Mb[c]) for c in B] for b in B]
    r = _rank(herm)
    lam_val = 0
    while True:                                           # @line L4
        lam = [Fraction(lam_val) ** i for i in range(n)]
        Mu = [[sum((lam[i] * Mx[i][a][b] for i in range(n)), Fraction(0))   # @line L5
               for b in range(D)] for a in range(D)]
        P = [Mb[B[0]]]
        for _ in range(D):
            P.append(_matmul(Mu, P[-1]))
        s = [sum((P[j][k][k] for k in range(D)), Fraction(0)) for j in range(D + 1)]
        f = _charpoly_newton(s, D)                        # @line L6
        g = _ugcd(f, _deriv(f))
        fbar = _udivmod(f, g)[0]                          # @line L7
        fbar = [c / fbar[-1] for c in fbar]
        d = len(fbar) - 1
        if d == r:                                        # @line L8
            break
        lam_val += 1
    # Horner polynomials H_k(T) = sum_{m=0}^{k} a_{d-m} T^{k-m}
    H = [[fbar[d - m] for m in range(k, -1, -1)] for k in range(d)]

    def g_of(Mv: list) -> UPoly:                          # @line L9
        out = [Fraction(0)] * d
        for j in range(d):
            t = _trace_prod(Mv, P[j])
            if t:
                for i, c in enumerate(H[d - 1 - j]):
                    out[i] += t * c
        return _trim(out)

    g1 = g_of(Mb[B[0]])
    gs = [g_of(Mx[i]) for i in range(n)]
    return lam, fbar, g1, gs                              # @line L10
