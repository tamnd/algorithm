# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-f-measure/. The authors are listed in prov/87X9C9.jsonl.

"""Boundary precision, recall and F-measure with one-to-one matching within a distance.

A boundary map is a list of rows of 0 and 1, bmap[v][u]. Two boundary pixels
can be matched if their Euclidean distance is at most d. The number of correct
pixels is the size of a maximum matching of the bipartite graph of such pairs,
found with augmenting paths (Kuhn's method). Counts are integers and scores are
Fractions. An empty map gives precision or recall 0, and F is 0 when both are 0.
Standard library only.
"""

import math
from fractions import Fraction


def points(bmap):
    return [(u, v) for v, row in enumerate(bmap) for u, x in enumerate(row) if x]


def boundary_of(labels):
    """Pixel (u, v) is a boundary pixel if its right or lower neighbor has another label."""
    h, w = len(labels), len(labels[0])
    out = [[0] * w for _ in range(h)]
    for v in range(h):
        for u in range(w):
            if (u + 1 < w and labels[v][u + 1] != labels[v][u]) or (v + 1 < h and labels[v + 1][u] != labels[v][u]):
                out[v][u] = 1
    return out


def max_matching(bpts, gpts, d):
    """Return a maximum matching as a dict from index in bpts to index in gpts."""
    r = int(math.floor(d))
    where = {p: j for j, p in enumerate(gpts)}
    adj = []
    for (u, v) in bpts:  # @line L1
        nb = []
        for dv in range(-r, r + 1):
            for du in range(-r, r + 1):
                if du * du + dv * dv <= d * d and (u + du, v + dv) in where:
                    nb.append(where[(u + du, v + dv)])
        adj.append(nb)
    owner = {}

    def augment(i, seen):
        for j in adj[i]:
            if j not in seen:
                seen.add(j)
                if j not in owner or augment(owner[j], seen):
                    owner[j] = i
                    return True
        return False

    for i in range(len(bpts)):  # @line L2
        augment(i, set())
    return {i: j for j, i in owner.items()}


def f_of(p, r):
    return 2 * p * r / (p + r) if p + r > 0 else Fraction(0)


def boundary_f(bmap, gmap, d):
    """Return (precision, recall, F) of the boundary map bmap against one human map gmap."""
    bpts, gpts = points(bmap), points(gmap)
    m = max_matching(bpts, gpts, d)
    p = Fraction(len(m), len(bpts)) if bpts else Fraction(0)  # @line L3
    r = Fraction(len(m), len(gpts)) if gpts else Fraction(0)
    return p, r, f_of(p, r)  # @line L4


def bsds_counts(bmap, gmaps, d):
    """Counts over several human maps: (matched machine pixels, machine pixels, matched human pixels, human pixels)."""
    bpts = points(bmap)
    acc = set()  # @line L5
    cnt_r = sum_r = 0
    for gmap in gmaps:  # @line L6
        gpts = points(gmap)
        m = max_matching(bpts, gpts, d)  # @line L7
        acc |= set(m)  # @line L8
        cnt_r += len(m)
        sum_r += len(gpts)
    return len(acc), len(bpts), cnt_r, sum_r  # @line L9


def scores(cnt_p, sum_p, cnt_r, sum_r):
    p = Fraction(cnt_p, sum_p) if sum_p else Fraction(0)
    r = Fraction(cnt_r, sum_r) if sum_r else Fraction(0)
    return p, r, f_of(p, r)


def threshold(soft, t):
    return [[1 if x >= t else 0 for x in row] for row in soft]


def ods_ois(softs, gmaps_list, thresholds, d):
    """ODS: one threshold for the whole data set. OIS: the best threshold of each image, then summed counts.

    Return (ODS F, ODS threshold, OIS F).
    """
    table = [[bsds_counts(threshold(s, t), g, d) for t in thresholds] for s, g in zip(softs, gmaps_list)]
    best_f, best_t = Fraction(-1), None
    for k, t in enumerate(thresholds):
        tot = [sum(row[k][q] for row in table) for q in range(4)]
        f = scores(*tot)[2]
        if f > best_f:
            best_f, best_t = f, t
    tot = [0, 0, 0, 0]
    for row in table:
        k = max(range(len(thresholds)), key=lambda k: (scores(*row[k])[2], -k))
        tot = [a + b for a, b in zip(tot, row[k])]
    return best_f, best_t, scores(*tot)[2]
