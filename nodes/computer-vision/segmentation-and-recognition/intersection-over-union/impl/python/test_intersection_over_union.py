# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/intersection-over-union/. The authors are listed in prov/20CWE7.jsonl.

import random
from fractions import Fraction

from intersection_over_union import (box_area, box_pixels, giou, intersection_area,
                                     intersection_over_min, iou, iou_matrix,
                                     jaccard_distance, mask_iou)


def random_box(rng, size=8):
    x1, x2 = sorted(rng.sample(range(size + 1), 2))
    y1, y2 = sorted(rng.sample(range(size + 1), 2))
    return (x1, y1, x2, y2)


def test_check_values():
    assert iou((0, 0, 2, 2), (1, 1, 3, 3)) == Fraction(1, 7)
    assert iou((0, 0, 10, 10), (5, 0, 15, 10)) == Fraction(1, 3)
    assert iou((0, 0, 3, 3), (1, 0, 4, 3)) == Fraction(1, 2)
    assert iou((0, 0, 10, 10), (0, 0, 7, 7)) == Fraction(49, 100)


def test_inclusive_pixel_form():
    # VOC devkit form: corners are inclusive pixel indices.
    assert iou((0, 0, 2, 2), (1, 1, 3, 3), inclusive=True) == Fraction(2, 7)
    assert iou((0, 0, 10, 10), (5, 0, 15, 10), inclusive=True) == Fraction(3, 8)
    rng = random.Random(3)
    for _ in range(200):
        a, b = random_box(rng), random_box(rng)
        grow = lambda r: (r[0], r[1], r[2] + 1, r[3] + 1)
        assert iou(a, b, inclusive=True) == iou(grow(a), grow(b))


def test_against_pixel_sets():
    rng = random.Random(1)
    for _ in range(300):
        a, b = random_box(rng), random_box(rng)
        assert intersection_area(a, b) == len(box_pixels(a) & box_pixels(b))
        assert iou(a, b) == mask_iou(box_pixels(a), box_pixels(b))


def test_range_symmetry_and_identity():
    rng = random.Random(2)
    for _ in range(300):
        a, b = random_box(rng), random_box(rng)
        v = iou(a, b)
        assert 0 <= v <= 1
        assert v == iou(b, a)
        assert iou(a, a) == 1
        if v == 1:
            assert a == b


def test_jaccard_distance_triangle_inequality():
    rng = random.Random(4)
    for _ in range(2000):
        a, b, c = random_box(rng, 6), random_box(rng, 6), random_box(rng, 6)
        assert jaccard_distance(a, c) <= jaccard_distance(a, b) + jaccard_distance(b, c)


def test_translation_and_scale_invariance():
    rng = random.Random(5)
    for _ in range(200):
        a, b = random_box(rng), random_box(rng)
        dx, dy, s = rng.randint(-5, 5), rng.randint(-5, 5), rng.randint(1, 4)
        move = lambda r: (s * r[0] + dx, s * r[1] + dy, s * r[2] + dx, s * r[3] + dy)
        assert iou(move(a), move(b)) == iou(a, b)


def test_floats():
    v = iou((0.0, 0.0, 2.0, 2.0), (1.0, 1.0, 3.0, 3.0))
    assert abs(v - 1.0 / 7.0) < 1e-15


def test_empty_union():
    assert iou((1, 1, 1, 1), (2, 2, 2, 2)) == 0
    assert iou((1, 1, 1, 1), (2, 2, 2, 2), empty=1) == 1
    assert box_area((3, 3, 1, 5)) == 0


def test_giou():
    assert giou((0, 0, 1, 1), (2, 0, 3, 1)) == Fraction(-1, 3)
    assert giou((0, 0, 1, 1), (5, 0, 6, 1)) == Fraction(-2, 3)
    assert giou((0, 0, 2, 2), (1, 1, 3, 3)) == Fraction(-5, 63)
    rng = random.Random(6)
    for _ in range(300):
        a, b = random_box(rng), random_box(rng)
        g = giou(a, b)
        assert -1 < g <= iou(a, b) <= 1
        inside = a[0] <= b[0] and a[1] <= b[1] and b[2] <= a[2] and b[3] <= a[3]
        if inside:
            assert g == iou(a, b)


def test_coverage_is_not_iou():
    big, small = (0, 0, 10, 10), (2, 2, 6, 6)
    assert intersection_over_min(big, small) == 1
    assert iou(big, small) == Fraction(4, 25)


def test_matrix():
    m = iou_matrix([(0, 0, 2, 2), (0, 0, 10, 10)], [(1, 1, 3, 3), (5, 0, 15, 10)])
    assert m[0][0] == Fraction(1, 7) and m[1][1] == Fraction(1, 3)
    assert m[0][1] == 0
