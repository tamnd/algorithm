# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mean-intersection-over-union/. The authors are listed in prov/7XWT5K.jsonl.

"""Mean intersection over union (mIoU) for semantic segmentation.

A label image is a list of rows, img[v][u]. Ground-truth values are class
indices 0 .. K - 1 or the void index (255 by default), which is ignored.
Predicted values must be class indices. All counts are integers and all scores
are Fractions, so results are exact. Standard library only.
"""

from fractions import Fraction

VOID = 255


def confusion_matrix(pairs, k, void=VOID):
    """Return the K x K matrix n with n[i][j] = pixels of true class i predicted as j, over all pairs."""
    n = [[0] * k for _ in range(k)]  # @line L1
    for gt, pred in pairs:  # @line L2
        for grow, prow in zip(gt, pred):
            for g, p in zip(grow, prow):
                if g == void:  # @line L3
                    continue
                if not (0 <= g < k and 0 <= p < k):
                    raise ValueError("label out of range")
                n[g][p] += 1  # @line L4
    return n


def class_iou(n):
    """Return the IoU of each class as a Fraction, or None for a class that is neither true nor predicted."""
    k = len(n)
    out = []
    for i in range(k):
        t = sum(n[i]) + sum(n[j][i] for j in range(k)) - n[i][i]
        out.append(Fraction(n[i][i], t) if t > 0 else None)
    return out


def mean_iou(n):
    """Mean of the class IoUs over the classes with a defined IoU, or None if there is none."""
    k = len(n)
    s, c = Fraction(0), 0  # @line L5
    for i in range(k):  # @line L6
        t = sum(n[i]) + sum(n[j][i] for j in range(k)) - n[i][i]  # @line L7
        if t > 0:  # @line L8
            s += Fraction(n[i][i], t)
            c += 1
    return s / c if c else None  # @line L9


def pixel_accuracy(n):
    total = sum(map(sum, n))
    return Fraction(sum(n[i][i] for i in range(len(n))), total) if total else None


def mean_accuracy(n):
    vals = [Fraction(n[i][i], sum(n[i])) for i in range(len(n)) if sum(n[i])]
    return sum(vals, Fraction(0)) / len(vals) if vals else None


def frequency_weighted_iou(n):
    total = sum(map(sum, n))
    ious = class_iou(n)
    return sum((Fraction(sum(n[i]), total) * ious[i] for i in range(len(n)) if sum(n[i])), Fraction(0))


def dice(n):
    """Per-class Dice (F1) score 2 n_ii / (|G_i| + |P_i|), or None."""
    k = len(n)
    out = []
    for i in range(k):
        s = sum(n[i]) + sum(n[j][i] for j in range(k))
        out.append(Fraction(2 * n[i][i], s) if s else None)
    return out


def per_image_mean_iou(pairs, k, void=VOID):
    """Average over images of the mIoU of each image: a different score, shown for contrast."""
    vals = [mean_iou(confusion_matrix([pair], k, void)) for pair in pairs]
    vals = [x for x in vals if x is not None]
    return sum(vals, Fraction(0)) / len(vals) if vals else None
