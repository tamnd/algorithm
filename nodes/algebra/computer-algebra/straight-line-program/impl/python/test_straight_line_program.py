# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/straight-line-program/. The authors are listed in prov/JGQ9GZ.jsonl.
"""Tests for straight-line programs.

The reference is the expanded polynomial: values, degrees and derivatives of
the program must agree with those of its expansion, in exact integer,
rational and modular arithmetic.
"""

import random
from fractions import Fraction

import pytest

from straight_line_program import (SLP, compose, degree_bound, evaluate, expand,
                                   gradient, is_zero)

P = 1_000_000_007


def random_slp(rng, n, L, consts=(-3, 3), max_deg=6):
    """A random program; products are kept to total degree max_deg so it expands fast."""
    g = SLP(n)
    for i in range(n):
        g.var(i)
    g.const(rng.randint(*consts))
    deg = [1] * n + [0]
    while len(g) < L:
        a, b = rng.randrange(len(g)), rng.randrange(len(g))
        o = rng.choice("+-*+*")
        if o == "*" and deg[a] + deg[b] > max_deg:
            o = "+"
        g.op(o, a, b)
        deg.append(deg[a] + deg[b] if o == "*" else max(deg[a], deg[b]))
    return g


def peval(f, pt, p=None):
    s = 0
    for e, c in f.items():
        v = c
        for x, k in zip(pt, e):
            v *= x ** k
        s += v
    return s % p if p is not None else s


def pdiff(f, i):
    out = {}
    for e, c in f.items():
        if e[i]:
            e2 = list(e)
            e2[i] -= 1
            out[tuple(e2)] = out.get(tuple(e2), 0) + c * e[i]
    return out


def total_degree(f):
    return max((sum(e) for e in f), default=-1)


@pytest.mark.parametrize("seed", range(8))
def test_against_expansion(seed):
    rng = random.Random(seed)
    for _ in range(25):
        n = rng.randint(1, 3)
        g = random_slp(rng, n, rng.randint(n + 1, n + 9))
        f = expand(g)
        assert degree_bound(g)[-1] >= total_degree(f)
        for _ in range(5):
            pt = [rng.randint(-5, 5) for _ in range(n)]
            assert evaluate(g, pt) == peval(f, pt)
            assert evaluate(g, pt, P) == peval(f, pt, P)
            gr = gradient(g, pt)
            assert gr == [peval(pdiff(f, i), pt) for i in range(n)]
            assert gradient(g, pt, P) == [x % P for x in gr]
        qt = [Fraction(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(n)]
        assert evaluate(g, qt) == peval(f, qt)
        assert gradient(g, qt) == [peval(pdiff(f, i), qt) for i in range(n)]


def test_repeated_squaring():
    k = 60
    g = SLP(1)
    g.var(0)
    for j in range(k):
        g.op("*", j, j)  # x^(2^(j+1))
    assert len(g) == k + 1
    assert degree_bound(g)[-1] == 2 ** k
    rng = random.Random(5)
    for _ in range(20):
        x = rng.randrange(1, P)
        assert evaluate(g, [x], P) == pow(x, 2 ** k, P)
        assert gradient(g, [x], P) == [2 ** k % P * pow(x, 2 ** k - 1, P) % P]
    with pytest.raises(OverflowError):  # (x + 1)^(2^20) has 2^20 + 1 terms
        h = SLP(1)
        h.var(0)
        h.const(1)
        h.op("+", 0, 1)
        for j in range(20):
            h.op("*", 2 + j, 2 + j)
        expand(h, max_terms=100)


def test_zero_test():
    rng = random.Random(9)
    g = SLP(2)  # (x + y)^2 - x^2 - 2 x y - y^2
    x, y = g.var(0), g.var(1)
    s = g.op("+", x, y)
    s2 = g.op("*", s, s)
    xx, yy, xy = g.op("*", x, x), g.op("*", y, y), g.op("*", x, y)
    t = g.op("-", s2, xx)
    t = g.op("-", t, yy)
    t = g.op("-", t, xy)
    g.op("-", t, xy)
    assert expand(g) == {}
    assert is_zero(g, P, rng)
    for seed in range(30):
        r = random.Random(seed)
        h = random_slp(r, 3, 12)
        nonzero = expand(h, P) != {}
        assert is_zero(h, P, rng) == (not nonzero)
        # h - h is zero
        last = len(h) - 1
        h.op("-", last, last)
        assert is_zero(h, P, rng)


def test_compose():
    rng = random.Random(11)
    for _ in range(20):
        m, n = rng.randint(1, 3), rng.randint(1, 3)
        outer = random_slp(rng, m, m + 6)
        inner = [random_slp(rng, n, n + 5) for _ in range(m)]
        c = compose(outer, inner)
        assert len(c) <= len(outer) + sum(map(len, inner)) + 2
        for _ in range(5):
            pt = [rng.randint(-4, 4) for _ in range(n)]
            vals = [evaluate(gi, pt) for gi in inner]
            assert evaluate(c, pt) == evaluate(outer, vals)


def test_edges():
    e = SLP(2)
    assert evaluate(e, [1, 2]) == 0 and gradient(e, [1, 2]) == [0, 0]
    assert expand(e) == {} and degree_bound(e) == []
    c = SLP(2)
    c.const(7)
    assert evaluate(c, [3, 4]) == 7 and gradient(c, [3, 4]) == [0, 0]
    assert expand(c) == {(0, 0): 7} and not is_zero(c, P, random.Random(1))
    z = SLP(1)
    z.const(0)
    assert degree_bound(z) == [-1] and is_zero(z, P, random.Random(1))
    v = SLP(3)
    v.var(2)
    assert gradient(v, [5, 6, 7]) == [0, 0, 1] and expand(v) == {(0, 0, 1): 1}
    w = SLP(1)  # x * 0 has degree bound -1
    w.var(0)
    w.const(0)
    w.op("*", 0, 1)
    assert degree_bound(w)[-1] == -1 and expand(w) == {}
