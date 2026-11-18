# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/percentage-closer-filtering/. The authors are listed in prov/CF3C6M.jsonl.

import random
from fractions import Fraction

from percentage_closer_filtering import (
    box_kernel,
    box_scene,
    filter_depths_then_compare,
    lit_tap,
    pcf,
    pcf_bilinear,
    tent_kernel,
)

HALF = Fraction(1, 2)


def random_map(rng, w, h):
    return [[Fraction(rng.randrange(0, 17), 16) for _ in range(w)] for _ in range(h)]


def summed_area(img):
    h, w = len(img), len(img[0])
    t = [[0] * (w + 1) for _ in range(h + 1)]
    for j in range(h):
        row = 0
        for i in range(w):
            row += img[j][i]
            t[j + 1][i + 1] = t[j][i + 1] + row
    return t


def test_example_on_the_page():
    s = box_scene(8, 8, Fraction(8, 10), Fraction(3, 10), 2, 2, 6, 6)
    z = Fraction(8, 10)
    # Just outside the box edge, one column of the 3 x 3 box is shadowed.
    assert pcf(s, Fraction(13, 2), Fraction(7, 2), z, 0, box_kernel(1)) == Fraction(2, 3)
    # Diagonally outside the box corner, 1 of 9 taps is shadowed.
    assert pcf(s, Fraction(13, 2), Fraction(13, 2), z, 0, box_kernel(1)) == Fraction(8, 9)
    assert pcf(s, Fraction(11, 2), Fraction(11, 2), z, 0, box_kernel(1)) == Fraction(5, 9)
    assert pcf(s, Fraction(11, 2), Fraction(7, 2), z, 0, box_kernel(1)) == Fraction(1, 3)
    # Filtering the depths first gives a hard 0 or 1.
    assert filter_depths_then_compare(s, Fraction(13, 2), Fraction(7, 2), z, 0, 1) == 0
    assert filter_depths_then_compare(s, Fraction(11, 2), Fraction(7, 2), z, 0, 1) == 0


def test_box_pcf_equals_summed_area_count():
    rng = random.Random(1)
    for _ in range(40):
        w, h = rng.randrange(4, 13), rng.randrange(4, 13)
        s = random_map(rng, w, h)
        z = Fraction(rng.randrange(0, 17), 16)
        b = Fraction(rng.randrange(0, 3), 32)
        lit = [[1 if z - b <= s[j][i] else 0 for i in range(w)] for j in range(h)]
        t = summed_area(lit)
        for r in range(3):
            for _ in range(10):
                i, j = rng.randrange(w), rng.randrange(h)
                x0, x1 = max(i - r, 0), min(i + r + 1, w)
                y0, y1 = max(j - r, 0), min(j + r + 1, h)
                inside = t[y1][x1] - t[y0][x1] - t[y1][x0] + t[y0][x0]
                outside = (2 * r + 1) ** 2 - (x1 - x0) * (y1 - y0)
                want = Fraction(inside + outside, (2 * r + 1) ** 2)
                assert pcf(s, i + HALF, j + HALF, z, b, box_kernel(r)) == want


def test_weighted_pcf_equals_brute_force_average():
    rng = random.Random(2)
    for _ in range(200):
        w, h = rng.randrange(3, 10), rng.randrange(3, 10)
        s = random_map(rng, w, h)
        z = Fraction(rng.randrange(0, 17), 16)
        x = Fraction(rng.randrange(0, 16 * w), 16)
        y = Fraction(rng.randrange(0, 16 * h), 16)
        r = rng.randrange(0, 3)
        k = tent_kernel(r)
        num = den = 0
        for (u, v), wt in k.items():
            i, j = int(x) + u, int(y) + v
            inside = 0 <= i < w and 0 <= j < h
            num += wt * (1 if not inside or z <= s[j][i] else 0)
            den += wt
        assert pcf(s, x, y, z, 0, k) == Fraction(num, den)


def test_radius_zero_is_the_binary_test():
    rng = random.Random(3)
    for _ in range(300):
        s = random_map(rng, 6, 5)
        z = Fraction(rng.randrange(0, 17), 16)
        x, y = Fraction(rng.randrange(0, 96), 16), Fraction(rng.randrange(0, 80), 16)
        want = 0 if z > s[int(y)][int(x)] else 1
        assert pcf(s, x, y, z, 0, box_kernel(0)) == want


def test_range_and_monotone_in_depth():
    rng = random.Random(4)
    for _ in range(60):
        s = random_map(rng, 8, 8)
        x, y = Fraction(rng.randrange(0, 128), 16), Fraction(rng.randrange(0, 128), 16)
        prev = None
        for zz in range(0, 18):
            z = Fraction(zz, 16)
            v = pcf(s, x, y, z, 0, box_kernel(2))
            assert 0 <= v <= 1
            if prev is not None:
                assert v <= prev
            prev = v
        assert prev == 0 or (x < 2 or y < 2 or x >= 6 or y >= 6)


def test_bilinear_pcf_is_the_box_integral_of_the_nearest_texel_test():
    rng = random.Random(5)
    n = 16
    for _ in range(80):
        s = random_map(rng, 6, 6)
        z = Fraction(rng.randrange(0, 17), 16)
        x = Fraction(rng.randrange(16, 80), 16)
        y = Fraction(rng.randrange(16, 80), 16)
        total = 0
        for a in range(n):
            for c in range(n):
                px = x - HALF + Fraction(2 * a + 1, 2 * n)
                py = y - HALF + Fraction(2 * c + 1, 2 * n)
                total += lit_tap(s, int(px), int(py), z, 0)
        assert pcf_bilinear(s, x, y, z, 0) == Fraction(total, n * n)


def test_bilinear_pcf_at_texel_centers_is_the_binary_test():
    rng = random.Random(6)
    s = random_map(rng, 7, 7)
    for j in range(7):
        for i in range(7):
            z = Fraction(rng.randrange(0, 17), 16)
            assert pcf_bilinear(s, i + HALF, j + HALF, z, 0) == lit_tap(s, i, j, z, 0)


def test_bias_moves_the_test():
    s = [[Fraction(1, 2)]]
    assert pcf(s, HALF, HALF, Fraction(9, 16), 0, box_kernel(0)) == 0
    assert pcf(s, HALF, HALF, Fraction(9, 16), Fraction(1, 16), box_kernel(0)) == 1
