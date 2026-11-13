# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sift/. The authors are listed in prov/P9C537.jsonl.

import math
import random
from fractions import Fraction

import pytest

from sift import (
    blur,
    build_pyramid,
    descriptor,
    detect_and_describe,
    dominant_orientations,
    downsample,
    gaussian_kernel,
    is_extremum,
    match,
    normalize_clip,
    passes_edge_test,
    quadratic_offset,
    scan_extrema,
)


def blobs(seed, w, h, n=6):
    rng = random.Random(seed)
    bl = [(rng.uniform(4, w - 5), rng.uniform(4, h - 5), rng.uniform(1.5, 3.5),
           rng.choice([-1, 1]) * rng.uniform(0.2, 0.4)) for _ in range(n)]
    return [[min(1.0, max(0.0, 0.5 + sum(a * math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * s * s))
                                         for cx, cy, s, a in bl)))
             for x in range(w)] for y in range(h)]


def rot90(img):
    """Counterclockwise: pixel (x, y) moves to (y, W - 1 - x)."""
    return [list(r) for r in zip(*img)][::-1]


def test_blur_matches_direct_2d_sum():
    rng = random.Random(1)
    img = [[rng.random() for _ in range(9)] for _ in range(7)]
    sigma = 1.3
    k = gaussian_kernel(sigma)
    r = len(k) // 2
    out = blur(img, sigma)
    for y in range(7):
        for x in range(9):
            direct = 0.0
            for j in range(-r, r + 1):
                for i in range(-r, r + 1):
                    yy = min(max(y + j, 0), 6)
                    xx = min(max(x + i, 0), 8)
                    direct += k[i + r] * k[j + r] * img[yy][xx]
            assert abs(out[y][x] - direct) < 1e-12


def test_blur_keeps_a_constant_image():
    out = blur([[0.25] * 6 for _ in range(5)], 2.0)
    assert all(abs(v - 0.25) < 1e-15 for r in out for v in r)


def test_pyramid_shape():
    img = blobs(2, 33, 41)
    gauss, dog = build_pyramid(img, n_octaves=3, s=3)
    assert [len(g) for g in gauss] == [6, 6, 6]
    assert [len(d) for d in dog] == [5, 5, 5]
    assert [(len(g[0][0]), len(g[0])) for g in gauss] == [(33, 41), (17, 21), (9, 11)]
    assert gauss[1][0] == downsample(gauss[0][3])


def brute_extrema(d):
    out = []
    for i in range(1, len(d) - 1):
        for y in range(1, len(d[0]) - 1):
            for x in range(1, len(d[0][0]) - 1):
                v = d[i][y][x]
                nb = [d[i + a][y + b][x + c] for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1)
                      if (a, b, c) != (0, 0, 0)]
                assert len(nb) == 26
                if all(v > u for u in nb) or all(v < u for u in nb):
                    out.append((i, y, x))
    return out


@pytest.mark.parametrize("seed", range(4))
def test_extrema_scan_matches_brute_force(seed):
    rng = random.Random(10 + seed)
    d = [[[rng.randint(0, 6) for _ in range(7)] for _ in range(6)] for _ in range(4)]
    assert scan_extrema(d) == brute_extrema(d)


def test_extremum_needs_strict_inequality():
    d = [[[0] * 3 for _ in range(3)] for _ in range(3)]
    d[1][1][1] = 5
    assert is_extremum(d, 1, 1, 1)
    d[0][0][0] = 5
    assert not is_extremum(d, 1, 1, 1)


def test_quadratic_fit_is_exact_on_a_quadratic():
    # D(x, y, s) = c - q(p - p0) for a positive definite q, sampled on a 3 x 3 x 3 grid.
    p0 = (Fraction(1, 5), Fraction(-1, 3), Fraction(2, 7))
    m = [[Fraction(3), Fraction(1, 2), Fraction(0)],
         [Fraction(1, 2), Fraction(2), Fraction(1, 4)],
         [Fraction(0), Fraction(1, 4), Fraction(1)]]
    c = Fraction(9, 10)

    def f(x, y, s):
        v = (x - p0[0], y - p0[1], s - p0[2])
        return c - sum(v[a] * m[a][b] * v[b] for a in range(3) for b in range(3)) / 2

    d = [[[f(x - 1, y - 1, s - 1) for x in range(3)] for y in range(3)] for s in range(3)]
    z, val = quadratic_offset(d, 1, 1, 1)
    assert z == list(p0)
    assert val == c


