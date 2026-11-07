# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/faddeev-leverrier-algorithm/. The authors are listed in prov/6P3FW5.jsonl.

import random
from fractions import Fraction
from itertools import combinations, permutations

import pytest

from faddeev_leverrier_algorithm import adjugate, characteristic_polynomial, determinant, faddeev_leverrier, inverse


def det_leibniz(a):
    n = len(a)
    total = 0
    for p in permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
        t = 1
        for i in range(n):
            t *= a[p[i]][i]
        total += -t if inv % 2 else t
    return total


def charpoly_minors(a):
    n = len(a)
    out = [1]
    for k in range(1, n + 1):
        e = sum(det_leibniz([[a[i][j] for j in s] for i in s]) for s in combinations(range(n), k))
        out.append((-1) ** k * e)
    return out


def adj_cofactors(a):
    n = len(a)
    if n == 1:
        return [[1]]
    return [[(-1) ** (i + k) * det_leibniz([[a[r][c] for c in range(n) if c != i] for r in range(n) if r != k])
             for k in range(n)] for i in range(n)]


class ModP:
    P = 101

    def __init__(self, v: int) -> None:
        self.v = v % ModP.P

    def __add__(self, o):
        return ModP(self.v + (o.v if isinstance(o, ModP) else o))

    __radd__ = __add__

    def __mul__(self, o):
        return ModP(self.v * (o.v if isinstance(o, ModP) else o))

    __rmul__ = __mul__

    def __neg__(self):
        return ModP(-self.v)

    def __truediv__(self, k: int):
        if k % ModP.P == 0:
            raise ZeroDivisionError("k is not invertible modulo P")
        return ModP(self.v * pow(k, -1, ModP.P))

    def __eq__(self, o):
        return self.v == (o.v if isinstance(o, ModP) else o % ModP.P)


def test_example() -> None:
    m = [[2, 1, 0], [1, 3, 1], [0, 1, 4]]
    c, mn = faddeev_leverrier(m)
    assert c == [1, -9, 24, -18]
    assert mn == [[11, -4, 1], [-4, 8, -2], [1, -2, 5]]
    assert inverse(m) == [[Fraction(x, 18) for x in row] for row in mn]


def test_edges() -> None:
    assert faddeev_leverrier([]) == ([1], [])
    assert determinant([]) == 1 and inverse([]) == []
    assert characteristic_polynomial([[5]]) == [1, -5]
    assert adjugate([[5]]) == [[1]]
    assert inverse([[0]]) is None
    assert characteristic_polynomial([[0, 1], [0, 0]]) == [1, 0, 0]
    assert inverse([[1, 2], [2, 4]]) is None


def test_random_integer() -> None:
    rng = random.Random(1840)
    for _ in range(600):
        n = rng.randint(1, 5)
        a = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)]
        if rng.random() < 0.2:
            a[rng.randrange(n)] = [0] * n
        if rng.random() < 0.15:
            for i in range(n):
                a[i][rng.randrange(n)] = 0
        assert characteristic_polynomial(a) == charpoly_minors(a)
        assert determinant(a) == det_leibniz(a)
        assert adjugate(a) == adj_cofactors(a)
        inv = inverse(a)
        if det_leibniz(a) == 0:
            assert inv is None
        else:
            prod = [[sum(a[i][t] * inv[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
            assert prod == [[int(i == j) for j in range(n)] for i in range(n)]


def test_rational_entries() -> None:
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randint(1, 4)
        a = [[Fraction(rng.randint(-6, 6), rng.randint(1, 5)) for _ in range(n)] for _ in range(n)]
        assert characteristic_polynomial(a) == charpoly_minors(a)


def test_mod_p_large_characteristic() -> None:
    rng = random.Random(4)
    for _ in range(150):
        n = rng.randint(1, 5)
        a = [[rng.randrange(101) for _ in range(n)] for _ in range(n)]
        got = characteristic_polynomial([[ModP(x) for x in row] for row in a])
        assert all(g == e for g, e in zip(got, charpoly_minors(a)))


def test_small_characteristic_fails() -> None:
    ModP.P = 2
    try:
        with pytest.raises(ZeroDivisionError):
            characteristic_polynomial([[ModP(1), ModP(1)], [ModP(1), ModP(0)]])
    finally:
        ModP.P = 101


def test_large_entries() -> None:
    rng = random.Random(5)
    for _ in range(10):
        n = 5
        a = [[rng.randint(-10**20, 10**20) for _ in range(n)] for _ in range(n)]
        assert characteristic_polynomial(a) == charpoly_minors(a)
