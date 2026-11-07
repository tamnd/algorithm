# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/f5-algorithm/. The authors are listed in prov/2QB464.jsonl.

"""A signature-based Groebner basis algorithm in the style of F5, over Q.

A polynomial in K[x_1, ..., x_n] is a dict from exponent tuples to nonzero
Fractions. A monomial order is one of "lex", "grlex", "grevlex" with
x_1 > x_2 > ... > x_n. Signatures are terms u e_i of the free module R^s,
stored as (i, u), and compared position over term: first by the index i,
then by u in the same monomial order. This is the incremental order of F5.

f5(F, order) returns the reduced Groebner basis of <F> and statistics
{"reductions": ..., "zero_reductions": ...}. The criteria are the F5
(syzygy) criterion with the principal syzygies LM(g) e_i of the earlier
generators, the signatures of reductions to zero, and the rewrite rule that
keeps one candidate per signature and discards singular top-reducible ones.

Cost model: operations in Q. For a homogeneous regular sequence of n
polynomials in grevlex, F5 performs no reduction to zero (Faugere 2002), and
the matrix variant costs O(N^omega) operations, N the number of monomials of
degree at most the degree of regularity (Bardet, Faugere and Salvy 2015). In general the worst case is
doubly exponential in n (Mayr and Meyer 1982).
"""

from fractions import Fraction
from typing import Callable, Dict, List, Set, Tuple

Mono = Tuple[int, ...]
Poly = Dict[Mono, Fraction]
Key = Callable[[Mono], Tuple[object, ...]]
Sig = Tuple[int, Mono]

ORDERS: Dict[str, Key] = {
    "lex": lambda a: tuple(a),
    "grlex": lambda a: (sum(a),) + tuple(a),
    "grevlex": lambda a: (sum(a),) + tuple(-e for e in reversed(a)),
}


def lm(f: Poly, key: Key) -> Mono:
    return max(f, key=key)


def divides(a: Mono, b: Mono) -> bool:
    return all(x <= y for x, y in zip(a, b))


def mmul(a: Mono, b: Mono) -> Mono:
    return tuple(x + y for x, y in zip(a, b))


def mdiv(b: Mono, a: Mono) -> Mono:
    return tuple(y - x for x, y in zip(a, b))


def shift(f: Poly, u: Mono, c: Fraction) -> Poly:
    return {mmul(e, u): c * v for e, v in f.items()}


def axpy(f: Poly, c: Fraction, g: Poly) -> Poly:
    h = dict(f)
    for e, v in g.items():
        w = h.get(e, Fraction(0)) - c * v
        if w:
            h[e] = w
        else:
            h.pop(e, None)
    return h


def reduce_full(f: Poly, G: List[Poly], key: Key) -> Poly:
    p, r = dict(f), {}
    while p:
        m = lm(p, key)
        for g in G:
            gm = lm(g, key)
            if divides(gm, m):
                p = axpy(p, p[m] / g[gm], shift(g, mdiv(m, gm), Fraction(1)))
                break
        else:
            r[m] = p.pop(m)
    return r


def reduced_basis(G: List[Poly], key: Key) -> List[Poly]:
    minimal: List[Poly] = []
    for g in sorted(G, key=lambda g: key(lm(g, key))):
        if not any(divides(lm(h, key), lm(g, key)) for h in minimal):
            minimal.append(g)
    out = []
    for i, g in enumerate(minimal):
        m = lm(g, key)
        tail = {e: v / g[m] for e, v in g.items() if e != m}
        r = reduce_full(tail, minimal[:i] + minimal[i + 1:], key)
        r[m] = Fraction(1)
        out.append(r)
    return sorted(out, key=lambda g: key(lm(g, key)))


def f5(F: List[Poly], order: str) -> Tuple[List[Poly], Dict[str, int]]:
    """Reduced Groebner basis of <F>, with counts of reductions and reductions to zero.

    Precondition: F is a list of polynomials over Q in the same number of variables.
    Cost: doubly exponential in the number of variables in the worst case.
    """
    key = ORDERS[order]

    def skey(s: Sig) -> Tuple[object, ...]:
        return (s[0],) + key(s[1])

    def smul(u: Mono, s: Sig) -> Sig:
        return (s[0], mmul(u, s[1]))

    F = [{e: Fraction(c) for e, c in f.items() if c} for f in F]
    nonzero = [f for f in F if f]
    if not nonzero:
        return [], {"reductions": 0, "zero_reductions": 0}
    n = len(next(iter(nonzero[0])))
    one: Mono = tuple([0] * n)
    B: List[Tuple[Sig, Poly]] = []  # @line L1
    syz: List[Sig] = []
    queue: List[Tuple[Sig, Poly]] = [((i, one), f) for i, f in enumerate(F)]
    handled: Set[Sig] = set()
    stats = {"reductions": 0, "zero_reductions": 0}

    def regular_reduce(sigma: Sig, p: Poly) -> Poly:
        p, r = dict(p), {}
        while p:
            m = lm(p, key)
            for s, g in B:
                gm = lm(g, key)
                if divides(gm, m):
                    t = mdiv(m, gm)
                    if skey(smul(t, s)) < skey(sigma):
                        p = axpy(p, p[m] / g[gm], shift(g, t, Fraction(1)))
                        break
            else:
                r[m] = p.pop(m)
        return r

    def singular_reducible(sigma: Sig, r: Poly) -> bool:
        m = lm(r, key)
        for s, g in B:
            gm = lm(g, key)
            if divides(gm, m) and smul(mdiv(m, gm), s) == sigma:
                return True
        return False

    while queue:  # @line L2
        queue.sort(key=lambda q: skey(q[0]), reverse=True)
        sigma, p = queue.pop()  # @line L3
        if sigma in handled:
            continue
        handled.add(sigma)
        i, u = sigma
        if u == one:  # @line L4
            for s, g in B:
                if s[0] < i:
                    syz.append((i, lm(g, key)))
        if any(t[0] == i and divides(t[1], u) for t in syz):  # @line L5
            continue
        stats["reductions"] += 1
        r = regular_reduce(sigma, p)  # @line L6
        if not r:  # @line L7
            stats["zero_reductions"] += 1
            syz.append(sigma)
            continue
        if singular_reducible(sigma, r):  # @line L8
            continue
        rm = lm(r, key)
        for s, g in B:  # @line L9
            gm = lm(g, key)
            l = tuple(max(a, b) for a, b in zip(rm, gm))
            ur, ug = mdiv(l, rm), mdiv(l, gm)
            sr, sg = smul(ur, sigma), smul(ug, s)
            if sr == sg:
                continue
            spoly = axpy(shift(r, ur, 1 / r[rm]), 1 / g[gm], shift(g, ug, Fraction(1)))
            top = sr if skey(sr) > skey(sg) else sg
            if top not in handled:
                queue.append((top, spoly))
        B.append((sigma, r))  # @line L10
    return reduced_basis([g for _, g in B], key), stats  # @line L11
