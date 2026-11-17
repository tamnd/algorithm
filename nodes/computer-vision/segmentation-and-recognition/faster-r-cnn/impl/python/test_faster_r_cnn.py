# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/faster-r-cnn/. The authors are listed in prov/5WFTBK.jsonl.

import math
import random
from fractions import Fraction

from faster_r_cnn import (
    anchors,
    decode,
    encode,
    faster_rcnn,
    iou,
    label_anchors,
    rpn_loss,
    rpn_proposals,
    sample_anchors,
)

ROW = [(-8, 0, 24, 32), (8, 0, 40, 32), (24, 0, 56, 32), (40, 0, 72, 32)]
ZERO = [(0.0, 0.0, 0.0, 0.0)] * 4


def test_anchor_shapes():
    a = anchors(5, 3, 16)
    assert len(a) == 5 * 3 * 9
    for k, b in enumerate(a):
        w, h = b[2] - b[0], b[3] - b[1]
        size = (128, 256, 512)[k % 3]
        ratio = (0.5, 1, 2)[(k % 9) // 3]
        assert abs(w * h - size * size) < 1e-6 and abs(h / w - ratio) < 1e-9
        cell = k // 9
        assert abs((b[0] + b[2]) / 2 - (cell % 5 + 0.5) * 16) < 1e-9
        assert abs((b[1] + b[3]) / 2 - (cell // 5 + 0.5) * 16) < 1e-9


def test_page_example_proposals():
    scores = [0.9, 0.8, 0.3, 0.6]
    out = rpn_proposals(ROW, scores, ZERO, 64, 32, min_size=16, nms_thr=0.3)
    assert out == [(0.9, (0, 0, 24, 32)), (0.6, (40, 0, 64, 32))]
    assert iou((0, 0, 24, 32), (8, 0, 40, 32)) == Fraction(2, 5)
    out = rpn_proposals(ROW, scores, ZERO, 64, 32, min_size=16, nms_thr=0.7)
    assert [s for s, _ in out] == [0.9, 0.8, 0.6, 0.3]
    # A minimum size of 32 drops the two clipped boxes, which are 24 wide.
    out = rpn_proposals(ROW, scores, ZERO, 64, 32, min_size=32, nms_thr=0.7)
    assert [b for _, b in out] == [(8, 0, 40, 32), (24, 0, 56, 32)]
    # Offsets move the box before the clip: shift anchor 2 right by half its width and double its width.
    out = rpn_proposals(ROW[2:3], [1.0], [(0.5, 0.0, math.log(2), 0.0)], 64, 32, min_size=1)
    assert out == [(1.0, (24.0, 0.0, 64, 32.0))]


def test_page_example_labels():
    anchor_list = [(0, 0, 10, 10), (5, 0, 15, 10), (10, 0, 20, 10), (20, 0, 30, 10), (35, 0, 45, 10)]
    gts = [(4, 0, 14, 10), (21, 0, 25, 4)]
    labels, match = label_anchors(anchor_list, gts, 40, 10)
    assert labels == [-1, 1, 0, 1, -1]
    assert match[1] == 0 and match[3] == 1
    assert iou(anchor_list[0], gts[0]) == Fraction(3, 7) and iou(anchor_list[3], gts[1]) == Fraction(4, 25)


def test_labels_match_the_definition():
    rng = random.Random(1)

    def rbox(lo, hi):
        x, y = rng.randint(lo, hi), rng.randint(lo, hi)
        return (x, y, x + rng.randint(2, 16), y + rng.randint(2, 16))

    for _ in range(80):
        anchor_list = [rbox(-6, 34) for _ in range(20)]
        gts = [rbox(0, 24) for _ in range(rng.randint(1, 3))]
        labels, match = label_anchors(anchor_list, gts, 40, 40)
        inside = [a[0] >= 0 and a[1] >= 0 and a[2] <= 40 and a[3] <= 40 for a in anchor_list]
        best_gt = [max((iou(a, g) for a, ok in zip(anchor_list, inside) if ok), default=0) for g in gts]
        for i, a in enumerate(anchor_list):
            if not inside[i]:
                assert labels[i] == -1
                continue
            o = [iou(a, g) for g in gts]
            forced = any(best_gt[j] > 0 and o[j] == best_gt[j] for j in range(len(gts)))
            if forced or max(o) >= Fraction(7, 10):
                assert labels[i] == 1 and o[match[i]] > 0
            elif max(o) < Fraction(3, 10):
                assert labels[i] == 0
            else:
                assert labels[i] == -1
        sampled = sample_anchors(labels, rng, batch=8)
        assert sum(1 for v in sampled if v == 1) <= 4 and sum(1 for v in sampled if v >= 0) <= 8
        assert all(v == -1 or v == labels[i] for i, v in enumerate(sampled))


def test_rpn_loss_value():
    probs = [0.9, 0.2, 0.5]
    deltas = [(0.5, 0.0, 0.0, 2.0), (9.0, 9.0, 9.0, 9.0), (0.0, 0.0, 0.0, 0.0)]
    targets = [(0.0, 0.0, 0.0, 0.0)] * 3
    labels = [1, 0, -1]
    want = -(math.log(0.9) + math.log(0.8)) / 2 + 10 * (0.125 + 1.5) / 50
    assert abs(rpn_loss(probs, deltas, labels, targets, n_reg=50) - want) < 1e-12


def test_proposals_properties_on_random_outputs():
    rng = random.Random(2)
    for _ in range(6):
        fw, fh = rng.randint(2, 5), rng.randint(2, 4)
        a = anchors(fw, fh, 16, sizes=(16, 32), ratios=(0.5, 1, 2))
        scores = [rng.random() for _ in a]
        deltas = [tuple(rng.gauss(0, 0.2) for _ in range(4)) for _ in a]
        out = rpn_proposals(a, scores, deltas, fw * 16, fh * 16, min_size=4, nms_thr=0.7, post_nms=10)
        assert len(out) <= 10
        assert [s for s, _ in out] == sorted((s for s, _ in out), reverse=True)
        for _, b in out:
            assert 0 <= b[0] and b[2] <= fw * 16 and 0 <= b[1] and b[3] <= fh * 16
            assert b[2] - b[0] >= 4 and b[3] - b[1] >= 4
        for i in range(len(out)):
            for j in range(i):
                assert iou(out[i][1], out[j][1]) <= 0.7


def test_whole_pipeline():
    truth = (20.0, 12.0, 44.0, 36.0)
    a = anchors(4, 3, 16, sizes=(16, 32), ratios=(1,))
    # An RPN that likes anchors near the truth and points them at it.
    scores = [float(iou(b, truth)) for b in a]
    deltas = [encode(b, truth) if iou(b, truth) > 0.3 else (0.0, 0.0, 0.0, 0.0) for b in a]

    def head(box):
        o = float(iou(box, truth))
        return [1 - o, o], [encode(box, truth)]

    props, dets = faster_rcnn(4, 3, 16, scores, deltas, head, 64, 48, sizes=(16, 32), ratios=(1,),
                              min_size=8)
    assert all(abs(x - y) < 1e-9 for x, y in zip(props[0][1], truth))
    assert len(dets[1]) == 1
    s, b = dets[1][0]
    assert s > 0.99 and all(abs(x - y) < 1e-9 for x, y in zip(b, truth))
    assert all(abs(x - y) < 1e-9 for x, y in zip(decode(a[5], encode(a[5], truth)), truth))