@pytest.mark.parametrize("seed", range(3))
def test_edge_test_matches_eigenvalue_ratio(seed):
    rng = random.Random(20 + seed)
    r = 10
    for _ in range(500):
        dxx = rng.randint(-40, 40)
        dyy = rng.randint(-40, 40)
        dxy = rng.randint(-20, 20)
        tr, det = dxx + dyy, dxx * dyy - dxy * dxy
        ok = passes_edge_test(dxx, dyy, dxy, r)
        if det <= 0:
            assert not ok
            continue
        disc = math.sqrt(((dxx - dyy) / 2) ** 2 + dxy * dxy)
        l1, l2 = (dxx + dyy) / 2 + disc, (dxx + dyy) / 2 - disc
        big, small = max(abs(l1), abs(l2)), min(abs(l1), abs(l2))
        ratio = big / small
        if abs(ratio - r) > 1e-9:
            assert ok == (ratio < r)


def test_edge_test_boundary_is_ratio_r():
    # Eigenvalues 10 and 1: (11)^2 / 10 is not below (r + 1)^2 / r, so it is rejected.
    assert not passes_edge_test(10, 1, 0, 10)
    assert passes_edge_test(9, 1, 0, 10)
    assert passes_edge_test(-9, -1, 0, 10)


def test_orientation_peaks_and_parabola():
    hist = [0.0] * 36
    hist[4], hist[5], hist[6] = 2.0, 4.0, 3.0
    hist[20] = 3.5
    hist[30] = 1.0
    peaks = dominant_orientations(hist)
    assert len(peaks) == 2
    # Bin 5 covers [50, 60) degrees; the parabola moves the peak by (2 - 3) / (2 (2 - 8 + 3)) = 1/6 bin.
    assert abs(math.degrees(peaks[0]) - (55 + 10 / 6)) < 1e-9
    assert abs(math.degrees(peaks[1]) - 205) < 1e-9


def test_normalize_clip():
    v = normalize_clip([1.0] + [0.0] * 127)
    assert v[0] == 1.0
    # 3 / sqrt(33) > 0.2 is clipped; 1 / sqrt(33) < 0.2 is kept.
    v = normalize_clip([3.0] + [1.0] * 24)
    assert abs(sum(x * x for x in v) - 1) < 1e-12
    assert abs(v[0] / v[1] - 0.2 * math.sqrt(33)) < 1e-9


def brute_match(a, b, ratio):
    out = []
    for i, p in enumerate(a):
        dist = sorted((sum((x - y) ** 2 for x, y in zip(p, q)), j) for j, q in enumerate(b))
        if len(dist) >= 2 and math.sqrt(dist[0][0]) < ratio * math.sqrt(dist[1][0]):
            out.append((i, dist[0][1]))
    return out


@pytest.mark.parametrize("seed", range(4))
def test_match_equals_brute_force(seed):
    rng = random.Random(30 + seed)
    b = [[rng.random() for _ in range(16)] for _ in range(25)]
    a = [[x + rng.gauss(0, 0.05) for x in rng.choice(b)] for _ in range(10)]
    a += [[rng.random() for _ in range(16)] for _ in range(10)]
    assert match(a, b, 0.8) == brute_match(a, b, 0.8)


def test_descriptor_is_unit_length_with_128_entries():
    img = blobs(4, 31, 31)
    gauss, _ = build_pyramid(img, 1)
    d = descriptor(gauss[0][1], 15, 15, 15.2, 14.9, 2.0, 0.7)
    assert len(d) == 128
    assert abs(sum(v * v for v in d) - 1) < 1e-12
    assert min(d) >= 0


def test_rotation_by_90_degrees_on_odd_sizes():
    img = blobs(3, 33, 41)
    w = len(img[0])
    k1 = detect_and_describe(img)
    k2 = detect_and_describe(rot90(img))
    assert len(k1) == len(k2) > 0
    pairs = {}
    for i, a in enumerate(k1):
        hits = [j for j, b in enumerate(k2)
                if abs(b["x"] - a["y"]) < 1e-9 and abs(b["y"] - (w - 1 - a["x"])) < 1e-9
                and abs(b["sigma"] - a["sigma"]) < 1e-9
                and abs((b["theta"] - a["theta"] + math.pi / 2 + math.pi) % (2 * math.pi) - math.pi) < 1e-9]
        assert len(hits) == 1
        j = hits[0]
        assert max(abs(p - q) for p, q in zip(a["desc"], k2[j]["desc"])) < 1e-9
        pairs[i] = j
    found = match([a["desc"] for a in k1], [b["desc"] for b in k2])
    assert found and all(pairs[i] == j for i, j in found)
