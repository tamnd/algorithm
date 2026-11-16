# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mosse-filter/. The authors are listed in prov/Q4156Y.jsonl.

import cmath
import math
import random

import pytest

from mosse_filter import Mosse, fft, fft2, gaussian_target, response


def dft(x):
    n = len(x)
    return [sum(x[j] * cmath.exp(-2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]


def test_fft_matches_the_direct_transform():
    rng = random.Random(1)
    for n in [1, 2, 8, 16]:
        x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        for a, b in zip(fft(x), dft(x)):
            assert abs(a - b) < 1e-9
        for a, b in zip(fft(fft(x), inverse=True), x):
            assert abs(a - b) < 1e-12
    with pytest.raises(ValueError):
        fft([1, 2, 3])


def test_fft2_matches_the_direct_transform():
    rng = random.Random(2)
    n = 4
    img = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    got = fft2(img)
    for k in range(n):
        for l in range(n):
            want = sum(img[v][u] * cmath.exp(-2j * math.pi * (u * l + v * k) / n)
                       for v in range(n) for u in range(n))
            assert abs(got[k][l] - want) < 1e-9


def test_product_with_conjugate_is_circular_correlation():
    rng = random.Random(3)
    n = 8
    f = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    h = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    ff, hh = fft2(f), fft2(h)
    g = fft2([[ff[v][u] * hh[v][u].conjugate() for u in range(n)] for v in range(n)], inverse=True)
    for v in range(n):
        for u in range(n):
            want = sum(f[(j + v) % n][(i + u) % n] * h[j][i] for j in range(n) for i in range(n))
            assert abs(g[v][u] - want) < 1e-9


def test_single_image_filter_reproduces_the_target():
    rng = random.Random(4)
    n = 16
    f_hat = fft2([[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)])
    g = gaussian_target(n)
    g_hat = fft2(g)
    a = [[g_hat[v][u] * f_hat[v][u].conjugate() for u in range(n)] for v in range(n)]
    b = [[f_hat[v][u] * f_hat[v][u].conjugate() for u in range(n)] for v in range(n)]
    out = response(f_hat, a, b, 1e-12)
    for v in range(n):
        for u in range(n):
            assert abs(out[v][u] - g[v][u]) < 1e-6


def test_a_missing_frequency_lowers_the_peak():
    f = [1, 2, 0, -1]
    f_hat = fft(f)
    assert abs(f_hat[2]) < 1e-12
    g_hat = fft([1, 0, 0, 0])
    eps = 1e-9
    h_conj = [gk * fk.conjugate() / (fk * fk.conjugate() + eps) for gk, fk in zip(g_hat, f_hat)]
    out = fft([fk * hk for fk, hk in zip(f_hat, h_conj)], inverse=True)
    for a, b in zip(out, [0.75, 0.25, -0.25, 0.25]):
        assert abs(a - b) < 1e-6


def texture(seed, k, lo, hi):
    rng = random.Random(seed)
    blobs = [(rng.uniform(lo, hi), rng.uniform(lo, hi), rng.uniform(2, 4), rng.uniform(40, 160))
             for _ in range(k)]

    def f(u, v):
        return 20 + sum(a * math.exp(-((u - x) ** 2 + (v - y) ** 2) / (2 * s * s)) for x, y, s, a in blobs)

    return f


N, HALF = 64, 16


def make_scene():
    back = texture(1, 40, -5, N + 5)
    bg = [[back(u, v) for u in range(N)] for v in range(N)]
    target = texture(2, 20, -3, 2 * HALF + 3)
    other = texture(3, 20, -3, 2 * HALF + 3)

    def frame(c, tex=target):
        img = [row[:] for row in bg]
        for v in range(N):
            for u in range(N):
                du, dv = u - c[0], v - c[1]
                if abs(du) <= HALF and abs(dv) <= HALF:
                    img[v][u] = tex(du + HALF, dv + HALF)
        return img

    return frame, other


def test_tracks_a_moving_target_and_stops_at_an_occlusion():
    frame, other = make_scene()
    truth = [(24 + 2.4 * t, 26 + 1.7 * t) for t in range(7)]
    tracker = Mosse(frame(truth[0]), truth[0])
    for c in truth[1:]:
        p, score, ok = tracker.update(frame(c))
        assert ok and score > 7
        assert math.dist(p, c) < 1
    before = tracker.center
    p, score, ok = tracker.update(frame(truth[-1], other))
    assert not ok and score < 7
    assert p == before
