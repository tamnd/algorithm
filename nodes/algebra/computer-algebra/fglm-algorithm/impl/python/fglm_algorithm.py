# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fglm-algorithm/. The authors are listed in prov/FWH4VF.jsonl.

"""FGLM: change of monomial order for a zero-dimensional ideal, over Q.

A polynomial in K[x_1, ..., x_n] is a dict from exponent tuples to nonzero
Fractions. A monomial order is one of "lex", "grlex", "grevlex" with
x_1 > x_2 > ... > x_n.

fglm(G1, order1, order2, n) takes the reduced Groebner basis G1 of a
zero-dimensional ideal I for order1 and returns the reduced Groebner basis
of I for order2, sorted by leading monomial.

Cost model: operations in Q. With D = dim_K K[x]/I (the number of standard
monomials) and n variables, building the multiplication matrices costs n D
normal forms, and the main loop makes at most n D + 1 linear dependency tests
of cost O(D^2) each, so O(n D^3) field operations in total, as in the paper.
"""

from fractions import Fraction
from typing import Callable, Dict, List, Optional, Tuple

Mono = Tuple[int, ...]
Poly = Dict[Mono, Fraction]
Key = Callable[[Mono], Tuple[object, ...]]


def key_lex(a: Mono) -> Tuple[object, ...]:
    return tuple(a)


def key_grlex(a: Mono) -> Tuple[object, ...]:
    return (sum(a),) + tuple(a)


def key_grevlex(a: Mono) -> Tuple[object, ...]:
    return (sum(a),) + tuple(-e for e in reversed(a))


ORDERS: Dict[str, Key] = {"lex": key_lex, "grlex": key_grlex, "grevlex": key_grevlex}


def lm(f: Poly, key: Key) -> Mono:
    return max(f, key=key)


def divides(a: Mono, b: Mono) -> bool:
    return all(x <= y for x, y in zip(a, b))


def mono_mul(a: Mono, b: Mono) -> Mono:
    return tuple(x + y for x, y in zip(a, b))


def mono_div(b: Mono, a: Mono) -> Mono:
    return tuple(y - x for x, y in zip(a, b))


def normal_form(f: Poly, G: List[Poly], key: Key) -> Poly:
    """Remainder of f on division by G (full reduction), iterative."""
    f = dict(f)
    r: Poly = {}
    lms = [(lm(g, key), g) for g in G]
    while f:
        m = lm(f, key)
        c = f[m]
        for gm, g in lms:
            if divides(gm, m):
                q = mono_div(m, gm)
                s = c / g[gm]
                for e, v in g.items():
                    e2 = mono_mul(e, q)
                    w = f.get(e2, Fraction(0)) - s * v
                    if w:
                        f[e2] = w
                    else:
                        f.pop(e2, None)
                break
        else:
            r[m] = c
            del f[m]
    return r


def standard_monomials(G: List[Poly], key: Key, n: int) -> List[Mono]:
    """Monomials not divisible by any LM(g), in increasing order; ValueError if infinite."""
    lms = [lm(g, key) for g in G]
    for i in range(n):
        if not any(all(e == 0 for j, e in enumerate(m) if j != i) for m in lms):
            raise ValueError("the ideal is not zero-dimensional")
    seen = {tuple([0] * n)}
    stack = [tuple([0] * n)]
    if any(divides(m, stack[0]) for m in lms):
        return []
    while stack:
        a = stack.pop()
        for i in range(n):
            b = tuple(e + (1 if j == i else 0) for j, e in enumerate(a))
            if b not in seen and not any(divides(m, b) for m in lms):
                seen.add(b)
                stack.append(b)
    return sorted(seen, key=key)


class Echelon:
    """Incremental row echelon form of vectors in K^D, remembering combinations."""

    def __init__(self, D: int) -> None:
        self.D = D
        self.rows: List[Tuple[int, List[Fraction], List[Fraction]]] = []

    def reduce(self, v: List[Fraction], k: int) -> Tuple[List[Fraction], List[Fraction]]:
        """Reduce v by the stored rows; also return the combination of the k inputs used."""
        v = list(v)
        comb = [Fraction(0)] * k
        for p, row, rc in self.rows:
            c = v[p]
            if c:
                for j in range(self.D):
                    if row[j]:
                        v[j] -= c * row[j]
                for j in range(len(rc)):
                    if rc[j]:
                        comb[j] -= c * rc[j]
        return v, comb

    def add(self, v: List[Fraction], comb: List[Fraction], k: int) -> None:
        """Store reduced v (nonzero) that equals input k plus comb of earlier inputs."""
        p = next(j for j in range(self.D) if v[j])
        inv = 1 / v[p]
        row = [x * inv for x in v]
        rc = [x * inv for x in comb] + [Fraction(0)] * (k + 1 - len(comb))
        rc[k] = inv
        self.rows.append((p, row, rc))


def fglm(G1: List[Poly], order1: str, order2: str, n: int) -> List[Poly]:
    """Reduced Groebner basis for order2 of the ideal with reduced Groebner basis G1 for order1.

    Precondition: G1 is a reduced Groebner basis of a zero-dimensional ideal for order1.
    Cost: O(n D^3) operations in Q, D the number of standard monomials.
    """
    k1, k2 = ORDERS[order1], ORDERS[order2]
    G1 = [g for g in G1 if g]
    if not G1:
        raise ValueError("the zero ideal is not zero-dimensional")
    B1 = standard_monomials(G1, k1, n)  # @line L1
    D = len(B1)
    if D == 0:
        return [{tuple([0] * n): Fraction(1)}]
    index = {b: i for i, b in enumerate(B1)}

    def vec(p: Poly) -> List[Fraction]:
        v = [Fraction(0)] * D
        for e, c in p.items():
            v[index[e]] = c
        return v

    unit = [tuple(1 if j == i else 0 for j in range(n)) for i in range(n)]
    mult = [[vec(normal_form({mono_mul(b, unit[i]): Fraction(1)}, G1, k1)) for b in B1] for i in range(n)]

    def times(i: int, v: List[Fraction]) -> List[Fraction]:
        out = [Fraction(0)] * D
        for j, c in enumerate(v):
            if c:
                col = mult[i][j]
                for r in range(D):
                    if col[r]:
                        out[r] += c * col[r]
        return out

    zero = tuple([0] * n)
    one = vec(normal_form({zero: Fraction(1)}, G1, k1))
    staircase: List[Mono] = []  # @line L2
    vectors: Dict[Mono, List[Fraction]] = {}
    G2: List[Poly] = []
    ech = Echelon(D)
    candidates: Dict[Mono, Tuple[int, Mono]] = {zero: (-1, zero)}
    while candidates:  # @line L3
        m = min(candidates, key=k2)  # @line L4
        i, parent = candidates.pop(m)
        if any(divides(lm(g, k2), m) for g in G2):  # @line L5
            continue
        v = one if i < 0 else times(i, vectors[parent])  # @line L6
        r, comb = ech.reduce(v, len(staircase))
        if not any(r):  # @line L7
            g: Poly = {m: Fraction(1)}
            for j, c in enumerate(comb):
                if c:
                    g[staircase[j]] = c
            G2.append(g)
        else:  # @line L8
            ech.add(r, comb, len(staircase))
            staircase.append(m)
            vectors[m] = v
            for j in range(n):
                nm = mono_mul(m, unit[j])
                if nm not in candidates:
                    candidates[nm] = (j, m)
    return sorted(G2, key=lambda g: k2(lm(g, k2)))  # @line L9
