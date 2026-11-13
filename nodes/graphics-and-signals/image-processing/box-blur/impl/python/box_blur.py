# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/box-blur/. The authors are listed in prov/ES8PJ7.jsonl.

"""Box blur by running sums: the mean over a (2r+1) x (2r+1) window at each pixel.

An image is a list of H rows of W numbers, image[y][x], with the pixel centers
at integer coordinates. A pixel outside the image takes its value from the
border rule: "clamp" (repeat the edge pixel), "mirror" (reflect about the edge,
with the edge pixel repeated), "wrap" (periodic) or "zero". The work is
O(WH + (W + H) r) additions for any radius r, against O(WH r^2) for the direct
sum. Integer or Fraction input gives exact sums and exact Fraction means.
"""

from fractions import Fraction
from typing import List, Optional, Sequence, Union

Num = Union[int, float, Fraction]
Image = List[List[Num]]
BORDERS = ("clamp", "mirror", "wrap", "zero")


def border_index(i: int, n: int, border: str) -> Optional[int]:
    """Map an index i of an axis of length n to an index in 0..n-1, or None for zero."""
    if 0 <= i < n:
        return i
    if border == "clamp":
        return 0 if i < 0 else n - 1
    if border == "wrap":
        return i % n
    if border == "mirror":
        m = i % (2 * n)
        return m if m < n else 2 * n - 1 - m
    if border == "zero":
        return None
    raise ValueError(f"unknown border rule {border!r}")


def box_sum(image: Sequence[Sequence[Num]], r: int, border: str = "clamp") -> Image:
    """Return the window sums h[y][x] = sum of the extended image over |u|, |v| <= r.

    Precondition: r >= 0 and all rows have the same length.
    Cost: O(WH + (W + H) r) additions and O(WH) extra space.
    """
    if r < 0:
        raise ValueError("the radius must be at least 0")
    height = len(image)
    width = len(image[0]) if height else 0
    if height == 0 or width == 0:
        return []

    def row_at(y: int, i: int) -> Num:
        j = border_index(i, width, border)
        return 0 if j is None else image[y][j]

    g: Image = [[0] * width for _ in range(height)]
    for y in range(height):  # @line L1
        s = sum(row_at(y, u) for u in range(-r, r + 1))  # @line L2
        g[y][0] = s  # @line L3
        for x in range(1, width):  # @line L4
            s = s + row_at(y, x + r) - row_at(y, x - r - 1)  # @line L5
            g[y][x] = s  # @line L6

    def col_at(x: int, i: int) -> Num:
        j = border_index(i, height, border)
        return 0 if j is None else g[j][x]

    h: Image = [[0] * width for _ in range(height)]
    for x in range(width):  # @line L7
        s = sum(col_at(x, v) for v in range(-r, r + 1))  # @line L8
        h[0][x] = s  # @line L9
        for y in range(1, height):  # @line L10
            s = s + col_at(x, y + r) - col_at(x, y - r - 1)  # @line L11
            h[y][x] = s  # @line L12
    return h


def box_blur(image: Sequence[Sequence[Num]], r: int, border: str = "clamp") -> Image:
    """Return the box blur: each window sum divided by (2r+1)^2.

    Integer and Fraction pixels give Fraction means; float pixels give floats.
    Cost: O(WH + (W + H) r) time and O(WH) extra space.
    """
    n = (2 * r + 1) ** 2
    sums = box_sum(image, r, border)
    return [[v / n if isinstance(v, float) else Fraction(v) / n for v in row] for row in sums]  # @line L13
