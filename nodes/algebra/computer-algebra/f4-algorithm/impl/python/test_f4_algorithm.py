# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/f4-algorithm/. The authors are listed in prov/XY5Z26.jsonl.

"""Tests for F4 against a plain Buchberger algorithm (product criterion only).

Each output is also checked by the defining property (every S-polynomial
reduces to zero), by containing the input in its ideal, and by ideal
membership through linear algebra on a Macaulay matrix in bounded degree.
"""

import random
from fractions import Fraction
from typing import Dict, List, Tuple

from f4_algorithm import f4

Mono = Tuple[int, ...]
Poly = Dict[Mono, Fraction]

KEYS = {
    "lex": lambda a: tuple(a),
    "grlex": lambda a: (sum(a),) + tuple(a),
    "grevlex": lambda a: (sum(a),) + tuple(-e for e in reversed(a)),
}


def lead(f: Poly, order: str) -> Mono:
    return max(f, key=KEYS[order])


def sub_scaled(f: Poly, g: Poly, c: Fraction, u: Mono) -> Poly:
    h = dict(f)
    for e, v in g.items():
        e2 = tuple(a + b for a, b in zip(e, u))
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


def buchberger_reduced(F: List[Poly], order: str) -> List[Poly]:
    G = [dict(f) for f in F if f]
    pairs = [(i, j) for j in range(len(G)) for i in range(j)]
    def lcm_degree(p: Tuple[int, int]) -> int:
        a, b = lead(G[p[0]], order), lead(G[p[1]], order)
        return sum(max(x, y) for x, y in zip(a, b))

    while pairs:
        pairs.sort(key=lcm_degree, reverse=True)
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
        if not any(all(x <= y for x, y in zip(lead(h, order), lead(g, order))) for h in minimal):
            minimal.append(g)
    out = []
    for i, g in enumerate(minimal):
        m = lead(g, order)
        tail = {e: v / g[m] for e, v in g.items() if e != m}
        r = remainder(tail, minimal[:i] + minimal[i + 1:], order)
        r[m] = Fraction(1)
        out.append(r)
    return sorted(out, key=lambda g: KEYS[order](lead(g, order)))


def canon(G: List[Poly]) -> List[List[Tuple[Mono, Fraction]]]:
    return sorted(sorted(g.items()) for g in G)


def is_groebner(G: List[Poly], order: str) -> bool:
    return all(not remainder(spoly(G[i], G[j], order), G, order)
               for j in range(len(G)) for i in range(j))


def monomials_upto(n: int, e: int) -> List[Mono]:
    out: List[Mono] = [()]
    for _ in range(n):
        out = [m + (k,) for m in out for k in range(e + 1)]
    return [m for m in out if sum(m) <= e]


def echelon_size(rows: List[Poly]) -> int:
    piv: Dict[Mono, Poly] = {}
    for r in rows:
        r = dict(r)
        while r and max(r) in piv:
            m = max(r)
            q = piv[m]
            r = sub_scaled(r, q, r[m] / q[m], tuple(0 for _ in m))
        if r:
            piv[max(r)] = r
    return len(piv)


def macaulay_rows(G: List[Poly], n: int, e: int) -> List[Poly]:
    rows = []
    for g in G:
        dg = max(sum(m) for m in g)
        if e >= dg:
            for m in monomials_upto(n, e - dg):
                rows.append({tuple(a + b for a, b in zip(k, m)): v for k, v in g.items()})
    return rows


def random_poly(rng: random.Random, n: int, d: int, terms: int) -> Poly:
    f: Poly = {}
    for _ in range(terms):
        m = tuple(rng.randint(0, d) for _ in range(n))
        if sum(m) <= d:
            f[m] = f.get(m, Fraction(0)) + rng.randint(-4, 4)
    return {m: c for m, c in f.items() if c}


def random_system(rng: random.Random, n: int, k: int, dmax: int) -> List[Poly]:
    """k polynomials with 2 to 5 terms, each with a term of its top degree."""
    F = []
    for _ in range(k):
        dd = rng.randint(1, dmax)
        top = [m for m in monomials_upto(n, dd) if sum(m) == dd]
        rest = monomials_upto(n, dd)
        f = {rng.choice(top): Fraction(rng.choice([-2, -1, 1, 2, 3]))}
        for m in rng.sample(rest, min(len(rest), rng.randint(1, 4))):
            f[m] = f.get(m, Fraction(0)) + rng.randint(-3, 3)
        F.append({m: c for m, c in f.items() if c})
    return F


