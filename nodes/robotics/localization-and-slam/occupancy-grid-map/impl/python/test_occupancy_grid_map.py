# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/occupancy-grid-map/. The authors are listed in prov/MJFAZ4.jsonl.

import math
import random

import pytest

import robest
from occupancy_grid_map import OccupancyGridMap

L_OCC = robest.logodds(0.7)
L_FREE = robest.logodds(0.4)


def open_cell_meets_segment(g, i, j, a, b):
    """Brute force: does the open square of cell (i, j) meet the segment ab?"""
    lo, hi = 0.0, 1.0
    for k, (c0, c1) in enumerate(
        [(g.ox + i * g.res, g.ox + (i + 1) * g.res), (g.oy + j * g.res, g.oy + (j + 1) * g.res)]
    ):
        p, d = a[k], b[k] - a[k]
        if d == 0:
            if not c0 < p < c1:
                return False
            continue
        t0, t1 = sorted(((c0 - p) / d, (c1 - p) / d))
        lo, hi = max(lo, t0), min(hi, t1)
    return lo < hi


def test_index_and_center():
    g = OccupancyGridMap(-1.0, 2.0, 0.25, 8, 4)
    assert g.index(-1.0, 2.0) == (0, 0)
    assert g.index(-0.76, 2.24) == (0, 0)
    assert g.index(-0.75, 2.25) == (1, 1)  # cells are half-open
    assert g.index(0.99, 2.99) == (7, 3)
    assert g.index(1.0, 2.5) is None
    assert g.index(-1.01, 2.5) is None
    for i in range(8):
        for j in range(4):
            assert g.index(*g.center(i, j)) == (i, j)


def test_prior_and_check_values():
    g = OccupancyGridMap(0.0, 0.0, 1.0, 3, 3)
    assert g.l0 == 0.0 and g.probability(1, 1) == 0.5
    g.update(1, 1, L_OCC)
    assert g.log_odds(1, 1) == pytest.approx(0.84730, abs=1e-5)
    assert g.probability(1, 1) == pytest.approx(0.7, abs=1e-12)
    g.update(2, 0, robest.logodds(0.6))
    assert g.log_odds(2, 0) == pytest.approx(0.40547, abs=1e-5)
    assert g.log_odds(0, 2) == 0.0


def test_updates_without_clamping_equal_the_closed_form_sum():
    rng = random.Random(11)
    g = OccupancyGridMap(0.0, 0.0, 0.5, 6, 5, p_prior=0.3)
    total = [[g.l0] * 5 for _ in range(6)]
    for _ in range(400):
        i, j = rng.randrange(6), rng.randrange(5)
        v = rng.choice([L_OCC, L_FREE, robest.logodds(rng.uniform(0.05, 0.95))])
        g.update(i, j, v)
        total[i][j] += v - g.l0
    for i in range(6):
        for j in range(5):
            assert g.log_odds(i, j) == pytest.approx(total[i][j], abs=1e-9)


def test_clamping_keeps_bounds_and_makes_the_order_matter():
    def run(seq):
        g = OccupancyGridMap(0.0, 0.0, 1.0, 1, 1, p_min=0.12, p_max=0.97)
        for v in seq:
            g.update(0, 0, v)
            assert g.l_min <= g.log_odds(0, 0) <= g.l_max
        return g.log_odds(0, 0)

    g = OccupancyGridMap(0.0, 0.0, 1.0, 1, 1, p_min=0.12, p_max=0.97)
    assert g.l_max == pytest.approx(3.476, abs=1e-3)
    assert g.l_min == pytest.approx(-1.992, abs=1e-3)
    a = run([L_OCC] * 5 + [L_FREE])
    b = run([L_FREE] + [L_OCC] * 5)
    assert a == pytest.approx(g.l_max + L_FREE, abs=1e-12)
    assert b == pytest.approx(g.l_max, abs=1e-12)
    assert run([L_FREE] * 20) == pytest.approx(g.l_min, abs=1e-12)


def test_random_operations_against_a_dict_model():
    rng = random.Random(23)
    for _ in range(5):
        w, h = rng.randint(1, 7), rng.randint(1, 7)
        g = OccupancyGridMap(rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(0.1, 1.0), w, h,
                             p_prior=0.4, p_min=0.1, p_max=0.95)
        model = {}
        lo, hi = robest.logodds(0.1), robest.logodds(0.95)
        for _ in range(500):
            i, j = rng.randrange(w), rng.randrange(h)
            if rng.random() < 0.7:
                v = rng.choice([L_OCC, L_FREE, rng.uniform(-3.0, 3.0)])
                g.update(i, j, v)
                model[(i, j)] = min(hi, max(lo, model.get((i, j), g.l0) + v - g.l0))
            got = g.probability(i, j)
            want = 1.0 / (1.0 + math.exp(-model.get((i, j), g.l0)))
            assert got == pytest.approx(want, abs=1e-12)
            g.check_invariant()
        for i in range(w):
            for j in range(h):
                assert g.log_odds(i, j) == pytest.approx(model.get((i, j), g.l0), abs=1e-12)


