# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-interpolation/. The authors are listed in prov/2CT8SN.jsonl.

import random
from fractions import Fraction

import pytest

from fast_interpolation import (
    interpolate,
    interpolate_newton,
    schoolbook_mul,
    subproduct_tree,
    linear_combination,
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


# Independent oracle: Lagrange's formula with plain integers modulo p, or with
# Fraction, and evaluation of the result at the points.


def lagrange(points, values, p=None):
    n = len(points)
    f = [0] * n
    for i in range(n):
        num = [1]
        den = 1
        for j in range(n):
            if j != i:
                num = [(a - points[j] * b) for a, b in zip([0] + num, num + [0])]
                den *= points[i] - points[j]
        w = values[i] * (pow(den, -1, p) if p else Fraction(1, 1) / den)
        for k in range(n):
            f[k] += w * num[k]
    if p:
        f = [c % p for c in f]
    while f and f[-1] == 0:
        f.pop()
    return f


def ints(v):
    return [x.v if isinstance(x, ModP) else x for x in v]


def distinct(rng, n, lo, hi):
    return rng.sample(range(lo, hi), n)


PRIMES = [3, 7, 998244353]


def test_page_example():
    pts = [Fraction(u) for u in [0, 1, 2, 3, 4]]
    vals = [1, 15, 129, 547, 1593]
    assert interpolate(pts, vals) == [1, 2, 3, 4, 5]


def test_linear_combination_page_trace():
    levels = subproduct_tree([0, 1, 2, 3])
    # c = (1, 1, 1, 1) gives m' for m = x^4 - 6x^3 + 11x^2 - 6x.
    assert linear_combination([1, 1, 1, 1], levels) == [-6, 22, -18, 4]


@pytest.mark.parametrize("p", PRIMES)
def test_mod_p_random(p):
    rng = random.Random(p)
    for _ in range(40):
        n = rng.randint(1, min(p, 40))
        pts = distinct(rng, n, 0, p) if p < 10**6 else [rng.randrange(p) for _ in range(n)]
        if len(set(pts)) < n:
            continue
        vals = [rng.randrange(p) for _ in range(n)]
        got = interpolate([ModP(u, p) for u in pts], [ModP(v, p) for v in vals])
        assert ints(got) == lagrange(pts, vals, p)


def test_mod_2_all_points():
    for vals in ([0, 0], [1, 0], [0, 1], [1, 1]):
        got = interpolate([ModP(0, 2), ModP(1, 2)], [ModP(v, 2) for v in vals])
        assert ints(got) == lagrange([0, 1], vals, 2)


def test_fraction_random():
    rng = random.Random(6)
    for _ in range(40):
        n = rng.randint(1, 25)
        pts = [Fraction(u, rng.randint(1, 4)) for u in distinct(rng, n, -60, 60)]
        if len(set(pts)) < n:
            continue
        vals = [Fraction(rng.randint(-20, 20), rng.randint(1, 3)) for _ in range(n)]
        f = interpolate(pts, vals)
        assert f == lagrange(pts, vals)
        assert f == interpolate_newton(pts, vals)


def test_round_trip_mod_p():
    p = 998244353
    rng = random.Random(10)
    n = 200
    f = [rng.randrange(p) for _ in range(n)]
    pts = rng.sample(range(p), n)
    vals = [sum(c * pow(u, k, p) for k, c in enumerate(f)) % p for u in pts]
    got = interpolate([ModP(u, p) for u in pts], [ModP(v, p) for v in vals])
    assert ints(got) == f


def test_schoolbook_multiplier_agrees():
    rng = random.Random(3)
    p = 7
    pts = [ModP(u, p) for u in range(7)]
    for _ in range(20):
        vals = [ModP(rng.randrange(p), p) for _ in range(7)]
        assert interpolate(pts, vals, mul=schoolbook_mul) == interpolate(pts, vals)


def test_over_z_unit_differences():
    # Over Z the differences must be +1 or -1: only two consecutive integers.
    assert interpolate([0, 1], [3, 5]) == [3, 2]
    assert interpolate([4], [9]) == [9]
    with pytest.raises(ValueError):
        interpolate([0, 2], [1, 1])


def test_edge_cases():
    assert interpolate([], []) == []
    # All values zero gives the zero polynomial.
    assert interpolate([Fraction(1), Fraction(2), Fraction(3)], [0, 0, 0]) == []
    # Constant values give a constant.
    assert interpolate([Fraction(u) for u in range(9)], [5] * 9) == [5]
    # Degree 1 data.
    assert interpolate([Fraction(u) for u in range(6)], [2 * u + 1 for u in range(6)]) == [1, 2]
    # Odd number of points, so a tree node has no sibling.
    pts = [Fraction(u) for u in range(7)]
    assert interpolate(pts, [u * u for u in range(7)]) == [0, 0, 1]
    # Repeated points are rejected.
    with pytest.raises(ValueError):
        interpolate([Fraction(1), Fraction(1)], [1, 2])
    with pytest.raises(ValueError):
        interpolate([ModP(1, 7), ModP(8, 7)], [ModP(1, 7), ModP(2, 7)])
    with pytest.raises(ValueError):
        interpolate([1, 2], [1])
