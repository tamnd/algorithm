# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flux-balance-analysis/. The authors are listed in prov/TC2TH5.jsonl.
"""Tests of the shared module sy3lp.py and of fba().

The reference for fba() is the maximum of c v over all vertices of the flux
polytope, found by brute force, and the value of the dual LP.
"""

import random
from fractions import Fraction as F

from flux_balance_analysis import (C_N, LB_N, S_N, UB_N, fba,
                                   knockout_bounds)
from sy3lp import (nullspace, polytope_vertices, rank, rref, simplex_standard,
                   solve_linear, solve_lp)


def matvec(M, x):
    return [sum(F(a) * b for a, b in zip(row, x)) for row in M]


def random_matrix(rng, rows, cols, lo=-2, hi=2):
    return [[rng.randint(lo, hi) for _ in range(cols)] for _ in range(rows)]


# Tests of sy3lp.py.

def test_rref_and_rank():
    R, piv = rref([[1, 2, 3], [2, 4, 6], [1, 0, 1]])
    assert piv == [0, 1]
    assert R == [[1, 0, 1], [0, 1, 1], [0, 0, 0]]
    assert rank([[1, 2], [2, 4]]) == 1
    assert rank([]) == 0


def test_nullspace_random():
    rng = random.Random(1)
    for _ in range(60):
        rows, cols = rng.randint(1, 4), rng.randint(1, 6)
        M = random_matrix(rng, rows, cols)
        B = nullspace(M, cols)
        assert len(B) == cols - rank(M)
        for x in B:
            assert all(v == 0 for v in matvec(M, x))
        if B:
            assert rank(B) == len(B)


def test_solve_linear():
    rng = random.Random(2)
    for _ in range(60):
        rows, cols = rng.randint(1, 4), rng.randint(1, 5)
        A = random_matrix(rng, rows, cols)
        x0 = [rng.randint(-3, 3) for _ in range(cols)]
        b = matvec(A, x0)
        x = solve_linear(A, b)
        assert x is not None and matvec(A, x) == b
    assert solve_linear([[1, 1], [1, 1]], [1, 2]) is None


def test_beale_cycling_example():
    # Beale (1955): Dantzig's rule with the lowest-index tie break cycles here.
    A = [[1, 0, 0, F(1, 4), -8, -1, 9],
         [0, 1, 0, F(1, 2), -12, F(-1, 2), 3],
         [0, 0, 1, 0, 0, 1, 0]]
    c = [0, 0, 0, F(-3, 4), 20, F(-1, 2), 6]
    res = simplex_standard(A, [0, 0, 1], c)
    assert res.status == "optimal"
    assert res.value == F(-5, 4)


def test_simplex_status():
    assert simplex_standard([[1, 1]], [-1], [1, 1]).status == "infeasible"
    assert simplex_standard([[1, -1]], [0], [-1, 0]).status == "unbounded"
    # A redundant row is dropped after phase 1.
    res = simplex_standard([[1, 1], [2, 2]], [1, 2], [1, 2])
    assert res.status == "optimal" and res.x == [1, 0]


def test_solve_lp_against_vertices():
    rng = random.Random(3)
    for _ in range(40):
        n = rng.randint(2, 5)
        rows = rng.randint(1, 2)
        A = random_matrix(rng, rows, n)
        lb = [rng.randint(-3, 0) for _ in range(n)]
        ub = [lo + rng.randint(0, 4) for lo in lb]
        x0 = [rng.randint(lo, hi) for lo, hi in zip(lb, ub)]
        b = matvec(A, x0)
        c = [rng.randint(-3, 3) for _ in range(n)]
        verts = polytope_vertices(A, b, lb, ub)
        assert verts
        best = min(sum(F(ci) * vi for ci, vi in zip(c, v)) for v in verts)
        res = solve_lp(c, A_eq=A, b_eq=b, lb=lb, ub=ub)
        assert res.status == "optimal" and res.value == best
        res = solve_lp(c, A_le=A, b_le=b, lb=lb, ub=ub, maximize=True)
        assert res.status == "optimal"
        assert all(a <= bi for a, bi in zip(matvec(A, res.x), b))


