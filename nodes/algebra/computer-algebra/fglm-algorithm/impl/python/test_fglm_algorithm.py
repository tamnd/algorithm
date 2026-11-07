# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fglm-algorithm/. The authors are listed in prov/FWH4VF.jsonl.

"""Tests for FGLM against Buchberger's algorithm run directly in the target order.

The oracle is an independent Buchberger implementation with reduced-basis
post-processing. Each output is also checked by the defining property (every
S-polynomial reduces to zero) and by ideal membership through linear algebra
in bounded degree, using the degree-order basis as a Macaulay matrix.
"""

import random
from fractions import Fraction
from typing import Dict, List, Tuple

import pytest

from fglm_algorithm import fglm

Mono = Tuple[int, ...]
Poly = Dict[Mono, Fraction]

KEYS = {
    "lex": lambda a: tuple(a),
    "grlex": lambda a: (sum(a),) + tuple(a),
    "grevlex": lambda a: (sum(a),) + tuple(-e for e in reversed(a)),
}


def lead(f: Poly, order: str) -> Mono:
    return max(f, key=KEYS[order])


def sub_scaled(f: Poly, g: Poly, c: Fraction, shift: Mono) -> Poly:
    h = dict(f)
    for e, v in g.items():
        e2 = tuple(a + b for a, b in zip(e, shift))
        w = h.get(e2, Fraction(0)) - c * v
        if w:
            h[e2] = w
        else:
            h.pop(e2, None)
    return h


def remainder(f: Poly, G: List[Poly], order: str) -> Poly:
    p, r = dict(f), {}
    while p:
        m = lead(p, order)
        for g in G:
            gm = lead(g, order)
            if all(x <= y for x, y in zip(gm, m)):
                p = sub_scaled(p, g, p[m] / g[gm], tuple(y - x for x, y in zip(gm, m)))
                break
        else:
            r[m] = p.pop(m)
    return r


def spoly(f: Poly, g: Poly, order: str) -> Poly:
    a, b = lead(f, order), lead(g, order)
    l = tuple(max(x, y) for x, y in zip(a, b))
    s = sub_scaled({}, f, -1 / f[a], tuple(x - y for x, y in zip(l, a)))
    return sub_scaled(s, g, 1 / g[b], tuple(x - y for x, y in zip(l, b)))


def reduced_basis(F: List[Poly], order: str) -> List[Poly]:
    G = [dict(f) for f in F if f]
    pairs = [(i, j) for j in range(len(G)) for i in range(j)]
    while pairs:
        i, j = pairs.pop()
        a, b = lead(G[i], order), lead(G[j], order)
        if all(x == 0 or y == 0 for x, y in zip(a, b)):
            continue
        h = remainder(spoly(G[i], G[j], order), G, order)
        if h:
            pairs += [(k, len(G)) for k in range(len(G))]
            G.append(h)
    minimal: List[Poly] = []
    for g in sorted(G, key=lambda g: KEYS[order](lead(g, order))):
        m = lead(g, order)
        if not any(all(x <= y for x, y in zip(lead(h, order), m)) for h in minimal):
            minimal.append(g)
    out = []
    for i, g in enumerate(minimal):
        m = lead(g, order)
        tail = {e: v / g[m] for e, v in g.items() if e != m}
        r = remainder(tail, minimal[:i] + minimal[i + 1:], order)
        r[m] = Fraction(1)
        out.append(r)
    return sorted(out, key=lambda g: KEYS[order](lead(g, order)))


def same(A: List[Poly], B: List[Poly]) -> bool:
    return sorted(sorted(g.items()) for g in A) == sorted(sorted(g.items()) for g in B)


def is_groebner(G: List[Poly], order: str) -> bool:
    return all(not remainder(spoly(G[i], G[j], order), G, order)
               for j in range(len(G)) for i in range(j))


def monomials_upto(n: int, e: int) -> List[Mono]:
    out: List[Mono] = [()]
    for _ in range(n):
        out = [m + (k,) for m in out for k in range(e + 1)]
    return [m for m in out if sum(m) <= e]


def echelon(rows: List[Poly]) -> List[Poly]:
    piv: List[Tuple[Mono, Poly]] = []
    for r in rows:
        r = dict(r)
        for m, q in piv:
            if m in r:
                r = sub_scaled(r, q, r[m] / q[m], tuple(0 for _ in m))
        if r:
            piv.append((max(r), r))
    return [q for _, q in piv]


def macaulay_rows(G: List[Poly], n: int, e: int) -> List[Poly]:
    rows = []
    for g in G:
        dg = max(sum(m) for m in g)
        for m in monomials_upto(n, e - dg) if e >= dg else []:
            rows.append({tuple(a + b for a, b in zip(k, m)): v for k, v in g.items()})
    return rows


