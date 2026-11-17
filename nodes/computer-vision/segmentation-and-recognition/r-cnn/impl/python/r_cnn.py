# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/r-cnn/. The authors are listed in prov/4YN1M9.jsonl.
"""R-CNN detection around a given feature extractor.

The CNN is not part of this file. The caller passes `features`, a function
from a warped patch (a list of rows) to a feature vector; the tests pass a
small hand-written function. This file has the parts of R-CNN that are not
learned: the context box and the warp of each proposal (Appendix A of the
paper), the linear SVM scores, the class-specific box decoding, the greedy
non-maximum suppression for each class, and the three labeling rules used in
training (fine-tuning, SVM and box regression).

Boxes are (x1, y1, x2, y2) in continuous pixel coordinates: pixel (u, v)
covers [u, u + 1) x [v, v + 1) and its center is (u + 0.5, v + 0.5). Images
are lists of rows of numbers, indexed img[v][u]. Standard library only.
"""

import math
from fractions import Fraction


def area(b):
    return max(0, b[2] - b[0]) * max(0, b[3] - b[1])


def iou(a, b):
    """Intersection over union of two boxes; exact on ints and Fractions."""
    iw = min(a[2], b[2]) - max(a[0], b[0])
    ih = min(a[3], b[3]) - max(a[1], b[1])
    if iw <= 0 or ih <= 0:
        return 0
    inter = iw * ih
    union = area(a) + area(b) - inter
    if isinstance(inter, int) and isinstance(union, int):
        return Fraction(inter, union)
    return inter / union


def context_box(box, size=227, pad=16):
    """Grow the box about its center so that, warped to size x size, the
    original box covers [pad, size - pad] and pad pixels of context surround it."""
    x1, y1, x2, y2 = box
    f = size / (size - 2 * pad)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    hw, hh = (x2 - x1) * f / 2, (y2 - y1) * f / 2
    return (cx - hw, cy - hh, cx + hw, cy + hh)


def image_mean(img):
    return sum(sum(row) for row in img) / (len(img) * len(img[0]))


def sample(img, x, y, fill):
    """Bilinear sample at the continuous point (x, y); fill outside the image."""
    h, w = len(img), len(img[0])
    if x < 0 or y < 0 or x >= w or y >= h:
        return fill
    fx = min(max(x - 0.5, 0.0), w - 1.0)
    fy = min(max(y - 0.5, 0.0), h - 1.0)
    u0, v0 = int(math.floor(fx)), int(math.floor(fy))
    u1, v1 = min(u0 + 1, w - 1), min(v0 + 1, h - 1)
    a, b = fx - u0, fy - v0
    top = (1 - a) * img[v0][u0] + a * img[v0][u1]
    bot = (1 - a) * img[v1][u0] + a * img[v1][u1]
    return (1 - b) * top + b * bot


def warp(img, box, size, fill):
    """Scale the box, without keeping its aspect ratio, to a size x size patch."""
    x1, y1, x2, y2 = box
    sx, sy = (x2 - x1) / size, (y2 - y1) / size
    return [[sample(img, x1 + (u + 0.5) * sx, y1 + (v + 0.5) * sy, fill) for u in range(size)]
            for v in range(size)]


def decode(p, d):
    """Apply class-specific offsets d = (dx, dy, dw, dh) to a proposal p (Appendix C)."""
    pw, ph = p[2] - p[0], p[3] - p[1]
    px, py = p[0] + pw / 2, p[1] + ph / 2
    gx, gy = px + pw * d[0], py + ph * d[1]
    gw, gh = pw * math.exp(d[2]), ph * math.exp(d[3])
    return (gx - gw / 2, gy - gh / 2, gx + gw / 2, gy + gh / 2)


def greedy_nms(boxes, scores, thr):
    """Indices kept by greedy NMS: take the best box, drop boxes with IoU above thr with it."""
    order = sorted(range(len(boxes)), key=lambda i: (-scores[i], i))
    keep = []
    for i in order:
        if all(iou(boxes[i], boxes[k]) <= thr for k in keep):
            keep.append(i)
    return keep


def detect(img, proposals, features, svm, regressors=None, nms_thr=0.3, size=227, pad=16):
    """R-CNN test time. svm[c] = (w, b) for each object class c; regressors[c] maps a
    feature vector to offsets, or is None. Returns, for each class, a list of
    (score, box, proposal index), best first."""
    fill = image_mean(img)
    feats = []
    for p in proposals:  # @line L1
        patch = warp(img, context_box(p, size, pad), size, fill)  # @line L2
        feats.append(features(patch))  # @line L3
    out = {}
    for c, (w, b) in svm.items():  # @line L4
        scores = [sum(wi * fi for wi, fi in zip(w, f)) + b for f in feats]  # @line L5
        if regressors and regressors.get(c):
            boxes = [decode(p, regressors[c](f)) for p, f in zip(proposals, feats)]  # @line L6
        else:
            boxes = list(proposals)
        keep = greedy_nms(boxes, scores, nms_thr)  # @line L7
        out[c] = [(scores[i], boxes[i], i) for i in keep]
    return out  # @line L8


def finetune_labels(proposals, gts, gt_classes, thr=0.5):
    """Fine-tuning label: the class of the best-overlapping truth if IoU >= thr, else 0."""
    labels = []
    for p in proposals:
        best, lab = 0, 0
        for g, c in zip(gts, gt_classes):
            o = iou(p, g)
            if o > best:
                best, lab = o, c
        labels.append(lab if best >= thr else 0)
    return labels


def svm_examples(proposals, gts, gt_classes, c, neg_thr=0.3):
    """SVM training set for class c: the truths of class c are the positives, and the
    proposals with IoU below neg_thr with every truth of class c are the negatives.
    The other proposals are ignored."""
    pos = [g for g, k in zip(gts, gt_classes) if k == c]
    neg = [i for i, p in enumerate(proposals) if all(iou(p, g) < neg_thr for g in pos)]
    return pos, neg


def regression_pairs(proposals, gts, thr=0.6):
    """Pairs (proposal index, truth index) for box regression: the best truth, if IoU > thr."""
    pairs = []
    for i, p in enumerate(proposals):
        if not gts:
            break
        j = max(range(len(gts)), key=lambda k: (iou(p, gts[k]), -k))
        if iou(p, gts[j]) > thr:
            pairs.append((i, j))
    return pairs
