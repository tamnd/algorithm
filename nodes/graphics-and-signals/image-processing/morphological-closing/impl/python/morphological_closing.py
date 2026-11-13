# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morphological-closing/. The authors are listed in prov/V188PY.jsonl.

"""Morphological closing of a binary or gray image by a flat structuring element.

An image is a list of H rows of W integers, f[y][x]. A structuring element is a
list of integer offsets (u, v). The closing is the dilation followed by the
erosion with the same element:

    d(p) = max over b in B with p - b inside of f(p - b)    (0 if there is none)
    g(p) = min over b in B with p + b inside of d(p + b)    (top if there is none)

Both steps ignore the pixels outside the image. The closing of f is the
complement of the opening of the complement of f by the reflected element.
It costs O(W H |B|) time and O(W H) extra space.
"""

from typing import List, Sequence, Tuple

Image = List[List[int]]
Offset = Tuple[int, int]


def close_image(f: Sequence[Sequence[int]], se: Sequence[Offset], top: int = 1) -> Image:
    """Close f by the flat element se. Every value of f must lie in 0..top."""
    height = len(f)
    width = len(f[0]) if height else 0
    d = [[0] * width for _ in range(height)]  # @line L1
    for (u, v) in se:  # @line L2
        for y in range(height):
            yy = y - v
            if not 0 <= yy < height:
                continue
            for x in range(width):  # @line L3
                xx = x - u
                if 0 <= xx < width and f[yy][xx] > d[y][x]:
                    d[y][x] = f[yy][xx]
    g = [[top] * width for _ in range(height)]  # @line L4
    for (u, v) in se:  # @line L5
        for y in range(height):
            yy = y + v
            if not 0 <= yy < height:
                continue
            for x in range(width):  # @line L6
                xx = x + u
                if 0 <= xx < width and d[yy][xx] < g[y][x]:
                    g[y][x] = d[yy][xx]
    return g  # @line L7


def reflect(se: Sequence[Offset]) -> List[Offset]:
    """The reflected element: each offset (u, v) becomes (-u, -v)."""
    return [(-u, -v) for (u, v) in se]


def rectangle(x0: int, x1: int, y0: int, y1: int) -> List[Offset]:
    """All offsets (u, v) with x0 <= u <= x1 and y0 <= v <= y1."""
    return [(u, v) for v in range(y0, y1 + 1) for u in range(x0, x1 + 1)]