def test_prior_outside_the_clamping_bounds_is_rejected():
    with pytest.raises(ValueError):
        OccupancyGridMap(0.0, 0.0, 1.0, 2, 2, p_prior=0.05, p_min=0.12, p_max=0.97)


def test_cells_on_segment_against_brute_force():
    rng = random.Random(5)
    g = OccupancyGridMap(-0.3, 0.7, 0.2, 10, 10)
    for _ in range(300):
        a = (rng.uniform(-2.0, 2.0), rng.uniform(-1.0, 3.0))
        b = (rng.uniform(-2.0, 2.0), rng.uniform(-1.0, 3.0))
        cells = g.cells_on_segment(a, b)
        assert cells[0] == g.cell_of(*a)
        assert cells[-1] == g.cell_of(*b)
        for (i0, j0), (i1, j1) in zip(cells, cells[1:]):
            assert abs(i1 - i0) + abs(j1 - j0) == 1
        assert len(set(cells)) == len(cells)
        ia, ja = g.cell_of(*a)
        ib, jb = g.cell_of(*b)
        want = {
            (i, j)
            for i in range(min(ia, ib), max(ia, ib) + 1)
            for j in range(min(ja, jb), max(ja, jb) + 1)
            if open_cell_meets_segment(g, i, j, a, b)
        }
        assert set(cells) == want


def test_cells_on_axis_parallel_segments():
    g = OccupancyGridMap(0.0, 0.0, 1.0, 10, 10)
    assert g.cells_on_segment((0.5, 2.5), (4.5, 2.5)) == [(i, 2) for i in range(5)]
    assert g.cells_on_segment((3.5, 4.5), (3.5, 1.5)) == [(3, j) for j in range(4, 0, -1)]
    assert g.cells_on_segment((2.2, 2.7), (2.8, 2.1)) == [(2, 2)]


def test_page_example():
    g = OccupancyGridMap(0.0, 0.0, 1.0, 5, 3)
    a = (0.5, 0.5)
    assert g.cells_on_segment(a, (3.7, 2.4)) == [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2)]
    for b in [(3.7, 2.4), (4.5, 0.5), (3.7, 2.4)]:
        g.insert_ray(a, b, hit=True)
        g.check_invariant()
    want = {
        (3, 2): 2 * L_OCC,
        (1, 1): 2 * L_FREE, (2, 1): 2 * L_FREE, (3, 1): 2 * L_FREE,
        (0, 0): 3 * L_FREE, (1, 0): 3 * L_FREE, (2, 0): L_FREE, (3, 0): L_FREE, (4, 0): L_OCC,
    }
    for i in range(5):
        for j in range(3):
            assert g.log_odds(i, j) == pytest.approx(want.get((i, j), 0.0), abs=1e-12)
    assert g.probability(3, 2) == pytest.approx(0.49 / 0.58, abs=1e-12)
    assert g.probability(0, 0) == pytest.approx(8 / 35, abs=1e-12)


def test_insert_ray_hit_and_max_range():
    g = OccupancyGridMap(0.0, 0.0, 1.0, 10, 3)
    g.insert_ray((0.5, 1.5), (4.5, 1.5), hit=True)
    assert [g.log_odds(i, 1) for i in range(6)] == [L_FREE] * 4 + [L_OCC, 0.0]
    g.insert_ray((0.5, 0.5), (4.5, 0.5), hit=False)
    assert [g.log_odds(i, 0) for i in range(6)] == [L_FREE] * 5 + [0.0]
    assert all(g.log_odds(i, 2) == 0.0 for i in range(10))


def test_insert_ray_skips_cells_outside_the_grid():
    g = OccupancyGridMap(0.0, 0.0, 1.0, 4, 4)
    g.insert_ray((2.5, 2.5), (7.5, 2.5), hit=True)
    assert [g.log_odds(i, 2) for i in range(4)] == [0.0, 0.0, L_FREE, L_FREE]
    g.insert_ray((-3.5, 0.5), (1.5, 0.5), hit=True)
    assert [g.log_odds(i, 0) for i in range(4)] == [L_FREE, L_OCC, 0.0, 0.0]


def test_storage_is_row_major():
    g = OccupancyGridMap(0.0, 0.0, 1.0, 5, 3)
    g.update(4, 1, L_OCC)
    assert g.l[1 * 5 + 4] == L_OCC
    assert sum(1 for v in g.l if v != 0.0) == 1
    assert len(g.l) == 15


def test_invalid_grid():
    with pytest.raises(ValueError):
        OccupancyGridMap(0.0, 0.0, 0.0, 5, 5)
    with pytest.raises(ValueError):
        OccupancyGridMap(0.0, 0.0, 1.0, 0, 5)
