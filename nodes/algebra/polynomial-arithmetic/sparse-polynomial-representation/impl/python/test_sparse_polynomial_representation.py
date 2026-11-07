# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-polynomial-representation/. The authors are listed in prov/3AC783.jsonl.

import random
from fractions import Fraction

import pytest

import sparse_polynomial_representation as sp


class Fp:
    """An element of Z/pZ, for the tests."""

    __slots__ = ("v", "p")

    def __init__(self, v: int, p: int) -> None:
        self.v = v % p
        self.p = p

    def _c(self, o: object) -> int:
        return o.v if isinstance(o, Fp) else o  # type: ignore[return-value]

    def __add__(self, o: object) -> "Fp":
        return Fp(self.v + self._c(o), self.p)

    __radd__ = __add__

    def __sub__(self, o: object) -> "Fp":
        return Fp(self.v - self._c(o), self.p)

    def __rsub__(self, o: object) -> "Fp":
        return Fp(self._c(o) - self.v, self.p)

    def __mul__(self, o: object) -> "Fp":
        return Fp(self.v * self._c(o), self.p)

    __rmul__ = __mul__

    def __neg__(self) -> "Fp":
        return Fp(-self.v, self.p)

    def __truediv__(self, o: object) -> "Fp":
        return Fp(self.v * pow(self._c(o), -1, self.p), self.p)

    def __rtruediv__(self, o: object) -> "Fp":
        return Fp(self._c(o) * pow(self.v, -1, self.p), self.p)

    def __eq__(self, o: object) -> bool:
        return (self.v - self._c(o)) % self.p == 0

    def __hash__(self) -> int:
        return hash(self.v)

    def __repr__(self) -> str:
        return f"Fp({self.v}, {self.p})"




