# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/detection-mean-average-precision/. The authors are listed in prov/ZNZ16Q.jsonl.
"""Average precision (AP) and mean average precision (mAP) for detection.

A detection is (image_id, score, box) and a box is (x1, y1, x2, y2) in
continuous coordinates. Ground truth is a dict image_id -> list of boxes, for
one class. Two matching rules are given:

    match_voc   the rule of the PASCAL VOC development kit: a detection takes
                the ground-truth box with the largest IoU; it is a true
                positive if that IoU is above the threshold and the box is
                not used yet, and a false positive otherwise. A match with a
                box marked "difficult" is ignored.
    match_coco  the rule of the COCO API: a detection takes the unused
                ground-truth box with the largest IoU among those with IoU at
                least the threshold.

Three ways to turn the ranked list into one number are given: the 11-point
AP of VOC 2007, the all-point AP of VOC 2010 and later, and the 101-point AP
of COCO. All values are exact Fractions when the boxes are integers.
Standard library only.
"""

from fractions import Fraction


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


def rank(dets):
    """Indices of the detections by score, highest first, ties by index."""
    return sorted(range(len(dets)), key=lambda k: (-dets[k][1], k))


def match_voc(dets, gts, threshold=Fraction(1, 2), difficult=None):
    """Return (flags, npos). flags[r] is True (TP), False (FP) or None
    (ignored) for the detection of rank r; npos counts the boxes that are
    not difficult.
    """
    difficult = difficult or {}
    order = rank(dets)  # @line L1
    used = {img: [False] * len(boxes) for img, boxes in gts.items()}  # @line L2
    flags = []
    for k in order:  # @line L3
        img, _, box = dets[k]
        cands = gts.get(img, [])
        best, j = -1, -1
        for g, gbox in enumerate(cands):  # @line L4
            o = iou(box, gbox)
            if o > best:
                best, j = o, g
        diff = difficult.get(img, [False] * len(cands))
        if j >= 0 and best > threshold:  # @line L5
            if diff[j]:
                flags.append(None)
            elif not used[img][j]:
                used[img][j] = True
                flags.append(True)
            else:
                flags.append(False)  # @line L6
        else:
            flags.append(False)
    npos = sum(1 for img, boxes in gts.items() for g in range(len(boxes))
               if not difficult.get(img, [False] * len(boxes))[g])
    return flags, npos


def match_coco(dets, gts, threshold=Fraction(1, 2)):
    """Return (flags, npos) with the matching rule of the COCO API (no crowd
    regions and no area ranges)."""
    used = {img: [False] * len(boxes) for img, boxes in gts.items()}
    flags = []
    for k in rank(dets):
        img, _, box = dets[k]
        best, j = None, -1
        for g, gbox in enumerate(gts.get(img, [])):
            if used[img][g]:
                continue
            o = iou(box, gbox)
            if o >= threshold and (best is None or o > best):
                best, j = o, g
        if j >= 0:
            used[img][j] = True
            flags.append(True)
        else:
            flags.append(False)
    npos = sum(len(b) for b in gts.values())
    return flags, npos


def precision_recall(flags, npos):
    """Precision and recall after each rank; ignored detections are skipped."""
    prec, rec, tp, fp = [], [], 0, 0
    for f in flags:
        if f is None:
            continue
        if f:
            tp += 1
        else:
            fp += 1
        prec.append(Fraction(tp, tp + fp))  # @line L7
        rec.append(Fraction(tp, npos) if npos else Fraction(0))
    return prec, rec


def interpolated(prec, rec, r):
    """p_interp(r): the largest precision at a recall of at least r, else 0."""
    vals = [p for p, q in zip(prec, rec) if q >= r]  # @line L8
    return max(vals) if vals else Fraction(0)


def ap_all_points(prec, rec):
    """VOC 2010 and later: the area under the interpolated curve."""
    total, last = Fraction(0), Fraction(0)
    for k in range(len(rec)):
        if rec[k] > last:
            total += (rec[k] - last) * interpolated(prec, rec, rec[k])  # @line L9
            last = rec[k]
    return total


def ap_11_points(prec, rec):
    """VOC 2007: the mean of p_interp at the recalls 0, 0.1, ..., 1."""
    return sum(interpolated(prec, rec, Fraction(k, 10)) for k in range(11)) / 11


def ap_101_points(prec, rec):
    """COCO: the mean of p_interp at the recalls 0, 0.01, ..., 1."""
    return sum(interpolated(prec, rec, Fraction(k, 100)) for k in range(101)) / 101


def average_precision(dets, gts, threshold=Fraction(1, 2), rule="voc", points="all",
                      difficult=None):
    """AP of one class."""
    if rule == "voc":
        flags, npos = match_voc(dets, gts, threshold, difficult)
    else:
        flags, npos = match_coco(dets, gts, threshold)
    prec, rec = precision_recall(flags, npos)
    if points == "all":
        return ap_all_points(prec, rec)
    if points == 11:
        return ap_11_points(prec, rec)
    return ap_101_points(prec, rec)


def mean_average_precision(per_class, threshold=Fraction(1, 2), rule="voc", points="all"):
    """mAP: the mean of AP over classes. per_class maps a class name to a
    pair (dets, gts)."""
    aps = [average_precision(d, g, threshold, rule, points) for d, g in per_class.values()]
    return sum(aps) / len(aps)


COCO_THRESHOLDS = [Fraction(50 + 5 * k, 100) for k in range(10)]


def coco_map(per_class):
    """COCO AP: the mean over the IoU thresholds 0.50, 0.55, ..., 0.95 and
    over classes, with COCO matching and 101 recall points."""
    vals = [mean_average_precision(per_class, t, "coco", 101) for t in COCO_THRESHOLDS]
    return sum(vals) / len(vals)
