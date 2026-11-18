# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horizon-based-ambient-occlusion/. The authors are listed in prov/7TY98V.jsonl.

"""Horizon-based ambient occlusion (Bavoil, Sainz and Dimitrov 2008).

The camera is orthographic and looks along -z, so that the view vector is
(0, 0, 1) at every pixel and the tests can use height fields. The pixel (i, j)
has its center at (i + 1/2, j + 1/2) in view units, D[j][i] is the positive
view depth, and the point of a pixel is (x, y, -d). Elevation angles are
measured from the view plane z = const, positive toward the camera.

For each screen direction theta, the method marches the depth buffer, keeps
the highest elevation seen so far (the horizon), and adds W(r) (sin h - sin h')
each time the horizon rises from h' to h, starting at the tangent angle t.
With W = 1 the sum of one direction is sin h - sin t. The result is
A = 1 - (1 / N_d) sum over directions, the visibility (1 = open).
"""

import math
from typing import List, Optional, Tuple

Vec = Tuple[float, float, float]
Grid = List[List[float]]


def lookup(D: Grid, x: float, y: float, mode: str = "nearest") -> float:
    h, w = len(D), len(D[0])
    if mode == "nearest":
        i = min(max(int(math.floor(x)), 0), w - 1)
        j = min(max(int(math.floor(y)), 0), h - 1)
        return D[j][i]
    u = min(max(x - 0.5, 0.0), w - 1.0)
    v = min(max(y - 0.5, 0.0), h - 1.0)
    i0, j0 = min(int(u), w - 2), min(int(v), h - 2)
    fu, fv = u - i0, v - j0
    top = D[j0][i0] * (1 - fu) + D[j0][i0 + 1] * fu
    bot = D[j0 + 1][i0] * (1 - fu) + D[j0 + 1][i0 + 1] * fu
    return top * (1 - fv) + bot * fv


def normal_from_depth(D: Grid, i: int, j: int) -> Vec:
    h, w = len(D), len(D[0])
    il, ir = max(i - 1, 0), min(i + 1, w - 1)
    jb, jt = max(j - 1, 0), min(j + 1, h - 1)
    gx = (D[j][ir] - D[j][il]) / (ir - il)
    gy = (D[jt][i] - D[jb][i]) / (jt - jb)
    s = math.sqrt(gx * gx + gy * gy + 1.0)
    return (gx / s, gy / s, 1.0 / s)


def tangent_angle(n: Vec, cx: float, cy: float) -> float:
    """The elevation of the tangent plane of n in the screen direction (cx, cy)."""
    return math.atan(-(n[0] * cx + n[1] * cy) / n[2])


def hbao_pixel(
    D: Grid,
    i: int,
    j: int,
    directions: int,
    steps: int,
    step: float,
    radius: float,
    falloff: bool = True,
    jitter: float = 0.0,
    normal: Optional[Vec] = None,
    mode: str = "nearest",
) -> float:
    d = D[j][i]
    px, py = i + 0.5, j + 0.5
    n = normal if normal is not None else normal_from_depth(D, i, j)
    occ = 0.0  # @line L1
    for k in range(directions):  # @line L2
        theta = 2 * math.pi * (k + jitter) / directions
        cx, cy = math.cos(theta), math.sin(theta)
        h = tangent_angle(n, cx, cy)  # @line L3
        sin_h = math.sin(h)
        for s in range(1, steps + 1):  # @line L4
            r = s * step
            dz = d - lookup(D, px + r * cx, py + r * cy, mode)
            dist2 = r * r + dz * dz  # @line L5
            if dist2 > radius * radius:
                continue
            a = math.atan2(dz, r)  # @line L6
            if a > h:  # @line L7
                w = 1.0 - dist2 / (radius * radius) if falloff else 1.0
                sin_a = math.sin(a)
                occ += w * (sin_a - sin_h)
                h, sin_h = a, sin_a
    return 1.0 - occ / directions  # @line L8


def hbao(D: Grid, directions: int, steps: int, step: float, radius: float, **kw) -> Grid:
    return [[hbao_pixel(D, i, j, directions, steps, step, radius, **kw) for i in range(len(D[0]))] for j in range(len(D))]


def wall_reference(delta: float, height: float) -> float:
    """The HBAO value with W = 1 and no radius limit for a point on a frontal
    floor at the distance delta from an infinite wall of the given height:
    1 - atan(height / delta) / pi, the open share of the solid angle."""
    return 1.0 - math.atan2(height, delta) / math.pi
