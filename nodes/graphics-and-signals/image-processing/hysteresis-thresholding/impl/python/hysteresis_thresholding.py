# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hysteresis-thresholding/. The authors are listed in prov/97HN4Z.jsonl.

"""Hysteresis thresholding with two thresholds and 8-connectivity.

The input is an image of edge strengths (a list of rows of numbers), with
pixel (x, y) at [y][x]. A pixel is strong when its value is at least high,
and a candidate when its value is at least low. The output marks with True
each candidate that an 8-connected path of candidates joins to a strong pixel.
"""

Grid = list[list[float]]
NEIGHBORS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))


def hysteresis_threshold(strength: Grid, low: float, high: float) -> list[list[bool]]:
    """Return the edge mask. Requires low <= high."""
    if low > high:
        raise ValueError("low must not exceed high")
    h = len(strength)
    w = len(strength[0]) if h else 0
    edge = [[False] * w for _ in range(h)]
    stack: list[tuple[int, int]] = []
    for y in range(h):  # @line L1
        for x in range(w):
            if strength[y][x] >= high:  # @line L2
                edge[y][x] = True
                stack.append((x, y))
    while stack:  # @line L3
        x, y = stack.pop()  # @line L4
        for dx, dy in NEIGHBORS:  # @line L5
            xx, yy = x + dx, y + dy
            if 0 <= xx < w and 0 <= yy < h and not edge[yy][xx] and strength[yy][xx] >= low:  # @line L6
                edge[yy][xx] = True  # @line L7
                stack.append((xx, yy))
    return edge  # @line L8
