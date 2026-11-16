# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hota-metric/. The authors are listed in prov/SAT5C8.jsonl.
"""HOTA, higher order tracking accuracy (Luiten et al. 2021), with IoU as the similarity S.

A sequence is a list of frames; a frame is a dict from an identity to a box
(x1, y1, x2, y2). For each alpha in {0.05, 0.10, ..., 0.95}:
  1. in each frame, the true and the predicted detections with S >= alpha are
     matched one to one, maximizing the sum of MS = 1/eps + A_max + eps S
     (the Hungarian algorithm). A_max(g, p) = n / (|g| + |p| - n), where n is the
     number of frames in which g and p have S >= alpha;
  2. the matches are the TPs, the other true detections the FNs and the other
     predicted detections the FPs;
  3. a TP c with identities (g, p) has TPA(c) = the TPs with the identities
     (g, p), FNA(c) = |g| - TPA(c), FPA(c) = |p| - TPA(c), and
     A(c) = TPA / (TPA + FNA + FPA);
  4. DetA = TP / (TP + FN + FP), AssA = the mean of A(c) over the TPs,
     HOTA_alpha = sqrt(DetA AssA).
HOTA is the mean of HOTA_alpha over the 19 values of alpha. The squares and
the parts are exact fractions.
"""

import math
from fractions import Fraction

ALPHAS = [Fraction(k, 20) for k in range(1, 20)]
EPS = Fraction(1, 10 ** 6)


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


def lengths(frames):
    out = {}
    for f in frames:
        for k in f:
            out[k] = out.get(k, 0) + 1
    return out


def potential_counts(gt_frames, pr_frames, alpha):
    """n[(g, p)] = the number of frames in which g and p have S >= alpha."""
    n = {}
    for gt, pr in zip(gt_frames, pr_frames):
        for g, a in gt.items():
            for p, b in pr.items():
                if iou(a, b) >= alpha:
                    n[(g, p)] = n.get((g, p), 0) + 1
    return n


def match_score(s, a_max, eps=EPS):
    return 1 / eps + a_max + eps * s


def frame_matching(gt, pr, alpha, a_max, eps=EPS):
    """The pairs (g, p) of one frame with S >= alpha and the largest sum of MS."""
    gs, ps = sorted(gt, key=repr), sorted(pr, key=repr)
    if not gs or not ps:
        return []
    sim = [[iou(gt[g], pr[p]) for p in ps] for g in gs]
    cost = [[-match_score(sim[i][j], a_max.get((g, p), 0), eps) if sim[i][j] >= alpha else 0
             for j, p in enumerate(ps)] for i, g in enumerate(gs)]
    return [(gs[i], ps[j]) for i, j in hungarian_min(cost) if sim[i][j] >= alpha]


def hota_alpha(gt_frames, pr_frames, alpha, eps=EPS):
    """Returns a dict with tp, fn, fp, deta, assa, hota_sq (exact), hota and loca."""
    glen, plen = lengths(gt_frames), lengths(pr_frames)
    n = potential_counts(gt_frames, pr_frames, alpha)
    a_max = {k: Fraction(v, glen[k[0]] + plen[k[1]] - v) for k, v in n.items()}
    tpa = {}
    tp, sum_s = 0, Fraction(0)
    for gt, pr in zip(gt_frames, pr_frames):
        for g, p in frame_matching(gt, pr, alpha, a_max, eps):  # @line L2
            tpa[(g, p)] = tpa.get((g, p), 0) + 1
            tp += 1
            sum_s += iou(gt[g], pr[p])
    fn = sum(glen.values()) - tp  # @line L3
    fp = sum(plen.values()) - tp
    # sum over the TPs c of A(c): each identity pair (g, p) has tpa TPs with the same A
    sum_a = sum((Fraction(k * k, glen[g] + plen[p] - k) for (g, p), k in tpa.items()), Fraction(0))
    total = tp + fn + fp
    deta = Fraction(tp, total) if total else Fraction(0)  # @line L4
    assa = sum_a / tp if tp else Fraction(0)
    hota_sq = deta * assa
    return {"tp": tp, "fn": fn, "fp": fp, "deta": deta, "assa": assa, "hota_sq": hota_sq,
            "hota": math.sqrt(hota_sq), "loca": sum_s / tp if tp else None, "tpa": tpa}


def hota(gt_frames, pr_frames, alphas=ALPHAS, eps=EPS):
    """Returns HOTA, DetA, AssA and LocA averaged over alpha, and the per alpha results.
    LocA is averaged over the alphas with at least one TP."""
    per = [hota_alpha(gt_frames, pr_frames, a, eps) for a in alphas]  # @line L1
    k = len(per)
    locs = [r["loca"] for r in per if r["loca"] is not None]
    return {
        "hota": sum(r["hota"] for r in per) / k,  # @line L5
        "deta": sum((r["deta"] for r in per), Fraction(0)) / k,
        "assa": sum((r["assa"] for r in per), Fraction(0)) / k,
        "loca": sum(locs, Fraction(0)) / len(locs) if locs else None,
        "per_alpha": per,
    }
