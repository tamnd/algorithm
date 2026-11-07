# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pseudo-division/. The authors are listed in prov/XBNRYF.jsonl.

import random
from fractions import Fraction

import pytest

from pseudo_division import pseudo_divmod


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


PRIMES = [2, 3, 7, 998244353]


def scal(c, a):
    return strip([c * x for x in a])


def check_identity(f, g, q, r):
    f, g = strip(f), strip(g)
    m, n = len(f) - 1, len(g) - 1
    lead = g[-1]
    e = max(m - n + 1, 0)
    lhs = scal(lead**e if not isinstance(lead, Fp) else Fp(pow(lead.v, e, lead.p), lead.p), f)
    assert add(mul(q, g), r) == lhs
    assert len(r) - 1 < n


def rand_poly(rng, mk, deg, monic=False):
    a = [mk() for _ in range(deg + 1)]
    if monic:
        a[-1] = a[-1] * 0 + 1
    return a


def test_knuth_example():
    u = [-5, 2, 8, -3, -3, 0, 1, 0, 1]
    v = [21, -9, -4, 0, 5, 0, 3]
    assert pseudo_divmod(u, v) == ([-6, 0, 9], [-9, 0, 3, 0, -15])


def test_edge_cases():
    with pytest.raises(ZeroDivisionError):
        pseudo_divmod([1, 2], [])
    with pytest.raises(ZeroDivisionError):
        pseudo_divmod([1, 2], [0, 0])
    assert pseudo_divmod([], [1, 2]) == ([], [])
    assert pseudo_divmod([3, 1], [0, 0, 5]) == ([], [3, 1])  # m < n
    assert pseudo_divmod([4, 6, 2], [2]) == ([16, 24, 8], [])  # n = 0: q = lc^m f
    assert pseudo_divmod([1, 2, 0, 0], [1, 1]) == ([2], [-1])  # leading zeros
    assert pseudo_divmod([7], [3]) == ([7], [])
    # monic divisor: ordinary division
    assert pseudo_divmod([-1, 0, 0, 1], [-1, 1]) == ([1, 1, 1], [])


@pytest.mark.parametrize("seed", [11, 12])
def test_against_field_division_over_q(seed):
    rng = random.Random(seed)
    for _ in range(250):
        m, n = rng.randint(0, 9), rng.randint(0, 7)
        f = rand_poly(rng, lambda: rng.randint(-9, 9), m)
        g = rand_poly(rng, lambda: rng.randint(-9, 9), n)
        if not strip(g):
            continue
        q, r = pseudo_divmod(f, g)
        assert all(isinstance(c, int) for c in q + r)
        fs, gs = strip(f), strip(g)
        e = max(len(fs) - len(gs) + 1, 0)
        lead = Fraction(gs[-1]) ** e
        qq, rr = ref_divmod([Fraction(c) for c in fs], [Fraction(c) for c in gs])
        assert q == scal(lead, qq) and r == scal(lead, rr)
        check_identity(f, g, q, r)


@pytest.mark.parametrize("p", PRIMES)
def test_over_prime_fields(p):
    rng = random.Random(p)
    for _ in range(150):
        m, n = rng.randint(0, 10), rng.randint(0, 6)
        mk = lambda: Fp(rng.randrange(p), p)
        f = rand_poly(rng, mk, m)
        g = rand_poly(rng, mk, n, monic=rng.random() < 0.3)
        if not strip(g):
            continue
        q, r = pseudo_divmod(f, g)
        fs, gs = strip(f), strip(g)
        e = max(len(fs) - len(gs) + 1, 0)
        lead = Fp(pow(gs[-1].v, e, p), p)
        qq, rr = ref_divmod(fs, gs)
        assert q == scal(lead, qq) and r == scal(lead, rr)


def test_over_rationals_and_very_different_degrees():
    rng = random.Random(5)
    for _ in range(40):
        f = rand_poly(rng, lambda: Fraction(rng.randint(-5, 5), rng.randint(1, 5)), rng.randint(30, 40))
        g = rand_poly(rng, lambda: Fraction(rng.randint(1, 5), rng.randint(1, 5)), rng.randint(0, 2))
        q, r = pseudo_divmod(f, g)
        check_identity(f, g, q, r)


def test_identity_over_ring_with_zero_divisors():
    # Z/8Z is not a domain; the identity still holds when lc(g) is a zero divisor
    rng = random.Random(8)
    for _ in range(200):
        f = rand_poly(rng, lambda: Fp(rng.randrange(8), 8), rng.randint(0, 7))
        g = rand_poly(rng, lambda: Fp(rng.randrange(8), 8), rng.randint(0, 4))
        if not strip(g):
            continue
        q, r = pseudo_divmod(f, g)
        check_identity(f, g, q, r)


def test_large_integers_stay_exact():
    rng = random.Random(9)
    for _ in range(30):
        f = rand_poly(rng, lambda: rng.randint(-10**30, 10**30), 12)
        g = rand_poly(rng, lambda: rng.randint(1, 10**20), 5)
        q, r = pseudo_divmod(f, g)
        check_identity(f, g, q, r)
