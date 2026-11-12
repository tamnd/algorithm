# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lossy-image-compression/. The authors are listed in prov/DWVCRA.jsonl.

"""Pieces of a lossy image coder that do not depend on the transform: the
JFIF colour conversion between RGB and YCbCr, 4:2:0 chroma subsampling, and
the two usual quality measures, PSNR and SSIM (Wang, Bovik, Sheikh and
Simoncelli, 2004).

An image is a list of rows of numbers. Every function costs time linear in
the number of pixels, except ssim, which costs O(w^2) per pixel for a
w x w window (w = 11 by default).
"""

import math
from typing import List, Sequence, Tuple

Image = List[List[float]]

# JFIF 1.02, "Conversion to and from RGB" (also ITU-T T.871, clause 7).
_Y = (0.299, 0.587, 0.114)
_CB = (-0.1687, -0.3313, 0.5)
_CR = (0.5, -0.4187, -0.0813)


def rgb_to_ycbcr(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """JFIF forward conversion of one pixel; values stay real (no rounding)."""
    y = _Y[0] * r + _Y[1] * g + _Y[2] * b
    cb = _CB[0] * r + _CB[1] * g + _CB[2] * b + 128
    cr = _CR[0] * r + _CR[1] * g + _CR[2] * b + 128
    return y, cb, cr


def ycbcr_to_rgb(y: float, cb: float, cr: float) -> Tuple[float, float, float]:
    """JFIF inverse conversion of one pixel; values stay real (no clamping)."""
    r = y + 1.402 * (cr - 128)
    g = y - 0.34414 * (cb - 128) - 0.71414 * (cr - 128)
    b = y + 1.772 * (cb - 128)
    return r, g, b


def clamp8(v: float) -> int:
    """Round to the nearest integer and clamp to 0..255."""
    return max(0, min(255, int(math.floor(v + 0.5))))


def subsample_420(plane: Sequence[Sequence[float]]) -> Image:
    """Average each 2 x 2 block (the edge row or column is repeated for odd sizes)."""
    h, w = len(plane), len(plane[0])
    out = []
    for i in range(0, h, 2):
        row = []
        for j in range(0, w, 2):
            i2, j2 = min(i + 1, h - 1), min(j + 1, w - 1)
            row.append((plane[i][j] + plane[i][j2] + plane[i2][j] + plane[i2][j2]) / 4)
        out.append(row)
    return out


def upsample_420(plane: Sequence[Sequence[float]], h: int, w: int) -> Image:
    """Replicate each chroma sample over its 2 x 2 block, cut to h x w."""
    return [[plane[i // 2][j // 2] for j in range(w)] for i in range(h)]


def mse(x: Sequence[Sequence[float]], y: Sequence[Sequence[float]]) -> float:
    """Mean squared error of two images of the same size."""
    n = 0
    s = 0.0
    for rx, ry in zip(x, y):
        for a, b in zip(rx, ry):
            s += (a - b) ** 2
            n += 1
    return s / n


def psnr(x: Sequence[Sequence[float]], y: Sequence[Sequence[float]], peak: float = 255.0) -> float:
    """10 log10(peak^2 / MSE) in dB; infinite for equal images."""
    d = mse(x, y)
    return math.inf if d == 0 else 10 * math.log10(peak * peak / d)


def gaussian_window(size: int = 11, sigma: float = 1.5) -> List[List[float]]:
    """Circular-symmetric Gaussian weights normalized to unit sum."""
    c = (size - 1) / 2
    w = [[math.exp(-((i - c) ** 2 + (j - c) ** 2) / (2 * sigma * sigma)) for j in range(size)] for i in range(size)]
    total = sum(map(sum, w))
    return [[v / total for v in row] for row in w]


def ssim_window(x: Sequence[float], y: Sequence[float], w: Sequence[float], peak: float = 255.0, k1: float = 0.01, k2: float = 0.03) -> float:
    """SSIM of two equal-length samples with weights w (summing to 1)."""
    c1, c2 = (k1 * peak) ** 2, (k2 * peak) ** 2  # @line L1
    mx = sum(wi * a for wi, a in zip(w, x))  # @line L2
    my = sum(wi * b for wi, b in zip(w, y))
    vx = sum(wi * (a - mx) ** 2 for wi, a in zip(w, x))  # @line L3
    vy = sum(wi * (b - my) ** 2 for wi, b in zip(w, y))
    cxy = sum(wi * (a - mx) * (b - my) for wi, a, b in zip(w, x, y))
    return ((2 * mx * my + c1) * (2 * cxy + c2)) / ((mx * mx + my * my + c1) * (vx + vy + c2))  # @line L4


def ssim(x: Sequence[Sequence[float]], y: Sequence[Sequence[float]], size: int = 11, sigma: float = 1.5, peak: float = 255.0) -> float:
    """Mean SSIM over every window position that fits inside the image.

    With sigma = 0 the window is uniform. Images smaller than the window
    use one window that covers the whole image, with uniform weights.
    """
    h, wd = len(x), len(x[0])
    if h < size or wd < size:
        flat_x = [v for row in x for v in row]
        flat_y = [v for row in y for v in row]
        n = len(flat_x)
        return ssim_window(flat_x, flat_y, [1.0 / n] * n, peak)
    if sigma > 0:
        win = [v for row in gaussian_window(size, sigma) for v in row]
    else:
        win = [1.0 / (size * size)] * (size * size)
    total = 0.0
    count = 0
    for i in range(h - size + 1):  # @line L5
        for j in range(wd - size + 1):
            px = [x[i + a][j + b] for a in range(size) for b in range(size)]
            py = [y[i + a][j + b] for a in range(size) for b in range(size)]
            total += ssim_window(px, py, win, peak)  # @line L6
            count += 1
    return total / count  # @line L7
