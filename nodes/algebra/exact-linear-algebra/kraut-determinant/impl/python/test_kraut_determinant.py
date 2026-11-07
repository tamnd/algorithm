# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kraut-determinant/. The authors are listed in prov/VFMNY1.jsonl.

import random
from fractions import Fraction
from itertools import permutations

from kraut_determinant import crout, kraut_determinant


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
    """An element of Z/pZ, enough of a field for the algorithm."""

    def __init__(self, v: int, p: int) -> None:
        self.v, self.p = v % p, p

    def __sub__(self, o):
        return ModP(self.v - o.v, self.p)

    def __mul__(self, o):
        return ModP(self.v * o.v, self.p)

    def __truediv__(self, o):
        return ModP(self.v * pow(o.v, self.p - 2, self.p), self.p)

    def __neg__(self):
        return ModP(-self.v, self.p)

    def __eq__(self, o):
        if isinstance(o, ModP):
            return self.v == o.v
        return self.v == o % self.p

    def __ne__(self, o):
        return not self == o


def check_factorization(a, res):
    w, perm, s = res
    n = len(a)
    lo = [[w[i][j] if j <= i else 0 for j in range(n)] for i in range(n)]
    up = [[1 if i == j else (w[i][j] if j > i else 0) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            assert sum(lo[i][k] * up[k][j] for k in range(n)) == a[perm[i]][j]
    inv = sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])
    assert s == (-1) ** inv


def test_examples() -> None:
    a = [[0, 1, 2, 3], [1, 0, 1, 2], [2, 1, 0, 1], [3, 2, 1, 0]]
    assert kraut_determinant(a) == -12
    w, perm, s = crout(a)
    assert perm == [1, 0, 2, 3] and s == -1
    assert [w[j][j] for j in range(4)] == [1, 1, -4, -3]
    assert kraut_determinant([[2, 1, 0], [1, 3, 1], [0, 1, 4]]) == 18


def test_edges() -> None:
    assert kraut_determinant([]) == 1
    assert kraut_determinant([[5]]) == 5
    assert kraut_determinant([[0]]) == 0
    assert kraut_determinant([[0, 1], [1, 0]]) == -1
    assert kraut_determinant([[1, 2], [2, 4]]) == 0
    assert kraut_determinant([[0, 0, 0], [1, 2, 3], [4, 5, 6]]) == 0
    assert crout([[0, 0], [0, 1]]) is None


def test_random_rational() -> None:
    rng = random.Random(1941)
    for _ in range(800):
        n = rng.randint(1, 6)
        a = [[rng.randint(-4, 4) for _ in range(n)] for _ in range(n)]
        if rng.random() < 0.2:
            a[rng.randrange(n)] = [0] * n
        if rng.random() < 0.3:
            a[0][0] = 0
        if rng.random() < 0.2:
            for i in range(n):
                a[i][rng.randrange(n)] = 0
        d = det_leibniz(a)
        assert kraut_determinant(a) == d
        res = crout(a)
        assert (res is None) == (d == 0)
        if res is not None:
            check_factorization(a, res)


def test_random_mod_p() -> None:
    rng = random.Random(23)
    for p in (2, 3, 5, 7, 101):
        for _ in range(150):
            n = rng.randint(1, 5)
            a = [[rng.randrange(p) for _ in range(n)] for _ in range(n)]
            got = kraut_determinant([[ModP(x, p) for x in row] for row in a])
            assert got.v == det_leibniz(a) % p


def test_fractions_and_large_entries() -> None:
    rng = random.Random(8)
    for _ in range(20):
        n = 5
        a = [[rng.randint(-10**30, 10**30) for _ in range(n)] for _ in range(n)]
        assert kraut_determinant(a) == det_leibniz(a)
        b = [[Fraction(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(4)] for _ in range(4)]
        assert kraut_determinant(b) == det_leibniz(b)
