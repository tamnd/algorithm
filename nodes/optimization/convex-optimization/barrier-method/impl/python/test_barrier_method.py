# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/barrier-method/. The authors are listed in prov/0ZMXKV.jsonl.

import itertools
import math
import random
from fractions import Fraction

from barrier_method import barrier_method, cholesky, newton_bound


def frac_solve(m, r):
    k = len(r)
    a = [row[:] + [r[i]] for i, row in enumerate(m)]
    for col in range(k):
        piv = next((i for i in range(col, k) if a[i][col] != 0), None)
        if piv is None:
            return None
        a[col], a[piv] = a[piv], a[col]
        for i in range(k):
            if i != col and a[i][col] != 0:
                fct = a[i][col] / a[col][col]
                for j in range(col, k + 1):
                    a[i][j] -= fct * a[col][j]
    return [a[i][k] / a[i][i] for i in range(k)]


def lp_by_vertices(a, b, c):
    """min c^T x, A x <= b over a bounded polytope, by enumeration of all vertices in exact arithmetic."""
    n = len(c)
    best = None
    for rows in itertools.combinations(range(len(a)), n):
        x = frac_solve([a[i] for i in rows], [b[i] for i in rows])
        if x is None or any(sum(a[i][j] * x[j] for j in range(n)) > b[i] for i in range(len(a))):
            continue
        v = sum(c[j] * x[j] for j in range(n))
        best = v if best is None else min(best, v)
    return best


def lp_as_lmi(a, b):
    m, n = len(a), len(a[0])
    diag = lambda v: [[float(v[i]) if i == j else 0.0 for j in range(m)] for i in range(m)]
    return [diag(b)] + [diag([-a[i][j] for i in range(m)]) for j in range(n)]


def check_dual(res, c, f, gap_tol):
    """Z = F(x)^-1 / t is positive definite and nearly dual feasible. The gap c^T x + tr(F_0 Z) equals
    p / t plus the term sum x_i (c_i - tr(F_i Z)) that comes from the inexact centering."""
    p = len(f[0])
    z = res.z
    assert cholesky([[z[i][j] + (1e-12 if i == j else 0.0) for j in range(p)] for i in range(p)]) is not None
    resid = []
    for i, ci in enumerate(c):
        resid.append(ci - sum(f[i + 1][r][s] * z[s][r] for r in range(p) for s in range(p)))
        assert abs(resid[-1]) <= 1e-6 * (1 + abs(ci))
    primal = sum(ci * xi for ci, xi in zip(c, res.x))
    dual = -sum(f[0][r][s] * z[s][r] for r in range(p) for s in range(p))
    assert abs((primal - dual) - p / res.t - sum(x * r for x, r in zip(res.x, resid))) <= 1e-9
    assert abs((primal - dual) - p / res.t) <= gap_tol
    return primal, dual


def check_newton_counts(res, p, mu=10.0):
    for _, _, steps in res.outer[1:]:
        assert steps <= newton_bound(p, mu)


def test_lambda_max_2x2() -> None:
    # minimize x subject to x I - M psd: the answer is the largest eigenvalue of M
    rng = random.Random(7)
    for _ in range(200):
        a, b, d = (rng.randint(-5, 5) for _ in range(3))
        f = [[[-a, -b], [-b, -d]], [[1.0, 0.0], [0.0, 1.0]]]
        res = barrier_method([1.0], f, [abs(a) + abs(b) + abs(d) + 1.0], eps=1e-5)
        lmax = (a + d) / 2 + math.sqrt(((a - d) / 2) ** 2 + b * b)
        primal, dual = check_dual(res, [1.0], f, 1e-6)
        assert dual - 1e-6 <= lmax <= primal + 1e-9
        assert primal - lmax <= 2 / res.t + 1e-9


def test_two_by_two_sdp() -> None:
    # minimize x1 + x2 subject to [[x1, 1], [1, x2]] psd: optimum 2 at (1, 1); dual Z = [[1, -1], [-1, 1]]
    f = [[[0.0, 1.0], [1.0, 0.0]], [[1.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 1.0]]]
    res = barrier_method([1.0, 1.0], f, [3.0, 2.0], eps=1e-5)
    primal, dual = check_dual(res, [1.0, 1.0], f, 1e-6)
    assert dual - 1e-6 <= 2.0 <= primal + 1e-9
    assert primal - 2.0 <= 2 / res.t + 1e-9
    assert abs(res.x[0] - 1) < 1e-3 and abs(res.x[1] - 1) < 1e-3
    assert abs(res.z[0][1] + 1) < 1e-5
    check_newton_counts(res, 2)


def test_page_example() -> None:
    # minimize x subject to 0 <= x <= 1, as a 2 x 2 diagonal LMI
    f = [[[0.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, -1.0]]]
    res = barrier_method([1.0], f, [0.5], t0=1.0, mu=10.0, eps=1e-6)
    assert len(res.outer) == 8
    for t, val, _ in res.outer:
        exact = ((t + 2) - math.sqrt(t * t + 4)) / (2 * t)
        assert abs(val - exact) <= 1e-7 * exact
        assert 0 < val <= 2 / t


def test_random_lp() -> None:
    rng = random.Random(11)
    for _ in range(500):
        n = rng.randint(1, 3)
        rows = [[Fraction(rng.randint(-4, 4)) for _ in range(n)] for _ in range(rng.randint(0, 3))]
        # a box keeps the polytope bounded; b > 0 keeps x = 0 strictly feasible
        a = rows + [[Fraction(1 if j == i else 0) for j in range(n)] for i in range(n)]
        a += [[Fraction(-1 if j == i else 0) for j in range(n)] for i in range(n)]
        b = [Fraction(rng.randint(1, 6)) for _ in a]
        c = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        fstar = float(lp_by_vertices(a, b, c))
        f = lp_as_lmi(a, b)
        cf = [float(v) for v in c]
        res = barrier_method(cf, f, [0.0] * n, eps=1e-5)
        m = len(a)
        primal, dual = check_dual(res, cf, f, 1e-6)
        assert dual - 1e-6 <= fstar <= primal + 1e-9
        assert primal - fstar <= m / res.t + 1e-9
        check_newton_counts(res, m)
