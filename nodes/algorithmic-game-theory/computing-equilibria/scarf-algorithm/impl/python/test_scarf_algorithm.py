# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scarf-algorithm/. The authors are listed in prov/E57190.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from agtgame import from_bimatrix, is_epsilon_nash, max_gain
from scarf_algorithm import (ScarfGrid, approximate_fixed_point, approximate_symmetric_equilibrium,
                             brouwer_label, primitive_sets, scarf)

F = Fraction
HALF = F(1, 2)
SMALL = [(1, 3), (2, 3), (2, 4), (3, 2)]
_CACHE = {}


def grid_and_prims(d, N):
    if (d, N) not in _CACHE:
        grid = ScarfGrid(d, N)
        _CACHE[(d, N)] = (grid, primitive_sets(grid))
    return _CACHE[(d, N)]


def labels_of(grid, S, point_label):
    return sorted(v if grid.is_slack(v) else point_label(grid.point(v)) for v in S)


def test_each_member_of_a_primitive_set_holds_one_order():
    for d, N in SMALL:
        grid, prims = grid_and_prims(d, N)
        for S in prims:
            assert len({grid.minimum(S, i) for i in range(d + 1)}) == d + 1


def test_doors_lie_in_two_primitive_sets_except_the_slack_sets():
    for d, N in SMALL:
        grid, prims = grid_and_prims(d, N)
        count = {}
        for S in prims:
            for Q in combinations(S, d):
                count[Q] = count.get(Q, 0) + 1
        boundary = sorted(Q for Q, c in count.items() if c == 1)
        assert boundary == sorted(combinations(range(d + 1), d))
        assert all(c <= 2 for c in count.values())
        for S in prims:
            for y in S:
                Q = [v for v in S if v != y]
                if count[tuple(Q)] == 2:
                    z = grid.replace(list(S), y)
                    assert z != y and grid.is_primitive(Q + [z])


def test_random_labelings_odd_count_and_path():
    rng = random.Random(20261120)
    for d, N in SMALL:
        grid, prims = grid_and_prims(d, N)
        for _ in range(15):
            table = {p: rng.randint(0, d) for p in grid.points}

            def lab(p):
                return table[tuple(int(c * N) for c in p)]

            full = [S for S in prims if labels_of(grid, S, lab) == list(range(d + 1))]
            assert len(full) % 2 == 1
            trace = []
            P, pivots = scarf(grid, lab, trace)
            assert tuple(sorted(P)) in full
            assert len(trace) == pivots + 1
            assert len({tuple(sorted(S)) for S in trace}) == len(trace)
            for S in trace:
                assert grid.is_primitive(S)
                assert set(range(1, d + 1)) <= set(labels_of(grid, S, lab))


def test_start_is_already_complete():
    grid = ScarfGrid(2, 5)
    P, pivots = scarf(grid, lambda p: 0)
    assert pivots == 0 and sorted(P) == [1, 2, grid.vertex_e0()]


def test_cyclic_map_example():
    grid = ScarfGrid(2, 4)
    f = (lambda p: (p[1], p[2], p[0]))
    P, pivots = scarf(grid, brouwer_label(f))
    assert pivots == 3
    assert sorted(grid.points[v - 3] for v in P) == [(1, 2, 1), (2, 1, 1), (3, 1, 0)]


def stochastic_map(rng, k):
    cols = []
    for _ in range(k):
        w = [rng.randint(0, 5) for _ in range(k)]
        if sum(w) == 0:
            w[0] = 1
        cols.append([F(v, sum(w)) for v in w])
    M = [[cols[c][r] for c in range(k)] for r in range(k)]
    lam = max(sum(row) for row in M)
    return (lambda p: tuple(sum((M[r][c] * p[c] for c in range(k)), F(0)) for r in range(k))), lam


def test_linear_maps_within_the_bound():
    rng = random.Random(4)
    for d, N in [(1, 10), (1, 31), (2, 8), (2, 15), (3, 6)]:
        for _ in range(3):
            f, lam = stochastic_map(rng, d + 1)
            p = approximate_fixed_point(f, d, N)
            assert sum(p) == 1 and min(p) >= 0
            err = max(abs(a - b) for a, b in zip(f(p), p))
            assert err <= F(d * (d + 1), N) * (1 + lam)


def test_symmetric_games():
    rps = [[HALF, 0, 1], [1, HALF, 0], [0, 1, HALF]]
    chicken = [[0, 1], [F(2, 7), F(6, 7)]]
    for C in (rps, chicken):
        k = len(C)
        game = from_bimatrix(C, [list(r) for r in zip(*C)])
        gains = []
        for N in (6, 12, 24):
            q = approximate_symmetric_equilibrium(C, N)
            assert is_epsilon_nash(game, [q, q], F(2 * k * k, N))
            gains.append(max_gain(game, [q, q]))
        assert gains[-1] <= F(2 * k * k, 24)
    # Chicken: the mixed equilibrium plays C (strategy 1) with probability 2/3, a grid point for N = 24.
    q = approximate_symmetric_equilibrium(chicken, 24)
    assert abs(q[1] - F(2, 3)) <= F(4, 24)
