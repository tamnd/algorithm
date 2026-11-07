# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regular-chain/. The authors are listed in prov/1VMKVR.jsonl.
"""Regular chains in Q[x_1, ..., x_n] with x_1 < x_2 < ... < x_n.

A polynomial is a dict {exponent tuple: Fraction}. A triangular set is a list
of polynomials with strictly increasing main variables. Operations:
    mvar, init, prem (pseudo-remainder by one polynomial and by a chain),
    iterated resultant, is_regular (p regular modulo sat(T)),
    is_regular_chain, in_saturation (p in sat(T) for a regular chain T).
Cost model: operations in Q. prem by a chain of r polynomials of degree at most
d in their main variables costs a number of polynomial operations polynomial
in d and r, but the sizes of the polynomials can grow exponentially in r.
"""

from __future__ import annotations

from fractions import Fraction as Q


def clean(p):
    return {e: c for e, c in p.items() if c != 0}


def add(p, q, s=1):
    r = dict(p)
    for e, c in q.items():
        r[e] = r.get(e, 0) + s * c
    return clean(r)


def mul(p, q):
    r = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            e = tuple(a + b for a, b in zip(e1, e2))
            r[e] = r.get(e, 0) + c1 * c2
    return clean(r)


def mono(n, i, k, c=1):
    e = [0] * n
    e[i] = k
    return {tuple(e): Q(c)}


def mvar(p):
    """Index of the largest variable in p, or -1 for constants."""
    return max((i for e in p for i, k in enumerate(e) if k), default=-1)


def deg(p, i):
    return max((e[i] for e in p), default=-1)


def coeff(p, i, k):
    """Coefficient of x_i^k, as a polynomial without x_i."""
    out = {}
    for e, c in p.items():
        if e[i] == k:
            out[e[:i] + (0,) + e[i + 1:]] = c
    return out


def init(p):
    """Leading coefficient of p in its main variable."""
    i = mvar(p)
    return coeff(p, i, deg(p, i)) if i >= 0 else dict(p)


def prem(p, q):
    """Pseudo-remainder of p by q in the main variable of q."""
    i = mvar(q)
    d, h = deg(q, i), init(q)
    n = len(next(iter(q)))
    r = dict(p)
    while r and deg(r, i) >= d:
        k = deg(r, i)
        lead = mul(coeff(r, i, k), mono(n, i, k - d))
        r = add(mul(h, r), mul(lead, q), -1)
    return r


def prem_chain(p, T):
    """prem(p, T): reduce by T_r, ..., T_1 in turn (top variable first)."""
    r = dict(p)
    for t in reversed(T):  # @line L1
        if not r:
            break
        r = prem(r, t)     # @line L2
    return r


def exact_div(a, b):
    """a / b when b divides a exactly."""
    if len(b) == 1:
        (lb, c), = b.items()
        return {tuple(x - y for x, y in zip(e, lb)): v / c for e, v in a.items()}
    key = lambda e: e[::-1]
    lb = max(b, key=key)
    q, a = {}, dict(a)
    while a:
        la = max(a, key=key)
        e = tuple(x - y for x, y in zip(la, lb))
        assert min(e) >= 0, "not divisible"
        t = {e: a[la] / b[lb]}
        q = add(q, t)
        a = add(a, mul(t, b), -1)
    return q


def resultant(p, q, i):
    """Resultant in x_i, by the Sylvester matrix and fraction-free elimination."""
    dp, dq = deg(p, i), deg(q, i)
    if dp <= 0 or dq <= 0:  # a factor without x_i: res = p^dq or q^dp
        base, k = (p, dq) if dp <= 0 else (q, dp)
        n = len(next(iter(base))) if base else 0
        r = {(0,) * n: Q(1)} if n else {}
        for _ in range(max(k, 0)):
            r = mul(r, base)
        return r if base else {}
    N = dp + dq
    cp = [coeff(p, i, k) for k in range(dp, -1, -1)]
    cq = [coeff(q, i, k) for k in range(dq, -1, -1)]
    M = [[{} for _ in range(N)] for _ in range(N)]
    for r in range(dq):
        for j, c in enumerate(cp):
            M[r][r + j] = c
    for r in range(dp):
        for j, c in enumerate(cq):
            M[dq + r][r + j] = c
    n = len(next(iter(p)))
    prev, sign = {(0,) * n: Q(1)}, 1
    for k in range(N - 1):  # Bareiss
        piv = next((r for r in range(k, N) if M[r][k]), None)
        if piv is None:
            return {}
        if piv != k:
            M[k], M[piv] = M[piv], M[k]
            sign = -sign
        for r in range(k + 1, N):
            for j in range(k + 1, N):
                M[r][j] = exact_div(add(mul(M[k][k], M[r][j]), mul(M[r][k], M[k][j]), -1), prev)
            M[r][k] = {}
        prev = M[k][k]
    det = M[N - 1][N - 1]
    return {e: sign * c for e, c in det.items()}


def iterated_resultant(p, T):
    r = dict(p)
    for t in reversed(T):
        if not r:
            break
        i = mvar(t)
        if deg(r, i) > 0:
            r = resultant(r, t, i)
    return r


def is_regular(p, T):
    """True when p is neither zero nor a zero divisor modulo sat(T); T a regular chain."""
    r = prem_chain(p, T)                      # @line R1
    if not r:
        return False
    return bool(iterated_resultant(r, T))     # @line R2


def is_regular_chain(T):
    vs = [mvar(t) for t in T]
    if any(v < 0 for v in vs) or any(a >= b for a, b in zip(vs, vs[1:])):
        return False                          # @line R3
    for k in range(1, len(T)):                # @line R4
        if not is_regular(init(T[k]), T[:k]):  # @line R5
            return False
    return True


def in_saturation(p, T):
    """p in sat(T) = (T) : h^infinity, for a regular chain T."""
    return not prem_chain(p, T)               # @line L3
