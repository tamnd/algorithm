# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/occupancy-grid-mapping/. The authors are listed in prov/NBXJ4P.jsonl.

import math
import random

import pytest

import robest
from occupancy_grid_mapping import (
    Grid,
    InverseRangeSensorModel,
    new_map,
    occupancy_grid_mapping,
    probabilities,
)

# A rectangular room with walls on x = 0, x = 4, y = 0 and y = 3. The grid
# puts cell centers at -0.5, -0.4, ..., so the walls run through the centers
# of the columns i = 5 and i = 45 and of the rows j = 5 and j = 35.
GRID = Grid(-0.55, -0.55, 0.1, 51, 41)
ROOM = (0.0, 4.0, 0.0, 3.0)
POSES = [(1.0, 1.0, 0.3), (2.0, 1.5, 0.0), (3.0, 2.0, 1.0)]
N_BEAMS = 120
BEARINGS = [-math.pi + 2.0 * math.pi * k / N_BEAMS for k in range(N_BEAMS)]


def room_range(pose, bearing, z_max):
    """Return the exact range to the room walls, capped at z_max."""
    x, y, theta = pose
    c, s = math.cos(theta + bearing), math.sin(theta + bearing)
    x0, x1, y0, y1 = ROOM
    ts = []
    if c > 0:
        ts.append((x1 - x) / c)
    elif c < 0:
        ts.append((x0 - x) / c)
    if s > 0:
        ts.append((y1 - y) / s)
    elif s < 0:
        ts.append((y0 - y) / s)
    return min(min(ts), z_max)


def room_scan(pose, z_max):
    return [(room_range(pose, b, z_max), b) for b in BEARINGS]


def room_ism():
    # The beam width is a little more than the beam spacing, so every
    # direction is within beta / 2 of a beam.
    return InverseRangeSensorModel(z_max=6.0, alpha=0.2, beta=1.2 * 2.0 * math.pi / N_BEAMS)


@pytest.fixture(scope="module")
def room_map():
    ism = room_ism()
    l = new_map(GRID, ism)
    for pose in POSES:
        occupancy_grid_mapping(l, GRID, pose, room_scan(pose, ism.z_max), ism)
    return l


def test_logodds_check_values():
    ism = InverseRangeSensorModel(z_max=5.0, alpha=0.2, beta=0.05)
    assert ism.l_occ == pytest.approx(0.84730, abs=1e-5)
    assert ism.l_free == pytest.approx(-0.40547, abs=1e-5)
    assert ism.l0 == 0.0


def test_inverse_model_hand_cases():
    ism = InverseRangeSensorModel(z_max=3.0, alpha=0.2, beta=0.1)
    pose = (0.0, 0.0, 0.0)
    scan = [(1.0, 0.0), (2.0, math.pi / 2)]
    assert ism((0.5, 0.0), pose, scan) == ism.l_free
    assert ism((1.0, 0.0), pose, scan) == ism.l_occ
    assert ism((1.05, 0.0), pose, scan) == ism.l_occ
    assert ism((0.95, 0.0), pose, scan) == ism.l_occ
    assert ism((1.2, 0.0), pose, scan) == ism.l0
    assert ism((0.5, 0.5), pose, scan) == ism.l0  # between the beams
    assert ism((0.0, 1.5), pose, scan) == ism.l_free
    assert ism((0.0, 2.0), pose, scan) == ism.l_occ
    assert ism((0.0, -1.0), pose, scan) == ism.l0  # no beam points there


def test_inverse_model_max_range_reading_marks_no_obstacle():
    ism = InverseRangeSensorModel(z_max=3.0, alpha=0.2, beta=0.1)
    pose = (0.0, 0.0, 0.0)
    scan = [(3.0, 0.0)]
    assert ism((2.95, 0.0), pose, scan) == ism.l_free
    assert ism((3.0, 0.0), pose, scan) == ism.l_free
    assert ism((3.05, 0.0), pose, scan) == ism.l0


