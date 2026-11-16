# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/camshift/. The authors are listed in prov/WQRMAE.jsonl.

import math
import random

from camshift import (
    back_project,
    camshift,
    camshift_frame,
    lookup_table,
    moments,
    shape,
    window_side,
)

N = 80


def blank():
    return [[0.0] * N for _ in range(N)]


def ellipse(phi_deg, a, b, c=(40, 40)):
    phi = math.radians(phi_deg)
    prob = blank()
    for v in range(N):
        for u in range(N):
            du, dv = u - c[0], v - c[1]
            x = math.cos(phi) * du + math.sin(phi) * dv
            y = -math.sin(phi) * du + math.cos(phi) * dv
            if (x / a) ** 2 + (y / b) ** 2 <= 1:
                prob[v][u] = 255.0
    return prob


def scene(rng, c, half):
    img = [[rng.randrange(0, 120) for _ in range(N)] for _ in range(N)]
    for v in range(N):
        for u in range(N):
            if abs(u - c[0]) <= half and abs(v - c[1]) <= half:
                img[v][u] = 180 + rng.randrange(0, 60)
    return img


def test_lookup_table_and_back_projection():
    img = scene(random.Random(1), (30, 30), 5)
    table = lookup_table(img, (30, 30, 5, 5), 16)
    assert max(table) == 255
    assert all(table[b] == 0 for b in range(8))
    prob = back_project(img, table, 16)
    assert prob[30][30] > 0 and prob[5][5] == 0


def test_size_rule():
    prob = blank()
    for v in range(30, 40):
        for u in range(20, 30):
            prob[v][u] = 255.0
    m = moments(prob, (24.5, 34.5, 15, 15))
    assert m[0] == 25500
    assert window_side(m[0]) == 21
    assert window_side(0) == 3
    for m00 in [1, 100, 2560, 25600, 123456]:
        s = window_side(m00)
        assert s % 2 == 1 and s >= 2 * math.sqrt(m00 / 256)


def test_shape_of_a_uniform_square():
    prob = blank()
    for v in range(30, 40):
        for u in range(20, 30):
            prob[v][u] = 255.0
    (xc, yc), _, length, width = shape(moments(prob, (24.5, 34.5, 15, 15)))
    assert (xc, yc) == (24.5, 34.5)
    # the variance of 10 consecutive integers is 99 / 12
    assert abs(length - math.sqrt(99 / 12)) < 1e-9
    assert abs(width - math.sqrt(99 / 12)) < 1e-9


def test_orientation_and_axes_of_an_ellipse():
    for phi in [-60, -30, 0, 15, 30, 75]:
        prob = ellipse(phi, 12, 5)
        _, theta, length, width = shape(moments(prob, (40, 40, 30, 30)))
        diff = (math.degrees(theta) - phi + 90) % 180 - 90
        assert abs(diff) < 2
        assert abs(length - 6) < 0.2
        assert abs(width - 2.5) < 0.2


def test_centered_window_is_a_fixed_point():
    prob = ellipse(30, 12, 5)
    window, info = camshift_frame(prob, (40, 40, 15, 15))
    assert math.dist(window[:2], (40, 40)) < 1e-9
    assert info is not None


def test_follows_a_moving_growing_target():
    rng = random.Random(7)
    truth = [(20 + 3 * t, 25 + 2 * t, 4 + 0.5 * t) for t in range(10)]
    frames = [scene(rng, (x, y), h) for x, y, h in truth]
    out = camshift(frames, (20, 25, 4, 4))
    errors = [math.dist(window[:2], (x, y)) for (window, _), (x, y, _) in zip(out, truth[1:])]
    assert all(info is not None for _, info in out)
    # the first window is only as large as the target, so it stops short;
    # once the size rule has grown the window, the center is close
    assert errors[0] < 1.5
    assert max(errors[1:]) < 0.5
    halves = [w[2] for w, _ in out]
    assert all(b >= a for a, b in zip(halves, halves[1:]))
    assert halves[-1] > 2 * 4


def test_empty_window_is_lost():
    window, info = camshift_frame(blank(), (40, 40, 5, 5))
    assert info is None and window == (40, 40, 5, 5)
