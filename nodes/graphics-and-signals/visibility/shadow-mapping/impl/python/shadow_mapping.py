# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shadow-mapping/. The authors are listed in prov/4VKYK3.jsonl.

"""Shadow mapping (Williams 1978) with percentage-closer filtering
(Reeves, Salesin and Cook 1987).

The light transform m is a 4 x 4 matrix (rows) that takes a world point
(x, y, z, 1) to light clip space; after the divide by w, x and y are texel
units of the map, x to the right, y down, and z is the light depth, smaller
nearer. Texel (i, j) has its center at (i + 1/2, j + 1/2). An orthographic
light has last row (0, 0, 0, 1). Precondition: w > 0 at every vertex and every
query point, so no clipping is needed. With Fraction or int input every
decision is exact.
"""

from fractions import Fraction
from math import ceil, floor

HALF = Fraction(1, 2)
FAR = float("inf")


def to_light(m, p):
    """Return (x, y, z) of the world point p in light space."""
    x, y, z = p
    h = [m[r][0] * x + m[r][1] * y + m[r][2] * z + m[r][3] for r in range(4)]
    if h[3] <= 0:
        raise ValueError("the point is not in front of the light")
    return tuple(Fraction(h[r]) / h[3] for r in range(3))


def _edge(ax, ay, bx, by, px, py):
    return (bx - ax) * (py - ay) - (by - ay) * (px - ax)


def _top_left(ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    return dy < 0 or (dy == 0 and dx > 0)


def _fragments(tri, width, height):
    """Yield (i, j, z) for each texel center the triangle covers (top-left rule)."""
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = tri
    area = _edge(x0, y0, x1, y1, x2, y2)
    if area == 0:
        return
    if area < 0:
        x1, y1, z1, x2, y2, z2 = x2, y2, z2, x1, y1, z1
        area = -area
    edges = ((x1, y1, x2, y2), (x2, y2, x0, y0), (x0, y0, x1, y1))
    tl = [_top_left(*e) for e in edges]
    for j in range(max(0, ceil(min(y0, y1, y2) - HALF)), min(height - 1, floor(max(y0, y1, y2) - HALF)) + 1):
        for i in range(max(0, ceil(min(x0, x1, x2) - HALF)), min(width - 1, floor(max(x0, x1, x2) - HALF)) + 1):
            w = [_edge(*e, i + HALF, j + HALF) for e in edges]
            if all(w[k] > 0 or (w[k] == 0 and tl[k]) for k in range(3)):
                yield i, j, (w[0] * z0 + w[1] * z1 + w[2] * z2) / area


def shadow_map(width, height, triangles, m):
    """Pass 1: a z-buffer seen from the light. Empty texels hold FAR."""
    smap = [[FAR] * width for _ in range(height)]  # @line L1
    for t in triangles:  # @line L2
        lt = [to_light(m, v) for v in t]  # @line L3
        for i, j, z in _fragments(lt, width, height):  # @line L4
            if z < smap[j][i]:
                smap[j][i] = z
    return smap


def _test(smap, i, j, z, bias):
    """1 if a stored depth is nearer than z - bias at texel (i, j), else 0.
    A texel outside the map counts as lit."""
    if 0 <= j < len(smap) and 0 <= i < len(smap[0]):
        return 1 if z - bias > smap[j][i] else 0  # @line L7
    return 0


def shadowed(smap, m, p, bias=0):
    """Pass 2: is the world point p in shadow?"""
    x, y, z = to_light(m, p)  # @line L5
    i, j = floor(x), floor(y)  # @line L6: the texel that holds (x, y)
    return _test(smap, i, j, z, bias) == 1


def pcf(smap, m, p, bias=0, r=1):
    """Percentage-closer filtering: the fraction of the (2r + 1)^2 texels
    around p whose binary depth test says shadow. Filter the test results,
    not the depths."""
    x, y, z = to_light(m, p)  # @line L8
    i, j = floor(x), floor(y)
    hits = sum(_test(smap, i + di, j + dj, z, bias)  # @line L9
               for dj in range(-r, r + 1) for di in range(-r, r + 1))
    return Fraction(hits, (2 * r + 1) ** 2)  # @line L10
