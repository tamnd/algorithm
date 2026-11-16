# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cortes-coverage-algorithm/. The authors are listed in prov/CV7WDC.jsonl.

import math
import random

from cortes_coverage_algorithm import (
    cell_data,
    centroid_gap,
    coverage_cost,
    coverage_step,
    moments,
    run,
    voronoi_cell,
)

SQUARE = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
PENTAGON = [(0.0, 0.0), (2.0, 0.0), (2.5, 1.2), (1.0, 2.0), (-0.4, 1.1)]


def grid_cost(pts, n=200):
    """Midpoint rule for the cost on the unit square."""
    h = 1.0 / n
    tot = 0.0
    for a in range(n):
        x = (a + 0.5) * h
        for b in range(n):
            y = (b + 0.5) * h
            tot += min((x - p[0]) ** 2 + (y - p[1]) ** 2 for p in pts)
    return tot * h * h


def test_moments_of_simple_shapes() -> None:
    m, cx, cy, j = moments(SQUARE)
    assert (m, cx, cy) == (1.0, 0.5, 0.5)
    assert abs(j - 2 / 3) < 1e-15
    m, cx, cy, _ = moments([(0.0, 0.0), (3.0, 0.0), (0.0, 3.0)])
    assert abs(m - 4.5) < 1e-12 and abs(cx - 1) < 1e-12 and abs(cy - 1) < 1e-12


def test_cells_partition_the_region() -> None:
    rng = random.Random(1)
    region_area = moments(PENTAGON)[0]
    for _ in range(30):
        pts = [(rng.uniform(-0.4, 2.5), rng.uniform(0, 2)) for _ in range(rng.randrange(1, 9))]
        cells = [voronoi_cell(i, pts, PENTAGON) for i in range(len(pts))]
        assert abs(sum(moments(c)[0] for c in cells) - region_area) < 1e-9
        for c, p in zip(cells, pts):
            for v in c:
                d = math.dist(v, p)
                assert all(math.dist(v, q) >= d - 1e-9 for q in pts)


STRIP = [(0.0, 0.0), (1.0, 0.0), (1.0, 0.1), (0.0, 0.1)]


def test_one_dimensional_example() -> None:
    pts = [(0.1, 0.05), (0.2, 0.05), (0.9, 0.05)]
    data = cell_data(pts, STRIP)
    assert [round(m, 12) for m, _, _ in data] == [0.015, 0.04, 0.045]
    assert [round(c[0], 12) for _, c, _ in data] == [0.075, 0.35, 0.775]
    two = coverage_step(coverage_step(pts, STRIP), STRIP)
    assert [round(p[0], 12) for p in two] == [0.10625, 0.3875, 0.78125]
    out = run(pts, STRIP, 1.0, 300)
    for p, x in zip(out, [1 / 6, 1 / 2, 5 / 6]):
        assert abs(p[0] - x) < 1e-9 and abs(p[1] - 0.05) < 1e-12


def test_line_in_square_is_a_saddle() -> None:
    line = [(1 / 6, 0.5), (0.5, 0.5), (5 / 6, 0.5)]
    assert centroid_gap(line, SQUARE) < 1e-14
    assert abs(coverage_cost(line, SQUARE) - 5 / 54) < 1e-14
    out = run([(1 / 6, 0.5), (0.5, 0.5 - 1e-6), (5 / 6, 0.5)], SQUARE, 1.0, 200)
    assert centroid_gap(out, SQUARE) < 1e-9
    assert coverage_cost(out, SQUARE) < 0.067


def test_cost_against_known_values_and_grid() -> None:
    assert abs(coverage_cost([(0.5, 0.5)], SQUARE) - 1 / 6) < 1e-14
    assert abs(coverage_cost([(0.25, 0.5), (0.75, 0.5)], SQUARE) - 5 / 48) < 1e-14
    assert abs(coverage_cost([(1 / 3, 2 / 3), (2 / 3, 1 / 3)], SQUARE) - 1 / 9) < 1e-14
    rng = random.Random(2)
    pts = [(rng.random(), rng.random()) for _ in range(4)]
    assert abs(coverage_cost(pts, SQUARE) - grid_cost(pts)) < 1e-4


def test_cost_never_increases_and_decrease_bound() -> None:
    rng = random.Random(3)
    for k in (0.3, 0.7, 1.0):
        pts = [(rng.uniform(0, 2), rng.uniform(0, 1.5)) for _ in range(6)]
        for _ in range(25):
            data = cell_data(pts, PENTAGON)
            before = sum(c for _, _, c in data)
            gap = sum(m * math.dist(p, c) ** 2 for p, (m, c, _) in zip(pts, data))
            pts = coverage_step(pts, PENTAGON, k)
            after = coverage_cost(pts, PENTAGON)
            assert after <= before - k * (2 - k) * gap + 1e-12


def test_robots_stay_inside_and_distinct() -> None:
    rng = random.Random(4)
    pts = [(rng.uniform(0, 2), rng.uniform(0, 1.5)) for _ in range(7)]
    for _ in range(30):
        pts = coverage_step(pts, PENTAGON, 0.5)
        for p in pts:
            assert moments(voronoi_cell(0, [p], PENTAGON))[0] > 0
        assert min(math.dist(a, b) for i, a in enumerate(pts) for b in pts[i + 1:]) > 1e-6


def test_converges_to_centroidal_configuration() -> None:
    rng = random.Random(5)
    pts = [(rng.random(), rng.random()) for _ in range(5)]
    out = run(pts, SQUARE, 1.0, 400)
    assert centroid_gap(out, SQUARE) < 1e-6


def test_diagonal_critical_point_is_fixed_but_not_optimal() -> None:
    diag = [(1 / 3, 2 / 3), (2 / 3, 1 / 3)]
    assert centroid_gap(diag, SQUARE) < 1e-14
    halves = [(0.25, 0.5), (0.75, 0.5)]
    assert centroid_gap(halves, SQUARE) < 1e-14
    assert coverage_cost(halves, SQUARE) < coverage_cost(diag, SQUARE)
    assert run(diag, SQUARE, 1.0, 50) == diag
    out = run([(1 / 3 + 1e-6, 2 / 3), (2 / 3, 1 / 3)], SQUARE, 1.0, 200)
    assert abs(coverage_cost(out, SQUARE) - 5 / 48) < 1e-12
    assert centroid_gap(out, SQUARE) < 1e-9
