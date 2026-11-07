# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subresultant-gcd/. The authors are listed in prov/DB9KV8.jsonl.

import math
import random
from fractions import Fraction

import pytest

from subresultant_gcd import subresultant_gcd, subresultant_prs


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


def ref_gcd_field(f, g):
    """Monic gcd over a field by Euclid with the reference division."""
    a, b = strip(f), strip(g)
    while b:
        a, b = b, ref_divmod(a, b)[1]
    if not a:
        return []
    inv = 1 / a[-1]
    return [x * inv for x in a]


def ref_gcd_z(f, g):
    """gcd in Z[x]: the gcd over Q made primitive, times the gcd of the contents."""
    f, g = strip(f), strip(g)
    if not f and not g:
        return []
    h = ref_gcd_field([Fraction(x) for x in f], [Fraction(x) for x in g])
    den = math.lcm(*[x.denominator for x in h])
    hz = [int(x * den) for x in h]
    c = math.gcd(*hz)
    hz = [x // c for x in hz]
    cf = math.gcd(*f) if f else 0
    cg = math.gcd(*g) if g else 0
    return [math.gcd(cf, cg) * x for x in hz]


def det(M):
    """Determinant over a field (Fraction or Fp) by elimination."""
    M = [row[:] for row in M]
    n = len(M)
    if n == 0:
        return 1
    d = M[0][0] * 0 + 1
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return d * 0
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d = d * M[c][c]
        inv = 1 / M[c][c]
        for r in range(c + 1, n):
            k = M[r][c] * inv
            if k != 0:
                for j in range(c, n):
                    M[r][j] = M[r][j] - k * M[c][j]
    return d


def subres(f, g, j):
    """The j-th subresultant of f (degree m) and g (degree n), j < n, by determinants."""
    m, n = len(f) - 1, len(g) - 1
    cols = m + n - j
    rows = []
    for i in range(n - j):
        row = [f[0] * 0] * cols
        for k, c in enumerate(f):
            row[cols - 1 - (k + n - j - 1 - i)] = c
        rows.append(row)
    for i in range(m - j):
        row = [f[0] * 0] * cols
        for k, c in enumerate(g):
            row[cols - 1 - (k + m - j - 1 - i)] = c
        rows.append(row)
    lead = m + n - 2 * j - 1
    out = []
    for i in range(j + 1):
        col = cols - 1 - i
        out.append(det([r[:lead] + [r[col]] for r in rows]))
    return strip(out)


def rand_poly(rng, mk, deg):
    a = [mk() for _ in range(deg + 1)]
    while a and a[-1] == 0:
        a[-1] = mk()
    return a


def test_knuth_example():
    u = [-5, 2, 8, -3, -3, 0, 1, 0, 1]
    v = [21, -9, -4, 0, 5, 0, 3]
    seq = subresultant_prs(u, v)
    assert seq[2:] == [[-9, 0, 3, 0, -15], [-245, 125, 65], [12300, -9326], [260708]]
    assert subresultant_gcd(u, v) == [1]


def test_edge_cases():
    assert subresultant_gcd([], []) == []
    assert subresultant_gcd([0, 0], [0]) == []
    assert subresultant_gcd([], [-6, -4]) == [6, 4]
    assert subresultant_gcd([2, 2], []) == [2, 2]
    assert ref_gcd_z([], [-6, -4]) == [6, 4]
    assert subresultant_gcd([4], [6]) == [2]
    assert subresultant_gcd([4], [3, 6]) == [1]
    assert subresultant_gcd([6, 12, 6], [-4, 0, 4]) == [2, 2]
    assert subresultant_gcd([-1, 0, 0, 0, 1], [1, 2, 2, 1]) == [1, 1]
    assert subresultant_gcd([1, 1, 0, 0], [2, 2]) == [1, 1]  # leading zeros
    assert subresultant_gcd([-2, 1], [-2, 1]) == [-2, 1]
    with pytest.raises(ValueError):
        subresultant_prs([1, 1], [1, 1, 1])


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_gcd_against_rational_euclid(seed):
    rng = random.Random(seed)
    for _ in range(200):
        mk = lambda: rng.randint(-6, 6)
        h = rand_poly(rng, mk, rng.randint(0, 3))
        f = mul(h, rand_poly(rng, mk, rng.randint(0, 5)))
        g = mul(h, rand_poly(rng, mk, rng.randint(0, 5)))
        if rng.random() < 0.3:
            g = rand_poly(rng, mk, rng.randint(0, 6))
        f = [rng.choice([1, 1, 2, 3]) * x for x in f]
        assert subresultant_gcd(f, g) == ref_gcd_z(f, g)


def test_very_different_degrees_and_large_coefficients():
    rng = random.Random(4)
    for _ in range(10):
        h = rand_poly(rng, lambda: rng.randint(-10**6, 10**6), 2)
        f = mul(h, rand_poly(rng, lambda: rng.randint(-99, 99), 20))
        g = mul(h, rand_poly(rng, lambda: rng.randint(-99, 99), 1))
        assert subresultant_gcd(f, g) == ref_gcd_z(f, g)


def check_prs_against_determinants(f, g):
    seq = subresultant_prs(f, g)
    for i in range(2, len(seq)):
        j = len(seq[i - 1]) - 2  # deg of the member before, minus 1
        s = subres(strip(f), strip(g), j)
        assert seq[i] == s or seq[i] == [-x for x in s]
    return seq


@pytest.mark.parametrize("seed", [5, 6])
def test_prs_members_are_subresultants_over_z(seed):
    rng = random.Random(seed)
    for _ in range(40):
        n = rng.randint(1, 5)
        m = n + rng.randint(0, 3)
        mk = lambda: rng.randint(-5, 5)
        f, g = rand_poly(rng, mk, m), rand_poly(rng, mk, n)
        seq = [[Fraction(x) for x in p] for p in check_prs_against_determinants(
            [Fraction(x) for x in f], [Fraction(x) for x in g])]
        assert subresultant_prs(f, g) == [[int(x) for x in p] for p in seq]


@pytest.mark.parametrize("p", PRIMES)
def test_over_prime_fields(p):
    rng = random.Random(p)
    for _ in range(40):
        mk = lambda: Fp(rng.randrange(p), p)
        h = rand_poly(rng, mk, rng.randint(0, 2))
        f = mul(h, rand_poly(rng, mk, rng.randint(1, 4)))
        g = mul(h, rand_poly(rng, mk, rng.randint(0, 3)))
        f, g = strip(f), strip(g)
        if not f or not g:
            continue
        if len(f) < len(g):
            f, g = g, f
        seq = check_prs_against_determinants(f, g)
        last = seq[-1]
        expect = ref_gcd_field(f, g)
        assert [x * (1 / last[-1]) for x in last] == expect or (len(last) == 1 and expect == [1])
