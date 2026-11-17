# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spin-images/. The authors are listed in prov/9YPF70.jsonl.
"""Spin images, after Johnson and Hebert (1999).

An oriented point (p, n) gives every point x two cylindrical coordinates:
    beta  = n . (x - p)                       the height along the normal,
    alpha = sqrt(|x - p|^2 - beta^2)          the distance from the normal line.
The spin image is the 2D histogram of (alpha, beta) over the points x whose
normal makes an angle at most the support angle with n. The image has
width x width cells of size bin_size. Rows run from beta = +beta_max (row 0)
down to -beta_max, and columns from alpha = 0 to alpha_max, with
    beta_max = (width - 1) * bin_size / 2,  alpha_max = (width - 1) * bin_size,
so the cell centers are at the grid nodes. Each point spreads its unit
weight over the four cells around it by bilinear interpolation. A point
with alpha > alpha_max or |beta| > beta_max is out of support.

The point p itself is a point of the cloud and adds its weight at alpha = 0,
beta = 0, as in the original, where every mesh vertex is counted.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

Image = List[List[float]]


def spin_coordinates(p: Sequence[float], n: Sequence[float], x: Sequence[float]) -> Tuple[float, float]:
    """The (alpha, beta) coordinates of x in the spin basis of (p, n)."""
    d = [x[0] - p[0], x[1] - p[1], x[2] - p[2]]
    beta = n[0] * d[0] + n[1] * d[1] + n[2] * d[2]
    alpha = math.sqrt(max(0.0, d[0] * d[0] + d[1] * d[1] + d[2] * d[2] - beta * beta))
    return alpha, beta


def spin_image(points: Sequence[Sequence[float]], normals: Sequence[Sequence[float]],
               p: Sequence[float], n: Sequence[float], bin_size: float, width: int,
               support_angle_degrees: float = 60.0) -> Image:
    """The width x width spin image of the oriented point (p, n), with unit n."""
    if bin_size <= 0 or width < 2:
        raise ValueError("bin_size must be positive and width at least 2")
    img = [[0.0] * width for _ in range(width)]  # @line L1
    beta_max = (width - 1) * bin_size / 2.0
    alpha_max = (width - 1) * bin_size
    min_cos = math.cos(math.radians(support_angle_degrees))
    for x, nx in zip(points, normals):  # @line L2
        if n[0] * nx[0] + n[1] * nx[1] + n[2] * nx[2] < min_cos:  # @line L3
            continue
        alpha, beta = spin_coordinates(p, n, x)  # @line L4
        if alpha > alpha_max or abs(beta) > beta_max:  # @line L5
            continue
        u = (beta_max - beta) / bin_size  # @line L6
        s = alpha / bin_size
        i, j = min(width - 1, int(u)), min(width - 1, int(s))  # @line L7
        a, c = u - i, s - j
        for di, wi in ((0, 1.0 - a), (1, a)):  # @line L8
            for dj, wj in ((0, 1.0 - c), (1, c)):
                if i + di < width and j + dj < width:
                    img[i + di][j + dj] += wi * wj
    return img  # @line L9


def correlation(a: Image, b: Image) -> Optional[float]:
    """The Pearson correlation of two images of the same size, over all
    cells, or None when one image is constant."""
    xs = [v for row in a for v in row]
    ys = [v for row in b for v in row]
    if len(xs) != len(ys):
        raise ValueError("images of different sizes")
    m = len(xs)
    mx, my = sum(xs) / m, sum(ys) / m
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return None
    return sxy / math.sqrt(sxx * syy)
