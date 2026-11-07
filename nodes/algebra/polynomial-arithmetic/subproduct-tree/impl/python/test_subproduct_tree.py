# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subproduct-tree/. The authors are listed in prov/1HPPT6.jsonl.

import random
from fractions import Fraction

import pytest

from subproduct_tree import build, combine, evaluate, interpolate


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


def horner(f, x):
    acc = x * 0
    for c in reversed(f):
        acc = acc * x + c
    return acc


def linear_product(us, one):
    m = [one]
    for u in us:
        m = mul(m, [-u, one])
    return m


def lagrange(us, vs):
    """Independent oracle for interpolation over a field."""
    n = len(us)
    out = []
    for j in range(n):
        num = linear_product([us[i] for i in range(n) if i != j], us[0] * 0 + 1)
        den = us[0] * 0 + 1
        for i in range(n):
            if i != j:
                den = den * (us[j] - us[i])
        out = add(out, [c * vs[j] / den for c in num])
    return out


def rings():
    yield "Z", lambda rng: rng.randint(-6, 6), 1
    for p in (2, 3, 7, 998244353):
        yield f"F{p}", (lambda p: lambda rng: Fp(rng.randrange(p), p))(p), Fp(1, p)
    yield "Q", lambda rng: Fraction(rng.randint(-6, 6), rng.randint(1, 4)), Fraction(1)


def test_worked_example():
    t = build([0, 1, 2, 3])
    assert t == [[[0, 1], [-1, 1], [-2, 1], [-3, 1]], [[0, -1, 1], [6, -5, 1]], [[0, -6, 11, -6, 1]]]
    assert evaluate(t, [2, 0, 0, 1]) == [2, 3, 10, 29]
    assert combine(t, [1, 1, 1, 1]) == [-6, 22, -18, 4]
    t5 = build([0, 1, 2, 3, 4])
    assert [len(level) for level in t5] == [5, 3, 2, 1]
    assert t5[-1][0] == [0, 24, -50, 35, -10, 1]
    assert interpolate([Fraction(u) for u in range(4)], [2, 3, 10, 29]) == [2, 0, 0, 1]


def test_edge_cases():
    with pytest.raises(ValueError):
        build([])
    t = build([5])
    assert t == [[[-5, 1]]]
    assert evaluate(t, []) == [0]
    assert evaluate(t, [7]) == [7]
    assert evaluate(t, [1, 1, 1]) == [31]
    assert combine(t, [4]) == [4]
    assert combine(build([1, 2, 3]), [0, 0, 0]) == []
    # Repeated points are allowed in build and evaluate, not in interpolate.
    t = build([2, 2, 2])
    assert t[-1][0] == [-8, 12, -6, 1]
    assert evaluate(t, [0, 0, 1]) == [4, 4, 4]
    with pytest.raises(ZeroDivisionError):
        interpolate([Fraction(1), Fraction(1)], [Fraction(0), Fraction(1)])
    # f of much larger degree than n, and a constant f.
    t = build([1, -1])
    assert evaluate(t, [0] * 40 + [1]) == [1, 1]
    assert evaluate(t, [9]) == [9, 9]


@pytest.mark.parametrize("name,coef,one", list(rings()))
def test_nodes_are_range_products(name, coef, one):
    rng = random.Random(len(name) * 1009)
    for n in range(1, 20):
        us = [coef(rng) for _ in range(n)]
        t = build(us)
        assert len(t) - 1 == (n - 1).bit_length()
        for h, level in enumerate(t):
            assert len(level) == -(-n // 2 ** h)
            for i, node in enumerate(level):
                assert node == linear_product(us[i * 2 ** h:(i + 1) * 2 ** h], one)


@pytest.mark.parametrize("name,coef,one", list(rings()))
def test_evaluate_against_horner(name, coef, one):
    rng = random.Random(len(name) * 7 + 1)
    for _ in range(120):
        n = rng.randint(1, 12)
        us = [coef(rng) for _ in range(n)]
        f = strip([coef(rng) for _ in range(rng.randint(0, 2 * n + 2))])
        assert evaluate(build(us), f) == [horner(f, u) for u in us]


@pytest.mark.parametrize("name,coef,one", list(rings()))
def test_combine_against_direct_sum(name, coef, one):
    rng = random.Random(len(name) * 13 + 5)
    for _ in range(60):
        n = rng.randint(1, 10)
        us = [coef(rng) for _ in range(n)]
        cs = [coef(rng) for _ in range(n)]
        want = []
        for j in range(n):
            want = add(want, [c * cs[j] for c in linear_product(us[:j] + us[j + 1:], one)])
        assert combine(build(us), cs) == want


@pytest.mark.parametrize("p", [7, 998244353, 0])
def test_interpolate_against_lagrange(p):
    rng = random.Random(p + 3)
    for _ in range(80):
        if p:
            n = rng.randint(1, min(p, 10))
            us = [Fp(v, p) for v in rng.sample(range(p), n)]
            vs = [Fp(rng.randrange(p), p) for _ in range(n)]
        else:
            n = rng.randint(1, 9)
            us = [Fraction(v, rng.randint(1, 3)) for v in rng.sample(range(-20, 20), n)]
            us = list(dict.fromkeys(us))
            n = len(us)
            vs = [Fraction(rng.randint(-9, 9)) for _ in range(n)]
        f = interpolate(us, vs)
        assert len(f) <= n
        assert [horner(f, u) for u in us] == vs
        assert f == lagrange(us, vs)