def test_inverse_model_uses_the_robot_heading():
    ism = InverseRangeSensorModel(z_max=3.0, alpha=0.2, beta=0.1)
    scan = [(1.0, 0.0)]
    pose = (1.0, 1.0, math.pi / 2)
    assert ism((1.0, 2.0), pose, scan) == ism.l_occ
    assert ism((2.0, 1.0), pose, scan) == ism.l0
    # The bearing difference wraps around at pi.
    scan = [(1.0, math.pi - 0.01)]
    pose = (0.0, 0.0, 0.0)
    assert ism((-1.0, -0.01), pose, scan) == ism.l_occ


def test_update_equals_binary_bayes_filter_in_probability_form():
    # A prior other than 0.5 makes the "- l0" term matter.
    ism = InverseRangeSensorModel(z_max=3.0, alpha=0.2, beta=0.1, p_prior=0.3)
    grid = Grid(-1.0, -1.0, 0.25, 8, 8)
    rng = random.Random(7)
    l = new_map(grid, ism)
    p0 = 0.3
    bel = [[p0] * grid.height for _ in range(grid.width)]
    for _ in range(12):
        pose = (rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5), rng.uniform(-math.pi, math.pi))
        scan = [(rng.uniform(0.2, 3.0), -math.pi + 2 * math.pi * k / 72) for k in range(72)]
        for i in range(grid.width):
            for j in range(grid.height):
                p = robest.prob_from_logodds(ism(grid.center(i, j), pose, scan))
                a = p * bel[i][j] / p0
                b = (1 - p) * (1 - bel[i][j]) / (1 - p0)
                bel[i][j] = a / (a + b)
        occupancy_grid_mapping(l, grid, pose, scan, ism)
    got = probabilities(l)
    for i in range(grid.width):
        for j in range(grid.height):
            assert got[i][j] == pytest.approx(bel[i][j], abs=1e-12)


def test_reach_restriction_equals_the_full_loop():
    ism = InverseRangeSensorModel(z_max=1.0, alpha=0.2, beta=0.08)
    grid = Grid(0.0, 0.0, 0.1, 30, 20)
    pose = (1.0, 1.0, 0.4)
    rng = random.Random(3)
    scan = [(rng.uniform(0.3, 1.0), -math.pi + 2 * math.pi * k / 90) for k in range(90)]
    fast = occupancy_grid_mapping(new_map(grid, ism), grid, pose, scan, ism)
    full = new_map(grid, ism)
    for i in range(grid.width):
        for j in range(grid.height):
            full[i][j] += ism(grid.center(i, j), pose, scan) - ism.l0
    assert fast == full
    assert any(v != ism.l0 for col in fast for v in col)


def test_order_of_scans_does_not_matter():
    ism = room_ism()
    grid = Grid(-0.55, -0.55, 0.2, 26, 21)
    scans = [(pose, room_scan(pose, ism.z_max)) for pose in POSES]
    a = new_map(grid, ism)
    for pose, scan in scans:
        occupancy_grid_mapping(a, grid, pose, scan, ism)
    b = new_map(grid, ism)
    for pose, scan in reversed(scans):
        occupancy_grid_mapping(b, grid, pose, scan, ism)
    for ca, cb in zip(a, b):
        for va, vb in zip(ca, cb):
            assert va == pytest.approx(vb, abs=1e-12)


def test_room_walls_are_occupied(room_map):
    for i in range(8, 43):  # the walls y = 0 and y = 3, away from the corners
        assert room_map[i][5] > 0.0
        assert room_map[i][35] > 0.0
    for j in range(8, 33):  # the walls x = 0 and x = 4
        assert room_map[5][j] > 0.0
        assert room_map[45][j] > 0.0


def test_room_interior_is_free(room_map):
    for i in range(8, 43):
        for j in range(8, 33):
            assert room_map[i][j] < 0.0


def test_cells_behind_the_walls_keep_the_prior(room_map):
    for i in range(GRID.width):
        for j in range(GRID.height):
            if i <= 3 or i >= 47 or j <= 3 or j >= 37:
                assert room_map[i][j] == 0.0


def test_probabilities_of_the_room_map(room_map):
    p = probabilities(room_map)
    assert p[0][0] == 0.5
    assert p[25][5] > 0.9
    # Three scans saw the cell (2.0, 1.5) as free: odds (0.4 / 0.6)^3 = 8 / 27.
    assert p[25][20] == pytest.approx(8 / 35, abs=1e-12)
