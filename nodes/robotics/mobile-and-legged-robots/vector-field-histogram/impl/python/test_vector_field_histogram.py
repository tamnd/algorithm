# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vector-field-histogram/. The authors are listed in prov/Z398RM.jsonl.

import math
import random

from vector_field_histogram import polar_histogram, run, smooth, speed, steer, valleys

A = math.sqrt(2.0) * 16 * 0.1  # a for b = 1, ws = 33, cells of 10 cm


def test_single_cells_land_in_their_sectors():
    x, y = 0.05, 0.05  # the center of cell (0, 0)
    for cell, sector, dist in (((10, 0), 0, 1.0), ((0, 10), 18, 1.0), ((-7, -7), 45, math.sqrt(98) * 0.1),
                               ((3, 1), 3, math.sqrt(10) * 0.1), ((-5, 2), 31, math.sqrt(29) * 0.1)):
        h = polar_histogram({cell: 2.0}, x, y)
        assert [k for k in range(72) if h[k] != 0.0] == [sector]
        assert abs(h[sector] - 4.0 * (A - dist)) < 1e-12


def test_histogram_matches_brute_force_and_rotates_with_the_grid():
    rng = random.Random(21)
    x, y = 0.05, 0.05
    for _ in range(20):
        grid = {(rng.randint(-20, 20), rng.randint(-20, 20)): float(rng.randint(1, 15)) for _ in range(60)}
        grid.pop((0, 0), None)
        h = polar_histogram(grid, x, y)
        # Brute force: every cell of the window contributes c^2 max(0, a - d) once.
        total = sum(c * c * max(0.0, A - math.hypot(i * 0.1, j * 0.1))
                    for (i, j), c in grid.items() if abs(i) <= 16 and abs(j) <= 16)
        assert abs(sum(h) - total) < 1e-9 * (1.0 + total)
        # Rotating the grid by 90 degrees about the robot shifts the histogram by 18 sectors.
        rot = {(-j, i): c for (i, j), c in grid.items()}
        hr = polar_histogram(rot, x, y)
        for k in range(72):
            assert abs(hr[(k + 18) % 72] - h[k]) < 1e-9 * (1.0 + h[k])


def test_smoothing_is_a_triangular_average():
    assert all(abs(v - 3.0) < 1e-12 for v in smooth([3.0] * 72))
    h = [0.0] * 72
    h[2] = 36.0
    hs = smooth(h, 5)
    for k in range(72):
        j = min((k - 2) % 72, (2 - k) % 72)
        assert abs(hs[k] - (6 - j if j <= 5 else 0)) < 1e-12


def blocked(sectors):
    hs = [0.0] * 72
    for k in sectors:
        hs[k % 72] = 10.0
    return hs


def test_steering_hand_cases():
    free = [0.0] * 72
    assert steer(free, 37.0, 1.0) == 37.5
    assert steer([5.0] * 72, 37.0, 1.0) is None
    # Sectors 0..9 blocked, target at 0 degrees: the near border is sector 71, so
    # k_n = 71, k_f = 71 - 18 = 53 and theta is sector 62.
    assert steer(blocked(range(10)), 0.0, 1.0) == 312.5
    # Target inside the wide valley but close to its border: keep s_max / 2 sectors away.
    assert steer(blocked(range(10)), 62.0, 1.0) == 97.5
    # Target well inside the wide valley: go straight to it.
    assert steer(blocked(range(10)), 182.0, 1.0) == 182.5
    # A narrow valley of sectors 20..25: steer to its middle.
    assert steer(blocked([k for k in range(72) if not 20 <= k <= 25]), 300.0, 1.0) == 115.0


def test_steering_always_picks_a_free_sector():
    rng = random.Random(22)
    for _ in range(500):
        hs = [rng.choice([0.0, 0.0, 0.0, 5.0]) for _ in range(72)]
        target = rng.uniform(0.0, 360.0)
        theta = steer(hs, target, 1.0)
        if all(v >= 1.0 for v in hs):
            assert theta is None
            continue
        k = int(theta / 5.0) % 72
        assert hs[k] < 1.0
        kt = int(target / 5.0)
        # A free target with at least 9 free sectors on each side is steered to directly.
        if all(hs[(kt + j) % 72] < 1.0 for j in range(-9, 10)):
            assert theta == (kt + 0.5) * 5.0


def test_valleys_are_maximal_runs():
    free = [False] * 72
    for k in list(range(70, 72)) + list(range(0, 3)) + list(range(10, 14)):
        free[k] = True
    assert sorted(valleys(free)) == [(10, 4), (70, 5)]
    assert valleys([True] * 72) == [(0, 72)]


def test_speed_rule():
    assert speed(0.0, 0.0, 0.6, 10.0, 120.0, 0.04) == 0.6 + 0.04
    assert speed(25.0, 0.0, 0.6, 10.0, 120.0, 0.04) == 0.04
    assert speed(0.0, -120.0, 0.6, 10.0, 120.0, 0.04) == 0.04
    assert abs(speed(5.0, 60.0, 0.6, 10.0, 120.0, 0.04) - (0.15 + 0.04)) < 1e-12


def scene():
    # A wall along x = 3 m with a gap of 1.2 m between y = 1.4 and y = 2.6, and a pole.
    g = {(30, j): 5.0 for j in range(-10, 50) if not 1.4 <= (j + 0.5) * 0.1 <= 2.6}
    g[(15, 12)] = 5.0
    return g


def test_passes_the_gap_and_keeps_away_from_obstacles():
    g = scene()
    for threshold in (5.0, 20.0):
        path = []
        _, _, _, steps, reached = run(g, (0.5, 0.5), 0.0, (5.0, 2.0), threshold, steps=200,
                                      record=lambda *p: path.append(p))
        assert reached and steps < 100
        clear = min(math.hypot((i + 0.5) * 0.1 - p[0], (j + 0.5) * 0.1 - p[1]) for p in path for (i, j) in g)
        assert clear > 0.15
