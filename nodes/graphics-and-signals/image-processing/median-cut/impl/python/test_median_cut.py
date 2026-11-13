# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/median-cut/. The authors are listed in prov/FCH3KR.jsonl.

import random
from collections import Counter
from fractions import Fraction as F

from median_cut import box_mean, median_cut, palette, quantize, squared_distance, total_error


def partitions(items, k):
    """All partitions of the list items into at most k nonempty groups."""
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in partitions(rest, k):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1 :]
        if len(p) < k:
            yield [[first]] + p


def best_error(colors, k):
    """The least total squared error of any palette of at most k colors, by trying every partition."""
    count = Counter(colors)
    best = None
    for p in partitions(list(count), k):
        e = 0
        for group in p:
            pixels = [c for c in group for _ in range(count[c])]
            m = box_mean(pixels)
            e += sum(squared_distance(c, m) for c in pixels)
        best = e if best is None else min(best, e)
    return best


def random_image(rng, n, top):
    return [tuple(rng.randrange(top) for _ in range(3)) for _ in range(n)]


def test_palette_size_is_k_or_the_number_of_distinct_colors() -> None:
    rng = random.Random(8)
    for _ in range(300):
        colors = random_image(rng, rng.randrange(1, 60), rng.choice([2, 4, 256]))
        k = rng.randrange(1, 40)
        boxes = median_cut(colors, k)
        pal = palette(boxes)
        assert len(pal) == min(k, len(set(colors)))
        assert len(set(pal)) == len(pal)
        # the boxes split the pixels, and no color is in two boxes
        assert sorted(c for box in boxes for c in box) == sorted(colors)
        owners = {}
        for j, box in enumerate(boxes):
            for c in box:
                assert owners.setdefault(c, j) == j


def test_split_at_the_median_halves_distinct_values() -> None:
    rng = random.Random(8)
    for n in range(2, 40):
        reds = rng.sample(range(256), n)
        colors = [(r, rng.randrange(4), rng.randrange(4)) for r in reds]
        left, right = median_cut(colors, 2)
        assert (len(left), len(right)) == (n // 2, n - n // 2)
        assert max(c[0] for c in left) < min(c[0] for c in right)


def test_example_from_the_page() -> None:
    colors = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (100, 0, 0)]
    assert median_cut(colors, 2) == [[(0, 0, 0), (1, 0, 0)], [(2, 0, 0), (3, 0, 0), (100, 0, 0)]]
    pal, index = quantize(colors, 2)
    assert pal == [(F(1, 2), 0, 0), (35, 0, 0)]
    assert index == [0, 0, 0, 0, 1]
    assert total_error(colors, pal, index) == 4234
    assert best_error(colors, 2) == 5


def test_the_error_ratio_is_not_bounded() -> None:
    for m in range(12, 300):
        colors = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (m, 0, 0)]
        pal, index = quantize(colors, 2)
        assert total_error(colors, pal, index) == 9 + F(2 * m - 5, 3) ** 2
        assert best_error(colors, 2) == 5


def test_never_better_than_the_exhaustive_best_and_often_worse() -> None:
    rng = random.Random(8)
    worse = 0
    for _ in range(200):
        colors = random_image(rng, rng.randrange(3, 9), 16)
        k = rng.randrange(2, 4)
        pal, index = quantize(colors, k)
        e, b = total_error(colors, pal, index), best_error(colors, k)
        assert e >= b
        worse += e > b
    assert worse == 130


def test_nearest_mapping_is_no_worse_than_box_mapping() -> None:
    rng = random.Random(8)
    for _ in range(100):
        colors = random_image(rng, 50, 64)
        boxes = median_cut(colors, 6)
        pal = palette(boxes)
        by_box = sum(squared_distance(c, pal[j]) for j, box in enumerate(boxes) for c in box)
        _, index = quantize(colors, 6)
        assert total_error(colors, pal, index) <= by_box
