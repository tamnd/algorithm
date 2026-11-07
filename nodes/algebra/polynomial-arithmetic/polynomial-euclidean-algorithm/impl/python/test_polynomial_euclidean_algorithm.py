# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polynomial-euclidean-algorithm/. The authors are listed in prov/EBMDJ7.jsonl.

import random
from fractions import Fraction

import pytest

from polynomial_euclidean_algorithm import polynomial_gcd


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


def ref_divmod(f, g):
    """Reference division over a field: the quotient from the reversals and a
    power series inverse computed term by term, then r = f - q g."""
    f, g = strip(f), strip(g)
    m, n = len(f) - 1, len(g) - 1
    if m < n:
        return [], f
    k = m - n + 1
    rf, rg = f[::-1], g[::-1]
    inv = [1 / rg[0]]
    for i in range(1, k):
        s = rg[0] * 0
        for j in range(1, min(i, n) + 1):
            s = s + rg[j] * inv[i - j]
        inv.append(-s * inv[0])
    rq = [sum((rf[j] * inv[i - j] for j in range(i + 1)), rf[0] * 0) for i in range(k)]
    q = strip(rq[::-1])
    return q, sub(f, mul(q, g))


def sylvester_rank(f, g):
    """Rank of the Sylvester matrix of f and g, by Gaussian elimination."""
    m, n = len(f) - 1, len(g) - 1
    size = m + n
    rows = []
    for i in range(n):
        rows.append([f[0] * 0] * i + f[::-1] + [f[0] * 0] * (n - 1 - i))
    for i in range(m):
        rows.append([g[0] * 0] * i + g[::-1] + [g[0] * 0] * (m - 1 - i))
    rank = 0
    for col in range(size):
        piv = next((i for i in range(rank, len(rows)) if rows[i][col] != 0), None)
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        p = rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i][col] != 0:
                c = rows[i][col] / p[col]
                rows[i] = [x - c * y for x, y in zip(rows[i], p)]
        rank += 1
    return rank


def check(f, g):
    h = polynomial_gcd(f, g)
    fs, gs = strip(f), strip(g)
    if not fs and not gs:
        assert h == []
        return h
    assert h and h[-1] == 1
    assert ref_divmod(fs, h)[1] == []
    assert ref_divmod(gs, h)[1] == []
    if not fs or not gs:
        assert len(h) == len(fs or gs)
    else:
        assert len(h) - 1 == len(fs) + len(gs) - 2 - sylvester_rank(fs, gs)
    assert polynomial_gcd(g, f) == h
    return h


def F(xs):
    return [Fraction(x) for x in xs]


def P(xs, p):
    return [Fp(x, p) for x in xs]


def test_example_over_q():
    h = check(F([-1, 0, 0, 0, 1]), F([1, 2, 2, 1]))
    assert h == [1, 1]


def test_example_over_f7():
    h = check(P([-1, 0, 0, 0, 1], 7), P([1, 2, 2, 1], 7))
    assert [c.v for c in h] == [1, 1]


def test_shared_cubic():
    f = F([-2, -1, 0, 2, 1])
    g = F([-3, -1, 0, 3, 1])
    assert check(f, g) == [-1, 0, 0, 1]


def test_edges():
    assert polynomial_gcd([], []) == []
    assert polynomial_gcd(F([0, 0]), F([0])) == []
    assert check([], F([4, 2])) == [2, 1]
    assert check(F([0, 3, 0]), []) == [0, 1]
    assert check(F([5]), F([1, 2, 3])) == [1]
    assert check(F([7]), F([3])) == [1]
    assert check(F([1, 2, 1, 0, 0]), F([2, 2, 0])) == [1, 1]
    assert check(F([2, 4, 2]), F([2, 4, 2])) == [1, 2, 1]
    assert check(F([-1, 1]), F([-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])) == [-1, 1]
    assert check(F([Fraction(1, 2), Fraction(3, 4)]), F([1])) == [1]


def test_int_input_is_rejected():
    with pytest.raises(ValueError):
        polynomial_gcd([0, 0, 2], [1, 2])


def test_f2_example():
    h = check(P([0, 1, 0, 0, 1], 2), P([1, 0, 1], 2))
    assert [c.v for c in h] == [1, 1]


def rand_poly(rng, d, make):
    return [make(rng.randint(-5, 5)) for _ in range(d + 1)]


def test_random_rationals():
    rng = random.Random(5101)
    for _ in range(400):
        if rng.random() < 0.6:
            h = rand_poly(rng, rng.randint(0, 3), Fraction)
            f = mul(h, rand_poly(rng, rng.randint(0, 4), Fraction))
            g = mul(h, rand_poly(rng, rng.randint(0, 4), Fraction))
        else:
            f = rand_poly(rng, rng.randint(0, 6), Fraction)
            g = rand_poly(rng, rng.randint(0, 6), Fraction)
        if rng.random() < 0.2:
            f = f + [Fraction(0)] * rng.randint(1, 3)
        check(f, g)


@pytest.mark.parametrize("p", [2, 3, 7, 998244353])
def test_random_mod_p(p):
    rng = random.Random(5200 + p)
    make = lambda x: Fp(x, p)
    for _ in range(150):
        if rng.random() < 0.6:
            h = rand_poly(rng, rng.randint(0, 3), make)
            f = mul(h, rand_poly(rng, rng.randint(0, 4), make))
            g = mul(h, rand_poly(rng, rng.randint(0, 4), make))
        else:
            f = rand_poly(rng, rng.randint(0, 6), make)
            g = rand_poly(rng, rng.randint(0, 6), make)
        check(f, g)


def test_very_different_degrees():
    rng = random.Random(5301)
    for _ in range(8):
        h = [Fp(rng.randint(0, 6), 7) for _ in range(2)] + [Fp(1, 7)]
        f = mul(h, [Fp(rng.randint(0, 6), 7) for _ in range(40)] + [Fp(1, 7)])
        g = mul(h, [Fp(rng.randint(1, 6), 7)])
        hh = check(f, g)
        assert len(hh) >= 3
