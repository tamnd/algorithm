# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kannan-bachem-algorithm/. The authors are listed in prov/XTZT1P.jsonl.

import random
from fractions import Fraction
from itertools import combinations, permutations
from math import gcd, isqrt

from kannan_bachem_algorithm import hermite_normal_form, kannan_bachem, xgcd


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


def det_exact(a):
    n = len(a)
    m = [[Fraction(x) for x in row] for row in a]
    d = Fraction(1)
    for c in range(n):
        p = next((i for i in range(c, n) if m[i][c]), None)
        if p is None:
            return 0
        if p != c:
            m[c], m[p] = m[p], m[c]
            d = -d
        d *= m[c][c]
        for i in range(c + 1, n):
            f = m[i][c] / m[c][c]
            if f:
                m[i] = [x - f * y for x, y in zip(m[i], m[c])]
    return d


def rank_minors(a):
    m = len(a)
    n = len(a[0]) if m else 0
    for k in range(min(m, n), 0, -1):
        for rs in combinations(range(m), k):
            for cs in combinations(range(n), k):
                if det_leibniz([[a[i][j] for j in cs] for i in rs]):
                    return k
    return 0


def matmul(u, a, n):
    return [[sum(u[i][k] * a[k][j] for k in range(len(a))) for j in range(n)] for i in range(len(u))]


def check(a, n=None):
    m = len(a)
    n = len(a[0]) if m else (n or 0)
    h, u = kannan_bachem(a)
    assert len(h) == m and len(u) == m
    assert matmul(u, a, n) == h
    assert abs(det_exact(u)) == 1
    pivots = []
    for row in h:
        lead = next((j for j in range(n) if row[j]), None)
        if lead is None:
            pivots.append(None)
            continue
        assert row[lead] > 0
        pivots.append(lead)
    nz = [p for p in pivots if p is not None]
    r = len(nz)
    assert pivots[:r] == nz and all(p is None for p in pivots[r:])  # zero rows at the bottom
    assert nz == sorted(set(nz))  # strictly increasing pivot columns
    for k, c in enumerate(nz):
        for i in range(k):
            assert 0 <= h[i][c] < h[k][c]
    bound_b = max([1] + [abs(x) for row in a for x in row])
    bound = isqrt(r ** r) * r * bound_b ** r + r * bound_b ** r if r else 0
    assert all(abs(x) <= max(bound, 0) for row in h for x in row)
    return h, r


def random_unimodular(rng, m):
    v = [[int(i == j) for j in range(m)] for i in range(m)]
    for _ in range(3 * m):
        i, j = rng.sample(range(m), 2) if m > 1 else (0, 0)
        if i == j:
            v[0] = [-x for x in v[0]]
            continue
        f = rng.randint(-3, 3)
        v[i] = [x + f * y for x, y in zip(v[i], v[j])]
    rng.shuffle(v)
    return v


def test_examples() -> None:
    m = [[2, 1, 0], [1, 3, 1], [0, 1, 4]]
    assert kannan_bachem(m) == ([[1, 0, 7], [0, 1, 4], [0, 0, 18]], [[1, -1, 2], [0, 0, 1], [1, -2, 5]])
    assert hermite_normal_form([[2, 3, 6, 2], [5, 6, 1, 6], [8, 3, 1, 1]]) == [
        [1, 0, 50, -11], [0, 3, 28, -2], [0, 0, 61, -13]]
    assert hermite_normal_form([[4, 6], [2, 2]]) == [[2, 0], [0, 2]]
    assert hermite_normal_form([[6, 4], [4, 2]]) == [[2, 0], [0, 2]]
    assert hermite_normal_form([[2, 8], [0, 5]]) == [[2, 3], [0, 5]]


def test_xgcd() -> None:
    rng = random.Random(3)
    for _ in range(500):
        a, b = rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)
        g, x, y = xgcd(a, b)
        assert g == gcd(a, b) and x * a + y * b == g


def test_edges() -> None:
    assert kannan_bachem([]) == ([], [])
    assert kannan_bachem([[]]) == ([[]], [[1]])
    assert kannan_bachem([[0]]) == ([[0]], [[1]])
    assert kannan_bachem([[-5]]) == ([[5]], [[-1]])
    check([[0, 0, 0], [0, 0, 0]])
    check([[0, 3], [0, 6], [0, 9]])
    check([[0, 1, 2], [1, 0, 0]])  # needs the new row in front
    check([[1, 2, 3, 4, 5]])
    check([[2], [3], [5]])
    h, r = check([[1, 2, 3, 4], [2, 4, 6, 8], [3, 5, 7, 9]])
    assert r == 2


def test_random() -> None:
    rng = random.Random(1979)
    for trial in range(600):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        a = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(m)]
        if rng.random() < 0.2:
            a[rng.randrange(m)] = [0] * n
        if rng.random() < 0.2:
            j = rng.randrange(n)
            for row in a:
                row[j] = 0
        if rng.random() < 0.2 and m > 1:
            i, j = rng.sample(range(m), 2)
            a[i] = [rng.randint(-2, 2) * x for x in a[j]]
        h, r = check(a)
        assert r == rank_minors(a)
        if m == n:
            d = det_leibniz(a)
            prod = 1
            for i in range(n):
                prod *= h[i][i]
            assert prod == abs(d)
        v = random_unimodular(rng, m)
        assert hermite_normal_form(matmul(v, a, n)) == h  # uniqueness


def test_larger_and_large_entries() -> None:
    rng = random.Random(8)
    for _ in range(10):
        m, n = rng.randint(5, 9), rng.randint(5, 9)
        a = [[rng.randint(-10**12, 10**12) for _ in range(n)] for _ in range(m)]
        check(a)
    for _ in range(10):
        n = 8
        a = [[rng.randint(-50, 50) for _ in range(n)] for _ in range(n)]
        h, r = check(a)
        prod = 1
        for i in range(r):
            prod *= h[i][i]
        if r == n:
            assert prod == abs(det_exact(a))