def poly(terms: List[Tuple[Mono, int]]) -> Poly:
    return {m: Fraction(c) for m, c in terms if c}


def check(F: List[Poly], order: str) -> List[Poly]:
    G, _ = f4(F, order)
    assert canon(G) == canon(buchberger_reduced(F, order))
    assert is_groebner(G, order)
    for f in F:
        assert not remainder(f, G, order)
    return G


CYCLIC3 = [poly([((1, 0, 0), 1), ((0, 1, 0), 1), ((0, 0, 1), 1)]),
           poly([((1, 1, 0), 1), ((0, 1, 1), 1), ((1, 0, 1), 1)]),
           poly([((1, 1, 1), 1), ((0, 0, 0), -1)])]


def test_worked_example_circle_hyperbola() -> None:
    F = [poly([((2, 0), 1), ((0, 2), 1), ((0, 0), -4)]), poly([((1, 1), 1), ((0, 0), -1)])]
    G, sizes = f4(F, "grevlex")
    assert G == [poly([((1, 1), 1), ((0, 0), -1)]),
                 poly([((2, 0), 1), ((0, 2), 1), ((0, 0), -4)]),
                 poly([((0, 3), 1), ((1, 0), 1), ((0, 1), -4)])]
    assert sizes == [(2, 4), (4, 5)]


def test_cyclic3_all_orders() -> None:
    for order in KEYS:
        check(CYCLIC3, order)
    G, _ = f4(CYCLIC3, "lex")
    assert canon(G) == canon([poly([((1, 0, 0), 1), ((0, 1, 0), 1), ((0, 0, 1), 1)]),
                              poly([((0, 2, 0), 1), ((0, 1, 1), 1), ((0, 0, 2), 1)]),
                              poly([((0, 0, 3), 1), ((0, 0, 0), -1)])])


def test_edge_cases() -> None:
    assert f4([], "lex") == ([], [])
    assert f4([{}], "grevlex")[0] == []
    one = poly([((0, 0), 1)])
    assert f4([poly([((0, 0), 7)])], "grevlex")[0] == [one]
    assert f4([poly([((1, 0), 1)]), poly([((1, 0), 1), ((0, 0), 1)])], "lex")[0] == [one]
    single = poly([((2, 1), 3), ((0, 1), -6)])
    assert f4([single], "grlex")[0] == [poly([((2, 1), 1), ((0, 1), -2)])]
    assert f4([single, {}], "grlex")[0] == [poly([((2, 1), 1), ((0, 1), -2)])]


def test_many_reduction_steps() -> None:
    F = [poly([((5, 0), 1), ((0, 1), -1)]), poly([((0, 5), 1), ((1, 0), -1), ((0, 0), -1)])]
    G = check(F, "lex")
    assert max(max(m[1] for m in g) for g in G) == 25


def test_random_against_buchberger() -> None:
    rng = random.Random(4)
    for trial in range(520):
        n = rng.choice([2, 2, 3])
        F = random_system(rng, n, rng.randint(2, 3), 3 if n == 2 else 2)
        if trial % 10 == 0:
            F.append(random_poly(rng, n, 2, rng.randint(1, 3)))
        check(F, rng.choice(list(KEYS)))


def test_membership_agrees_with_linear_algebra() -> None:
    rng = random.Random(11)
    for _ in range(150):
        n = 2
        F = random_system(rng, n, 2, 3)
        order = rng.choice(list(KEYS))
        G, _ = f4(F, order)
        Gdeg = buchberger_reduced(F, "grevlex")
        e = max(max(sum(m) for m in g) for g in Gdeg) + 1
        rows = macaulay_rows(Gdeg, n, e)
        p: Poly = {}
        for r in rng.sample(rows, min(3, len(rows))):
            p = sub_scaled(p, r, Fraction(-rng.randint(-3, 3)), (0,) * n)
        if rng.random() < 0.5:
            p = sub_scaled(p, {rng.choice(monomials_upto(n, e)): Fraction(1)}, Fraction(-1), (0,) * n)
        member = echelon_size(rows + [p]) == echelon_size(rows)
        assert (not remainder(p, G, order)) == member
