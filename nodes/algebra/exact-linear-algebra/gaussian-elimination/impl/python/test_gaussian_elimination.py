# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-elimination/. The authors are listed in prov/82ZZ65.jsonl.

import random
from fractions import Fraction
from itertools import combinations, permutations

from gaussian_elimination import gaussian_elimination, solve


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
    """The largest t such that some t by t minor is nonzero."""
    m = len(a)
    for t in range(min(m, n), 0, -1):
        for rows in combinations(range(m), t):
            for cols in combinations(range(n), t):
                if det_leibniz([[a[i][j] for j in cols] for i in rows]) != 0:
                    return t
    return 0


def check_echelon(e, r, pivots, m, n):
    assert len(pivots) == r and pivots == sorted(set(pivots))
    for i in range(m):
        nz = [j for j in range(n) if e[i][j] != 0]
        if i < r:
            assert nz and nz[0] == pivots[i]
        else:
            assert not nz


def random_matrix(rng, m, n, lo=-3, hi=3):
    a = [[rng.randint(lo, hi) for _ in range(n)] for _ in range(m)]
    if m and n and rng.random() < 0.3:  # force rank deficiency: copy a combination of rows
        i, k = rng.randrange(m), rng.randrange(m)
        c = rng.randint(-2, 2)
        a[i] = [c * x for x in a[k]]
    if n and rng.random() < 0.2:  # a zero column
        j = rng.randrange(n)
        for row in a:
            row[j] = 0
    return a


def test_example() -> None:
    a = [[0, 2, 1], [1, -1, 0], [2, 0, 3]]
    e, r, pivots = gaussian_elimination([row + [b] for row, b in zip(a, [3, -1, -1])])
    assert e == [[1, -1, 0, -1], [0, 2, 1, 3], [0, 0, 2, -2]]
    assert r == 3 and pivots == [0, 1, 2]
    assert solve(a, [3, -1, -1]) == [1, 2, -1]


def test_edges() -> None:
    assert gaussian_elimination([]) == ([], 0, [])
    assert gaussian_elimination([], 3) == ([], 0, [])
    assert gaussian_elimination([[], []]) == ([[], []], 0, [])
    assert gaussian_elimination([[5]]) == ([[5]], 1, [0])
    assert gaussian_elimination([[0]]) == ([[0]], 0, [])
    assert gaussian_elimination([[0, 0], [0, 0]])[1] == 0
    assert solve([], []) == []
    assert solve([[0, 0]], [1]) is None
    assert solve([[0, 0]], [0]) == [0, 0]
    # zero first pivot that needs a swap
    e, r, p = gaussian_elimination([[0, 1], [1, 0]])
    assert e == [[1, 0], [0, 1]] and r == 2 and p == [0, 1]
    # input is not changed
    a = [[0, 1], [1, 0]]
    gaussian_elimination(a)
    assert a == [[0, 1], [1, 0]]


def test_large_entries() -> None:
    rng = random.Random(77)
    for _ in range(20):
        n = 6
        a = [[rng.randint(-10**30, 10**30) for _ in range(n)] for _ in range(n)]
        x0 = [Fraction(rng.randint(-10**20, 10**20), rng.randint(1, 10**10)) for _ in range(n)]
        b = [sum(a[i][j] * x0[j] for j in range(n)) for i in range(n)]
        x = solve(a, b)
        assert x == x0  # the random matrix is nonsingular with high probability; then x is unique


def test_random_rank_and_shape() -> None:
    rng = random.Random(4021)
    for _ in range(600):
        m, n = rng.randint(0, 4), rng.randint(0, 4)
        a = random_matrix(rng, m, n)
        e, r, pivots = gaussian_elimination(a, n)
        check_echelon(e, r, pivots, m, n)
        assert r == rank_brute(a, n)
        # e has the same row space as a: stacking does not raise the rank
        assert rank_brute(a + [[int(x) if x.denominator == 1 else x for x in row] for row in e], n) == r


def test_random_solve() -> None:
    rng = random.Random(918)
    for _ in range(600):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        a = random_matrix(rng, m, n)
        if rng.random() < 0.5:
            x0 = [rng.randint(-3, 3) for _ in range(n)]
            b = [sum(a[i][j] * x0[j] for j in range(n)) for i in range(m)]
        else:
            b = [rng.randint(-3, 3) for _ in range(m)]
        x = solve(a, b)
        consistent = rank_brute([row + [bi] for row, bi in zip(a, b)], n + 1) == rank_brute(a, n)
        if x is None:
            assert not consistent
        else:
            assert consistent
            assert all(sum(a[i][j] * x[j] for j in range(n)) == b[i] for i in range(m))
