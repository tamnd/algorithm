# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/determinant-of-hessian-detector/. The authors are listed in prov/698GJR.jsonl.

"""Determinant of Hessian (DoH) blob detector with scale selection.

An image is a list of H rows of W floats; pixel (u, v) is img[v][u], with u
the column (to the right) and v the row (down). The scale parameter is the
variance t = sigma^2. L(., t) is the image blurred with a sampled Gaussian of
variance t (cut at radius ceil(3 sigma), normalized, clamp border).

The response is the scale-normalized determinant of the Hessian,

    D(u, v, t) = t^2 (Lxx Lyy - Lxy^2),

with central second differences. A point is a sample (u, v, i), 1 <= i <= K - 2
for K scales, off the border, where D > tau and D is larger than all 26
neighbours in space and scale. It is refined by a parabola in each of u, v
and log t.
"""

import math
from typing import List, Sequence, Tuple

Image = List[List[float]]


def gaussian_kernel(sigma: float) -> List[float]:
    """Sampled Gaussian on -R..R with R = ceil(3 sigma), normalized to sum 1."""
    if sigma <= 0:
        return [1.0]
    rad = max(1, int(math.ceil(3 * sigma)))
    k = [math.exp(-(i * i) / (2 * sigma * sigma)) for i in range(-rad, rad + 1)]
    s = sum(k)
    return [x / s for x in k]


def blur(img: Sequence[Sequence[float]], t: float) -> Image:
    """Separable Gaussian blur of variance t with the clamp border rule."""
    h, w = len(img), len(img[0])
    k = gaussian_kernel(math.sqrt(t))
    r = len(k) // 2
    tmp = [[sum(k[j] * row[min(max(u + j - r, 0), w - 1)] for j in range(len(k))) for u in range(w)]
           for row in img]
    return [[sum(k[j] * tmp[min(max(v + j - r, 0), h - 1)][u] for j in range(len(k))) for u in range(w)]
            for v in range(h)]


def doh_response(img: Sequence[Sequence[float]], t: float) -> Image:
    """t^2 (Lxx Lyy - Lxy^2) at each pixel; 0 on the one-pixel border."""
    L = blur(img, t)
    h, w = len(L), len(L[0])
    out = [[0.0] * w for _ in range(h)]
    for v in range(1, h - 1):
        for u in range(1, w - 1):
            c = L[v][u]
            lxx = L[v][u + 1] + L[v][u - 1] - 2 * c
            lyy = L[v + 1][u] + L[v - 1][u] - 2 * c
            lxy = (L[v + 1][u + 1] - L[v + 1][u - 1] - L[v - 1][u + 1] + L[v - 1][u - 1]) / 4
            out[v][u] = t * t * (lxx * lyy - lxy * lxy)
    return out


def scale_maxima(stack: List[Image], tau: float) -> List[Tuple[int, int, int]]:
    """Samples (i, u, v) off the border of space and scale with value > tau and > all 26 neighbours."""
    out = []
    k, h, w = len(stack), len(stack[0]), len(stack[0][0])
    for i in range(1, k - 1):
        for v in range(1, h - 1):
            for u in range(1, w - 1):
                x = stack[i][v][u]
                if x <= tau:
                    continue
                if all(stack[i + a][v + b][u + c] < x
                       for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1) if a or b or c):
                    out.append((i, u, v))
    return out


def parabola_offset(fm: float, f0: float, fp: float) -> float:
    """Offset of the vertex of the parabola through (-1, fm), (0, f0), (1, fp); 0 if flat."""
    den = fm - 2 * f0 + fp
    if den >= 0:
        return 0.0
    return 0.5 * (fm - fp) / den


def doh_blobs(img: Sequence[Sequence[float]], scales: Sequence[float], tau: float = 0.0):
    """Return blobs (x, y, t, D) for the scale list t_0 < t_1 < ... (best with a constant ratio).

    Precondition: img is a rectangular list of rows of floats, at least 3 x 3,
    and scales has at least 3 increasing positive values.
    """
    stack = [doh_response(img, t) for t in scales]  # @line L1 @line L2
    blobs = []  # @line L3
    for i, u, v in scale_maxima(stack, tau):  # @line L4
        S = stack[i]
        du = parabola_offset(S[v][u - 1], S[v][u], S[v][u + 1])  # @line L5
        dv = parabola_offset(S[v - 1][u], S[v][u], S[v + 1][u])
        di = parabola_offset(stack[i - 1][v][u], S[v][u], stack[i + 1][v][u])
        lo, hi = math.log(scales[i - 1]), math.log(scales[i + 1])
        lt = math.log(scales[i]) + di * ((hi - lo) / 2)
        blobs.append((u + du, v + dv, math.exp(lt), S[v][u]))  # @line L6
    return blobs  # @line L7
