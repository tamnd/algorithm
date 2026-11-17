# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anchor-boxes/. The authors are listed in prov/JNRSBB.jsonl.
"""Anchor boxes: a fixed set of reference boxes at each position of a feature map.

A box is (x1, y1, x2, y2) in continuous image coordinates. The aspect ratio
r of a box is h / w, as in the Faster R-CNN code. A size sigma and a ratio r
give the box with w = sigma / sqrt(r) and h = sigma * sqrt(r), so its area is
sigma^2. Position (u, v) of a feature map with stride s has its anchors
centered at ((u + o) s, (v + o) s); the offset o is 0.5 in SSD and 0 in
torchvision, so state it. Standard library only.
"""

import math
from fractions import Fraction


def base_shapes(sizes, ratios):
    """The (w, h) of the anchors of one position, sizes outer, ratios inner."""
    shapes = []  # @line L1
    for sigma in sizes:
        for r in ratios:
            shapes.append((sigma / math.sqrt(r), sigma * math.sqrt(r)))  # @line L2
    return shapes


def anchors(wf, hf, stride, sizes, ratios, offset=0.5):
    """All anchors of a wf x hf feature map, position by position (rows, then columns)."""
    shapes = base_shapes(sizes, ratios)
    out = []  # @line L3
    for v in range(hf):  # @line L4
        for u in range(wf):
            cx, cy = (u + offset) * stride, (v + offset) * stride  # @line L5
            for w, h in shapes:
                out.append((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))  # @line L6
    return out  # @line L7


def legacy_base_anchors(base_size=16, ratios=(0.5, 1, 2), scales=(8, 16, 32)):
    """generate_anchors of the py-faster-rcnn code: inclusive pixel boxes, rounded sizes.

    Python round() rounds halves to even, as numpy.round does in the original.
    """
    w = h = base_size
    xc = yc = 0.5 * (base_size - 1)
    out = []
    for r in ratios:
        ws = round(math.sqrt(w * h / r))
        hs = round(ws * r)
        for s in scales:
            ww, hh = ws * s, hs * s
            out.append((xc - 0.5 * (ww - 1), yc - 0.5 * (hh - 1), xc + 0.5 * (ww - 1), yc + 0.5 * (hh - 1)))
    return out


def iou(a, b):
    """IoU of two boxes; a Fraction on integer or Fraction boxes."""
    iw = min(a[2], b[2]) - max(a[0], b[0])
    ih = min(a[3], b[3]) - max(a[1], b[1])
    inter = iw * ih if iw > 0 and ih > 0 else 0
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    if all(isinstance(v, (int, Fraction)) for v in (inter, union)):
        return Fraction(inter) / union
    return inter / union


def best_iou(box, anchor_list):
    """The largest IoU of the box with any anchor, by brute force."""
    return max(iou(box, a) for a in anchor_list)


def centered_iou(wh1, wh2):
    """IoU of two boxes with the same center, given only (w, h)."""
    iw, ih = min(wh1[0], wh2[0]), min(wh1[1], wh2[1])
    inter = iw * ih
    return inter / (wh1[0] * wh1[1] + wh2[0] * wh2[1] - inter)


def kmeans_shapes(shapes, k, rng, iters=50):
    """YOLOv2 dimension clusters: k-means on (w, h) with the distance 1 - centered IoU.

    The center of a cluster is the mean (w, h) of its members, the usual k-means
    update. The mean does not minimize the sum of 1 - IoU, so the loop is not
    sure to settle; it stops at a fixed point or after iters rounds.
    """
    centers = rng.sample(shapes, k)
    assign = None
    for _ in range(iters):
        new = [max(range(k), key=lambda j: (centered_iou(s, centers[j]), -j)) for s in shapes]
        if new == assign:
            break
        assign = new
        for j in range(k):
            members = [s for s, a in zip(shapes, assign) if a == j]
            if members:
                centers[j] = (sum(m[0] for m in members) / len(members),
                              sum(m[1] for m in members) / len(members))
    return sorted(centers), assign


def mean_best_iou(shapes, centers):
    """Average over the shapes of the best centered IoU with a center, the YOLOv2 score."""
    return sum(max(centered_iou(s, c) for c in centers) for s in shapes) / len(shapes)
