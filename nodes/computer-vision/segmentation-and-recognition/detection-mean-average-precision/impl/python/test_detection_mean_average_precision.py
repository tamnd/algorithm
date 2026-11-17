# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/detection-mean-average-precision/. The authors are listed in prov/ZNZ16Q.jsonl.

import random
from fractions import Fraction

from detection_mean_average_precision import (COCO_THRESHOLDS, ap_11_points, ap_101_points,
                                              ap_all_points, average_precision, coco_map,
                                              interpolated, iou, match_coco, match_voc,
                                              mean_average_precision, precision_recall)

GTS = {"A": [(0, 0, 10, 10), (20, 0, 30, 10)], "B": [(0, 0, 10, 10)]}
DETS = [("A", 0.9, (1, 0, 11, 10)), ("A", 0.8, (0, 1, 10, 11)), ("B", 0.7, (0, 0, 9, 10)),
        ("A", 0.6, (24, 0, 34, 10)), ("B", 0.5, (40, 40, 50, 50))]


def random_class(rng, n_images=3, n_gt=3, n_det=8):
    gts, dets = {}, []
    for img in range(n_images):
        boxes = []
        for _ in range(rng.randint(0, n_gt)):
            x, y = rng.randint(0, 20), rng.randint(0, 20)
            boxes.append((x, y, x + rng.randint(3, 8), y + rng.randint(3, 8)))
        gts[img] = boxes
    for _ in range(rng.randint(0, n_det)):
        img = rng.randrange(n_images)
        if gts[img] and rng.random() < 0.7:
            g = rng.choice(gts[img])
            dx, dy = rng.randint(-2, 2), rng.randint(-2, 2)
            box = (g[0] + dx, g[1] + dy, g[2] + dx + rng.randint(-1, 1), g[3] + dy)
        else:
            x, y = rng.randint(0, 20), rng.randint(0, 20)
            box = (x, y, x + 5, y + 5)
        if box[2] <= box[0]:
            box = (box[0], box[1], box[0] + 1, box[3])
        dets.append((img, rng.randint(1, 5), box))  # integer scores with ties
    return dets, gts


def test_page_example():
    assert iou(DETS[0][2], GTS["A"][0]) == Fraction(9, 11)
    assert iou(DETS[3][2], GTS["A"][1]) == Fraction(3, 7)
    flags, npos = match_voc(DETS, GTS)
    assert flags == [True, False, True, False, False] and npos == 3
    prec, rec = precision_recall(flags, npos)
    assert prec == [1, Fraction(1, 2), Fraction(2, 3), Fraction(1, 2), Fraction(2, 5)]
    assert rec == [Fraction(1, 3), Fraction(1, 3), Fraction(2, 3), Fraction(2, 3), Fraction(2, 3)]
    assert ap_all_points(prec, rec) == Fraction(5, 9)
    assert ap_11_points(prec, rec) == Fraction(6, 11)
    assert ap_101_points(prec, rec) == Fraction(56, 101)


def test_page_example_coco():
    per_t = []
    for t in COCO_THRESHOLDS:
        flags, npos = match_coco(DETS, GTS, t)
        per_t.append(ap_101_points(*precision_recall(flags, npos)))
    assert per_t == [Fraction(56, 101)] * 7 + [Fraction(34, 303)] * 2 + [0]
    assert coco_map({"c": (DETS, GTS)}) == Fraction(622, 1515)
    # IoU exactly 9/10 counts at threshold 0.9 in COCO (at least) but not
    # in the VOC rule (above).
    assert match_coco(DETS, GTS, Fraction(9, 10))[0][2] is True
    assert match_voc(DETS, GTS, Fraction(9, 10))[0][2] is False


def test_voc_and_coco_matching_differ():
    gts = {"X": [(0, 0, 10, 10), (2, 0, 12, 10)]}
    dets = [("X", 0.9, (1, 0, 11, 10)), ("X", 0.8, (0, 0, 10, 10))]
    assert iou(*gts["X"]) == Fraction(2, 3)
    assert match_voc(dets, gts) == ([True, False], 2)
    assert match_coco(dets, gts) == ([True, True], 2)
    assert average_precision(dets, gts) == Fraction(1, 2)
    assert average_precision(dets, gts, rule="coco") == 1


