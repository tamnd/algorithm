# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/detr/. The authors are listed in prov/WE3F6C.jsonl.
"""DETR around given network outputs.

The backbone and the transformer are not part of this file. The caller passes
the N query outputs: for each query a list of C + 1 class probabilities, with
the no-object class last, and a box (cx, cy, w, h) relative to the image. The
tests build them by hand or with a fixed seed. This file has the parts that are
not learned: the generalized IoU, the matching cost, the Hungarian algorithm
for the optimal one-to-one matching of truths to queries, the set loss, and
the test-time output without non-maximum suppression.

Standard library only.
"""

import math

L1_WEIGHT = 5.0
GIOU_WEIGHT = 2.0
NO_OBJECT_WEIGHT = 0.1


def to_corners(b):
    return (b[0] - b[2] / 2, b[1] - b[3] / 2, b[0] + b[2] / 2, b[1] + b[3] / 2)


def giou(a, b):
    """Generalized IoU of two corner boxes of positive area: IoU - |C \\ (A u B)| / |C|,
    where C is the smallest box that holds both."""
    iw = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    ih = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = iw * ih
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    hull = (max(a[2], b[2]) - min(a[0], b[0])) * (max(a[3], b[3]) - min(a[1], b[1]))
    return inter / union - (hull - union) / hull


def box_loss(b, t):
    """lambda_L1 ||b - t||_1 + lambda_iou (1 - GIoU(b, t)) for boxes (cx, cy, w, h)."""
    l1 = sum(abs(x - y) for x, y in zip(b, t))
    return L1_WEIGHT * l1 + GIOU_WEIGHT * (1 - giou(to_corners(b), to_corners(t)))


def match_cost(probs, box, cls, tbox):
    """The matching cost of the paper: -p(class of the truth) + L_box."""
    return -probs[cls] + box_loss(box, tbox)


def hungarian(cost):
    """Minimum-cost assignment of the n rows to distinct columns of an n x m matrix,
    n <= m, by the Hungarian algorithm with potentials in O(n^2 m) time.
    Returns col[r], the column of row r."""
    n = len(cost)
    if n == 0:
        return []
    m = len(cost[0])
    assert n <= m
    inf = float("inf")
    u, v = [0.0] * (n + 1), [0.0] * (m + 1)
    p, way = [0] * (m + 1), [0] * (m + 1)
    for i in range(1, n + 1):
        p[0], j0 = i, 0
        minv, used = [inf] * (m + 1), [False] * (m + 1)
        while True:
            used[j0] = True
            i0, delta, j1 = p[j0], inf, 0
            for j in range(1, m + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j], way[j] = cur, j0
                    if minv[j] < delta:
                        delta, j1 = minv[j], j
            for j in range(m + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while j0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    col = [-1] * n
    for j in range(1, m + 1):
        if p[j]:
            col[p[j] - 1] = j - 1
    return col


def set_loss(probs, boxes, gt_classes, gt_boxes):
    """The DETR set loss on given outputs. Returns (loss, sigma), where sigma[j]
    is the query matched to truth j.

    The class term is the weighted mean of -log p_i(target_i), with weight 0.1
    for the no-object target; the box term is summed over the matched pairs and
    divided by the number of truths."""
    # probs and boxes are the outputs of the network for the N queries.
    n, no_obj = len(probs), len(probs[0]) - 1  # @line L1
    cost = [[match_cost(probs[i], boxes[i], c, t) for i in range(n)]
            for c, t in zip(gt_classes, gt_boxes)]  # @line L2
    sigma = hungarian(cost)  # @line L3
    target = [no_obj] * n
    for j, i in enumerate(sigma):
        target[i] = gt_classes[j]  # @line L4
    w = [NO_OBJECT_WEIGHT if target[i] == no_obj else 1.0 for i in range(n)]
    cls = sum(-w[i] * math.log(probs[i][target[i]]) for i in range(n)) / sum(w)  # @line L5
    box = sum(box_loss(boxes[i], gt_boxes[j]) for j, i in enumerate(sigma))
    box /= max(1, len(gt_boxes))  # @line L6
    return cls + box, sigma  # @line L7


def detect(probs, boxes, score_thr=0.7):
    """Test-time output: for each query, its best class other than no-object and
    the probability of it; queries above the threshold are returned as
    (score, class, corner box), best first. There is no NMS."""
    out = []
    for p, b in zip(probs, boxes):
        c = max(range(len(p) - 1), key=lambda k: (p[k], -k))
        if p[c] > score_thr:
            out.append((p[c], c, to_corners(b)))
    out.sort(key=lambda d: (-d[0], d[1]))
    return out
