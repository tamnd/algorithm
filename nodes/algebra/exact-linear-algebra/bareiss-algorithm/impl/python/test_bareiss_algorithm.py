# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bareiss-algorithm/. The authors are listed in prov/S667TN.jsonl.

import random
from itertools import combinations, permutations

from bareiss_algorithm import bareiss, bareiss_determinant, fraction_free_echelon


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


def test_examples() -> None:
    m = [[2, 1, 0], [1, 3, 1], [0, 1, 4]]
    d, u, perm = bareiss(m)
    assert d == 18 and u[1][1:] == [5, 2] and u[2][2] == 18 and perm == [0, 1, 2]
    assert bareiss_determinant([[0, 1, 2, 3], [1, 0, 1, 2], [2, 1, 0, 1], [3, 2, 1, 0]]) == -12


def test_edges() -> None:
    assert bareiss_determinant([]) == 1
    assert bareiss_determinant([[7]]) == 7
    assert bareiss_determinant([[0]]) == 0
    assert bareiss_determinant([[0, 1], [1, 0]]) == -1
    assert bareiss_determinant([[0, 0], [0, 5]]) == 0
    assert bareiss_determinant([[1, 2], [2, 4]]) == 0
    assert bareiss_determinant([[1, 2, 3], [0, 0, 0], [4, 5, 6]]) == 0
    assert fraction_free_echelon([]) == ([], 0, [])
    assert fraction_free_echelon([[0, 0, 3]]) == ([[0, 0, 3]], 1, [2])


def test_random_determinant() -> None:
    rng = random.Random(1968)
    for _ in range(800):
        n = rng.randint(1, 6)
        a = [[rng.randint(-4, 4) for _ in range(n)] for _ in range(n)]
        if rng.random() < 0.2:
            a[rng.randrange(n)] = [0] * n
        if rng.random() < 0.3:
            for i in range(n):
                a[i][0] = 0 if i < n - 1 else a[i][0]
        if n >= 2 and rng.random() < 0.15:
            a[1] = [2 * x for x in a[0]]
        assert bareiss_determinant(a) == det_leibniz(a)


def test_intermediate_entries_are_minors() -> None:
    rng = random.Random(77)
    for _ in range(400):
        n = rng.randint(1, 5)
        a = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)]
        d, u, perm = bareiss(a)
        if d == 0:
            continue
        pa = [a[i] for i in perm]
        for k in range(n):
            for j in range(k, n):
                cols = list(range(k)) + [j]
                minor = det_leibniz([[pa[i][c] for c in cols] for i in range(k + 1)])
                assert u[k][j] == minor


def test_random_echelon() -> None:
    rng = random.Random(4096)
    for _ in range(600):
        m, n = rng.randint(0, 4), rng.randint(0, 5)
        a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
        if m >= 2 and rng.random() < 0.3:
            a[-1] = [x - y for x, y in zip(a[0], a[1])]
        e, r, piv = fraction_free_echelon(a, n)
        assert r == rank_brute(a, n) == len(piv)
        for i in range(m):
            nz = [j for j in range(n) if e[i][j] != 0]
            if i < r:
                assert nz[0] == piv[i]
            else:
                assert not nz
        assert piv == sorted(piv)
        assert rank_brute(a + e, n) == r


def test_large_entries() -> None:
    rng = random.Random(5)
    for _ in range(20):
        n = 5
        a = [[rng.randint(-10**40, 10**40) for _ in range(n)] for _ in range(n)]
        assert bareiss_determinant(a) == det_leibniz(a)
