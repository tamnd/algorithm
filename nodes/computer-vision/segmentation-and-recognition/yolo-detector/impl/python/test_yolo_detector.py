# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yolo-detector/. The authors are listed in prov/D6VPA6.jsonl.

import math
import random

from yolo_detector import (
    cell_box,
    decode_v2,
    detect,
    dimension_clusters,
    iou,
    shape_iou,
    yolo_v1_loss,
)


def close(a, b, tol=1e-9):
    return all(abs(x - y) < tol for x, y in zip(a, b))


def page_tensor():
    return [
        [[0.8, 0.8, 0.6, 0.6, 0.9, 0.8, 0.2], [0.3, 0.5, 0.4, 0.4, 0.6, 0.1, 0.9]],
        [[0.8, 0.0, 0.6, 0.6, 0.6, 0.6, 0.4], [0.5, 0.5, 0.2, 0.2, 0.1, 0.5, 0.5]],
    ]


def test_page_example_decoding():
    out = page_tensor()
    assert close(cell_box(0, 0, 0.8, 0.8, 0.6, 0.6, 2, 100, 100), (10, 10, 70, 70))
    assert close(cell_box(0, 1, 0.3, 0.5, 0.4, 0.4, 2, 100, 100), (45, 5, 85, 45))
    assert close(cell_box(1, 0, 0.8, 0.0, 0.6, 0.6, 2, 100, 100), (10, 20, 70, 80))
    assert abs(iou((10, 10, 70, 70), (10, 20, 70, 80)) - 5 / 7) < 1e-12
    dets = detect(out, 2, 1, 2, 100, 100)
    assert [(round(sc, 9), cl) for sc, cl, _ in dets] == [(0.72, 0), (0.54, 1), (0.24, 1)]
    assert close(dets[0][2], (10, 10, 70, 70)) and close(dets[2][2], (10, 20, 70, 80))
    # With a looser NMS threshold the second box of class 0 stays.
    dets = detect(out, 2, 1, 2, 100, 100, nms_thr=0.75)
    assert [(round(sc, 9), cl) for sc, cl, _ in dets] == [(0.72, 0), (0.54, 1), (0.36, 0), (0.24, 1)]


def test_detect_properties_on_random_outputs():
    rng = random.Random(6)
    for _ in range(5):
        s, b, c = 4, 2, 3
        out = [[[rng.random() for _ in range(5 * b + c)] for _ in range(s)] for _ in range(s)]
        dets = detect(out, s, b, c, 64, 64, score_thr=0.15, nms_thr=0.4)
        assert len(dets) <= s * s * b * c
        assert [d[0] for d in dets] == sorted((d[0] for d in dets), reverse=True)
        assert all(d[0] > 0.15 for d in dets)
        for x in range(len(dets)):
            for y in range(x):
                if dets[x][1] == dets[y][1]:
                    assert iou(dets[x][2], dets[y][2]) <= 0.4


def test_page_example_loss():
    out = [[[0.6, 0.5, 0.6, 0.6, 0.7, 0.5, 0.5, 0.2, 0.2, 0.4, 0.3, 0.7]]]
    want = 5 * 0.1 ** 2 + (0.7 - 5 / 7) ** 2 + 0.5 * 0.4 ** 2 + 0.3 ** 2 + 0.3 ** 2
    assert abs(yolo_v1_loss(out, [(20, 20, 80, 80)], [1], 1, 2, 2, 100, 100) - want) < 1e-12
    # With no object, only the no-object term of both confidences is left.
    assert abs(yolo_v1_loss(out, [], [], 1, 2, 2, 100, 100) - 0.5 * (0.49 + 0.16)) < 1e-12


def test_loss_is_zero_on_perfect_outputs():
    rng = random.Random(7)
    s, b, c = 3, 2, 4
    for _ in range(20):
        cells = rng.sample([(i, j) for i in range(s) for j in range(s)], 3)
        gts, labels = [], []
        out = [[[0.0] * (5 * b + c) for _ in range(s)] for _ in range(s)]
        for i, j in cells:
            x, y = rng.uniform(0.05, 0.95), rng.uniform(0.05, 0.95)
            w, h = rng.uniform(0.1, 0.5), rng.uniform(0.1, 0.5)
            g = cell_box(i, j, x, y, w, h, s, 90, 90)
            cl = rng.randrange(c)
            gts.append(g)
            labels.append(cl)
            k = rng.randrange(b)
            out[i][j][5 * k:5 * k + 5] = [x, y, w, h, 1.0]
            out[i][j][5 * b + cl] = 1.0
        assert yolo_v1_loss(out, gts, labels, s, b, c, 90, 90) < 1e-12


def test_square_root_weights_small_boxes():
    def loss_for(w_true, w_pred):
        g = cell_box(0, 0, 0.5, 0.5, w_true, 0.5, 1, 100, 100)
        out = [[[0.5, 0.5, w_pred, 0.5, 0.0, 1.0]]]
        return yolo_v1_loss(out, [g], [0], 1, 1, 1, 100, 100, l_noobj=0.0)

    small = loss_for(0.1, 0.15) - (0 - float(iou(cell_box(0, 0, 0.5, 0.5, 0.15, 0.5, 1, 100, 100),
                                               cell_box(0, 0, 0.5, 0.5, 0.1, 0.5, 1, 100, 100)))) ** 2
    large = loss_for(0.8, 0.85) - (0 - float(iou(cell_box(0, 0, 0.5, 0.5, 0.85, 0.5, 1, 100, 100),
                                               cell_box(0, 0, 0.5, 0.5, 0.8, 0.5, 1, 100, 100)))) ** 2
    assert small > 5 * large


def test_v2_decoding():
    box, obj = decode_v2((0.0, 0.0, 0.0, 0.0, 0.0), 1, 2, (2.0, 3.0), 32)
    assert close(box, (48, 0, 112, 96)) and obj == 0.5
    rng = random.Random(8)
    for _ in range(100):
        t = [rng.gauss(0, 5) for _ in range(5)]
        i, j = rng.randrange(13), rng.randrange(13)
        box, obj = decode_v2(t, i, j, (1.5, 2.5), 32)
        cx, cy = (box[0] + box[2]) / 64, (box[1] + box[3]) / 64
        assert j <= cx <= j + 1 and i <= cy <= i + 1 and 0 <= obj <= 1


def test_dimension_clusters():
    rng = random.Random(9)
    groups = [(1.0, 1.0), (3.0, 1.0), (1.0, 4.0)]
    shapes = [(gw * rng.uniform(0.9, 1.1), gh * rng.uniform(0.9, 1.1)) for gw, gh in groups for _ in range(30)]
    cents, assign = dimension_clusters(shapes, 3, seed=1)
    for gw, gh in groups:
        assert any(abs(cw - gw) < 0.1 * gw and abs(ch - gh) < 0.1 * gh for cw, ch in cents)
    for sh, a in zip(shapes, assign):
        assert shape_iou(sh, cents[a]) >= max(shape_iou(sh, cc) for cc in cents) - 1e-12
    assert math.isclose(shape_iou((2, 2), (1, 4)), 2 / 6)
