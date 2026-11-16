# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/daisy-descriptor/. The authors are listed in prov/HGVST3.jsonl.

import math
import random

from daisy_descriptor import bilinear, convolve, daisy, describe, gaussian_kernel, layers, orientation_maps, sigmas


def random_image(seed, w, h):
    rng = random.Random(seed)
    return [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]


def close(a, b, tol):
    return len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))


def test_length_and_unit_histograms():
    img = random_image(1, 32, 32)
    lay = layers(img)
    d = describe(lay, 16, 15)
    assert len(d) == 200 == (1 + 3 * 8) * 8
    for k in range(25):
        n = math.sqrt(sum(x * x for x in d[8 * k:8 * k + 8]))
        assert abs(n - 1.0) < 1e-12
    assert sigmas() == [2.5, 5.0, 7.5]


def test_orientation_maps_on_a_ramp():
    img = [[3.0 * u + 2.0 * v for u in range(10)] for v in range(10)]
    maps = orientation_maps(img, 8)
    for o in range(8):
        a = 2 * math.pi * o / 8
        assert abs(maps[o][5][5] - max(0.0, 3 * math.cos(a) + 2 * math.sin(a))) < 1e-12
    # Opposite maps hold the two rectified halves of the directional derivative.
    img = random_image(2, 12, 12)
    maps = orientation_maps(img, 8)
    for o in range(4):
        for v in range(12):
            for u in range(12):
                assert maps[o][v][u] == 0.0 or maps[o + 4][v][u] == 0.0


def test_kernel_and_constant_maps():
    for s in (0.5, 1.0, 2.5, 3.7):
        k = gaussian_kernel(s)
        assert abs(sum(k) - 1.0) < 1e-12 and k == k[::-1]
    flat = [[5.0] * 9 for _ in range(7)]
    assert all(abs(x - 5.0) < 1e-12 for row in convolve(flat, 2.0) for x in row)


def test_incremental_convolution_matches_direct_convolution_inside():
    img = random_image(3, 56, 56)
    maps = orientation_maps(img, 4)
    lay = layers(img, R=6.0, Q=3, bins=4)
    for i, s in enumerate(sigmas(6.0, 3)):
        direct = convolve(maps[1], s)
        top = max(direct[v][u] for v in range(20, 36) for u in range(20, 36))
        err = max(abs(direct[v][u] - lay[i][1][v][u]) for v in range(20, 36) for u in range(20, 36))
        assert err < 1e-3 * top


def test_rotation_by_90_degrees_permutes_the_descriptor():
    img = random_image(4, 28, 28)
    rot = [[img[27 - u][v] for u in range(28)] for v in range(28)]
    a, b = layers(img, R=6.0), layers(rot, R=6.0)
    for u, v in [(14, 11), (9, 16), (18, 18)]:
        # The pixel (u, v) of img is the pixel (27 - v, u) of rot; a quarter turn is 2 steps of 45 degrees.
        assert close(describe(b, 27 - v, u, R=6.0, k=2), describe(a, u, v, R=6.0), 1e-9)
    assert not close(describe(b, 27 - 11, 14, R=6.0), describe(a, 14, 11, R=6.0), 1e-3)


def test_offset_and_gain():
    img = random_image(5, 28, 28)
    base = describe(layers(img, R=6.0), 12, 15, R=6.0)
    assert describe(layers([[x + 30 for x in row] for row in img], R=6.0), 12, 15, R=6.0) == base
    assert close(describe(layers([[3 * x for x in row] for row in img], R=6.0), 12, 15, R=6.0), base, 1e-12)


def test_bilinear_and_dense_grid():
    ramp = [[2.0 * u - v for u in range(8)] for v in range(8)]
    assert abs(bilinear(ramp, 3.25, 4.5) - (6.5 - 4.5)) < 1e-12
    assert bilinear(ramp, 2, 5) == ramp[5][2]
    img = random_image(6, 24, 24)
    dense = daisy(img, step=8, R=6.0, Q=2, T=4, bins=4)
    assert sorted(dense) == [(u, v) for u in (0, 8, 16) for v in (0, 8, 16)]
    lay = layers(img, 6.0, 2, 4)
    assert dense[(8, 16)] == describe(lay, 8, 16, 6.0, 4)
    assert len(dense[(0, 0)]) == (1 + 2 * 4) * 4
