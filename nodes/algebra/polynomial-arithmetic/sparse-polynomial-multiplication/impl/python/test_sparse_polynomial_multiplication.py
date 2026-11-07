# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-polynomial-multiplication/. The authors are listed in prov/YHNK2G.jsonl.

import random
from fractions import Fraction

import pytest

from sparse_polynomial_multiplication import heap_multiply


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


def to_dense(a):
    if not a:
        return []
    z = a[0][1] * 0
    c = [z] * (a[-1][0] + 1)
    for e, v in a:
        c[e] = v
    return c


def from_dense(c):
    return [(e, v) for e, v in enumerate(c) if v != 0]


def dict_multiply(a, b):
    """Independent oracle: accumulate all products in a dictionary, then sort."""
    acc = {}
    for e, u in a:
        for f, v in b:
            acc[e + f] = acc.get(e + f, 0) + u * v
    return [(k, acc[k]) for k in sorted(acc) if acc[k] != 0]


def normalized(a):
    return all(v != 0 for _, v in a) and all(a[i][0] < a[i + 1][0] for i in range(len(a) - 1))


def rand_sparse(rng, t, maxe, coef):
    es = sorted(rng.sample(range(maxe + 1), min(t, maxe + 1)))
    out = []
    for e in es:
        v = coef()
        if v != 0:
            out.append((e, v))
    return out


def evaluate(a, x, p):
    return sum(int(v) * pow(x, e, p) for e, v in a) % p


def test_worked_examples():
    assert heap_multiply([(0, 1), (2, 1)], [(0, 1), (2, -1), (4, 1)]) == [(0, 1), (6, 1)]
    assert heap_multiply([(0, 1), (5, 2)], [(0, 3), (2, 1), (10, 1)]) == [
        (0, 3), (2, 1), (5, 6), (7, 2), (10, 1), (15, 2)]


def test_edge_cases():
    assert heap_multiply([], []) == []
    assert heap_multiply([], [(0, 1)]) == []
    assert heap_multiply([(3, 5)], []) == []
    assert heap_multiply([(0, 7)], [(0, 6)]) == [(0, 42)]
    assert heap_multiply([(0, 2)], [(1, 3), (9, -1)]) == [(1, 6), (9, -2)]
    assert heap_multiply([(4, 1)], [(0, 1), (1, 1)]) == [(4, 1), (5, 1)]
    # Total cancellation is impossible over a domain, but zero divisors give 0.
    p = 6
    assert heap_multiply([(0, 2), (1, 2)], [(3, 3)]) == [(3, 6), (4, 6)]
    two, three = Fp(2, p), Fp(3, p)
    assert heap_multiply([(0, two), (1, two)], [(3, three)]) == []
    # Very different sizes, both argument orders.
    big = [(e, 1) for e in range(0, 400, 3)]
    assert heap_multiply([(1, 1)], big) == [(e + 1, 1) for e in range(0, 400, 3)]
    assert heap_multiply(big, [(1, 1)]) == [(e + 1, 1) for e in range(0, 400, 3)]


def test_against_schoolbook_over_z():
    rng = random.Random(20261107)
    for _ in range(600):
        a = rand_sparse(rng, rng.randint(0, 8), rng.randint(0, 20), lambda: rng.randint(-3, 3))
        b = rand_sparse(rng, rng.randint(0, 8), rng.randint(0, 20), lambda: rng.randint(-3, 3))
        c = heap_multiply(a, b)
        assert normalized(c)
        assert c == from_dense(strip(mul(to_dense(a), to_dense(b))))
        assert c == heap_multiply(b, a)


@pytest.mark.parametrize("p", [2, 3, 7, 998244353])
def test_against_schoolbook_over_fp(p):
    rng = random.Random(p)
    for _ in range(300):
        a = rand_sparse(rng, rng.randint(0, 7), rng.randint(0, 15), lambda: Fp(rng.randrange(p), p))
        b = rand_sparse(rng, rng.randint(0, 7), rng.randint(0, 15), lambda: Fp(rng.randrange(p), p))
        c = heap_multiply(a, b)
        assert normalized(c)
        assert c == from_dense(strip(mul(to_dense(a), to_dense(b))))


def test_over_fraction():
    rng = random.Random(7)
    for _ in range(200):
        coef = lambda: Fraction(rng.randint(-5, 5), rng.randint(1, 4))
        a = rand_sparse(rng, rng.randint(0, 6), 12, coef)
        b = rand_sparse(rng, rng.randint(0, 6), 12, coef)
        assert heap_multiply(a, b) == from_dense(strip(mul(to_dense(a), to_dense(b))))


def test_huge_exponents_against_dictionary_and_evaluation():
    rng = random.Random(99)
    p = 998244353
    for _ in range(60):
        a = rand_sparse(rng, rng.randint(1, 40), 10**12, lambda: rng.randint(-9, 9))
        b = rand_sparse(rng, rng.randint(1, 40), 10**12, lambda: rng.randint(-9, 9))
        c = heap_multiply(a, b)
        assert c == dict_multiply(a, b)
        x = rng.randrange(p)
        assert evaluate(c, x, p) == evaluate(a, x, p) * evaluate(b, x, p) % p


def test_heap_size_bound_by_smaller_operand():
    import heapq

    sizes = []
    orig = heapq.heappush

    def spy(h, item):
        sizes.append(len(h) + 1)
        orig(h, item)

    a = [(e, 1) for e in range(0, 50, 5)]
    b = [(e, 1) for e in range(0, 3000, 7)]
    heapq.heappush = spy
    try:
        heap_multiply(b, a)
    finally:
        heapq.heappush = orig
    assert max(sizes) <= len(a)
