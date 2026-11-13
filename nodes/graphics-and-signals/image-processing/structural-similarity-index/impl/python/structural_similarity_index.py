# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/structural-similarity-index/. The authors are listed in prov/N7A0E4.jsonl.

"""Structural similarity index (SSIM) of Wang, Bovik, Sheikh and Simoncelli (2004).

Images are lists of rows of numbers (int, float or Fraction) with the same
size. The window is separable: a one-dimensional weight list w whose sum is
1, used along rows and along columns, so the two-dimensional weight is
w[i] * w[j]. The default is the 11 tap Gaussian with standard deviation 1.5
from the paper. Only windows that lie fully inside the image are used.
With Fraction inputs and a Fraction window the result is exact.
"""

import math
from fractions import Fraction


def gaussian_window(size: int = 11, sigma: float = 1.5) -> list[float]:
    """One-dimensional Gaussian weights, normalized to sum 1."""
    half = (size - 1) / 2
    w = [math.exp(-((i - half) ** 2) / (2 * sigma * sigma)) for i in range(size)]
    s = sum(w)
    return [v / s for v in w]


def _filter_valid(img: list[list], w: list) -> list[list]:
    """Weighted sums over every k by k window fully inside img, by two 1D passes."""
    k = len(w)
    rows = [[sum(w[t] * row[j + t] for t in range(k)) for j in range(len(row) - k + 1)] for row in img]
    height = len(rows)
    return [
        [sum(w[t] * rows[i + t][j] for t in range(k)) for j in range(len(rows[0]))]
        for i in range(height - k + 1)
    ]


def ssim(
    x: list[list],
    y: list[list],
    data_range=255,
    window: list | None = None,
    k1=Fraction(1, 100),
    k2=Fraction(3, 100),
):
    """Return (mean SSIM, SSIM map) of images x and y.

    data_range is L in C1 = (K1 L)^2 and C2 = (K2 L)^2, 255 for 8-bit images.
    Cost: O(W H k) time for a k tap window and O(W H) extra space.
    """
    if window is None:
        window = gaussian_window()
    k = len(window)
    height, width = len(x), len(x[0]) if x else 0
    if len(y) != height or any(len(a) != width or len(b) != width for a, b in zip(x, y)):
        raise ValueError("the images must have the same size")
    if height < k or width < k:
        raise ValueError("the images must be at least as large as the window")
    c1 = (k1 * data_range) ** 2  # @line L1
    c2 = (k2 * data_range) ** 2
    mu_x = _filter_valid(x, window)  # @line L2
    mu_y = _filter_valid(y, window)
    e_xx = _filter_valid([[a * a for a in row] for row in x], window)
    e_yy = _filter_valid([[b * b for b in row] for row in y], window)
    e_xy = _filter_valid([[a * b for a, b in zip(ra, rb)] for ra, rb in zip(x, y)], window)
    total = 0  # @line L3
    smap = []
    for i in range(len(mu_x)):  # @line L4
        srow = []
        for j in range(len(mu_x[0])):
            mx, my = mu_x[i][j], mu_y[i][j]  # @line L5
            vx, vy, cxy = e_xx[i][j] - mx * mx, e_yy[i][j] - my * my, e_xy[i][j] - mx * my  # @line L6
            s = (2 * mx * my + c1) * (2 * cxy + c2) / ((mx * mx + my * my + c1) * (vx + vy + c2))  # @line L7
            total += s  # @line L8
            srow.append(s)
        smap.append(srow)
    count = len(smap) * len(smap[0])
    return total / count, smap  # @line L9
