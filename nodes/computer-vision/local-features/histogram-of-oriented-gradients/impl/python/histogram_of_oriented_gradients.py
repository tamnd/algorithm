# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/histogram-of-oriented-gradients/. The authors are listed in prov/DA8C98.jsonl.

"""Histogram of oriented gradients (HOG) for one detection window.

An image is a list of H rows of W numbers; pixel (u, v) is img[v][u], with u
the column (to the right) and v the row (down). The window is the whole image.

Steps, following the default detector of Dalal and Triggs (2005):
1. Gradients by the centered masks [-1, 0, 1] in u and in v, with no
   smoothing. At the border the image is extended by its edge pixels.
2. Unsigned orientation phi = atan2(g_v, g_u) folded into [0, 180) degrees.
3. Each pixel votes its gradient magnitude into the two nearest of the B
   orientation bins (centers at (b + 1/2) 180 / B degrees, circular), with
   linear weights. With spatial=True it also splits its vote between the four
   nearest cell centers with bilinear weights (trilinear voting).
4. Blocks of 2 x 2 cells, with a stride of one cell, are normalized by L2-Hys:
   v / sqrt(|v|^2 + eps^2), values clipped at 0.2, then normalized again.

The Gaussian window over each block (sigma = half the block width) of the
paper is left out; so the cell histograms are shared by all blocks.
"""

import math
from typing import List, Sequence

Image = Sequence[Sequence[float]]


def gradients(img: Image):
    """Return (magnitude, angle in degrees in [0, 180)) for each pixel."""
    h, w = len(img), len(img[0])
    mag = [[0.0] * w for _ in range(h)]
    ang = [[0.0] * w for _ in range(h)]
    for v in range(h):
        for u in range(w):
            gu = img[v][min(u + 1, w - 1)] - img[v][max(u - 1, 0)]  # @line L1
            gv = img[min(v + 1, h - 1)][u] - img[max(v - 1, 0)][u]
            mag[v][u] = math.hypot(gu, gv)
            a = math.degrees(math.atan2(gv, gu)) % 180.0  # @line L2
            ang[v][u] = 0.0 if a >= 180.0 else a
    return mag, ang


def orientation_votes(angle: float, bins: int):
    """The two bins and their weights for an unsigned angle in [0, 180)."""
    width = 180.0 / bins
    x = angle / width - 0.5
    b0 = math.floor(x)
    f = x - b0
    return (b0 % bins, 1.0 - f), ((b0 + 1) % bins, f)


def cell_histograms(img: Image, cell: int = 8, bins: int = 9, spatial: bool = True) -> List[List[List[float]]]:
    """Histograms hist[cy][cx][b] of the cells of size cell x cell."""
    h, w = len(img), len(img[0])
    ny, nx = h // cell, w // cell
    hist = [[[0.0] * bins for _ in range(nx)] for _ in range(ny)]
    mag, ang = gradients(img)
    for v in range(ny * cell):
        for u in range(nx * cell):
            m = mag[v][u]
            if m == 0.0:
                continue
            ov = orientation_votes(ang[v][u], bins)  # @line L3
            if not spatial:
                cy, cx = v // cell, u // cell
                for b, wb in ov:
                    hist[cy][cx][b] += m * wb
                continue
            # Cell centers are at (c + 1/2) cell - 1/2 in pixel coordinates.
            x = (u + 0.5) / cell - 0.5
            y = (v + 0.5) / cell - 0.5
            x0, y0 = math.floor(x), math.floor(y)
            fx, fy = x - x0, y - y0
            for cy, wy in ((y0, 1.0 - fy), (y0 + 1, fy)):
                if not 0 <= cy < ny or wy == 0.0:
                    continue
                for cx, wx in ((x0, 1.0 - fx), (x0 + 1, fx)):
                    if not 0 <= cx < nx or wx == 0.0:
                        continue
                    for b, wb in ov:
                        hist[cy][cx][b] += m * wy * wx * wb  # @line L4
    return hist


def l2_hys(vec: List[float], eps: float = 1e-3, clip: float = 0.2) -> List[float]:
    """L2 normalization, clipping at clip, and L2 normalization again."""
    n = math.sqrt(sum(x * x for x in vec) + eps * eps)
    out = [min(x / n, clip) for x in vec]
    n2 = math.sqrt(sum(x * x for x in out) + eps * eps)
    return [x / n2 for x in out]


def hog(img: Image, cell: int = 8, bins: int = 9, block: int = 2, spatial: bool = True,
        eps: float = 1e-3) -> List[float]:
    """The HOG descriptor of the window: the normalized blocks, row by row."""
    hist = cell_histograms(img, cell, bins, spatial)
    ny, nx = len(hist), len(hist[0]) if hist else 0
    out: List[float] = []
    for by in range(ny - block + 1):  # @line L5
        for bx in range(nx - block + 1):
            vec: List[float] = []
            for cy in range(by, by + block):
                for cx in range(bx, bx + block):
                    vec.extend(hist[cy][cx])  # @line L6
            out.extend(l2_hys(vec, eps))  # @line L7
    return out  # @line L8


def hog_length(width: int, height: int, cell: int = 8, bins: int = 9, block: int = 2) -> int:
    """Length of the descriptor of a width x height window with a stride of one cell."""
    nx, ny = width // cell, height // cell
    return (nx - block + 1) * (ny - block + 1) * block * block * bins
