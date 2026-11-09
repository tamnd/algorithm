# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-phase-simplex-method/. The authors are listed in prov/AJZNEC.jsonl.

import itertools
import random
from fractions import Fraction

from two_phase_simplex_method import two_phase_simplex_method


def solve_square(cols, b):
    """Solve cols x = b (cols is a list of columns). None if the columns are dependent or b is not in their span."""
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
    k = rank(a)
    out = []
    for s in itertools.combinations(range(n), k):
        xs = solve_square([[row[j] for row in a] for j in s], b)
        if xs is not None and all(v >= 0 for v in xs):
            x = [Fraction(0)] * n
            for j, v in zip(s, xs):
                x[j] = v
            out.append(x)
    return out


def brute(a, b, c):
    """The status and optimal value of min c^T x, A x = b, x >= 0, by enumeration of all bases."""
    n = len(c)
    vertices = basic_feasible(a, b, n)
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
        assert all(s >= 0 for s in slack)
        assert sum(bi * yi for bi, yi in zip(b, y)) == res.value
        assert all(x[j] * slack[j] == 0 for j in range(n))
    elif res.status == "unbounded":
        x, d = res.x, res.ray
        assert all(v >= 0 for v in x) and all(v >= 0 for v in d)
        assert all(sum(a[i][j] * x[j] for j in range(n)) == b[i] for i in range(m))
        assert all(sum(a[i][j] * d[j] for j in range(n)) == 0 for i in range(m))
        assert sum(cj * dj for cj, dj in zip(c, d)) < 0
    else:
        z = res.farkas
        assert all(sum(a[i][j] * z[i] for i in range(m)) <= 0 for j in range(n))
        assert sum(bi * zi for bi, zi in zip(b, z)) > 0


def test_example() -> None:
    # minimize 2 x1 + 3 x2 with x1 + x2 >= 4 and x1 + 3 x2 >= 6, surplus columns x3 and x4
    a = [[1, 1, -1, 0], [1, 3, 0, -1]]
    res = two_phase_simplex_method(a, [4, 6], [2, 3, 0, 0])
    assert res.status == "optimal" and res.value == 9
    assert res.x == [3, 1, 0, 0]
    assert res.y == [Fraction(3, 2), Fraction(1, 2)]
    assert res.phase1_pivots == 2
    check_certificates(a, [4, 6], [2, 3, 0, 0], res)


def test_edges() -> None:
    res = two_phase_simplex_method([[1, 1], [2, 2]], [1, 2], [1, 3])
    assert res.status == "optimal" and res.value == 1 and len(res.rows) == 1  # a redundant row is dropped
    check_certificates([[1, 1], [2, 2]], [1, 2], [1, 3], res)
    res = two_phase_simplex_method([[1, 1], [1, 1]], [1, 2], [1, 3])
    assert res.status == "infeasible"
    check_certificates([[1, 1], [1, 1]], [1, 2], [1, 3], res)
    res = two_phase_simplex_method([[1, 1]], [-1], [1, 1])
    assert res.status == "infeasible" and res.farkas == [-1]
    res = two_phase_simplex_method([[-1, -1]], [-2], [1, 1])  # a row with b < 0 is flipped
    assert res.status == "optimal" and res.value == 2
    check_certificates([[-1, -1]], [-2], [1, 1], res)
    res = two_phase_simplex_method([[1, -1]], [0], [-1, 0])
    assert res.status == "unbounded"
    check_certificates([[1, -1]], [0], [-1, 0], res)
    res = two_phase_simplex_method([[0, 0]], [0], [1, 1])  # a zero row
    assert res.status == "optimal" and res.value == 0 and res.rows == []


def random_lp(rng, degenerate):
    m, n = rng.randint(1, 4), rng.randint(2, 5)
    a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
    if m >= 2 and rng.random() < 0.2:  # make a dependent row
        a[-1] = [u + v for u, v in zip(a[0], a[1])]
    b = [0 if degenerate and rng.random() < 0.6 else rng.randint(-5, 6) for _ in range(m)]
    if m >= 2 and rng.random() < 0.5 and a[-1] == [u + v for u, v in zip(a[0], a[1])]:
        b[-1] = b[0] + b[1]
    c = [rng.randint(-4, 4) for _ in range(n)]
    return a, b, c


def test_against_brute_force() -> None:
    rng = random.Random(41)
    seen = set()
    for t in range(800):
        a, b, c = random_lp(rng, degenerate=t % 2 == 0)
        want = brute(a, b, c)
        res = two_phase_simplex_method(a, b, c)
        assert (res.status, res.value) == want, (a, b, c)
        check_certificates(a, b, c, res)
        seen.add(want[0])
    assert seen == {"optimal", "unbounded", "infeasible"}
