# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-polynomial-division/. The authors are listed in prov/X5VM5A.jsonl.

import random
from fractions import Fraction

import pytest

from fast_polynomial_division import (
    divmod_fast,
    divmod_schoolbook,
    karatsuba_mul,
    normalize,
    reversed_inverse,
    schoolbook_mul,
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


# Independent oracle on plain ints: textbook long division modulo p, or over
# Fraction, written without any code from the module under test.


def oracle_divmod(a, b, p=None):
    a = [x % p for x in a] if p else [Fraction(x) for x in a]
    b = [x % p for x in b] if p else [Fraction(x) for x in b]
    while a and a[-1] == 0:
        a.pop()
    while b and b[-1] == 0:
        b.pop()
    q = [0] * max(len(a) - len(b) + 1, 0)
    r = list(a)
    inv = pow(b[-1], -1, p) if p else 1 / b[-1]
    while len(r) >= len(b):
        c = r[-1] * inv
        if p:
            c %= p
        s = len(r) - len(b)
        q[s] = c
        for j, y in enumerate(b):
            r[s + j] -= c * y
            if p:
                r[s + j] %= p
        r.pop()
        while r and r[-1] == 0:
            r.pop()
    while q and q[-1] == 0:
        q.pop()
    return q, r


def to_int(v):
    return [x.v if isinstance(x, ModP) else x for x in v]


def rand_poly(rng, deg, lo=-9, hi=9):
    return [rng.randint(lo, hi) for _ in range(deg)] + [rng.choice([x for x in range(lo, hi + 1) if x])]


def check_identity(a, b, q, r):
    """a == q b + r and deg r < deg b, using the schoolbook product."""
    a, b = normalize(a), normalize(b)
    qb = schoolbook_mul(q, b) if q else []
    n = max(len(a), len(qb), len(r))
    pad = lambda v: list(v) + [0] * (n - len(v))
    assert [x - y - z for x, y, z in zip(pad(a), pad(qb), pad(r))] == [0] * n
    assert len(r) < len(b)
    assert not r or r[-1] != 0
    assert not q or q[-1] != 0


PRIMES = [2, 3, 7, 998244353]


def test_small_example():
    q, r = divmod_fast([6, 5, 4, 3, 2, 1], [1, 1, 1])
    assert q == [2, 1, 1, 1] and r == [4, 2]


def test_worked_example():
    # The example on the page: a = x^5 + 2x^4 + 3x^3 + 4x^2 + 5x + 6, b = x^2 + x + 1.
    a = [6, 5, 4, 3, 2, 1]
    b = [1, 1, 1]
    rinv = reversed_inverse(b, 4)
    assert rinv == [1, -1, 0, 1]
    assert divmod_fast(a, b, rinv=rinv) == ([2, 1, 1, 1], [4, 2])


def test_over_z_monic_random():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(0, 60)
        m = rng.randint(0, 40)
        a = rand_poly(rng, n)
        b = rand_poly(rng, m)[:-1] + [rng.choice([1, -1])]
        q, r = divmod_fast(a, b)
        check_identity(a, b, q, r)
        assert (q, r) == divmod_schoolbook(a, b)
        oq, orr = oracle_divmod(a, b)
        assert q == oq and r == orr


@pytest.mark.parametrize("p", PRIMES)
def test_mod_p_random(p):
    rng = random.Random(p)
    for _ in range(200):
        n = rng.randint(0, 50)
        m = rng.randint(0, 50)
        a = [ModP(rng.randrange(p), p) for _ in range(n + 1)]
        b = [ModP(rng.randrange(p), p) for _ in range(m)] + [ModP(rng.randrange(1, p), p)]
        q, r = divmod_fast(a, b)
        oq, orr = oracle_divmod(to_int(a), to_int(b), p)
        assert to_int(q) == oq and to_int(r) == orr
        assert (q, r) == divmod_schoolbook(a, b)


def test_fraction_non_monic():
    rng = random.Random(5)
    for _ in range(150):
        n = rng.randint(0, 30)
        m = rng.randint(0, 25)
        a = [Fraction(x) for x in rand_poly(rng, n)]
        b = [Fraction(x) for x in rand_poly(rng, m)]
        q, r = divmod_fast(a, b)
        check_identity(a, b, q, r)
        oq, orr = oracle_divmod([int(x) for x in a], [int(x) for x in b])
        assert q == oq and r == orr


def test_schoolbook_multiplier_agrees():
    rng = random.Random(9)
    for _ in range(50):
        a = rand_poly(rng, rng.randint(0, 80))
        b = rand_poly(rng, rng.randint(0, 30))[:-1] + [1]
        assert divmod_fast(a, b, mul=schoolbook_mul) == divmod_fast(a, b, mul=karatsuba_mul)


def test_precomputed_inverse_reused():
    rng = random.Random(11)
    b = rand_poly(rng, 7)[:-1] + [1]
    rinv = reversed_inverse(b, 40)
    for _ in range(50):
        a = rand_poly(rng, rng.randint(0, 46))
        assert divmod_fast(a, b, rinv=rinv) == divmod_schoolbook(a, b)
    with pytest.raises(ValueError):
        divmod_fast([0] * 60 + [1], b, rinv=rinv)


def test_edge_cases():
    # Zero dividend.
    assert divmod_fast([], [3, 1]) == ([], [])
    assert divmod_fast([0, 0], [3, 1]) == ([], [])
    # Dividend of lower degree than the divisor.
    assert divmod_fast([1, 2], [0, 0, 1]) == ([], [1, 2])
    # Constant divisors.
    assert divmod_fast([4, 5, 6], [1]) == ([4, 5, 6], [])
    assert divmod_fast([4, 5, 6], [-1]) == ([-4, -5, -6], [])
    assert divmod_fast([Fraction(4), 6], [Fraction(2)]) == ([2, 3], [])
    # Constant dividend and divisor.
    assert divmod_fast([7], [1]) == ([7], [])
    # Degree 1 divisor: remainder is a(c) for b = x - c.
    a = [1, -3, 0, 2]
    q, r = divmod_fast(a, [-2, 1])
    assert r == [1 - 6 + 0 + 16]
    # Leading zeros are stripped.
    assert divmod_fast([6, 5, 4, 3, 2, 1, 0, 0], [1, 1, 1, 0]) == ([2, 1, 1, 1], [4, 2])
    # Same degree.
    assert divmod_fast([5, 3, 2], [1, 1, 1]) == ([2], [3, 1])
    # Exact division.
    assert divmod_fast(schoolbook_mul([1, 2, 1], [3, 0, 1]), [3, 0, 1]) == ([1, 2, 1], [])
    # Very different degrees.
    rng = random.Random(3)
    a = rand_poly(rng, 400)
    for b in ([5, 1], rand_poly(rng, 399)[:-1] + [1]):
        assert divmod_fast(a, b) == divmod_schoolbook(a, b)


def test_errors():
    with pytest.raises(ZeroDivisionError):
        divmod_fast([1, 2], [])
    with pytest.raises(ZeroDivisionError):
        divmod_fast([1, 2], [0, 0])
    # Non-unit leading coefficient over Z.
    with pytest.raises(ValueError):
        divmod_fast([1, 2, 3], [1, 2])
    with pytest.raises(ValueError):
        divmod_schoolbook([1, 2, 3], [1, 2])
