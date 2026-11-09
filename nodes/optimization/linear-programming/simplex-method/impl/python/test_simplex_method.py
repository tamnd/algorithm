# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simplex-method/. The authors are listed in prov/1FHAJA.jsonl.

import itertools
import random
from fractions import Fraction

from simplex_method import simplex_method, solve


def solve_square(cols, b):
    """Solve cols x = b (cols is a list of columns, m rows). None if the columns are dependent or b is not in their span."""
    m, k = len(b), len(cols)
    rows = [[Fraction(cols[j][i]) for j in range(k)] + [Fraction(b[i])] for i in range(m)]
    r = 0
    for col in range(k):
        p = next((i for i in range(r, m) if rows[i][col] != 0), None)
        if p is None:
            return None
        rows[r], rows[p] = rows[p], rows[r]
        rows[r] = [v / rows[r][col] for v in rows[r]]
        for i in range(m):
            if i != r and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [vi - f * vr for vi, vr in zip(rows[i], rows[r])]
        r += 1
    if any(rows[i][k] != 0 for i in range(r, m)):
        return None
    return [rows[i][k] for i in range(k)]


def rank(a):
    rows = [[Fraction(v) for v in row] for row in a]
    r = 0
    for col in range(len(rows[0]) if rows else 0):
        p = next((i for i in range(r, len(rows)) if rows[i][col] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(r + 1, len(rows)):
            f = rows[i][col] / rows[r][col]
            rows[i] = [vi - f * vr for vi, vr in zip(rows[i], rows[r])]
        r += 1
    return r


def basic_feasible(a, b, n):
    """All basic feasible solutions of A x = b, x >= 0, by trying every set of rank(A) columns."""
    k = rank(a) if a else 0
    out = []
    for s in itertools.combinations(range(n), k):
        xs = solve_square([[row[j] for row in a] for j in s], b) if a else []
        if xs is not None and all(v >= 0 for v in xs):
            x = [Fraction(0)] * n
            for j, v in zip(s, xs):
                x[j] = v
            out.append(x)
    return out


def brute(a, b, c):
    """The status and optimal value of min c^T x, A x = b, x >= 0, by enumeration of all bases."""
    n = len(c)
    if a and any(len(row) != n for row in a):
        raise ValueError
    vertices = basic_feasible(a, b, n) if a else [[Fraction(0)] * n]
    if not vertices:
        return "infeasible", None
    rays = basic_feasible(a + [[1] * n], [0] * len(a) + [1], n)
    if any(sum(cj * dj for cj, dj in zip(c, d)) < 0 for d in rays):
        return "unbounded", None
    return "optimal", min(sum(cj * xj for cj, xj in zip(c, x)) for x in vertices)


def check_certificates(a, b, c, res):
    m, n = len(a), len(c)
    if res.status == "optimal":
        x, y = res.x, res.y
        assert all(v >= 0 for v in x)
        assert all(sum(a[i][j] * x[j] for j in range(n)) == b[i] for i in range(m))
        slack = [c[j] - sum(a[i][j] * y[i] for i in range(m)) for j in range(n)]
        assert all(s >= 0 for s in slack)  # dual feasible
        assert sum(bi * yi for bi, yi in zip(b, y)) == res.value  # strong duality
        assert all(x[j] * slack[j] == 0 for j in range(n))  # complementary slackness
    if res.status == "unbounded":
        d = res.ray
        assert all(v >= 0 for v in d)
        assert all(sum(a[i][j] * d[j] for j in range(n)) == 0 for i in range(m))
        assert sum(cj * dj for cj, dj in zip(c, d)) < 0


# Beale (1955): Dantzig's rule cycles on it from the slack basis.
BEALE_A = [[1, 0, 0, Fraction(1, 4), -8, -1, 9], [0, 1, 0, Fraction(1, 2), -12, Fraction(-1, 2), 3], [0, 0, 1, 0, 0, 1, 0]]
BEALE_B = [0, 0, 1]
BEALE_C = [0, 0, 0, Fraction(-3, 4), 20, Fraction(-1, 2), 6]


def klee_minty(n):
    """Chvatal's form: maximize sum 10^(n-j) x_j with 2 sum_{j<i} 10^(i-j) x_j + x_i <= 100^(i-1), as a minimization with slacks."""
    a = [[2 * 10 ** (i - j) for j in range(i)] + [1] + [0] * (n - i - 1) + [int(k == i) for k in range(n)] for i in range(n)]
    b = [100**i for i in range(n)]
    c = [-(10 ** (n - 1 - j)) for j in range(n)] + [0] * n
    return a, b, c


def test_example() -> None:
    # minimize -3 x1 - 5 x2 with x1 <= 4, 2 x2 <= 12, 3 x1 + 2 x2 <= 18
    a = [[1, 0, 1, 0, 0], [0, 2, 0, 1, 0], [3, 2, 0, 0, 1]]
    res = simplex_method(a, [4, 12, 18], [-3, -5, 0, 0, 0], [2, 3, 4], rule="dantzig")
    assert res.status == "optimal" and res.value == -36 and res.pivots == 2
    assert res.x == [2, 6, 2, 0, 0]
    assert res.y == [0, Fraction(-3, 2), -1]


def test_edges() -> None:
    assert solve([], [], [1, 2]).value == 0
    assert solve([], [], [1, -2]).status == "unbounded"
    assert solve([[1, 1]], [-1], [1, 1]).status == "infeasible"
    assert solve([[1, 1], [2, 2]], [1, 2], [1, 3]).value == 1  # a redundant row
    assert solve([[1, 1], [1, 1]], [1, 2], [1, 3]).status == "infeasible"
    assert solve([[1, -1]], [0], [-1, 0]).status == "unbounded"
    res = simplex_method([[1, -1, 1]], [0], [0, -1, 0], [2])
    assert res.status == "unbounded" and res.ray == [0, 1, 1]


def test_beale_cycles_under_dantzig_and_not_under_bland() -> None:
    res = simplex_method(BEALE_A, BEALE_B, BEALE_C, [0, 1, 2], rule="dantzig")
    assert res.status == "cycle" and res.pivots == 6 and sorted(res.basis) == [0, 1, 2]
    res = simplex_method(BEALE_A, BEALE_B, BEALE_C, [0, 1, 2], rule="bland")
    assert res.status == "optimal" and res.value == Fraction(-5, 4)
    assert res.x == [Fraction(3, 4), 0, 0, 1, 0, 1, 0]
    assert brute(BEALE_A, BEALE_B, BEALE_C) == ("optimal", Fraction(-5, 4))
    check_certificates(BEALE_A, BEALE_B, BEALE_C, res)


def test_klee_minty_pivot_counts() -> None:
    for n in range(1, 8):
        a, b, c = klee_minty(n)
        start = list(range(n, 2 * n))
        dz = simplex_method(a, b, c, start, rule="dantzig")
        assert dz.status == "optimal" and dz.value == -(100 ** (n - 1))
        assert dz.pivots == 2**n - 1
        assert simplex_method(a, b, c, start, rule="steepest-edge").pivots == 1
        assert simplex_method(a, b, c, start, rule="bland").value == -(100 ** (n - 1))


def random_lp(rng, degenerate):
    m, n = rng.randint(1, 3), rng.randint(2, 5)
    a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
    b = [0 if degenerate and rng.random() < 0.6 else rng.randint(-4, 6) for _ in range(m)]
    c = [rng.randint(-4, 4) for _ in range(n)]
    return a, b, c


def test_against_brute_force() -> None:
    rng = random.Random(29)
    seen = set()
    for t in range(700):
        a, b, c = random_lp(rng, degenerate=t % 2 == 0)
        want = brute(a, b, c)
        for rule in ("bland", "dantzig", "steepest-edge"):
            res = solve(a, b, c, rule)
            if res.status == "cycle":
                continue
            assert (res.status, res.value) == want, (a, b, c, rule)
            check_certificates(a, b, c, res)
        seen.add(want[0])
    assert seen == {"optimal", "unbounded", "infeasible"}


def test_slack_basis_degenerate_inequalities() -> None:
    rng = random.Random(7)
    for _ in range(300):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        g = [[rng.randint(-2, 3) for _ in range(n)] for _ in range(m)]
        b = [rng.choice([0, 0, 1, 2, 3]) for _ in range(m)]
        c = [rng.randint(-3, 2) for _ in range(n)] + [0] * m
        a = [row + [int(k == i) for k in range(m)] for i, row in enumerate(g)]
        res = simplex_method(a, b, c, list(range(n, n + m)), rule="bland")
        assert (res.status, res.value) == brute(a, b, c)
        check_certificates(a, b, c, res)
