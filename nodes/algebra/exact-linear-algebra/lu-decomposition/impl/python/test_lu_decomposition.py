# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lu-decomposition/. The authors are listed in prov/EH2SQ6.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from lu_decomposition import lu_decomposition, lu_determinant, lu_solve


def leibniz(a, p=None):
    n = len(a)
    total = 0
    for s in itertools.permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if s[i] > s[j])
        t = -1 if inv % 2 else 1
        for i in range(n):
            t *= a[i][s[i]]
        total += t
    return total if p is None else total % p


def brute_rank(a, p=None):
    m = len(a)
    n = len(a[0]) if m else 0
    for k in range(min(m, n), 0, -1):
        for rows in itertools.combinations(range(m), k):
            for cols in itertools.combinations(range(n), k):
                if leibniz([[a[i][j] for j in cols] for i in rows], p) != 0:
                    return k
    return 0


def matmul(x, y, p=None):
    inner = len(y)
    cols = len(y[0]) if y else 0
    out = [[sum((x[i][k] * y[k][j] for k in range(inner)), Fraction(0)) for j in range(cols)] for i in range(len(x))]
    return out if p is None else [[int(v) % p for v in row] for row in out]


def check(a, p=None):
    m = len(a)
    n = len(a[0]) if m else 0
    perm, low, u = lu_decomposition(a, p)
    assert sorted(perm) == list(range(m))
    for i in range(m):
        assert low[i][i] == 1
        assert all(low[i][j] == 0 for j in range(i + 1, m))
    pa = [[a[perm[i]][j] if p is None else a[perm[i]][j] % p for j in range(n)] for i in range(m)]
    assert matmul(low, u, p) == pa
    lead = [next((j for j in range(n) if u[i][j] != 0), None) for i in range(m)]
    rank = sum(1 for x in lead if x is not None)
    assert all(x is None for x in lead[rank:])
    assert all(lead[i] < lead[i + 1] for i in range(rank - 1))
    return perm, low, u, rank


def test_worked_example():
    a = [[2, 1, 1, 0], [4, 2, 3, 1], [-2, 0, 1, 3], [6, 3, 5, 4]]
    perm, low, u, rank = check(a)
    assert perm == [0, 2, 1, 3]
    assert low == [[1, 0, 0, 0], [-1, 1, 0, 0], [2, 0, 1, 0], [3, 0, 2, 1]]
    assert u == [[2, 1, 1, 0], [0, 1, 2, 3], [0, 0, 1, 1], [0, 0, 0, 2]]
    assert lu_solve(perm, low, u, [3, 8, 0, 13]) == [1, -1, 2, 0]
    assert lu_determinant(a) == -4 == leibniz(a)


def test_edges():
    assert lu_decomposition([]) == ([], [], [])
    assert lu_decomposition([[]]) == ([0], [[1]], [[]])
    assert lu_decomposition([[5]]) == ([0], [[1]], [[5]])
    assert lu_determinant([]) == 1
    assert lu_solve(*lu_decomposition([[3]]), [6]) == [2]
    assert check([[0, 0], [0, 0]])[3] == 0
    perm, low, u, rank = check([[0, 1], [1, 1]])
    assert perm == [1, 0] and lu_determinant([[0, 1], [1, 1]]) == -1
    assert check([[0, 0, 1], [0, 2, 3], [0, 4, 5]])[3] == 2
    assert check([[1, 2, 3, 4]])[3] == 1
    assert check([[0], [0], [7]])[3] == 1
    with pytest.raises(ZeroDivisionError):
        lu_solve(*lu_decomposition([[1, 2], [2, 4]]), [1, 2])


def test_large_entries():
    rng = random.Random(7)
    for _ in range(20):
        n = rng.randrange(1, 6)
        a = [[rng.randrange(-2**80, 2**80) for _ in range(n)] for _ in range(n)]
        perm, low, u, rank = check(a)
        assert lu_determinant(a) == leibniz(a)
        if rank == n:
            x = [rng.randrange(-2**40, 2**40) for _ in range(n)]
            b = [sum(r[j] * x[j] for j in range(n)) for r in a]
            assert lu_solve(perm, low, u, b) == x


def test_random_over_q():
    rng = random.Random(2024)
    for _ in range(600):
        m, n = rng.randrange(0, 5), rng.randrange(0, 5)
        a = [[rng.choice([0, 0, 1, -1, 2, rng.randrange(-9, 10)]) for _ in range(n)] for _ in range(m)]
        if m and rng.random() < 0.3:
            a[rng.randrange(m)] = [0] * n
        perm, low, u, rank = check(a)
        if m and n:
            assert rank == brute_rank(a)
        if m == n:
            assert lu_determinant(a) == leibniz(a)
            if rank == n and n:
                b = [rng.randrange(-9, 10) for _ in range(n)]
                x = lu_solve(perm, low, u, b)
                assert [sum(a[i][j] * x[j] for j in range(n)) for i in range(n)] == b


@pytest.mark.parametrize("p", [2, 3, 7])
def test_random_mod_p(p):
    rng = random.Random(p)
    for _ in range(300):
        m, n = rng.randrange(1, 5), rng.randrange(1, 5)
        a = [[rng.randrange(p) for _ in range(n)] for _ in range(m)]
        perm, low, u, rank = check(a, p)
        assert rank == brute_rank(a, p)
        if m == n:
            assert lu_determinant(a, p) == leibniz(a, p)
            if rank == n:
                b = [rng.randrange(p) for _ in range(n)]
                x = lu_solve(perm, low, u, b, p)
                assert [sum(a[i][j] * x[j] for j in range(n)) % p for i in range(n)] == b
