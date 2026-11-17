# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-r-cnn/. The authors are listed in prov/CTWF7A.jsonl.

import math
import random
from fractions import Fraction

from fast_r_cnn import (
    decode,
    detect,
    encode,
    iou,
    multitask_loss,
    roi_pool,
    roi_pool_backward,
    sample_rois,
    smooth_l1,
    smooth_l1_grad,
    softmax,
)


def test_page_example_loss():
    truth = [(0, 0, 10, 10)]
    rois = [(0, 0, 10, 8), (0, 0, 10, 6), (6, 0, 16, 10), (9, 0, 19, 10), (30, 30, 40, 40)]
    assert [iou(r, truth[0]) for r in rois] == [Fraction(4, 5), Fraction(3, 5), Fraction(1, 4),
                                               Fraction(1, 19), 0]
    # A batch of 4 takes one of the two foreground RoIs (25 percent) and the one background RoI.
    for seed in range(5):
        picked = sorted(sample_rois(rois, truth, [1], 4, random.Random(seed)), key=lambda x: x[0])
        assert picked in ([(0, 1, 0), (2, 0, None)], [(1, 1, 0), (2, 0, None)])
    picked = sample_rois(rois, truth, [1], 8, random.Random(0))
    assert sorted(picked, key=lambda x: x[0]) == [(0, 1, 0), (1, 1, 0), (2, 0, None)]
    loss = multitask_loss([0.2, 0.8], 1, (0.5, -2.0, 0.0, 0.1), (0.0, 0.0, 0.0, 0.0))
    assert abs(loss - (-math.log(0.8) + 0.125 + 1.5 + 0.0 + 0.005)) < 1e-12
    assert abs(multitask_loss([0.7, 0.3], 0, (9.0, 9.0, 9.0, 9.0), (0, 0, 0, 0)) + math.log(0.7)) < 1e-12


def test_roi_pool_check_value():
    feat = [[[(3 * r + 5 * c) % 11 for c in range(8)] for r in range(6)]]
    y, s = roi_pool(feat, (5, 3, 26, 17), 0.25, 2, 2)
    assert y == [[[10, 9], [10, 10]]]
    for (p, q) in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        r, c = s[0][p][q]
        assert feat[0][r][c] == y[0][p][q]


def test_roi_pool_backward_is_the_gradient():
    rng = random.Random(1)
    fh, fw = 9, 11
    for _ in range(10):
        feat = [[[rng.random() for _ in range(fw)] for _ in range(fh)] for _ in range(2)]
        x1, y1 = rng.randint(0, 20), rng.randint(0, 16)
        box = (x1, y1, x1 + rng.randint(4, 24), y1 + rng.randint(4, 20))
        wts = [[[rng.uniform(-1, 1) for _ in range(3)] for _ in range(2)] for _ in range(2)]

        def f(m):
            y, _ = roi_pool(m, box, 0.5, 2, 3)
            return sum(wts[k][p][q] * y[k][p][q] for k in range(2) for p in range(2) for q in range(3))

        _, s = roi_pool(feat, box, 0.5, 2, 3)
        g = roi_pool_backward(wts, s, fh, fw)
        eps = 1e-7
        for k in range(2):
            for r in range(fh):
                for c in range(fw):
                    old = feat[k][r][c]
                    feat[k][r][c] = old + eps
                    up = f(feat)
                    feat[k][r][c] = old - eps
                    dn = f(feat)
                    feat[k][r][c] = old
                    assert abs((up - dn) / (2 * eps) - g[k][r][c]) < 1e-6


def test_decode_inverts_encode_with_normalization():
    rng = random.Random(2)
    mean, std = (0.01, -0.02, 0.05, 0.0), (0.1, 0.1, 0.2, 0.2)
    for _ in range(100):
        r = (rng.uniform(0, 40), rng.uniform(0, 40))
        r = r + (r[0] + rng.uniform(2, 30), r[1] + rng.uniform(2, 30))
        g = (rng.uniform(0, 40), rng.uniform(0, 40))
        g = g + (g[0] + rng.uniform(2, 30), g[1] + rng.uniform(2, 30))
        assert all(abs(a - b) < 1e-9 for a, b in zip(decode(r, encode(r, g, mean, std), mean, std), g))


def test_detect_on_a_hand_built_head():
    # One channel, 8 x 8 cells, scale 1/4: a bright 3 x 3 patch of cells at rows 2..4, columns 2..4.
    feat = [[[1.0 if 2 <= r <= 4 and 2 <= c <= 4 else 0.0 for c in range(8)] for r in range(8)]]

    def head(pooled):
        vals = [v for row in pooled[0] for v in row]
        m = sum(vals) / len(vals)
        # Class 1 likes a fully bright RoI; class 2 likes a dark one. No box offsets.
        return [0.0, 6 * m - 3, 3 - 6 * m], [(0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0)]

    rois = [(8, 8, 20, 20), (8, 8, 24, 20), (24, 0, 32, 8), (24, 24, 32, 32), (4, 8, 20, 20)]
    out = detect(feat, rois, 0.25, head, out_h=2, out_w=2, nms_thr=0.3, score_thr=0.5)
    # RoIs 1 and 4 score as high as RoI 0 but overlap it by IoU 3/4, so NMS removes them.
    assert [i for _, _, i in out[1]] == [0]
    assert [i for _, _, i in out[2]] == [2, 3]
    probs = softmax([0.0, 3.0, -3.0])
    assert abs(out[1][0][0] - probs[1]) < 1e-12 and out[1][0][1] == (8.0, 8.0, 20.0, 20.0)


def test_sampling_rules():
    rng = random.Random(3)

    def rbox():
        x, y = rng.randint(0, 40), rng.randint(0, 40)
        return (x, y, x + rng.randint(2, 20), y + rng.randint(2, 20))

    for _ in range(40):
        gts = [rbox() for _ in range(rng.randint(1, 3))]
        cls = [rng.randint(1, 3) for _ in gts]
        rois = [rbox() for _ in range(40)] + [(g[0] + 1, g[1], g[2] + 1, g[3]) for g in gts]
        batch = 16
        picked = sample_rois(rois, gts, cls, batch, rng)
        assert len(picked) <= batch and len({i for i, _, _ in picked}) == len(picked)
        n_fg = sum(1 for _, c, _ in picked if c > 0)
        assert n_fg <= 4
        for i, c, j in picked:
            best = max(iou(rois[i], g) for g in gts)
            if c > 0:
                assert best >= Fraction(1, 2) and iou(rois[i], gts[j]) == best and cls[j] == c
            else:
                assert Fraction(1, 10) <= best < Fraction(1, 2)


def test_smooth_l1():
    assert smooth_l1(0.5) == 0.125 and smooth_l1(-2.0) == 1.5 and smooth_l1(1.0) == 0.5
    for x in [-3.0, -1.0, -0.4, 0.0, 0.3, 0.999, 2.5]:
        assert abs(smooth_l1_grad(x)) <= 1
        eps = 1e-6
        if abs(abs(x) - 1) > 1e-3:
            assert abs((smooth_l1(x + eps) - smooth_l1(x - eps)) / (2 * eps) - smooth_l1_grad(x)) < 1e-6
    # The loss is continuous at |x| = 1.
    assert abs(smooth_l1(1 - 1e-12) - smooth_l1(1 + 1e-12)) < 1e-9
