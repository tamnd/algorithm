# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/difference-of-gaussians-detector/. The authors are listed in prov/832KGB.jsonl.

"""Difference-of-Gaussians (DoG) keypoint detector, the detector part of SIFT.

An image is a list of H rows of W floats in [0, 1]; pixel (u, v) is img[v][u],
with u the column (to the right) and v the row (down). The blur is a sampled
Gaussian, cut at radius ceil(3 sigma) and normalized to sum 1, applied to rows
and then to columns with the clamp border rule.

Each octave has s + 3 Gaussian images with sigma_i = sigma0 k^i, k = 2^(1/s),
in the pixel units of the octave, and s + 2 DoG images D_i = G_(i+1) - G_i.
A sample (u, v, i) with 1 <= i <= s, not on the border of the octave, is a
candidate when it is larger than all 26 neighbours or smaller than all of
them. A candidate is refined by fitting a quadratic to D (a 3 x 3 solve). It
is kept when |D| at the fitted point is at least the contrast threshold and
the spatial Hessian passes the edge test tr^2 / det < (r + 1)^2 / r.
"""

import math
from typing import List, Optional, Sequence, Tuple

Image = List[List[float]]


def gaussian_kernel(sigma: float) -> List[float]:
    """Sampled Gaussian on -R..R with R = ceil(3 sigma), normalized to sum 1."""
    if sigma <= 0:
        return [1.0]
    rad = max(1, int(math.ceil(3 * sigma)))
    k = [math.exp(-(i * i) / (2 * sigma * sigma)) for i in range(-rad, rad + 1)]
    s = sum(k)
    return [x / s for x in k]


def blur(img: Sequence[Sequence[float]], sigma: float) -> Image:
    """Separable Gaussian blur with the clamp border rule: rows, then columns."""
    h, w = len(img), len(img[0])
    k = gaussian_kernel(sigma)
    r = len(k) // 2
    tmp = [[sum(k[j] * row[min(max(u + j - r, 0), w - 1)] for j in range(len(k))) for u in range(w)]
           for row in img]
    return [[sum(k[j] * tmp[min(max(v + j - r, 0), h - 1)][u] for j in range(len(k))) for u in range(w)]
            for v in range(h)]


def octave_stack(base: Image, s: int, sigma0: float) -> Tuple[List[Image], List[Image]]:
    """Return the s + 3 Gaussian images and the s + 2 DoG images of one octave.

    base has blur sigma0. Image i is base blurred by sqrt(sigma_i^2 - sigma0^2).
    """
    k = 2.0 ** (1.0 / s)
    gauss = []
    for i in range(s + 3):
        si = sigma0 * k ** i
        gauss.append(blur(base, math.sqrt(max(si * si - sigma0 * sigma0, 0.0))) if i else [row[:] for row in base])
    dog = [[[a - b for a, b in zip(r1, r0)] for r1, r0 in zip(gauss[i + 1], gauss[i])] for i in range(s + 2)]
    return gauss, dog


def find_extrema(dog: List[Image]) -> List[Tuple[int, int, int]]:
    """Samples (i, u, v), 1 <= i <= len(dog) - 2, off the border, larger or smaller than all 26 neighbours."""
    out = []
    h, w = len(dog[0]), len(dog[0][0])
    for i in range(1, len(dog) - 1):
        for v in range(1, h - 1):
            for u in range(1, w - 1):
                x = dog[i][v][u]
                hi = lo = True
                for di in (-1, 0, 1):
                    plane = dog[i + di]
                    for dv in (-1, 0, 1):
                        row = plane[v + dv]
                        for du in (-1, 0, 1):
                            if di == 0 and dv == 0 and du == 0:
                                continue
                            y = row[u + du]
                            if y >= x:
                                hi = False
                            if y <= x:
                                lo = False
                    if not (hi or lo):
                        break
                if hi or lo:
                    out.append((i, u, v))
    return out


def _solve3(m: List[List[float]], b: List[float]) -> Optional[List[float]]:
    """Solve m x = b by Cramer's rule; None if m is singular."""
    def det(a):
        return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
                - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
                + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    d = det(m)
    if abs(d) < 1e-15:
        return None
    out = []
    for c in range(3):
        a = [[b[r] if j == c else m[r][j] for j in range(3)] for r in range(3)]
        out.append(det(a) / d)
    return out


