# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distance-driven-projector/. The authors are listed in prov/MVREDC.jsonl.
"""The distance-driven projector and its exact transpose, for 2D parallel beams.

Conventions:
- The image is n x n on the square [-1, 1]^2, stored as img[i][j] with row i
  from the top and column j from the left. The center of pixel (i, j) is
  x_j = -1 + (2 j + 1) / n and y_i = 1 - (2 i + 1) / n, so y goes up.
- A view has the angle theta, and the detector coordinate of a point (x, y)
  is s = x cos(theta) + y sin(theta). Bin b covers [s0 + b w, s0 + (b + 1) w].
- The value of a bin is the average over its width of the projection of the
  image model: inside each row (or column) the image is constant on each
  pixel, and the row has the thickness h / |cos(theta)| along the ray.
- The code works with float or with fractions.Fraction values of cos(theta),
  sin(theta), s0 and w. With Fraction input the weights are exact.
"""

import math
from fractions import Fraction


def _overlaps(pb, bb):
    """Sweep two increasing lists of cell borders; yield (cell of pb, cell of bb, overlap length)."""
    p, q = 0, 0
    while p < len(pb) - 1 and q < len(bb) - 1:  # @line L7
        length = min(pb[p + 1], bb[q + 1]) - max(pb[p], bb[q])  # @line L8
        if length > 0:
            yield p, q, length  # @line L9
        if pb[p + 1] < bb[q + 1]:  # @line L10
            p += 1
        else:
            q += 1


def view_weights(n, c, sn, s0, w, nbins):
    """The (b, i, j, weight) entries of one view with c = cos(theta), sn = sin(theta)."""
    exact = any(isinstance(v, Fraction) for v in (c, sn, s0, w))
    h = Fraction(2, n) if exact else 2.0 / n  # @line L1
    bins = [s0 + b * w for b in range(nbins + 1)]  # @line L5
    out = []
    rows = abs(c) >= abs(sn)  # @line L2
    step = h / abs(c) if rows else h / abs(sn)
    for k in range(n):  # @line L3
        if rows:  # row k: pixel borders x = -1 + j h at the height y_k
            y = 1 - (2 * k + 1) * h / 2
            borders = [(-1 + j * h) * c + y * sn for j in range(n + 1)]
        else:  # column k: pixel borders y = 1 - i h at the abscissa x_k
            x = -1 + (2 * k + 1) * h / 2
            borders = [x * c + (1 - i * h) * sn for i in range(n + 1)]
        flip = borders[0] > borders[-1]  # @line L4
        if flip:
            borders.reverse()
        for p, b, length in _overlaps(borders, bins):  # @line L6
            m = n - 1 - p if flip else p
            i, j = (k, m) if rows else (m, k)
            out.append((b, i, j, step * length / w))
    return out


def detector(nbins):
    """(s0, w) of the bins of imgkit: nbins bins of width 2 sqrt(2) / nbins on [-sqrt(2), sqrt(2)]."""
    return -math.sqrt(2.0), 2.0 * math.sqrt(2.0) / nbins


def dd_project_view(img, c, sn, s0, w, nbins):
    """The bin values of one view."""
    out = [0 * w] * nbins
    for b, i, j, wt in view_weights(len(img), c, sn, s0, w, nbins):
        out[b] += wt * img[i][j]
    return out  # @line L11


def dd_project(img, angles, nbins):
    """The sinogram as a flat list: entry k * nbins + b holds angle k and bin b."""
    s0, w = detector(nbins)
    out = []
    for theta in angles:
        out.extend(dd_project_view(img, math.cos(theta), math.sin(theta), s0, w, nbins))
    return out


def dd_back_project(n, angles, nbins, values):
    """The exact transpose of dd_project: each weight carries its bin value back to its pixel."""
    s0, w = detector(nbins)
    out = [[0.0] * n for _ in range(n)]
    for k, theta in enumerate(angles):
        for b, i, j, wt in view_weights(n, math.cos(theta), math.sin(theta), s0, w, nbins):
            out[i][j] += wt * values[k * nbins + b]
    return out


def dd_matrix(n, angles, nbins):
    """The system matrix as sparse rows of (column, weight) pairs, column i * n + j."""
    s0, w = detector(nbins)
    rows = []
    for theta in angles:
        acc = [dict() for _ in range(nbins)]
        for b, i, j, wt in view_weights(n, math.cos(theta), math.sin(theta), s0, w, nbins):
            acc[b][i * n + j] = acc[b].get(i * n + j, 0.0) + wt
        rows.extend(sorted(d.items()) for d in acc)
    return rows
