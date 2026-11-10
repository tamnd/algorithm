# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karp-partitioning-tsp/. The authors are listed in prov/56Q4XY.jsonl.

import itertools
import math
import random

import pytest

from karp_partitioning_tsp import (
    bounding_square,
    cell_tours_length,
    grid_cells,
    held_karp_tour,
    karp_partition_tour,
    snake_order,
    tour_length,
)

POINTS = [(0, 0), (2, 0), (5, 1), (4, 4), (1, 3), (6, 3)]  # A to F of the page


def brute_force(points):
    n = len(points)
    if n <= 1:
        return 0.0
    return min(tour_length(points, [0, *p]) for p in itertools.permutations(range(1, n)))


def clipped_length(a, b, x0, y0, x1, y1):
    """The length of the part of segment ab inside the closed rectangle (Liang-Barsky clipping)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    lo, hi = 0.0, 1.0
    for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
        if p == 0:
            if q < 0:
                return 0.0
        elif p < 0:
            lo = max(lo, q / p)
        else:
            hi = min(hi, q / p)
    return max(0.0, hi - lo) * math.hypot(dx, dy)


def seeded(n, seed):
    rng = random.Random(seed)
    return [(rng.random(), rng.random()) for _ in range(n)]


def test_held_karp_is_optimal() -> None:
    for n in range(1, 9):
        for seed in range(8):
            points = seeded(n, 100 * n + seed)
            tour = held_karp_tour(points, list(range(n)))
            assert sorted(tour) == list(range(n))
            assert abs(tour_length(points, tour) - brute_force(points)) < 1e-9


def test_example() -> None:
    cells = grid_cells(POINTS, 2)
    assert cells == {(0, 0): [0, 1], (1, 0): [2], (1, 1): [3, 5], (0, 1): [4]}
    assert snake_order(cells, 2) == [(0, 0), (1, 0), (1, 1), (0, 1)]
    tour = karp_partition_tour(POINTS, 2)
    assert "".join("ABCDEF"[i] for i in tour) == "ABCFDE"
    assert abs(tour_length(POINTS, tour) - brute_force(POINTS)) < 1e-9


def test_one_cell_is_exact() -> None:
    for n in range(2, 9):
        points = seeded(n, n)
        assert abs(tour_length(points, karp_partition_tour(points, 1)) - brute_force(points)) < 1e-9


def test_additive_bound_against_brute_force() -> None:
    for n in range(2, 9):
        for k in (1, 2, 3, 4):
            for seed in range(5):
                points = seeded(n, 1000 * k + 10 * n + seed)
                tour = karp_partition_tour(points, k)
                assert sorted(tour) == list(range(n))
                alg, opt = tour_length(points, tour), brute_force(points)
                side = bounding_square(points)[2]
                m = len(grid_cells(points, k))
                cells = cell_tours_length(points, k)
                # Lemma: the cell tours cost at most OPT + (3/2) times the perimeters of the nonempty cells.
                assert cells <= opt + 1.5 * m * 4 * side / k + 1e-9
                # Join: the snake through the cells costs at most (sqrt 2 + 1) k L + sqrt 2 L.
                assert alg <= cells + (math.sqrt(2) + 1) * k * side + math.sqrt(2) * side + 1e-9
                assert opt - 1e-9 <= alg <= opt + ((7 + math.sqrt(2)) * k + math.sqrt(2)) * side + 1e-9


def test_cell_lemma_with_clipped_optimal_tour() -> None:
    for n in range(3, 9):
        for k in (2, 3):
            points = seeded(n, 77 * n + k)
            opt_tour = held_karp_tour(points, list(range(n)))
            edges = [(points[opt_tour[i]], points[opt_tour[(i + 1) % n]]) for i in range(n)]
            x0, y0, side = bounding_square(points)
            a = side / k
            total = 0.0
            for (col, row), ids in grid_cells(points, k).items():
                box = (x0 + col * a, y0 + row * a, x0 + (col + 1) * a, y0 + (row + 1) * a)
                inside = sum(clipped_length(p, q, *box) for p, q in edges)
                local = tour_length(points, held_karp_tour(points, ids))
                assert local <= inside + 1.5 * 4 * a + 1e-9
            for col in range(k):
                for row in range(k):
                    box = (x0 + col * a, y0 + row * a, x0 + (col + 1) * a, y0 + (row + 1) * a)
                    total += sum(clipped_length(p, q, *box) for p, q in edges)
            assert abs(total - tour_length(points, opt_tour)) < 1e-9


def test_large_random_instance() -> None:
    n = 1000
    points = seeded(n, 1977)
    tour = karp_partition_tour(points, 18, 15)
    assert sorted(tour) == list(range(n))
    # Measured, not a bound: about 1.04 sqrt(n) here, against about 0.7124 sqrt(n) for OPT as n grows.
    assert 0.7 * math.sqrt(n) < tour_length(points, tour) < 1.2 * math.sqrt(n)


def test_large_cell_is_refused() -> None:
    with pytest.raises(ValueError):
        karp_partition_tour(seeded(20, 3), 1, 12)
    assert karp_partition_tour([], 3) == []
    assert karp_partition_tour([(1.0, 1.0)] * 3, 2) == [0, 1, 2]
