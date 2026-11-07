# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/determinant-gaussian-elimination/. The authors are listed in prov/KQ2JBB.jsonl.

import random
from fractions import Fraction
from itertools import permutations

from determinant_gaussian_elimination import determinant_gaussian_elimination as det


def det_leibniz(a):
    n = len(a)
    total = 0
    for p in permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
        t = 1
        for i in range(n):
            t *= a[p[i]][i]
        total += -t if inv % 2 else t
    return total


class ModP:
    """An element of Z/pZ for a prime p, enough for the test."""

    def __init__(self, v: int, p: int) -> None:
        self.p, self.v = p, v % p

    def _c(self, o):
        return o if isinstance(o, ModP) else ModP(o, self.p)

    def __add__(self, o):
        return ModP(self.v + self._c(o).v, self.p)

    def __sub__(self, o):
        return ModP(self.v - self._c(o).v, self.p)

    def __mul__(self, o):
        return ModP(self.v * self._c(o).v, self.p)

    __rmul__ = __mul__

    def __neg__(self):
        return ModP(-self.v, self.p)

    def __truediv__(self, o):
        return self * ModP(pow(self._c(o).v, -1, self.p), self.p)

    def __eq__(self, o):
        return self.v == self._c(o).v

    def __ne__(self, o):
        return not self == o


def test_example() -> None:
    a = [[0, 1, 2, 3], [1, 0, 1, 2], [2, 1, 0, 1], [3, 2, 1, 0]]
    assert det(a) == -12 == det_leibniz(a)


def test_edges() -> None:
    assert det([]) == 1
    assert det([[7]]) == 7 and det([[0]]) == 0
    assert det([[0, 1], [1, 0]]) == -1  # a zero pivot that needs a swap
    assert det([[1, 2], [2, 4]]) == 0
    assert det([[1, 2, 3], [0, 0, 0], [4, 5, 6]]) == 0  # a zero row
    assert det([[0, 1, 2], [0, 3, 4], [0, 5, 6]]) == 0  # a zero column
    assert det([[Fraction(1, 2), Fraction(1, 3)], [Fraction(1, 4), Fraction(1, 5)]]) == Fraction(1, 60)
    a = [[0, 1], [1, 0]]
    det(a)
    assert a == [[0, 1], [1, 0]]


def test_random_against_leibniz() -> None:
    rng = random.Random(1201)
    for _ in range(700):
        n = rng.randint(1, 5)
        a = [[rng.randint(-4, 4) for _ in range(n)] for _ in range(n)]
        if rng.random() < 0.3:  # dependent rows
            i, k = rng.randrange(n), rng.randrange(n)
            a[i] = [2 * x for x in a[k]]
        if rng.random() < 0.3:  # zeros on the diagonal force swaps
            for i in range(n):
                a[i][i] = 0
        assert det(a) == det_leibniz(a)


def test_large_entries() -> None:
    rng = random.Random(55)
    for _ in range(10):
        n = 6
        a = [[rng.randint(-10**25, 10**25) for _ in range(n)] for _ in range(n)]
        assert det(a) == det_leibniz(a)


def test_prime_field() -> None:
    rng = random.Random(9)
    for p in (2, 3, 5, 7, 101):
        for _ in range(150):
            n = rng.randint(1, 5)
            a = [[rng.randrange(p) for _ in range(n)] for _ in range(n)]
            got = det([[ModP(x, p) for x in row] for row in a])
            assert ModP(1, p) * got == ModP(det_leibniz(a), p)
