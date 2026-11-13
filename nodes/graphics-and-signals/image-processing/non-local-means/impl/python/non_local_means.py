# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-local-means/. The authors are listed in prov/S75JEX.jsonl.

"""Non-local means (Buades, Coll and Morel 2005), in the per-offset form with integral images.

An image is a list of H rows of W numbers, image[y][x]. For a pixel p the
output is a weighted mean of the pixels q in its search window of radius s:

    NL(p) = sum_q w(p, q) f(q) / sum_q w(p, q),   w(p, q) = weight(d(p, q)),

where d(p, q) is the mean squared difference of the (2f+1) x (2f+1) patches
around p and q, and the default weight is exp(-d / h^2). Border rules: the
search window is cut at the image border (q must lie inside the image), and
a patch pixel outside the image takes the value of the nearest edge pixel
(clamp).

For one offset o = q - p the squared differences D(x) = (f(x) - f(x + o))^2
are the same for every pixel, so one integral image of D gives every patch
distance for that offset in O(1). The cost is O(WH s^2) for any patch radius
f, against O(WH s^2 f^2) for the direct evaluation (Darbon et al. 2008).
"""

import math
from fractions import Fraction
from typing import Callable, List, Optional, Sequence, Union

Num = Union[int, float, Fraction]
Image = List[List[Num]]


def _clamp(i: int, n: int) -> int:
    return 0 if i < 0 else (n - 1 if i >= n else i)


def non_local_means(image: Sequence[Sequence[Num]], h: float = 10.0, search: int = 3, patch: int = 1,
                    weight: Optional[Callable[[Num], Num]] = None) -> Image:
    """NL-means with search radius `search` and patch radius `patch`.

    weight maps the mean squared patch distance d to a positive weight; the
    default is exp(-d / h^2). With a rational weight and integer pixels the
    result is exact. Cost: O(WH search^2) time, O(WH) extra space.
    """
    height = len(image)
    width = len(image[0]) if height else 0
    if height == 0 or width == 0:
        return []
    if weight is None:
        weight = lambda d: math.exp(-d / (h * h))
    f = patch
    area = (2 * f + 1) ** 2
    pw, ph = width + 2 * f, height + 2 * f
    num: List[List[Num]] = [[0] * width for _ in range(height)]
    den: List[List[Num]] = [[0] * width for _ in range(height)]
    for ov in range(-search, search + 1):  # @line L1
        for ou in range(-search, search + 1):
            s: List[List[Num]] = [[0] * (pw + 1) for _ in range(ph + 1)]
            for j in range(ph):
                run: Num = 0
                y = j - f
                for i in range(pw):
                    x = i - f
                    a = image[_clamp(y, height)][_clamp(x, width)]
                    b = image[_clamp(y + ov, height)][_clamp(x + ou, width)]
                    run = run + (a - b) * (a - b)  # @line L2
                    s[j + 1][i + 1] = s[j][i + 1] + run  # @line L3
            for y in range(max(0, -ov), min(height, height - ov)):  # @line L4
                for x in range(max(0, -ou), min(width, width - ou)):
                    y0, x0, y1, x1 = y, x, y + 2 * f + 1, x + 2 * f + 1
                    total = s[y1][x1] - s[y0][x1] - s[y1][x0] + s[y0][x0]
                    d = total / area if isinstance(total, float) else Fraction(total, area)  # @line L5
                    wq = weight(d)  # @line L6
                    num[y][x] = num[y][x] + wq * image[y + ov][x + ou]  # @line L7
                    den[y][x] = den[y][x] + wq
    return [[num[y][x] / den[y][x] for x in range(width)] for y in range(height)]  # @line L8
