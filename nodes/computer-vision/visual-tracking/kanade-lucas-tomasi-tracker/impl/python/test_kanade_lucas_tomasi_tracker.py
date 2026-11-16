# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kanade-lucas-tomasi-tracker/. The authors are listed in prov/GW9GYD.jsonl.

import math
import random

from kanade_lucas_tomasi_tracker import (
    LOST,
    corner_strength,
    klt_track,
    min_eigenvalue,
    pyr_lk,
    pyramid,
    select_features,
)

N = 48


def texture(seed):
    """A smooth texture: 14 Gaussian blobs at seeded places."""
    rng = random.Random(seed)
    blobs = [(rng.uniform(4, 44), rng.uniform(4, 44), rng.uniform(2.0, 3.5), rng.uniform(60, 200))
             for _ in range(14)]

    def f(u, v):
        return sum(a * math.exp(-((u - x) ** 2 + (v - y) ** 2) / (2 * s * s)) for x, y, s, a in blobs)

    return f


def frame(f, du=0.0, dv=0.0):
    """The texture moved by (du, dv): frame(u + du, v + dv) = f(u, v)."""
    return [[f(u - du, v - dv) for u in range(N)] for v in range(N)]


def interior(pts, margin=8):
    return [p for p in pts if margin <= p[0] <= N - margin and margin <= p[1] <= N - margin]


def test_pyramid_sizes_and_constant_image():
    img = [[7.0] * N for _ in range(N)]
    pyr = pyramid(img, 2)
    assert [(len(x), len(x[0])) for x in pyr] == [(48, 48), (24, 24), (12, 12)]
    assert all(abs(val - 7.0) < 1e-12 for lev in pyr for row in lev for val in row)


def test_min_eigenvalue_is_the_minimum_of_the_quadratic_form():
    rng = random.Random(3)
    for _ in range(20):
        a, c = rng.uniform(0, 10), rng.uniform(0, 10)
        b = rng.uniform(-1, 1) * math.sqrt(a * c)
        scan = min(a * math.cos(t) ** 2 + 2 * b * math.cos(t) * math.sin(t) + c * math.sin(t) ** 2
                   for t in (k * math.pi / 3600 for k in range(3600)))
        assert abs(min_eigenvalue(a, b, c) - scan) < 1e-4 * (a + c + 1)


def test_selection_threshold_spacing_and_maximality():
    img = frame(texture(1))
    lam = corner_strength(img, 3)
    quality, dist = 0.05, 6.0
    pts = select_features(img, 3, quality, dist)
    top = max(lam.values())
    kept = [(int(u), int(v)) for u, v in pts]
    assert kept and kept[0] == max(lam, key=lambda p: lam[p])
    for p in kept:
        assert lam[p] >= quality * top
    for i, p in enumerate(kept):
        for q in kept[:i]:
            assert math.dist(p, q) >= dist
    # every strong pixel that was not kept is close to a kept pixel at least as strong
    for p, val in lam.items():
        if val >= quality * top and p not in kept:
            assert any(math.dist(p, q) < dist and lam[q] >= val for q in kept)


def test_subpixel_translation():
    f = texture(1)
    img0, img1 = frame(f), frame(f, 1.3, -0.7)
    p0, p1 = pyramid(img0, 2), pyramid(img1, 2)
    pts = interior(select_features(img0, 3, 0.05, 6.0, 10))
    assert len(pts) >= 5
    for p in pts:
        d = pyr_lk(p0, p1, p)
        assert d is not LOST
        assert math.hypot(d[0] - 1.3, d[1] + 0.7) < 0.1


def test_pyramid_handles_large_motion():
    f = texture(1)
    img0, img1 = frame(f), frame(f, 6.0, 4.0)
    pts = interior(select_features(img0, 3, 0.05, 6.0, 10))
    errors = {}
    for levels in (0, 2):
        p0, p1 = pyramid(img0, levels), pyramid(img1, levels)
        errs = []
        for p in pts:
            d = pyr_lk(p0, p1, p)
            errs.append(math.inf if d is LOST else math.hypot(d[0] - 6.0, d[1] - 4.0))
        errors[levels] = errs
    assert max(errors[2]) < 0.01
    assert max(errors[0]) > 1.0


def test_straight_edge_is_lost():
    edge = [[100.0 / (1 + math.exp(-(u - 23.6))) for u in range(N)] for v in range(N)]
    moved = [[100.0 / (1 + math.exp(-(u - 24.6))) for u in range(N)] for v in range(N)]
    assert pyr_lk(pyramid(edge, 1), pyramid(moved, 1), (24.0, 24.0)) is LOST


def test_constant_velocity_over_frames():
    f = texture(1)
    vel = (0.8, 0.5)
    frames = [frame(f, vel[0] * t, vel[1] * t) for t in range(8)]
    tracks = klt_track(frames, levels=2, r=3, max_count=10, min_dist=6.0)
    # points that stay at least 8 pixels inside the image for all 8 frames
    full = [tr for tr in tracks if len(tr) == 8 and tr[0] in interior([tr[0]]) and tr[-1] in interior([tr[-1]])]
    assert len(full) >= 4
    for tr in full:
        start = tr[0]
        for t, p in enumerate(tr):
            assert math.hypot(p[0] - start[0] - vel[0] * t, p[1] - start[1] - vel[1] * t) < 0.2


def test_forward_backward_check_drops_an_occluded_point():
    f, other = texture(1), texture(3)
    img0 = frame(f)
    img1 = frame(f, 1.0, 0.5)
    for v in range(19, 36):
        for u in range(29, 46):
            img1[v][u] = other(u, v)
    tracks = klt_track([img0, img1], levels=2, r=3, max_count=10, min_dist=6.0, fb_max=0.5)
    by_start = {tr[0]: tr for tr in tracks}
    assert len(by_start[(37.0, 27.0)]) == 1
    for p in [(34.0, 4.0), (13.0, 21.0), (24.0, 18.0), (8.0, 5.0)]:
        tr = by_start[p]
        assert len(tr) == 2
        assert math.hypot(tr[1][0] - p[0] - 1.0, tr[1][1] - p[1] - 0.5) < 0.1
