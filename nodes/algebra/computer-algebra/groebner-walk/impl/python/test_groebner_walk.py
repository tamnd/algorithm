# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/groebner-walk/. The authors are listed in prov/2Y8G4M.jsonl.

"""Tests for the Gröbner walk against Buchberger's algorithm run directly in the target order.

The oracle uses its own order keys (not matrices), its own division and its own
reduced basis. Outputs are also checked by the defining property (every
S-polynomial reduces to zero) and by ideal membership of the input.
"""

import random
from fractions import Fraction
from typing import Dict, List, Tuple

from groebner_walk import groebner_walk, order_matrix

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


def random_poly(rng: random.Random, n: int, d: int, terms: int) -> Poly:
    f: Poly = {}
    for _ in range(terms):
        m = tuple(rng.randint(0, d) for _ in range(n))
        if sum(m) <= d:
            f[m] = f.get(m, Fraction(0)) + rng.randint(-4, 4)
    return {m: c for m, c in f.items() if c}


def walk(F: List[Poly], src: str, dst: str, n: int):
    G = buchberger_reduced(F, src)
    return groebner_walk(G, order_matrix(src, n), order_matrix(dst, n))


def P(*terms) -> Poly:
    return {tuple(e): Fraction(c) for c, e in terms}


def test_order_matrices_agree_with_keys():
    rng = random.Random(1)
    from groebner_walk import key_of
    for n in (1, 2, 3, 4):
        for name in KEYS:
            k = key_of(order_matrix(name, n))
            for _ in range(200):
                a = tuple(rng.randint(0, 4) for _ in range(n))
                b = tuple(rng.randint(0, 4) for _ in range(n))
                assert (k(a) > k(b)) == (KEYS[name](a) > KEYS[name](b))


def test_worked_example():
    # circle and hyperbola, grevlex to lex
    F = [P((1, (2, 0)), (1, (0, 2)), (-4, (0, 0))), P((1, (1, 1)), (-1, (0, 0)))]
    G, path = walk(F, "grevlex", "lex", 2)
    assert canon(G) == canon(buchberger_reduced(F, "lex"))
    assert canon(G) == canon([P((1, (1, 0)), (1, (0, 3)), (-4, (0, 1))),
                              P((1, (0, 4)), (-4, (0, 2)), (1, (0, 0)))])
    assert path == [[1, 1], [3, 1], [1, 0]]


def test_twisted_cubic_positive_dimensional():
    # ideal of the twisted cubic (t, t^2, t^3) in variables x > y > z
    F = [P((1, (0, 1, 0)), (-1, (2, 0, 0))), P((1, (0, 0, 1)), (-1, (3, 0, 0)))]
    for src in KEYS:
        for dst in KEYS:
            G, _ = walk(F, src, dst, 3)
            assert canon(G) == canon(buchberger_reduced(F, dst))


def test_edge_cases():
    for n in (1, 2, 3):
        # unit ideal
        G, _ = walk([P((3, (0,) * n))], "grevlex", "lex", n)
        assert canon(G) == canon([P((1, (0,) * n))])
        # zero ideal
        G, _ = walk([], "grevlex", "lex", n)
        assert G == []
        # a single polynomial
        f = P((2, (1,) + (0,) * (n - 1)), (5, (0,) * (n - 1) + (2,)), (1, (0,) * n))
        G, _ = walk([f], "grevlex", "lex", n)
        assert canon(G) == canon(buchberger_reduced([f], "lex"))
    # same source and target
    F = [P((1, (2, 1)), (-1, (0, 1))), P((1, (1, 2)), (1, (1, 0)))]
    G, path = walk(F, "lex", "lex", 2)
    assert canon(G) == canon(buchberger_reduced(F, "lex"))
    assert path == [[1, 0]]


def test_many_cones():
    # x^5 - y, y^5 - x - 1: lex basis of degree 25, several walls on the path
    F = [P((1, (5, 0)), (-1, (0, 1))), P((1, (0, 5)), (-1, (1, 0)), (-1, (0, 0)))]
    G, path = walk(F, "grevlex", "lex", 2)
    assert canon(G) == canon(buchberger_reduced(F, "lex"))
    assert len(path) >= 3


def random_system(rng: random.Random, n: int, k: int, d: int) -> List[Poly]:
    out = []
    while len(out) < k:
        f = random_poly(rng, n, d, rng.randint(3, 8))
        top = tuple(rng.choice(range(d + 1)) for _ in range(n))
        if sum(top) <= d and sum(top) > 0:
            f[top] = f.get(top, Fraction(0)) + 1
            f = {m: c for m, c in f.items() if c}
        if f:
            out.append(f)
    return out


def weight_order(w: Tuple[int, ...]):
    """Register the weight order w refined by lex in the oracle, and return its matrix."""
    name = "w" + ",".join(map(str, w))
    KEYS[name] = lambda a, w=w: (sum(x * y for x, y in zip(w, a)),) + tuple(a)
    n = len(w)
    return name, [list(w)] + [[1 if j == i else 0 for j in range(n)] for i in range(n)]


def test_weight_matrix_agrees_with_key():
    rng = random.Random(3)
    from groebner_walk import key_of
    for _ in range(50):
        w = tuple(rng.randint(0, 4) for _ in range(3))
        name, M = weight_order(w)
        for _ in range(40):
            a = tuple(rng.randint(0, 4) for _ in range(3))
            b = tuple(rng.randint(0, 4) for _ in range(3))
            assert (key_of(M)(a) > key_of(M)(b)) == (KEYS[name](a) > KEYS[name](b))


def test_random_against_direct_buchberger():
    rng = random.Random(31337)
    walked = 0
    for trial in range(540):
        n = rng.choice((2, 2, 3))
        d = 3 if n == 2 else 2
        k = rng.randint(1, n)
        F = random_system(rng, n, k, d)
        src = rng.choice(("grevlex", "grlex", "lex"))
        Ms = order_matrix(src, n)
        kind = trial % 3
        if kind == 0:
            dst, Mt = "lex", order_matrix("lex", n)
        elif kind == 1:
            dst, Mt = "grevlex", order_matrix("grevlex", n)
        else:
            dst, Mt = weight_order(tuple(rng.randint(1, 5) for _ in range(n)))
        G, path = groebner_walk(buchberger_reduced(F, src), Ms, Mt)
        expected = buchberger_reduced(F, dst)
        assert canon(G) == canon(expected)
        assert is_groebner(G, dst)
        assert all(not remainder(f, G, dst) for f in F)
        assert path[0] == Ms[0] and path[-1] == Mt[0]
        walked += len(path) >= 3
    assert walked >= 80  # 95 with this seed: at least one wall inside the path
