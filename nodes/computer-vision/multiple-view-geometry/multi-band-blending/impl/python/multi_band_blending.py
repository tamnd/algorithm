# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-band-blending/. The authors are listed in prov/AXXSRR.jsonl.
"""Multi-band blending of two images with a mask (Burt and Adelson, 1983).

An image is a list of rows; pixel (u, v) is img[v][u]. A, B and the mask M
have the same size W x H; M holds weights in [0, 1], 1 where the result
should come from A. Each image is split into a Laplacian pyramid, each band
is mixed with the matching level of the Gaussian pyramid of M, and the
mixed pyramid is collapsed.

REDUCE and EXPAND follow the Laplacian pyramid page: the 5-tap binomial
kernel (1, 4, 6, 4, 1) / 16, the reflect-101 border, sizes ceil(W / 2) and
ceil(H / 2), and EXPAND by zero insertion and a blur with twice the kernel.
With int or Fraction pixels every step is exact.

Cost: O(W H) time and space for any number of levels, because the levels
shrink by a factor of 4.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Sequence

Image = List[List]
KERNEL = [Fraction(1, 16), Fraction(4, 16), Fraction(6, 16), Fraction(4, 16), Fraction(1, 16)]


def reflect101(i: int, n: int) -> int:
    """Mirror an index into 0 .. n - 1 without repeating the edge sample."""
    if n == 1:
        return 0
    period = 2 * n - 2
    i %= period
    return period - i if i >= n else i


def reduce_level(g: Sequence[Sequence]) -> Image:
    """Blur with the kernel in both directions and keep even rows and columns."""
    h, w = len(g), len(g[0])
    w2, h2 = (w + 1) // 2, (h + 1) // 2
    rows = [[sum(KERNEL[m + 2] * r[reflect101(2 * i + m, w)] for m in range(-2, 3))
             for i in range(w2)] for r in g]
    return [[sum(KERNEL[m + 2] * rows[reflect101(2 * j + m, h)][i] for m in range(-2, 3))
             for i in range(w2)] for j in range(h2)]


def expand(g: Sequence[Sequence], width: int, height: int) -> Image:
    """Put g on the even positions of a zero grid of size width x height and
    blur with twice the kernel per axis (once on an axis of length 1)."""
    z = [[0] * width for _ in range(height)]
    for j, row in enumerate(g):
        for i, val in enumerate(row):
            z[2 * j][2 * i] = val
    gx = 1 if width == 1 else 2
    gy = 1 if height == 1 else 2
    r = [[sum(gx * KERNEL[m + 2] * zr[reflect101(x - m, width)] for m in range(-2, 3))
          for x in range(width)] for zr in z]
    return [[sum(gy * KERNEL[m + 2] * r[reflect101(y - m, height)][x] for m in range(-2, 3))
             for x in range(width)] for y in range(height)]


def gaussian_pyramid(img: Sequence[Sequence], levels: int) -> List[Image]:
    """[G_0, ..., G_N] with G_0 = img and G_(l+1) = REDUCE(G_l), N = levels."""
    pyr = [[list(r) for r in img]]
    for _ in range(levels):
        pyr.append(reduce_level(pyr[-1]))
    return pyr


def laplacian_from_gaussian(gp: Sequence[Image]) -> List[Image]:
    """L_l = G_l - EXPAND(G_(l+1)) for l < N, and L_N = G_N."""
    lap = []
    for lvl in range(len(gp) - 1):
        fine = gp[lvl]
        e = expand(gp[lvl + 1], len(fine[0]), len(fine))
        lap.append([[a - b for a, b in zip(rf, re)] for rf, re in zip(fine, e)])
    lap.append([list(r) for r in gp[-1]])
    return lap


def collapse(lap: Sequence[Image]) -> Image:
    """Undo laplacian_from_gaussian: S = L_N, then S = L_l + EXPAND(S)."""
    s = [list(r) for r in lap[-1]]
    for lvl in range(len(lap) - 2, -1, -1):
        band = lap[lvl]
        e = expand(s, len(band[0]), len(band))
        s = [[a + b for a, b in zip(rb, re)] for rb, re in zip(band, e)]
    return s


def multi_band_blend(A: Sequence[Sequence], B: Sequence[Sequence],
                     M: Sequence[Sequence], levels: int) -> Image:
    """Blend A and B with the mask M over levels + 1 frequency bands.

    Precondition: A, B and M are W x H with W, H >= 1, levels >= 0, and the
    entries of M lie in [0, 1]. levels = 0 gives the plain per-pixel mix
    M A + (1 - M) B. Cost O(W H)."""
    if levels < 0:
        raise ValueError("levels must be >= 0")
    h, w = len(A), len(A[0])
    for img in (B, M):
        if len(img) != h or any(len(r) != w for r in img):
            raise ValueError("A, B and M must have the same size")
    gm = gaussian_pyramid(M, levels)  # @line L1
    ga = gaussian_pyramid(A, levels)  # @line L2
    gb = gaussian_pyramid(B, levels)  # @line L2
    la = laplacian_from_gaussian(ga)  # @line L3
    lb = laplacian_from_gaussian(gb)  # @line L3
    ls = []
    for lvl in range(levels + 1):  # @line L4
        ls.append([[m * a + (1 - m) * b for m, a, b in zip(rm, ra, rb)]  # @line L5
                   for rm, ra, rb in zip(gm[lvl], la[lvl], lb[lvl])])
    s = ls[levels]  # @line L6
    for lvl in range(levels - 1, -1, -1):  # @line L7
        band = ls[lvl]
        e = expand(s, len(band[0]), len(band))
        s = [[a + b for a, b in zip(rb, re)] for rb, re in zip(band, e)]  # @line L8
    return s  # @line L9
