# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimization-of-metabolic-adjustment/. The authors are listed in prov/845EGQ.jsonl.
"""Tests of moma().

References:
- hand solutions on the toy network N, checked on a grid of feasible points;
- the projection inequality: v is the point of a convex set P closest to w
  if and only if (w - v) . (p - v) <= 0 for every p in P. For a polytope it
  is enough to test the vertices p, found by brute force.
"""

import random
from fractions import Fraction as F

from minimization_of_metabolic_adjustment import (C_N, LB_N, S_N, UB_N, moma,
                                                  sq_dist)
from sy3lp import polytope_vertices, solve_lp

W_N = [10, F(10, 3), 0, 0, 0, F(20, 3)]


def knockout(lb, ub, ko):
    lb, ub = list(lb), list(ub)
    for j in ko:
        lb[j] = ub[j] = 0
    return lb, ub


def test_wild_type_is_fba_optimum():
    res = solve_lp(C_N, A_eq=S_N, b_eq=[0, 0, 0], lb=LB_N, ub=UB_N,
                   maximize=True)
    assert res.x == W_N


def test_double_knockout_on_a_line():
    lb, ub = knockout(LB_N, UB_N, [1, 2])
    v = moma(S_N, lb, ub, W_N)
    z = F(80, 21)
    assert v == [2 * z, 0, 0, z, z, z]
    # The feasible set is v = (2t, 0, 0, t, t, t) with 0 <= t <= 5.
    best = sq_dist(v, W_N)
    for k in range(0, 501):
        t = F(k, 100)
        assert best <= sq_dist([2 * t, 0, 0, t, t, t], W_N)


def test_single_knockout_on_a_grid():
    lb, ub = knockout(LB_N, UB_N, [1])
    v = moma(S_N, lb, ub, W_N)
    assert v == [F(485, 51), 0, F(45, 17), F(40, 51), F(40, 51), F(310, 51)]
    # FBA keeps the growth 20/3 here; MOMA predicts less.
    assert v[5] < F(20, 3)
    # Feasible set: v = (3a + 2b, 0, a, b, b, 2a + b), a, b >= 0, 3a + 2b <= 10.
    best = sq_dist(v, W_N)
    for i in range(0, 61):
        for k in range(0, 61):
            a, b = F(i, 18), F(k, 12)
            if 3 * a + 2 * b <= 10:
                p = [3 * a + 2 * b, 0, a, b, b, 2 * a + b]
                assert best <= sq_dist(p, W_N)


def test_feasible_reference_is_returned():
    lb, ub = knockout(LB_N, UB_N, [2])
    assert moma(S_N, lb, ub, W_N) == W_N


def test_infeasible():
    lb, ub = knockout(LB_N, UB_N, [5])
    lb[5] = 1
    ub[5] = 1
    lb, ub = knockout(lb, ub, [0])
    assert moma(S_N, lb, ub, W_N) is None


def test_random_against_projection_inequality():
    rng = random.Random(11)
    done = 0
    while done < 30:
        n, m = rng.randint(1, 2), rng.randint(3, 5)
        S = [[rng.randint(-2, 2) for _ in range(m)] for _ in range(n)]
        lb = [rng.choice([0, -1, -2]) for _ in range(m)]
        ub = [rng.randint(0, 3) for _ in range(m)]
        w = [F(rng.randint(-6, 6), rng.randint(1, 3)) for _ in range(m)]
        v = moma(S, lb, ub, w)
        verts = polytope_vertices(S, [0] * n, lb, ub)
        assert v is not None and verts  # v = 0 is always feasible here
        assert all(sum(F(a) * b for a, b in zip(row, v)) == 0 for row in S)
        assert all(lo <= x <= hi for lo, x, hi in zip(lb, v, ub))
        for p in verts:
            assert sum((wi - vi) * (pi - vi) for wi, vi, pi in zip(w, v, p)) <= 0
        done += 1
