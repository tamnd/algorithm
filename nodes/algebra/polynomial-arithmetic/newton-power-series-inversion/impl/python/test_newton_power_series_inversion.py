# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-power-series-inversion/. The authors are listed in prov/8P4715.jsonl.

import random
from fractions import Fraction

import pytest

from newton_power_series_inversion import (
    divide_series,
    inverse,
    inverse_naive,
    karatsuba_mul,
    precisions,
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


# Independent oracle on plain ints: truncated schoolbook product.


def trunc_mul(a, b, n, p=None):
    c = [0] * n
    for i, x in enumerate(a[:n]):
        for j, y in enumerate(b[: n - i]):
            c[i + j] += x * y
    return [v % p for v in c] if p is not None else c


def is_one_mod(c, n):
    return c[0] == 1 and all(v == 0 for v in c[1:n])


def test_worked_example_fibonacci():
    assert inverse([1, -1, -1], 8) == [1, 1, 2, 3, 5, 8, 13, 21]
    assert precisions(8) == [1, 2, 4, 8]
    assert precisions(5) == [1, 2, 3, 5]
    assert precisions(1) == [1]


def test_geometric_series():
    assert inverse([1, -1], 10) == [1] * 10
    assert inverse([1, 1], 6) == [1, -1, 1, -1, 1, -1]


def test_edge_cases():
    assert inverse([1], 0) == []
    assert inverse([5], 0) == []
    assert inverse([1], 1) == [1]
    assert inverse([-1], 4) == [-1, 0, 0, 0]
    assert inverse([Fraction(3)], 3) == [Fraction(1, 3), 0, 0]
    # trailing zeros in the input change nothing
    assert inverse([1, 2, 0, 0, 0, 0], 5) == inverse([1, 2], 5)
    # input longer than the precision: extra terms are ignored
    assert inverse([1, 2, 3, 4, 5, 6, 7], 2) == [1, -2]
    with pytest.raises(ValueError):
        inverse([], 3)
    with pytest.raises(ValueError):
        inverse([0, 1], 3)
    with pytest.raises(ValueError):
        inverse([2, 1], 3)  # 2 is not a unit of Z
    with pytest.raises(ValueError):
        inverse([ModP(0, 7), ModP(1, 7)], 3)


def test_random_over_integers():
    rng = random.Random(101)
    for _ in range(150):
        k = rng.randint(1, 40)
        f = [rng.choice([1, -1])] + [rng.randint(-50, 50) for _ in range(k - 1)]
        n = rng.randint(1, 70)
        g = inverse(f, n)
        assert g == inverse_naive(f, n)
        assert is_one_mod(trunc_mul(f, g, n), n)


@pytest.mark.parametrize("p", [2, 3, 7, 998244353])
def test_random_mod_p(p):
    rng = random.Random(p)
    for _ in range(60):
        k = rng.randint(1, 30)
        f0 = rng.randrange(1, p)
        raw = [f0] + [rng.randrange(p) for _ in range(k - 1)]
        f = [ModP(v, p) for v in raw]
        n = rng.randint(1, 80)
        g = inverse(f, n)
        assert len(g) == n
        prod = trunc_mul(raw, [x.v for x in g], n, p)
        assert prod[0] == 1 and all(v == 0 for v in prod[1:])
        assert [x.v for x in g] == [x.v for x in inverse_naive(f, n)]


def test_random_over_rationals():
    rng = random.Random(7)
    for _ in range(40):
        k = rng.randint(1, 20)
        f = [Fraction(rng.randint(1, 9), rng.randint(1, 9)) * rng.choice([1, -1])]
        f += [Fraction(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(k - 1)]
        n = rng.randint(1, 40)
        g = inverse(f, n)
        assert g == inverse_naive(f, n)
        assert is_one_mod(trunc_mul(f, g, n), n)


def test_large_precision_uses_karatsuba():
    rng = random.Random(3)
    p = 998244353
    raw = [1] + [rng.randrange(p) for _ in range(599)]
    f = [ModP(v, p) for v in raw]
    n = 600
    g = inverse(f, n)
    # check f g = 1 mod x^n at a few random coefficients by direct sums
    gv = [x.v for x in g]
    for k in [0, 1, 2, 300, 599] + [rng.randrange(n) for _ in range(10)]:
        s = sum(raw[j] * gv[k - j] for j in range(k + 1)) % p
        assert s == (1 if k == 0 else 0)


def test_karatsuba_against_schoolbook():
    rng = random.Random(11)
    for _ in range(60):
        a = [rng.randint(-99, 99) for _ in range(rng.randint(0, 120))]
        b = [rng.randint(-99, 99) for _ in range(rng.randint(0, 120))]
        assert karatsuba_mul(a, b) == schoolbook_mul(a, b)
    # very different lengths
    a = [rng.randint(-9, 9) for _ in range(300)]
    b = [rng.randint(-9, 9) for _ in range(40)]
    assert karatsuba_mul(a, b) == schoolbook_mul(a, b)
    assert karatsuba_mul(b, a) == schoolbook_mul(a, b)


def test_divide_series():
    # (1 + x) / (1 - x) = 1 + 2x + 2x^2 + ...
    assert divide_series([1, 1], [1, -1], 6) == [1, 2, 2, 2, 2, 2]
    assert divide_series([], [1, -1], 3) == [0, 0, 0]
    assert divide_series([1, 2, 3], [1], 0) == []
    rng = random.Random(5)
    for _ in range(40):
        a = [rng.randint(-9, 9) for _ in range(rng.randint(1, 20))]
        f = [1] + [rng.randint(-9, 9) for _ in range(rng.randint(0, 20))]
        n = rng.randint(1, 30)
        q = divide_series(a, f, n)
        assert trunc_mul(f, q, n) == (a + [0] * n)[:n]


def test_schoolbook_multiplier_gives_same_result():
    rng = random.Random(9)
    f = [1] + [rng.randint(-5, 5) for _ in range(30)]
    assert inverse(f, 50, mul=schoolbook_mul) == inverse(f, 50)
