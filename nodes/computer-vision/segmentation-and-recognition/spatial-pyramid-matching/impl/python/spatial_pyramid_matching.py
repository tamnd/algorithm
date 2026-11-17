# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spatial-pyramid-matching/. The authors are listed in prov/QX9B5V.jsonl.
"""Spatial pyramid matching (Lazebnik, Schmid and Ponce, CVPR 2006).

A feature is a triple (u, v, m): a position in a W x H image (u the column,
v the row, 0 <= u <= W and 0 <= v <= H) and a visual word m in 0..M-1.
Level l of the pyramid cuts the image into 2^l x 2^l equal cells; a feature
falls into cell (min(floor(u 2^l / W), 2^l - 1), min(floor(v 2^l / H), 2^l - 1)).
I^l is the histogram intersection of the two images at level l over the bins
(cell, word), and the kernel is
    K = I^L + sum_{l=0}^{L-1} (I^l - I^{l+1}) / 2^(L - l).
Histograms are sparse dicts, so the cost is O(n L) for n features, plus the
size of the smaller dict per intersection. Weights are exact Fractions, so
the kernel is exact on integer counts. Standard library only.
"""

from fractions import Fraction


def cell_of(u, v, level, W, H):
    """The cell (cu, cv) of position (u, v) at a level; points on the far edge go to the last cell."""
    s = 1 << level
    cu = min(int((u * s) // W), s - 1)
    cv = min(int((v * s) // H), s - 1)
    return cu, cv


def level_histogram(features, level, W, H, weight=1):
    """Sparse histogram {(cu, cv, m): weight times count} of the features at one level."""
    h = {}
    for u, v, m in features:
        key = cell_of(u, v, level, W, H) + (m,)
        h[key] = h.get(key, 0) + weight
    return h


def intersection(h1, h2):
    """Histogram intersection: the sum over bins of min(h1[b], h2[b])."""
    if len(h2) < len(h1):
        h1, h2 = h2, h1
    return sum(min(c, h2[b]) for b, c in h1.items() if b in h2)


def level_intersections(X, Y, L, W, H, normalize=False):
    """The list I^0, ..., I^L. With normalize, each histogram is divided by its number of features."""
    wx = Fraction(1, len(X)) if normalize and X else 1
    wy = Fraction(1, len(Y)) if normalize and Y else 1
    out = []
    for level in range(L + 1):  # @line L1
        hx = level_histogram(X, level, W, H, wx)  # @line L2
        hy = level_histogram(Y, level, W, H, wy)  # @line L3
        out.append(intersection(hx, hy))  # @line L4
    return out


def spm_kernel(X, Y, L, W, H, normalize=False):
    """The spatial pyramid match kernel, Eq. (2) of Lazebnik et al."""
    I = level_intersections(X, Y, L, W, H, normalize)
    kappa = Fraction(I[L])  # @line L5
    for level in range(L):  # @line L6
        kappa += Fraction(I[level] - I[level + 1]) / (1 << (L - level))
    return kappa  # @line L7


def level_weight(level, L):
    """Weight of level l in Eq. (3): 1/2^L for l = 0, and 1/2^(L - l + 1) for l >= 1."""
    if level == 0:
        return Fraction(1, 1 << L)
    return Fraction(1, 1 << (L - level + 1))


def spm_kernel_eq3(X, Y, L, W, H, normalize=False):
    """The same kernel as a weighted sum of the level intersections, Eq. (3)."""
    I = level_intersections(X, Y, L, W, H, normalize)
    return sum(level_weight(level, L) * I[level] for level in range(L + 1))


def pyramid_vector(X, M, L, W, H, normalize=False):
    """The concatenated weighted histograms as a dense list of length M (4^(L+1) - 1) / 3.

    The histogram intersection of two such vectors is the pyramid kernel.
    """
    wx = Fraction(1, len(X)) if normalize and X else 1
    out = []
    for level in range(L + 1):
        s = 1 << level
        h = level_histogram(X, level, W, H, wx)
        a = level_weight(level, L)
        for cv in range(s):
            for cu in range(s):
                for m in range(M):
                    out.append(a * h.get((cu, cv, m), 0))
    return out


def dense_intersection(p, q):
    return sum(min(a, b) for a, b in zip(p, q))
