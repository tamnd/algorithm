# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplacian-of-gaussian/. The authors are listed in prov/P120H7.jsonl.

"""Laplacian of Gaussian filtering and the Marr-Hildreth zero crossing edge detector.

An image is a list of H rows of W numbers, with pixel (x, y) at [y][x], x to
the right and y downward. Reads outside the image use the nearest border pixel
(clamp). The kernel is the sampled Laplacian of a Gaussian of scale sigma on
the offsets -r..r, r = ceil(4 sigma), scaled so that its sum is 0 and so that
it returns exactly 2 on the image I(x, y) = x * x. The 2D kernel is the sum of
two separable kernels, so the filter costs O(H W r).
"""

import math

Grid = list[list[float]]


def log_kernels(sigma: float) -> tuple[list[float], list[float], int]:
    """Return (g, dxx, r). The 2D kernel is dxx[u] g[v] + g[u] dxx[v] at offset (u, v)."""
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    r = max(1, math.ceil(4 * sigma))
    raw = [math.exp(-(k * k) / (2 * sigma * sigma)) for k in range(-r, r + 1)]
    total = sum(raw)
    g = [v / total for v in raw]
    m2 = sum(k ** 2 * g[k + r] for k in range(-r, r + 1))
    m4 = sum(k ** 4 * g[k + r] for k in range(-r, r + 1))
    a = 2.0 / (m4 - m2 * m2)
    dxx = [a * (k * k - m2) * g[k + r] for k in range(-r, r + 1)]
    return g, dxx, r


def _rows(image: Grid, kernel: list[float], r: int) -> Grid:
    h, w = len(image), len(image[0])
    return [[sum(kernel[k + r] * image[y][min(max(x + k, 0), w - 1)] for k in range(-r, r + 1))
             for x in range(w)] for y in range(h)]


def _cols(image: Grid, kernel: list[float], r: int) -> Grid:
    h, w = len(image), len(image[0])
    return [[sum(kernel[k + r] * image[min(max(y + k, 0), h - 1)][x] for k in range(-r, r + 1))
             for x in range(w)] for y in range(h)]


def laplacian_of_gaussian(image: Grid, sigma: float) -> Grid:
    """Return the image correlated with the sampled Laplacian of Gaussian kernel."""
    g, dxx, r = log_kernels(sigma)  # @line L1
    a = _cols(_rows(image, dxx, r), g, r)  # @line L2
    b = _rows(_cols(image, dxx, r), g, r)  # @line L3
    h, w = len(image), len(image[0])
    return [[a[y][x] + b[y][x] for x in range(w)] for y in range(h)]  # @line L4


def zero_crossings(lap: Grid, threshold: float) -> list[list[bool]]:
    """Mark the zero crossings of lap.

    For each pair of 4-neighbors p, q with opposite signs and |lap(p) - lap(q)| >= threshold,
    mark the one of p, q with the smaller absolute value (p, the first in scan order, on a tie).
    A pixel with value exactly 0 is marked when its two neighbors on one axis have opposite
    signs and a difference of at least threshold.
    """
    h = len(lap)
    w = len(lap[0]) if h else 0
    mark = [[False] * w for _ in range(h)]
    for y in range(h):  # @line L5
        for x in range(w):
            p = lap[y][x]
            for dx, dy in ((1, 0), (0, 1)):
                xx, yy = x + dx, y + dy
                if xx < w and yy < h:
                    q = lap[yy][xx]
                    if p * q < 0 and abs(p - q) >= threshold:  # @line L6
                        if abs(p) <= abs(q):
                            mark[y][x] = True
                        else:
                            mark[yy][xx] = True
                xm, ym = x - dx, y - dy
                if p == 0 and xm >= 0 and ym >= 0 and xx < w and yy < h:
                    s, t = lap[ym][xm], lap[yy][xx]
                    if s * t < 0 and abs(s - t) >= threshold:  # @line L7
                        mark[y][x] = True
    return mark  # @line L8


def marr_hildreth(image: Grid, sigma: float, threshold: float) -> list[list[bool]]:
    """Return the Marr-Hildreth edge mask: the zero crossings of the LoG filtered image."""
    if not image or not image[0]:
        return []
    return zero_crossings(laplacian_of_gaussian(image, sigma), threshold)
