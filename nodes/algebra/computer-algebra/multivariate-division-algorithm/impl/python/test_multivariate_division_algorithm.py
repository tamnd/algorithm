# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multivariate-division-algorithm/. The authors are listed in prov/8BTTVF.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from multivariate_division_algorithm import divide, leading_monomial, order_key

ORDERS = ("lex", "grlex", "grevlex")


class GF:
    """The field Z/pZ for a small prime p, used as a second coefficient field."""

    p = 7

    def __init__(self, v: int) -> None:
        self.v = v % GF.p

    def _c(self, o):
        return o if isinstance(o, GF) else GF(o)

    def __add__(self, o):
        return GF(self.v + self._c(o).v)

    __radd__ = __add__

    def __sub__(self, o):
        return GF(self.v - self._c(o).v)

    def __rsub__(self, o):
        return GF(self._c(o).v - self.v)

    def __mul__(self, o):
        return GF(self.v * self._c(o).v)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = self._c(o)
        if o.v == 0:
            raise ZeroDivisionError
        return GF(self.v * pow(o.v, GF.p - 2, GF.p))

    def __eq__(self, o):
        return self.v == self._c(o).v

    def __hash__(self):
        return hash(self.v)


def add(f, g, c=1):
    h = dict(f)
    for m, v in g.items():
        w = h.get(m, 0) + c * v
        if w == 0:
            h.pop(m, None)
        else:
            h[m] = w
    return h


def mul(f, g):
    h = {}
    for a, u in f.items():
        for b, v in g.items():
            m = tuple(x + y for x, y in zip(a, b))
            h[m] = h.get(m, 0) + u * v
    return {m: v for m, v in h.items() if v != 0}


def rand_poly(rng, n, deg, terms, field=Fraction):
    f = {}
    for _ in range(terms):
        e = tuple(rng.randint(0, deg) for _ in range(n))
        c = field(rng.randint(-5, 5))
        f = add(f, {e: c}) if c != 0 else f
    return f


def divides(a, b):
    return all(x <= y for x, y in zip(a, b))


def check_division(f, gs, order, q, r):
    key = order_key(order)
    total = dict(r)
    for qi, gi in zip(q, gs):
        total = add(total, mul(qi, gi))
    assert total == {m: v for m, v in f.items() if v != 0}
    heads = [leading_monomial(g, order) for g in gs]
    for m in r:
        assert not any(divides(h, m) for h in heads)
    if f:
        top = key(leading_monomial(f, order))
        for qi, gi in zip(q, gs):
            prod = mul(qi, gi)
            if prod:
                assert key(leading_monomial(prod, order)) <= top


def F(*pairs):
    return {tuple(e): Fraction(c) for e, c in pairs}


def test_worked_example():
    f = F(((2, 1), 1), ((1, 2), 1), ((0, 2), 1))
    g1 = F(((1, 1), 1), ((0, 0), -1))
    g2 = F(((0, 2), 1), ((0, 0), -1))
    q, r = divide(f, [g1, g2], "lex")
    assert q == [F(((1, 0), 1), ((0, 1), 1)), F(((0, 0), 1),)]
    assert r == F(((1, 0), 1), ((0, 1), 1), ((0, 0), 1))
    q, r = divide(f, [g2, g1], "lex")
    assert q == [F(((1, 0), 1), ((0, 0), 1)), F(((1, 0), 1),)]
    assert r == F(((1, 0), 2), ((0, 0), 1))


def test_cox_little_oshea_first_example():
    f = F(((1, 2), 1), ((0, 0), 1))
    q, r = divide(f, [F(((1, 1), 1), ((0, 0), 1)), F(((0, 1), 1), ((0, 0), 1))], "lex")
    assert q == [F(((0, 1), 1),), F(((0, 0), -1),)]
    assert r == F(((0, 0), 2),)


def test_edges():
    g = F(((1, 0), 1), ((0, 1), -1))
    assert divide({}, [g], "lex") == ([{}], {})
    c = F(((0, 0), 3),)
    q, r = divide(c, [g], "grlex")
    assert q == [{}] and r == c
    f = F(((3, 2), 2), ((1, 0), 5))
    q, r = divide(f, [F(((0, 0), 2),)], "grevlex")
    assert r == {} and q == [F(((3, 2), 1), ((1, 0), Fraction(5, 2)))]
    q, r = divide(f, [], "lex")
    assert q == [] and r == f
    with pytest.raises(ValueError):
        divide(f, [{}], "lex")
    with pytest.raises(ValueError):
        divide(f, [g], "revlex")


