# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berkowitz-algorithm/. The authors are listed in prov/PM8CKR.jsonl.

import random
from itertools import combinations, permutations

from berkowitz_algorithm import berkowitz, berkowitz_determinant


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


def charpoly_minors(a):
    """Coefficients of det(xI - a), highest first, from sums of principal minors."""
    n = len(a)
    out = [1]
    for k in range(1, n + 1):
        e = sum(det_leibniz([[a[i][j] for j in s] for i in s]) for s in combinations(range(n), k))
        out.append((-1) ** k * e)
    return out


class ModN:
    """An element of Z/NZ for any N >= 2, a ring that may have zero divisors."""

    def __init__(self, v: int, n: int) -> None:
        self.v, self.n = v % n, n

    def __add__(self, o):
        return ModN(self.v + o.v, self.n)

    def __sub__(self, o):
        return ModN(self.v - o.v, self.n)

    def __mul__(self, o):
        return ModN(self.v * o.v, self.n)

    def __neg__(self):
        return ModN(-self.v, self.n)


def matmul(x, y):
    return [[sum(x[i][k] * y[k][j] for k in range(len(y))) for j in range(len(y[0]))] for i in range(len(x))]


def test_examples() -> None:
    assert berkowitz([[2, 1, 0], [1, 3, 1], [0, 1, 4]]) == [1, -9, 24, -18]
    assert berkowitz([[1, 2], [3, 4]]) == [1, -5, -2]
    assert berkowitz([[0, 0, -5], [1, 0, 2], [0, 1, 0]]) == [1, 0, -2, 5]
    assert berkowitz_determinant([[0, 1, 2, 3], [1, 0, 1, 2], [2, 1, 0, 1], [3, 2, 1, 0]]) == -12


def test_edges() -> None:
    assert berkowitz([]) == [1]
    assert berkowitz_determinant([]) == 1
    assert berkowitz([[7]]) == [1, -7]
    assert berkowitz_determinant([[7]]) == 7
    assert berkowitz([[0, 0], [0, 0]]) == [1, 0, 0]
    assert berkowitz([[0, 1], [0, 0]]) == [1, 0, 0]


def test_random_integer() -> None:
    rng = random.Random(1984)
    for _ in range(600):
        n = rng.randint(1, 5)
        a = [[rng.randint(-4, 4) for _ in range(n)] for _ in range(n)]
        if rng.random() < 0.2:
            a[rng.randrange(n)] = [0] * n
        if rng.random() < 0.2:
            for i in range(n):
                a[i][0] = 0
        c = berkowitz(a)
        assert c == charpoly_minors(a)
        assert berkowitz_determinant(a) == det_leibniz(a)
        # Cayley-Hamilton: c(A) = 0
        acc = [[0] * n for _ in range(n)]
        for coef in c:
            acc = matmul(acc, a)
            for i in range(n):
                acc[i][i] += coef
        assert acc == [[0] * n for _ in range(n)]


def test_ring_with_zero_divisors() -> None:
    rng = random.Random(6)
    for modulus in (4, 6, 12, 2**64):
        for _ in range(150):
            n = rng.randint(1, 5)
            a = [[rng.randrange(modulus) for _ in range(n)] for _ in range(n)]
            got = berkowitz([[ModN(x, modulus) for x in row] for row in a], ModN(1, modulus))
            assert [x.v for x in got] == [x % modulus for x in charpoly_minors(a)]


def test_large_entries() -> None:
    rng = random.Random(9)
    for _ in range(15):
        n = 5
        a = [[rng.randint(-10**25, 10**25) for _ in range(n)] for _ in range(n)]
        assert berkowitz(a) == charpoly_minors(a)
