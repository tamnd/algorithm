# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mean-intersection-over-union/. The authors are listed in prov/7XWT5K.jsonl.

import random
from fractions import Fraction

from mean_intersection_over_union import (VOID, class_iou, confusion_matrix, dice, frequency_weighted_iou,
                                          mean_accuracy, mean_iou, per_image_mean_iou, pixel_accuracy)

GT = [[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 2, 2], [VOID, 0, 2, 2]]
PRED = [[0, 0, 0, 1], [0, 1, 1, 1], [0, 0, 2, 2], [2, 0, 0, 2]]


def random_pair(rng, k, w, h, void_rate=0.1):
    gt = [[VOID if rng.random() < void_rate else rng.randrange(k) for _ in range(w)] for _ in range(h)]
    pred = [[rng.randrange(k) for _ in range(w)] for _ in range(h)]
    return gt, pred


def jaccard_by_sets(pairs, k, i):
    """IoU of class i from pixel sets, keyed by (image, u, v)."""
    g, p = set(), set()
    for idx, (gt, pred) in enumerate(pairs):
        for v, row in enumerate(gt):
            for u, lab in enumerate(row):
                if lab == VOID:
                    continue
                if lab == i:
                    g.add((idx, u, v))
                if pred[v][u] == i:
                    p.add((idx, u, v))
    union = g | p
    return Fraction(len(g & p), len(union)) if union else None


def test_page_example():
    n = confusion_matrix([(GT, PRED)], 3)
    assert n == [[6, 1, 0], [1, 3, 0], [1, 0, 3]]
    assert class_iou(n) == [Fraction(2, 3), Fraction(3, 5), Fraction(3, 4)]
    assert mean_iou(n) == Fraction(121, 180)
    assert pixel_accuracy(n) == Fraction(4, 5)
    assert mean_accuracy(n) == Fraction(11, 14)
    assert frequency_weighted_iou(n) == Fraction(151, 225)


def test_matches_set_jaccard():
    rng = random.Random(31)
    for _ in range(20):
        k = rng.randrange(2, 6)
        pairs = [random_pair(rng, k, rng.randrange(1, 9), rng.randrange(1, 9)) for _ in range(rng.randrange(1, 4))]
        n = confusion_matrix(pairs, k)
        ious = class_iou(n)
        for i in range(k):
            assert ious[i] == jaccard_by_sets(pairs, k, i)
        defined = [x for x in ious if x is not None]
        assert mean_iou(n) == sum(defined, Fraction(0)) / len(defined)


def test_void_is_ignored_and_order_does_not_matter():
    rng = random.Random(32)
    pairs = [random_pair(rng, 4, 6, 5, void_rate=0.3) for _ in range(4)]
    n = confusion_matrix(pairs, 4)
    assert sum(map(sum, n)) == sum(1 for gt, _ in pairs for row in gt for x in row if x != VOID)
    changed = []
    for gt, pred in pairs:
        pred2 = [[(x + 1) % 4 if g == VOID else x for g, x in zip(gr, pr)] for gr, pr in zip(gt, pred)]
        changed.append((gt, pred2))
    assert confusion_matrix(changed, 4) == n
    assert confusion_matrix(list(reversed(pairs)), 4) == n


def test_range_and_perfect_prediction():
    rng = random.Random(33)
    for _ in range(20):
        gt, pred = random_pair(rng, 3, 5, 5)
        n = confusion_matrix([(gt, pred)], 3)
        m = mean_iou(n)
        assert 0 <= m <= 1
        perfect = [[x if x != VOID else 0 for x in row] for row in gt]
        assert mean_iou(confusion_matrix([(gt, perfect)], 3)) == 1
        assert (m == 1) == all(n[i][j] == 0 for i in range(3) for j in range(3) if i != j)


def test_absent_class_rules():
    gt, pred = [[0, 0]], [[0, 0]]
    n = confusion_matrix([(gt, pred)], 3)
    assert class_iou(n) == [1, None, None] and mean_iou(n) == 1
    n = confusion_matrix([(gt, [[0, 2]])], 3)
    assert class_iou(n) == [Fraction(1, 2), None, 0]  # predicted but absent: IoU 0, and it counts
    assert mean_iou(n) == Fraction(1, 4)


def test_dataset_score_differs_from_mean_of_images():
    a = ([[0, 0, 0, 1]], [[0, 0, 0, 0]])
    b = ([[1, 1, 1, 1]], [[1, 1, 1, 1]])
    assert mean_iou(confusion_matrix([a, b], 2)) == Fraction(31, 40)
    assert per_image_mean_iou([a, b], 2) == Fraction(11, 16)


def test_imbalance_accuracy_versus_miou():
    g = [[0] * 8 for _ in range(8)]
    g[0][0] = 1
    p = [[0] * 8 for _ in range(8)]
    n = confusion_matrix([(g, p)], 2)
    assert pixel_accuracy(n) == Fraction(63, 64)
    assert mean_iou(n) == Fraction(63, 128)


def test_dice_is_increasing_function_of_iou():
    rng = random.Random(34)
    gt, pred = random_pair(rng, 5, 8, 8)
    n = confusion_matrix([(gt, pred)], 5)
    for j, d in zip(class_iou(n), dice(n)):
        assert (j is None and d is None) or d == 2 * j / (1 + j)


def test_permuting_labels_keeps_the_score():
    rng = random.Random(35)
    gt, pred = random_pair(rng, 4, 7, 6)
    perm = [2, 0, 3, 1]
    gt2 = [[x if x == VOID else perm[x] for x in row] for row in gt]
    pred2 = [[perm[x] for x in row] for row in pred]
    assert mean_iou(confusion_matrix([(gt, pred)], 4)) == mean_iou(confusion_matrix([(gt2, pred2)], 4))


def test_bad_labels_raise():
    try:
        confusion_matrix([([[0]], [[3]])], 3)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
