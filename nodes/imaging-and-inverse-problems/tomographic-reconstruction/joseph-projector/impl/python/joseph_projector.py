# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/joseph-projector/. The authors are listed in prov/YFWYC3.jsonl.
"""Joseph's projector: line integrals through an image by linear interpolation along rows or columns.

Conventions:
- The image is n x n on the square [-1, 1]^2, stored as img[i][j] with row i
  from the top and column j from the left. The center of pixel (i, j) is
  x_j = -1 + (2 j + 1) / n and y_i = 1 - (2 i + 1) / n, so y goes up.
- A ray is the line x cos(theta) + y sin(theta) = s.
- The code works with float or with fractions.Fraction values of
  cos(theta), sin(theta) and s. With Fraction input the result is exact.
"""

import math
from fractions import Fraction


def ray_weights(n, c, sn, s):
    """The (i, j, weight) entries of the ray x c + y sn = s, with c = cos(theta) and sn = sin(theta).

    The weights are the linear interpolation weights in each row (or column)
    times the length of the ray between two rows (or columns). An index
    outside the image gets no weight, which is the same as a zero value there.
    """
    exact = any(isinstance(v, Fraction) for v in (c, sn, s))
    h = Fraction(2, n) if exact else 2.0 / n  # @line L1
    out = []
    if abs(c) >= abs(sn):  # @line L2
        step = h / abs(c)  # @line L3
        for i in range(n):  # @line L4
            y = 1 - (2 * i + 1) * h / 2
            x = (s - y * sn) / c  # @line L5
            u = ((x + 1) * n - 1) / 2  # the column coordinate: u = j at the center x_j
            j = math.floor(u)  # @line L6
            t = u - j
            for jj, w in ((j, 1 - t), (j + 1, t)):  # @line L7
                if 0 <= jj < n and w != 0:
                    out.append((i, jj, step * w))
    else:
        step = h / abs(sn)  # @line L8
        for j in range(n):
            x = -1 + (2 * j + 1) * h / 2
            y = (s - x * c) / sn  # @line L9
            v = ((1 - y) * n - 1) / 2  # the row coordinate: v = i at the center y_i
            i = math.floor(v)
            t = v - i
            for ii, w in ((i, 1 - t), (i + 1, t)):  # @line L10
                if 0 <= ii < n and w != 0:
                    out.append((ii, j, step * w))
    return out


def joseph_ray(img, c, sn, s):
    """The line integral of the interpolated image along x c + y sn = s."""
    return sum(w * img[i][j] for i, j, w in ray_weights(len(img), c, sn, s))  # @line L11


def bin_centers(nbins):
    """s_b = -sqrt(2) + (b + 1/2) w with w = 2 sqrt(2) / nbins, the bins of imgkit."""
    smax = math.sqrt(2.0)
    width = 2.0 * smax / nbins
    return [-smax + (b + 0.5) * width for b in range(nbins)]


def joseph_project(img, angles, nbins):
    """The sinogram as a flat list: entry k * nbins + b holds angle k and bin b."""
    out = []
    for theta in angles:
        c, sn = math.cos(theta), math.sin(theta)
        out.extend(joseph_ray(img, c, sn, s) for s in bin_centers(nbins))
    return out


def joseph_back_project(n, angles, nbins, values):
    """The adjoint of joseph_project: each ray adds its value times its weights to its pixels."""
    out = [[0.0] * n for _ in range(n)]
    k = 0
    for theta in angles:
        c, sn = math.cos(theta), math.sin(theta)
        for s in bin_centers(nbins):
            v = values[k]
            k += 1
            if v == 0:
                continue
            for i, j, w in ray_weights(n, c, sn, s):
                out[i][j] += w * v
    return out


def joseph_matrix(n, angles, nbins):
    """The system matrix as sparse rows of (column, weight) pairs, column i * n + j."""
    rows = []
    for theta in angles:
        c, sn = math.cos(theta), math.sin(theta)
        for s in bin_centers(nbins):
            acc = {}
            for i, j, w in ray_weights(n, c, sn, s):
                acc[i * n + j] = acc.get(i * n + j, 0.0) + w
            rows.append(sorted(acc.items()))
    return rows
