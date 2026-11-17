# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flux-variability-analysis/. The authors are listed in prov/3ZQX3G.jsonl.
"""Tests of fva() against enumeration of the vertices of the polytope.

The set {S v = 0, lb <= v <= ub, c v >= t} is a polytope when the bounds are
finite. A linear function takes its minimum and its maximum over a polytope
at vertices, so the range of v_j is the range of v_j over the vertices.
The constraint c v >= t is written with a slack s = c v - t in [0, U].
"""

import random
from fractions import Fraction as F

from flux_variability_analysis import (C_N, LB_N, S_N, UB_N,
                                       blocked_reactions, fva)
from sy3lp import polytope_vertices, solve_lp


def brute_ranges(S, lb, ub, c, t, big):
    """Ranges of each v_j over the vertices, with a slack in [0, big]."""
    m = len(c)
    A = [list(row) + [0] for row in S] + [list(c) + [-1]]
    b = [0] * len(S) + [t]
    verts = polytope_vertices(A, b, list(lb) + [0], list(ub) + [big])
    return [(min(v[j] for v in verts), max(v[j] for v in verts))
            for j in range(m)]


def test_network_n_fraction_one():
    z, ranges = fva(S_N, LB_N, UB_N, C_N)
    assert z == F(20, 3)
    assert ranges == [(10, 10), (0, F(10, 3)), (0, F(10, 3)), (0, 0),
                      (0, 0), (F(20, 3), F(20, 3))]


def test_network_n_fraction_09():
    z, ranges = fva(S_N, LB_N, UB_N, C_N, fraction=F(9, 10))
    assert z == F(20, 3)
    # c v >= 6. With uptake a, respiration r and fermentation f:
    # growth = 2r + f, a = 3r + 2f <= 10.
    assert ranges[5] == (6, F(20, 3))
    assert ranges[3] == (0, 2)
    assert ranges[0] == (9, 10)
    big = 100
    ub = [x if x is not None else big for x in UB_N]
    assert ranges == brute_ranges(S_N, LB_N, ub, C_N, 6, big)


def test_unbounded_range():
    # A free internal cycle A -> B -> A with no bound gives an infinite range.
    S = [[1, -1, 1, -1], [0, 1, -1, 0]]
    lb = [0, 0, 0, 0]
    ub = [5, None, None, None]
    c = [0, 0, 0, 1]
    z, ranges = fva(S, lb, ub, c)
    assert z == 5
    assert ranges[1] == (0, None) and ranges[2] == (0, None)
    assert ranges[3] == (5, 5)


def test_blocked():
    # The third reaction makes D, which nothing uses.
    S = [[1, -1, -1], [0, 0, 1]]
    assert blocked_reactions(S, [0, 0, 0], [4, 4, 4]) == [2]


def random_case(rng):
    n, m = rng.randint(1, 3), rng.randint(3, 6)
    S = [[rng.randint(-2, 2) for _ in range(m)] for _ in range(n)]
    lb = [rng.choice([0, 0, -1, -2]) for _ in range(m)]
    ub = [rng.randint(0, 3) for _ in range(m)]
    c = [rng.randint(-1, 2) for _ in range(m)]
    return S, lb, ub, c


def test_random_against_vertices():
    rng = random.Random(7)
    for _ in range(25):
        S, lb, ub, c = random_case(rng)
        f = rng.choice([F(1), F(1), F(9, 10), F(1, 2)])
        z, ranges = fva(S, lb, ub, c, fraction=f)
        t = z - (1 - f) * abs(z)
        big = sum(abs(ci) * max(abs(lo), abs(hi))
                  for ci, lo, hi in zip(c, lb, ub)) + abs(t) + 1
        assert ranges == brute_ranges(S, lb, ub, c, t, big)


def test_optimal_vertex_inside_ranges():
    rng = random.Random(8)
    for _ in range(25):
        S, lb, ub, c = random_case(rng)
        z, ranges = fva(S, lb, ub, c)
        v = solve_lp(c, A_eq=S, b_eq=[0] * len(S), lb=lb, ub=ub,
                     maximize=True).x
        assert all(lo <= x <= hi for x, (lo, hi) in zip(v, ranges))
        # The objective is fixed on the optimal face.
        if c == [0] * (len(c) - 1) + [1]:
            assert ranges[-1] == (z, z)