def test_difficult_boxes_are_ignored():
    gts = {"X": [(0, 0, 10, 10), (20, 0, 30, 10)]}
    diff = {"X": [False, True]}
    dets = [("X", 0.9, (20, 0, 30, 10)), ("X", 0.8, (0, 0, 10, 10))]
    flags, npos = match_voc(dets, gts, difficult=diff)
    assert flags == [None, True] and npos == 1
    assert average_precision(dets, gts, difficult=diff) == 1


def test_all_points_equals_mean_over_recall_levels():
    # Recall moves in steps of 1/npos, so the area under the interpolated
    # curve is the mean of p_interp(k / npos) over k = 1..npos.
    rng = random.Random(21)
    for trial in range(200):
        dets, gts = random_class(rng)
        flags, npos = match_voc(dets, gts)
        if npos == 0:
            continue
        prec, rec = precision_recall(flags, npos)
        ref = sum(interpolated(prec, rec, Fraction(k, npos)) for k in range(1, npos + 1)) / npos
        assert ap_all_points(prec, rec) == ref


def test_ap_from_brute_force_over_ranks():
    # Brute force: for each true positive at rank r, take the best precision
    # at rank r or later; average over all npos objects (missed ones give 0).
    rng = random.Random(22)
    for trial in range(200):
        flags = [rng.random() < 0.5 for _ in range(rng.randint(0, 12))]
        npos = sum(flags) + rng.randint(0, 3)
        if npos == 0:
            continue
        prec, rec = precision_recall(flags, npos)
        total = Fraction(0)
        for r, f in enumerate(flags):
            if f:
                total += max(prec[r:])
        assert ap_all_points(prec, rec) == total / npos


def test_perfect_and_empty_detectors():
    gts = {0: [(0, 0, 4, 4), (10, 10, 14, 14)], 1: [(3, 3, 9, 9)]}
    dets = [(img, 1, b) for img, bs in gts.items() for b in bs]
    for points in ("all", 11, 101):
        assert average_precision(dets, gts, points=points) == 1
        assert average_precision([], gts, points=points) == 0
    assert coco_map({"c": (dets, gts)}) == 1


def test_only_the_order_of_scores_matters():
    rng = random.Random(23)
    for trial in range(100):
        dets, gts = random_class(rng)
        moved = [(img, 3 * s * s + 7, box) for img, s, box in dets]
        for rule in ("voc", "coco"):
            assert average_precision(dets, gts, rule=rule) == average_precision(moved, gts, rule=rule)


def test_coco_matching_is_one_to_one_and_respects_threshold():
    rng = random.Random(24)
    for trial in range(150):
        dets, gts = random_class(rng)
        t = rng.choice(COCO_THRESHOLDS)
        flags, npos = match_coco(dets, gts, t)
        # The true positives form a one-to-one matching on pairs with IoU at
        # least t, so they cannot exceed a maximum matching found by search.
        edges = [[(img, g) for g, gb in enumerate(gts[img]) if iou(box, gb) >= t]
                 for img, _, box in dets]

        def best(k, taken):
            if k == len(edges):
                return 0
            res = best(k + 1, taken)
            for e in edges[k]:
                if e not in taken:
                    res = max(res, 1 + best(k + 1, taken | {e}))
            return res

        assert sum(flags) <= best(0, frozenset())
        # A detection with no pair at IoU at least t is never a true positive.
        order = sorted(range(len(dets)), key=lambda k: (-dets[k][1], k))
        for r, k in enumerate(order):
            if not edges[k]:
                assert flags[r] is False


def test_mean_over_classes():
    per_class = {"a": (DETS, GTS), "b": ([("A", 1, (0, 0, 10, 10))], {"A": [(0, 0, 10, 10)]})}
    assert mean_average_precision(per_class) == (Fraction(5, 9) + 1) / 2
