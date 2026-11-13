# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/integral-image/. The authors are listed in prov/863FHC.jsonl.

"""The integral image (summed-area table) of a gray image, with rectangle sums and box means.

An image is a list of H rows of W numbers, image[y][x]. The table S has H + 1
rows and W + 1 columns, and S[y][x] is the sum of image[j][i] over j < y and
i < x, so row 0 and column 0 are zero. A rectangle is half-open:
x0 <= x < x1 and y0 <= y < y1. BUILD costs O(WH) additions; a rectangle sum
costs 3 additions or subtractions for any rectangle size.

With a modulus m, the entries are kept modulo m, as unsigned machine words of
b bits keep them modulo 2^b. A rectangle sum is then correct whenever the true
sum lies in 0..m-1, however large the image is.
"""

from fractions import Fraction
from typing import List, Optional, Sequence, Union

Num = Union[int, float, Fraction]


class IntegralImage:
    """A static summed-area table over a W x H image."""

    def __init__(self, image: Sequence[Sequence[Num]], modulus: Optional[int] = None) -> None:
        """BUILD: one pass over the pixels, a running row sum plus the entry above.

        Precondition: all rows have the same length; with a modulus, the pixels are integers.
        Cost: O(WH) time and (W + 1)(H + 1) entries of space.
        """
        self.height = len(image)
        self.width = len(image[0]) if self.height else 0
        self.modulus = modulus
        w, h, m = self.width, self.height, modulus
        table: List[List[Num]] = [[0] * (w + 1) for _ in range(h + 1)]  # @line L1
        for y in range(h):  # @line L2
            run: Num = 0  # @line L3
            for x in range(w):  # @line L4
                run = run + image[y][x]  # @line L5
                if m is not None:
                    run %= m
                entry = table[y][x + 1] + run  # @line L6
                table[y + 1][x + 1] = entry % m if m is not None else entry
        self.table = table  # @line L7

    def rect_sum(self, x0: int, y0: int, x1: int, y1: int) -> Num:
        """RECT-SUM: the sum over x0 <= x < x1, y0 <= y < y1, in O(1).

        Precondition: 0 <= x0 <= x1 <= W and 0 <= y0 <= y1 <= H.
        """
        if not (0 <= x0 <= x1 <= self.width and 0 <= y0 <= y1 <= self.height):
            raise ValueError("the rectangle must lie inside the image")
        s = self.table
        total = s[y1][x1] - s[y0][x1] - s[y1][x0] + s[y0][x0]  # @line L8
        return total % self.modulus if self.modulus is not None else total

    def rect_mean(self, x0: int, y0: int, x1: int, y1: int) -> Num:
        """The mean over a nonempty rectangle; exact Fraction for integer or Fraction pixels."""
        area = (x1 - x0) * (y1 - y0)
        if area <= 0:
            raise ValueError("the rectangle must not be empty")
        total = self.rect_sum(x0, y0, x1, y1)
        return total / area if isinstance(total, float) else Fraction(total) / area

    def box_mean(self, x: int, y: int, r: int) -> Num:
        """BOX-MEAN: the mean over the (2r+1) x (2r+1) window of (x, y), cut at the image border."""
        x0, x1 = max(0, x - r), min(self.width, x + r + 1)  # @line L9
        y0, y1 = max(0, y - r), min(self.height, y + r + 1)
        return self.rect_mean(x0, y0, x1, y1)  # @line L10

    def box_filter(self, r: int) -> List[List[Num]]:
        """The box mean of every pixel, with the window cut at the border. O(WH) for any r."""
        return [[self.box_mean(x, y, r) for x in range(self.width)] for y in range(self.height)]

    def check_invariant(self, image: Sequence[Sequence[Num]]) -> bool:
        """Check S[y][x] against the direct sum of the top-left rectangle. O(W^2 H^2)."""
        for y in range(self.height + 1):
            for x in range(self.width + 1):
                direct = sum(image[j][i] for j in range(y) for i in range(x))
                if self.modulus is not None:
                    direct %= self.modulus
                if self.table[y][x] != direct:
                    return False
        return True


def local_variance(image: Sequence[Sequence[Num]], r: int) -> List[List[Num]]:
    """The variance over each window cut at the border, from a table of values and a table of squares."""
    first = IntegralImage(image)
    second = IntegralImage([[v * v for v in row] for row in image])
    out = []
    for y in range(first.height):
        row = []
        for x in range(first.width):
            mean = first.box_mean(x, y, r)
            row.append(second.box_mean(x, y, r) - mean * mean)
        out.append(row)
    return out
