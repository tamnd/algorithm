# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morphological-dilation/. The authors are listed in prov/GK4YJV.jsonl.

"""Morphological dilation of a binary or gray image by a flat structuring element.

An image is a list of H rows of W integers, f[y][x], with the pixel centers at
integer coordinates. A binary image holds 0 (background) and 1 (foreground).
A structuring element is a list of integer offsets (u, v); the origin is (0, 0).

The dilation is g(x, y) = max over (u, v) in B of f(x - u, y - v). For a binary
image this is the Minkowski sum: the set of all p + b with p in the foreground
and b in B. A pixel outside the image takes the value `outside`; the default
None means "ignore the outside", which is the same as giving it the bottom
value 0. The method takes the maximum of the translates of the image, one
offset at a time: O(W H |B|) time and O(W H) extra space.
"""

from typing import List, Optional, Sequence, Tuple

Image = List[List[int]]
Offset = Tuple[int, int]


def reflect(se: Sequence[Offset]) -> List[Offset]:
    """The reflected element: each offset (u, v) becomes (-u, -v)."""
    return [(-u, -v) for (u, v) in se]


def dilate(f: Sequence[Sequence[int]], se: Sequence[Offset],
           outside: Optional[int] = None, bottom: int = 0) -> Image:
    """Dilate f by the flat element se.

    Precondition: every value of f is at least bottom. With outside=None, a
    pixel outside the image counts as bottom.
    """
    height = len(f)
    width = len(f[0]) if height else 0
    o = bottom if outside is None else outside
    g = [[bottom] * width for _ in range(height)]  # @line L1
    for (u, v) in se:  # @line L2
        for y in range(height):  # @line L3
            row = g[y]
            yy = y - v
            for x in range(width):  # @line L4
                xx = x - u
                if 0 <= xx < width and 0 <= yy < height:  # @line L5
                    t = f[yy][xx]
                else:
                    t = o  # @line L6
                if t > row[x]:  # @line L7
                    row[x] = t
    return g  # @line L8


def rectangle(x0: int, x1: int, y0: int, y1: int) -> List[Offset]:
    """All offsets (u, v) with x0 <= u <= x1 and y0 <= v <= y1."""
    return [(u, v) for v in range(y0, y1 + 1) for u in range(x0, x1 + 1)]
