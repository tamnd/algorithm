# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affine-scaling-method/. The authors are listed in prov/CWE5Y6.jsonl.

import itertools
import random
from fractions import Fraction

from affine_scaling_method import affine_scaling_method, dot

TOL = 1e-6  # stated tolerance on the optimal value, relative to 1 + |optimum|


def solve_exact(m, rhs):
    """Exact Gaussian elimination; None if the matrix is singular."""
    t = [[Fraction(v) for v in r] + [Fraction(x)] for r, x in zip(m, rhs)]
    k = len(t)
    for col in range(k):
        p = next((i for i in range(col, k) if t[i][col] != 0), None)
        if p is None:
            return None
        t[col], t[p] = t[p], t[col]
        for i in range(k):
            if i != col and t[i][col] != 0:
                f = t[i][col] / t[col][col]
                t[i] = [vi - f * vc for vi, vc in zip(t[i], t[col])]
    return [t[i][k] / t[i][i] for i in range(k)]


def brute_force(a, b, c):
    """The least c^T x over all basic feasible solutions, exactly; None if A has no basis."""
    m, n = len(a), len(c)
    best, any_basis = None, False
    for cols in itertools.combinations(range(n), m):
        z = solve_exact([[a[i][j] for j in cols] for i in range(m)], b)
        if z is None:
            continue
        any_basis = True
        if min(z) >= 0:
            v = sum(c[j] * zj for j, zj in zip(cols, z))
            best = v if best is None or v < best else best
    return best if any_basis else None


def instance(rng, unbounded):
    m = rng.randint(1, 3)
    n = rng.randint(m + 1, 6)
    a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
    x0 = [Fraction(rng.randint(1, 9), rng.randint(1, 4)) for _ in range(n)]
    if unbounded:  # make d = (d', 1) >= 0 a direction with A d = 0, and c^T d < 0
        dp = [rng.randint(0, 2) for _ in range(n - 1)]
        for row in a:
            row[-1] = -sum(r * v for r, v in zip(row, dp))
        c = [rng.randint(-3, 3) for _ in range(n)]
        c[-1] = -sum(ci * v for ci, v in zip(c, dp)) - rng.randint(1, 3)
    else:  # c = A^T u + v with v >= 0, so c^T x = u^T b + v^T x is bounded below
        u = [rng.randint(-2, 2) for _ in range(m)]
        v = [rng.choice([0, 0, rng.randint(1, 3)]) for _ in range(n)]
        c = [sum(u[i] * a[i][j] for i in range(m)) + v[j] for j in range(n)]
    b = [sum(r * v for r, v in zip(row, x0)) for row in a]
    return a, b, c, x0


def test_example() -> None:
    # maximize x1 + x2 subject to x1 + 2 x2 <= 4 and 3 x1 + x2 <= 6, with slacks x3 and x4
    a, c = [[1, 2, 1, 0], [3, 1, 0, 1]], [-1, -1, 0, 0]
    res = affine_scaling_method(a, c, [1, 1, 1, 2])
    assert res.status == "optimal"
    assert abs(dot(c, res.x) + 2.8) < TOL
    assert abs(res.y[0] + 0.4) < TOL and abs(res.y[1] + 0.2) < TOL
    expected = [-2.0, -2.48485, -2.67713, -2.75789, -2.78558]
    assert all(abs(u - v) < 1e-5 for u, v in zip(res.values, expected))
    assert affine_scaling_method(a, c, [1, 1, 1, 2], gamma=0.99).iterations < res.iterations


def test_against_brute_force() -> None:
    rng = random.Random(43)
    seen = set()
    cases = 0
    while cases < 600:
        unbounded = cases % 4 == 0
        a, b, c, x0 = instance(rng, unbounded)
        opt = brute_force(a, b, c)
        if opt is None and not unbounded:
            continue  # A has dependent rows and no basis; skip
        cases += 1
        bf = [float(v) for v in b]
        res = affine_scaling_method(a, c, x0)
        seen.add(res.status)
        assert all(u >= v - 1e-12 * (1 + abs(u)) for u, v in zip(res.values, res.values[1:]))  # c^T x never rises
        assert min(res.x) > 0
        size = 1 + max(abs(v) for v in res.x)
        assert all(abs(dot(row, res.x) - bi) <= 1e-9 * size for row, bi in zip(a, bf)), (a, b, c, res)
        if unbounded:
            assert res.status == "unbounded"
            d = res.ray
            scale = max(abs(v) for v in d)
            assert min(d) >= -1e-9 * scale and dot(c, d) < 0
            assert all(abs(dot(row, d)) <= 1e-9 * scale for row in a)
        else:
            assert res.status == "optimal", (a, b, c)
            value = dot(c, res.x)
            assert abs(value - float(opt)) <= TOL * (1 + abs(float(opt))), (value, opt)
            assert abs(dot(bf, res.y) - float(opt)) <= TOL * (1 + abs(float(opt)))  # the dual estimate
    assert seen == {"optimal", "unbounded"}


def test_edge_cases() -> None:
    # one variable fixed by the constraint: the start is optimal
    res = affine_scaling_method([[1]], [5], [2])
    assert res.status == "optimal" and res.iterations == 0 and res.x == [2.0]
    # no constraints with c >= 0: x goes to 0
    res = affine_scaling_method([], [1, 2], [1, 1])
    assert res.status == "optimal" and max(res.x) < 1e-6
    # no constraints with a negative cost: unbounded
    res = affine_scaling_method([], [1, -1], [1, 1])
    assert res.status == "unbounded" and res.ray[1] > 0
