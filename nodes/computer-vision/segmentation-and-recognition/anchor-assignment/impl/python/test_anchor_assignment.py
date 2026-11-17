# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anchor-assignment/. The authors are listed in prov/RFHSZS.jsonl.

import random
from fractions import Fraction

from anchor_assignment import (
    assign_atss,
    assign_max_iou,
    assign_ssd,
    iou,
    iou_matrix,
    mean_std,
    sample,
)

ANCHORS = [(0, 0, 10, 10), (5, 0, 15, 10), (10, 0, 20, 10), (20, 0, 30, 10)]
GTS = [(4, 0, 14, 10), (21, 0, 25, 4)]


def rand_box(rng, size=100):
    x1, y1 = rng.randint(0, size - 2), rng.randint(0, size - 2)
    return (x1, y1, rng.randint(x1 + 1, size), rng.randint(y1 + 1, size))


def test_page_example():
    m = iou_matrix(ANCHORS, GTS)
    assert [row[0] for row in m] == [Fraction(3, 7), Fraction(9, 11), Fraction(1, 4), 0]
    assert [row[1] for row in m] == [0, 0, 0, Fraction(4, 25)]
    labels, matched = assign_max_iou(ANCHORS, GTS)
    assert labels == [-1, 1, 0, 1]
    assert matched == [0, 0, 0, 1]
    labels, _ = assign_max_iou(ANCHORS, GTS, best_for_gt=False)
    assert labels == [-1, 1, 0, 0]
    # RetinaNet thresholds: 3/7 lies in [0.4, 0.5), so the first anchor is still ignored.
    labels, _ = assign_max_iou(ANCHORS, GTS, 0.5, 0.4, best_for_gt=False)
    assert labels == [-1, 1, 0, 0]


def test_rule_against_definition():
    rng = random.Random(1)
    for _ in range(60):
        anchors = [rand_box(rng) for _ in range(25)]
        gts = [rand_box(rng) for _ in range(rng.randint(1, 4))]
        labels, matched = assign_max_iou(anchors, gts)
        m = [[iou(a, g) for g in gts] for a in anchors]
        best_gt = [max(m[i][j] for i in range(len(anchors))) for j in range(len(gts))]
        for i in range(len(anchors)):
            mi = max(m[i])
            assert m[i][matched[i]] == mi
            is_best = any(m[i][j] == best_gt[j] > 0 for j in range(len(gts)))
            if mi >= Fraction(7, 10) or is_best:
                assert labels[i] == 1
            elif mi < Fraction(3, 10):
                assert labels[i] == 0
            else:
                assert labels[i] == -1
        for j in range(len(gts)):
            if best_gt[j] > 0:
                assert any(labels[i] == 1 and m[i][j] == best_gt[j] for i in range(len(anchors)))


def test_ties_and_no_overlap():
    anchors = [(0, 0, 10, 10), (10, 0, 20, 10), (40, 40, 50, 50)]
    labels, _ = assign_max_iou(anchors, [(5, 0, 15, 10)])
    assert labels == [1, 1, 0]
    # A true box that touches no anchor makes no anchor positive.
    labels, matched = assign_max_iou(anchors, [(100, 100, 110, 110)])
    assert labels == [0, 0, 0] and matched == [0, 0, 0]
    assert assign_max_iou(anchors, []) == ([0, 0, 0], [-1, -1, -1])


def test_sampling():
    rng = random.Random(2)
    labels = [1] * 300 + [0] * 5000 + [-1] * 200
    out = sample(labels, 256, 0.5, rng)
    assert out.count(1) == 128 and out.count(0) == 128
    assert all(o == -1 or o == v for o, v in zip(out, labels))
    out = sample([1] * 10 + [0] * 5000, 256, 0.5, rng)
    assert out.count(1) == 10 and out.count(0) == 246


def test_ssd_every_box_gets_an_anchor():
    rng = random.Random(3)
    for _ in range(60):
        anchors = [rand_box(rng) for _ in range(30)]
        gts = [rand_box(rng) for _ in range(rng.randint(1, 3))]
        labels, matched = assign_ssd(anchors, gts)
        assert -1 not in labels
        m = [[iou(a, g) for g in gts] for a in anchors]
        for i in range(len(anchors)):
            if max(m[i]) > Fraction(1, 2):
                assert labels[i] == 1
        bests = [max(range(len(anchors)), key=lambda i: (m[i][j], -i)) for j in range(len(gts))]
        if len(set(bests)) == len(gts):
            for j, i in enumerate(bests):
                assert labels[i] == 1 and matched[i] == j


def test_ssd_example():
    labels, matched = assign_ssd(ANCHORS, GTS)
    assert labels == [0, 1, 0, 1] and matched[1] == 0 and matched[3] == 1


def test_mean_std():
    mu, sd = mean_std([1.0, 2.0, 3.0, 4.0])
    assert mu == 2.5 and abs(sd - (5 / 3) ** 0.5) < 1e-12


def grid(stride, size, n):
    return [(u * stride + stride / 2 - size / 2, v * stride + stride / 2 - size / 2,
             u * stride + stride / 2 + size / 2, v * stride + stride / 2 + size / 2)
            for v in range(n) for u in range(n)]


def test_atss_properties():
    rng = random.Random(4)
    levels = [grid(8, 32, 16), grid(16, 64, 8), grid(32, 128, 4)]
    flat = [a for lv in levels for a in lv]
    for _ in range(20):
        gts = []
        for _ in range(rng.randint(1, 3)):
            w, h = rng.uniform(16, 100), rng.uniform(16, 100)
            x, y = rng.uniform(0, 128 - w), rng.uniform(0, 128 - h)
            gts.append((x, y, x + w, y + h))
        labels, matched = assign_atss(levels, gts, k=9)
        for i, v in enumerate(labels):
            if v == 1:
                g = gts[matched[i]]
                cx, cy = (flat[i][0] + flat[i][2]) / 2, (flat[i][1] + flat[i][3]) / 2
                assert g[0] < cx < g[2] and g[1] < cy < g[3]
            else:
                assert matched[i] == -1
        # Only the k nearest anchors of each level are candidates: at most 27 per box.
        for j in range(len(gts)):
            assert sum(1 for i in range(len(flat)) if matched[i] == j) <= 27


def test_atss_threshold_by_hand():
    # One level, k = 3. The candidates have IoUs 1, 1/3 and 1/3 with the box:
    # mean 5/9, sample std 0.3849, threshold 0.940, so only the exact anchor passes.
    level = [(0, 0, 4, 4), (2, 0, 6, 4), (-2, 0, 2, 4), (20, 20, 24, 24)]
    assert iou(level[1], (0, 0, 4, 4)) == Fraction(1, 3)
    labels, matched = assign_atss([level], [(0, 0, 4, 4)], k=3)
    assert labels == [1, 0, 0, 0] and matched == [0, -1, -1, -1]
