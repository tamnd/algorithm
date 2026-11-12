# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wu-line-algorithm/. The authors are listed in prov/ZEVX63.jsonl.

from fractions import Fraction

Pixel = tuple[int, int, Fraction]


def wu_line(x0: int, y0: int, x1: int, y1: int, w: int = 16) -> list[Pixel]:
    """Antialiased line by Wu's method with a w-bit error accumulator, first octant only.

    Precondition: x0 < x1 and 0 <= y1 - y0 <= x1 - x0, integer endpoints (pixel centers), w >= 1.
    Returns (x, y, intensity) triples, intensity in [0, 1] as an exact Fraction. The endpoints get
    intensity 1, and each inner column gets two pixels whose intensities add up to 1.
    Cost: 2 (x1 - x0) pixels, O(1) extra space besides the output, integer additions only.
    """
    one = 1 << w
    dx, dy = x1 - x0, y1 - y0  # @line L1
    d = (2 * dy * one + dx) // (2 * dx)  # @line L2: floor(dy 2^w / dx + 1/2)
    acc, y = 0, y0  # @line L3
    out: list[Pixel] = [(x0, y0, Fraction(1)), (x1, y1, Fraction(1))]  # @line L4
    for x in range(x0 + 1, x1):  # @line L5
        acc += d  # @line L6
        if acc >= one:  # @line L7
            acc -= one
            y += 1
        out.append((x, y, Fraction(one - acc, one)))  # @line L8
        out.append((x, y + 1, Fraction(acc, one)))  # @line L9
    return out


def wu_line_exact(x0: int, y0: int, x1: int, y1: int) -> list[Pixel]:
    """The same method with an exact accumulator: the error is kept as a numerator over dx.

    Same precondition and output as wu_line. The intensities are the exact tent weights
    1 - |j - Y| of the two pixels around the true height Y of each inner column.
    """
    dx, dy = x1 - x0, y1 - y0
    acc, y = 0, y0
    out: list[Pixel] = [(x0, y0, Fraction(1)), (x1, y1, Fraction(1))]
    for x in range(x0 + 1, x1):
        acc += dy
        if acc >= dx:
            acc -= dx
            y += 1
        out.append((x, y, Fraction(dx - acc, dx)))
        out.append((x, y + 1, Fraction(acc, dx)))
    return out


def wu_line_any(x0: int, y0: int, x1: int, y1: int, w: int = 16, exact: bool = False) -> list[Pixel]:
    """Wu's line for any two integer endpoints, by reflection and exchange of the axes."""
    if (x0, y0) == (x1, y1):
        return [(x0, y0, Fraction(1))]
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0, x1, y1 = y0, x0, y1, x1
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    flip = y1 < y0
    if flip:
        y0, y1 = -y0, -y1
    pts = wu_line_exact(x0, y0, x1, y1) if exact else wu_line(x0, y0, x1, y1, w)
    res = []
    for x, y, a in pts:
        if flip:
            y = -y
        res.append((y, x, a) if steep else (x, y, a))
    return res
