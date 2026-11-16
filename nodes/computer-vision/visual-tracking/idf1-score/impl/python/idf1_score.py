# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/idf1-score/. The authors are listed in prov/QK543C.jsonl.
"""The identity measures IDP, IDR and IDF1 (Ristani et al. 2016), with IoU.

A sequence is a list of frames; a frame is a dict from an identity to a box
(x1, y1, x2, y2). A true trajectory o and a computed trajectory h agree in a
frame when both are present and IoU >= delta. n(o, h) is the number of such
frames. One global one-to-one matching of true to computed trajectories with
the largest total n gives IDTP; then
  IDFN = (true detections) - IDTP,  IDFP = (computed detections) - IDTP,
  IDF1 = 2 IDTP / (true detections + computed detections).
The paper states the matching as a minimum cost problem with extra nodes for
the unmatched trajectories; min_cost_with_dummy_nodes builds that form, and
the tests check that both forms agree. All values are exact fractions.
"""

from fractions import Fraction


def iou(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    inter = w * h if w > 0 and h > 0 else 0
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return Fraction(inter) / union if union > 0 else Fraction(0)


def hungarian_min(cost):
    """Minimum cost assignment of a rectangular matrix; exact for integers and fractions.
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


def overlap_counts(gt_frames, hyp_frames, delta=Fraction(1, 2)):
    """Returns (true ids, computed ids, n, true lengths, computed lengths)."""
    gt_ids = sorted({o for f in gt_frames for o in f}, key=repr)
    hyp_ids = sorted({h for f in hyp_frames for h in f}, key=repr)
    gi = {o: i for i, o in enumerate(gt_ids)}
    hi = {h: j for j, h in enumerate(hyp_ids)}
    n = [[0] * len(hyp_ids) for _ in gt_ids]
    glen, hlen = [0] * len(gt_ids), [0] * len(hyp_ids)
    for gt, hyp in zip(gt_frames, hyp_frames):  # @line L1
        for o, a in gt.items():
            glen[gi[o]] += 1
            for h, b in hyp.items():
                if iou(a, b) >= delta:
                    n[gi[o]][hi[h]] += 1
        for h in hyp:
            hlen[hi[h]] += 1
    return gt_ids, hyp_ids, n, glen, hlen


def max_overlap_matching(n):
    """A one-to-one matching of rows to columns with the largest total n.
    Returns (pairs, total); pairs with n = 0 are left out."""
    if not n or not n[0]:
        return [], 0
    pairs = [(i, j) for i, j in hungarian_min([[-x for x in row] for row in n]) if n[i][j] > 0]  # @line L2
    return pairs, sum(n[i][j] for i, j in pairs)


def idf1(gt_frames, hyp_frames, delta=Fraction(1, 2)):
    """Returns a dict with idtp, idfn, idfp, idp, idr, idf1 and the matched identities."""
    gt_ids, hyp_ids, n, glen, hlen = overlap_counts(gt_frames, hyp_frames, delta)
    pairs, idtp = max_overlap_matching(n)
    total_gt, total_hyp = sum(glen), sum(hlen)
    idfn = total_gt - idtp  # @line L3
    idfp = total_hyp - idtp
    idp = Fraction(idtp, total_hyp) if total_hyp else None  # @line L4
    idr = Fraction(idtp, total_gt) if total_gt else None
    f1 = Fraction(2 * idtp, total_gt + total_hyp) if total_gt + total_hyp else None
    return {"idtp": idtp, "idfn": idfn, "idfp": idfp, "idp": idp, "idr": idr, "idf1": f1,
            "matching": [(gt_ids[i], hyp_ids[j]) for i, j in pairs]}


def min_cost_with_dummy_nodes(n, glen, hlen):
    """The form of the paper: rows are the true trajectories and one false positive
    node per computed trajectory; columns are the computed trajectories and one false
    negative node per true trajectory. Matching o to h costs the misses of both,
    glen + hlen - 2 n; o to its own false negative node costs glen; the false
    positive node of h to h costs hlen; two extra nodes cost 0. Returns the minimum."""
    t, c = len(glen), len(hlen)
    size = t + c
    big = sum(glen) + sum(hlen) + 1  # no edge
    cost = [[big] * size for _ in range(size)]
    for i in range(t):
        for j in range(c):
            cost[i][j] = glen[i] + hlen[j] - 2 * n[i][j]
        cost[i][c + i] = glen[i]
    for j in range(c):
        cost[t + j][j] = hlen[j]
        for i in range(t):
            cost[t + j][c + i] = 0
    pairs = hungarian_min(cost)
    return sum(cost[i][j] for i, j in pairs)
