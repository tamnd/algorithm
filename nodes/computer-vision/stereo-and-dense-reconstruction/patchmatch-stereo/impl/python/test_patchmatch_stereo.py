# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/patchmatch-stereo/. The authors are listed in prov/G3M5MP.jsonl.

import math
import random

from patchmatch_stereo import (
    Params,
    View,
    disparity,
    disparity_maps,
    fill_invalid,
    left_right_check,
    normal_of_plane,
    patchmatch_stereo,
    plane_cost,
    plane_from_point_normal,
    transfer_plane,
)


def texture(seed):
    rng = random.Random(seed)
    waves = []
    for _ in range(6):
        period = rng.uniform(3.0, 9.0)
        ang = rng.uniform(0.0, math.pi)
        k = 2.0 * math.pi / period
        waves.append((k * math.cos(ang), k * math.sin(ang), rng.uniform(0.0, 6.3), rng.uniform(15.0, 30.0)))

    def g(x, y):
        return 128.0 + sum(a * math.sin(kx * x + ky * y + ph) for kx, ky, ph, a in waves)

    return g


def slanted_scene(fl, w, h, seed):
    """Left image g(x, y); right image g(x' + d_R(x', y), y) for the plane fl."""
    g = texture(seed)
    fr = transfer_plane(fl, 0)
    left = [[g(x, y) for x in range(w)] for y in range(h)]
    right = [[g(x + disparity(fr, x, y), y) for x in range(w)] for y in range(h)]
    return left, right


def test_example_plane() -> None:
    f = plane_from_point_normal(5, 3, 4.0, (0.6, 0.0, 0.8))
    assert all(abs(u - v) < 1e-12 for u, v in zip(f, (-0.75, 0.0, 7.75)))
    assert abs(disparity(f, 5, 3) - 4.0) < 1e-12
    g = transfer_plane(f, 0)
    assert all(abs(u - v) < 1e-12 for u, v in zip(g, (-0.75 / 1.75, 0.0, 7.75 / 1.75)))
    # The left pixel x = 5 with disparity 4 is the right pixel x' = 1.
    assert abs(disparity(g, 1, 3) - 4.0) < 1e-12


def test_plane_normal_round_trip() -> None:
    rng = random.Random(1)
    for _ in range(200):
        n = [rng.gauss(0, 1) for _ in range(3)]
        n[2] = abs(n[2]) + 0.1
        s = math.sqrt(sum(t * t for t in n))
        n = tuple(t / s for t in n)
        x0, y0, z0 = rng.uniform(0, 30), rng.uniform(0, 20), rng.uniform(0, 10)
        f = plane_from_point_normal(x0, y0, z0, n)
        assert abs(disparity(f, x0, y0) - z0) < 1e-9
        assert all(abs(u - v) < 1e-9 for u, v in zip(normal_of_plane(f), n))


def test_transfer_plane() -> None:
    rng = random.Random(2)
    for _ in range(200):
        f = (rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5), rng.uniform(0, 10))
        for v in (0, 1):
            g = transfer_plane(f, v)
            back = transfer_plane(g, 1 - v)
            assert all(abs(u - w) < 1e-9 for u, w in zip(back, f))
            # A point and its match have the same disparity in both planes.
            x, y = rng.uniform(0, 30), rng.uniform(0, 20)
            d = disparity(f, x, y)
            xm = x - d if v == 0 else x + d
            assert abs(disparity(g, xm, y) - d) < 1e-9
    assert transfer_plane((1.0, 0.0, 2.0), 0) is None


def test_cost_zero_at_true_shift() -> None:
    rng = random.Random(3)
    w, h, shift = 16, 9, 2
    left = [[rng.randrange(256) for _ in range(w)] for _ in range(h)]
    right = [[left[y][min(x + shift, w - 1)] for x in range(w)] for y in range(h)]
    prm = Params(radius=2, max_disp=5.0)
    views = [View(left, prm.radius, prm.gamma), View(right, prm.radius, prm.gamma)]
    for y in range(h):
        for x in range(shift + 3, w - 3):
            assert plane_cost(views, 0, x, y, (0.0, 0.0, float(shift)), prm) < 1e-9
            assert plane_cost(views, 0, x, y, (0.0, 0.0, shift + 1.0), prm) > 1.0


def test_slanted_plane_and_monotone_cost() -> None:
    fl = (0.15, 0.05, 2.0)
    w, h = 20, 12
    left, right = slanted_scene(fl, w, h, 5)
    inner = [(x, y) for y in range(3, h - 3) for x in range(9, w - 3)]
    errors = {}
    for fronto in (False, True):
        prm = Params(radius=3, max_disp=8.0, fronto=fronto)
        hist = []
        planes, _ = patchmatch_stereo(left, right, prm, random.Random(3), history=hist)
        for before, after in zip(hist, hist[1:]):
            for v in (0, 1):
                assert all(after[v][p] <= before[v][p] for p in before[v])
        dl, _ = disparity_maps(planes, (h, w))
        e = [abs(dl[y][x] - disparity(fl, x, y)) for x, y in inner]
        errors[fronto] = sum(e) / len(e)
        if not fronto:
            assert max(e) < 0.5
    assert errors[False] < 0.1
    assert errors[False] < errors[True]


def test_left_right_check_and_fill() -> None:
    dl = [[2.0, 2.0, 2.0, 2.0, 2.0, 4.0, 2.0, 2.0]]
    dr = [[2.0] * 8]
    valid = left_right_check(dl, dr)
    # x = 0 and x = 1 match outside the right image; x = 5 disagrees by 2.
    assert valid == [[False, False, True, True, True, False, True, True]]
    planes = {(x, 0): (0.0, 0.0, dl[0][x]) for x in range(8)}
    planes[(4, 0)] = (-0.5, 0.0, 4.0)  # 2.0 at x = 4, 1.5 at x = 5
    out = fill_invalid(dl, valid, planes)
    # x = 5 takes the lower of the plane of x = 4 (1.5) and of x = 6 (2.0).
    assert out[0][5] == 1.5
    # x = 0 and x = 1 have a valid pixel only to the right.
    assert out[0][0] == 2.0 and out[0][1] == 2.0
    assert out[0][2:5] == dl[0][2:5]


def test_deterministic() -> None:
    left, right = slanted_scene((0.1, 0.0, 1.0), 10, 6, 9)
    prm = Params(radius=1, max_disp=4.0, iterations=1)
    a = patchmatch_stereo(left, right, prm, random.Random(4))
    b = patchmatch_stereo(left, right, prm, random.Random(4))
    assert a == b
