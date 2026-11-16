# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mean-shift-tracking/. The authors are listed in prov/85H8BD.jsonl.

import math
import random

from mean_shift_tracking import (
    bhattacharyya,
    histogram,
    mean_shift_step,
    track,
    weighted_mean_shift,
)

N = 64
H = (8, 6)


def scene(rng, c):
    """Noise from 0 to 95, and an ellipse with half axes 8 and 6 at c whose
    left half is bright (200 to 239) and right half is mid gray (130 to 159)."""
    img = [[rng.randrange(0, 96) for _ in range(N)] for _ in range(N)]
    for v in range(N):
        for u in range(N):
            du, dv = u - c[0], v - c[1]
            if (du / 8) ** 2 + (dv / 6) ** 2 <= 1:
                img[v][u] = 200 + rng.randrange(0, 40) if du < 0 else 130 + rng.randrange(0, 30)
    return img


def test_histogram_and_coefficient():
    rng = random.Random(1)
    img = [[rng.randrange(256) for _ in range(N)] for _ in range(N)]
    for y in [(20, 20), (31.4, 12.7), (3, 60)]:
        p = histogram(img, y, H, 16)
        assert abs(sum(p) - 1) < 1e-12
        assert abs(bhattacharyya(p, p) - 1) < 1e-12
        q = histogram(img, (40, 40), H, 16)
        assert 0 <= bhattacharyya(p, q) <= 1 + 1e-12


def test_weighted_step_raises_the_density():
    rng = random.Random(2)
    h = (5.0, 3.0)

    def density(pts, ws, y):
        s = 0.0
        for (u, v), w in zip(pts, ws):
            r = ((u - y[0]) / h[0]) ** 2 + ((v - y[1]) / h[1]) ** 2
            if r < 1:
                s += w * (1 - r)
        return s

    for _ in range(200):
        pts = [(rng.uniform(0, 20), rng.uniform(0, 20)) for _ in range(30)]
        ws = [rng.uniform(0, 2) for _ in pts]
        y0 = (rng.uniform(0, 20), rng.uniform(0, 20))
        y1 = weighted_mean_shift(pts, ws, y0, h)
        inside = sum(w for (u, v), w in zip(pts, ws)
                     if ((u - y0[0]) / h[0]) ** 2 + ((v - y0[1]) / h[1]) ** 2 <= 1)
        gain = inside * (((y1[0] - y0[0]) / h[0]) ** 2 + ((y1[1] - y0[1]) / h[1]) ** 2)
        assert density(pts, ws, y1) - density(pts, ws, y0) >= gain - 1e-9


def test_model_window_is_a_fixed_point():
    img = scene(random.Random(3), (30, 30))
    q = histogram(img, (30, 30), H, 16)
    y, rho, history = mean_shift_step(img, q, (30, 30), q, H, 16)
    assert math.dist(y, (30, 30)) < 1e-9
    assert abs(rho - 1) < 1e-12
    assert len(history) == 2


def test_coefficient_never_decreases():
    rng = random.Random(4)
    img = scene(rng, (30, 32))
    q = histogram(scene(random.Random(5), (30, 32)), (30, 32), H, 16)
    for _ in range(10):
        y0 = (30 + rng.uniform(-12, 12), 32 + rng.uniform(-9, 9))
        _, _, history = mean_shift_step(img, q, y0, histogram(img, y0, H, 16), H, 16)
        for a, b in zip(history, history[1:]):
            assert b >= a


def test_tracks_a_moving_target():
    rng = random.Random(4)
    truth = [(16 + 2.5 * t, 20 + 1.5 * t) for t in range(12)]
    frames = [scene(rng, c) for c in truth]
    centers, scores = track(frames, truth[0], H)
    for c, t in zip(centers, truth):
        assert math.dist(c, t) < 0.3
    assert min(scores) > 0.98


def test_reach_is_set_by_the_overlap():
    for jump, found in [(6, True), (14, True), (18, False)]:
        rng = random.Random(4)
        frames = [scene(rng, (20, 30)), scene(rng, (20 + jump, 30))]
        centers, scores = track(frames, (20, 30), H)
        if found:
            assert math.dist(centers[1], (20 + jump, 30)) < 0.5
        else:
            assert centers[1] == (20, 30)
            assert scores[1] == 0
