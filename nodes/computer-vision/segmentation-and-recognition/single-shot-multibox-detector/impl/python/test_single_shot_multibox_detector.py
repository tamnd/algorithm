# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/single-shot-multibox-detector/. The authors are listed in prov/TNJGM1.jsonl.

import math
import random

from single_shot_multibox_detector import (
    corners,
    decode,
    default_boxes,
    detect,
    encode,
    hard_negatives,
    iou,
    match,
    ssd_loss,
    ssd_scales,
)

SSD300_MAPS = [38, 19, 10, 5, 3, 1]
SSD300_RATIOS = [[1, 2, 0.5]] + [[1, 2, 3, 0.5, 1 / 3]] * 3 + [[1, 2, 0.5]] * 2


def test_scales_and_box_count():
    s = ssd_scales(6)
    assert all(abs(a - b) < 1e-12 for a, b in zip(s, [0.2, 0.34, 0.48, 0.62, 0.76, 0.9]))
    d = default_boxes(SSD300_MAPS, SSD300_RATIOS)
    assert len(d) == 38 * 38 * 4 + 19 * 19 * 6 + 10 * 10 * 6 + 5 * 5 * 6 + 3 * 3 * 4 + 4 == 8732


def test_default_box_shapes():
    s = ssd_scales(3)
    d = default_boxes([4, 2, 1], [[1, 2, 0.5], [1, 3], [2]])
    assert len(d) == 16 * 4 + 4 * 3 + 1
    first = d[:4]
    assert all(abs(b[0] - 0.125) < 1e-12 and abs(b[1] - 0.125) < 1e-12 for b in first)
    for (_, _, w, h), a in zip(first[:3], [1, 2, 0.5]):
        assert abs(w * h - s[0] ** 2) < 1e-12 and abs(w / h - a) < 1e-12
    assert abs(first[3][2] - math.sqrt(s[0] * s[1])) < 1e-12
    # The single box of the last map has ratio 2 and no extra box.
    cx, cy, w, h = d[-1]
    assert (cx, cy) == (0.5, 0.5) and abs(w * h - s[2] ** 2) < 1e-12 and abs(w / h - 2) < 1e-12
    for b in d:
        assert 0 < b[0] < 1 and 0 < b[1] < 1


def test_page_example_matching():
    gts = [(0, 0, 10, 10), (20, 0, 30, 10)]
    boxes = [(0, 0, 10, 10), (0, 0, 10, 8), (0, 0, 10, 4), (25, 0, 35, 10), (40, 0, 50, 10)]
    assert match(boxes, gts) == [0, 0, -1, 1, -1]
    # Two truths that prefer the same box: the second gets its own box in step 1.
    gts = [(0, 0, 10, 10), (0, 0, 10, 9)]
    boxes = [(0, 0, 10, 10), (0, 0, 10, 4)]
    assert match(boxes, gts) == [0, 1]
    assert match(boxes, []) == [-1, -1]


def test_matching_properties():
    rng = random.Random(3)

    def rbox():
        x, y = rng.randint(0, 20), rng.randint(0, 20)
        return (x, y, x + rng.randint(2, 12), y + rng.randint(2, 12))

    for _ in range(150):
        boxes = [rbox() for _ in range(rng.randint(1, 12))]
        gts = [rbox() for _ in range(rng.randint(1, 4))]
        m = match(boxes, gts)
        for i, b in enumerate(boxes):
            best = max(iou(b, g) for g in gts)
            if best > 0.5:
                assert m[i] >= 0
            if m[i] >= 0:
                assert iou(b, gts[m[i]]) > 0
            else:
                assert best <= 0.5
        for j, g in enumerate(gts):
            if j not in m:
                # Every box that overlaps g was given to another truth in step 1.
                assert all(m[i] >= 0 for i, b in enumerate(boxes) if iou(b, g) > 0)


def test_hard_negatives():
    losses = [0.1, 2.0, 0.5, 1.2, 0.05]
    assert hard_negatives(losses, 1) == [1, 3, 2]
    assert hard_negatives(losses, 2) == [1, 3, 2, 0, 4]
    assert hard_negatives(losses, 0) == []
    assert hard_negatives([1.0, 1.0, 1.0], 1, ratio=2) == [0, 1]


def test_page_example_loss():
    defaults = [(0.25, 0.25, 0.5, 0.5), (0.75, 0.25, 0.5, 0.5), (0.25, 0.75, 0.5, 0.5),
                (0.75, 0.75, 0.5, 0.5)]
    gts = [(0.0, 0.0, 0.5, 0.5)]
    l3 = math.log(3)
    logits = [[0.0, l3], [0.0, 0.0], [l3, 0.0], [0.0, l3]]
    locs = [(0.5, 0.0, 0.0, 0.0), (0.0,) * 4, (0.0,) * 4, (0.0,) * 4]
    want = -math.log(3 / 4) + math.log(4) + 0.125
    assert abs(ssd_loss(defaults, logits, locs, gts, [1], ratio=1) - want) < 1e-12
    want += math.log(2) + math.log(4 / 3)
    assert abs(ssd_loss(defaults, logits, locs, gts, [1]) - want) < 1e-12
    assert ssd_loss(defaults, logits, locs, [], []) == 0.0


def test_encode_decode_round_trip():
    rng = random.Random(4)
    for _ in range(50):
        d = (rng.random(), rng.random(), rng.uniform(0.05, 0.5), rng.uniform(0.05, 0.5))
        x, y = rng.random(), rng.random()
        g = (x, y, x + rng.uniform(0.01, 0.6), y + rng.uniform(0.01, 0.6))
        for var in [(1.0, 1.0), (0.1, 0.2)]:
            assert all(abs(a - b) < 1e-9 for a, b in zip(decode(d, encode(d, g, var), var), g))


def test_detect_properties_on_random_outputs():
    rng = random.Random(5)
    defaults = default_boxes([4, 2, 1], [[1, 2, 0.5], [1, 3], [1]])
    for _ in range(4):
        logits = [[rng.gauss(0, 2) for _ in range(4)] for _ in defaults]
        locs = [tuple(rng.gauss(0, 0.2) for _ in range(4)) for _ in defaults]
        out = detect(defaults, logits, locs, conf_thr=0.2, top_k=15)
        assert len(out) <= 15
        assert [s for s, _, _ in out] == sorted((s for s, _, _ in out), reverse=True)
        assert all(s > 0.2 for s, _, _ in out)
        for a in range(len(out)):
            for b in range(a):
                if out[a][1] == out[b][1]:
                    assert iou(out[a][2], out[b][2]) <= 0.45


def test_detect_recovers_a_box():
    truth = (0.3, 0.2, 0.7, 0.9)
    defaults = default_boxes([4, 2], [[1, 2, 0.5], [1, 0.5]])
    logits, locs = [], []
    for d in defaults:
        o = float(iou(corners(d), truth))
        logits.append([0.0, -2.0, 8.0 * o])
        locs.append(encode(d, truth) if o > 0.3 else (0.0,) * 4)
    out = detect(defaults, logits, locs)
    s, c, b = out[0]
    assert c == 2 and all(abs(x - y) < 1e-9 for x, y in zip(b, truth))
    assert all(iou(bb, truth) <= 0.45 for _, cc, bb in out[1:] if cc == 2)
