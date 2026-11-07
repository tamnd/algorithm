# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paterson-stockmeyer-algorithm/. The authors are listed in prov/E2T01W.jsonl.

import random
from fractions import Fraction

import pytest

from paterson_stockmeyer_algorithm import (
    Mat,
    block_size,
    counted_run,
    horner,
    nonscalar_count,
    paterson_stockmeyer,
    trace,
)


class ModP:
    """An element of Z/pZ, enough for the tests."""

    def __init__(self, v: int, p: int) -> None:
        self.p = p
        self.v = v % p

    def _c(self, o):
        return o.v if isinstance(o, ModP) else o

    def __add__(self, o):
        return ModP(self.v + self._c(o), self.p)

    __radd__ = __add__

    def __sub__(self, o):
        return ModP(self.v - self._c(o), self.p)

    def __rsub__(self, o):
        return ModP(self._c(o) - self.v, self.p)

    def __mul__(self, o):
        return ModP(self.v * self._c(o), self.p)

    __rmul__ = __mul__

    def __neg__(self):
        return ModP(-self.v, self.p)

    def __truediv__(self, o):
        d = self._c(o) % self.p
        if d == 0:
            raise ZeroDivisionError
        return ModP(self.v * pow(d, -1, self.p), self.p)

    def __rtruediv__(self, o):
        return ModP(o, self.p) / self

    def __eq__(self, o):
        return self.v == self._c(o) % self.p

    def __hash__(self):
        return hash(self.v)

    def __repr__(self):
        return f"{self.v} mod {self.p}"


# Independent oracles: the sum of a_i x^i with powers formed one by one.


def oracle_scalar(a, x, p=None):
    if p:
        return sum(c * pow(x, i, p) for i, c in enumerate(a)) % p
    return sum(c * x**i for i, c in enumerate(a))


def mat_mul(u, v):
    d = len(u)
    return [[sum(u[i][t] * v[t][j] for t in range(d)) for j in range(d)] for i in range(d)]


def oracle_matrix(a, x, zero, one):
    d = len(x)
    acc = [[zero for _ in range(d)] for _ in range(d)]
    pw = [[one if i == j else zero for j in range(d)] for i in range(d)]
    for c in a:
        acc = [[acc[i][j] + c * pw[i][j] for j in range(d)] for i in range(d)]
        pw = mat_mul(pw, x)
    return acc


PRIMES = [2, 3, 7, 998244353]


def test_page_example():
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert trace(a, 2) == ([1, 2, 4, 8], [17, 38, 59], [59, 510, 4097])
    assert counted_run(a, 2) == (4097, 4, 9)
    assert counted_run(a, 2, method="horner")[:2] == (4097, 8)
    j = Mat([[1, 1], [0, 1]])
    assert paterson_stockmeyer(a, j, Mat.identity(2), scale=Mat.scale) == Mat([[45, 240], [0, 45]])


def test_edge_cases():
    assert paterson_stockmeyer([], 5) == 0
    assert paterson_stockmeyer([7], 5) == 7
    assert paterson_stockmeyer([7, 3], 5) == 22
    assert paterson_stockmeyer([0, 0, 0], 5) == 0
    # leading zero coefficients do not change the value
    assert paterson_stockmeyer([1, 2, 0, 0, 0], 3) == 7
    assert paterson_stockmeyer([2, 0, 0, 1], 0) == 2
    with pytest.raises(ValueError):
        paterson_stockmeyer([1, 2], 3, k=0)
    z = Mat([[0, 0], [0, 0]])
    assert paterson_stockmeyer([], z, Mat.identity(2), scale=Mat.scale) == z
    assert paterson_stockmeyer([4], z, Mat.identity(2), scale=Mat.scale) == Mat([[4, 0], [0, 4]])


def test_over_z_random_and_all_block_sizes():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(0, 60)
        a = [rng.randint(-99, 99) for _ in range(n + 1)]
        x = rng.randint(-5, 5)
        want = oracle_scalar(a, x)
        assert paterson_stockmeyer(a, x) == want
        assert horner(a, x) == want
        k = rng.randint(1, n + 3)
        assert paterson_stockmeyer(a, x, k=k) == want


@pytest.mark.parametrize("p", PRIMES)
def test_over_z_mod_p(p):
    rng = random.Random(p)
    for _ in range(200):
        n = rng.randint(0, 70)
        a = [rng.randrange(p) for _ in range(n + 1)]
        x = rng.randrange(p)
        got = paterson_stockmeyer([ModP(c, p) for c in a], ModP(x, p), ModP(1, p))
        assert got == oracle_scalar(a, x, p)


def test_over_fractions():
    rng = random.Random(5)
    for _ in range(150):
        n = rng.randint(0, 30)
        a = [Fraction(rng.randint(-20, 20), rng.randint(1, 9)) for _ in range(n + 1)]
        x = Fraction(rng.randint(-7, 7), rng.randint(1, 5))
        assert paterson_stockmeyer(a, x, Fraction(1)) == oracle_scalar(a, x)


def test_matrix_argument_over_z_and_mod_p():
    rng = random.Random(11)
    for _ in range(60):
        d = rng.randint(1, 4)
        n = rng.randint(0, 25)
        a = [rng.randint(-9, 9) for _ in range(n + 1)]
        x = [[rng.randint(-2, 2) for _ in range(d)] for _ in range(d)]
        got = paterson_stockmeyer(a, Mat(x), Mat.identity(d), scale=Mat.scale)
        assert got.r == oracle_matrix(a, x, 0, 1)
    for p in PRIMES:
        for _ in range(15):
            d = rng.randint(1, 3)
            n = rng.randint(0, 25)
            a = [ModP(rng.randrange(p), p) for _ in range(n + 1)]
            x = [[ModP(rng.randrange(p), p) for _ in range(d)] for _ in range(d)]
            one, zero = ModP(1, p), ModP(0, p)
            got = paterson_stockmeyer(a, Mat(x), Mat.identity(d, one, zero), scale=Mat.scale)
            assert got.r == oracle_matrix(a, x, zero, one)


def test_matrix_over_fractions():
    rng = random.Random(13)
    for _ in range(20):
        n = rng.randint(0, 15)
        a = [Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(n + 1)]
        x = [[Fraction(rng.randint(-3, 3), rng.randint(1, 3)) for _ in range(2)] for _ in range(2)]
        one, zero = Fraction(1), Fraction(0)
        got = paterson_stockmeyer(a, Mat(x), Mat.identity(2, one, zero), scale=Mat.scale)
        assert got.r == oracle_matrix(a, x, zero, one)


def test_nonscalar_counts():
    for n in range(0, 400):
        k = block_size(n)
        assert (k - 1) ** 2 < n + 1 <= k * k
        a = list(range(1, n + 2))
        v, ns, sc = counted_run(a, 3)
        assert v == oracle_scalar(a, 3)
        assert ns == nonscalar_count(n)
        if n >= 1:
            assert ns <= 2 * k - 2
        assert sc <= n + 1 + k
    for n in range(1, 60):
        for k in range(1, n + 3):
            a = [1] * (n + 1)
            assert counted_run(a, 2, k=k)[1] == nonscalar_count(n, k)
    # Horner uses n nonscalar products
    assert counted_run(list(range(101)), 2, method="horner")[1] == 100
    assert counted_run(list(range(101)), 2)[1] == 10 + 9
