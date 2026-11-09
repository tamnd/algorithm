# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/offline-orthogonal-range-counting/. The authors are listed in prov/V3ZHMG.jsonl.

import random
from fractions import Fraction

from offline_orthogonal_range_counting import offline_range_count


def scan(points, box):
    x1, x2, y1, y2 = box
    return sum(1 for p in points if x1 <= p[0] <= x2 and y1 <= p[1] <= y2)


EXAMPLE = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (3, 8), (6, 6)]


def test_worked_example():
    st = {}
    assert offline_range_count(EXAMPLE, [(3, 7, 2, 6), (6, 9, 1, 6)], st) == [3, 4]
    assert st["events"] == 12 and st["reads"] == 4


def test_empty_inputs():
    assert offline_range_count([], []) == []
    assert offline_range_count([], [(0, 9, 0, 9)]) == [0]
    assert offline_range_count([(1, 1)], []) == []
    assert offline_range_count([(1, 1)], [(1, 1, 1, 1), (0, 0, 0, 9), (2, 0, 0, 9), (0, 9, 2, 0)]) == [1, 0, 0, 0]


def test_duplicates_and_boundary():
    pts = [(2, 5), (2, 5), (2, 5), (1, 5), (3, 5), (2, 4)]
    boxes = [(2, 2, 5, 5), (2, 2, 4, 5), (1, 3, 5, 5), (2, 3, 0, 4), (3, 3, 5, 5), (1, 1, 1, 9)]
    assert offline_range_count(pts, boxes) == [scan(pts, b) for b in boxes] == [3, 4, 5, 1, 1, 1]


def test_fractions():
    pts = [(Fraction(i, 3), Fraction((5 * i) % 11, 4)) for i in range(25)]
    boxes = [(Fraction(1, 2), Fraction(6), Fraction(3, 4), Fraction(2)), (Fraction(0), Fraction(8), Fraction(0), Fraction(5, 2))]
    assert offline_range_count(pts, boxes) == [scan(pts, b) for b in boxes]


def test_random_against_scan():
    rng = random.Random(2024)
    for trial in range(800):
        n = rng.randint(0, 30)
        c = rng.choice([2, 8, 40])
        pts = [(rng.randint(0, c), rng.randint(0, c)) for _ in range(n)]
        boxes = []
        for _ in range(rng.randint(0, 8)):
            boxes.append((rng.randint(-1, c + 1), rng.randint(-1, c + 1),
                          rng.randint(-1, c + 1), rng.randint(-1, c + 1)))
        assert offline_range_count(pts, boxes) == [scan(pts, b) for b in boxes]


def test_large_matches_scan():
    rng = random.Random(3)
    pts = [(rng.randint(0, 1000), rng.randint(0, 1000)) for _ in range(2000)]
    boxes = []
    for _ in range(200):
        x1, x2 = sorted(rng.randint(0, 1000) for _ in range(2))
        y1, y2 = sorted(rng.randint(0, 1000) for _ in range(2))
        boxes.append((x1, x2, y1, y2))
    st = {}
    assert offline_range_count(pts, boxes, st) == [scan(pts, b) for b in boxes]
    assert st["reads"] == 2 * len(boxes)
