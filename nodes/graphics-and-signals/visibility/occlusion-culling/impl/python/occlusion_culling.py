# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/occlusion-culling/. The authors are listed in prov/J4XCZM.jsonl.

"""Occlusion culling with a depth buffer and bounding-box tests.

The view is orthographic along the z axis, and a larger z is nearer to the
viewer. Pixel (i, j) is a point sample at its center (i + 1/2, j + 1/2). An
object is a list of triangles ((x, y, z), (x, y, z), (x, y, z)) with int or
Fraction coordinates, none of them seen edge on. The objects are taken from
near to far by the nearest z of their bounding boxes. Before an object is
drawn, its box is tested against the depth buffer: if every pixel center in
the projection of the box already holds a depth strictly nearer than the
nearest point of the box, the object is hidden and is skipped.
"""

from fractions import Fraction
from math import ceil, floor
from typing import Optional, Sequence

NEG_INF = None  # the depth of an empty pixel; it is farther than each real depth


def bounding_box(obj):
    pts = [p for tri in obj for p in tri]
    lo = tuple(min(p[k] for p in pts) for k in range(3))
    hi = tuple(max(p[k] for p in pts) for k in range(3))
    return lo, hi


def pixel_range(lo, hi, size):
    """The indices i with lo <= i + 1/2 <= hi and 0 <= i < size."""
    a = max(0, ceil(Fraction(lo) - Fraction(1, 2)))
    b = min(size - 1, floor(Fraction(hi) - Fraction(1, 2)))
    return range(a, b + 1)


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def covers(tri, c) -> bool:
    """Is the point c in the closed projection of the triangle onto the xy plane?"""
    a, b, d = tri
    s = orient(a, b, d)
    o1, o2, o3 = orient(a, b, c), orient(b, d, c), orient(d, a, c)
    return (o1 >= 0 and o2 >= 0 and o3 >= 0) if s > 0 else (o1 <= 0 and o2 <= 0 and o3 <= 0)


def depth_at(tri, c) -> Fraction:
    """The z of the plane of the triangle above the point c, by barycentric weights."""
    a, b, d = tri
    s = orient(a, b, d)
    wa, wb, wd = Fraction(orient(b, d, c), s), Fraction(orient(d, a, c), s), Fraction(orient(a, b, c), s)
    return wa * a[2] + wb * b[2] + wd * d[2]


def nearer(z, old) -> bool:
    return old is NEG_INF or z > old


def occlusion_cull(objects: Sequence, width: int, height: int):
    """Return (drawn, image, depth): the indices of the drawn objects, and the final buffers.

    The image holds an object index or None. The result is the image of a full
    z-buffer that draws the objects in the same order.
    """
    depth: list[list[Optional[Fraction]]] = [[NEG_INF] * width for _ in range(height)]  # @line L1
    image: list[list[Optional[int]]] = [[None] * width for _ in range(height)]
    drawn: list[int] = []
    boxes = [bounding_box(o) for o in objects]
    order = sorted(range(len(objects)), key=lambda k: (-boxes[k][1][2], k))  # @line L2
    for k in order:  # @line L3
        lo, hi = boxes[k]
        rows, cols = pixel_range(lo[1], hi[1], height), pixel_range(lo[0], hi[0], width)  # @line L4
        hidden = True
        for j in rows:  # @line L5
            for i in cols:
                if not (depth[j][i] is not NEG_INF and depth[j][i] > hi[2]):
                    hidden = False
                    break
            if not hidden:
                break
        if hidden:
            continue  # @line L6
        for tri in objects[k]:  # @line L7
            tl, th = bounding_box([tri])
            for j in pixel_range(tl[1], th[1], height):
                for i in pixel_range(tl[0], th[0], width):
                    c = (Fraction(2 * i + 1, 2), Fraction(2 * j + 1, 2))
                    if covers(tri, c):
                        z = depth_at(tri, c)
                        if nearer(z, depth[j][i]):  # @line L8
                            depth[j][i], image[j][i] = z, k
        drawn.append(k)  # @line L9
    return drawn, image, depth  # @line L10
