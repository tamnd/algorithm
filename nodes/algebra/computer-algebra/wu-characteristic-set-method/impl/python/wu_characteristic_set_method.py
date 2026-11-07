# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wu-characteristic-set-method/. The authors are listed in prov/RYT59J.jsonl.
"""Wu's characteristic set method over a commutative ring R (Z, Q or Z/pZ).

A polynomial in R[x_0, ..., x_{n-1}] is a dict {exponent tuple: coefficient},
with the variable order x_0 < x_1 < ... < x_{n-1}. Only ring operations
(+, -, *) and zero tests on coefficients are used, so the code runs on int,
Fraction or any field element class. Cost model: operations in R; over Z the
coefficients can grow exponentially in the number of reductions.

    charset(P)          -> (C, P') a Ritt-Wu characteristic set of P
    decompose(P)        -> [C_1, ...] with Zero(P) = union of Zero(C_i / I_i)
    wu_prove(H, g)      -> (proved, remainder, nondegeneracy conditions)
"""

from __future__ import annotations


def clean(p):
    return {e: c for e, c in p.items() if c != 0}


def add(p, q, s=1):
    r = dict(p)
    for e, c in q.items():
        r[e] = r.get(e, 0) + c * s
    return clean(r)


def mul(p, q):
    r = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            e = tuple(a + b for a, b in zip(e1, e2))
            r[e] = r.get(e, 0) + c1 * c2
    return clean(r)


def cls(p):
    """Class: index of the main variable, -1 for a constant."""
    return max((i for e in p for i, k in enumerate(e) if k), default=-1)


def deg(p, i):
    return max((e[i] for e in p), default=-1)


def rank(p):
    c = cls(p)
    return (c, deg(p, c) if c >= 0 else 0)


def coeff(p, i, k):
    return {e[:i] + (0,) + e[i + 1:]: c for e, c in p.items() if e[i] == k}


def init(p):
    c = cls(p)
    return coeff(p, c, deg(p, c)) if c >= 0 else dict(p)


def shift(p, i, k):
    return {e[:i] + (e[i] + k,) + e[i + 1:]: c for e, c in p.items()}


def prem(p, q):
    """Pseudo-remainder of p by q in the main variable of q."""
    i = cls(q)
    d, h, r = deg(q, i), init(q), dict(p)
    while r and deg(r, i) >= d:
        k = deg(r, i)
        r = add(mul(h, r), mul(shift(coeff(r, i, k), i, k - d), q), -1)
    return r


def prem_chain(p, C):
    r = dict(p)
    for b in reversed(C):
        if not r:
            break
        r = prem(r, b)
    return r


def reduced(p, C):
    return all(deg(p, cls(b)) < deg(b, cls(b)) for b in C)


def is_constant(C):
    return len(C) == 1 and cls(C[0]) < 0


def basic_set(P):
    """A basic set: an ascending set of lowest rank contained in P."""
    Ps = sorted((p for p in P if p), key=rank)
    if not Ps:
        return []
    if cls(Ps[0]) < 0:
        return [Ps[0]]                       # a nonzero constant
    B = []
    for p in Ps:
        if (not B or cls(p) > cls(B[-1])) and reduced(p, B):
            B.append(p)
    return B


def charset(P):
    """Return (C, P') with C a characteristic set of P and P' = P plus remainders."""
    P = [p for p in P if p]
    while True:                              # @line L1
        B = basic_set(P)                     # @line L2
        if is_constant(B):                   # @line L3
            return B, P
        R = []
        for p in P:                          # @line L4
            if not any(p is b for b in B):
                r = prem_chain(p, B)
                if r and r not in R:
                    R.append(r)
        if not R:                            # @line L5
            return B, P
        P = P + R                            # @line L6


def decompose(P):
    """Wu's zero decomposition: Zero(P) is the union of Zero(C / I_C)."""
    out, stack = [], [[p for p in P if p]]
    while stack:                             # @line D1
        Q = stack.pop()
        C, Q2 = charset(Q)                   # @line D2
        if is_constant(C):                   # @line D3
            continue
        out.append(C)                        # @line D4
        for b in C:                          # @line D5
            h = init(b)
            if cls(h) >= 0:
                stack.append(Q2 + [h])       # @line D6
    return out


def wu_prove(H, g):
    """Prove that g vanishes on Zero(H) where all initials of C are nonzero."""
    C, _ = charset(H)                        # @line W1
    if is_constant(C):
        return True, {}, []                  # the hypotheses have no zeros
    r = prem_chain(g, C)                     # @line W2
    conds = [init(b) for b in C if cls(init(b)) >= 0]
    return (not r), r, conds                 # @line W3
