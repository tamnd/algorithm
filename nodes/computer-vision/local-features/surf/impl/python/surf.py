# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/surf/. The authors are listed in prov/RH1WJP.jsonl.

"""Speeded up robust features (SURF): Fast-Hessian detector and 64-value descriptor.

An image is a list of H rows of W numbers; pixel (u, v) is img[v][u], with u
the column (to the right) and v the row (down). Angles are atan2(dv, du).

Detector (Bay, Tuytelaars and Van Gool): box filters of odd size L = 9, 15,
21, 27, ... approximate the second derivatives of a Gaussian with scale
s = 1.2 L / 9. Each response is divided by L^2, and the blob response is
det = Dxx Dyy - (0.9 Dxy)^2. Keypoints are local maxima over 3 x 3 x 3
neighbors in (u, v, L) above a threshold, refined by a quadratic fit.

Orientation: Haar responses of size 4s at the points of step s within a
radius of 6s, weighted by a Gaussian with sigma 2.5s; the longest sum of the
responses in a sliding window of pi/3 gives the direction.

Descriptor: a square of side 20s turned to the orientation, 4 x 4 subregions
of 5 x 5 samples; Haar responses of size 2s, weighted by a Gaussian with
sigma 3.3s, turned into the frame of the keypoint; each subregion gives
(sum dx, sum dy, sum |dx|, sum |dy|), and the 64 values are scaled to length 1.

Outside the image a box sum counts 0 (zero padding).
"""

import math
from typing import List, Optional, Sequence, Tuple

Image = Sequence[Sequence[float]]


def integral_image(img: Image) -> List[List[float]]:
    """ii[v][u] = sum of img over rows < v and columns < u."""
    h, w = len(img), len(img[0])
    ii = [[0] * (w + 1) for _ in range(h + 1)]
    for v in range(h):
        row = 0
        for u in range(w):
            row += img[v][u]
            ii[v + 1][u + 1] = ii[v][u + 1] + row
    return ii


def box(ii, u0: int, v0: int, u1: int, v1: int):
    """Sum over columns u0 <= u < u1 and rows v0 <= v < v1, clipped to the image."""
    h, w = len(ii) - 1, len(ii[0]) - 1
    u0, u1 = max(0, min(w, u0)), max(0, min(w, u1))
    v0, v1 = max(0, min(h, v0)), max(0, min(h, v1))
    if u0 >= u1 or v0 >= v1:
        return 0
    return ii[v1][u1] - ii[v0][u1] - ii[v1][u0] + ii[v0][u0]


