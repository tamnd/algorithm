# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hit-or-miss-transform/. The authors are listed in prov/TADBZ8.jsonl.

"""The hit-or-miss transform of a binary image by a pair of disjoint elements.

An image is a list of H rows of W values 0 or 1, X[y][x], with y growing
downward. B1 (the hit set) and B2 (the miss set) are disjoint lists of integer
offsets (u, v). The transform keeps the pixels p such that p + b is foreground
for every b in B1 and background for every b in B2:

    HMT(X; B1, B2) = (X eroded by B1) intersected with (complement of X eroded by B2).

A pixel outside the image has the value `outside`, 0 (background) by default.
The cost is O(W H (|B1| + |B2|)) time and O(W H) extra space.
"""

from typing import List, Sequence, Tuple

Image = List[List[int]]
Offset = Tuple[int, int]


def hit_or_miss(x: Sequence[Sequence[int]], hit: Sequence[Offset], miss: Sequence[Offset],
                outside: int = 0) -> Image:
    """Return the hit-or-miss transform of the binary image x."""
    if set(hit) & set(miss):
        raise ValueError("the hit and miss elements must be disjoint")
    height = len(x)
    width = len(x[0]) if height else 0
    r = [[1] * width for _ in range(height)]  # @line L1
    for (u, v) in hit:  # @line L2
        for y in range(height):
            for xx in range(width):  # @line L3
                qx, qy = xx + u, y + v
                t = x[qy][qx] if 0 <= qx < width and 0 <= qy < height else outside
                if t == 0:
                    r[y][xx] = 0
    for (u, v) in miss:  # @line L4
        for y in range(height):
            for xx in range(width):  # @line L5
                qx, qy = xx + u, y + v
                t = x[qy][qx] if 0 <= qx < width and 0 <= qy < height else outside
                if t == 1:
                    r[y][xx] = 0
    return r  # @line L6


def from_template(rows: Sequence[str]) -> Tuple[List[Offset], List[Offset]]:
    """Read a template with an odd number of rows and columns, centered on the origin.

    '1' is a hit pixel, '0' a miss pixel and '.' a pixel that does not matter.
    """
    h, w = len(rows), len(rows[0])
    cy, cx = h // 2, w // 2
    hit, miss = [], []
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c == "1":
                hit.append((x - cx, y - cy))
            elif c == "0":
                miss.append((x - cx, y - cy))
    return hit, miss


def rotate(se: Sequence[Offset]) -> List[Offset]:
    """Rotate the offsets by a quarter turn: (u, v) becomes (-v, u)."""
    return [(-v, u) for (u, v) in se]
