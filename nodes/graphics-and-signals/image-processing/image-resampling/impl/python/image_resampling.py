# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/image-resampling/. The authors are listed in prov/ZHSZ9B.jsonl.

"""Resize a gray image by separable resampling with a reconstruction kernel.

The input is a list of H rows of W numbers. Pixel j of a row of n pixels
covers the interval [j, j+1) and has its center at j + 1/2, so for an
output row of m pixels the center of output pixel j sits at the input
coordinate

    x = (j + 1/2) * n / m - 1/2,

measured so that input pixel centers are at the integers 0, ..., n-1.
The output value is a weighted sum of input pixels,

    out(j) = sum_i k((x - i) / s) in(clamp(i)) / sum_i k((x - i) / s),

where k is the kernel, clamp(i) is the nearest index in 0..n-1, and s is
the scale n/m when antialias is on and n > m, else 1. Widening the kernel
by s when the image gets smaller makes it a low-pass filter that removes
the frequencies the smaller grid cannot hold.

The kernels are the box (nearest neighbor), the tent (linear) and the
Keys cubic with a = -1/2. Coordinates and weights are exact fractions, so
integer or Fraction input gives exact Fraction output. A 2D resize applies
the 1D rule to every row and then to every column. Cost: O((W' H + W' H')
c) time for an output of W' x H' pixels, with c taps per output sample.
"""

import math
from fractions import Fraction
from typing import Callable, Dict, List, Sequence

HALF = Fraction(1, 2)


def box(t: Fraction) -> Fraction:
    """Nearest neighbor kernel: 1 on [-1/2, 1/2), else 0."""
    return Fraction(1) if -HALF <= t < HALF else Fraction(0)


def tent(t: Fraction) -> Fraction:
    """Linear interpolation kernel: 1 - |t| on |t| < 1, else 0."""
    t = abs(t)
    return 1 - t if t < 1 else Fraction(0)


def keys(t: Fraction, a: Fraction = Fraction(-1, 2)) -> Fraction:
    """Keys (1981) cubic convolution kernel with parameter a."""
    t = abs(t)
    if t < 1:
        return (a + 2) * t ** 3 - (a + 3) * t ** 2 + 1
    if t < 2:
        return a * t ** 3 - 5 * a * t ** 2 + 8 * a * t - 4 * a
    return Fraction(0)


KERNELS: Dict[str, tuple] = {
    "nearest": (box, HALF),
    "linear": (tent, Fraction(1)),
    "cubic": (keys, Fraction(2)),
}


def weights(n: int, m: int, kernel: str = "linear", antialias: bool = True) -> List[Dict[int, Fraction]]:
    """For each of m output samples, the map from input index to normalized weight."""
    if n < 1 or m < 1:
        raise ValueError("sizes must be positive")
    k, support = KERNELS[kernel]
    s = Fraction(n, m)
    scale = s if antialias and s > 1 else Fraction(1)
    rows = []
    for j in range(m):
        x = (j + HALF) * s - HALF
        lo = math.floor(x - support * scale)
        hi = math.ceil(x + support * scale)
        acc: Dict[int, Fraction] = {}
        for i in range(lo, hi + 1):
            w = k((x - i) / scale)
            if w:
                c = min(max(i, 0), n - 1)
                acc[c] = acc.get(c, 0) + w
        total = sum(acc.values())
        rows.append({c: w / total for c, w in acc.items()})
    return rows


def resample_row(row: Sequence, m: int, kernel: str = "linear", antialias: bool = True) -> list:
    """Resample one row of samples to m samples."""
    return [sum(w * row[i] for i, w in ws.items()) for ws in weights(len(row), m, kernel, antialias)]


def resize(img: Sequence[Sequence], new_w: int, new_h: int, kernel: str = "linear",
           antialias: bool = True) -> list:
    """Resize an H x W image to new_h rows of new_w samples, rows first, then columns."""
    if not img or not img[0]:
        raise ValueError("the image is empty")
    w = len(img[0])
    if any(len(r) != w for r in img):
        raise ValueError("rows must have the same length")
    wide = [resample_row(r, new_w, kernel, antialias) for r in img]
    cols = [resample_row([r[x] for r in wide], new_h, kernel, antialias) for x in range(new_w)]
    return [[cols[x][y] for x in range(new_w)] for y in range(new_h)]
