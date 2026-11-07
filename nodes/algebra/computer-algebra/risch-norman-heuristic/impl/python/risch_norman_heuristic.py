# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/risch-norman-heuristic/. The authors are listed in prov/XPCGZH.jsonl.
"""The Risch-Norman (parallel Risch) heuristic over Q.

The integrand lives in Q(x, t_1, ..., t_m), where each t_i is a monomial
(for example exp(a(x)), log(b(x)) or tan(x)) given by its derivative
t_i' = N_i / d with N_i in Q[x, t] and one common denominator d in Q[x].
The scaled derivation is D = d d/dx + sum_i N_i d/dt_i, so D = d * (d/dx).
Polynomials are dicts {exponent tuple (x, t_1, ..., t_m): Fraction}.

The integrand is P / Q with Q given as a list of factors (q, e), the q
pairwise coprime and squarefree. The method guesses

    integral = U / B + sum_j c_j log(v_j),

with B from the factors of Q, v_j the factors of Q and any extra candidates,
U a polynomial of bounded total degree with unknown coefficients and c_j
unknown constants, and solves one linear system over Q. It returns
(U, B, [(c_j, v_j)]) or None. None does not prove that no elementary integral
exists: the guess may be too small.

Cost model: operations in Q. With N unknowns, S the largest number of terms
of a polynomial in the cleared equation and E <= the number of its
monomials, building the system takes O(N S^2) and Gaussian elimination
O(E N^2); both are proved bounds for this procedure. Whether it succeeds is
a matter of the guess, and it is observed to succeed on most integrals met
in practice.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product as iproduct

Poly = dict


def clean(p: Poly) -> Poly:
    return {e: c for e, c in p.items() if c != 0}


def padd(*ps: Poly) -> Poly:
    r: Poly = {}
    for p in ps:
        for e, c in p.items():
            r[e] = r.get(e, Fraction(0)) + c
    return clean(r)


def pscale(p: Poly, c) -> Poly:
    return clean({e: v * c for e, v in p.items()})


def pmul(*ps: Poly) -> Poly:
    if not ps:
        raise ValueError("pmul needs at least one factor")
    r = ps[0]
    for p in ps[1:]:
        out: Poly = {}
        for a, x in r.items():
            for b, y in p.items():
                k = tuple(i + j for i, j in zip(a, b))
                out[k] = out.get(k, Fraction(0)) + x * y
        r = clean(out)
    return r


def ppow(p: Poly, k: int, nv: int) -> Poly:
    r = {tuple([0] * nv): Fraction(1)}
    for _ in range(k):
        r = pmul(r, p)
    return r


def pdiff(p: Poly, i: int) -> Poly:
    out: Poly = {}
    for e, c in p.items():
        if e[i]:
            k = e[:i] + (e[i] - 1,) + e[i + 1:]
            out[k] = out.get(k, Fraction(0)) + c * e[i]
    return clean(out)


def tdeg(p: Poly) -> int:
    return max((sum(e) for e in p), default=0)


def derive(p: Poly, d: Poly, N: list) -> Poly:
    """The scaled derivation D(p) = d dp/dx + sum N_i dp/dt_i."""
    terms = [pmul(d, pdiff(p, 0))] if pdiff(p, 0) else []
    for i, Ni in enumerate(N):
        dp = pdiff(p, i + 1)
        if dp:
            terms.append(pmul(Ni, dp))
    return padd(*terms) if terms else {}


def divides(a: Poly, b: Poly) -> bool:
    """True if a divides b in Q[x, t] (division by a single polynomial)."""
    if not b:
        return True
    key = lambda e: e  # lex order on (x, t_1, ..., t_m)
    la = max(a, key=key)
    r = dict(b)
    while r:
        lb = max(r, key=key)
        if any(i < j for i, j in zip(lb, la)):
            return False  # the leading monomial of a does not divide it
        q = tuple(i - j for i, j in zip(lb, la))
        c = r[lb] / a[la]
        r = padd(r, pscale(pmul(a, {q: Fraction(1)}), -c))
    return True


def ansatz_denominator(Qf: list, d: Poly, N: list, nv: int) -> Poly:
    """B = prod q^(e-1) over normal q, times prod q^e over special q."""
    B = {tuple([0] * nv): Fraction(1)}
    for q, e in Qf:
        special = divides(q, derive(q, d, N))
        B = pmul(B, ppow(q, e if special else e - 1, nv))
    return B


def _solve(cols: list, rhs: Poly):
    """Solve sum_k z_k cols[k] = rhs coefficientwise; None if inconsistent."""
    mons = sorted(set(rhs).union(*[set(c) for c in cols]))
    rows = [[c.get(m, Fraction(0)) for c in cols] + [rhs.get(m, Fraction(0))]
            for m in mons]
    nc = len(cols)
    piv_cols = []
    r = 0
    for c in range(nc):
        p = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        inv = 1 / rows[r][c]
        rows[r] = [v * inv for v in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv_cols.append(c)
        r += 1
    if any(row[nc] for row in rows[r:]):
        return None
    z = [Fraction(0)] * nc  # free unknowns are set to 0
    for i, c in enumerate(piv_cols):
        z[c] = rows[i][nc]
    return z


def risch_norman(P: Poly, Qf: list, d: Poly, N: list,
                 extra_logs: tuple = (), deg_bound=None):
    """Try to integrate P / prod(q^e) in the tower given by d and N."""
    nv = len(N) + 1
    one = {tuple([0] * nv): Fraction(1)}
    P = clean({e: Fraction(c) for e, c in P.items()})
    if not P:
        return {}, one, []
    Q = one
    for q, e in Qf:
        Q = pmul(Q, ppow(q, e, nv))
    B = ansatz_denominator(Qf, d, N, nv)                       # @line L1
    V = [q for q, _ in Qf if tdeg(q) > 0] + list(extra_logs)   # @line L2
    if deg_bound is None:                                      # @line L3
        deg_bound = max(tdeg(P) - tdeg(Q), 0) + tdeg(B) + 1
    mons = [e for e in iproduct(range(deg_bound + 1), repeat=nv)
            if sum(e) <= deg_bound]                            # @line L4
    W = one
    for v in V:
        W = pmul(W, v)
    DB = derive(B, d, N)
    QW = pmul(Q, W)
    cols = []                                                  # @line L5
    for m in mons:
        mono = {m: Fraction(1)}
        cols.append(pmul(padd(pmul(derive(mono, d, N), B),
                              pscale(pmul(mono, DB), -1)) or {m: Fraction(0)}, QW))
    B2Q = pmul(B, B, Q)
    for j, v in enumerate(V):
        rest = one
        for k, w in enumerate(V):
            if k != j:
                rest = pmul(rest, w)
        cols.append(pmul(derive(v, d, N) or {tuple([0] * nv): Fraction(0)}, B2Q, rest))
    rhs = pmul(d, P, B, B, W)                                  # @line L6
    z = _solve([clean(c) for c in cols], rhs)                  # @line L7
    if z is None:
        return None
    U = clean({m: z[k] for k, m in enumerate(mons)})
    logs = [(z[len(mons) + j], v) for j, v in enumerate(V) if z[len(mons) + j]]
    return U, B, logs                                          # @line L8
