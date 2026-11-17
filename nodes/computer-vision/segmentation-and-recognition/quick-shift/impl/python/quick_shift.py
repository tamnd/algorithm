# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quick-shift/. The authors are listed in prov/5E6C9Y.jsonl.

"""Quick shift on a gray image.

A pixel (u, v) has the value img[v][u] and the feature f = (u, v, lam * img[v][u]).
The density of a pixel is a sum of Gaussian kernels of standard deviation sigma
over the pixels in a square window of radius ceil(3 sigma). Each pixel links to
the nearest pixel, in feature distance, with a larger key (density, index),
if that pixel is at distance at most tau. Pixels with no link are roots, and
each tree is one segment.
"""

import math


def quick_shift(img, sigma, tau, lam=1.0):
    """Return (labels, parent, dist, dens).

    labels[v][u] is the index v * w + u of the root of the tree of (u, v).
    parent[i] is the parent of pixel i (i itself for a root), dist[i] is the
    feature distance to the parent (inf for a root) and dens[i] the density.
    """
    h, w = len(img), len(img[0])
    n = w * h
    feat = [(u, v, lam * img[v][u]) for v in range(h) for u in range(w)]  # @line L1
    rs = math.ceil(3 * sigma)
    two_s2 = 2.0 * sigma * sigma
    dens = [0.0] * n
    for i in range(n):  # @line L2
        u, v, c = feat[i]
        s = 0.0
        for y in range(max(0, v - rs), min(h, v + rs + 1)):
            for x in range(max(0, u - rs), min(w, u + rs + 1)):
                fu, fv, fc = feat[y * w + x]
                s += math.exp(-((fu - u) ** 2 + (fv - v) ** 2 + (fc - c) ** 2) / two_s2)  # @line L3
        dens[i] = s
    rt = max(w, h) if math.isinf(tau) else math.ceil(tau)
    parent = list(range(n))
    dist = [math.inf] * n
    for i in range(n):  # @line L4
        u, v, c = feat[i]
        best, bj = math.inf, i  # @line L5
        for y in range(max(0, v - rt), min(h, v + rt + 1)):  # @line L6
            for x in range(max(0, u - rt), min(w, u + rt + 1)):
                j = y * w + x
                if (dens[j], j) > (dens[i], i):  # @line L7
                    fu, fv, fc = feat[j]
                    d = math.sqrt((fu - u) ** 2 + (fv - v) ** 2 + (fc - c) ** 2)
                    if d <= tau and d < best:
                        best, bj = d, j  # @line L8
        parent[i], dist[i] = bj, best
    return roots_of(parent, w, h), parent, dist, dens


def roots_of(parent, w, h):
    """Follow the links to the root of each pixel and return the root index as a label map."""
    n = w * h
    root = [-1] * n
    for i in range(n):  # @line L9
        path = []
        j = i
        while root[j] < 0 and parent[j] != j:
            path.append(j)
            j = parent[j]
        r = root[j] if root[j] >= 0 else j
        root[j] = r
        for k in path:
            root[k] = r
    return [[root[v * w + u] for u in range(w)] for v in range(h)]  # @line L10


def cut(parent, dist, t, w, h):
    """Cut every link longer than t and return the label map of the remaining trees."""
    p = [j if dist[i] <= t else i for i, j in enumerate(parent)]
    return roots_of(p, w, h)
