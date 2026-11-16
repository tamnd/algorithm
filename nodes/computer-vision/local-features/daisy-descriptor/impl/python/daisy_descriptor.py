# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/daisy-descriptor/. The authors are listed in prov/HGVST3.jsonl.

"""DAISY: a dense descriptor from convolved orientation maps (Tola, Lepetit and Fua).

An image is a list of H rows of W numbers; pixel (u, v) is img[v][u], with u
the column (to the right) and v the row (down). Angles grow from the u axis
toward the v axis.

1. Gradients by central differences, with the border pixels repeated.
2. B orientation maps G_o = max(0, cos(t_o) g_u + sin(t_o) g_v), t_o = 2 pi o / B.
3. Each map is convolved with Gaussians of sigma_i = R (i + 1) / (2 Q) for
   i = 0, ..., Q - 1, incrementally: the layer i + 1 is the layer i convolved
   with sigma = sqrt(sigma_{i+1}^2 - sigma_i^2).
4. At a pixel, the descriptor has 1 + Q T histograms of B values: one at the
   center from layer 0, and T on each ring i of radius R (i + 1) / Q from
   layer i, read by bilinear interpolation. Each histogram is scaled to length
   1 on its own. The defaults R = 15, Q = 3, T = 8, B = 8 give 200 values.

Turning the descriptor by k steps of 2 pi / T moves the ring points by k and,
when B is a multiple of T, the histogram bins by k B / T.
"""

import math
from typing import List, Sequence

Image = Sequence[Sequence[float]]
Map = List[List[float]]


def gradients(img: Image):
    h, w = len(img), len(img[0])
    gu = [[(img[v][min(u + 1, w - 1)] - img[v][max(u - 1, 0)]) / 2.0 for u in range(w)] for v in range(h)]
    gv = [[(img[min(v + 1, h - 1)][u] - img[max(v - 1, 0)][u]) / 2.0 for u in range(w)] for v in range(h)]
    return gu, gv  # @line L1


def orientation_maps(img: Image, bins: int = 8) -> List[Map]:
    gu, gv = gradients(img)
    h, w = len(img), len(img[0])
    maps = []
    for o in range(bins):
        c, s = math.cos(2 * math.pi * o / bins), math.sin(2 * math.pi * o / bins)
        maps.append([[max(0.0, c * gu[v][u] + s * gv[v][u]) for u in range(w)] for v in range(h)])  # @line L2
    return maps


def gaussian_kernel(sigma: float) -> List[float]:
    r = max(1, int(math.ceil(4 * sigma)))
    k = [math.exp(-(x * x) / (2 * sigma * sigma)) for x in range(-r, r + 1)]
    s = sum(k)
    return [x / s for x in k]


def convolve(m: Map, sigma: float) -> Map:
    """Separable Gaussian convolution with the border pixels repeated."""
    k = gaussian_kernel(sigma)
    r = len(k) // 2
    h, w = len(m), len(m[0])
    tmp = [[sum(k[i] * row[min(max(u + i - r, 0), w - 1)] for i in range(len(k))) for u in range(w)] for row in m]
    return [[sum(k[i] * tmp[min(max(v + i - r, 0), h - 1)][u] for i in range(len(k))) for u in range(w)]
            for v in range(h)]


def sigmas(R: float = 15.0, Q: int = 3) -> List[float]:
    return [R * (i + 1) / (2 * Q) for i in range(Q)]


def layers(img: Image, R: float = 15.0, Q: int = 3, bins: int = 8) -> List[List[Map]]:
    """layers[i][o]: the map o convolved with sigma_i, built incrementally."""
    maps = orientation_maps(img, bins)
    out = []
    prev = 0.0
    cur = maps
    for s in sigmas(R, Q):
        cur = [convolve(m, math.sqrt(s * s - prev * prev)) for m in cur]  # @line L3
        out.append(cur)
        prev = s
    return out


def bilinear(m: Map, x: float, y: float) -> float:
    h, w = len(m), len(m[0])
    x = min(max(x, 0.0), w - 1.0)
    y = min(max(y, 0.0), h - 1.0)
    x0, y0 = min(int(x), w - 2), min(int(y), h - 2)
    fx, fy = x - x0, y - y0
    return ((1 - fy) * ((1 - fx) * m[y0][x0] + fx * m[y0][x0 + 1])
            + fy * ((1 - fx) * m[y0 + 1][x0] + fx * m[y0 + 1][x0 + 1]))


def _unit(h: List[float]) -> List[float]:
    n = math.sqrt(sum(x * x for x in h))
    return [x / n for x in h] if n > 0 else h


def describe(lay: List[List[Map]], u: float, v: float, R: float = 15.0, T: int = 8, k: int = 0) -> List[float]:
    """The descriptor at (u, v), turned by k steps of 2 pi / T."""
    Q, bins = len(lay), len(lay[0])
    if k % T and bins % T:
        raise ValueError("turning needs a number of bins that is a multiple of T")
    shift = k * bins // T
    hist = [lay[0][(o + shift) % bins] for o in range(bins)]
    out = _unit([bilinear(m, u, v) for m in hist])  # @line L5
    for i in range(Q):
        r = R * (i + 1) / Q
        maps = [lay[i][(o + shift) % bins] for o in range(bins)]
        for j in range(T):
            a = 2 * math.pi * ((j + k) % T) / T
            x, y = u + r * math.cos(a), v + r * math.sin(a)
            out.extend(_unit([bilinear(m, x, y) for m in maps]))  # @line L6
    return out  # @line L7


def daisy(img: Image, step: int = 1, R: float = 15.0, Q: int = 3, T: int = 8, bins: int = 8):
    """Dense descriptors on the grid of the given step: {(u, v): descriptor}."""
    lay = layers(img, R, Q, bins)
    h, w = len(img), len(img[0])
    out = {}
    for v in range(0, h, step):  # @line L4
        for u in range(0, w, step):
            out[(u, v)] = describe(lay, u, v, R, T)
    return out  # @line L8
