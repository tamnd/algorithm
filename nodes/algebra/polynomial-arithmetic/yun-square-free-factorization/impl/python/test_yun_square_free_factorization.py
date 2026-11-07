# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yun-square-free-factorization/. The authors are listed in prov/8QF8S3.jsonl.

import random
from fractions import Fraction

import pytest

from yun_square_free_factorization import yun


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


def rem(f, g):
    f = strip(f)
    while len(f) >= len(g):
        t = f[-1] / g[-1]
        k = len(f) - len(g)
        f = strip([c - t * g[i - k] if i >= k else c for i, c in enumerate(f)])
    return f


def gcd(a, b):
    a, b = strip(a), strip(b)
    while b:
        a, b = b, rem(a, b)
    return [c / a[-1] for c in a] if a else []


def deriv(a):
    return strip([a[k] * k for k in range(1, len(a))])


def exquo(a, b):
    a = strip(a)
    q = [a[0] * 0] * (len(a) - len(b) + 1)
    while a and len(a) >= len(b):
        t = a[-1] / b[-1]
        k = len(a) - len(b)
        q[k] = t
        a = strip([c - t * b[i - k] if i >= k else c for i, c in enumerate(a)])
    assert not a
    return strip(q)


def musser(f):
    """Independent oracle: the repeated-gcd method, characteristic 0 or p > deg f."""
    f = [c / f[-1] for c in f]
    g = gcd(f, deriv(f))
    w = exquo(f, g)
    out = []
    while len(w) > 1:
        y = gcd(w, g)
        out.append(exquo(w, y))
        w = y
        g = exquo(g, y)
    return out


def power(a, e, one):
    r = [one]
    for _ in range(e):
        r = mul(r, a)
    return r


def check(f, lc, parts, one):
    prod = [lc]
    for i, a in enumerate(parts, 1):
        assert a[-1] == 1
        prod = mul(prod, power(a, i, one))
        if len(a) > 1:
            assert len(gcd(a, deriv(a))) == 1
        for b in parts[:i - 1]:
            assert len(gcd(a, b)) == 1
    assert prod == strip(f)
    if parts:
        assert len(parts[-1]) > 1


def test_worked_examples():
    lc, a = yun([-1, 1, 2, -2, -1, 1])
    assert lc == 1 and a == [[1], [1, 1], [-1, 1]]
    lc, a = yun([0, 0, 0, -2, 1, -4, 2, -2, 1])
    assert a == [[-2, 1], [1, 0, 1], [0, 1]]
    lc, a = yun([-2, -2, 2, 2])
    assert lc == 2 and a == [[-1, 1], [1, 1]]
    assert yun([0, 0, 0, 0, 1])[1] == [[1], [1], [1], [0, 1]]


def test_edge_cases():
    with pytest.raises(ValueError):
        yun([])
    with pytest.raises(ValueError):
        yun([0, 0])
    assert yun([5]) == (5, [])
    assert yun([5, 0, 0]) == (5, [])
    assert yun([3, 2]) == (2, [[Fraction(3, 2), 1]])
    lc, a = yun([3, 9, 9, 3, 0])  # 3 (x + 1)^3 with a leading zero
    assert lc == 3 and a == [[1], [1], [1, 1]]
    # Square-free input: one part.
    assert yun([-1, 0, 1]) == (1, [[-1, 0, 1]])


def test_precondition_matters_in_small_characteristic():
    # (x + 1)^3 (x + 2) over F_3: deg f = 4 > p, and the result is wrong.
    p = 3
    f = mul(mul(power([Fp(1, p), Fp(1, p)], 3, Fp(1, p)), [Fp(2, p), Fp(1, p)]), [Fp(1, p)])
    lc, a = yun(f)
    assert a == [[Fp(2, p), Fp(1, p)]]
    prod = [lc]
    for i, x in enumerate(a, 1):
        prod = mul(prod, power(x, i, Fp(1, p)))
    assert prod != f


def random_case(rng, coef, one, maxmult, nroots, p=None, integral=False):
    """Distinct roots grouped by multiplicity, times one random square-free factor."""
    if p is None:
        roots = rng.sample(range(-50, 50), nroots)
        roots = [Fraction(r, 1 if integral else rng.randint(1, 3)) for r in roots]
        roots = list(dict.fromkeys(roots))
    else:
        roots = [Fp(r, p) for r in rng.sample(range(p), min(nroots, p))]
    groups = {}
    for r in roots:
        groups.setdefault(rng.randint(1, maxmult), []).append(r)
    k = max(groups) if groups else 0
    parts = []
    for i in range(1, k + 1):
        a = [one]
        for r in groups.get(i, []):
            a = mul(a, [-r, one])
        parts.append(a)
    lc = coef(rng)
    while lc == 0:
        lc = coef(rng)
    f = [lc]
    for i, a in enumerate(parts, 1):
        f = mul(f, power(a, i, one))
    return f, lc, parts


def test_against_construction_over_q():
    rng = random.Random(1)
    for _ in range(250):
        f, lc, parts = random_case(rng, lambda r: Fraction(r.randint(-5, 5), r.randint(1, 3)),
                                   Fraction(1), 4, rng.randint(0, 5))
        got_lc, got = yun(f)
        assert got_lc == lc and got == parts
        check(f, got_lc, got, Fraction(1))


def test_over_z_monic_parts_are_integral():
    rng = random.Random(2)
    for _ in range(250):
        f, lc, parts = random_case(rng, lambda r: r.choice([1, -1, 2, 3]), 1, 3, rng.randint(0, 5),
                                   integral=True)
        f = [int(c) for c in f]
        got_lc, got = yun(f)
        assert got_lc == lc
        for a in got:
            assert all(Fraction(c).denominator == 1 for c in a)
        check([Fraction(c) for c in f], got_lc, got, Fraction(1))


@pytest.mark.parametrize("p", [2, 3, 7, 998244353])
def test_over_fp_with_degree_below_p(p):
    rng = random.Random(p)
    one = Fp(1, p)
    for _ in range(150):
        f = strip([Fp(rng.randrange(p), p) for _ in range(rng.randint(1, min(p, 9)))])
        if not f:
            continue
        lc, a = yun(f)
        check(f, lc, a, one)
        if len(f) > 1:
            assert a == musser(f)
        g, glc, parts = random_case(rng, lambda r: Fp(r.randrange(1, p), p), one,
                                    3, rng.randint(0, 3), p)
        if len(g) - 1 < p:
            assert yun(g) == (glc, parts)


def test_random_rational_polynomials_against_musser():
    rng = random.Random(3)
    for _ in range(300):
        base = strip([Fraction(rng.randint(-3, 3)) for _ in range(rng.randint(2, 4))])
        if len(base) < 2:
            continue
        f = mul(mul(base, base), strip([Fraction(rng.randint(-3, 3)) for _ in range(3)]) or [Fraction(1)])
        lc, a = yun(f)
        check(f, lc, a, Fraction(1))
        assert a == musser(f)
