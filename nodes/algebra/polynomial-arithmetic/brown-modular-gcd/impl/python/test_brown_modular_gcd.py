# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brown-modular-gcd/. The authors are listed in prov/02TR5G.jsonl.

import random
from fractions import Fraction
from math import gcd

import pytest

from brown_modular_gcd import brown_gcd, gcd_mod_p, word_primes


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


# Independent oracle: the Euclidean algorithm over a field (Fraction or ModP).
def ref_trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def ref_rem(a, b):
    a = ref_trim(a)
    while len(a) >= len(b):
        c = a[-1] / b[-1]
        s = len(a) - len(b)
        a = ref_trim([a[i] - (c * b[i - s] if i >= s else 0) for i in range(len(a))])
    return a


def ref_monic_gcd(a, b):
    a, b = ref_trim(a), ref_trim(b)
    while b:
        a, b = b, ref_rem(a, b)
    if not a:
        return []
    lead = a[-1]
    return [x / lead for x in a]


def ref_mul(a, b):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            out[i + j] += a[i] * b[j]
    return ref_trim(out)


def ref_int_gcd(f, g):
    """gcd in Z[x] = gcd of contents times the primitive part of the gcd over Q."""
    f, g = ref_trim(f), ref_trim(g)
    if not f or not g:
        h = f or g
        return [-x for x in h] if h and h[-1] < 0 else h
    cf = cg = 0
    for x in f:
        cf = gcd(cf, x)
    for x in g:
        cg = gcd(cg, x)
    q = ref_monic_gcd([Fraction(x) for x in f], [Fraction(x) for x in g])
    den = 1
    for x in q:
        den = den * x.denominator // gcd(den, x.denominator)
    ints = [int(x * den) for x in q]
    c = 0
    for x in ints:
        c = gcd(c, x)
    return [gcd(cf, cg) * x // c for x in ints]


def small_primes():
    n = 2
    while True:
        if all(n % q for q in range(2, int(n ** 0.5) + 1)):
            yield n
        n += 1


def rand_poly(rng, deg, bound, monic=False):
    a = [rng.randint(-bound, bound) for _ in range(deg + 1)]
    if monic:
        a[-1] = 1
    while a[-1] == 0:
        a[-1] = rng.randint(-bound, bound)
    return a


def test_worked_example():
    log = []
    f = [3, 1, 6, 2]
    g = [-1, 3, -2, 6]
    assert brown_gcd(f, g, [5, 7, 11, 13], log) == [1, 0, 2]
    assert log == [(5, 3, "restarted"), (7, 2, "restarted"), (11, 2, "accepted")]
    assert ref_int_gcd(f, g) == [1, 0, 2]


@pytest.mark.parametrize("which", ["word", "small", "ntt"])
def test_random_against_rational_euclid(which):
    rng = random.Random({"word": 1, "small": 2, "ntt": 3}[which])
    for _ in range(60):
        G = rand_poly(rng, rng.randint(0, 4), 9, monic=rng.random() < 0.3)
        A = rand_poly(rng, rng.randint(0, 5), 9)
        B = rand_poly(rng, rng.randint(0, 5), 9)
        f = ref_mul([rng.choice([1, 2, -3, 6])], ref_mul(G, A))
        g = ref_mul([rng.choice([1, 4, -9])], ref_mul(G, B))
        if which == "word":
            primes = word_primes()
        elif which == "small":
            primes = small_primes()
        else:
            primes = iter([998244353, 3, 7, 2] + list(_take(word_primes(2 ** 20), 40)))
        assert brown_gcd(f, g, primes) == ref_int_gcd(f, g)


def _take(it, k):
    out = []
    for x in it:
        out.append(x)
        if len(out) == k:
            break
    return out


def test_unlucky_primes_are_skipped():
    # x + 3 and x - 2 agree modulo 5, so 5 is unlucky for this pair
    f = ref_mul([1, 0, 1], [3, 1])
    g = ref_mul([1, 0, 1], [-2, 1])
    log = []
    assert brown_gcd(f, g, [5, 2, 3, 7, 11, 13, 17], log) == [1, 0, 1]
    assert log[0] == (5, 3, "restarted")
    # many primes in a row are unlucky: x and x + 30 agree modulo 2, 3 and 5
    f = ref_mul([1, 1, 1], [0, 1])
    g = ref_mul([1, 1, 1], [30, 1])
    log = []
    assert brown_gcd(f, g, small_primes(), log) == [1, 1, 1]
    assert [e[1] for e in log[:3]] == [3, 3, 3]


@pytest.mark.parametrize("p", [2, 3, 7, 998244353])
def test_gcd_mod_p(p):
    rng = random.Random(p % 1000)
    for _ in range(80):
        a = [rng.randrange(p) for _ in range(rng.randint(0, 7))]
        b = [rng.randrange(p) for _ in range(rng.randint(0, 7))]
        if rng.random() < 0.5:
            c = [rng.randrange(p) for _ in range(rng.randint(1, 3))]
            a, b = ref_mul(a, c), ref_mul(b, c)
        want = ref_monic_gcd([ModP(x, p) for x in a], [ModP(x, p) for x in b])
        assert gcd_mod_p(a, b, p) == [x.v for x in want]


def test_edge_cases():
    assert brown_gcd([], []) == []
    assert brown_gcd([0, 0], [0]) == []
    assert brown_gcd([], [-2, -4]) == [2, 4]
    assert brown_gcd([3, 6], []) == [3, 6]
    assert brown_gcd([6], [4]) == [2]
    assert brown_gcd([6, 12], [4, 0, 8]) == [2]
    assert brown_gcd([5], [1, 1]) == [1]
    # leading zero coefficients are stripped
    assert brown_gcd([1, 0, -1, 0, 0], [1, 1, 0]) == [1, 1]
    # coprime, equal, and dividing inputs
    assert brown_gcd([1, 1], [-1, 1]) == [1]
    assert brown_gcd([-2, 0, -4], [-2, 0, -4]) == [2, 0, 4]
    assert brown_gcd([-1, 0, 1], [1, 1]) == [1, 1]
    # negative leading coefficients give a positive gcd
    assert brown_gcd([1, -1], [-1, 0, 1]) == [-1, 1]
    # contents: gcd(6 (x + 1), 4 (x + 1) (x - 1)) = 2 (x + 1)
    assert brown_gcd([6, 6], [-4, 0, 4]) == [2, 2]
    # very different degrees
    big = ref_mul([1, 1], [1] * 30)
    assert brown_gcd(big, [3, 3]) == [1, 1]
    # degree 1 non-monic gcd
    assert brown_gcd(ref_mul([1, 3], [5, 7]), ref_mul([1, 3], [-2, 0, 9])) == [1, 3]


def test_large_coefficients_need_many_primes():
    rng = random.Random(9)
    for _ in range(10):
        G = rand_poly(rng, 3, 10 ** 30)
        f = ref_mul(G, rand_poly(rng, 3, 10 ** 20))
        g = ref_mul(G, rand_poly(rng, 2, 10 ** 20))
        log = []
        assert brown_gcd(f, g, small_primes(), log) == ref_int_gcd(f, g)
        assert len(log) > 10


def test_runs_out_of_primes():
    with pytest.raises(ValueError):
        brown_gcd([1, 0, 1], [1, 0, 1], [2])
