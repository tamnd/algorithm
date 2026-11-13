# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morphological-erosion/. The authors are listed in prov/8EKNQA.jsonl.

"""Morphological erosion of a binary or gray image by a flat structuring element.

An image is a list of H rows of W integers, f[y][x], with the pixel centers at
integer coordinates. A binary image holds 0 (background) and 1 (foreground).
A structuring element is a list of integer offsets (u, v); the origin is (0, 0).

The erosion is g(x, y) = min over (u, v) in B of f(x + u, y + v). A pixel
outside the image takes the value `outside`; the default None means "ignore the
outside", which is the same as giving it the top value, so that the border does
not shrink the result. The method takes the minimum of the translates of the
image, one offset at a time: O(W H |B|) time and O(W H) extra space.
"""

from typing import List, Optional, Sequence, Tuple

Image = List[List[int]]
Offset = Tuple[int, int]


def reflect(se: Sequence[Offset]) -> List[Offset]:
    """The reflected element: each offset (u, v) becomes (-u, -v)."""
    return [(-u, -v) for (u, v) in se]


def erode(f: Sequence[Sequence[int]], se: Sequence[Offset],
          outside: Optional[int] = None, top: int = 1) -> Image:
    """Erode f by the flat element se.

    Precondition: every value of f is at most top (use top=1 for a binary
    image and top=255 for an 8-bit gray image). With outside=None, a pixel
    outside the image counts as top.
    """
    height = len(f)
    width = len(f[0]) if height else 0
    o = top if outside is None else outside
    g = [[top] * width for _ in range(height)]  # @line L1
    for (u, v) in se:  # @line L2
        for y in range(height):  # @line L3
            row = g[y]
            yy = y + v
            for x in range(width):  # @line L4
                xx = x + u
                if 0 <= xx < width and 0 <= yy < height:  # @line L5
                    t = f[yy][xx]
                else:
                    t = o  # @line L6
                if t < row[x]:  # @line L7
                    row[x] = t
    return g  # @line L8


def erode_by_parts(f: Sequence[Sequence[int]], parts: Sequence[Sequence[Offset]],
                   outside: Optional[int] = None, top: int = 1) -> Image:
    """Erode by each part in turn: f eroded by A + B equals (f eroded by A) eroded by B.

    On a finite image this equals the erosion by the Minkowski sum of the parts
    when the sum is a rectangle and the parts are its horizontal and vertical
    segments, because the image and the element are then products of intervals.
    """
    g = [list(row) for row in f]
    for part in parts:
        g = erode(g, part, outside, top)
    return g


def rectangle(x0: int, x1: int, y0: int, y1: int) -> List[Offset]:
    """All offsets (u, v) with x0 <= u <= x1 and y0 <= v <= y1."""
    return [(u, v) for v in range(y0, y1 + 1) for u in range(x0, x1 + 1)]
