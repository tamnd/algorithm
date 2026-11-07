# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/groebner-walk/. The authors are listed in prov/2Y8G4M.jsonl.

"""The Gröbner walk of Collart, Kalkbrener and Mall over Q.

Polynomials in Q[x_1, ..., x_n] are dicts from exponent tuples to Fractions.
A monomial order is a matrix order: a list of integer rows, x^a > x^b when the
vector (r . a) for the rows r is lexicographically larger. The first row is the
weight vector of the order and must be nonnegative.

groebner_walk(G, Ms, Mt) takes the reduced Gröbner basis G of an ideal I for the
order Ms and returns (the reduced Gröbner basis of I for Mt, the list of weight
vectors visited). Ideals of any dimension are allowed.

Cost model: operations in Q. Each step costs one Gröbner basis computation for
an ideal of initial forms, one division and one interreduction; the number of
steps is the number of cones of the Gröbner fan met by the segment from the
first row of Ms to the first row of Mt. No useful worst-case bound is known.
"""

from fractions import Fraction
from math import gcd
from typing import Callable, Dict, List, Sequence, Tuple

Mono = Tuple[int, ...]
Poly = Dict[Mono, Fraction]
Matrix = List[List[int]]


def order_matrix(name: str, n: int) -> Matrix:
    """The matrices of lex, grlex and grevlex with x_1 > ... > x_n."""
    unit = [[1 if j == i else 0 for j in range(n)] for i in range(n)]
    if name == "lex":
        return unit
    if name == "grlex":
        return [[1] * n] + unit[: n - 1]
    if name == "grevlex":
        return [[1 if j < n - i else 0 for j in range(n)] for i in range(n)]
    raise ValueError(name)


def dot(w: Sequence[int], a: Mono) -> int:
    return sum(x * y for x, y in zip(w, a))


def key_of(M: Matrix) -> Callable[[Mono], Tuple[int, ...]]:
    return lambda a: tuple(dot(r, a) for r in M)


def lead(f: Poly, M: Matrix) -> Mono:
    return max(f, key=key_of(M))


def divides(a: Mono, b: Mono) -> bool:
    return all(x <= y for x, y in zip(a, b))


def add_multiple(f: Poly, g: Poly, c: Fraction, u: Mono) -> None:
    """f <- f - c x^u g, in place."""
    for e, v in g.items():
        e2 = tuple(x + y for x, y in zip(e, u))
        w = f.get(e2, Fraction(0)) - c * v
        if w:
            f[e2] = w
        else:
            f.pop(e2, None)


def divide(f: Poly, F: List[Poly], M: Matrix) -> Tuple[List[Poly], Poly]:
    """Multivariate division of f by the list F for M: quotients and remainder."""
    key = key_of(M)
    leads = [max(g, key=key) for g in F]
    q: List[Poly] = [{} for _ in F]
    p, r = dict(f), {}
    while p:
        m = max(p, key=key)
        for i, g in enumerate(F):
            if divides(leads[i], m):
                c = p[m] / g[leads[i]]
                u = tuple(y - x for x, y in zip(leads[i], m))
                q[i][u] = q[i].get(u, Fraction(0)) + c
                add_multiple(p, g, c, u)
                break
        else:
            r[m] = p.pop(m)
    return q, r


def reduced_basis(F: List[Poly], M: Matrix) -> List[Poly]:
    """Reduced Gröbner basis for M by Buchberger's algorithm with the product criterion."""
    key = key_of(M)
    G = [dict(f) for f in F if f]
    pairs = [(i, j) for j in range(len(G)) for i in range(j)]
    while pairs:
        pairs.sort(key=lambda p: -sum(max(x, y) for x, y in zip(lead(G[p[0]], M), lead(G[p[1]], M))))
        i, j = pairs.pop()
        a, b = lead(G[i], M), lead(G[j], M)
        if all(x == 0 or y == 0 for x, y in zip(a, b)):
            continue
        l = tuple(max(x, y) for x, y in zip(a, b))
        s: Poly = {}
        add_multiple(s, G[i], -1 / G[i][a], tuple(x - y for x, y in zip(l, a)))
        add_multiple(s, G[j], 1 / G[j][b], tuple(x - y for x, y in zip(l, b)))
        h = divide(s, G, M)[1]
        if h:
            pairs += [(k, len(G)) for k in range(len(G))]
            G.append(h)
    return interreduce(G, M)


def interreduce(G: List[Poly], M: Matrix) -> List[Poly]:
    """Turn a Gröbner basis for M into the reduced one, sorted by leading monomial."""
    key = key_of(M)
    minimal: List[Poly] = []
    for g in sorted(G, key=lambda g: key(lead(g, M))):
        if not any(divides(lead(h, M), lead(g, M)) for h in minimal):
            minimal.append(g)
    out: List[Poly] = []
    for i, g in enumerate(minimal):
        m = lead(g, M)
        tail = {e: v / g[m] for e, v in g.items() if e != m}
        r = divide(tail, minimal[:i] + minimal[i + 1:], M)[1]
        r[m] = Fraction(1)
        out.append(r)
    return sorted(out, key=lambda g: key(lead(g, M)))


def initial_form(g: Poly, w: Sequence[int]) -> Poly:
    top = max(dot(w, e) for e in g)
    return {e: c for e, c in g.items() if dot(w, e) == top}


def primitive(v: Sequence[Fraction]) -> List[int]:
    """Positive multiple of a nonnegative rational vector with coprime integer entries."""
    den = 1
    for x in v:
        den = den * Fraction(x).denominator // gcd(den, Fraction(x).denominator)
    ints = [int(Fraction(x) * den) for x in v]
    g = 0
    for x in ints:
        g = gcd(g, x)
    return [x // g for x in ints] if g else ints


def groebner_walk(G: List[Poly], Ms: Matrix, Mt: Matrix) -> Tuple[List[Poly], List[List[int]]]:
    """Convert the reduced Gröbner basis G for Ms into the reduced basis for Mt.

    Precondition: G is the reduced Gröbner basis of I for Ms, and the first rows
    of Ms and Mt are nonnegative. Cost: one small Gröbner basis per cone crossed.
    """
    w, tau = list(Ms[0]), list(Mt[0])  # @line L1
    M_old = Ms
    G = [dict(g) for g in G]
    path = [list(w)]
    while True:  # @line L2
        M_new = [list(w)] + [list(r) for r in Mt]  # @line L3
        In = [initial_form(g, w) for g in G]
        H = reduced_basis(In, M_new)  # @line L4
        lifted: List[Poly] = []
        for h in H:  # @line L5
            q, r = divide(h, In, M_old)
            assert not r
            hp: Poly = {}
            for qi, g in zip(q, G):
                for u, c in qi.items():
                    add_multiple(hp, g, -c, u)
            lifted.append(hp)
        G = interreduce(lifted, M_new)  # @line L6
        if w == tau:  # @line L7
            return G, path
        u = Fraction(1)  # @line L8
        for g in G:
            a = lead(g, M_new)
            for b in g:
                diff = tuple(x - y for x, y in zip(a, b))
                wt, tt = dot(w, diff), dot(tau, diff)
                if tt < 0:
                    u = min(u, Fraction(wt, wt - tt))
        w = primitive([(1 - u) * x + u * y for x, y in zip(w, tau)])  # @line L9
        if u == 1:
            w = list(tau)
        M_old = M_new
        path.append(list(w))
