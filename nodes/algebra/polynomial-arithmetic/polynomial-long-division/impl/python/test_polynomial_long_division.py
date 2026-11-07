# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polynomial-long-division/. The authors are listed in prov/0Q78BZ.jsonl.

import random
from fractions import Fraction

import pytest

from polynomial_long_division import polynomial_long_division


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


def ref_divmod(f, g, inv_lc):
    """Independent reference: the quotient from the reversal and a power series inverse."""
    f, g = strip(f), strip(g)
    m, n = len(f) - 1, len(g) - 1
    if m < n:
        return [], f
    k = m - n + 1
    rf, rg = f[::-1], g[::-1]
    h = [inv_lc]
    for i in range(1, k):
        s = 0
        for j in range(1, min(i, n) + 1):
            s = s + rg[j] * h[i - j]
        h.append(-s * inv_lc)
    rq = [0] * k
    for i in range(k):
        for j in range(i + 1):
            if i - j < len(h) and j < len(rf):
                rq[i] = rq[i] + rf[j] * h[i - j]
    q = strip(rq[::-1])
    r = add(f, [-c for c in mul(q, g)])
    return q, r


def check(f, g, inv_lc):
    q, r = polynomial_long_division(f, g)
    assert q == strip(q) and r == strip(r)
    assert len(r) < len(strip(g))
    assert add(mul(q, g), r) == strip(f)
    rq, rr = ref_divmod(f, g, inv_lc)
    assert q == rq and r == rr


def test_example() -> None:
    q, r = polynomial_long_division([5, -1, 0, 3, 2], [1, 1, 1])
    assert q == [-3, 1, 2] and r == [8, 1]


def test_example_f7() -> None:
    p = 7
    f = [Fp(c, p) for c in [1, 0, 3, 0, 1, 4]]
    g = [Fp(c, p) for c in [3, 0, 2]]
    q, r = polynomial_long_division(f, g)
    assert q == [6, 4, 4, 2] and r == [4, 2]


def test_edges() -> None:
    assert polynomial_long_division([], [1, 1]) == ([], [])
    assert polynomial_long_division([1, 1], [0, 0, 0, 1]) == ([], [1, 1])
    assert polynomial_long_division([4, 5, 6], [1]) == ([4, 5, 6], [])
    assert polynomial_long_division([4, 5, 6], [-1]) == ([-4, -5, -6], [])
    assert polynomial_long_division([3, 2, 0, 0], [1, 1, 0]) == ([2], [1])
    assert polynomial_long_division([7], [7 * Fraction(1)]) == ([1], [])
    q, r = polynomial_long_division([Fraction(1), 0, 1], [Fraction(2), Fraction(3)])
    assert add(mul(q, [2, 3]), r) == [1, 0, 1] and len(r) <= 1
    # a divisor of degree 0 that is a zero after stripping
    with pytest.raises(ZeroDivisionError):
        polynomial_long_division([1, 2], [0, 0])
    with pytest.raises(ZeroDivisionError):
        polynomial_long_division([1, 2], [])
    # over Z the leading coefficient must be a unit
    with pytest.raises(ValueError):
        polynomial_long_division([0, 0, 1], [0, 2])


def test_division_by_linear_gives_value() -> None:
    f = [5, -1, 0, 3, 2]
    for a in range(-5, 6):
        _, r = polynomial_long_division(f, [-a, 1])
        val = sum(c * a**i for i, c in enumerate(f))
        assert r == strip([val])


def test_random_integers_unit_leading() -> None:
    rng = random.Random(4061)
    for _ in range(600):
        f = [rng.randint(-20, 20) for _ in range(rng.randint(0, 12))]
        g = [rng.randint(-20, 20) for _ in range(rng.randint(0, 7))] + [rng.choice([1, -1])]
        g += [0] * rng.randint(0, 2)  # zero top coefficients that must be stripped
        check(f, g, strip(g)[-1])


def test_random_fractions() -> None:
    rng = random.Random(4062)
    for _ in range(400):
        f = [Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(rng.randint(0, 10))]
        g = [Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(rng.randint(0, 6))]
        g.append(Fraction(rng.choice([-3, -2, 1, 2, 5]), rng.randint(1, 3)))
        check(f, g, 1 / g[-1])


@pytest.mark.parametrize("p", [2, 3, 7, 998244353])
def test_random_mod_p(p: int) -> None:
    rng = random.Random(4063 + p)
    for _ in range(300):
        f = [Fp(rng.randrange(p), p) for _ in range(rng.randint(0, 12))]
        g = [Fp(rng.randrange(p), p) for _ in range(rng.randint(0, 6))]
        g.append(Fp(rng.randrange(1, p), p))
        check(f, g, 1 / g[-1])


def test_very_different_degrees() -> None:
    rng = random.Random(4064)
    f = [Fraction(rng.randint(-5, 5)) for _ in range(200)] + [Fraction(1)]
    check(f, [Fraction(3), Fraction(-2)], Fraction(-1, 2))
    g = [Fraction(rng.randint(-5, 5)) for _ in range(150)] + [Fraction(7)]
    check(f, g, Fraction(1, 7))
    check(g, f, Fraction(1))
