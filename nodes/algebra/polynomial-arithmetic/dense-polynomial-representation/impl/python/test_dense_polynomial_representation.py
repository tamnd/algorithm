# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dense-polynomial-representation/. The authors are listed in prov/YEET6X.jsonl.

import random
from fractions import Fraction

import pytest

from dense_polynomial_representation import (
    add,
    degree,
    derivative,
    divmod_poly,
    evaluate,
    mul,
    normalize,
    scale,
    sub,
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
        return ModP(self.v * pow(self._c(o), -1, self.p), self.p)

    def __rtruediv__(self, o):
        return ModP(self._c(o) * pow(self.v, -1, self.p), self.p)

    def __eq__(self, o):
        return self.v == self._c(o) % self.p

    def __hash__(self):
        return hash(self.v)

    def __repr__(self):
        return f"{self.v} mod {self.p}"


# An independent oracle: polynomials as dicts {exponent: value}, with plain
# Python numbers, reduced mod p when p is given.


def to_dict(a, p=None):
    d = {}
    for i, x in enumerate(a):
        v = x.v if isinstance(x, ModP) else x
        if p is not None:
            v %= p
        if v != 0:
            d[i] = v
    return d


def d_mul(a, b, p=None):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            out[i + j] = out.get(i + j, 0) + x * y
    if p is not None:
        out = {k: v % p for k, v in out.items()}
    return {k: v for k, v in out.items() if v != 0}


def d_add(a, b, p=None):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + v
    if p is not None:
        out = {k: v % p for k, v in out.items()}
    return {k: v for k, v in out.items() if v != 0}


def d_eval(a, u, p=None):
    s = sum(v * u**k for k, v in a.items())
    return s % p if p is not None else s


def is_normalized(a):
    return not a or not a[-1] == 0


def rand_poly(rng, n, make, lo=-5, hi=5, top_zeros=0):
    c = [make(rng.randint(lo, hi)) for _ in range(n)]
    return c + [make(0)] * top_zeros


RINGS = [
    ("Z", None, lambda x: x),
    ("F2", 2, lambda x: ModP(x, 2)),
    ("F3", 3, lambda x: ModP(x, 3)),
    ("F7", 7, lambda x: ModP(x, 7)),
    ("F998244353", 998244353, lambda x: ModP(x, 998244353)),
    ("Q", None, lambda x: Fraction(x, 1)),
]


def test_example_product():
    a = [1, 1, 0, 3]  # 1 + x + 3x^3
    b = [2, -1]  # 2 - x
    assert mul(a, b) == [2, 1, -1, 6, -3]


def test_example_cancellation():
    assert add([1, 2, 1], [4, -2, -1]) == [5]
    assert sub([1, 2, 1], [1, 2, 1]) == []


def test_example_division_over_z():
    q, r = divmod_poly([5, 2, 0, 1], [1, 1, 1])
    assert q == [-1, 1] and r == [6, 2]


def test_example_division_over_f7():
    a = [ModP(x, 7) for x in [5, 2, 0, 1]]
    b = [ModP(1, 7), ModP(3, 7)]
    q, r = divmod_poly(a, b)
    assert q == [2, 3, 5] and r == [3]


def test_example_evaluation():
    assert evaluate([-1, 2, -6, 2], 3) == 5


def test_zero_and_constants():
    assert add([], []) == [] and mul([], [1, 2]) == [] and mul([3], []) == []
    assert mul([3], [4]) == [12] and evaluate([], 7) == 0 and evaluate([4], 9) == 4
    assert degree([]) == -1 and degree([5]) == 0 and degree([0, 1]) == 1
    assert divmod_poly([], [1, 1]) == ([], [])
    assert divmod_poly([7], [2, 1]) == ([], [7])
    assert divmod_poly([3, 1], [1]) == ([3, 1], [])
    assert derivative([5]) == [] and derivative([]) == [] and derivative([1, 2, 3]) == [2, 6]
    assert scale(0, [1, 2]) == [] and scale(2, []) == []
    with pytest.raises(ZeroDivisionError):
        divmod_poly([1], [])
    with pytest.raises(ValueError):
        divmod_poly([1, 0, 1], [1, 2])


def test_strip_leading_zeros():
    assert normalize([1, 2, 0, 0]) == [1, 2] and normalize([0, 0]) == []
    # 3x^2 + x over Z/3Z is x
    a = normalize([ModP(0, 3), ModP(1, 3), ModP(3, 3)])
    assert len(a) == 2 and a == [0, 1]
    # (2x + 1)^2 over Z/4Z is 1: the top coefficient 4 vanishes
    sq = mul([ModP(1, 4), ModP(2, 4)], [ModP(1, 4), ModP(2, 4)])
    assert sq == [1]
    # x^2 + x + 1 and -x^2 - x over Z: the sum drops two degrees
    assert add([1, 1, 1], [0, -1, -1]) == [1]


def test_degree_one_and_far_apart():
    rng = random.Random(1)
    big = [rng.randint(-9, 9) for _ in range(60)] + [1]
    q, r = divmod_poly(big, [-2, 1])
    assert r == ([evaluate(big, 2)] if evaluate(big, 2) != 0 else [])
    assert add(mul(q, [-2, 1]), r) == big
    small = [4, 1]
    assert mul(big, small) == mul(small, big)
    assert divmod_poly(small, big) == ([], small)


@pytest.mark.parametrize("name,p,make", RINGS)
def test_random_against_oracle(name, p, make):
    rng = random.Random(hash(name) % 1000 + 7)
    for _ in range(300):
        m, n = rng.randint(0, 9), rng.randint(0, 9)
        a = normalize(rand_poly(rng, m, make))
        b = normalize(rand_poly(rng, n, make))
        assert is_normalized(a) and is_normalized(b)
        da, db = to_dict(a, p), to_dict(b, p)
        s, pr = add(a, b), mul(a, b)
        assert is_normalized(s) and is_normalized(pr)
        assert to_dict(s, p) == d_add(da, db, p)
        assert to_dict(pr, p) == d_mul(da, db, p)
        assert to_dict(sub(a, b), p) == d_add(da, {k: -v for k, v in db.items()}, p)
        u = rng.randint(-4, 4)
        ev = evaluate(a, make(u))
        want = d_eval(da, u, p)
        assert ev == want
        # division by a divisor whose leading coefficient is a unit
        if p is None and name == "Z":
            if b:
                b = b[:-1] + [rng.choice([1, -1])]
            else:
                b = [1]
        elif not b:
            b = [make(1)]
        db = to_dict(b, p)
        q, r = divmod_poly(a, b)
        assert is_normalized(q) and is_normalized(r)
        assert len(r) < len(b)
        assert to_dict(add(mul(q, b), r), p) == da
        assert d_add(d_mul(to_dict(q, p), db, p), to_dict(r, p), p) == da


@pytest.mark.parametrize("name,p,make", RINGS)
def test_random_with_top_zeros(name, p, make):
    rng = random.Random(len(name) * 31)
    for _ in range(200):
        n = rng.randint(0, 6)
        raw = rand_poly(rng, n, make, top_zeros=rng.randint(0, 3))
        a = normalize(list(raw))
        assert is_normalized(a)
        assert to_dict(a, p) == to_dict(raw, p)


def test_monic_and_non_monic_divisors_over_q():
    rng = random.Random(5)
    for _ in range(300):
        a = normalize([Fraction(rng.randint(-6, 6), rng.randint(1, 4)) for _ in range(rng.randint(0, 10))])
        b = normalize([Fraction(rng.randint(-6, 6), rng.randint(1, 4)) for _ in range(rng.randint(1, 6))])
        if not b:
            continue
        monic = [x / b[-1] for x in b]
        for d in (b, monic):
            q, r = divmod_poly(a, d)
            assert len(r) < len(d)
            assert add(mul(q, d), r) == a
