# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/screen-space-ambient-occlusion/. The authors are listed in prov/EGC7ET.jsonl.

"""Screen-space ambient occlusion with sample points tested against the depth buffer.

The camera is orthographic and looks along -z, so that the tests can use
height fields with known answers. The pixel (i, j) has its center at
(i + 1/2, j + 1/2) in view units, j counted from the bottom, and D[j][i] is the
positive view depth of the visible surface. The point of a pixel with depth d
is P = (x, y, -d). The result per pixel is the visibility A in [0, 1]: 1 means
not occluded.

Two kernels are given: points in a sphere around P, as in the first SSAO of
2007, and points in the hemisphere around the normal. The depth lookup is
bilinear (exact on planes) or nearest (exact on steps at pixel edges).
"""

import math
import random
from typing import List, Optional, Sequence, Tuple

Vec = Tuple[float, float, float]
Grid = List[List[float]]


def lookup(D: Grid, x: float, y: float, mode: str = "bilinear") -> float:
    """The depth buffer at a screen position, clamped at the borders."""
    h, w = len(D), len(D[0])
    if mode == "nearest":
        i = min(max(int(math.floor(x)), 0), w - 1)
        j = min(max(int(math.floor(y)), 0), h - 1)
        return D[j][i]
    u = min(max(x - 0.5, 0.0), w - 1.0)
    v = min(max(y - 0.5, 0.0), h - 1.0)
    i0, j0 = min(int(u), w - 2) if w > 1 else 0, min(int(v), h - 2) if h > 1 else 0
    i1, j1 = min(i0 + 1, w - 1), min(j0 + 1, h - 1)
    fu, fv = u - i0, v - j0
    top = D[j0][i0] * (1 - fu) + D[j0][i1] * fu
    bot = D[j1][i0] * (1 - fu) + D[j1][i1] * fu
    return top * (1 - fv) + bot * fv


def normal_from_depth(D: Grid, i: int, j: int) -> Vec:
    """The normal of the surface z = -D from central differences, facing +z."""
    h, w = len(D), len(D[0])
    il, ir = max(i - 1, 0), min(i + 1, w - 1)
    jb, jt = max(j - 1, 0), min(j + 1, h - 1)
    gx = (D[j][ir] - D[j][il]) / (ir - il) if ir > il else 0.0
    gy = (D[jt][i] - D[jb][i]) / (jt - jb) if jt > jb else 0.0
    n = (gx, gy, 1.0)
    s = math.sqrt(gx * gx + gy * gy + 1.0)
    return (n[0] / s, n[1] / s, n[2] / s)


def _ball_point(rng: random.Random, radius: float) -> Vec:
    while True:
        p = (rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))
        if 0 < p[0] ** 2 + p[1] ** 2 + p[2] ** 2 <= 1:
            return (p[0] * radius, p[1] * radius, p[2] * radius)


def sphere_kernel(rng: random.Random, pairs: int, radius: float) -> List[Vec]:
    """Uniform points in a ball, in antithetic pairs k and -k."""
    out = []
    for _ in range(pairs):
        k = _ball_point(rng, radius)
        out += [k, (-k[0], -k[1], -k[2])]
    return out


def hemisphere_kernel(rng: random.Random, count: int, radius: float) -> List[Vec]:
    """Uniform points in the half ball with z > 0, in the tangent frame."""
    out = []
    while len(out) < count:
        k = _ball_point(rng, radius)
        if k[2] != 0:
            out.append((k[0], k[1], abs(k[2])))
    return out


def to_normal_frame(k: Vec, n: Vec) -> Vec:
    """Rotate a tangent-frame offset so that its z axis becomes n."""
    a = (1.0, 0.0, 0.0) if abs(n[0]) < 0.9 else (0.0, 1.0, 0.0)
    # t = normalize(a - (a . n) n), b = n x t
    d = a[0] * n[0] + a[1] * n[1] + a[2] * n[2]
    t = (a[0] - d * n[0], a[1] - d * n[1], a[2] - d * n[2])
    tl = math.sqrt(t[0] ** 2 + t[1] ** 2 + t[2] ** 2)
    t = (t[0] / tl, t[1] / tl, t[2] / tl)
    b = (n[1] * t[2] - n[2] * t[1], n[2] * t[0] - n[0] * t[2], n[0] * t[1] - n[1] * t[0])
    return tuple(k[0] * t[c] + k[1] * b[c] + k[2] * n[c] for c in range(3))


def smoothstep01(t: float) -> float:
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def ssao_pixel(
    D: Grid,
    i: int,
    j: int,
    kernel: Sequence[Vec],
    oriented: bool,
    bias: float = 0.0,
    range_radius: Optional[float] = None,
    mode: str = "bilinear",
) -> float:
    d = D[j][i]
    P = (i + 0.5, j + 0.5, -d)  # @line L1
    n = normal_from_depth(D, i, j) if oriented else None  # @line L2
    occ = 0.0  # @line L3
    for k in kernel:  # @line L4
        o = to_normal_frame(k, n) if oriented else k
        s = (P[0] + o[0], P[1] + o[1], P[2] + o[2])
        b = lookup(D, s[0], s[1], mode)  # @line L5
        ds = -s[2]
        if b < ds - bias:  # @line L6
            if range_radius is None:
                occ += 1.0
            else:
                gap = abs(d - b)
                occ += 1.0 if gap == 0 else smoothstep01(range_radius / gap)
    return 1.0 - occ / len(kernel)  # @line L7


def box_blur(A: Grid, r: int) -> Grid:
    """A (2r+1) by (2r+1) box filter, clamped at the borders."""
    h, w = len(A), len(A[0])
    out = []
    for j in range(h):
        row = []
        for i in range(w):
            acc, cnt = 0.0, 0
            for jj in range(max(0, j - r), min(h, j + r + 1)):
                for ii in range(max(0, i - r), min(w, i + r + 1)):
                    acc += A[jj][ii]
                    cnt += 1
            row.append(acc / cnt)
        out.append(row)
    return out


def ssao(D: Grid, kernel: Sequence[Vec], oriented: bool, blur: int = 0, **kw) -> Grid:
    A = [[ssao_pixel(D, i, j, kernel, oriented, **kw) for i in range(len(D[0]))] for j in range(len(D))]
    return box_blur(A, blur) if blur > 0 else A  # @line L8


def half_ball_beyond(delta: float, radius: float) -> float:
    """The fraction of the half ball of the given radius with x > delta, for
    0 <= delta <= radius: the occluded fraction next to an infinite wall at
    distance delta that is higher than the radius."""
    return (radius - delta) ** 2 * (2 * radius + delta) / (4 * radius ** 3)
