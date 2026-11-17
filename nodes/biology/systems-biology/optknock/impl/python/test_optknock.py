# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optknock/. The authors are listed in prov/K9KY6N.jsonl.
"""Tests of optknock().

The reference is the bilevel program solved in two steps for every knockout
set D: first the inner FBA optimum z(D) = max v_bio, then the largest v_prod
over the inner optimal face (v_bio = z(D)). This uses no duality, so it
checks the single-level LP of optknock.py. Strong duality on each inner LP
is checked against an explicit dual LP, and the inner optimum against the
vertices of the flux polytope.
"""

import random
from fractions import Fraction as F
from itertools import combinations

from optknock import (BIO_N, CAND_N, LB_N, PROD_N, S_N, UB_N, knockout,
                      optknock, single_level_lp)
from sy3lp import polytope_vertices, solve_lp


def inner_fba(S, lb, ub, bio):
    c = [0] * len(lb)
    c[bio] = 1
    return solve_lp(c, A_eq=S, b_eq=[0] * len(S), lb=lb, ub=ub,
                    maximize=True)


def two_step(S, lb, ub, bio, prod, mu_min, pessimistic=False):
    """The bilevel value for fixed bounds, without duality."""
    res = inner_fba(S, lb, ub, bio)
    if res.status != "optimal" or res.value < mu_min:
        return None
    lo, hi = list(lb), list(ub)
    lo[bio] = hi[bio] = res.value
    c = [0] * len(lb)
    c[prod] = 1
    out = solve_lp(c, A_eq=S, b_eq=[0] * len(S), lb=lo, ub=hi,
                   maximize=not pessimistic)
    return out.value


def brute(S, lb, ub, bio, prod, K, cand, mu_min=0):
    best = None
    for k in range(K + 1):
        for D in combinations(cand, k):
            lbD, ubD = knockout(lb, ub, D)
            val = two_step(S, lbD, ubD, bio, prod, mu_min)
            if val is not None and (best is None or val > best):
                best = val
    return best


def test_toy_network():
    assert optknock(S_N, LB_N, UB_N, BIO_N, PROD_N, 0, CAND_N)[1][PROD_N] == 0
    D, v = optknock(S_N, LB_N, UB_N, BIO_N, PROD_N, 1, CAND_N)
    assert v[PROD_N] == 0
    D, v = optknock(S_N, LB_N, UB_N, BIO_N, PROD_N, 2, CAND_N)
    assert D == (1, 2)
    assert v == [10, 0, 0, 5, 5, 5]


def test_growth_floor():
    # With mu_min = 6 the double knockout (growth 5) is not allowed.
    D, v = optknock(S_N, LB_N, UB_N, BIO_N, PROD_N, 2, CAND_N, mu_min=6)
    assert v[PROD_N] == 0 and v[BIO_N] == F(20, 3)
    assert optknock(S_N, LB_N, UB_N, BIO_N, PROD_N, 2, CAND_N, mu_min=7) is None


def test_optimistic_tie():
    # One respiration route A -> E. The growth optimum 5 does not fix the
    # split between respiration and fermentation, so the product at the
    # growth optimum is anything in [0, 5]. OptKnock reports the best case.
    S = [[1, -1, -1, 0, -1], [0, 1, 1, 0, -1], [0, 0, 1, -1, 0]]
    lb = [0] * 5
    ub = [10, None, None, None, None]
    D, v = optknock(S, lb, ub, 4, 3, 0, [1, 2])
    assert v[3] == 5 and v[4] == 5
    assert two_step(S, lb, ub, 4, 3, 0, pessimistic=True) == 0


def dual_value(S, lb, ub, bio):
    n, m = len(S), len(lb)
    A_idx = [j for j in range(m) if ub[j] is not None]
    B_idx = [j for j in range(m) if lb[j] is not None]
    cost = [0] * n + [ub[j] for j in A_idx] + [-lb[j] for j in B_idx]
    A = []
    for j in range(m):
        row = [S[i][j] for i in range(n)]
        row += [int(k == j) for k in A_idx] + [-int(k == j) for k in B_idx]
        A.append(row)
    b = [int(j == bio) for j in range(m)]
    lo = [None] * n + [0] * (len(A_idx) + len(B_idx))
    return solve_lp(cost, A_eq=A, b_eq=b, lb=lo)


def random_case(rng):
    n, m = rng.randint(1, 3), rng.randint(4, 6)
    S = [[rng.randint(-2, 2) for _ in range(m)] for _ in range(n)]
    lb = [rng.choice([0, 0, -1]) for _ in range(m)]
    ub = [rng.randint(1, 3) for _ in range(m)]
    bio, prod = rng.sample(range(m), 2)
    return S, lb, ub, bio, prod


def test_strong_duality_and_vertices():
    rng = random.Random(21)
    for _ in range(25):
        S, lb, ub, bio, prod = random_case(rng)
        for D in [(), (rng.randrange(len(lb)),)]:
            lbD, ubD = knockout(lb, ub, D)
            primal = inner_fba(S, lbD, ubD, bio)
            dual = dual_value(S, lbD, ubD, bio)
            assert primal.status == dual.status == "optimal"
            assert primal.value == dual.value
            verts = polytope_vertices(S, [0] * len(S), lbD, ubD)
            assert primal.value == max(v[bio] for v in verts)


def test_single_level_matches_two_step():
    rng = random.Random(22)
    for _ in range(25):
        S, lb, ub, bio, prod = random_case(rng)
        res = single_level_lp(S, lb, ub, bio, prod)
        ref = two_step(S, lb, ub, bio, prod, 0)
        assert res.status == "optimal" and res.x[prod] == ref


def test_against_enumeration():
    rng = random.Random(23)
    for _ in range(8):
        S, lb, ub, bio, prod = random_case(rng)
        cand = [j for j in range(len(lb)) if j not in (bio, prod)]
        for K in (1, 2):
            got = optknock(S, lb, ub, bio, prod, K, cand)
            assert got[1][prod] == brute(S, lb, ub, bio, prod, K, cand)
