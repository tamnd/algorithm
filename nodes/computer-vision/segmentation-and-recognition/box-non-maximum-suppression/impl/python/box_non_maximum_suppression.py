# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/box-non-maximum-suppression/. The authors are listed in prov/5JRR0P.jsonl.
"""Greedy non-maximum suppression (NMS) of scored detection boxes.

A box is (x1, y1, x2, y2) in continuous image coordinates. Boxes are ranked by
score, highest first, with ties broken by the smaller index. The best box is
kept, every later box whose overlap with it is above the threshold is removed,
and the loop goes on with the next box that is still there. The overlap is IoU
by default; any function overlap(kept_box, other_box) can be given instead.
Standard library only. Cost: O(n log n) for the sort plus one overlap per
pair (kept box, later box), so O(n k) for k kept boxes and O(n^2) in the
worst case.
"""

from fractions import Fraction
from itertools import combinations


def iou(a, b):
    """IoU of two boxes; exact (a Fraction) on integer boxes."""
    iw = min(a[2], b[2]) - max(a[0], b[0])
    ih = min(a[3], b[3]) - max(a[1], b[1])
    inter = iw * ih if iw > 0 and ih > 0 else 0
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    if union == 0:
        return 0
    if isinstance(inter, int) and isinstance(union, int):
        return Fraction(inter, union)
    return inter / union


def coverage(kept, other):
    """The part of `other` that `kept` covers, |kept & other| / |other|.

    This is the overlap of the deformable part model code, not IoU.
    """
    iw = min(kept[2], other[2]) - max(kept[0], other[0])
    ih = min(kept[3], other[3]) - max(kept[1], other[1])
    inter = iw * ih if iw > 0 and ih > 0 else 0
    area = (other[2] - other[0]) * (other[3] - other[1])
    if isinstance(inter, int) and isinstance(area, int):
        return Fraction(inter, area)
    return inter / area


def rank_order(scores):
    """Indices sorted by score, highest first; ties go to the smaller index."""
    return sorted(range(len(scores)), key=lambda i: (-scores[i], i))


def greedy_nms(boxes, scores, threshold=0.5, overlap=iou, max_keep=None):
    """Return the indices of the kept boxes, in decreasing score order."""
    n = len(boxes)
    order = rank_order(scores)  # @line L1
    keep, removed = [], [False] * n  # @line L2
    for pos, i in enumerate(order):  # @line L3
        if removed[i]:  # @line L4
            continue
        keep.append(i)  # @line L5
        if max_keep is not None and len(keep) == max_keep:
            break
        for j in order[pos + 1:]:  # @line L6
            if not removed[j] and overlap(boxes[i], boxes[j]) > threshold:  # @line L7
                removed[j] = True  # @line L8
    return keep  # @line L9


def batched_nms(boxes, scores, labels, threshold=0.5, overlap=iou):
    """Class-aware NMS: run greedy NMS inside each label separately.

    The result is the union of the kept sets, in decreasing score order.
    """
    groups = {}
    for i, lab in enumerate(labels):
        groups.setdefault(lab, []).append(i)
    keep = []
    for idx in groups.values():
        sub = greedy_nms([boxes[i] for i in idx], [scores[i] for i in idx], threshold, overlap)
        keep.extend(idx[k] for k in sub)
    pos = {i: r for r, i in enumerate(rank_order(scores))}
    return sorted(keep, key=lambda i: pos[i])


def fast_nms(boxes, scores, threshold=0.5, overlap=iou):
    """Fast NMS (Bolya et al. 2019): remove a box if ANY higher-ranked box,
    kept or not, overlaps it above the threshold. It removes at least the
    boxes that greedy NMS removes, and sometimes more.
    """
    order = rank_order(scores)
    keep = []
    for r, j in enumerate(order):
        if all(overlap(boxes[i], boxes[j]) <= threshold for i in order[:r]):
            keep.append(j)
    return keep


def is_greedy_nms_output(boxes, scores, keep, threshold=0.5, overlap=iou):
    """Check the two conditions that characterize the greedy NMS output:
    (i) no kept box is removed by a higher-ranked kept box, and
    (ii) every other box is removed by some higher-ranked kept box.
    """
    order = rank_order(scores)
    rank = {i: r for r, i in enumerate(order)}
    ks = set(keep)
    for j in range(len(boxes)):
        hit = any(rank[i] < rank[j] and overlap(boxes[i], boxes[j]) > threshold for i in ks)
        if (j in ks) == hit:
            return False
    return True


def brute_force_nms(boxes, scores, threshold=0.5, overlap=iou):
    """Try every subset and return the one subset that meets both conditions,
    in decreasing score order. Exponential; for tests on tiny inputs only.
    """
    n = len(boxes)
    found = []
    for size in range(n + 1):
        for sub in combinations(range(n), size):
            if is_greedy_nms_output(boxes, scores, sub, threshold, overlap):
                found.append(sub)
    if len(found) != 1:
        raise AssertionError("the characterization must give exactly one subset")
    pos = {i: r for r, i in enumerate(rank_order(scores))}
    return sorted(found[0], key=lambda i: pos[i])
