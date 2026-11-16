# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/determinant-of-hessian-detector/. The authors are listed in prov/698GJR.jsonl.

import math
import random

from determinant_of_hessian_detector import (
    doh_blobs,
    doh_response,
    gaussian_kernel,
    parabola_offset,
    scale_maxima,
)

SCALES = [2 ** (i / 2) for i in range(9)]  # 1, 1.41, 2, ..., 16


def blob(n, cx, cy, t0, amp=1.0):
    return [[amp * math.exp(-((u - cx) ** 2 + (v - cy) ** 2) / (2 * t0)) for u in range(n)] for v in range(n)]


def direct_response(img, t):
    """2D convolution, then the Hessian by the same differences; independent of the separable code."""
    k = gaussian_kernel(math.sqrt(t))
    r = len(k) // 2
    h, w = len(img), len(img[0])
    L = [[sum(k[i + r] * k[j + r] * img[min(max(v + j, 0), h - 1)][min(max(u + i, 0), w - 1)]
              for i in range(-r, r + 1) for j in range(-r, r + 1)) for u in range(w)] for v in range(h)]
    out = [[0.0] * w for _ in range(h)]
    for v in range(1, h - 1):
        for u in range(1, w - 1):
            # A 3 x 3 Taylor fit gives the same second differences.
            m = [[L[v + b][u + a] for a in (-1, 0, 1)] for b in (-1, 0, 1)]
            lxx = m[1][2] - 2 * m[1][1] + m[1][0]
            lyy = m[2][1] - 2 * m[1][1] + m[0][1]
            lxy = (m[2][2] - m[2][0] - m[0][2] + m[0][0]) / 4
            out[v][u] = t * t * (lxx * lyy - lxy ** 2)
    return out


def oracle_maxima(stack, tau):
    out = []
    for i in range(1, len(stack) - 1):
        for v in range(1, len(stack[0]) - 1):
            for u in range(1, len(stack[0][0]) - 1):
                x = stack[i][v][u]
                nb = [stack[i + a][v + b][u + c] for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1)]
                nb.remove(x)
                if x > tau and max(nb) < x:
                    out.append((i, u, v))
    return out


def test_response_matches_direct_convolution():
    rng = random.Random(8)
    for _ in range(10):
        w, h = rng.randint(3, 7), rng.randint(3, 7)
        img = [[rng.random() for _ in range(w)] for _ in range(h)]
        for t in (0.5, 1.5):
            a, b = doh_response(img, t), direct_response(img, t)
            assert all(abs(x - y) < 1e-12 for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def test_scale_maxima_against_oracle():
    rng = random.Random(1998)
    for _ in range(600):
        k, h, w = rng.randint(3, 5), rng.randint(3, 6), rng.randint(3, 6)
        stack = [[[rng.randint(-3, 3) for _ in range(w)] for _ in range(h)] for _ in range(k)]
        tau = rng.choice([-10, 0, 1])
        assert sorted(scale_maxima(stack, tau)) == sorted(oracle_maxima(stack, tau))


def test_parabola_offset():
    for x0 in (-0.5, -0.2, 0.0, 0.3, 0.5):
        f = lambda x: 3 - 2 * (x - x0) ** 2
        assert abs(parabola_offset(f(-1), f(0), f(1)) - x0) < 1e-12
    assert parabola_offset(1.0, 1.0, 1.0) == 0.0


def test_worked_example_blob():
    img = blob(32, 16, 16, 4.0)
    (x, y, t, d), = doh_blobs(img, SCALES, 1e-5)
    assert (x, y) == (16.0, 16.0)
    assert abs(t - 4.12) < 0.01 and abs(d - 0.05898) < 1e-5
    # Continuous value at the centre: t0^2 t^2 / (t0 + t)^4, which is 1/16 at t = t0.
    centre = [doh_response(img, s)[16][16] for s in SCALES]
    for s, c in zip(SCALES, centre):
        want = 16 * s * s / (4 + s) ** 4
        assert abs(c - want) < 0.1 * want
    assert max(range(9), key=lambda i: centre[i]) == 4  # t = 4


def test_selected_scale_follows_blob_variance():
    for t0 in (2.0, 4.0, 8.0):
        (x, y, t, d), = doh_blobs(blob(32, 16, 16, t0), SCALES, 1e-5)
        assert abs(t - t0) < 0.08 * t0
        assert abs(x - 16) < 1e-9 and abs(y - 16) < 1e-9


def test_dark_blob_and_offset_give_the_same_blob():
    img = blob(32, 16, 16, 4.0)
    a = doh_blobs(img, SCALES, 1e-5)
    b = doh_blobs([[1 - p for p in r] for r in img], SCALES, 1e-5)
    c = doh_blobs([[p + 5 for p in r] for r in img], SCALES, 1e-5)
    for other in (b, c):
        assert len(other) == 1 and all(abs(p - q) < 1e-9 for p, q in zip(a[0], other[0]))


def test_straight_edge_and_flat_give_nothing():
    edge = [[1.0 if u >= 16 else 0.0 for u in range(32)] for v in range(32)]
    assert all(abs(x) < 1e-12 for row in doh_response(edge, 2.0) for x in row)
    assert doh_blobs(edge, SCALES, 1e-5) == []
    assert doh_blobs([[0.3] * 10 for _ in range(10)], [1, 2, 4], 0.0) == []


def test_rotation_by_90_degrees():
    rng = random.Random(31)
    h, w = 7, 9
    img = [[rng.random() for _ in range(w)] for _ in range(h)]
    rot = [[img[h - 1 - j][i] for j in range(h)] for i in range(w)]
    a, b = doh_response(img, 1.0), doh_response(rot, 1.0)
    for v in range(h):
        for u in range(w):
            assert abs(a[v][u] - b[u][h - 1 - v]) < 1e-12
