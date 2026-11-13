# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/image-warping/. The authors are listed in prov/V5CTT9.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from image_warping import (affine, forward_warp, homography, invert_affine, inverse_warp,
                           rotation_about, sample_nearest)


def tent(t):
    return max(F(0), 1 - abs(t))


def bilinear_direct(img, x, y, fill):
    """Sum over all pixel centers of tent(x - i) tent(y - j) I[j][i], the tensor form of bilinear interpolation."""
    h, w = len(img), len(img[0])
    if not (0 <= x <= w - 1 and 0 <= y <= h - 1):
        return fill
    return sum(tent(x - i) * tent(y - j) * img[j][i] for j in range(h) for i in range(w))


def rand_frac(rng, lo, hi, den=6):
    return F(rng.randint(lo * den, hi * den), den)


def test_inverse_warp_against_direct_formula():
    rng = random.Random(1990)
    done = 0
    while done < 500:
        w, h = rng.randint(1, 5), rng.randint(1, 5)
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        coef = [rand_frac(rng, -2, 2) for _ in range(6)]
        if coef[0] * coef[4] - coef[1] * coef[3] == 0:
            continue
        inv = affine(*coef)
        ow, oh = rng.randint(1, 6), rng.randint(1, 6)
        out = inverse_warp(img, ow, oh, inv, fill=-1)
        for v in range(oh):
            for u in range(ow):
                x, y = inv(u, v)
                assert out[v][u] == bilinear_direct(img, x, y, -1)
        done += 1


def test_rotation_by_90_is_a_permutation():
    rng = random.Random(3)
    for _ in range(200):
        w, h = rng.randint(1, 6), rng.randint(1, 6)
        img = [[rng.randint(0, 999) for _ in range(w)] for _ in range(h)]
        # output is h wide and w high; output (u, v) reads input (v, h - 1 - u)
        out = inverse_warp(img, h, w, lambda u, v: (v, h - 1 - u))
        for v in range(w):
            for u in range(h):
                assert out[v][u] == img[h - 1 - u][v]
        assert sorted(sum(out, [])) == sorted(sum(img, []))
        back = img
        for _ in range(4):
            hh, ww = len(back), len(back[0])
            back = inverse_warp(back, hh, ww, lambda u, v, hh=hh: (v, hh - 1 - u), method="nearest")
        assert back == img


def test_identity_translation_and_nearest():
    rng = random.Random(5)
    for _ in range(200):
        w, h = rng.randint(1, 6), rng.randint(1, 6)
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        assert inverse_warp(img, w, h, lambda u, v: (u, v)) == img
        dx, dy = rng.randint(-3, 3), rng.randint(-3, 3)
        out = inverse_warp(img, w, h, lambda u, v: (u - dx, v - dy), fill=-1)
        for v in range(h):
            for u in range(w):
                inside = 0 <= u - dx < w and 0 <= v - dy < h
                assert out[v][u] == (img[v - dy][u - dx] if inside else -1)
        x, y = rand_frac(rng, 0, w - 1), rand_frac(rng, 0, h - 1)
        i = min(range(w), key=lambda k: (abs(x - k), -k))
        j = min(range(h), key=lambda k: (abs(y - k), -k))
        assert sample_nearest(img, x, y) == img[j][i]


def test_forward_mapping_leaves_holes_and_inverse_does_not():
    img = [[10, 20, 30], [40, 50, 60], [70, 80, 90]]
    out, holes = forward_warp(img, 4, 4, affine(F(3, 2), 0, 0, 0, F(3, 2), 0))
    assert out == [[10, 0, 20, 30], [0, 0, 0, 0], [40, 0, 50, 60], [70, 0, 80, 90]]
    assert sum(map(sum, holes)) == 7
    inv = inverse_warp(img, 4, 4, affine(F(2, 3), 0, 0, 0, F(2, 3), 0), fill=-1)
    assert inv[0] == [10, F(50, 3), F(70, 3), 30]
    assert inv[3] == [70, F(230, 3), F(250, 3), 90]
    assert all(v != -1 for r in inv for v in r)


def test_rotation_example():
    n = 16
    img = [[(x * 16 + y) % 256 for x in range(n)] for y in range(n)]
    coef = rotation_about(7.5, 7.5, math.radians(30))
    inv = invert_affine(*coef)
    _, holes = forward_warp(img, n, n, affine(*coef), fill=-1)
    covered = [(u, v) for v in range(n) for u in range(n)
               if 0 <= inv(u, v)[0] <= n - 1 and 0 <= inv(u, v)[1] <= n - 1]
    assert len(covered) == 200
    assert sum(holes[v][u] for u, v in covered) == 24
    hits = {}
    for y in range(n):
        for x in range(n):
            u, v = affine(*coef)(x, y)
            key = (math.floor(u + 0.5), math.floor(v + 0.5))
            if 0 <= key[0] < n and 0 <= key[1] < n:
                hits[key] = hits.get(key, 0) + 1
    assert sorted(set(hits.values())) == [1, 2] and list(hits.values()).count(2) == 24
    out = inverse_warp(img, n, n, inv, fill=-1)
    assert all(out[v][u] != -1 for u, v in covered)


def test_affine_inverse_and_homography():
    rng = random.Random(11)
    done = 0
    while done < 200:
        coef = [rand_frac(rng, -3, 3) for _ in range(6)]
        if coef[0] * coef[4] - coef[1] * coef[3] == 0:
            continue
        fwd, inv = affine(*coef), invert_affine(*coef)
        x, y = rand_frac(rng, -5, 5), rand_frac(rng, -5, 5)
        assert inv(*fwd(x, y)) == (x, y)
        hm = homography([[coef[0], coef[1], coef[2]], [coef[3], coef[4], coef[5]], [0, 0, 1]])
        assert hm(x, y) == fwd(x, y)
        done += 1
    with pytest.raises(ValueError):
        invert_affine(1, 2, 0, 2, 4, 0)
    with pytest.raises(ValueError):
        inverse_warp([], 1, 1, lambda u, v: (u, v))