def hessian_boxes(ii, u: int, v: int, size: int) -> Tuple[float, float, float]:
    """Box filter approximations (Dxx, Dyy, Dxy) of size x size at (u, v), divided by size^2."""
    l0 = size // 3
    half = (size - 1) // 2
    # Dxx: lobes +1, -2, +1 along u, each l0 wide and 2 l0 - 1 high.
    whole = box(ii, u - half, v - l0 + 1, u + half + 1, v + l0)
    mid = box(ii, u - (l0 - 1) // 2, v - l0 + 1, u + (l0 - 1) // 2 + 1, v + l0)
    dxx = whole - 3 * mid
    whole = box(ii, u - l0 + 1, v - half, u + l0, v + half + 1)
    mid = box(ii, u - l0 + 1, v - (l0 - 1) // 2, u + l0, v + (l0 - 1) // 2 + 1)
    dyy = whole - 3 * mid
    # Dxy: four l0 x l0 squares, +1 on the top-left and bottom-right, -1 on the others.
    dxy = (box(ii, u - l0, v - l0, u, v) + box(ii, u + 1, v + 1, u + l0 + 1, v + l0 + 1)
           - box(ii, u + 1, v - l0, u + l0 + 1, v) - box(ii, u - l0, v + 1, u, v + l0 + 1))
    a = float(size * size)
    return dxx / a, dyy / a, dxy / a  # @line L2


def hessian_det(ii, u: int, v: int, size: int, w: float = 0.9) -> float:
    dxx, dyy, dxy = hessian_boxes(ii, u, v, size)
    return dxx * dyy - (w * dxy) ** 2  # @line L3


def filter_sizes(octave: int, layers: int = 4) -> List[int]:
    """Sizes 9, 15, 21, 27 for octave 0; 15, 27, 39, 51 for octave 1; and so on."""
    return [3 * ((2 ** (octave + 1)) * (i + 1) + 1) for i in range(layers)]


def _solve3(a, b):
    """Solve the 3 x 3 system a x = b by Cramer's rule; None if singular."""
    def det3(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    d = det3(a)
    if abs(d) < 1e-300:
        return None
    out = []
    for k in range(3):
        m = [row[:] for row in a]
        for i in range(3):
            m[i][k] = b[i]
        out.append(det3(m) / d)
    return out


def detect(img: Image, threshold: float = 1.0, octaves: int = 2, ii=None) -> List[Tuple[float, float, float, int]]:
    """Fast-Hessian keypoints (u, v, s, sign of the Laplacian)."""
    if ii is None:
        ii = integral_image(img)  # @line L1
    h, w = len(img), len(img[0])
    keypoints = []
    for o in range(octaves):
        sizes = filter_sizes(o)
        step = 2 ** o
        margin = (sizes[-1] - 1) // 2 + step
        us = list(range(margin, w - margin, step))
        vs = list(range(margin, h - margin, step))
        if len(us) < 3 or len(vs) < 3:
            continue
        maps = [[[hessian_det(ii, u, v, L) for u in us] for v in vs] for L in sizes]
        for k in range(1, len(sizes) - 1):
            for j in range(1, len(vs) - 1):
                for i in range(1, len(us) - 1):
                    d = maps[k][j][i]
                    if d <= threshold:
                        continue
                    if any(maps[k + dk][j + dj][i + di] >= d
                           for dk in (-1, 0, 1) for dj in (-1, 0, 1) for di in (-1, 0, 1)
                           if (dk, dj, di) != (0, 0, 0)):
                        continue  # @line L4
                    # Quadratic fit in (u, v, L) as in Brown and Lowe.
                    f = lambda dk, dj, di: maps[k + dk][j + dj][i + di]
                    g = [(f(0, 0, 1) - f(0, 0, -1)) / 2, (f(0, 1, 0) - f(0, -1, 0)) / 2,
                         (f(1, 0, 0) - f(-1, 0, 0)) / 2]
                    hxx = f(0, 0, 1) + f(0, 0, -1) - 2 * d
                    hyy = f(0, 1, 0) + f(0, -1, 0) - 2 * d
                    hss = f(1, 0, 0) + f(-1, 0, 0) - 2 * d
                    hxy = (f(0, 1, 1) - f(0, 1, -1) - f(0, -1, 1) + f(0, -1, -1)) / 4
                    hxs = (f(1, 0, 1) - f(1, 0, -1) - f(-1, 0, 1) + f(-1, 0, -1)) / 4
                    hys = (f(1, 1, 0) - f(1, -1, 0) - f(-1, 1, 0) + f(-1, -1, 0)) / 4
                    off = _solve3([[hxx, hxy, hxs], [hxy, hyy, hys], [hxs, hys, hss]], [-x for x in g])
                    if off is None or max(abs(x) for x in off) > 0.5:
                        off = [0.0, 0.0, 0.0]
                    u = us[i] + off[0] * step
                    v = vs[j] + off[1] * step
                    size = sizes[k] + off[2] * (sizes[k + 1] - sizes[k])
                    dxx, dyy, _ = hessian_boxes(ii, us[i], vs[j], sizes[k])
                    keypoints.append((u, v, 1.2 * size / 9.0, 1 if dxx + dyy >= 0 else -1))
    return keypoints


def haar(ii, u: float, v: float, size: int) -> Tuple[float, float]:
    """Haar wavelet responses (dx, dy) of side size (even) centered near (u, v)."""
    cu, cv, r = int(round(u)), int(round(v)), size // 2
    dx = box(ii, cu, cv - r, cu + r, cv + r) - box(ii, cu - r, cv - r, cu, cv + r)
    dy = box(ii, cu - r, cv, cu + r, cv + r) - box(ii, cu - r, cv - r, cu + r, cv)
    return dx, dy


def _haar_size(t: float) -> int:
    return max(2, 2 * int(round(t / 2.0)))


def orientation(ii, u: float, v: float, s: float) -> float:
    """Dominant direction of the Haar responses around (u, v) at scale s."""
    hs = _haar_size(4 * s)
    resp = []
    for j in range(-6, 7):
        for i in range(-6, 7):
            if i * i + j * j >= 36:
                continue
            g = math.exp(-(i * i + j * j) / (2 * 2.5 * 2.5))
            dx, dy = haar(ii, u + i * s, v + j * s, hs)
            if dx or dy:
                resp.append((g * dx, g * dy, math.atan2(g * dy, g * dx)))  # @line L5
    if not resp:
        return 0.0
    best, best_angle = -1.0, 0.0
    for _, _, a0 in resp:
        sx = sy = 0.0
        for dx, dy, a in resp:
            d = (a - a0 + math.pi) % (2 * math.pi) - math.pi
            if abs(d) <= math.pi / 6:
                sx += dx
                sy += dy
        n = sx * sx + sy * sy
        if n > best:
            best, best_angle = n, math.atan2(sy, sx)
    return best_angle  # @line L6


def describe(ii, u: float, v: float, s: float, theta: float = 0.0) -> List[float]:
    """The 64-value SURF descriptor of a keypoint with orientation theta (0 gives U-SURF)."""
    c, sn = math.cos(theta), math.sin(theta)
    hs = _haar_size(2 * s)
    desc = [0.0] * 64
    for l in range(20):
        for k in range(20):
            x, y = (k - 9.5) * s, (l - 9.5) * s
            pu, pv = u + c * x - sn * y, v + sn * x + c * y
            dx, dy = haar(ii, pu, pv, hs)
            g = math.exp(-((k - 9.5) ** 2 + (l - 9.5) ** 2) / (2 * 3.3 * 3.3))
            rx, ry = g * (c * dx + sn * dy), g * (-sn * dx + c * dy)
            b = 4 * (4 * (l // 5) + k // 5)
            desc[b] += rx
            desc[b + 1] += ry
            desc[b + 2] += abs(rx)
            desc[b + 3] += abs(ry)  # @line L7
    n = math.sqrt(sum(x * x for x in desc))
    return [x / n for x in desc] if n > 0 else desc  # @line L8


def surf(img: Image, threshold: float = 1.0, octaves: int = 2, upright: bool = False):
    """Detect keypoints and return a list of ((u, v, s, theta, laplacian sign), descriptor)."""
    ii = integral_image(img)
    out = []
    for u, v, s, sign in detect(img, threshold, octaves, ii):
        theta = 0.0 if upright else orientation(ii, u, v, s)
        out.append(((u, v, s, theta, sign), describe(ii, u, v, s, theta)))
    return out


def nearest(desc: List[float], others: List[List[float]]) -> Optional[int]:
    """Index of the descriptor nearest to desc in Euclidean distance."""
    best, arg = math.inf, None
    for i, o in enumerate(others):
        d = sum((a - b) ** 2 for a, b in zip(desc, o))
        if d < best:
            best, arg = d, i
    return arg
