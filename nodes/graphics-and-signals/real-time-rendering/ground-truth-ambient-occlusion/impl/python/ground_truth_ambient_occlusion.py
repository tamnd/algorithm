# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ground-truth-ambient-occlusion/. The authors are listed in prov/2H8H92.jsonl.

"""Ground-truth ambient occlusion: horizons per slice and a closed-form
cosine-weighted inner integral.

The camera is orthographic and looks along -z, so the view vector is
v = (0, 0, 1) everywhere and the tests can use height fields. The pixel (i, j)
has its center at (i + 1/2, j + 1/2) in view units, D[j][i] is the positive
view depth, and the point of a pixel is (x, y, -d).

A slice is the plane through v and a screen direction (cos phi, sin phi, 0).
Angles h in a slice are measured from v, positive toward the screen
direction. The two horizons h1 <= 0 <= h2 are found by marching the depth
buffer both ways and clamped to the hemisphere of the normal. The visibility is

    A = (1 / pi) integral over phi in [0, pi) of |n_p| a(phi) dphi,
    a = integral from h1 to h2 of cos(h - gamma) |sin h| dh,

where n_p is the normal projected into the slice and gamma its angle from v.
The inner integral has the closed form of inner_integral().
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


def inner_integral(h1: float, h2: float, gamma: float) -> float:
    """The integral of cos(h - gamma) |sin h| over [h1, h2], for h1 <= 0 <= h2."""
    a = 0.25 * (-math.cos(2 * h1 - gamma) + math.cos(gamma) + 2 * h1 * math.sin(gamma))
    b = 0.25 * (-math.cos(2 * h2 - gamma) + math.cos(gamma) + 2 * h2 * math.sin(gamma))
    return a + b


def _max_cos(D, px, py, d, cx, cy, steps, step, radius, start, mode):
    """The largest cosine to v of the samples on one side, starting at the
    cosine of the clamped tangent horizon."""
    best = start
    for s in range(1, steps + 1):
        r = s * step
        dz = d - lookup(D, px + r * cx, py + r * cy, mode)
        dist = math.hypot(r, dz)
        if dist > radius:
            continue
        best = max(best, dz / dist)
    return best


def gtao_pixel(
    D: Grid,
    i: int,
    j: int,
    slices: int,
    steps: int,
    step: float,
    radius: float,
    jitter: float = 0.0,
    normal: Optional[Vec] = None,
    mode: str = "nearest",
) -> float:
    d = D[j][i]
    px, py = i + 0.5, j + 0.5
    n = normal if normal is not None else normal_from_depth(D, i, j)
    acc = 0.0  # @line L1
    for k in range(slices):  # @line L2
        phi = math.pi * (k + jitter) / slices
        cx, cy = math.cos(phi), math.sin(phi)
        n_dir = n[0] * cx + n[1] * cy  # @line L3
        n_v = n[2]
        length = math.hypot(n_dir, n_v)
        gamma = math.atan2(n_dir, n_v)
        # The tangent horizons gamma -/+ pi/2 have the cosines sin(gamma) and -sin(gamma).
        c2 = _max_cos(D, px, py, d, cx, cy, steps, step, radius, -math.sin(gamma), mode)  # @line L4
        c1 = _max_cos(D, px, py, d, -cx, -cy, steps, step, radius, math.sin(gamma), mode)  # @line L5
        h1 = -math.acos(min(1.0, c1))  # @line L6
        h2 = math.acos(min(1.0, c2))
        acc += length * inner_integral(h1, h2, gamma)  # @line L7
    return acc / slices  # @line L8


def gtao(D: Grid, slices: int, steps: int, step: float, radius: float, **kw) -> Grid:
    return [[gtao_pixel(D, i, j, slices, steps, step, radius, **kw) for i in range(len(D[0]))] for j in range(len(D))]


def wall_reference(delta: float, height: float) -> float:
    """The cosine-weighted visibility of a point on a frontal floor at the
    distance delta from an infinite wall of the given height, with no radius
    limit: (1 + delta / sqrt(delta^2 + height^2)) / 2."""
    return 0.5 * (1.0 + delta / math.hypot(delta, height))
