# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fourier-motzkin-elimination/. The authors are listed in prov/JK7PSR.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from fourier_motzkin_elimination import eliminate, fourier_motzkin


def _solve(M: list[list[Fraction]], r: list[Fraction]) -> list[Fraction] | None:
    """Solve the square system M z = r exactly; None if M is singular."""
    k = len(M)
    T = [list(M[i]) + [r[i]] for i in range(k)]
    for c in range(k):
        piv = next((i for i in range(c, k) if T[i][c] != 0), None)
        if piv is None:
            return None
        T[c], T[piv] = T[piv], T[c]
        for i in range(k):
            if i != c and T[i][c] != 0:
                f = T[i][c] / T[c][c]
                T[i] = [u - f * v for u, v in zip(T[i], T[c])]
    return [T[i][k] / T[i][i] for i in range(k)]


def brute_feasible(A: list[list[int]], b: list[int]) -> bool:
    """Oracle: A x <= b is feasible iff the standard form A u - A v + s = b,
    u, v, s >= 0 has a basic feasible solution. Try every basis."""
    m, n = len(A), len(A[0])
    cols = [[Fraction(A[i][j]) for i in range(m)] for j in range(n)]
    cols += [[-c for c in col] for col in cols[:n]]
    cols += [[Fraction(int(i == t)) for i in range(m)] for t in range(m)]
    rhs = [Fraction(v) for v in b]
    for B in combinations(range(len(cols)), m):
        M = [[cols[j][i] for j in B] for i in range(m)]
        z = _solve(M, rhs)
        if z is not None and all(v >= 0 for v in z):
            return True
    return False


def check(A: list[list[int]], b: list[int], ok: bool, v: list[Fraction]) -> None:
    m, n = len(A), len(A[0])
    if ok:
        assert len(v) == n
        for i in range(m):
            assert sum(A[i][j] * v[j] for j in range(n)) <= b[i]
    else:
        assert len(v) == m
        assert all(c >= 0 for c in v)
        for j in range(n):
            assert sum(v[i] * A[i][j] for i in range(m)) == 0
        assert sum(v[i] * b[i] for i in range(m)) < 0


def test_running_example() -> None:
    # x1 + x2 <= 4, x1 + 3 x2 <= 9, x1 <= 3, x >= 0, and 3 x1 + 2 x2 >= t.
    base = [[1, 1], [1, 3], [1, 0], [-1, 0], [0, -1]]
    rhs = [4, 9, 3, 0, 0]
    ok, x = fourier_motzkin(base + [[-3, -2]], rhs + [-11])
    assert ok
    assert 3 * x[0] + 2 * x[1] >= 11
    A, b = base + [[-3, -2]], rhs + [Fraction(-111, 10)]
    ok, y = fourier_motzkin(A, b)
    assert not ok
    check(A, b, ok, y)


def test_certificate() -> None:
    A = [[1, 1], [-1, 0], [0, -1]]
    b = [1, -2, 0]
    ok, y = fourier_motzkin(A, b)
    assert not ok
    check(A, b, ok, y)


def test_edges() -> None:
    assert fourier_motzkin([], [], 2) == (True, [0, 0])
    assert fourier_motzkin([[0, 0]], [0]) == (True, [0, 0])
    ok, y = fourier_motzkin([[0, 0]], [-1])
    assert not ok and y == [1]
    ok, x = fourier_motzkin([[1], [-1]], [5, -5])  # x = 5
    assert ok and x == [5]
    ok, y = fourier_motzkin([[1], [-1]], [4, -5])  # x <= 4 and x >= 5
    assert not ok
    check([[1], [-1]], [4, -5], ok, y)


def test_row_count_bound() -> None:
    rng = random.Random(7)
    for _ in range(300):
        m, n = rng.randint(1, 8), rng.randint(1, 3)
        rows = []
        for i in range(m):
            a = [Fraction(rng.randint(-3, 3)) for _ in range(n)]
            rows.append((a, Fraction(rng.randint(-3, 3)), [Fraction(int(i == t)) for t in range(m)]))
        out = eliminate(rows, n - 1)
        assert len(out) <= max(m, m * m // 4)
        for a, beta, y in out:
            assert a[n - 1] == 0
            assert all(c >= 0 for c in y)
            for j in range(n):
                assert sum(y[i] * rows[i][0][j] for i in range(m)) == a[j]
            assert sum(y[i] * rows[i][1] for i in range(m)) == beta


def test_random_against_brute_force() -> None:
    rng = random.Random(2026)
    seen = {True: 0, False: 0}
    for _ in range(600):
        m, n = rng.randint(1, 5), rng.randint(1, 3)
        A = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
        b = [rng.randint(-4, 4) for _ in range(m)]
        ok, v = fourier_motzkin(A, b)
        check(A, b, ok, v)
        assert ok == brute_feasible(A, b)
        seen[ok] += 1
    assert seen[True] > 50 and seen[False] > 50
