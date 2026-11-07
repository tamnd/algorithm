# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zeilberger-algorithm/. The authors are listed in prov/8S5NXW.jsonl.
"""Zeilberger's algorithm (fast creative telescoping) over Q.

The summand is a proper hypergeometric term

    F(n, k) = poly(n, k) * x^k * prod_i (a_i n + b_i k + c_i)!^(e_i),

given as poly = {(i, j): c} for c n^i k^j, a rational x != 0 and a list of
(a_i, b_i, c_i, e_i) with integers a_i, b_i, c_i and e_i = +1 or -1. The
algorithm finds the least J >= 0 and polynomials a_0(n), ..., a_J(n), not all
zero, and a rational function R(n, k) with

    sum_j a_j(n) F(n + j, k) = G(n, k + 1) - G(n, k),   G = R F.

Summing over k with natural boundaries gives sum_j a_j(n) S(n + j) = 0 for
S(n) = sum_k F(n, k).

Polynomials in n are lists of Fractions, low degree first. Polynomials in k
with coefficients in Q[n] are lists of such lists. Elements of Q(n) are
pairs (numerator, monic denominator).

Cost model: operations in the field Q(n). For each trial order j <= J the
method solves one linear system with m <= D + J + 2 unknowns, where D is
Gosper's degree bound, by fraction-free Gaussian elimination over Q[n]:
O(m^3) ring operations for each order, O(J m^3) in total (a proved bound). Over Q the cost also
depends on the degrees in n of the entries; it is not bounded here.
Termination for every proper hypergeometric term is the theorem of Wilf and
Zeilberger; max_order only stops the search early.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd, lcm

# ---------- polynomials in n over Q ----------


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def nadd(a, b):
    r = [Fraction(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        r[i] += x
    for i, x in enumerate(b):
        r[i] += x
    return trim(r)


def nneg(a):
    return [-x for x in a]


def nmul(a, b):
    if not a or not b:
        return []
    r = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return trim(r)


def ndivmod(a, b):
    a = trim(a)
    q = [Fraction(0)] * max(len(a) - len(b) + 1, 0)
    while a and len(a) >= len(b):
        c = a[-1] / b[-1]
        s = len(a) - len(b)
        q[s] = c
        for i, y in enumerate(b):
            a[i + s] -= c * y
        a = trim(a)
    return trim(q), a


def ngcd(a, b):
    a, b = trim(a), trim(b)
    while b:
        a, b = b, ndivmod(a, b)[1]
    return [x / a[-1] for x in a] if a else []


def nshift(a, s):
    """a(n + s) by Horner's rule."""
    r = []
    for c in reversed(a):
        r = nadd(nmul(r, [Fraction(s), Fraction(1)]), [c])
    return r


# ---------- Q(n) ----------

ONE = ([Fraction(1)], [Fraction(1)])
ZERO = ([], [Fraction(1)])


def rf(num, den=None):
    den = [Fraction(1)] if den is None else trim(den)
    num = trim(num)
    if not num:
        return ZERO
    g = ngcd(num, den)
    num, den = ndivmod(num, g)[0], ndivmod(den, g)[0]
    lc = den[-1]
    return [x / lc for x in num], [x / lc for x in den]


# ---------- polynomials in k over Q[n] ----------


def kadd(a, b):
    r = [[] for _ in range(max(len(a), len(b)))]
    for i, x in enumerate(a):
        r[i] = nadd(r[i], x)
    for i, x in enumerate(b):
        r[i] = nadd(r[i], x)
    while r and not r[-1]:
        r.pop()
    return r


