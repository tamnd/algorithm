# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ordered-dithering/. The authors are listed in prov/ZXEC5M.jsonl.

import random
from fractions import Fraction as F

from ordered_dithering import bayer, ordered_dither, thresholds

SIZES = (1, 2, 4, 8, 16)


def interleaved(x, y, k):
    """Bayer index by its digits: the lowest binary digits of x and y give the highest base-4 digit."""
    v = 0
    for i in range(k):
        xi, yi = (x >> i) & 1, (y >> i) & 1
        v = 4 * v + 2 * (xi ^ yi) + yi
    return v


def test_each_threshold_appears_once() -> None:
    for n in SIZES:
        m = bayer(n)
        assert sorted(v for row in m for v in row) == list(range(n * n))


def test_small_matrices() -> None:
    assert bayer(2) == [[0, 2], [3, 1]]
    assert bayer(4) == [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def test_recursion_equals_the_digit_formula() -> None:
    for k, n in enumerate(SIZES):
        m = bayer(n)
        assert all(m[y][x] == interleaved(x, y, k) for y in range(n) for x in range(n))


def test_constant_gray_gives_k_ones_in_every_tile() -> None:
    for n in (2, 4, 8):
        for k in range(n * n + 1):
            g = F(k, n * n)
            out = ordered_dither([[g] * (3 * n) for _ in range(2 * n)], n)
            for ty in range(2):
                for tx in range(3):
                    ones = sum(out[ty * n + y][tx * n + x] for y in range(n) for x in range(n))
                    assert ones == k


def test_any_gray_against_a_direct_count() -> None:
    rng = random.Random(8)
    for n in (2, 4, 8, 16):
        t = thresholds(n)
        for _ in range(40):
            g = F(rng.randrange(0, 1001), 1000)
            out = ordered_dither([[g] * n for _ in range(n)], n)
            ones = sum(map(sum, out))
            assert ones == sum(1 for row in t for th in row if g > th)
            # the count is g n^2 rounded to the nearest integer, a half going down
            assert abs(ones - g * n * n) <= F(1, 2)


def test_low_levels_are_spread_on_a_lattice() -> None:
    for k, n in enumerate(SIZES):
        m = bayer(n)
        for j in range(k + 1):
            step = 2**j
            below = {(x, y) for y in range(n) for x in range(n) if m[y][x] < n * n // 4**j}
            assert below == {(x, y) for y in range(0, n, step) for x in range(0, n, step)}
    # level 1/2 is a checkerboard
    out = ordered_dither([[F(1, 2)] * 8 for _ in range(8)], 8)
    assert out == [[(x + y + 1) % 2 for x in range(8)] for y in range(8)]


def test_example_from_the_page() -> None:
    out = ordered_dither([[F(5, 16)] * 4 for _ in range(4)], 4)
    assert out == [[1, 0, 1, 0], [0, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 0]]
    # a value of exactly a threshold stays off: 1/32 is the threshold of index 0
    assert ordered_dither([[F(1, 32)]], 4) == [[0]]
    assert ordered_dither([[F(1, 32) + F(1, 1000)]], 4) == [[1]]
