# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-jordan-elimination/. The authors are listed in prov/NK577G.jsonl.

import random
from fractions import Fraction
from itertools import combinations, permutations

from gauss_jordan_elimination import gauss_jordan_elimination as gj
from gauss_jordan_elimination import inverse, solve


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


def rank_brute(a, n):
    m = len(a)
    for t in range(min(m, n), 0, -1):
        for rows in combinations(range(m), t):
            for cols in combinations(range(n), t):
                if det_leibniz([[a[i][j] for j in cols] for i in rows]) != 0:
                    return t
    return 0


def check_rref(e, r, pivots, m, n):
    assert len(pivots) == r and pivots == sorted(set(pivots))
    for i in range(m):
        nz = [j for j in range(n) if e[i][j] != 0]
        if i < r:
            assert nz and nz[0] == pivots[i] and e[i][pivots[i]] == 1
        else:
            assert not nz
    for k, j in enumerate(pivots):
        assert all(e[i][j] == (1 if i == k else 0) for i in range(m))


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def test_example() -> None:
    a = [[0, 2, 1], [1, 1, 1], [2, 3, 1]]
    inv = inverse(a)
    assert inv == [[Fraction(-2, 3), Fraction(1, 3), Fraction(1, 3)],
                   [Fraction(1, 3), Fraction(-2, 3), Fraction(1, 3)],
                   [Fraction(1, 3), Fraction(4, 3), Fraction(-2, 3)]]
    e, r, p = gj([[0, 2, 4, 2], [1, 1, 1, 0], [2, 4, 6, 2]])
    assert e == [[1, 0, -1, -1], [0, 1, 2, 1], [0, 0, 0, 0]] and r == 2 and p == [0, 1]


def test_edges() -> None:
    assert gj([]) == ([], 0, [])
    assert gj([[], []]) == ([[], []], 0, [])
    assert gj([[4]]) == ([[1]], 1, [0])
    assert gj([[0, 0, 3]]) == ([[0, 0, 1]], 1, [2])
    assert inverse([]) == []
    assert inverse([[2]]) == [[Fraction(1, 2)]]
    assert inverse([[0]]) is None
    assert inverse([[1, 2], [2, 4]]) is None
    assert inverse([[0, 1], [1, 0]]) == [[0, 1], [1, 0]]


def test_random_rref() -> None:
    rng = random.Random(3307)
    for _ in range(600):
        m, n = rng.randint(0, 4), rng.randint(0, 4)
        a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
        if m >= 2 and rng.random() < 0.3:
            a[0] = [x + y for x, y in zip(a[1], a[-1])]
        e, r, p = gj(a, n)
        check_rref(e, r, p, m, n)
        assert r == rank_brute(a, n)
        assert rank_brute(a + e, n) == r  # same row space
        # uniqueness: a row permutation of a has the same reduced form
        b = a[:]
        rng.shuffle(b)
        assert gj(b, n)[0] == e


def test_random_inverse() -> None:
    rng = random.Random(611)
    for _ in range(600):
        n = rng.randint(1, 5)
        a = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)]
        if rng.random() < 0.25:
            a[rng.randrange(n)] = [0] * n
        if rng.random() < 0.25:
            for i in range(n):
                a[i][i] = 0
        inv = inverse(a)
        if det_leibniz(a) == 0:
            assert inv is None
        else:
            ident = [[int(i == j) for j in range(n)] for i in range(n)]
            assert matmul(a, inv) == ident and matmul(inv, a) == ident


def test_large_entries() -> None:
    rng = random.Random(31)
    for _ in range(10):
        n = 5
        a = [[rng.randint(-10**30, 10**30) for _ in range(n)] for _ in range(n)]
        inv = inverse(a)
        ident = [[int(i == j) for j in range(n)] for i in range(n)]
        assert matmul(a, inv) == ident


def test_random_solve() -> None:
    rng = random.Random(4242)
    for _ in range(600):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
        if rng.random() < 0.5:
            x0 = [rng.randint(-3, 3) for _ in range(n)]
            b = [sum(a[i][j] * x0[j] for j in range(n)) for i in range(m)]
        else:
            b = [rng.randint(-3, 3) for _ in range(m)]
        x = solve(a, b)
        consistent = rank_brute(a, n) == rank_brute([a[i] + [b[i]] for i in range(m)], n + 1)
        if consistent:
            assert x is not None
            assert all(sum(a[i][j] * x[j] for j in range(n)) == b[i] for i in range(m))
        else:
            assert x is None
    assert solve([[0, 2, 1], [1, -1, 0], [2, 0, 3]], [3, -1, -1]) == [1, 2, -1]
    assert solve([[1, 1], [1, 1]], [1, 2]) is None