def kmul(a, b, *more):
    if more:
        return kmul(kmul(a, b), *more)
    if not a or not b:
        return []
    r = [[] for _ in range(len(a) + len(b) - 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] = nadd(r[i + j], nmul(x, y))
    while r and not r[-1]:
        r.pop()
    return r


def kshift(p, s):
    """p(k + s) for an integer or rational s."""
    r = []
    for c in reversed(p):
        r = kadd(kmul(r, [[Fraction(s)], [Fraction(1)]]), [c])
    return r


def linear(u):
    """The monic linear polynomial k + u(n)."""
    return [trim(u), [Fraction(1)]]


def from_dict(poly, j):
    """poly(n + j, k) as a polynomial in k over Q[n]."""
    deg_k = max((e[1] for e in poly), default=-1)
    out = [[] for _ in range(deg_k + 1)]
    for (i, kk), c in poly.items():
        out[kk] = nadd(out[kk], nshift([Fraction(0)] * i + [Fraction(c)], j))
    while out and not out[-1]:
        out.pop()
    return out


# ---------- the term and its Gosper form ----------


def form(a, b, c):
    """a n + b k + c as (constant, monic part u) with a n + b k + c = b (k + u)."""
    return Fraction(b), [Fraction(c, b), Fraction(a, b)]


def setup(poly, x, facts, J):
    """phi_j(k) with F(n + j, k) = H(k) phi_j(k), and H(k+1)/H(k) = q(k)/r(k+1)."""
    phis = [from_dict(poly, j) for j in range(J + 1)]
    num, den, cq, cr = [], [], Fraction(x), Fraction(1)
    for a, b, c, e in facts:
        lo, hi = min(0, a * J), max(0, a * J)
        c0 = c + (lo if e > 0 else hi)  # H holds (a n + b k + c0)!^e
        for j in range(J + 1):
            ls = range(c0 + 1, c + a * j + 1) if e > 0 else range(c + a * j + 1, c0 + 1)
            for l in ls:  # one factor a n + b k + l of the polynomial phi_j
                phis[j] = kmul(phis[j], [[Fraction(l), Fraction(a)], [Fraction(b)]])
        if b == 0:
            continue
        shifts = range(1, b + 1) if b > 0 else range(0, b, -1)
        up = (e > 0) == (b > 0)  # the ratio factors go to the numerator
        for l in shifts:
            const, u = form(a, b, c0 + l)
            if up:
                num.append(u)
                cq *= const
            else:
                den.append(u)
                cr *= const
    return phis, cq, num, cr, den


def gosper_form(num, den):
    """Return q, r, c (monic linear factors) with q(k)/r(k+1) = num/den * c(k)/c(k+1).

    Here num/den = prod (k + u) / prod (k + w); on exit no factor k + u of q
    and k + w of r have u - w a positive integer.
    """
    q = [list(u) for u in num]
    r = [nadd(w, [Fraction(-1)]) for w in den]  # r(k) = den(k - 1)
    cfac = []
    changed = True
    while changed:
        changed = False
        for iq, u in enumerate(q):
            for ir, w in enumerate(r):
                diff = nadd(u, nneg(w))
                h = diff[0] if diff else Fraction(0)
                if len(diff) <= 1 and h.denominator == 1 and h >= 1:
                    cfac += [nadd(u, [Fraction(-i)]) for i in range(1, int(h))]
                    del q[iq], r[ir]
                    changed = True
                    break
            if changed:
                break
    return q, r, cfac


def kprod(factors, const=Fraction(1)):
    p = [[Fraction(const)]]
    for u in factors:
        p = kmul(p, linear(u))
    return p


def degree_bound(q, r, dP):
    """Gosper's bound on deg f for q f(k+1) - r f(k) = P with deg P = dP."""
    dq, dr = len(q) - 1, len(r) - 1
    if dq != dr or q[-1] != r[-1]:
        return dP - max(dq, dr)
    bound = dP - dq + 1
    if dq >= 1:
        s = rf(nadd(r[dq - 1], nneg(q[dq - 1])), q[dq])
        if len(s[0]) <= 1 and s[1] == [1]:
            v = s[0][0] if s[0] else Fraction(0)
            if v.denominator == 1 and v >= 0:
                bound = max(bound, int(v))
    return bound


def primitive(row):
    """Divide a row of polynomials in n by the gcd of its entries."""
    g = []
    for p in row:
        if p:
            g = ngcd(g, p) if g else ngcd(p, [])
    return [ndivmod(p, g)[0] for p in row] if g else row


def nullspace(rows, ncols):
    """A basis of the kernel over Q(n) of a matrix with entries in Q[n].

    Fraction-free Gauss-Jordan elimination: row_i <- p row_i - m row_r,
    then the row is divided by its content, so all entries stay in Q[n].
    """
    M = [primitive([trim(e) for e in row]) for row in rows]
    piv = []
    rr = 0
    for c in range(ncols):
        p = next((i for i in range(rr, len(M)) if M[i][c]), None)
        if p is None:
            continue
        M[rr], M[p] = M[p], M[rr]
        pv = M[rr][c]
        for i in range(len(M)):
            if i != rr and M[i][c]:
                m = M[i][c]
                M[i] = primitive([nadd(nmul(pv, x), nneg(nmul(m, y)))
                                  for x, y in zip(M[i], M[rr])])
        piv.append(c)
        rr += 1
    basis = []
    for free in (c for c in range(ncols) if c not in piv):
        v = [ZERO] * ncols
        v[free] = ONE
        for i, c in enumerate(piv):  # M[i][c] x_c + M[i][free] x_free = 0
            v[c] = rf(nneg(M[i][free]), M[i][c])
        basis.append(v)
    return basis


def zeilberger(poly, x, facts, max_order=4):
    """Return (J, [a_0, ..., a_J], R_num, R_den) or None if no order <= max_order works.

    R = R_num / R_den, both {(i, j): Fraction} for n^i k^j.
    """
    if not any(poly.values()):
        return 0, [[Fraction(1)]], {}, {(0, 0): Fraction(1)}  # F = 0, G = 0
    for J in range(max_order + 1):                              # @line L1
        phis, cq, num, cr, den = setup(poly, x, facts, J)       # @line L2
        qf, rf_, cfac = gosper_form(num, den)                   # @line L3
        q, r, cpol = kprod(qf, cq), kprod(rf_, cr), kprod(cfac)
        cols_a = [kmul(phi, cpol) for phi in phis]              # @line L4
        dP = max(len(p) - 1 for p in cols_a)
        D = degree_bound(q, r, dP)                              # @line L5
        D = max(D, -1)  # D = -1: only f = 0 is possible
        cols = [[nneg(c) for c in col] for col in cols_a]
        for i in range(D + 1):                                  # @line L6
            ki = [[] for _ in range(i)] + [[Fraction(1)]]
            cols.append(kadd(kmul(q, kshift(ki, 1)), [nneg(c) for c in kmul(r, ki)]))
        height = max(len(c) for c in cols)
        rows = [[c[e] if e < len(c) else [] for c in cols] for e in range(height)]
        for v in nullspace(rows, len(cols)):                    # @line L7
            if any(t[0] for t in v[:J + 1]):
                break
        else:
            continue
        # clear denominators: a_j and f_i become polynomials in n
        L = [Fraction(1)]
        for t in v:
            L = ndivmod(nmul(L, t[1]), ngcd(L, t[1]))[0]
        vals = [ndivmod(nmul(t[0], L), t[1])[0] for t in v]
        g = []
        for p in vals[:J + 1]:
            g = ngcd(g, p) if g else ngcd(p, [])
        a = [ndivmod(p, g)[0] for p in vals[:J + 1]]
        f = vals[J + 1:]  # f / g is the true f; g goes to the denominator of R
        # scale by a rational: integer coefficients, content 1, LC(a_J) > 0
        coeffs = [c for p in a for c in p]
        den = lcm(*[c.denominator for c in coeffs])
        num = gcd(*[(c * den).numerator for c in coeffs])
        lead = next(p for p in reversed(a) if p)[-1]
        scale = Fraction(den, num) * (1 if lead > 0 else -1)
        a = [[c * scale for c in p] for p in a]
        f = [[c * scale for c in p] for p in f]
        while f and not f[-1]:
            f.pop()
        # G = R F with R = r(k) f(k) / (g c(k) phi_0(k))
        return J, a, to_dict(kmul(r, f)), to_dict(kmul([g], cpol, phis[0]))  # @line L8
    return None


def to_dict(p):
    return {(i, j): c for j, cn in enumerate(p) for i, c in enumerate(cn) if c}
