# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algebraic-multigrid/. The authors are listed in prov/EZNBXD.jsonl.
import math
import random
from fractions import Fraction as F

import pytest

from algebraic_multigrid import (Singular, matvec, strength, split, interpolation,
                                 galerkin, setup, lu_solve_dense, gauss_seidel,
                                 vcycle, solve, pcg, poisson2d)


def tridiag(n, d=2, o=-1, kind=F):
    a = [{i: kind(d)} for i in range(n)]
    for i in range(n - 1):
        a[i][i + 1] = kind(o)
        a[i + 1][i] = kind(o)
    return a


def rand_spd(rng, n, kind=float, positive=False):
    """Symmetric, strictly diagonally dominant with positive diagonal,
    hence SPD. Off-diagonals mostly negative; some positive if asked."""
    a = [dict() for _ in range(n)]
    p = rng.choice([0.15, 0.3, 0.6])
    for i in range(n):
        for j in range(i):
            if rng.random() < p:
                v = -rng.randint(1, 9)
                if positive and rng.random() < 0.2:
                    v = -v
                a[i][j] = a[j][i] = kind(v)
    for i in range(n):
        a[i][i] = kind(sum(abs(v) for v in a[i].values()) + rng.randint(0, 3) + 1)
    return a


def dense(a, n):
    return [[a[i].get(j, 0) for j in range(n)] for i in range(n)]


def energy(a, e):
    return sum(x * y for x, y in zip(e, matvec(a, e)))


def test_page_example():
    a = tridiag(7)
    s = strength(a, 0.25)
    c = split(s)
    assert [i + 1 for i in range(7) if c[i]] == [2, 4, 6]
    p, nc = interpolation(a, s, c)
    assert nc == 3 and p[0] == {0: F(1, 2)} and p[2] == {0: F(1, 2), 1: F(1, 2)}
    ac = galerkin(a, p, nc)
    assert dense(ac, 3) == [[1, F(-1, 2), 0], [F(-1, 2), 1, F(-1, 2)], [0, F(-1, 2), 1]]
    lv = setup(a, max_coarse=3)
    assert len(lv) == 2
    b = [F(1)] * 7
    xs = [F(i * (8 - i), 2) for i in range(1, 8)]
    x0 = [F(0)] * 7
    x1 = vcycle(lv, b, x0)
    assert x1[0] == F(27601, 8192) and x1[6] == F(7, 2)
    e0 = [u - v for u, v in zip(xs, x0)]
    e1 = [u - v for u, v in zip(xs, x1)]
    assert energy(a, e1) / energy(a, e0) == F(1952217, 469762048)


def test_zero_row_sums_preserved_exactly():
    rng = random.Random(31)
    for _ in range(500):
        n = rng.randint(2, 14)
        a = rand_spd(rng, n, F)
        for i in range(n):  # make row sums zero: a singular M-matrix
            a[i][i] = -sum(v for j, v in a[i].items() if j != i)
        s = strength(a, 0.25)
        c = split(s)
        p, nc = interpolation(a, s, c)
        for i in range(n):
            if not c[i] and p[i]:
                assert sum(p[i].values()) == 1
        if nc:
            ac = galerkin(a, p, nc)
            for row in ac:
                assert sum(row.values()) == 0


def test_galerkin_against_dense_product():
    rng = random.Random(8)
    for _ in range(500):
        n = rng.randint(1, 12)
        a = rand_spd(rng, n, F, positive=True)
        s = strength(a, rng.choice([0.25, 0.5]))
        c = split(s)
        p, nc = interpolation(a, s, c)
        ad = dense(a, n)
        pd = [[p[i].get(j, 0) for j in range(nc)] for i in range(n)]
        ref = [[sum(pd[k][i] * ad[k][l] * pd[l][j] for k in range(n) for l in range(n))
                for j in range(nc)] for i in range(nc)]
        assert dense(galerkin(a, p, nc), nc) == ref
        for i in range(n):  # splitting property used by direct interpolation
            if not c[i]:
                ci = {j for j in s[i] if c[j]}
                assert ci or not any(a[i][j] < 0 for j in s[i])
                for j in s[i]:
                    if not c[j]:
                        assert s[j] & ci


def test_vcycle_contracts_energy_norm():
    rng = random.Random(2024)
    worst = 0.0
    for t in range(500):
        n = rng.randint(1, 30)
        a = rand_spd(rng, n, float, positive=(t % 3 == 0))
        lv = setup(a, max_coarse=rng.choice([1, 3, 6]))
        xs = [rng.uniform(-1, 1) for _ in range(n)]
        b = matvec(a, xs)
        x0 = [rng.uniform(-1, 1) for _ in range(n)]
        x1 = vcycle(lv, b, x0)
        e0 = [u - v for u, v in zip(xs, x0)]
        e1 = [u - v for u, v in zip(xs, x1)]
        q = math.sqrt(energy(a, e1) / energy(a, e0))
        assert q < 1 + 1e-9
        worst = max(worst, q)
    assert worst < 0.9  # observed on these diagonally dominant matrices


