# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morphological-antialiasing/. The authors are listed in prov/ZVD2J6.jsonl.

"""Morphological antialiasing (MLAA, Reshetov 2009), the black-and-white rules.

An image is H rows of W pixels, image[j][i], each pixel a tuple of channel
values; row j grows downward. Two neighbor pixels are *different* when some
channel differs by more than the threshold. Pixels outside the image repeat the
border pixels, so there is no separation line along the border.

Step 1 finds separation lines: maximal runs of differences along the boundary
between two rows (or two columns). Step 2 looks at the two end vertices of each
line for an orthogonal separation segment on one side: both ends give a Z or a U
shape, which is split in the middle into two L shapes; one end gives one L shape
over the whole line. Step 3 joins the middle of the secondary edge to the far
vertex of the primary edge and blends each cell between this line and the
primary edge with the cell across the primary edge, by the trapezoid area a:
c_new = (1 - a) c_old + a c_opposite, with c_opposite from the input image.
The blends are applied one after the other: all lines between rows, from top to
bottom and left to right, then all lines between columns.
Use fractions.Fraction values for exact results.
"""

from fractions import Fraction
from typing import List, Sequence, Tuple

Pixel = tuple
Image = List[List[Pixel]]
HALF = Fraction(1, 2)


def l_shape_areas(length: Fraction) -> List[Fraction]:
    """Areas of the cells under the line from height 1/2 at x = 0 to height 0 at x = length.

    Cell k covers [k, k + 1]. Precondition: length is a positive multiple of 1/2.
    """
    def h(x):
        return HALF * (1 - x / length)

    areas = []
    k = 0
    while k < length:
        right = min(Fraction(k + 1), length)
        areas.append((h(Fraction(k)) + h(right)) / 2 * (right - k))
        k += 1
    return areas


def _differ(p: Pixel, q: Pixel, threshold) -> bool:
    return any(abs(a - b) > threshold for a, b in zip(p, q))


def _blend(c: Pixel, o: Pixel, a) -> Pixel:
    return tuple((1 - a) * x + a * y for x, y in zip(c, o))


def _process_rows(img: Image, out: Image, threshold) -> None:
    """Find every shape whose primary edge lies between two rows of img and blend it into out."""
    h, w = len(img), len(img[0])

    def vertical_diff(x, y):
        """Is there a separation segment between columns x - 1 and x in row y?"""
        return 0 < x < w and 0 <= y < h and _differ(img[y][x - 1], img[y][x], threshold)

    def secondary(x, y):
        """Side of the orthogonal segment at the vertex (x, y + 1): -1 up, +1 down, 0 none or both."""
        up, down = vertical_diff(x, y), vertical_diff(x, y + 1)
        if up == down:
            return 0
        return -1 if up else 1

    for y in range(h - 1):  # @line L1
        x = 0
        while x < w:
            if not _differ(img[y][x], img[y + 1][x], threshold):
                x += 1
                continue
            a = x
            while x < w and _differ(img[y][x], img[y + 1][x], threshold):
                x += 1
            b = x  # @line L2
            left, right = secondary(a, y), secondary(b, y)  # @line L3
            n = Fraction(b - a)
            spans: List[Tuple[int, int, int, Fraction]] = []  # (start vertex, step, side, length)
            if left and right:  # @line L4
                spans = [(a, 1, left, n / 2), (b, -1, right, n / 2)]
            elif left or right:  # @line L5
                spans = [(a, 1, left, n)] if left else [(b, -1, right, n)]
            for start, step, side, length in spans:  # @line L6
                row, opp = (y, y + 1) if side < 0 else (y + 1, y)
                for k, area in enumerate(l_shape_areas(length)):  # @line L7
                    col = start + k if step == 1 else start - 1 - k
                    out[row][col] = _blend(out[row][col], img[opp][col], area)  # @line L8


def _transpose(grid: Image) -> Image:
    return [list(col) for col in zip(*grid)]


def morphological_antialiasing(image: Sequence[Sequence[Pixel]], threshold=0, directions: str = "hv") -> Image:
    """Return the MLAA-filtered image.

    directions selects the passes: "h" for lines between rows, "v" for lines
    between columns. Precondition: a nonempty rectangular image. Cost: Theta(W H)
    pixel comparisons and Theta(W H) blends.
    """
    img = [list(row) for row in image]
    out = [list(row) for row in image]
    if "h" in directions:
        _process_rows(img, out, threshold)
    if "v" in directions:
        out_t = _transpose(out)
        _process_rows(_transpose(img), out_t, threshold)
        out = _transpose(out_t)
    return out  # @line L9
