# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/correlative-scan-matching/. The authors are listed in prov/1ZMBCJ.jsonl.

import math
import random

import pytest

from correlative_scan_matching import (
    brute_force,
    build_tables,
    correlative_scan_match,
    covariance,
    lookup_table,
    pose_of,
    rotated_cells,
    score,
    window_max_table,
)

R = 0.05  # cell size, m
SIGMA = 0.05  # kernel width, m
D = 4  # cells per block side of the low resolution level
W = 8  # the shifts are -W to W cells, so +-0.4 m
THETAS = [k * 0.02 for k in range(-6, 7)]  # +-0.12 rad


def room():
    """The walls of a 4 m by 3 m room with a 1 m by 0.5 m box, every 5 cm."""
    pts = []
    for k in range(81):
        pts += [(k * 0.05, 0.0), (k * 0.05, 3.0)]
    for k in range(1, 60):
        pts += [(0.0, k * 0.05), (4.0, k * 0.05)]
    for k in range(21):
        pts += [(2.5 + k * 0.05, 1.0), (2.5 + k * 0.05, 1.5)]
    for k in range(1, 10):
        pts += [(2.5, 1.0 + k * 0.05), (3.5, 1.0 + k * 0.05)]
    return pts


def scan_from(pose, pts, rng, noise, keep):
    """The points pts seen from pose, in the frame of the robot, with noise."""
    x, y, th = pose
    c, s = math.cos(th), math.sin(th)
    out = []
    for px, py in pts:
        if rng.random() < keep:
            dx, dy = px - x, py - y
            out.append((c * dx + s * dy + rng.gauss(0.0, noise), -s * dx + c * dy + rng.gauss(0.0, noise)))
    return out


@pytest.fixture(scope="module")
def tables():
    return build_tables(room(), R, SIGMA, 0.6, D)


def test_window_max_bounds_every_cell(tables):
    t, low = tables
    for i in range(-D, t.nx + 2, 3):
        for j in range(-D, t.ny + 2, 3):
            want = max(t.get(i + a, j + b) for a in range(D) for b in range(D))
            assert low.get(i, j) == want


def test_branch_and_bound_finds_the_best_score():
    rng = random.Random(3)
    t, low = build_tables(room(), R, SIGMA, 0.6, D)
    for _ in range(4):
        truth = (1.2 + rng.uniform(-0.3, 0.3), 1.5 + rng.uniform(-0.3, 0.3), rng.uniform(-0.1, 0.1))
        scan = scan_from(truth, room(), rng, 0.02, 0.25)
        x0, y0 = 1.2, 1.5  # the prior guess
        best, pose, count = correlative_scan_match(t, low, D, scan, x0, y0, THETAS, W)
        bf_best, bf_pose, bf_count = brute_force(t, scan, x0, y0, THETAS, W)
        assert best == bf_best
        assert score(t, rotated_cells(t, scan, pose[0], x0, y0), pose[1], pose[2]) == best
        assert count < bf_count / 3
        x, y, th = pose_of(t, x0, y0, pose)
        assert math.hypot(x - truth[0], y - truth[1]) < 0.06 and abs(th - truth[2]) < 0.03


def test_exact_pose_on_the_grid_is_found():
    rng = random.Random(8)
    t, low = build_tables(room(), R, SIGMA, 0.6, D)
    truth = (1.0 + 3 * R, 1.6 - 5 * R, THETAS[9])
    scan = scan_from(truth, room(), rng, 0.0, 0.3)
    best, pose, _ = correlative_scan_match(t, low, D, scan, 1.0, 1.6, THETAS, W)
    assert pose == (THETAS[9], 3, -5)
    # every point lies on a reference point up to rounding to the grid
    assert best >= 60 * len(scan)


def test_corridor_is_uncertain_along_its_axis():
    # two long parallel walls: a shift along the walls barely changes the score
    ref = [(k * 0.05, 0.0) for k in range(-40, 120)] + [(k * 0.05, 1.0) for k in range(-40, 120)]
    rng = random.Random(1)
    truth = (2.0, 0.5, 0.0)
    pts = [(k * 0.05, 0.0) for k in range(20, 60)] + [(k * 0.05, 1.0) for k in range(20, 60)]
    scan = scan_from(truth, pts, rng, 0.0, 1.0)
    t = lookup_table(ref, R, SIGMA, 0.6)
    mean, cov = covariance(t, scan, 2.0, 0.5, [-0.04, -0.02, 0.0, 0.02, 0.04], 6, 0.05)
    assert cov[0][0] > 20.0 * cov[1][1]
    assert abs(mean[1] - 0.5) < 0.01 and abs(mean[2]) < 0.01


def test_room_covariance_is_small_and_symmetric(tables):
    t, _ = tables
    rng = random.Random(2)
    scan = scan_from((1.5, 1.5, 0.0), room(), rng, 0.0, 0.3)
    mean, cov = covariance(t, scan, 1.5, 1.5, THETAS, 4, 0.05)
    assert all(abs(cov[a][b] - cov[b][a]) < 1e-15 for a in range(3) for b in range(3))
    assert math.hypot(mean[0] - 1.5, mean[1] - 1.5) < 0.01
    assert cov[0][0] < 1e-3 and cov[1][1] < 1e-3


def test_errors():
    with pytest.raises(ValueError):
        lookup_table([], R, SIGMA, 0.5)
    with pytest.raises(ValueError):
        lookup_table([(0.0, 0.0)], 0.0, SIGMA, 0.5)
    t = lookup_table([(0.0, 0.0)], R, SIGMA, 0.5)
    assert t.get(t.cell(0.0, 0.0)[0], t.cell(0.0, 0.0)[1]) == 100
    assert t.get(-100, -100) == 0
    low = window_max_table(t, 1)
    assert all(low.get(i, j) == t.get(i, j) for i in range(t.nx) for j in range(t.ny))
