# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morphological-opening/. The authors are listed in prov/97EJK2.jsonl.

"""Morphological opening of a binary or gray image by a flat structuring element.

An image is a list of H rows of W integers, f[y][x]. A structuring element is a
list of integer offsets (u, v). The opening is the erosion followed by the
dilation with the same element:

    e(p) = min over b in B with p + b inside of f(p + b)    (top if there is none)
    g(p) = max over b in B with p - b inside of e(p - b)    (0 if there is none)

Both steps ignore the pixels outside the image. The result is the union (for a
binary image) or the maximum (for a gray image) of the translates of B, cut to
the image, that fit under f. It costs O(W H |B|) time and O(W H) extra space.
"""

from typing import List, Sequence, Tuple

Image = List[List[int]]
Offset = Tuple[int, int]


def open_image(f: Sequence[Sequence[int]], se: Sequence[Offset], top: int = 1) -> Image:
    """Open f by the flat element se. Every value of f must lie in 0..top."""
    height = len(f)
    width = len(f[0]) if height else 0
    e = [[top] * width for _ in range(height)]  # @line L1
    for (u, v) in se:  # @line L2
        for y in range(height):
            yy = y + v
            if not 0 <= yy < height:
                continue
            for x in range(width):  # @line L3
                xx = x + u
                if 0 <= xx < width and f[yy][xx] < e[y][x]:
                    e[y][x] = f[yy][xx]
    g = [[0] * width for _ in range(height)]  # @line L4
    for (u, v) in se:  # @line L5
        for y in range(height):
            yy = y - v
            if not 0 <= yy < height:
                continue
            for x in range(width):  # @line L6
                xx = x - u
                if 0 <= xx < width and e[yy][xx] > g[y][x]:
                    g[y][x] = e[yy][xx]
    return g  # @line L7


def rectangle(x0: int, x1: int, y0: int, y1: int) -> List[Offset]:
    """All offsets (u, v) with x0 <= u <= x1 and y0 <= v <= y1."""
    return [(u, v) for v in range(y0, y1 + 1) for u in range(x0, x1 + 1)]
