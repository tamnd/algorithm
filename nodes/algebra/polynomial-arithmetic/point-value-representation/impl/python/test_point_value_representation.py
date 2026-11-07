# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-value-representation/. The authors are listed in prov/T0CK84.jsonl.

import random
from fractions import Fraction

import pytest

from point_value_representation import (
    add,
    evaluate_at,
    extend,
    from_coefficients,
    mul,
    sub,
    to_coefficients,
    weights,
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
        return ModP(self.v * pow(self._c(o) % self.p, -1, self.p), self.p)

    def __rtruediv__(self, o):
        return ModP(self._c(o) * pow(self.v, -1, self.p), self.p)

    def __eq__(self, o):
        return self.v == self._c(o) % self.p

    def __hash__(self):
        return hash(self.v)


# Independent schoolbook oracle on plain numbers.


def school_mul(a, b, p=None):
    if not a or not b:
        return []
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return strip(c, p)


def strip(a, p=None):
    a = [x % p for x in a] if p is not None else list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def raw(xs):
    return [x.v if isinstance(x, ModP) else x for x in xs]


def test_example():
    pts = [Fraction(0), Fraction(1), Fraction(2)]
    f, g = [1, 2], [3, -1]  # 1 + 2x and 3 - x
    yf, yg = from_coefficients(f, pts), from_coefficients(g, pts)
    assert yf == [1, 3, 5] and yg == [3, 2, 1]
    yh = mul(yf, yg)
    assert yh == [3, 6, 5]
    assert to_coefficients(yh, pts) == [3, 5, -2]
    w = weights(pts)
    assert w == [Fraction(1, 2), -1, Fraction(1, 2)]
    assert evaluate_at(yh, pts, w, Fraction(3)) == 3 + 15 - 18
    assert evaluate_at(yh, pts, w, Fraction(1)) == 6


def test_too_few_points():
    pts = [Fraction(0), Fraction(1)]
    y = from_coefficients([0, 1], pts)  # x
    sq = mul(y, y)  # x^2 needs 3 points
    assert to_coefficients(sq, pts) == [0, 1]  # wrong: this is x, not x^2
    pts3 = pts + [Fraction(2)]
    assert to_coefficients(mul(extend(y, pts, pts3), extend(y, pts, pts3)), pts3) == [0, 0, 1]


def test_edges():
    pts = [Fraction(5)]
    assert to_coefficients([Fraction(7)], pts) == [7]
    assert to_coefficients([Fraction(0)], pts) == []
    assert to_coefficients([], []) == []
    pts = [Fraction(x) for x in (0, 1, 2, 3)]
    assert to_coefficients([0, 0, 0, 0], pts) == []
    assert to_coefficients([4, 4, 4, 4], pts) == [4]
    assert from_coefficients([], pts) == [0, 0, 0, 0]
    with pytest.raises(ValueError):
        weights([Fraction(1), Fraction(1)])
    # far apart degrees: a constant times a degree 5 polynomial
    big = [Fraction(x) for x in (1, -2, 0, 3, 0, 1)]
    pts6 = [Fraction(x) for x in range(-3, 3)]
    prod = mul(from_coefficients([Fraction(-4)], pts6), from_coefficients(big, pts6))
    assert to_coefficients(prod, pts6) == [-4 * x for x in big]


FIELDS = [
    ("F2", 2),
    ("F3", 3),
    ("F7", 7),
    ("F998244353", 998244353),
    ("Q", None),
]


@pytest.mark.parametrize("name,p", FIELDS)
def test_random_against_schoolbook(name, p):
    rng = random.Random(sum(map(ord, name)) * 13)
    for _ in range(500):
        n_pts = rng.randint(1, 9 if p is None or p > 9 else p)
        if p is None:
            vals = rng.sample(range(-20, 20), n_pts)
            pts = [Fraction(v, rng.choice([1, 2, 3])) for v in vals]
            if len(set(pts)) < n_pts:
                continue
            make = lambda x: Fraction(x)
        else:
            pts = [ModP(v, p) for v in rng.sample(range(min(p, 10**6)), n_pts)]
            make = lambda x: ModP(x, p)
        da = rng.randint(0, n_pts - 1)
        db = rng.randint(0, n_pts - 1 - da)
        a_int = strip([rng.randint(-9, 9) for _ in range(da + 1)], p)
        b_int = strip([rng.randint(-9, 9) for _ in range(db + 1)], p)
        a = [make(x) for x in a_int]
        b = [make(x) for x in b_int]
        ya, yb = from_coefficients(a, pts), from_coefficients(b, pts)
        want = school_mul(a_int, b_int, p)
        got = to_coefficients(mul(ya, yb), pts)
        assert strip(raw(got), p) == want if p is not None else got == want
        s = to_coefficients(add(ya, yb), pts)
        n = max(len(a_int), len(b_int))
        want_s = strip([(a_int[i] if i < len(a_int) else 0) + (b_int[i] if i < len(b_int) else 0) for i in range(n)], p)
        assert strip(raw(s), p) == want_s if p is not None else s == want_s
        d = to_coefficients(sub(ya, ya), pts)
        assert d == []
        # barycentric evaluation at a fresh point agrees with Horner
        w = weights(pts)
        t = make(rng.randint(-50, 50))
        yab = mul(ya, yb)
        assert evaluate_at(yab, pts, w, t) == from_coefficients(got, [t])[0]
        # round trip
        assert to_coefficients(ya, pts) == a or strip(raw(to_coefficients(ya, pts)), p) == a_int


def test_integer_coefficients_through_rationals():
    rng = random.Random(77)
    for _ in range(300):
        a = strip([rng.randint(-50, 50) for _ in range(rng.randint(0, 6))])
        b = strip([rng.randint(-50, 50) for _ in range(rng.randint(0, 6))])
        n = max(len(a) + len(b) - 1, 1)
        pts = [Fraction(i) for i in range(n)]
        got = to_coefficients(mul(from_coefficients(a, pts), from_coefficients(b, pts)), pts)
        assert got == school_mul(a, b)
