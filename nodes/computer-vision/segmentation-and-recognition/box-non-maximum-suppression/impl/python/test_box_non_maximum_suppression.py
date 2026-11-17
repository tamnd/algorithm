# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/box-non-maximum-suppression/. The authors are listed in prov/5JRR0P.jsonl.

import random
from fractions import Fraction

from box_non_maximum_suppression import (batched_nms, brute_force_nms, coverage,
                                         fast_nms, greedy_nms, iou,
                                         is_greedy_nms_output)

EXAMPLE_BOXES = [(0, 0, 10, 10), (1, 1, 11, 11), (6, 0, 16, 10), (20, 20, 30, 30), (7, 1, 17, 11)]
EXAMPLE_SCORES = [0.9, 0.8, 0.75, 0.6, 0.5]


def random_instance(rng, n, size=20):
    boxes = []
    for _ in range(n):
        x, y = rng.randint(0, size), rng.randint(0, size)
        w, h = rng.randint(2, 8), rng.randint(2, 8)
        boxes.append((x, y, x + w, y + h))
    scores = [rng.randint(0, 5) for _ in range(n)]  # many ties on purpose
    return boxes, scores


def test_iou_check_values():
    assert iou((0, 0, 2, 2), (1, 1, 3, 3)) == Fraction(1, 7)
    assert iou((0, 0, 10, 10), (5, 0, 15, 10)) == Fraction(1, 3)


def test_page_example():
    b, s = EXAMPLE_BOXES, EXAMPLE_SCORES
    assert iou(b[0], b[1]) == Fraction(81, 119)
    assert iou(b[0], b[2]) == Fraction(1, 4)
    assert iou(b[2], b[4]) == Fraction(81, 119)
    assert iou(b[0], b[4]) == Fraction(27, 173)
    assert greedy_nms(b, s, 0.5) == [0, 2, 3]
    # A lower threshold removes box 2, and then box 4 survives: the kept set
    # does not shrink monotonically as the threshold goes down.
    assert greedy_nms(b, s, 0.2) == [0, 3, 4]
    # Threshold 1: nothing is removed; the output is the rank order.
    assert greedy_nms(b, s, 1) == [0, 1, 2, 3, 4]


def test_removed_boxes_do_not_suppress():
    # Box 1 is removed by box 0; box 2 overlaps box 1 a lot but not box 0.
    boxes = [(0, 0, 10, 10), (5, 0, 15, 10), (9, 0, 19, 10)]
    scores = [3, 2, 1]
    assert iou(boxes[0], boxes[1]) == Fraction(1, 3)
    assert iou(boxes[1], boxes[2]) == Fraction(3, 7)
    assert iou(boxes[0], boxes[2]) == Fraction(1, 19)
    assert greedy_nms(boxes, scores, Fraction(3, 10)) == [0, 2]
    # Fast NMS lets the removed box 1 remove box 2.
    assert fast_nms(boxes, scores, Fraction(3, 10)) == [0]


def test_matches_brute_force():
    rng = random.Random(7)
    for trial in range(150):
        n = rng.randint(0, 8)
        boxes, scores = random_instance(rng, n)
        t = rng.choice([Fraction(1, 10), Fraction(3, 10), Fraction(1, 2), Fraction(7, 10)])
        keep = greedy_nms(boxes, scores, t)
        assert keep == brute_force_nms(boxes, scores, t)


def test_characterization_on_larger_inputs():
    rng = random.Random(8)
    for trial in range(40):
        boxes, scores = random_instance(rng, 40, size=30)
        keep = greedy_nms(boxes, scores, Fraction(1, 2))
        assert is_greedy_nms_output(boxes, scores, keep, Fraction(1, 2))
        # Kept boxes are pairwise below or at the threshold.
        for a in range(len(keep)):
            for b in range(a + 1, len(keep)):
                assert iou(boxes[keep[a]], boxes[keep[b]]) <= Fraction(1, 2)


def test_fast_nms_removes_a_superset():
    rng = random.Random(9)
    for trial in range(60):
        boxes, scores = random_instance(rng, 15)
        g = set(greedy_nms(boxes, scores, Fraction(1, 2)))
        f = set(fast_nms(boxes, scores, Fraction(1, 2)))
        assert f <= g


def test_monotone_in_threshold_for_the_first_box_only():
    # The best box is always kept, whatever the threshold.
    rng = random.Random(10)
    for trial in range(50):
        boxes, scores = random_instance(rng, 10)
        best = min(range(10), key=lambda i: (-scores[i], i))
        for t in (0, Fraction(1, 4), Fraction(1, 2), 1):
            assert greedy_nms(boxes, scores, t)[0] == best


def test_batched_nms_per_class():
    boxes = [(0, 0, 10, 10), (1, 1, 11, 11), (0, 0, 10, 10)]
    scores = [0.9, 0.8, 0.7]
    labels = ["person", "person", "dog"]
    assert batched_nms(boxes, scores, labels, 0.5) == [0, 2]
    assert greedy_nms(boxes, scores, 0.5) == [0]


def test_coverage_overlap():
    big, small = (0, 0, 10, 10), (2, 2, 6, 6)
    assert coverage(big, small) == 1
    assert coverage(small, big) == Fraction(16, 100)
    # With coverage, a high-scoring big box removes a small box inside it.
    assert greedy_nms([big, small], [2, 1], Fraction(1, 2), overlap=coverage) == [0]
    assert greedy_nms([big, small], [2, 1], Fraction(1, 2)) == [0, 1]


def test_max_keep_and_floats():
    boxes = [(0.0, 0.0, 1.0, 1.0), (2.0, 2.0, 3.0, 3.0), (0.1, 0.0, 1.1, 1.0)]
    assert greedy_nms(boxes, [0.3, 0.2, 0.25], 0.5) == [0, 1]
    assert greedy_nms(boxes, [0.3, 0.2, 0.25], 0.5, max_keep=1) == [0]


def test_worst_case_counts_all_pairs():
    calls = [0]

    def counting_iou(a, b):
        calls[0] += 1
        return iou(a, b)

    n = 30
    boxes = [(3 * i, 0, 3 * i + 2, 2) for i in range(n)]  # pairwise disjoint
    keep = greedy_nms(boxes, list(range(n, 0, -1)), 0.5, overlap=counting_iou)
    assert keep == list(range(n))
    assert calls[0] == n * (n - 1) // 2
