# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anchor-assignment/. The authors are listed in prov/RFHSZS.jsonl.
"""Anchor assignment: which anchors learn which true boxes.

A box is (x1, y1, x2, y2) in continuous coordinates. A label is 1 (positive,
the anchor learns the class and the offsets of its matched true box), 0
(negative, background) or -1 (ignored in the loss). Standard library only.

assign_max_iou is the rule of the Faster R-CNN region proposal network:
positive at IoU >= pos_thr (the code of py-faster-rcnn uses >=), negative
below neg_thr, and every anchor that ties for the best IoU of some true box is
positive too. The matched box of an anchor is always its own argmax, as in
py-faster-rcnn, Detectron2 and torchvision.
"""

import math
from fractions import Fraction


def iou(a, b):
    """IoU of two boxes; a Fraction on integer or Fraction boxes."""
    iw = min(a[2], b[2]) - max(a[0], b[0])
    ih = min(a[3], b[3]) - max(a[1], b[1])
    inter = iw * ih if iw > 0 and ih > 0 else 0
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    if all(isinstance(v, (int, Fraction)) for v in (inter, union)):
        return Fraction(inter) / union
    return inter / union


def iou_matrix(anchors, gts):
    return [[iou(a, g) for g in gts] for a in anchors]  # @line L1


def assign_max_iou(anchors, gts, pos_thr=0.7, neg_thr=0.3, best_for_gt=True):
    """Return (labels, matched): labels in {1, 0, -1} and the index of the matched true box.

    matched[i] is -1 when there is no true box. With best_for_gt=False this is
    the RetinaNet rule (0.5 and 0.4 there).
    """
    n = len(anchors)
    if not gts:
        return [0] * n, [-1] * n
    m = iou_matrix(anchors, gts)
    labels, matched, best = [], [], []
    for i in range(n):
        row = m[i]
        mi = max(row)  # @line L2
        matched.append(row.index(mi))
        best.append(mi)
        labels.append(0 if mi < neg_thr else -1)  # @line L3
    if best_for_gt:
        for j in range(len(gts)):
            bj = max(m[i][j] for i in range(n))  # @line L4
            if bj > 0:
                for i in range(n):
                    if m[i][j] == bj:
                        labels[i] = 1  # @line L5
    for i in range(n):
        if best[i] >= pos_thr:
            labels[i] = 1  # @line L6
    return labels, matched  # @line L7


def sample(labels, batch, fraction, rng):
    """Keep at most floor(fraction * batch) random positives, fill to batch with negatives."""
    pos = [i for i, v in enumerate(labels) if v == 1]
    neg = [i for i, v in enumerate(labels) if v == 0]
    n_pos = min(len(pos), int(math.floor(fraction * batch)))
    keep_pos = set(rng.sample(pos, n_pos))  # @line L8
    keep_neg = set(rng.sample(neg, min(len(neg), batch - n_pos)))
    out = []
    for i, v in enumerate(labels):
        if (v == 1 and i in keep_pos) or (v == 0 and i in keep_neg):
            out.append(v)
        else:
            out.append(-1)
    return out


def assign_ssd(anchors, gts, thr=0.5):
    """SSD matching: each true box takes its best anchor, then every anchor above thr takes its argmax.

    There is no ignore zone: all other anchors are negative. A forced anchor
    keeps the true box that forced it, as in common SSD code; a later true box
    wins when two pick the same anchor.
    """
    n = len(anchors)
    if not gts:
        return [0] * n, [-1] * n
    m = iou_matrix(anchors, gts)
    matched = [max(range(len(gts)), key=lambda j: (m[i][j], -j)) for i in range(n)]
    labels = [1 if m[i][matched[i]] > thr else 0 for i in range(n)]
    for j in range(len(gts)):
        i_best = max(range(n), key=lambda i: (m[i][j], -i))
        labels[i_best] = 1
        matched[i_best] = j
    return labels, matched


def center(b):
    return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)


def mean_std(values):
    """Mean and sample standard deviation (n - 1), as torch.std in the ATSS code."""
    n = len(values)
    mu = sum(values) / n
    if n < 2:
        return mu, 0.0
    return mu, math.sqrt(sum((v - mu) ** 2 for v in values) / (n - 1))


def assign_atss(levels, gts, k=9):
    """Adaptive training sample selection of Zhang et al. (CVPR 2020).

    levels is a list of anchor lists, one per pyramid level. For each true box,
    take the k anchors of each level whose centers are closest to its center,
    set the threshold to the mean plus the standard deviation of their IoUs,
    and keep those at or above it whose center lies inside the box. An anchor
    that is positive for several boxes takes the one with the highest IoU.
    Returns labels in {1, 0} and matched indices over the flat anchor list.
    """
    flat = [a for level in levels for a in level]
    offsets, start = [], 0
    for level in levels:
        offsets.append(start)
        start += len(level)
    labels, matched, best = [0] * len(flat), [-1] * len(flat), [-1.0] * len(flat)
    for j, g in enumerate(gts):
        gx, gy = center(g)
        cand = []
        for li, level in enumerate(levels):
            dist = sorted(range(len(level)),
                          key=lambda i: ((center(level[i])[0] - gx) ** 2 + (center(level[i])[1] - gy) ** 2, i))
            cand.extend(offsets[li] + i for i in dist[:k])
        ious = [float(iou(flat[i], g)) for i in cand]
        mu, sd = mean_std(ious)
        thr = mu + sd
        for i, v in zip(cand, ious):
            cx, cy = center(flat[i])
            inside = g[0] < cx < g[2] and g[1] < cy < g[3]
            if v >= thr and inside and v > best[i]:
                labels[i], matched[i], best[i] = 1, j, v
    return labels, matched
