# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interior-point-method/. The authors are listed in prov/MYGDGH.jsonl.

import itertools
import math
import random
from fractions import Fraction

from interior_point_method import THETA, interior_point_method, iteration_bound


def frac_solve(m: list[list[Fraction]], r: list[Fraction]) -> list[Fraction] | None:
    """Exact Gaussian elimination. Returns None if m is singular."""
    k = len(r)
    a = [row[:] + [r[i]] for i, row in enumerate(m)]
    for col in range(k):
        piv = next((i for i in range(col, k) if a[i][col] != 0), None)
        if piv is None:
            return None
        a[col], a[piv] = a[piv], a[col]
        for i in range(k):
            if i != col and a[i][col] != 0:
                f = a[i][col] / a[col][col]
                for j in range(col, k + 1):
                    a[i][j] -= f * a[col][j]
    return [a[i][k] / a[i][i] for i in range(k)]


def lp_by_bases(a, b, c):
    """Optimal value of min c^T x, A x = b, x >= 0 by enumeration of all bases, in exact arithmetic.

    Returns (value, x, y) for a basis that is primal and dual feasible."""
    m, n = len(a), len(c)
    for basis in itertools.combinations(range(n), m):
        bm = [[a[i][j] for j in basis] for i in range(m)]
        xb = frac_solve(bm, b)
        if xb is None or min(xb) < 0:
            continue
        bt = [[a[i][j] for i in range(m)] for j in basis]
        y = frac_solve(bt, [c[j] for j in basis])
        red = [c[j] - sum(a[i][j] * y[i] for i in range(m)) for j in range(n)]
        if min(red) < 0:
            continue
        x = [Fraction(0)] * n
        for k, j in enumerate(basis):
            x[j] = xb[k]
        return sum(c[j] * x[j] for j in range(n)), x, y
    return None


def make_lp(rng: random.Random, m: int, n: int):
    """A random LP whose start (x0, y0, s0) lies on the central path with mu0 = 1."""
    while True:
        a = [[Fraction(rng.randint(-3, 3)) for _ in range(n)] for _ in range(m)]
        if frac_solve([[sum(a[i][k] * a[j][k] for k in range(n)) for j in range(m)] for i in range(m)], [Fraction(0)] * m) is not None:
            break
    x0 = [Fraction(rng.randint(1, 4)) for _ in range(n)]
    s0 = [1 / xi for xi in x0]
    y0 = [Fraction(rng.randint(-2, 2)) for _ in range(m)]
    b = [sum(a[i][j] * x0[j] for j in range(n)) for i in range(m)]
    c = [sum(a[i][j] * y0[i] for i in range(m)) + s0[j] for j in range(n)]
    return a, b, c, x0, y0, s0


def fl(v):
    return [float(t) for t in v]


def check_run(a, b, c, x0, y0, s0, eps=1e-8):
    n = len(c)
    af = [fl(row) for row in a]
    res = interior_point_method(af, fl(x0), fl(y0), fl(s0), eps=eps)
    mu0 = float(sum(p * q for p, q in zip(x0, s0))) / n
    sigma = 1 - THETA / math.sqrt(n)
    # the gap falls by sigma exactly at each step
    for k, g in enumerate(res.gaps):
        assert abs(g - n * mu0 * sigma**k) <= 1e-9 * n * mu0
    # every iterate is strictly feasible and in the neighborhood N2(0.4)
    for x, s in res.points:
        mu = sum(p * q for p, q in zip(x, s)) / n
        assert min(x) > 0 and min(s) > 0
        assert math.sqrt(sum((x[j] * s[j] - mu) ** 2 for j in range(n))) <= THETA * mu * (1 + 1e-6)
        for i in range(len(a)):
            assert abs(sum(af[i][j] * x[j] for j in range(n)) - float(b[i])) <= 1e-7
    assert res.iterations <= iteration_bound(n, mu0, eps)
    # the gap equals c^T x - b^T y, and both sides bracket the exact optimum
    ref = lp_by_bases(a, b, c)
    assert ref is not None
    fstar = float(ref[0])
    primal = sum(float(c[j]) * res.x[j] for j in range(n))
    dual = sum(float(b[i]) * res.y[i] for i in range(len(b)))
    assert abs((primal - dual) - res.gaps[-1]) <= 1e-7
    assert dual - 1e-7 <= fstar <= primal + 1e-7
    assert primal - fstar <= eps + 1e-7
    return res


def test_page_example() -> None:
    a = [[Fraction(1), Fraction(1), Fraction(1)]]
    x0 = [Fraction(1), Fraction(1, 2), Fraction(1, 3)]
    s0 = [Fraction(1), Fraction(2), Fraction(3)]
    b = [sum(x0)]
    c = [Fraction(1), Fraction(2), Fraction(3)]
    res = check_run(a, b, c, x0, [Fraction(0)], s0, eps=1e-6)
    assert res.iterations == 57
    assert abs(res.x[0] - 11 / 6) < 1e-6 and abs(res.y[0] - 1) < 1e-6


def test_start_off_the_path() -> None:
    # x_i s_i = 1 + d_i with sum d = 0 and ||d|| = 0.3 <= 0.4: in N2(0.4) but not on the path
    a = [[Fraction(1), Fraction(2), Fraction(-1), Fraction(1)], [Fraction(0), Fraction(1), Fraction(1), Fraction(-2)]]
    x0 = [Fraction(1)] * 4
    d = [Fraction(3, 20), Fraction(-3, 20), Fraction(3, 20), Fraction(-3, 20)]
    s0 = [1 + t for t in d]
    y0 = [Fraction(1), Fraction(-1)]
    b = [sum(row) for row in a]
    c = [sum(a[i][j] * y0[i] for i in range(2)) + s0[j] for j in range(4)]
    check_run(a, b, c, x0, y0, s0)


def test_degenerate_optimum() -> None:
    # c is constant on the face x1 + x2 = 2, so the optimum is not unique
    a = [[Fraction(1), Fraction(1), Fraction(1)]]
    x0 = [Fraction(1), Fraction(1), Fraction(1)]
    s0 = [Fraction(1), Fraction(1), Fraction(1)]
    b = [Fraction(3)]
    c = [Fraction(1), Fraction(1), Fraction(1)]
    check_run(a, b, c, x0, [Fraction(0)], s0)


def test_random() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        m = rng.randint(1, 3)
        n = rng.randint(m + 1, 6)
        check_run(*make_lp(rng, m, n), eps=1e-6)
