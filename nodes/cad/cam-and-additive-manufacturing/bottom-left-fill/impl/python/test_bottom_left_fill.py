# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bottom-left-fill/. The authors are listed in prov/28CHNP.jsonl.

import random
from fractions import Fraction

import pytest

from bottom_left_fill import bottom_left_fill, overlap, place_one, strip_height


def brute_place(width, placed, w, h):
    """Least (y, x) over every integer position, by a direct overlap test."""
    top = sum(ph for (_, _, _, ph) in placed)
    for y in range(top + 1):
        for x in range(width - w + 1):
            r = (x, y, w, h)
            if not any(overlap(r, p) for p in placed):
                return x, y
    raise AssertionError("no position found")


def check_packing(width, rects, pos):
    boxes = [(x, y, w, h) for (w, h), (x, y) in zip(rects, pos)]
    for (x, y, w, h) in boxes:
        assert 0 <= x and x + w <= width and 0 <= y
    for i in range(len(boxes)):
        for j in range(i):
            assert not overlap(boxes[i], boxes[j])


def test_example():
    rects = [(2, 4), (6, 1), (2, 4), (10, 2), (5, 3)]
    pos = bottom_left_fill(10, rects)
    assert pos == [(0, 0), (2, 0), (8, 0), (0, 4), (2, 1)]
    assert strip_height(rects, pos) == 6
    check_packing(10, rects, pos)


def test_small_cases():
    assert bottom_left_fill(5, []) == []
    assert bottom_left_fill(5, [(5, 1)]) == [(0, 0)]
    assert bottom_left_fill(4, [(2, 1)] * 4) == [(0, 0), (2, 0), (0, 1), (2, 1)]
    # touching edges are allowed, so the second square sits right next to the first
    assert bottom_left_fill(2, [(1, 1), (1, 1), (2, 1)]) == [(0, 0), (1, 0), (0, 1)]
    with pytest.raises(ValueError):
        bottom_left_fill(3, [(4, 1)])
    with pytest.raises(ValueError):
        bottom_left_fill(3, [(1, 0)])


def test_hole_is_filled():
    # a lid on two posts leaves a closed hole; the last rectangle goes into it
    rects = [(1, 3), (3, 1), (1, 3), (5, 1), (1, 2)]
    pos = bottom_left_fill(5, rects)
    assert pos[:4] == [(0, 0), (1, 0), (4, 0), (0, 3)]
    assert pos[4] == (1, 1)
    check_packing(5, rects, pos)


def test_against_brute_force():
    rng = random.Random(28)
    for _ in range(400):
        width = rng.randint(2, 8)
        n = rng.randint(1, 7)
        rects = [(rng.randint(1, width), rng.randint(1, 4)) for _ in range(n)]
        pos = bottom_left_fill(width, rects)
        check_packing(width, rects, pos)
        placed = []
        for (w, h), p in zip(rects, pos):
            assert p == brute_place(width, placed, w, h)
            placed.append((p[0], p[1], w, h))


def test_fractions_scale():
    rng = random.Random(7)
    s = Fraction(2, 3)
    for _ in range(100):
        width = rng.randint(2, 7)
        rects = [(rng.randint(1, width), rng.randint(1, 3)) for _ in range(rng.randint(1, 6))]
        pos = bottom_left_fill(width, rects)
        pos_s = bottom_left_fill(width * s, [(w * s, h * s) for (w, h) in rects])
        assert pos_s == [(x * s, y * s) for (x, y) in pos]


def test_place_one_is_lowest_then_leftmost():
    rng = random.Random(3)
    for _ in range(200):
        width = rng.randint(3, 8)
        placed = []
        for (w, h) in [(rng.randint(1, width), rng.randint(1, 3)) for _ in range(5)]:
            x, y = place_one(width, placed, w, h)
            # no feasible integer position is lower, or as low and further left
            for yy in range(y + 1):
                for xx in range(width - w + 1):
                    if (yy, xx) < (y, x):
                        assert any(overlap((xx, yy, w, h), p) for p in placed)
            placed.append((x, y, w, h))
