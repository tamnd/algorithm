# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/z-buffer/. The authors are listed in prov/QPWQ6K.jsonl.

"""The z-buffer algorithm (Catmull 1974) on screen-space triangles.

A triangle is ((x0, y0, z0), (x1, y1, z1), (x2, y2, z2)). The coordinates
x and y are in pixels, with x to the right and y down. The pixel (i, j)
has its center at (i + 1/2, j + 1/2). The depth z is affine in x and y, as
the depth after a perspective divide is, and a smaller z is nearer.
Use int or Fraction coordinates: then every decision is exact.
"""

from fractions import Fraction
from math import ceil, floor
from typing import Sequence

Number = int | Fraction
Vertex = tuple[Number, Number, Number]
Triangle = tuple[Vertex, Vertex, Vertex]

HALF = Fraction(1, 2)


def edge(ax: Number, ay: Number, bx: Number, by: Number, px: Number, py: Number) -> Number:
    """Twice the signed area of (a, b, p). It is positive when p is on the inner side."""
    return (bx - ax) * (py - ay) - (by - ay) * (px - ax)


def is_top_left(ax: Number, ay: Number, bx: Number, by: Number) -> bool:
    """For a triangle with a positive edge function inside, the edge a -> b is a
    top edge (dy = 0, dx > 0) or a left edge (dy < 0) in y-down coordinates."""
    dx, dy = bx - ax, by - ay
    return dy < 0 or (dy == 0 and dx > 0)


def covered_pixels(tri: Triangle, width: int, height: int):
    """Yield (i, j, z) for each pixel center covered by tri under the top-left
    rule, with z the depth of the triangle plane at the center. Rows are visited
    with incremental edge functions, as a hardware rasterizer does."""
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = tri
    area = edge(x0, y0, x1, y1, x2, y2)
    if area == 0:
        return
    if area < 0:  # make the inside positive
        x1, y1, z1, x2, y2, z2 = x2, y2, z2, x1, y1, z1
        area = -area
    edges = ((x1, y1, x2, y2), (x2, y2, x0, y0), (x0, y0, x1, y1))
    tl = [is_top_left(*e) for e in edges]
    i_lo = max(0, ceil(min(x0, x1, x2) - HALF))
    i_hi = min(width - 1, floor(max(x0, x1, x2) - HALF))
    j_lo = max(0, ceil(min(y0, y1, y2) - HALF))
    j_hi = min(height - 1, floor(max(y0, y1, y2) - HALF))
    if i_lo > i_hi:
        return
    # E(p + (1, 0)) - E(p) = -(by - ay) for an edge a -> b.
    step = [-(e[3] - e[1]) for e in edges]
    for j in range(j_lo, j_hi + 1):
        px, py = i_lo + HALF, j + HALF
        w = [edge(*e, px, py) for e in edges]
        for i in range(i_lo, i_hi + 1):
            if all(w[k] > 0 or (w[k] == 0 and tl[k]) for k in range(3)):
                z = (w[0] * z0 + w[1] * z1 + w[2] * z2) / Fraction(area)
                yield i, j, z
            for k in range(3):
                w[k] += step[k]


def z_buffer(width: int, height: int, triangles: Sequence[Triangle],
             colors: Sequence[object], background: object = None):
    """Return (color, depth), two height x width grids. depth[j][i] is None
    where no triangle covers the pixel center. A fragment replaces the stored
    one only if it is strictly nearer, so of two equal depths the earlier
    triangle stays."""
    depth: list[list[Fraction | None]] = [[None] * width for _ in range(height)]  # @line L1
    color = [[background] * width for _ in range(height)]
    for k, tri in enumerate(triangles):  # @line L2
        for i, j, z in covered_pixels(tri, width, height):  # @line L3
            d = depth[j][i]  # @line L4: z is the plane depth at the center
            if d is None or z < d:  # @line L5
                depth[j][i] = z  # @line L6
                color[j][i] = colors[k]
    return color, depth  # @line L7
