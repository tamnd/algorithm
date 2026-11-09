# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/initial-basic-feasible-solution/. The authors are listed in prov/1EQ5XZ.jsonl.

import itertools
import random
from fractions import Fraction

from initial_basic_feasible_solution import initial_basic_feasible_solution


def solve_square(cols, b):
    """Solve cols x = b for m columns and m rows. None if the columns are dependent."""
    m = len(b)
    rows = [[Fraction(cols[j][i]) for j in range(m)] + [Fraction(b[i])] for i in range(m)]
    for col in range(m):
        p = next((i for i in range(col, m) if rows[i][col] != 0), None)
        if p is None:
            return None
        rows[col], rows[p] = rows[p], rows[col]
        rows[col] = [v / rows[col][col] for v in rows[col]]
        for i in range(m):
            if i != col and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [vi - f * vc for vi, vc in zip(rows[i], rows[col])]
    return [rows[i][m] for i in range(m)]


def brute_feasible(a, b):
    """A x <= b, x >= 0 is feasible iff A x + s = b has a basic feasible solution ([A | I] has rank m)."""
    m, n = len(b), len(a[0])
    full = [list(a[i]) + [int(k == i) for k in range(m)] for i in range(m)]
    for s in itertools.combinations(range(n + m), m):
        xs = solve_square([[row[j] for row in full] for j in s], b)
        if xs is not None and all(v >= 0 for v in xs):
            return True
    return False


def check(a, b, res):
    m, n = len(b), len(a[0])
    if res.feasible:
        full = [list(a[i]) + [int(k == i) for k in range(m)] for i in range(m)]
        assert len(set(res.basis)) == m and all(0 <= j < n + m for j in res.basis)
        xs = solve_square([[row[j] for row in full] for j in res.basis], b)
        assert xs is not None, "the basis columns must be independent"
        assert all(v >= 0 for v in xs)
        want = [Fraction(0)] * (n + m)
        for j, v in zip(res.basis, xs):
            want[j] = v
        assert res.x == want
    else:
        y = res.y
        assert all(v >= 0 for v in y)
        assert all(sum(y[i] * a[i][j] for i in range(m)) >= 0 for j in range(n))
        assert sum(yi * bi for yi, bi in zip(y, b)) < 0


def test_example() -> None:
    # CLRS 29.5: 2 x1 - x2 <= 2, x1 - 5 x2 <= -4, x >= 0
    a, b = [[2, -1], [1, -5]], [2, -4]
    res = initial_basic_feasible_solution(a, b)
    assert res.feasible and res.pivots == 2
    assert sorted(res.basis) == [1, 2]
    assert res.x == [0, Fraction(4, 5), Fraction(14, 5), 0]
    check(a, b, res)


def test_edges() -> None:
    res = initial_basic_feasible_solution([[1, 1], [0, 1]], [3, 0])
    assert res.feasible and res.basis == [2, 3] and res.pivots == 0  # b >= 0: the slack basis
    res = initial_basic_feasible_solution([[1, 1]], [-1])
    assert not res.feasible and res.y == [1]
    res = initial_basic_feasible_solution([[1, 0], [-1, 0]], [1, -2])  # x1 <= 1 and x1 >= 2
    assert not res.feasible
    check([[1, 0], [-1, 0]], [1, -2], res)
    res = initial_basic_feasible_solution([[-1], [-1]], [-1, -1])  # x1 >= 1 twice: degenerate
    assert res.feasible
    check([[-1], [-1]], [-1, -1], res)
    res = initial_basic_feasible_solution([[-1, 0], [1, 0]], [-1, 1])  # x1 = 1: x0 ends basic at 0
    assert res.feasible
    check([[-1, 0], [1, 0]], [-1, 1], res)


def test_against_brute_force() -> None:
    rng = random.Random(53)
    seen = set()
    for t in range(600):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
        if t % 3 == 0 and m >= 2:  # equal and opposite rows give equalities and degenerate ends
            a[1] = [-v for v in a[0]]
        b = [rng.randint(-5, 4) for _ in range(m)]
        if t % 3 == 0 and m >= 2:
            b[1] = -b[0]
        res = initial_basic_feasible_solution(a, b)
        assert res.feasible == brute_feasible(a, b), (a, b)
        check(a, b, res)
        seen.add(res.feasible)
    assert seen == {True, False}