def member_linear_algebra(p: Poly, basis_rows: List[Poly]) -> bool:
    return len(echelon(basis_rows + [p])) == len(echelon(basis_rows))


def random_poly(rng: random.Random, n: int, d: int, terms: int) -> Poly:
    f: Poly = {}
    for _ in range(terms):
        m = tuple(rng.randint(0, d) for _ in range(n))
        if sum(m) <= d:
            c = Fraction(rng.randint(-4, 4))
            if c:
                f[m] = f.get(m, Fraction(0)) + c
    return {m: c for m, c in f.items() if c}


def random_zero_dim(rng: random.Random, n: int, dmax: int) -> List[Poly]:
    """x_i^(d_i) + lower total degree terms, which is zero-dimensional; maybe one extra generator."""
    F = []
    for i in range(n):
        d = rng.randint(1, dmax)
        f = random_poly(rng, n, d - 1, rng.randint(0, 4))
        e = tuple(d if j == i else 0 for j in range(n))
        f[e] = f.get(e, Fraction(0)) + 1
        F.append({m: c for m, c in f.items() if c})
    if rng.random() < 0.25:
        extra = random_poly(rng, n, dmax, rng.randint(1, 4))
        if extra:
            F.append(extra)
    return F


def poly(terms: List[Tuple[Tuple[int, ...], int]]) -> Poly:
    return {m: Fraction(c) for m, c in terms if c}


def check_conversion(F: List[Poly], o1: str, o2: str, n: int) -> List[Poly]:
    G1 = reduced_basis(F, o1)
    G2 = fglm(G1, o1, o2, n)
    assert same(G2, reduced_basis(F, o2))
    assert is_groebner(G2, o2)
    for g in G2:
        assert not remainder(g, G1, o1)
    return G2


def test_worked_example_circle_hyperbola() -> None:
    F = [poly([((2, 0), 1), ((0, 2), 1), ((0, 0), -4)]), poly([((1, 1), 1), ((0, 0), -1)])]
    G1 = reduced_basis(F, "grevlex")
    assert same(G1, [F[0], F[1], poly([((0, 3), 1), ((1, 0), 1), ((0, 1), -4)])])
    G2 = fglm(G1, "grevlex", "lex", 2)
    assert G2 == [poly([((0, 4), 1), ((0, 2), -4), ((0, 0), 1)]),
                  poly([((1, 0), 1), ((0, 3), 1), ((0, 1), -4)])]


def test_edge_cases() -> None:
    one = poly([((0, 0), 1)])
    assert fglm([one], "grevlex", "lex", 2) == [one]
    single = [poly([((3,), 1), ((0,), -2)])]
    assert fglm(single, "lex", "grevlex", 1) == single
    linear = reduced_basis([poly([((1, 0, 0), 1), ((0, 0, 0), -2)]), poly([((0, 1, 0), 1), ((0, 0, 0), 3)]),
                            poly([((0, 0, 1), 1)])], "grevlex")
    assert same(fglm(linear, "grevlex", "lex", 3), linear)
    with pytest.raises(ValueError):
        fglm([poly([((1, 1), 1), ((0, 0), -1)])], "grevlex", "lex", 2)
    with pytest.raises(ValueError):
        fglm([{}], "grevlex", "lex", 2)


def test_many_reduction_steps() -> None:
    F = [poly([((5, 0), 1), ((0, 1), -1)]), poly([((0, 5), 1), ((1, 0), -1), ((0, 0), -1)])]
    G2 = check_conversion(F, "grevlex", "lex", 2)
    assert max(max(m[1] for m in g) for g in G2) == 25


def test_random_against_buchberger() -> None:
    rng = random.Random(20261107)
    orders = ["lex", "grlex", "grevlex"]
    count = 0
    for trial in range(600):
        n = 2 if trial % 3 else 3
        F = random_zero_dim(rng, n, 4 if n == 2 else 2)
        o1, o2 = rng.choice(orders), rng.choice(orders)
        check_conversion(F, o1, o2, n)
        count += 1
    assert count == 600


def test_membership_agrees_with_linear_algebra() -> None:
    rng = random.Random(7)
    for _ in range(200):
        F = random_zero_dim(rng, 2, 3)
        G1 = reduced_basis(F, "grevlex")
        G2 = fglm(G1, "grevlex", "lex", 2)
        e = max(max(sum(m) for m in g) for g in G1) + 1
        rows = macaulay_rows(G1, 2, e)
        p: Poly = {}
        for r in rng.sample(rows, min(3, len(rows))):
            c = Fraction(rng.randint(-3, 3))
            p = sub_scaled(p, r, -c, (0, 0))
        if rng.random() < 0.5:
            m = rng.choice(monomials_upto(2, e))
            p = sub_scaled(p, {m: Fraction(1)}, Fraction(-1), (0, 0))
        assert (not remainder(p, G2, "lex")) == member_linear_algebra(p, rows)
