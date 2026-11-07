# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brent-kung-composition/. The authors are listed in prov/48QJRY.jsonl.

import random
from fractions import Fraction

import pytest

from brent_kung_composition import block_size, compose_mod, compose_mod_horner, schoolbook_mul


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


# Independent oracle: expand f(g) in full by schoolbook products, then reduce
# by schoolbook long division with the inverse of the leading coefficient.


def strip(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def full_compose(f, g, zero):
    out = []
    pw = [zero + 1]
    for c in f:
        term = [c * x for x in pw]
        if len(out) < len(term):
            out += [zero] * (len(term) - len(out))
        for i, x in enumerate(term):
            out[i] = out[i] + x
        pw = schoolbook_mul(pw, g) if g else []
        if not pw:
            pw = []
    return strip(out)


def long_rem(a, h, inv):
    a = list(a)
    n = len(h) - 1
    for d in range(len(a) - 1, n - 1, -1):
        c = a[d] * inv
        for i in range(n + 1):
            a[d - n + i] = a[d - n + i] - c * h[i]
    return strip(a[:n])


def oracle(f, g, h, zero, inv):
    h = strip(h)
    if len(h) == 1:
        return []
    return long_rem(full_compose(strip(f), strip(g), zero), h, inv)


PRIMES = [2, 3, 7, 998244353]


def test_page_example():
    st = {}
    f, g, h = [1, 2, 3, 4], [0, 1, 1], [-2, 0, 0, 0, 1]
    assert compose_mod(f, g, h, stats=st) == [31, 26, 13, 10]
    assert st == {"mulmod": 2, "k": 2, "m": 2}
    # the intermediate values of the trace
    g2 = long_rem(schoolbook_mul(g, g), h, 1)
    assert g2 == [2, 0, 1, 2]
    c1 = [3, 4, 4]
    c0 = [1, 2, 2]
    s = long_rem(schoolbook_mul(c1, g2), h, 1)
    assert s == [30, 24, 11, 10]
    assert [x + y for x, y in zip(s, c0 + [0])] == [31, 26, 13, 10]


def test_edge_cases():
    h = [-2, 0, 0, 0, 1]
    assert compose_mod([], [1, 1], h) == []
    assert compose_mod([5], [1, 1], h) == [5]
    assert compose_mod([0, 0, 0], [1, 1], h) == []
    assert compose_mod([1, 2, 3], [], h) == [1]
    assert compose_mod([1, 2, 3], [1, 2], [7]) == []
    assert compose_mod([1, 2, 3], [1, 2], [1]) == []
    # leading zeros in all three inputs are stripped
    assert compose_mod([1, 2, 3, 0, 0], [0, 1, 1, 0], h + [0, 0]) == compose_mod([1, 2, 3], [0, 1, 1], h)
    # degree 1 modulus: f(g) mod (x - a) is the constant f(g(a))
    assert compose_mod([1, 2, 3], [4, 5], [-2, 1]) == [1 + 2 * 14 + 3 * 14 * 14]
    # g of higher degree than h is reduced first
    assert compose_mod([0, 1], [1, 2, 3, 4, 5, 6], h) == oracle([0, 1], [1, 2, 3, 4, 5, 6], h, 0, 1)
    # leading coefficient -1 is a unit of Z
    assert compose_mod([1, 1, 1], [0, 1, 1], [2, 0, -1]) == oracle([1, 1, 1], [0, 1, 1], [2, 0, -1], 0, -1)
    with pytest.raises(ValueError):
        compose_mod([1, 1, 1], [0, 1], [1, 0, 2])
    with pytest.raises(ZeroDivisionError):
        compose_mod([1, 1], [0, 1], [0, 0])


def test_over_z_random():
    rng = random.Random(1)
    for _ in range(100):
        n = rng.randint(1, 25)
        h = [rng.randint(-5, 5) for _ in range(n)] + [rng.choice([1, -1])]
        f = [rng.randint(-9, 9) for _ in range(rng.randint(0, n + 4))]
        g = [rng.randint(-3, 3) for _ in range(rng.randint(0, n + 3))]
        want = oracle(f, g, h, 0, h[-1])
        assert compose_mod(f, g, h) == want
        assert compose_mod_horner(f, g, h) == want


@pytest.mark.parametrize("p", PRIMES)
def test_over_z_mod_p(p):
    rng = random.Random(p)
    zero = ModP(0, p)
    for _ in range(40):
        n = rng.randint(1, 25)
        lc = rng.randrange(1, p)
        h = [ModP(rng.randrange(p), p) for _ in range(n)] + [ModP(lc, p)]
        f = [ModP(rng.randrange(p), p) for _ in range(rng.randint(0, n + 2))]
        g = [ModP(rng.randrange(p), p) for _ in range(rng.randint(0, n + 2))]
        want = oracle(f, g, h, zero, ModP(pow(lc, -1, p), p))
        assert compose_mod(f, g, h) == want


def test_over_fractions_non_monic():
    rng = random.Random(5)
    zero = Fraction(0)
    for _ in range(30):
        n = rng.randint(1, 12)
        h = [Fraction(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(n)] + [Fraction(rng.randint(1, 5), rng.randint(1, 3))]
        f = [Fraction(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(rng.randint(0, n + 1))]
        g = [Fraction(rng.randint(-3, 3), rng.randint(1, 3)) for _ in range(rng.randint(0, n))]
        assert compose_mod(f, g, h) == oracle(f, g, h, zero, 1 / h[-1])


def test_counts_and_larger_case():
    rng = random.Random(9)
    p = 998244353
    n = 64
    h = [rng.randrange(p) for _ in range(n)] + [1]
    g = [rng.randrange(p) for _ in range(n)]
    f = [rng.randrange(p) for _ in range(n)]
    hp, gp, fp = ([ModP(c, p) for c in v] for v in (h, g, f))
    st = {}
    got = compose_mod(fp, gp, hp, stats=st)
    assert got == compose_mod_horner(fp, gp, hp)
    k = block_size(n)
    assert st["k"] == 8 and st["m"] == 8
    assert st["mulmod"] == 2 * k - 2
    for N in range(1, 80):
        k = block_size(N)
        assert (k - 1) ** 2 < N <= k * k
        st = {}
        compose_mod([1] * N, [0, 1], [0, 0, 1], stats=st)
        assert st["mulmod"] <= max(2 * k - 2, 0)