def strip(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def mul(a, b):
    """Schoolbook product, the reference."""
    if not a or not b:
        return []
    c = [a[0] * 0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] = c[i + j] + x * y
    return strip(c)


def add(a, b):
    n = max(len(a), len(b))
    return strip([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])


def sub(a, b):
    return add(a, [-x for x in b])


PRIMES = [2, 3, 7, 998244353]


def dense_eval(a, x):
    s = x * 0
    for c in reversed(a):
        s = s * x + c
    return s


def rand_sparse(rng, maker, terms, maxexp):
    exps = sorted(rng.sample(range(maxexp + 1), min(terms, maxexp + 1)))
    out = []
    for e in exps:
        c = maker()
        if c != 0:
            out.append((e, c))
    return out


def makers(rng):
    yield "Z", lambda: rng.randint(-5, 5), 1
    yield "Q", lambda: Fraction(rng.randint(-6, 6), rng.randint(1, 4)), Fraction(1)
    for p in PRIMES:
        yield f"F{p}", (lambda p=p: Fp(rng.randrange(p), p)), Fp(1, p)


def test_merge_example_from_page():
    a = [(0, 3), (5, 2), (100, 1)]
    b = [(5, 4), (100, -1), (200, 1)]
    assert sp.add(a, b) == [(0, 3), (5, 6), (200, 1)]


def test_evaluate_example_from_page():
    a = [(0, Fp(3, 7)), (5, Fp(2, 7)), (100, Fp(1, 7))]
    assert sp.evaluate(a, Fp(3, 7), Fp(1, 7)) == 3


def test_product_with_cancellation():
    assert sp.mul([(0, 1), (100, 1)], [(0, -1), (100, 1)]) == [(0, -1), (200, 1)]


def test_zero_and_constants():
    assert sp.add([], []) == []
    assert sp.mul([], [(3, 1)]) == []
    assert sp.mul([(0, 2)], [(0, 3)]) == [(0, 6)]
    assert sp.add([(4, 1)], [(4, -1)]) == []
    assert sp.degree([]) == -1 and sp.degree([(7, 2)]) == 7
    assert sp.evaluate([], 5) == 0
    assert sp.derivative([(0, 9)]) == []
    assert sp.from_dense([0, 0, 0]) == [] and sp.to_dense([]) == []


def test_round_trip_with_leading_zeros():
    assert sp.from_dense([1, 0, 0, 2, 0, 0]) == [(0, 1), (3, 2)]
    assert sp.to_dense([(0, 1), (3, 2)]) == [1, 0, 0, 2]


def test_zero_divisors_drop_terms():
    # over Z/4Z, 2 * (2x + 1) = 2 and the x term vanishes
    a = [(0, Fp(1, 4)), (1, Fp(2, 4))]
    assert sp.scale(a, Fp(2, 4)) == [(0, Fp(2, 4))]
    # characteristic 3: the derivative of x^3 + x is 1
    assert sp.derivative([(1, Fp(1, 3)), (3, Fp(1, 3))]) == [(0, Fp(1, 3))]


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_against_dense_reference(seed):
    rng = random.Random(seed)
    count = 0
    for name, mk, one in makers(rng):
        for _ in range(60):
            a = rand_sparse(rng, mk, rng.randint(0, 6), rng.randint(0, 25))
            b = rand_sparse(rng, mk, rng.randint(0, 6), rng.randint(0, 25))
            assert sp.is_normalized(a) and sp.is_normalized(b)
            da, db = sp.to_dense(a, one * 0), sp.to_dense(b, one * 0)
            assert sp.from_dense(da) == a
            s, p, d = sp.add(a, b), sp.mul(a, b), sp.sub(a, b)
            assert sp.is_normalized(s) and sp.is_normalized(p) and sp.is_normalized(d)
            assert sp.to_dense(s, one * 0) == add(da, db)
            assert sp.to_dense(d, one * 0) == sub(da, db)
            assert sp.to_dense(p, one * 0) == mul(da, db)
            assert sp.add(a, sp.neg(a)) == []
            x = mk()
            assert sp.evaluate(a, x, one) == dense_eval(da, x)
            dd = strip([da[i] * i for i in range(1, len(da))])
            assert sp.to_dense(sp.derivative(a), one * 0) == dd
            count += 1
    assert count >= 360


@pytest.mark.parametrize("p", PRIMES)
def test_huge_exponents_by_evaluation(p):
    rng = random.Random(100 + p)
    one = Fp(1, p)
    for _ in range(60):
        a = rand_sparse(rng, lambda: Fp(rng.randrange(p), p), rng.randint(0, 8), 10**9)
        b = rand_sparse(rng, lambda: Fp(rng.randrange(p), p), rng.randint(0, 8), 10**9)
        x = Fp(rng.randrange(p), p)

        def naive(f):
            return sum((c * pow(x.v, e, p) for e, c in f), Fp(0, p))

        assert sp.evaluate(a, x, one) == naive(a)
        assert sp.evaluate(sp.mul(a, b), x, one) == naive(a) * naive(b)
        assert sp.evaluate(sp.add(a, b), x, one) == naive(a) + naive(b)
        assert sp.is_normalized(sp.mul(a, b)) and sp.is_normalized(sp.add(a, b))


def test_very_different_sizes():
    rng = random.Random(7)
    big = rand_sparse(rng, lambda: rng.randint(1, 9), 40, 200)
    small = [(3, 2)]
    assert sp.to_dense(sp.mul(big, small)) == mul(sp.to_dense(big), sp.to_dense(small))
    assert sp.to_dense(sp.add(big, small)) == add(sp.to_dense(big), sp.to_dense(small))


def test_dense_quotient_of_sparse():
    # (x^n - 1) = (x - 1)(x^(n-1) + ... + 1): a 2-term times an n-term product has 2 terms
    n = 50
    geo = [(i, 1) for i in range(n)]
    assert sp.mul([(0, -1), (1, 1)], geo) == [(0, -1), (n, 1)]