def test_vcycle_preconditioner_symmetric():
    rng = random.Random(6)
    for _ in range(60):
        n = rng.randint(2, 25)
        a = rand_spd(rng, n, float)
        lv = setup(a, max_coarse=2)
        u = [rng.uniform(-1, 1) for _ in range(n)]
        v = [rng.uniform(-1, 1) for _ in range(n)]
        bu, bv = vcycle(lv, u), vcycle(lv, v)
        lhs = sum(x * y for x, y in zip(u, bv))
        rhs = sum(x * y for x, y in zip(v, bu))
        assert abs(lhs - rhs) <= 1e-10 * (abs(lhs) + 1)
        assert sum(x * y for x, y in zip(u, bu)) > 0


def test_poisson_iterations_independent_of_size():
    its = []
    for k in (8, 16, 32):
        a = poisson2d(k)
        st = {}
        lv = setup(a, stats=st)
        rng = random.Random(k)
        b = [rng.uniform(-1, 1) for _ in a]
        x, info = solve(a, b, levels=lv)
        h = info["history"]
        assert info["converged"]
        assert max(h[i + 1] / h[i] for i in range(2, len(h) - 1)) < 0.25  # observed
        assert st["operator_complexity"] < 2.5 and st["grid_complexity"] < 1.8
        r = [bi - ai for bi, ai in zip(b, matvec(a, x))]
        assert math.sqrt(sum(t * t for t in r)) <= 1e-8 * math.sqrt(sum(t * t for t in b))
        _, info2 = pcg(a, b, levels=lv)
        assert info2["converged"] and info2["iterations"] < info["iterations"]
        its.append(info["iterations"])
    assert max(its) - min(its) <= 1 and max(its) <= 12


def test_anisotropic_semicoarsening():
    for eps in (0.001, 0.01):
        a = poisson2d(24, eps)
        st = {}
        lv = setup(a, stats=st)
        assert st["sizes"][1] == 288  # coarsened along the strong direction only
        b = [1.0] * len(a)
        _, info = solve(a, b, levels=lv)
        assert info["converged"] and info["iterations"] <= 13


def test_edge_cases():
    x, info = solve([{0: 3.0}], [6.0])
    assert x == [2.0] and info["iterations"] == 1
    d = [{i: float(i + 1)} for i in range(30)]
    st = {}
    lv = setup(d, stats=st)
    assert st["levels"] == 1
    x, info = solve(d, [1.0] * 30, levels=lv)
    assert info["iterations"] == 1 and abs(x[29] - 1 / 30) < 1e-15
    low = [{i: 4.0} for i in range(40)]
    for i in range(1, 40):
        low[i][i - 1] = -1.0
        if i > 1:
            low[i][i - 2] = -1.0
    x, info = solve(low, [1.0] * 40, max_coarse=4)
    assert info["iterations"] == 1  # forward Gauss-Seidel is exact
    assert lu_solve_dense([{1: F(1)}, {0: F(2)}], [F(3), F(4)]) == [2, 3]  # pivot swap
    h = [{j: F(1, i + j + 1) for j in range(8)} for i in range(8)]
    st = {}
    lv = setup(h, max_coarse=2, stats=st)
    assert st["levels"] == 1  # no negative couplings: no coarse grid
    xs = [F(1)] * 8
    assert vcycle(lv, matvec(h, xs)) == xs


def test_wilkinson_growth_in_coarse_solver():
    n = 12
    w = [{j: F(1) if j == i or j == n - 1 else F(-1) if j < i else F(0)
          for j in range(n)} for i in range(n)]
    xs = [F(i - 5) for i in range(n)]
    assert lu_solve_dense(w, matvec(w, xs)) == xs


def test_singular_and_indefinite_reported():
    a = tridiag(9, kind=float)
    a[0][0] = a[8][8] = 1.0  # Neumann: row sums zero, singular
    with pytest.raises(Singular):
        solve(a, [0.0] * 9, max_coarse=3)
    shifted = poisson2d(12)
    for row_i, row in enumerate(shifted):
        row[row_i] -= 1.0  # indefinite: smallest eigenvalue < 0
    _, info = solve(shifted, [1.0] * 144, maxit=60)
    assert not info["converged"]


def test_iteration_limit_reported():
    a = poisson2d(10)
    _, info = solve(a, [1.0] * 100, tol=1e-30, maxit=4)
    assert not info["converged"] and info["iterations"] == 4
    h = info["history"]
    assert all(h[i + 1] < h[i] for i in range(len(h) - 1))
