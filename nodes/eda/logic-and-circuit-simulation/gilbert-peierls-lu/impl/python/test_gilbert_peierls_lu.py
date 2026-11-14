# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gilbert-peierls-lu/. The authors are listed in prov/6ASGQ9.jsonl.

import random
from fractions import Fraction as F

import pytest

from gilbert_peierls_lu import SingularMatrixError, gp_lu, gp_solve
from sim3dense import solve

EXAMPLE = [
    [F(1), F(0), F(0), F(2)],
    [F(4), F(2), F(0), F(0)],
    [F(0), F(1), F(1), F(0)],
    [F(0), F(0), F(-1), F(1)],
]


def random_matrix(rng, n, density, exact=True):
    while True:
        a = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j or rng.random() < density:
                    v = rng.randint(-9, 9)
                    a[i][j] = F(v) if exact else float(v) + rng.random()
        try:
            solve([[F(x) for x in row] for row in a], [F(1)] * n)
            return a
        except ValueError:
            continue


def dense_factors(f):
    n = f.n
    pos = {r: k for k, r in enumerate(f.pivrow)}
    lo = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    up = [[F(0)] * n for _ in range(n)]
    for k in range(n):
        for r, l in f.lcols[k].items():
            lo[pos[r]][k] = l
        for j, v in f.ucols[k].items():
            up[j][k] = v
    return lo, up


def symbolic_lu(pattern):
    """Brute force: dense symbolic elimination without pivoting; returns (L set, U set)."""
    n = len(pattern)
    m = [row[:] for row in pattern]
    for k in range(n):
        for i in range(k + 1, n):
            if m[i][k]:
                for j in range(k + 1, n):
                    if m[k][j]:
                        m[i][j] = True
    lset = {(i, k) for k in range(n) for i in range(k + 1, n) if m[i][k]}
    uset = {(k, j) for k in range(n) for j in range(k, n) if m[k][j]}
    return lset, uset


def test_example_trace():
    f = gp_lu(EXAMPLE)
    assert f.pivrow == [1, 2, 3, 0]
    assert f.lcols == [{0: F(1, 4)}, {0: F(-1, 2)}, {0: F(-1, 2)}, {}]
    assert f.ucols == [{0: F(4)}, {0: F(2), 1: F(1)}, {1: F(1), 2: F(-1)}, {2: F(1), 3: F(5, 2)}]
    assert f.reach_per_column == [2, 3, 3, 2]
    assert (f.flops, f.dfs_edges, f.dfs_nodes) == (3, 3, 10)
    b = [F(3), F(6), F(2), F(0)]
    assert gp_solve(EXAMPLE, b) == solve(EXAMPLE, b) == [F(1)] * 4


def test_exact_factors_patterns_and_work():
    rng = random.Random(21)
    for _ in range(200):
        n = rng.randint(1, 8)
        a = random_matrix(rng, n, rng.choice([0.15, 0.3, 0.6]))
        f = gp_lu(a)
        lo, up = dense_factors(f)
        pa = [a[r] for r in f.pivrow]
        assert [[sum(lo[i][t] * up[t][j] for t in range(n)) for j in range(n)] for i in range(n)] == pa
        lset, uset = symbolic_lu([[x != 0 for x in row] for row in pa])
        pos = {r: k for k, r in enumerate(f.pivrow)}
        assert {(pos[r], k) for k in range(n) for r in f.lcols[k]} == lset
        assert {(j, k) for k in range(n) for j in f.ucols[k]} == uset
        for k in range(n):
            for l in f.lcols[k].values():
                assert abs(l) <= 1
        nnz = sum(1 for row in a for x in row if x != 0)
        assert f.dfs_edges == f.flops
        assert f.dfs_nodes <= nnz + f.flops
        b = [F(rng.randint(-5, 5)) for _ in range(n)]
        assert gp_solve(a, b) == solve(a, b)


def test_float_matrices():
    rng = random.Random(22)
    for n in (20, 60):
        a = random_matrix(rng, n, 3 / n, exact=False)
        b = [rng.uniform(-1, 1) for _ in range(n)]
        x = gp_solve(a, b, tol=1e-14)
        r = max(abs(sum(a[i][j] * x[j] for j in range(n)) - b[i]) for i in range(n))
        assert r < 1e-9


def test_mna_zero_diagonal_needs_pivoting():
    # 6 V source at node 1, 2 ohm from 1 to 2, 3 ohm from 2 to ground, 1 A into node 2.
    # Unknowns (e1, e2, j); the source row has a zero diagonal.
    a = [[F(1, 2), F(-1, 2), F(1)], [F(-1, 2), F(5, 6), F(0)], [F(1), F(0), F(0)]]
    assert gp_solve(a, [F(0), F(1), F(6)]) == [F(6), F(24, 5), F(-3, 5)]


def test_work_is_linear_on_tridiagonal():
    for n in (500, 1000, 2000):
        a = [{} for _ in range(n)]
        for j in range(n):
            a[j][j] = 4.0
            if j > 0:
                a[j][j - 1] = -1.0
            if j + 1 < n:
                a[j][j + 1] = -1.0
        f = gp_lu(a)
        assert f.flops == n - 1
        assert f.dfs_edges == n - 1
        assert f.dfs_nodes == 3 * n - 2


def test_singular():
    with pytest.raises(SingularMatrixError):
        gp_lu([[F(1), F(2)], [F(2), F(4)]])
    with pytest.raises(SingularMatrixError):
        gp_lu([[F(1), F(0)], [F(1), F(0)]])
