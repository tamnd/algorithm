# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/soft-nms/. The authors are listed in prov/CXYXEQ.jsonl.
"""Soft-NMS (Bodla et al. 2017): rescore overlapping detections instead of
removing them.

A box is (x1, y1, x2, y2) in continuous image coordinates and scores are
nonnegative. The loop picks the box with the highest current score, puts it
in the output with that score, and multiplies the score of every remaining
box by a decay f(IoU) in [0, 1]. A box whose score falls below s_min is
dropped. The decay rules are those of the paper:

    linear    f(o) = 1 if o < N_t, else 1 - o
    gaussian  f(o) = exp(-o * o / sigma)
    hard      f(o) = 1 if o < N_t, else 0    (greedy NMS with o >= N_t)

Standard library only. Cost: one overlap and one decay per pair (selected
box, remaining box), so O(n^2) time in the worst case and O(n) extra space.
"""

import math
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


def make_decay(method="linear", nt=0.3, sigma=0.5):
    """Return the decay function f(o) of one of the three rules."""
    if method == "linear":
        return lambda o: 1 if o < nt else 1 - o
    if method == "gaussian":
        return lambda o: math.exp(-(o * o) / sigma)
    if method == "hard":
        return lambda o: 1 if o < nt else 0
    raise ValueError("unknown method: %r" % (method,))


def soft_nms(boxes, scores, method="linear", nt=0.3, sigma=0.5, s_min=0.001,
             overlap=iou, decay=None):
    """Return a list of (index, new score) pairs in the order of selection.

    The new scores are nonincreasing along the list. Ties in the current
    score go to the smaller index.
    """
    f = decay if decay is not None else make_decay(method, nt, sigma)
    out, cur, rest = [], list(scores), list(range(len(boxes)))  # @line L1
    while rest:  # @line L2
        m = min(rest, key=lambda i: (-cur[i], i))  # @line L3
        rest.remove(m)  # @line L4
        out.append((m, cur[m]))
        survivors = []
        for i in rest:  # @line L5
            o = overlap(boxes[m], boxes[i])  # @line L6
            cur[i] = cur[i] * f(o)  # @line L7
            if cur[i] >= s_min:  # @line L8
                survivors.append(i)
        rest = survivors
    return out  # @line L9


def soft_nms_reference(boxes, scores, decay, s_min, overlap=iou):
    """A slow reference that keeps no running scores.

    At every step it recomputes the score of each candidate from scratch as
    s_i times the product of f(IoU(B_m, B_i)) over the boxes m selected so
    far, and it drops a candidate when one of these partial products, taken
    in selection order, falls below s_min. It must agree with soft_nms.
    """
    n = len(boxes)
    chosen, dropped = [], set()

    def partial(i, upto):
        v = scores[i]
        for m in chosen[:upto]:
            v = v * decay(overlap(boxes[m], boxes[i]))
        return v

    out = []
    while True:
        cands = []
        for i in range(n):
            if i in chosen or i in dropped:
                continue
            gone = any(partial(i, k) < s_min for k in range(1, len(chosen) + 1))
            if gone:
                dropped.add(i)
            else:
                cands.append(i)
        if not cands:
            return out
        m = min(cands, key=lambda i: (-partial(i, len(chosen)), i))
        out.append((m, partial(m, len(chosen))))
        chosen.append(m)


def greedy_nms_ge(boxes, scores, nt, overlap=iou):
    """Greedy NMS that removes a box when its overlap with a kept box is at
    least nt. This is the classic algorithm that the hard rule reproduces.
    """
    order = sorted(range(len(boxes)), key=lambda i: (-scores[i], i))
    keep, removed = [], [False] * len(boxes)
    for pos, i in enumerate(order):
        if removed[i]:
            continue
        keep.append(i)
        for j in order[pos + 1:]:
            if not removed[j] and overlap(boxes[i], boxes[j]) >= nt:
                removed[j] = True
    return keep
