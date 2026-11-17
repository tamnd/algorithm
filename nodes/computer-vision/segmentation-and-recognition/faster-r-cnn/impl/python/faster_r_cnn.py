# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/faster-r-cnn/. The authors are listed in prov/5WFTBK.jsonl.
"""Faster R-CNN around given network outputs.

The backbone, the region proposal network (RPN) head and the detection head
are not part of this file. The caller passes the RPN outputs as dicts keyed
by anchor index: an objectness score and four offsets per anchor. The tests
build them by hand or with a fixed seed. This file has the parts that are not
learned: the anchors, the proposal step (decode, clip, drop small boxes,
top-N, NMS, top-N), the anchor labels and the mini-batch sampling for RPN
training, the RPN loss, and the second-stage decoding and NMS on given class
scores and offsets.

Boxes are (x1, y1, x2, y2) in pixels of the scaled image. Standard library only.
"""

import math
from fractions import Fraction


def area(b):
    return max(0, b[2] - b[0]) * max(0, b[3] - b[1])


def iou(a, b):
    """Intersection over union; exact Fractions on integer boxes."""
    iw = min(a[2], b[2]) - max(a[0], b[0])
    ih = min(a[3], b[3]) - max(a[1], b[1])
    if iw <= 0 or ih <= 0:
        return 0
    inter = iw * ih
    union = area(a) + area(b) - inter
    if isinstance(inter, int) and isinstance(union, int):
        return Fraction(inter, union)
    return inter / union


def anchors(feat_w, feat_h, stride, sizes=(128, 256, 512), ratios=(0.5, 1, 2)):
    """k = len(sizes) * len(ratios) anchors at each feature cell, centered on the cell.
    A ratio is height / width, and an anchor of size s has area s^2. The order is
    row, column, then the k shapes, so anchor index = (row * feat_w + col) * k + shape."""
    shapes = []
    for r in ratios:
        for s in sizes:
            w, h = s / math.sqrt(r), s * math.sqrt(r)
            shapes.append((w, h))
    out = []
    for row in range(feat_h):
        for col in range(feat_w):
            cx, cy = (col + 0.5) * stride, (row + 0.5) * stride
            for w, h in shapes:
                out.append((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))
    return out


def decode(a, t):
    w, h = a[2] - a[0], a[3] - a[1]
    x, y = a[0] + w / 2, a[1] + h / 2
    gx, gy, gw, gh = x + w * t[0], y + h * t[1], w * math.exp(t[2]), h * math.exp(t[3])
    return (gx - gw / 2, gy - gh / 2, gx + gw / 2, gy + gh / 2)


def encode(a, g):
    w, h = a[2] - a[0], a[3] - a[1]
    gw, gh = g[2] - g[0], g[3] - g[1]
    return ((g[0] + g[2] - a[0] - a[2]) / 2 / w, (g[1] + g[3] - a[1] - a[3]) / 2 / h,
            math.log(gw / w), math.log(gh / h))


def clip(b, img_w, img_h):
    return (min(max(b[0], 0), img_w), min(max(b[1], 0), img_h),
            min(max(b[2], 0), img_w), min(max(b[3], 0), img_h))


def greedy_nms(boxes, scores, thr, max_keep=None):
    order = sorted(range(len(boxes)), key=lambda i: (-scores[i], i))
    keep = []
    for i in order:
        if max_keep is not None and len(keep) >= max_keep:
            break
        if all(iou(boxes[i], boxes[k]) <= thr for k in keep):
            keep.append(i)
    return keep


def rpn_proposals(anchor_list, scores, deltas, img_w, img_h, min_size=16, pre_nms=6000,
                  nms_thr=0.7, post_nms=300):
    """The proposal step of the RPN. Returns a list of (score, box), best first."""
    boxes = [clip(decode(a, d), img_w, img_h) for a, d in zip(anchor_list, deltas)]  # @line L3
    cand = [i for i, b in enumerate(boxes)
            if b[2] - b[0] >= min_size and b[3] - b[1] >= min_size]  # @line L4
    cand.sort(key=lambda i: (-scores[i], i))
    cand = cand[:pre_nms]  # @line L5
    keep = greedy_nms([boxes[i] for i in cand], [scores[i] for i in cand], nms_thr, post_nms)  # @line L6
    return [(scores[cand[j]], boxes[cand[j]]) for j in keep]


