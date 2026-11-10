# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/space-filling-curve-tsp/. The authors are listed in prov/CF8E6R.jsonl.

import itertools
import math
import random

from space_filling_curve_tsp import euclidean_tour_length, grid_cell, hilbert_index, space_filling_curve_tour

# The six cities A to F of the page, on an 8 x 8 grid.
POINTS = [(0, 0), (2, 0), (5, 1), (4, 4), (1, 3), (6, 3)]


def brute_force_opt(points):
    n = len(points)
    if n <= 1:
        return 0.0
    return min(euclidean_tour_length(points, [0, *p]) for p in itertools.permutations(range(1, n)))


def test_hilbert_curve_is_a_curve() -> None:
    for order in range(1, 6):
        size = 1 << order
        cell = {}
        for x in range(size):
            for y in range(size):
                cell[hilbert_index(order, x, y)] = (x, y)
        assert sorted(cell) == list(range(size * size))
        assert cell[0] == (0, 0) and cell[size * size - 1] == (size - 1, 0)
        for i in range(size * size - 1):
            (x1, y1), (x2, y2) = cell[i], cell[i + 1]
            assert abs(x1 - x2) + abs(y1 - y2) == 1


def test_each_coarse_cell_is_one_interval() -> None:
    """The cells of one level-k square have consecutive positions on the curve."""
    order = 5
    size = 1 << order
    for k in range(order + 1):
        shift = order - k
        block = {}
        for x in range(size):
            for y in range(size):
                block.setdefault((x >> shift, y >> shift), []).append(hilbert_index(order, x, y))
        for positions in block.values():
            assert max(positions) - min(positions) == len(positions) - 1


def test_example() -> None:
    assert [hilbert_index(3, x, y) for x, y in POINTS] == [0, 4, 56, 32, 12, 51]
    tour = space_filling_curve_tour(POINTS, 3, (0, 0, 8))
    assert "".join("ABCDEF"[i] for i in tour) == "ABEDFC"
    assert abs(euclidean_tour_length(POINTS, tour) - 17.8957) < 1e-3
    assert abs(brute_force_opt(POINTS) - 15.9590) < 1e-3


def test_edges() -> None:
    assert space_filling_curve_tour([]) == []
    assert space_filling_curve_tour([(3.0, 4.0)]) == [0]
    assert space_filling_curve_tour([(1.0, 1.0), (1.0, 1.0)]) == [0, 1]
    assert grid_cell([(0.0, 0.0), (1.0, 1.0)], 2) == [(0, 0), (3, 3)]


def test_log_bound_against_brute_force() -> None:
    rng = random.Random(1989)
    for n in range(2, 9):
        for _ in range(10):
            points = [(rng.random(), rng.random()) for _ in range(n)]
            tour = space_filling_curve_tour(points)
            assert sorted(tour) == list(range(n))
            alg = euclidean_tour_length(points, tour)
            opt = brute_force_opt(points)
            assert opt - 1e-9 <= alg <= (9 * math.sqrt(2) * math.ceil(math.log2(n)) + math.sqrt(2)) * opt


def test_level_counts_of_the_proof() -> None:
    """Tour edges whose ends split at level k are at most m_(k+1) - 1, and short."""
    rng = random.Random(36)
    order = 12
    size = 1 << order
    for n in (20, 200):
        points = [(rng.random(), rng.random()) for _ in range(n)]
        cells = grid_cell(points, order)
        tour = space_filling_curve_tour(points, order)
        xs, ys = [p[0] for p in points], [p[1] for p in points]
        side = max(max(xs) - min(xs), max(ys) - min(ys))
        for k in range(order):
            shift = order - k - 1
            occupied = {(cx >> shift, cy >> shift) for cx, cy in cells}
            split = 0
            for i in range(n - 1):
                a, b = cells[tour[i]], cells[tour[i + 1]]
                if (a[0] >> shift, a[1] >> shift) != (b[0] >> shift, b[1] >> shift):
                    if (a[0] >> (shift + 1), a[1] >> (shift + 1)) == (b[0] >> (shift + 1), b[1] >> (shift + 1)):
                        split += 1
                        gap = math.dist(points[tour[i]], points[tour[i + 1]])
                        assert gap <= math.sqrt(2) * side / 2**k * (1 + 1 / size) + 1e-12
            assert split <= len(occupied) - 1


def row_family(order):
    """The 2^order cell centers of one grid row, in the frame [0, 1] x [0, 1]."""
    size = 1 << order
    row = (2 * size) // 3
    return [((x + 0.5) / size, (row + 0.5) / size) for x in range(size)]


def test_row_family_ratio_grows() -> None:
    ratios = []
    for order in range(2, 11):
        points = row_family(order)
        tour = space_filling_curve_tour(points, order, (0.0, 0.0, 1.0))
        alg = euclidean_tour_length(points, tour)
        opt = 2 * (points[-1][0] - points[0][0])  # points on a line: OPT is two times the span
        ratios.append(alg / opt)
    assert all(b > a for a, b in zip(ratios[2:], ratios[3:]))
    assert ratios[-1] > 2.8
