# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bostan-mori-algorithm/. The authors are listed in prov/8WEKFW.jsonl.

import random
from fractions import Fraction

import pytest

from bostan_mori_algorithm import bostan_mori, nth_term, schoolbook_mul, series_coefficient_naive


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


# Independent oracles: run the recurrence forward, or power the companion
# matrix by repeated squaring modulo p.


def run_recurrence(c, a, n):
    seq = list(a)
    d = len(c)
    while len(seq) <= n:
        seq.append(sum(c[i] * seq[-1 - i] for i in range(d)))
    return seq[n]


def companion_power_term(c, a, n, p):
    d = len(c)
    if n < d:
        return a[n] % p
    # state (a_i, ..., a_(i+d-1)) -> (a_(i+1), ..., a_(i+d))
    m = [[0] * d for _ in range(d)]
    for i in range(d - 1):
        m[i][i + 1] = 1
    for j in range(d):
        m[d - 1][j] = c[d - 1 - j] % p

    def mm(x, y):
        return [[sum(x[i][t] * y[t][j] for t in range(d)) % p for j in range(d)] for i in range(d)]

    r = [[int(i == j) for j in range(d)] for i in range(d)]
    e = n
    b = m
    while e:
        if e & 1:
            r = mm(r, b)
        b = mm(b, b)
        e >>= 1
    return sum(r[0][j] * a[j] for j in range(d)) % p


PRIMES = [2, 3, 7, 998244353]


def test_page_example():
    steps = []
    assert bostan_mori([0, 1], [1, -1, -1], 10, steps=steps) == 55
    assert steps == [
        (5, [0, 1], [1, -3, 1]),
        (2, [1, 1], [1, -7, 1]),
        (1, [1, 8], [1, -47, 1]),
        (0, [55, 8], [1, -2207, 1]),
    ]
    assert nth_term([1, 1], [0, 1], 90) == 2880067194370816120


def test_edge_cases():
    assert bostan_mori([], [1, 1], 5) == 0
    assert bostan_mori([3], [1], 0) == 3
    assert bostan_mori([3], [1], 4) == 0
    assert bostan_mori([1, 2, 3], [1], 2) == 3
    assert bostan_mori([1, 2, 3], [1, 0, 0], 2) == 3
    assert bostan_mori([1, 2, 3, 0, 0], [1, -1, 0, 0], 7) == 6
    assert bostan_mori([1], [1, -1], 0) == 1
    assert bostan_mori([1], [1, -1], 10**30) == 1
    assert bostan_mori([1], [-1, 1], 3) == -1
    assert bostan_mori([5, 7], [1, -2], -1) == 0
    # numerator of higher degree than the denominator
    p, q = [1, 2, 3, 4, 5, 6, 7], [1, -1, 1]
    for n in range(20):
        assert bostan_mori(p, q, n) == series_coefficient_naive(p, q, n)
    with pytest.raises(ValueError):
        bostan_mori([1], [2, -1], 3)
    with pytest.raises(ZeroDivisionError):
        bostan_mori([1], [0, 0], 3)
    assert nth_term([], [], 5) == 0
    assert nth_term([2], [3], 0) == 3
    assert nth_term([2], [3], 10) == 3 * 2**10
    with pytest.raises(ValueError):
        nth_term([1, 1], [0], 3)


def test_over_z_random():
    rng = random.Random(1)
    for _ in range(300):
        d = rng.randint(1, 8)
        c = [rng.randint(-3, 3) for _ in range(d)]
        a = [rng.randint(-5, 5) for _ in range(d)]
        n = rng.randint(0, 300)
        assert nth_term(c, a, n) == run_recurrence(c, a, n)
        p = [rng.randint(-5, 5) for _ in range(rng.randint(0, d + 3))]
        q = [rng.choice([1, -1])] + [rng.randint(-3, 3) for _ in range(rng.randint(0, d))]
        m = rng.randint(0, 120)
        assert bostan_mori(p, q, m) == series_coefficient_naive(p, q, m)


@pytest.mark.parametrize("p", PRIMES)
def test_over_z_mod_p(p):
    rng = random.Random(p)
    for _ in range(60):
        d = rng.randint(1, 10)
        c = [rng.randrange(p) for _ in range(d)]
        a = [rng.randrange(p) for _ in range(d)]
        n = rng.randint(0, 400)
        got = nth_term([ModP(x, p) for x in c], [ModP(x, p) for x in a], n)
        assert got == run_recurrence(c, a, n) % p
    for _ in range(20):
        d = rng.randint(1, 6)
        c = [rng.randrange(p) for _ in range(d)]
        a = [rng.randrange(p) for _ in range(d)]
        n = rng.randrange(10**18)
        got = nth_term([ModP(x, p) for x in c], [ModP(x, p) for x in a], n)
        assert got == companion_power_term(c, a, n, p)
    # non-monic constant term, a unit mod p
    for _ in range(20):
        q = [ModP(rng.randrange(1, p), p)] + [ModP(rng.randrange(p), p) for _ in range(rng.randint(0, 5))]
        num = [ModP(rng.randrange(p), p) for _ in range(rng.randint(0, 6))]
        m = rng.randint(0, 60)
        assert bostan_mori(num, q, m) == series_coefficient_naive(num, q, m)


def test_over_fractions():
    rng = random.Random(5)
    for _ in range(60):
        q = [Fraction(rng.randint(1, 5), rng.randint(1, 4))] + [Fraction(rng.randint(-4, 4), rng.randint(1, 3)) for _ in range(rng.randint(0, 4))]
        p = [Fraction(rng.randint(-4, 4), rng.randint(1, 3)) for _ in range(rng.randint(0, 5))]
        n = rng.randint(0, 40)
        assert bostan_mori(p, q, n) == series_coefficient_naive(p, q, n)
    # 1 / (2 - x) = sum x^n / 2^(n + 1)
    assert bostan_mori([Fraction(1)], [Fraction(2), Fraction(-1)], 20) == Fraction(1, 2**21)


def test_huge_index_over_z():
    # Fibonacci identity F(2k) = F(k) (2 F(k + 1) - F(k)), checked at k = 5000
    k = 5000
    fk = nth_term([1, 1], [0, 1], k)
    fk1 = nth_term([1, 1], [0, 1], k + 1)
    assert nth_term([1, 1], [0, 1], 2 * k) == fk * (2 * fk1 - fk)
    assert fk == run_recurrence([1, 1], [0, 1], k)
