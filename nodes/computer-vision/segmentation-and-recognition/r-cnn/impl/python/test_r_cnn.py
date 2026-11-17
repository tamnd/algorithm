# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/r-cnn/. The authors are listed in prov/4YN1M9.jsonl.

import math
import random
from fractions import Fraction

from r_cnn import (
    context_box,
    decode,
    detect,
    finetune_labels,
    greedy_nms,
    iou,
    regression_pairs,
    svm_examples,
    warp,
)

TRUTH = [(0, 0, 10, 10)]
PROPS = [(0, 0, 10, 8), (0, 0, 10, 5), (5, 0, 15, 10), (6, 0, 16, 10), (20, 20, 30, 30)]


def test_page_example_labels():
    assert [iou(p, TRUTH[0]) for p in PROPS] == [Fraction(4, 5), Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), 0]
    assert finetune_labels(PROPS, TRUTH, [1]) == [1, 1, 0, 0, 0]
    pos, neg = svm_examples(PROPS, TRUTH, [1], 1)
    assert pos == TRUTH and neg == [3, 4]
    assert regression_pairs(PROPS, TRUTH) == [(0, 0)]


def test_page_example_nms():
    scores = [0.9, 0.6, 0.4, 0.3, 0.2]
    assert greedy_nms(PROPS, scores, 0.3) == [0, 2, 4]
    assert greedy_nms(PROPS, scores, 0.7) == [0, 1, 2, 4]


def test_context_box():
    assert all(abs(a - b) < 1e-9 for a, b in zip(context_box((0, 0, 195, 195)), (-16, -16, 211, 211)))
    rng = random.Random(1)
    for _ in range(50):
        x1, y1 = rng.uniform(-5, 50), rng.uniform(-5, 50)
        b = (x1, y1, x1 + rng.uniform(1, 40), y1 + rng.uniform(1, 40))
        size, pad = rng.choice([(227, 16), (20, 3), (9, 1)])
        c = context_box(b, size, pad)
        # The original edges map to pad and size - pad in the warped patch.
        for k, lo, hi in ((0, 0, 2), (1, 1, 3)):
            span = c[hi] - c[lo]
            assert abs((b[lo] - c[lo]) / span * size - pad) < 1e-9
            assert abs((b[hi] - c[lo]) / span * size - (size - pad)) < 1e-9


def test_warp_is_exact_on_a_ramp_and_fills_outside():
    img = [[3 * u - 2 * v + 7 for u in range(12)] for v in range(10)]
    box = (2.0, 1.5, 9.0, 8.0)
    size = 7
    patch = warp(img, box, size, fill=-1)
    for v in range(size):
        for u in range(size):
            x = box[0] + (u + 0.5) * (box[2] - box[0]) / size - 0.5
            y = box[1] + (v + 0.5) * (box[3] - box[1]) / size - 0.5
            assert abs(patch[v][u] - (3 * x - 2 * y + 7)) < 1e-9
    assert warp(img, (20, 20, 30, 30), 3, fill=5.5) == [[5.5] * 3] * 3


def test_decode_inverts_the_encoding():
    rng = random.Random(2)
    for _ in range(100):
        p = (rng.uniform(0, 50), rng.uniform(0, 50))
        p = p + (p[0] + rng.uniform(1, 30), p[1] + rng.uniform(1, 30))
        g = (rng.uniform(0, 50), rng.uniform(0, 50))
        g = g + (g[0] + rng.uniform(1, 30), g[1] + rng.uniform(1, 30))
        pw, ph, gw, gh = p[2] - p[0], p[3] - p[1], g[2] - g[0], g[3] - g[1]
        t = (((g[0] + g[2]) - (p[0] + p[2])) / 2 / pw, ((g[1] + g[3]) - (p[1] + p[3])) / 2 / ph,
             math.log(gw / pw), math.log(gh / ph))
        assert all(abs(a - b) < 1e-9 for a, b in zip(decode(p, t), g))
    assert decode((1, 2, 5, 9), (0, 0, 0, 0)) == (1, 2, 5, 9)


def test_detect_end_to_end():
    img = [[0] * 16 for _ in range(16)]
    for v in range(3, 9):
        for u in range(2, 8):
            img[v][u] = 100
    size, pad = 12, 2

    def features(patch):
        inner = [patch[v][u] for v in range(pad, size - pad) for u in range(pad, size - pad)]
        ring = [patch[v][u] for v in range(size) for u in range(size)
                if not (pad <= v < size - pad and pad <= u < size - pad)]
        return [sum(inner) / len(inner), sum(ring) / len(ring)]

    props = [(2, 3, 8, 9), (1, 2, 9, 10), (2, 3, 8, 6), (0, 0, 16, 16), (10, 10, 15, 15)]
    svm = {1: ([1.0, -1.0], -50.0)}
    shift = {1: lambda f: (0.0, 0.0, 0.0, 0.0)}
    out = detect(img, props, features, svm, shift, nms_thr=0.3, size=size, pad=pad)
    dets = out[1]
    assert dets[0][2] == 0 and dets[0][0] > 0
    kept = [i for _, _, i in dets]
    assert 1 not in kept and 2 not in kept
    assert all(s <= 0 for s, _, i in dets if i in (3, 4))
    # A regressor that moves every box right by its width moves the output boxes the same way.
    move = {1: lambda f: (1.0, 0.0, 0.0, 0.0)}
    out2 = detect(img, props, features, svm, move, nms_thr=0.3, size=size, pad=pad)
    b = out2[1][0][1]
    assert out2[1][0][2] == 0 and b == (8.0, 3.0, 14.0, 9.0)


def test_rules_agree_on_random_inputs():
    rng = random.Random(3)

    def rbox():
        x, y = rng.randint(0, 30), rng.randint(0, 30)
        return (x, y, x + rng.randint(1, 15), y + rng.randint(1, 15))

    for _ in range(60):
        gts = [rbox() for _ in range(rng.randint(1, 3))]
        cls = [rng.randint(1, 2) for _ in gts]
        props = [rbox() for _ in range(12)]
        ft = finetune_labels(props, gts, cls)
        for i, j in regression_pairs(props, gts):
            assert ft[i] == cls[j] and iou(props[i], gts[j]) > Fraction(3, 5)
        for c in (1, 2):
            pos, neg = svm_examples(props, gts, cls, c)
            for i in neg:
                assert ft[i] != c
        scores = [rng.random() for _ in props]
        keep = greedy_nms(props, scores, 0.3)
        for a in keep:
            for b in keep:
                assert a == b or iou(props[a], props[b]) <= 0.3
        for i in set(range(len(props))) - set(keep):
            assert any(scores[k] >= scores[i] and iou(props[i], props[k]) > 0.3 for k in keep)
