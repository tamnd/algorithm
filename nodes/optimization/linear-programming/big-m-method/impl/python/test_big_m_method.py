# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/big-m-method/. The authors are listed in prov/XN1HFE.jsonl.

import itertools
import random
from fractions import Fraction

from big_m_method import big_m_method


def solve_square(cols, b):
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
    for col in range(len(rows[0])):
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


def check(a, b, c, res):
    m, n = len(a), len(c)
    if res.status in ("optimal", "unbounded"):
        assert all(v >= 0 for v in res.x)
        assert all(sum(a[i][j] * res.x[j] for j in range(n)) == b[i] for i in range(m))
    if res.status == "unbounded":
        d = res.ray
        assert all(v >= 0 for v in d)
        assert all(sum(a[i][j] * d[j] for j in range(n)) == 0 for i in range(m))
        assert sum(cj * dj for cj, dj in zip(c, d)) < 0
    if res.status == "infeasible":
        z = res.farkas
        assert all(sum(a[i][j] * z[i] for i in range(m)) <= 0 for j in range(n))
        assert sum(bi * zi for bi, zi in zip(b, z)) > 0


EX_A, EX_B, EX_C = [[1, 1, -1, 0], [1, 3, 0, -1]], [4, 6], [2, 3, 0, 0]


def test_example() -> None:
    res = big_m_method(EX_A, EX_B, EX_C)
    assert res.status == "optimal" and res.value == 9 and res.x == [3, 1, 0, 0] and res.pivots == 2


def test_numeric_m_too_small() -> None:
    # The optimal dual is y = (3/2, 1/2). For M < 3/2 the penalty is too weak.
    res = big_m_method(EX_A, EX_B, EX_C, M=1)
    assert res.status == "infeasible" and res.artificial == 2  # a wrong answer
    for M in (2, 10, 1000):
        res = big_m_method(EX_A, EX_B, EX_C, M=M)
        assert res.status == "optimal" and res.value == 9


def test_ray_with_positive_artificial() -> None:
    # -x1 = 2 has no solution, but the column of x2 is a ray of cost -1 while a1 = 2
    a, b, c = [[-1, 0]], [2], [0, -1]
    res = big_m_method(a, b, c)
    assert res.status == "infeasible" and res.rerun and res.farkas == [1]
    check(a, b, c, res)
    res = big_m_method(a, b, c, M=10**6)  # a number M sees only the ray
    assert res.status == "unbounded" and res.artificial == 2
    # -x1 + x3 = 2: the same ray appears while a1 = 2, but x3 = 2 is feasible
    a, b, c = [[-1, 0, 1]], [2], [1, -1, -1]
    res = big_m_method(a, b, c)
    assert res.status == "unbounded" and res.rerun and res.x == [0, 0, 2]
    check(a, b, c, res)


def test_edges() -> None:
    assert big_m_method([[1, 1], [2, 2]], [1, 2], [1, 3]).value == 1
    res = big_m_method([[1, 1], [1, 1]], [1, 2], [1, 3])
    assert res.status == "infeasible"
    check([[1, 1], [1, 1]], [1, 2], [1, 3], res)
    res = big_m_method([[-1, -1]], [-2], [1, 1])
    assert res.status == "optimal" and res.value == 2


def random_lp(rng, t):
    m, n = rng.randint(1, 3), rng.randint(2, 5)
    a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
    b = [0 if t % 2 == 0 and rng.random() < 0.6 else rng.randint(-5, 6) for _ in range(m)]
    c = [rng.randint(-4, 4) for _ in range(n)]
    return a, b, c


def test_against_brute_force() -> None:
    rng = random.Random(67)
    seen, reruns = set(), set()
    for t in range(800):
        a, b, c = random_lp(rng, t)
        want = brute(a, b, c)
        res = big_m_method(a, b, c)
        assert (res.status, res.value) == want, (a, b, c)
        check(a, b, c, res)
        seen.add(want[0])
        if res.rerun:
            reruns.add(res.status)
    assert seen == {"optimal", "unbounded", "infeasible"}
    assert reruns == {"unbounded", "infeasible"}  # line L6 decides both ways
