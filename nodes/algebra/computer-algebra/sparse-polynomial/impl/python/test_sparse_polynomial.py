# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-polynomial/. The authors are listed in prov/28C10S.jsonl.

import random
from fractions import Fraction

import pytest

from sparse_polynomial import ORDERS, SparsePolynomial


def naive_mul(f: dict, g: dict) -> dict:
    out: dict = {}
    for a, c in f.items():
        for b, d in g.items():
            m = tuple(x + y for x, y in zip(a, b))
            out[m] = out.get(m, 0) + c * d
    return {m: c for m, c in out.items() if c != 0}


def naive_add(f: dict, g: dict) -> dict:
    out = dict(f)
    for a, c in g.items():
        out[a] = out.get(a, 0) + c
    return {m: c for m, c in out.items() if c != 0}


def rand_poly(rng: random.Random, n: int, order: str, terms: int, deg: int) -> SparsePolynomial:
    ts = []
    for _ in range(terms):
        a = tuple(rng.randint(0, deg) for _ in range(n))
        ts.append((a, rng.randint(-3, 3)))
    return SparsePolynomial(n, order, ts)


def test_example() -> None:
    f = SparsePolynomial(2, "grlex", [((1, 0), 1), ((0, 1), 1), ((0, 0), 1)])
    g = SparsePolynomial(2, "grlex", [((1, 0), 1), ((0, 1), -1), ((0, 0), 2)])
    h = f.mul(g)
    assert h.terms == [((2, 0), 1), ((0, 2), -1), ((1, 0), 3), ((0, 1), 1), ((0, 0), 2)]
    assert h.check_invariant()


def test_orders() -> None:
    # x^2 y versus x y^3 and x z^2 versus y^3: the standard distinctions.
    t = [((2, 1, 0), 1), ((1, 3, 0), 1), ((1, 0, 2), 1), ((0, 3, 0), 1)]
    lex = SparsePolynomial(3, "lex", t).terms
    grlex = SparsePolynomial(3, "grlex", t).terms
    grevlex = SparsePolynomial(3, "grevlex", t).terms
    assert [a for a, _ in lex] == [(2, 1, 0), (1, 3, 0), (1, 0, 2), (0, 3, 0)]
    assert [a for a, _ in grlex] == [(1, 3, 0), (2, 1, 0), (1, 0, 2), (0, 3, 0)]
    assert [a for a, _ in grevlex] == [(1, 3, 0), (2, 1, 0), (0, 3, 0), (1, 0, 2)]


def test_edges() -> None:
    z = SparsePolynomial(2, "lex")
    one = SparsePolynomial(2, "lex", [((0, 0), 1)])
    f = SparsePolynomial(2, "lex", [((3, 1), 5), ((0, 2), -1)])
    assert z.mul(f).is_zero() and f.mul(z).is_zero()
    assert one.mul(f).terms == f.terms
    assert f.sub(f).is_zero()
    assert f.add(z).terms == f.terms
    assert f.leading_term() == ((3, 1), 5)
    with pytest.raises(ValueError):
        z.leading_term()
    # cancellation inside the product: (x - y)(x + y) = x^2 - y^2
    p = SparsePolynomial(2, "lex", [((1, 0), 1), ((0, 1), -1)])
    q = SparsePolynomial(2, "lex", [((1, 0), 1), ((0, 1), 1)])
    assert p.mul(q).to_dict() == {(2, 0): 1, (0, 2): -1}
    # like terms in the constructor are combined, zeros dropped
    r = SparsePolynomial(1, "lex", [((1,), 2), ((1,), -2), ((0,), 3)])
    assert r.terms == [((0,), 3)]


def test_random_against_dict_model() -> None:
    rng = random.Random(28)
    for trial in range(600):
        order = rng.choice(list(ORDERS))
        n = rng.randint(1, 3)
        f = rand_poly(rng, n, order, rng.randint(0, 6), 3)
        g = rand_poly(rng, n, order, rng.randint(0, 6), 3)
        h = f.mul(g)
        assert h.check_invariant()
        assert h.to_dict() == naive_mul(f.to_dict(), g.to_dict())
        s = f.add(g)
        assert s.check_invariant() and s.to_dict() == naive_add(f.to_dict(), g.to_dict())
        a = tuple(rng.randint(0, 2) for _ in range(n))
        mt = f.mul_term(a, 3)
        assert mt.check_invariant() and mt.to_dict() == naive_mul(f.to_dict(), {a: 3})
        if not h.is_zero():
            # the leading term of a product is the product of the leading terms
            (a1, c1), (a2, c2) = f.leading_term(), g.leading_term()
            assert h.leading_term() == (tuple(x + y for x, y in zip(a1, a2)), c1 * c2)
        pt = [Fraction(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(n)]
        assert h.evaluate(pt) == f.evaluate(pt) * g.evaluate(pt)


def test_modular_coefficients() -> None:
    p = 7

    class Fp:
        def __init__(self, v: int) -> None:
            self.v = v % p

        def __add__(self, o: "Fp") -> "Fp":
            return Fp(self.v + o.v)

        def __mul__(self, o: "Fp") -> "Fp":
            return Fp(self.v * o.v)

        def __neg__(self) -> "Fp":
            return Fp(-self.v)

        def __eq__(self, o: object) -> bool:
            return self.v == (o.v if isinstance(o, Fp) else o % p)

        def __ne__(self, o: object) -> bool:
            return not self == o

    # (x + 1)^7 = x^7 + 1 over Z/7Z: all middle terms cancel in the heap.
    f = SparsePolynomial(1, "lex", [((1,), Fp(1)), ((0,), Fp(1))])
    h = f
    for _ in range(6):
        h = h.mul(f)
    assert [(a, c.v) for a, c in h.terms] == [((7,), 1), ((0,), 1)]
