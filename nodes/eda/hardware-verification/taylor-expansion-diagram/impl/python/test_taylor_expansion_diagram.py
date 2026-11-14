# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/taylor-expansion-diagram/. The authors are listed in prov/B790DF.jsonl.

import random
from fractions import Fraction
from math import factorial

from taylor_expansion_diagram import TED

F = Fraction
VARS = ("a", "b", "c", "d")


# ------------------------------------------------- a reference: dicts of monomials

def p_add(p, q):
    out = dict(p)
    for m, c in q.items():
        out[m] = out.get(m, 0) + c
        if out[m] == 0:
            del out[m]
    return out


def p_mul(p, q):
    out = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            m = tuple(x + y for x, y in zip(m1, m2))
            out[m] = out.get(m, 0) + c1 * c2
            if out[m] == 0:
                del out[m]
    return out


def expand(e, names=VARS):
    n = len(names)
    if isinstance(e, str):
        m = [0] * n
        m[names.index(e)] = 1
        return {tuple(m): F(1)}
    if isinstance(e, (int, Fraction)):
        return {(0,) * n: F(e)} if e else {}
    if e[0] == "^":
        r, base = {(0,) * n: F(1)}, expand(e[1], names)
        for _ in range(e[2]):
            r = p_mul(r, base)
        return r
    a, b = expand(e[1], names), expand(e[2], names)
    if e[0] == "+":
        return p_add(a, b)
    if e[0] == "-":
        return p_add(a, {m: -c for m, c in b.items()})
    return p_mul(a, b)


def random_expr(rng, depth):
    if depth == 0 or rng.random() < 0.25:
        if rng.random() < 0.6:
            return rng.choice(VARS)
        return F(rng.randint(-3, 3), rng.randint(1, 3))
    op = rng.choice("++-**^")
    if op == "^":
        return ("^", random_expr(rng, depth - 1), rng.randint(0, 3))
    return (op, random_expr(rng, depth - 1), random_expr(rng, depth - 1))


def as_sum_of_monomials(p, rng, names=VARS):
    """Another expression of the same polynomial: shuffled monomials and factors."""
    terms = list(p.items())
    rng.shuffle(terms)
    e = 0
    for mono, c in terms:
        factors = [n for n, k in zip(names, mono) for _ in range(k)]
        rng.shuffle(factors)
        t = c
        for x in factors:
            t = ("*", x, t) if rng.random() < 0.5 else ("*", t, x)
        e = ("+", t, e) if rng.random() < 0.5 else ("+", e, t)
    return e


def check_reduced(t):
    seen = set()
    for u, node in enumerate(t.nodes):
        assert node not in seen
        seen.add(node)
        if node[0] != "c":
            v, ch = node
            assert len(ch) >= 2 and ch[-1] != t.zero
            assert all(t.var_level(c) > v for c in ch)


# ----------------------------------------------------------------------- tests

def test_example_of_the_page():
    t = TED(("a", "b"))
    square = t.build(("*", ("+", "a", "b"), ("+", "a", "b")))
    expanded = t.build(("+", ("+", ("*", "a", "a"), ("*", 2, ("*", "a", "b"))), ("*", "b", "b")))
    assert square == expanded
    assert t.size(square) == 6                     # 3 inner nodes, sinks 0, 1, 2
    root = t.nodes[square]
    assert root[0] == 0 and len(root[1]) == 3      # children for k = 0, 1, 2
    assert t.to_poly(root[1][0]) == {(0, 2): 1}    # f(0, b) = b^2
    assert t.to_poly(root[1][1]) == {(0, 1): 2}    # df/da at a = 0 is 2b
    assert root[1][2] == t.one                     # (1/2) d2f/da2 = 1


def test_rational_example():
    t = TED(("x",))
    f = t.build(("*", ("+", "x", F(1, 2)), ("-", "x", F(1, 3))))
    g = t.build(("+", ("+", ("^", "x", 2), ("*", F(1, 6), "x")), F(-1, 6)))
    assert f == g
    assert [t.value(c) for c in t.children(f)] == [F(-1, 6), F(1, 6), F(1)]


def test_datapath_rewrite():
    t = TED(("A", "B", "C"))
    assert t.build(("+", ("*", "A", "B"), ("*", "A", "C"))) == t.build(("*", "A", ("+", "B", "C")))
    assert t.build(("-", ("*", "A", "B"), ("*", "B", "A"))) == t.zero
    assert t.build(("*", "A", "B")) != t.build(("*", "A", "C"))


def test_canonicity_on_random_expressions():
    rng = random.Random(1806)
    for _ in range(300):
        t = TED(VARS)
        e = random_expr(rng, 4)
        p = expand(e)
        u = t.build(e)
        assert t.to_poly(u) == {m: c for m, c in p.items()}
        assert t.build(as_sum_of_monomials(p, rng)) == u
        # A changed coefficient gives another node.
        mono = (rng.randint(0, 2), rng.randint(0, 2), 0, 0)
        q = p_add(p, {mono: F(1, 7)})
        assert t.build(as_sum_of_monomials(q, rng)) != u
        check_reduced(t)


def test_equal_nodes_iff_equal_polynomials():
    rng = random.Random(77)
    t = TED(VARS)
    seen = {}
    for _ in range(400):
        e = random_expr(rng, 3)
        key = tuple(sorted(expand(e).items()))
        u = t.build(e)
        if key in seen:
            assert seen[key] == u
        else:
            assert u not in seen.values()
            seen[key] = u
    assert len(seen) > 100
    check_reduced(t)


def test_children_are_taylor_coefficients():
    rng = random.Random(5)
    for _ in range(100):
        t = TED(VARS)
        p = expand(random_expr(rng, 4))
        u = t.build(as_sum_of_monomials(p, rng))
        if t.is_const(u):
            continue
        v = t.var_level(u)
        for k, c in enumerate(t.children(u)):
            # (1/k!) d^k f / dx_v^k at x_v = 0
            deriv = {}
            for m, q in p.items():
                if m[v] >= k:
                    m2 = list(m)
                    m2[v] -= k
                    deriv[tuple(m2)] = q * factorial(m[v]) / factorial(m[v] - k)
            at_zero = {m: q / factorial(k) for m, q in deriv.items() if m[v] == 0}
            assert t.to_poly(c) == at_zero


def test_evaluate_matches_the_expression():
    rng = random.Random(9)
    for _ in range(200):
        t = TED(VARS)
        e = random_expr(rng, 4)
        u = t.build(e)
        point = {x: F(rng.randint(-5, 5), rng.randint(1, 4)) for x in VARS}
        want = sum((c * prod_pow(point, m) for m, c in expand(e).items()), F(0))
        assert t.evaluate(u, point) == want


def prod_pow(point, mono):
    r = F(1)
    for x, k in zip(VARS, mono):
        r *= point[x] ** k
    return r
