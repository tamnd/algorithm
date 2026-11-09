# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-simplex-method/. The authors are listed in prov/M8KGT9.jsonl.

import itertools
import random
from fractions import Fraction

from dual_simplex_method import dual_simplex_method


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


def brute(a, b, c):
    """Status and value of min c^T x, A x = b, x >= 0 when A has full row rank (enumeration of all bases)."""
    m, n = len(a), len(c)
    best = None
    for s in itertools.combinations(range(n), m):
        xs = solve_square([[row[j] for row in a] for j in s], b)
        if xs is not None and all(v >= 0 for v in xs):
            v = sum(c[j] * x for j, x in zip(s, xs))
            best = v if best is None else min(best, v)
    return ("infeasible", None) if best is None else ("optimal", best)


def dual_feasible_bases(a, c):
    """All bases B with A_B nonsingular and c - A^T y >= 0 for y = A_B^-T c_B."""
    m, n = len(a), len(c)
    out = []
    for s in itertools.combinations(range(n), m):
        # A_B^T y = c_B: column k of A_B^T is row k of A restricted to s
        y = solve_square([[a[k][j] for j in s] for k in range(m)], [c[j] for j in s])
        if y is None:
            continue
        if all(c[j] - sum(a[i][j] * y[i] for i in range(m)) >= 0 for j in range(n)):
            out.append(list(s))
    return out


def check(a, b, c, res):
    m, n = len(a), len(c)
    if res.status == "optimal":
        x, y = res.x, res.y
        assert all(v >= 0 for v in x)
        assert all(sum(a[i][j] * x[j] for j in range(n)) == b[i] for i in range(m))
        assert all(c[j] - sum(a[i][j] * y[i] for i in range(m)) >= 0 for j in range(n))
        assert sum(bi * yi for bi, yi in zip(b, y)) == res.value
    else:
        z = res.farkas
        assert all(sum(a[i][j] * z[i] for i in range(m)) <= 0 for j in range(n))
        assert sum(bi * zi for bi, zi in zip(b, z)) > 0
    assert all(u <= v for u, v in zip(res.dual_values, res.dual_values[1:]))  # b^T y never falls


def covering(g, h, c):
    """min c^T x, G x >= h, x >= 0 as [-G | I] (x, s) = -h with the slack basis."""
    m, n = len(g), len(c)
    a = [[-v for v in g[i]] + [int(k == i) for k in range(m)] for i in range(m)]
    return a, [-v for v in h], list(c) + [0] * m, list(range(n, n + m))


def test_example() -> None:
    # min 2 x1 + 3 x2 with x1 + x2 >= 4 and x1 + 3 x2 >= 6: no phase one is needed
    a, b, c, basis = covering([[1, 1], [1, 3]], [4, 6], [2, 3])
    res = dual_simplex_method(a, b, c, basis, rule="most-negative")
    assert res.status == "optimal" and res.value == 9 and res.x[:2] == [3, 1]
    assert res.pivots == 2 and res.dual_values == [0, 6, 9]
    assert res.y == [Fraction(-3, 2), Fraction(-1, 2)]  # the rows were multiplied by -1
    check(a, b, c, res)


def test_infeasible_row() -> None:
    # x1 + x2 >= 3 and -x1 - x2 >= -1 (that is x1 + x2 <= 1)
    a, b, c, basis = covering([[1, 1], [-1, -1]], [3, -1], [1, 1])
    res = dual_simplex_method(a, b, c, basis)
    assert res.status == "infeasible"
    check(a, b, c, res)


def test_covering_against_brute_force() -> None:
    rng = random.Random(97)
    seen = set()
    for _ in range(400):
        m, n = rng.randint(1, 3), rng.randint(1, 3)
        g = [[rng.randint(-2, 3) for _ in range(n)] for _ in range(m)]
        h = [rng.randint(-2, 4) for _ in range(m)]
        cost = [rng.randint(0, 4) for _ in range(n)]
        a, b, c, basis = covering(g, h, cost)
        want = brute(a, b, c)
        for rule in ("least-index", "most-negative"):
            res = dual_simplex_method(a, b, c, basis, rule=rule)
            if res.status == "cycle":
                assert rule == "most-negative"
                continue
            assert (res.status, res.value) == want, (g, h, cost, rule)
            check(a, b, c, res)
        seen.add(want[0])
    assert seen == {"optimal", "infeasible"}


def test_random_dual_feasible_bases() -> None:
    rng = random.Random(101)
    done = 0
    while done < 300:
        m, n = rng.randint(1, 3), rng.randint(2, 5)
        if m > n:
            continue
        a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
        b = [0 if rng.random() < 0.3 else rng.randint(-5, 5) for _ in range(m)]
        c = [rng.randint(-2, 4) for _ in range(n)]
        starts = dual_feasible_bases(a, c)
        if not starts:
            continue
        basis = rng.choice(starts)
        res = dual_simplex_method(a, b, c, basis)
        assert res.status != "cycle"
        assert (res.status, res.value) == brute(a, b, c), (a, b, c, basis)
        check(a, b, c, res)
        done += 1
