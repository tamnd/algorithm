# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arora-euclidean-tsp-ptas/. The authors are listed in prov/CVQVJX.jsonl.

import itertools
import math
import random

from arora_euclidean_tsp_ptas import arora_tour, detour, length, line_level, portal_count, quadtree, snap

SEVEN = [(1, 2), (0, 5), (3, 3), (1, 0), (0, 0), (3, 4), (2, 6)]  # A to G of the page
OPT_SEVEN = [0, 4, 3, 2, 5, 6, 1]  # A E D C F G B, length 15.476


def brute_order(points):
    n = len(points)
    return min(([0, *q] for q in itertools.permutations(range(1, n))), key=lambda o: length(points, o))


def crossings(pts):
    n = len(pts)
    return sum(abs(pts[i][0] - pts[(i + 1) % n][0]) + abs(pts[i][1] - pts[(i + 1) % n][1]) for i in range(n))


def test_snap_moves_each_tour_little() -> None:
    rng = random.Random(1996)
    for n in (3, 5, 8):
        for c in (1.0, 2.0):
            points = [(rng.uniform(0, 5), rng.uniform(0, 3)) for _ in range(n)]
            grid, delta, L = snap(points, c)
            assert all(0 <= v < L for g in grid for v in g) and L & (L - 1) == 0
            x0, y0 = min(p[0] for p in points), min(p[1] for p in points)
            for p, g in zip(points, grid):
                assert math.dist(p, (x0 + g[0] * delta, y0 + g[1] * delta)) <= delta / math.sqrt(2) + 1e-12
            moved = [(x0 + g[0] * delta, y0 + g[1] * delta) for g in grid]
            for _ in range(5):
                order = list(range(n))
                rng.shuffle(order)
                assert abs(length(points, order) - length(moved, order)) <= math.sqrt(2) * n * delta + 1e-9


def test_line_levels_have_the_right_chances() -> None:
    L = 16
    depth = int(math.log2(2 * L))
    for k in range(L - 1):
        levels = [line_level(k, a, L) for a in range(L)]
        assert all(1 <= v <= depth for v in levels)
        for i in range(1, depth + 1):
            assert sum(v <= i for v in levels) == min(L, 2 ** (i - 1))  # P[level <= i] = 2^(i-1) / L


def test_portal_lemma_exactly_over_all_shifts() -> None:
    rng = random.Random(1998)
    cases = [(SEVEN, OPT_SEVEN, 1.0)]
    for n in (4, 5, 6):
        points = [(rng.random(), rng.random()) for _ in range(n)]
        cases.append((points, brute_order(points), 0.5))
    for points, order, c in cases:
        grid, _, L = snap(points, c)
        m = portal_count(L, c)
        pts = [grid[i] for i in order]
        mean = sum(detour(pts, a, b, L, m) for a in range(L) for b in range(L)) / L**2
        bound = math.log2(2 * L) / m * crossings(pts)
        assert mean <= bound + 1e-9
        assert crossings(pts) <= math.sqrt(2) * length(pts, range(len(pts))) + 1e-9
        assert mean <= length(pts, range(len(pts))) / (2 * c) + 1e-9  # the 1/(2c) share of the error budget


def test_more_portals_never_cost_more() -> None:
    grid, _, L = snap(SEVEN, 1.0)
    pts = [grid[i] for i in OPT_SEVEN]
    values = [detour(pts, 5, 9, L, m) for m in (4, 8, 16, 32, 64)]
    assert all(x >= y - 1e-9 for x, y in zip(values, values[1:]))


def test_quadtree_leaves() -> None:
    grid, _, L = snap(SEVEN, 1.0)
    for a, b in ((0, 0), (17, 40), (63, 63)):
        count, deepest = quadtree(grid, a, b, L)
        assert len(set(grid)) <= count and deepest <= math.log2(2 * L)
    assert quadtree(grid, 0, 0, L) == (12, 4)


def test_example() -> None:
    grid, delta, L = snap(SEVEN, 1.0)
    assert (L, portal_count(L, 1.0)) == (64, 32)
    assert grid[:2] == [(9, 19), (0, 47)]
    order, _, _ = arora_tour(SEVEN, 1.0, shift=(0, 0))
    assert order == [0, 2, 5, 6, 1, 4, 3]  # A C F G B E D: not OPT, but within the bound
    assert length(SEVEN, order) <= 2 * length(SEVEN, OPT_SEVEN)
    assert abs(length(SEVEN, order) / length(SEVEN, OPT_SEVEN) - 1.015) < 1e-3


def test_scheme_against_brute_force() -> None:
    rng = random.Random(2010)
    for n in (4, 5, 6):
        points = [(rng.random(), rng.random()) for _ in range(n)]
        opt = brute_order(points)
        for c in (1.0, 2.0):
            grid, _, L = snap(points, c)
            for _ in range(2):
                order, (a, b), m = arora_tour(points, c, rng)
                assert sorted(order) == list(range(n))
                mine = [grid[i] for i in order]
                best = [grid[i] for i in opt]
                # The order minimizes length plus detour, so it beats the optimal order on that sum.
                lhs = length(mine, range(n)) + detour(mine, a, b, L, m)
                assert lhs <= length(best, range(n)) + detour(best, a, b, L, m) + 1e-9
                assert length(points, order) <= (1 + 1 / c) * length(points, opt) + 1e-9  # measured per shift


def test_small_inputs() -> None:
    assert arora_tour([(0.0, 0.0)])[0] == [0]
    assert arora_tour([(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)])[0] == [0, 1, 2]
    assert snap([(1.0, 1.0), (1.0, 1.0)], 1.0) == ([(0, 0), (0, 0)], 1.0, 1)