def test_solve_lp_free_and_upper_only():
    # minimize x0 - x1 with x0 free, x1 <= 2, x0 + x1 = 1: x1 = 2, x0 = -1.
    res = solve_lp([1, -1], A_eq=[[1, 1]], b_eq=[1], lb=[None, None],
                   ub=[None, 2])
    assert res.status == "optimal" and res.x == [-1, 2] and res.value == -3


# Tests of fba().

def test_network_n():
    res = fba(S_N, LB_N, UB_N, C_N)
    assert res.status == "optimal"
    assert res.z == F(20, 3)
    v = res.v
    assert v[0] == 10 and v[1] + v[2] == F(10, 3) and v[3] == 0 and v[4] == 0
    assert all(x == 0 for x in matvec(S_N, v))


def test_network_n_knockouts():
    lb, ub = knockout_bounds(LB_N, UB_N, [1, 2])
    res = fba(S_N, lb, ub, C_N)
    assert res.z == 5 and res.v == [10, 0, 0, 5, 5, 5]
    lb, ub = knockout_bounds(LB_N, UB_N, [1])
    assert fba(S_N, lb, ub, C_N).z == F(20, 3)
    lb, ub = knockout_bounds(LB_N, UB_N, [0])
    res = fba(S_N, lb, ub, C_N)
    assert res.z == 0 and res.v == [0] * 6


def test_infeasible_and_unbounded():
    # A forced secretion of P with no source of P.
    lb = list(LB_N)
    lb[4] = 1
    lb2, ub2 = knockout_bounds(lb, UB_N, [3])
    assert fba(S_N, lb2, ub2, C_N).status == "infeasible"
    # Without the uptake bound the growth is unbounded.
    ub = list(UB_N)
    ub[0] = None
    assert fba(S_N, LB_N, ub, C_N).status == "unbounded"
    assert fba([[1]], [2], [1], [1]).status == "infeasible"


def dual_value(S, lb, ub, c):
    """min ub alpha - lb beta s.t. S^T lam + alpha - beta = c, alpha, beta >= 0.

    All bounds are finite here. Variables: lam (free, one per metabolite),
    then alpha, then beta (one per reaction each).
    """
    n, m = len(S), len(c)
    cost = [0] * n + list(ub) + [-x for x in lb]
    A = []
    for j in range(m):
        row = [S[i][j] for i in range(n)]
        row += [int(k == j) for k in range(m)] + [-int(k == j) for k in range(m)]
        A.append(row)
    lo = [None] * n + [0] * (2 * m)
    return solve_lp(cost, A_eq=A, b_eq=c, lb=lo)


def random_network(rng):
    n, m = rng.randint(1, 3), rng.randint(3, 6)
    S = random_matrix(rng, n, m)
    lb = [rng.choice([0, 0, -1, -2]) for _ in range(m)]
    ub = [rng.randint(0, 3) for _ in range(m)]
    c = [rng.randint(-1, 2) for _ in range(m)]
    return S, lb, ub, c


def test_random_networks_against_vertices_and_dual():
    rng = random.Random(4)
    for _ in range(50):
        S, lb, ub, c = random_network(rng)
        res = fba(S, lb, ub, c)
        verts = polytope_vertices(S, [0] * len(S), lb, ub)
        # v = 0 lies in the box and satisfies S v = 0, so the LP is feasible.
        assert verts and res.status == "optimal"
        best = max(sum(F(ci) * vi for ci, vi in zip(c, v)) for v in verts)
        assert res.z == best
        assert all(x == 0 for x in matvec(S, res.v))
        assert all(lo <= x <= hi for lo, x, hi in zip(lb, res.v, ub))
        dual = dual_value(S, lb, ub, c)
        assert dual.status == "optimal" and dual.value == res.z


def test_fba_matches_solve_lp_with_infinite_bounds():
    rng = random.Random(5)
    for _ in range(40):
        S, lb, ub, c = random_network(rng)
        lb = [None if rng.random() < 0.3 else x for x in lb]
        ub = [None if rng.random() < 0.3 else x for x in ub]
        res = fba(S, lb, ub, c)
        ref = solve_lp(c, A_eq=S, b_eq=[0] * len(S), lb=lb, ub=ub,
                       maximize=True)
        assert res.status == ref.status
        if res.status == "optimal":
            assert res.z == ref.value