def detect(proposals, head, img_w, img_h, nms_thr=0.3, score_thr=0.05):
    """Second stage on the proposals. head(box) returns (class probabilities with
    background first, K lists of 4 offsets). Returns {class: [(score, box)]}."""
    outs = [head(b) for _, b in proposals]  # @line L7
    if not outs:
        return {}
    out = {}
    for k in range(1, len(outs[0][0])):
        cand = [i for i, (p, _) in enumerate(outs) if p[k] > score_thr]
        boxes = [clip(decode(proposals[i][1], outs[i][1][k - 1]), img_w, img_h) for i in cand]
        scores = [outs[i][0][k] for i in cand]
        out[k] = [(scores[j], boxes[j]) for j in greedy_nms(boxes, scores, nms_thr)]
    return out  # @line L8


def faster_rcnn(feat_w, feat_h, stride, rpn_scores, rpn_deltas, head, img_w, img_h, **kw):
    """The whole test-time pipeline on given network outputs."""
    # rpn_scores and rpn_deltas are the outputs of the backbone and the RPN head.
    assert len(rpn_scores) == len(rpn_deltas)  # @line L1
    a = anchors(feat_w, feat_h, stride, kw.get("sizes", (128, 256, 512)),
                kw.get("ratios", (0.5, 1, 2)))  # @line L2
    props = rpn_proposals(a, rpn_scores, rpn_deltas, img_w, img_h, kw.get("min_size", 16),
                          kw.get("pre_nms", 6000), kw.get("rpn_nms", 0.7), kw.get("post_nms", 300))
    return props, detect(props, head, img_w, img_h, kw.get("nms", 0.3), kw.get("score_thr", 0.05))


def label_anchors(anchor_list, gts, img_w, img_h, pos_thr=0.7, neg_thr=0.3):
    """RPN training labels: 1 positive, 0 negative, -1 ignored, and the matched truth.
    Anchors that cross the image border are ignored. A positive has IoU >= pos_thr
    with some truth, or is an anchor of largest IoU for some truth (if that IoU is
    above zero); a negative has IoU < neg_thr with every truth."""
    inside = [a[0] >= 0 and a[1] >= 0 and a[2] <= img_w and a[3] <= img_h for a in anchor_list]
    labels = [-1] * len(anchor_list)
    match = [None] * len(anchor_list)
    if not gts:
        return [0 if ok else -1 for ok in inside], match
    ious = [[iou(a, g) for g in gts] if ok else None for a, ok in zip(anchor_list, inside)]
    for i, row in enumerate(ious):
        if row is None:
            continue
        j = max(range(len(gts)), key=lambda k: (row[k], -k))
        match[i] = j
        if row[j] < neg_thr:
            labels[i] = 0
        if row[j] >= pos_thr:
            labels[i] = 1
    for j in range(len(gts)):
        best = max((row[j] for row in ious if row is not None), default=0)
        if best > 0:
            for i, row in enumerate(ious):
                if row is not None and row[j] == best:
                    labels[i], match[i] = 1, j
    return labels, match


def sample_anchors(labels, rng, batch=256):
    """Up to batch / 2 positives, the rest negatives; the others become ignored (-1)."""
    pos = [i for i, v in enumerate(labels) if v == 1]
    neg = [i for i, v in enumerate(labels) if v == 0]
    pos = set(rng.sample(pos, min(len(pos), batch // 2)))
    neg = set(rng.sample(neg, min(len(neg), batch - len(pos))))
    return [v if (i in pos or i in neg) else -1 for i, v in enumerate(labels)]


def smooth_l1(x):
    return 0.5 * x * x if abs(x) < 1 else abs(x) - 0.5


def rpn_loss(probs, deltas, labels, targets, n_reg, lam=10.0):
    """(1/N_cls) sum log loss + lam (1/N_reg) sum over positives of smooth L1, where
    N_cls is the number of sampled anchors and n_reg the number of anchor locations."""
    used = [i for i, v in enumerate(labels) if v >= 0]
    if not used:
        return 0.0
    cls = -sum(math.log(probs[i] if labels[i] == 1 else 1 - probs[i]) for i in used) / len(used)
    reg = sum(smooth_l1(a - b) for i in used if labels[i] == 1 for a, b in zip(deltas[i], targets[i]))
    return cls + lam * reg / n_reg
