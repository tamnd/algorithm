# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/integral-image/. The authors are listed in prov/863FHC.jsonl.

import random
from fractions import Fraction as F

from integral_image import IntegralImage, local_variance

EXAMPLE = [
    [3, 1, 4, 1],
    [5, 9, 2, 6],
    [5, 3, 5, 8],
]


def direct_rect(image, x0, y0, x1, y1):
    return sum(image[y][x] for y in range(y0, y1) for x in range(x0, x1))


def test_example_table_and_queries() -> None:
    ii = IntegralImage(EXAMPLE)
    assert ii.table == [
        [0, 0, 0, 0, 0],
        [0, 3, 4, 8, 9],
        [0, 8, 18, 24, 31],
        [0, 13, 26, 37, 52],
    ]
    assert ii.rect_sum(1, 1, 3, 3) == 9 + 2 + 3 + 5 == 19
    assert ii.rect_sum(0, 0, 4, 3) == 52
    assert ii.box_mean(0, 0, 1) == F(18, 4)
    assert ii.box_mean(1, 1, 1) == F(37, 9)
    assert ii.check_invariant(EXAMPLE)


def test_edges() -> None:
    ii = IntegralImage([])
    assert ii.table == [[0]]
    one = IntegralImage([[7]])
    assert one.rect_sum(0, 0, 1, 1) == 7
    assert one.rect_sum(1, 0, 1, 1) == 0
    assert one.box_mean(0, 0, 5) == 7
    for bad in ((0, 0, 2, 1), (1, 0, 0, 1), (-1, 0, 1, 1)):
        try:
            one.rect_sum(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError(bad)


def test_random_rectangles_against_direct() -> None:
    rng = random.Random(1984)
    for _ in range(300):
        h, w = rng.randint(1, 8), rng.randint(1, 8)
        img = [[rng.randint(-255, 255) for _ in range(w)] for _ in range(h)]
        ii = IntegralImage(img)
        assert ii.check_invariant(img)
        for _ in range(10):
            x0, x1 = sorted(rng.randint(0, w) for _ in range(2))
            y0, y1 = sorted(rng.randint(0, h) for _ in range(2))
            assert ii.rect_sum(x0, y0, x1, y1) == direct_rect(img, x0, y0, x1, y1)


def test_box_filter_against_direct_truncated_mean() -> None:
    rng = random.Random(7)
    for _ in range(150):
        h, w, r = rng.randint(1, 7), rng.randint(1, 7), rng.randint(0, 4)
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        got = IntegralImage(img).box_filter(r)
        for y in range(h):
            for x in range(w):
                cells = [img[j][i] for j in range(max(0, y - r), min(h, y + r + 1))
                         for i in range(max(0, x - r), min(w, x + r + 1))]
                assert got[y][x] == F(sum(cells), len(cells))


def test_modular_table_gives_exact_small_sums() -> None:
    rng = random.Random(32)
    m = 2 ** 12
    for _ in range(100):
        h, w = rng.randint(1, 30), rng.randint(1, 30)
        img = [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]
        ii = IntegralImage(img, modulus=m)
        assert all(0 <= v < m for row in ii.table for v in row)
        for _ in range(20):
            x0 = rng.randint(0, w - 1)
            y0 = rng.randint(0, h - 1)
            x1 = min(w, x0 + rng.randint(1, 4))
            y1 = min(h, y0 + rng.randint(1, 4))
            true = direct_rect(img, x0, y0, x1, y1)
            assert true < m
            assert ii.rect_sum(x0, y0, x1, y1) == true


def test_local_variance_against_direct() -> None:
    rng = random.Random(99)
    for _ in range(60):
        h, w, r = rng.randint(1, 6), rng.randint(1, 6), rng.randint(0, 2)
        img = [[rng.randint(0, 20) for _ in range(w)] for _ in range(h)]
        var = local_variance(img, r)
        for y in range(h):
            for x in range(w):
                cells = [F(img[j][i]) for j in range(max(0, y - r), min(h, y + r + 1))
                         for i in range(max(0, x - r), min(w, x + r + 1))]
                mu = sum(cells) / len(cells)
                assert var[y][x] == sum((c - mu) ** 2 for c in cells) / len(cells)
