# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clear-mot-metrics/. The authors are listed in prov/TXWACJ.jsonl.
"""The CLEAR MOT metrics MOTA and MOTP (Bernardin and Stiefelhagen 2008), with IoU.

A sequence is a list of frames; a frame is a dict from an identity to a box
(x1, y1, x2, y2). A pair (object o, hypothesis h) is valid when IoU(o, h) >= T.
In each frame:
  1. the pairs of the frame before stay matched if both are present and valid;
  2. the other objects and hypotheses are matched with the most valid pairs,
     and among those the largest total IoU (the Hungarian algorithm);
  3. a match (o, h) is an identity switch if o was last matched to h' != h;
  4. unmatched objects are misses, unmatched hypotheses are false positives.
MOTA = 1 - (FN + FP + IDSW) / GT and MOTP = (sum of IoU of matches) / matches.
With integer boxes all values are exact fractions.
"""

from fractions import Fraction


def iou(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    inter = w * h if w > 0 and h > 0 else 0
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return Fraction(inter) / union if union > 0 else Fraction(0)


def hungarian_min(cost):
    """Minimum cost assignment of a rectangular matrix; exact for fractions.
    Returns the sorted pairs (row, column), min(rows, columns) of them."""
    r = len(cost)
    if r == 0 or len(cost[0]) == 0:
        return []
    c = len(cost[0])
    flip = r > c
    if flip:
        cost = [list(col) for col in zip(*cost)]
        r, c = c, r
    inf = float("inf")
    u, v = [0] * (r + 1), [0] * (c + 1)
    p, way = [0] * (c + 1), [0] * (c + 1)
    for i in range(1, r + 1):
        p[0], j0 = i, 0
        minv, used = [inf] * (c + 1), [False] * (c + 1)
        while True:
            used[j0] = True
            i0, delta, j1 = p[j0], inf, 0
            for j in range(1, c + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j], way[j] = cur, j0
                    if minv[j] < delta:
                        delta, j1 = minv[j], j
            for j in range(c + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    pairs = [(p[j] - 1, j - 1) for j in range(1, c + 1) if p[j] != 0]
    if flip:
        pairs = [(b, a) for a, b in pairs]
    return sorted(pairs)


def best_matching(sim, threshold):
    """Among the matchings that use only pairs with sim >= threshold, one with the
    most pairs and, among those, the largest total sim. sim[i][j] lies in [0, 1].
    Returns the sorted list of pairs (i, j)."""
    if not sim or not sim[0]:
        return []
    big = min(len(sim), len(sim[0])) + 1  # one more pair is worth more than any total sim
    cost = [[-(big + s) if s >= threshold else 0 for s in row] for row in sim]
    return [(i, j) for i, j in hungarian_min(cost) if sim[i][j] >= threshold]


def clear_mot(gt_frames, hyp_frames, threshold=Fraction(1, 2), keep_previous=True):
    """Returns a dict with gt, matches, fn, fp, idsw, sum_iou, mota and motp."""
    gt_total = matches = fn = fp = idsw = 0
    sum_iou = Fraction(0)
    previous = {}  # object -> hypothesis, the matches of the frame before
    last = {}  # object -> the hypothesis it was last matched to, in any earlier frame
    for gt, hyp in zip(gt_frames, hyp_frames):  # @line L1
        current = {}
        if keep_previous:
            for o, h in previous.items():  # @line L2
                if o in gt and h in hyp and iou(gt[o], hyp[h]) >= threshold:
                    current[o] = h
        objs = sorted(o for o in gt if o not in current)
        used = set(current.values())
        hyps = sorted(h for h in hyp if h not in used)
        sim = [[iou(gt[o], hyp[h]) for h in hyps] for o in objs]
        for i, j in best_matching(sim, threshold):  # @line L3
            current[objs[i]] = hyps[j]
        for o, h in current.items():
            if o in last and last[o] != h:  # @line L4
                idsw += 1
            last[o] = h
            sum_iou += iou(gt[o], hyp[h])
        gt_total += len(gt)  # @line L5
        matches += len(current)
        fn += len(gt) - len(current)
        fp += len(hyp) - len(current)
        previous = current
    mota = 1 - Fraction(fn + fp + idsw, gt_total) if gt_total else None  # @line L6
    motp = sum_iou / matches if matches else None
    return {"gt": gt_total, "matches": matches, "fn": fn, "fp": fp, "idsw": idsw,
            "sum_iou": sum_iou, "mota": mota, "motp": motp}
