# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/painters-algorithm/. The authors are listed in prov/5FR13Q.jsonl.

"""The painter's algorithm (depth sort) in screen space.

The scene is a list of planar convex polygons. Each polygon is a list of
vertices (x, y, z) with int or Fraction coordinates, in screen space: the
viewer looks down the z axis from z = +infinity, so a larger z is nearer.
The image has `width` by `height` pixels, and pixel (i, j) is the point
sample at the center (i + 1/2, j + 1/2). A pixel is covered by a polygon
when its center lies in the closed projection of the polygon onto the
xy plane. All tests are exact.
"""

from fractions import Fraction
from typing import Sequence, Union

Num = Union[int, Fraction]
Vertex = tuple[Num, Num, Num]
Polygon = Sequence[Vertex]


def covers(poly: Polygon, x: Num, y: Num) -> bool:
    """True when (x, y) lies in the closed projection of the convex polygon.

    The projection must have nonzero area. The vertices may be in either
    orientation. Cost O(k) for k vertices.
    """
    pos = neg = False
    k = len(poly)
    for a in range(k):
        ax, ay = poly[a][0], poly[a][1]
        bx, by = poly[(a + 1) % k][0], poly[(a + 1) % k][1]
        c = (bx - ax) * (y - ay) - (by - ay) * (x - ax)
        if c > 0:
            pos = True
        elif c < 0:
            neg = True
        if pos and neg:
            return False
    return True


def depth_at(poly: Polygon, x: Num, y: Num) -> Fraction:
    """The z of the plane of the polygon above the point (x, y), exactly."""
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = poly[0], poly[1], poly[2]
    ux, uy, uz = bx - ax, by - ay, bz - az
    vx, vy, vz = cx - ax, cy - ay, cz - az
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    return Fraction(az) - Fraction(nx * (x - ax) + ny * (y - ay), nz)


def painters_algorithm(polygons: Sequence[Polygon], width: int, height: int,
                       background: int = -1) -> list[list[int]]:
    """Paint the polygons farthest first and return the image of indices.

    image[j][i] is the index of the polygon painted last at pixel (i, j),
    or `background`. The sort key of a polygon is the z of its farthest
    vertex. The result is the visible polygon at each pixel when the
    order is a valid visibility order, for example when the z ranges of
    the polygons do not overlap; otherwise it can be wrong.

    Cost: O(n log n) for the sort plus O(W H k) per polygon here, because
    the coverage test runs at each pixel (a scan converter visits only the
    covered pixels).
    """
    n = len(polygons)
    key = [min(v[2] for v in polygons[p]) for p in range(n)]  # @line L1
    order = sorted(range(n), key=lambda p: key[p])  # @line L2
    image = [[background] * width for _ in range(height)]  # @line L3
    for p in order:  # @line L4
        for j in range(height):
            for i in range(width):
                if covers(polygons[p], Fraction(2 * i + 1, 2), Fraction(2 * j + 1, 2)):  # @line L5
                    image[j][i] = p  # @line L6
    return image  # @line L7