def test_many_steps_lex_chain():
    # x1 divided by x1 - x2^b, x2 - x3^b, x3 - x4^b under lex leaves x4^(b^3).
    b = 3
    gs = [
        F(((1, 0, 0, 0), 1), ((0, b, 0, 0), -1)),
        F(((0, 1, 0, 0), 1), ((0, 0, b, 0), -1)),
        F(((0, 0, 1, 0), 1), ((0, 0, 0, b), -1)),
    ]
    f = F(((1, 0, 0, 0), 1),)
    q, r = divide(f, gs, "lex")
    assert r == F(((0, 0, 0, b ** 3), 1),)
    check_division(f, gs, "lex", q, r)


def test_monomial_divisors_oracle():
    rng = random.Random(4417)
    for _ in range(300):
        n = rng.randint(1, 3)
        order = rng.choice(ORDERS)
        gs = [{tuple(rng.randint(0, 3) for _ in range(n)): Fraction(rng.randint(1, 4))} for _ in range(rng.randint(1, 3))]
        f = rand_poly(rng, n, 5, rng.randint(0, 8))
        q, r = divide(f, gs, order)
        heads = [next(iter(g)) for g in gs]
        expect = {m: v for m, v in f.items() if not any(divides(h, m) for h in heads)}
        assert r == expect
        check_division(f, gs, order, q, r)


def test_univariate_oracle():
    rng = random.Random(907)
    for _ in range(300):
        a = [Fraction(rng.randint(-6, 6)) for _ in range(rng.randint(1, 9))]
        b = [Fraction(rng.randint(-6, 6)) for _ in range(rng.randint(1, 5))]
        b[-1] = b[-1] or Fraction(1)
        # schoolbook long division on coefficient lists, lowest degree first
        rem, quo = list(a), [Fraction(0)] * max(1, len(a) - len(b) + 1)
        for k in range(len(a) - len(b), -1, -1):
            c = rem[k + len(b) - 1] / b[-1]
            quo[k] = c
            for j, bj in enumerate(b):
                rem[k + j] -= c * bj
        f = {(i,): c for i, c in enumerate(a) if c != 0}
        g = {(i,): c for i, c in enumerate(b) if c != 0}
        q, r = divide(f, [g], "lex")
        assert r == {(i,): c for i, c in enumerate(rem[: len(b) - 1]) if c != 0}
        assert q[0] == {(i,): c for i, c in enumerate(quo) if c != 0}


def coprime_heads_basis(rng, n, order, field):
    """Random polynomials whose leading monomials are pure powers of distinct
    variables. Their leading monomials are pairwise coprime, so they form a
    Groebner basis (Buchberger's first criterion)."""
    key = order_key(order)
    gs = []
    for v in rng.sample(range(n), rng.randint(1, n)):
        while True:
            e = [0] * n
            e[v] = rng.randint(1, 3)
            head = tuple(e)
            g = {head: field(rng.choice([1, 2, 3, -1]))}
            for _ in range(rng.randint(0, 3)):
                m = tuple(rng.randint(0, 2) for _ in range(n))
                if key(m) < key(head):
                    g = add(g, {m: field(rng.randint(1, 4))})
            if leading_monomial(g, order) == head:
                gs.append(g)
                break
    return gs


@pytest.mark.parametrize("field", [Fraction, GF])
def test_groebner_membership_and_uniqueness(field):
    rng = random.Random(1965 if field is Fraction else 2002)
    for _ in range(250):
        n = rng.randint(1, 3)
        order = rng.choice(ORDERS)
        gs = coprime_heads_basis(rng, n, order, field)
        hs = [rand_poly(rng, n, 2, rng.randint(0, 3), field) for _ in gs]
        f = {}
        for h, g in zip(hs, gs):
            f = add(f, mul(h, g))
        q, r = divide(f, gs, order)
        assert r == {}
        check_division(f, gs, order, q, r)
        f2 = add(f, rand_poly(rng, n, 4, rng.randint(1, 5), field))
        rs = []
        for perm in itertools.permutations(gs):
            q, r = divide(f2, list(perm), order)
            check_division(f2, list(perm), order, q, r)
            rs.append(r)
        assert all(x == rs[0] for x in rs)


@pytest.mark.parametrize("field", [Fraction, GF])
def test_random_properties(field):
    rng = random.Random(31337)
    for _ in range(500):
        n = rng.randint(1, 3)
        order = rng.choice(ORDERS)
        gs = [g for g in (rand_poly(rng, n, 2, rng.randint(1, 3), field) for _ in range(rng.randint(1, 3))) if g]
        f = rand_poly(rng, n, 4, rng.randint(0, 6), field)
        q, r = divide(f, gs, order)
        check_division(f, gs, order, q, r)