def refine(dog: List[Image], i: int, u: int, v: int, max_steps: int = 5):
    """Fit a quadratic to D around (u, v, i) and move to a neighbour while an offset exceeds 0.5.

    Return (u + du, v + dv, i + di, value, (dxx, dyy, dxy)) or None.
    """
    h, w = len(dog[0]), len(dog[0][0])
    for _ in range(max_steps):
        d = lambda a, b, c: dog[c][b][a]
        g = [(d(u + 1, v, i) - d(u - 1, v, i)) / 2,
             (d(u, v + 1, i) - d(u, v - 1, i)) / 2,
             (d(u, v, i + 1) - d(u, v, i - 1)) / 2]
        c0 = d(u, v, i)
        dxx = d(u + 1, v, i) + d(u - 1, v, i) - 2 * c0
        dyy = d(u, v + 1, i) + d(u, v - 1, i) - 2 * c0
        dss = d(u, v, i + 1) + d(u, v, i - 1) - 2 * c0
        dxy = (d(u + 1, v + 1, i) - d(u - 1, v + 1, i) - d(u + 1, v - 1, i) + d(u - 1, v - 1, i)) / 4
        dxs = (d(u + 1, v, i + 1) - d(u - 1, v, i + 1) - d(u + 1, v, i - 1) + d(u - 1, v, i - 1)) / 4
        dys = (d(u, v + 1, i + 1) - d(u, v - 1, i + 1) - d(u, v + 1, i - 1) + d(u, v - 1, i - 1)) / 4
        hess = [[dxx, dxy, dxs], [dxy, dyy, dys], [dxs, dys, dss]]
        off = _solve3(hess, [-x for x in g])
        if off is None:
            return None
        if all(abs(x) <= 0.5 for x in off):
            value = c0 + 0.5 * sum(a * b for a, b in zip(g, off))
            return (u + off[0], v + off[1], i + off[2], value, (dxx, dyy, dxy))
        u += int(round(off[0]))
        v += int(round(off[1]))
        i += int(round(off[2]))
        if not (1 <= i <= len(dog) - 2 and 1 <= u <= w - 2 and 1 <= v <= h - 2):
            return None
    return None


def passes_edge_test(dxx: float, dyy: float, dxy: float, r: float = 10.0) -> bool:
    """tr^2 / det < (r + 1)^2 / r with det > 0."""
    tr, det = dxx + dyy, dxx * dyy - dxy * dxy
    return det > 0 and tr * tr * r < (r + 1) ** 2 * det


def dog_keypoints(img: Sequence[Sequence[float]], s: int = 3, sigma0: float = 1.6, octaves: int = 2,
                  contrast: float = 0.03, edge_r: float = 10.0, sigma_in: float = 0.5):
    """Return keypoints (x, y, sigma, value) in the pixel units of the input image.

    Precondition: img is a rectangular list of rows of floats in [0, 1],
    s >= 1, 0 <= sigma_in < sigma0 and octaves >= 1. An octave smaller than
    3 x 3 pixels is not searched.
    """
    base = blur(img, math.sqrt(sigma0 * sigma0 - sigma_in * sigma_in))  # @line L1
    keys = []
    for o in range(octaves):  # @line L2
        if len(base) < 3 or len(base[0]) < 3:
            break
        gauss, dog = octave_stack(base, s, sigma0)  # @line L3 @line L4
        for i, u, v in find_extrema(dog):  # @line L5
            fit = refine(dog, i, u, v)  # @line L6
            if fit is None:
                continue
            x, y, si, value, (dxx, dyy, dxy) = fit
            if abs(value) >= contrast and passes_edge_test(dxx, dyy, dxy, edge_r):  # @line L7
                f = 2 ** o
                keys.append((x * f, y * f, sigma0 * 2 ** (o + si / s), value))  # @line L8
        base = [row[::2] for row in gauss[s][::2]]  # @line L9
    return keys  # @line L10
