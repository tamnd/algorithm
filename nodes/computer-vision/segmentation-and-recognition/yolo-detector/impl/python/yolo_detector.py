# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yolo-detector/. The authors are listed in prov/D6VPA6.jsonl.
"""YOLO (version 1, with the box decoding and anchor clusters of version 2)
around given network outputs.

The convolutional network is not part of this file. The caller passes the
output tensor as out[i][j], the list of B * 5 + C numbers of grid cell (row i,
column j): for each of the B boxes x, y, w, h and a confidence, then C class
probabilities. The tests build it by hand or with a fixed seed. This file has
the parts that are not learned: the decoding of the tensor, the class-specific
scores and the NMS for each class at test time, the version 1 training loss,
the version 2 decoding of offsets against anchors, and the k-means clustering
of box shapes with the distance 1 - IoU.

Boxes are (x1, y1, x2, y2) in pixels. Standard library only.
"""

import math
import random
from fractions import Fraction


def iou(a, b):
    """Intersection over union; exact Fractions on integer boxes."""
    iw = min(a[2], b[2]) - max(a[0], b[0])
    ih = min(a[3], b[3]) - max(a[1], b[1])
    if iw <= 0 or ih <= 0:
        return 0
    inter = iw * ih
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    if isinstance(inter, int) and isinstance(union, int):
        return Fraction(inter, union)
    return inter / union


def cell_box(i, j, x, y, w, h, s, img_w, img_h):
    """Version 1 decoding: x and y are offsets inside cell (i, j), and w and h
    are fractions of the image size."""
    cx, cy = (j + x) / s * img_w, (i + y) / s * img_h
    bw, bh = w * img_w, h * img_h
    return (cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2)


def greedy_nms(boxes, scores, thr):
    order = sorted(range(len(boxes)), key=lambda i: (-scores[i], i))
    keep = []
    for i in order:
        if all(iou(boxes[i], boxes[k]) <= thr for k in keep):
            keep.append(i)
    return keep


def detect(out, s, b, c, img_w, img_h, score_thr=0.2, nms_thr=0.5):
    """Test-time YOLO v1. Returns a list of (score, class, box), best first."""
    # out is the S x S x (5B + C) output of the network.
    assert len(out) == s and all(len(row) == s and all(len(v) == 5 * b + c for v in row)
                                 for row in out)  # @line L1
    boxes, scores = [], []
    for i in range(s):
        for j in range(s):
            v = out[i][j]
            probs = v[5 * b:]
            for k in range(b):
                x, y, w, h, conf = v[5 * k:5 * k + 5]
                boxes.append(cell_box(i, j, x, y, max(w, 0.0), max(h, 0.0), s, img_w, img_h))  # @line L2
                scores.append([p * conf for p in probs])  # @line L3
    dets = []
    for cl in range(c):  # @line L4
        cand = [n for n in range(len(boxes)) if scores[n][cl] > score_thr]  # @line L5
        keep = greedy_nms([boxes[n] for n in cand], [scores[n][cl] for n in cand], nms_thr)  # @line L6
        dets.extend((scores[cand[k]][cl], cl, boxes[cand[k]]) for k in keep)  # @line L7
    dets.sort(key=lambda d: (-d[0], d[1]))
    return dets  # @line L8


def yolo_v1_loss(out, gts, labels, s, b, c, img_w, img_h, l_coord=5.0, l_noobj=0.5):
    """The sum-squared loss of YOLO v1 on given outputs.

    The cell that holds the center of a truth box is responsible for it; if two
    centers fall in one cell, the first truth is kept. In that cell, the
    predictor whose box has the largest IoU with the truth (ties to the lower
    index) is responsible, and its confidence target is that IoU. Every other
    predictor gets the no-object term."""
    owner = {}
    for g, cl in zip(gts, labels):
        cx, cy = (g[0] + g[2]) / 2, (g[1] + g[3]) / 2
        i = min(int(cy / img_h * s), s - 1)
        j = min(int(cx / img_w * s), s - 1)
        if (i, j) not in owner:
            owner[(i, j)] = (g, cl, cx * s / img_w - j, cy * s / img_h - i,
                             (g[2] - g[0]) / img_w, (g[3] - g[1]) / img_h)
    loss = 0.0
    for i in range(s):
        for j in range(s):
            v = out[i][j]
            preds = [v[5 * k:5 * k + 5] for k in range(b)]
            if (i, j) not in owner:
                loss += l_noobj * sum(p[4] ** 2 for p in preds)
                continue
            g, cl, tx, ty, tw, th = owner[(i, j)]
            ious = [iou(cell_box(i, j, p[0], p[1], max(p[2], 0.0), max(p[3], 0.0), s, img_w, img_h), g)
                    for p in preds]
            r = max(range(b), key=lambda k: (ious[k], -k))
            for k, p in enumerate(preds):
                if k != r:
                    loss += l_noobj * p[4] ** 2
                    continue
                x, y, w, h, conf = p
                loss += l_coord * ((x - tx) ** 2 + (y - ty) ** 2)
                loss += l_coord * ((math.sqrt(max(w, 0.0)) - math.sqrt(tw)) ** 2
                                   + (math.sqrt(max(h, 0.0)) - math.sqrt(th)) ** 2)
                loss += (conf - float(ious[r])) ** 2
            loss += sum((v[5 * b + k] - (1.0 if k == cl else 0.0)) ** 2 for k in range(c))
    return loss


def sigmoid(t):
    return 1 / (1 + math.exp(-t))


def decode_v2(t, i, j, prior, stride):
    """Version 2 decoding of t = (t_x, t_y, t_w, t_h, t_o) at cell (row i, column j)
    with an anchor prior = (p_w, p_h) in grid units. Returns (box in pixels, objectness)."""
    bx, by = sigmoid(t[0]) + j, sigmoid(t[1]) + i
    bw, bh = prior[0] * math.exp(t[2]), prior[1] * math.exp(t[3])
    box = ((bx - bw / 2) * stride, (by - bh / 2) * stride, (bx + bw / 2) * stride, (by + bh / 2) * stride)
    return box, sigmoid(t[4])


def shape_iou(a, b):
    """IoU of two shapes (w, h) placed at the same center."""
    inter = min(a[0], b[0]) * min(a[1], b[1])
    return inter / (a[0] * a[1] + b[0] * b[1] - inter)


def dimension_clusters(shapes, k, seed=0, iters=100):
    """k-means on box shapes with the distance 1 - IoU and the mean as the center.
    Returns (centroids, assignment)."""
    rng = random.Random(seed)
    cents = rng.sample(list(shapes), k)
    assign = None
    for _ in range(iters):
        new = [max(range(k), key=lambda c: (shape_iou(sh, cents[c]), -c)) for sh in shapes]
        if new == assign:
            break
        assign = new
        for c in range(k):
            members = [sh for sh, a in zip(shapes, assign) if a == c]
            if members:
                cents[c] = (sum(m[0] for m in members) / len(members),
                            sum(m[1] for m in members) / len(members))
    return cents, assign
