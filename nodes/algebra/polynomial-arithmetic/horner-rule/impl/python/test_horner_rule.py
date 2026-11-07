# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horner-rule/. The authors are listed in prov/947TVN.jsonl.

import random
from fractions import Fraction

import pytest

from horner_rule import horner, horner_with_derivative, synthetic_division, taylor_shift


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

    def __eq__(self, o):
        return self.v == self._c(o) % self.p

    def __hash__(self):
        return hash(self.v)


# Independent oracles, on plain Python numbers.


def naive_eval(a, u, p=None):
    s = sum(c * u**i for i, c in enumerate(a))
    return s % p if p is not None else s


def poly_mul(a, b):
    if not a or not b:
        return []
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return c


def strip(a, p=None):
    a = [x % p for x in a] if p is not None else list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def expand_taylor(c, u):
    """sum c_k (x - u)^k as a plain coefficient list."""
    out = [0] * max(len(c), 1)
    power = [1]
    for ck in c:
        for i, x in enumerate(power):
            out[i] += ck * x
        power = poly_mul(power, [-u, 1])
    return out


def raw(xs):
    return [x.v if isinstance(x, ModP) else x for x in xs]


RINGS = [
    ("Z", None, lambda x: x),
    ("F2", 2, lambda x: ModP(x, 2)),
    ("F3", 3, lambda x: ModP(x, 3)),
    ("F7", 7, lambda x: ModP(x, 7)),
    ("F998244353", 998244353, lambda x: ModP(x, 998244353)),
    ("Q", None, lambda x: Fraction(x, 3)),
]


def test_example():
    f = [-1, 2, -6, 2]  # 2x^3 - 6x^2 + 2x - 1
    assert horner(f, 3) == 5
    q, r = synthetic_division(f, 3)
    assert q == [2, 0, 2] and r == 5
    assert taylor_shift(f, 3) == [5, 20, 12, 2]  # 5 + 20 (x-3) + 12 (x-3)^2 + 2 (x-3)^3
    assert horner_with_derivative(f, 3) == (5, 20)


def test_root_and_deflation():
    f = [-6, 11, -6, 1]  # (x - 1)(x - 2)(x - 3)
    q, r = synthetic_division(f, 1)
    assert r == 0 and q == [6, -5, 1]
    q2, r2 = synthetic_division(q, 2)
    assert r2 == 0 and q2 == [-3, 1]


def test_edges():
    assert horner([], 5) == 0
    assert horner([7], 5) == 7
    assert horner([7, 2], 5) == 17
    assert synthetic_division([7], 5) == ([], 7)
    assert synthetic_division([7, 2], 5) == ([2], 17)
    assert taylor_shift([], 4) == [] and taylor_shift([9], 4) == [9]
    assert horner([1, 0, 0, 0, 0, 1], -1) == 0
    assert horner([3, 1], ModP(2, 2)) == 1
    # the point 0 returns the constant term; a huge degree needs no recursion
    big = [1] * 5000
    assert horner(big, 0) == 1 and horner(big, 1) == 5000
    assert horner(big, -1) == 0


def test_matrix_point():
    def matmul(x, y):
        return [[sum(x[i][k] * y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

    class Mat:
        def __init__(self, m):
            self.m = m

        def __mul__(self, o):
            return Mat(matmul(self.m, o.m))

        def __add__(self, c):
            return Mat([[self.m[i][j] + (c if i == j else 0) for j in range(2)] for i in range(2)])

    a = Mat([[1, 1], [1, 0]])
    # x^2 - x - 1 vanishes at the Fibonacci matrix (Cayley-Hamilton)
    s = horner([-1, -1, Mat([[1, 0], [0, 1]])], a)
    assert s.m == [[0, 0], [0, 0]]


@pytest.mark.parametrize("name,p,make", RINGS)
def test_random_against_oracle(name, p, make):
    rng = random.Random(sum(map(ord, name)))
    for _ in range(600):
        n = rng.randint(0, 12)
        ints = [rng.randint(-20, 20) for _ in range(n)]
        if p is not None:
            ints = strip(ints, p)
        else:
            ints = strip(ints)
        a = [make(x) for x in ints]
        ui = rng.randint(-6, 6)
        u = make(ui)
        val = horner(a, u)
        if name == "Q":
            want = naive_eval([Fraction(x, 3) for x in ints], Fraction(ui, 3))
        else:
            want = naive_eval(ints, ui, p)
        assert val == want
        if not a:
            continue
        q, r = synthetic_division(a, u)
        assert r == val and len(q) == len(a) - 1
        # a == (x - u) q + r, checked with the plain schoolbook product
        if name == "Q":
            qq, aa, uu = list(q), [Fraction(x, 3) for x in ints], Fraction(ui, 3)
            back = poly_mul([-uu, 1], qq) if qq else [0]
            back[0] += r
            assert strip(back) == aa
            c = taylor_shift(a, u)
            assert strip(expand_taylor(c, uu)) == aa
            assert c[0] == val
        else:
            qq = raw(q)
            back = poly_mul([-ui, 1], qq) if qq else [0]
            back[0] += r.v if isinstance(r, ModP) else r
            assert strip(back, p) == strip(ints, p)
            c = raw(taylor_shift(a, u))
            assert strip(expand_taylor(c, ui), p) == strip(ints, p)
        s, d = horner_with_derivative(a, u)
        deriv = [i * x for i, x in enumerate(a)][1:]
        assert s == val and d == horner(deriv, u, zero=make(0))
