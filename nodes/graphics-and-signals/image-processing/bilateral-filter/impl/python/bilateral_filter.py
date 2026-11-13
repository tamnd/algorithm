# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bilateral-filter/. The authors are listed in prov/1PRAE4.jsonl.

"""The bilateral filter of Tomasi and Manduchi (1998), evaluated directly.

An image is a list of H rows of W numbers, image[y][x]. The output at p is

    g(p) = sum_q ws(q - p) wr(f(q) - f(p)) f(q) / sum_q ws(q - p) wr(f(q) - f(p))

over the pixels q of the (2R+1) x (2R+1) window of p. Border rule: the window
is cut at the image border, so only pixels inside the image take part, and the
division by the sum of the weights renormalizes the cut window.

The loops run offset by offset ("shift and accumulate"): the spatial weight
of an offset is computed once, then added into a numerator and a denominator
for every pixel. The cost is O(WH R^2), the same as the per-pixel loop order.
"""

import math
from fractions import Fraction
from typing import Callable, List, Optional, Sequence, Union

Num = Union[int, float, Fraction]
Image = List[List[Num]]
Weight = Callable[[int, int], Num]
RangeWeight = Callable[[Num], Num]


def gaussian_spatial(sigma_s: float) -> Weight:
    """ws(u, v) = exp(-(u^2 + v^2) / (2 sigma_s^2))."""
    return lambda u, v: math.exp(-(u * u + v * v) / (2 * sigma_s * sigma_s))


def gaussian_range(sigma_r: float) -> RangeWeight:
    """wr(d) = exp(-d^2 / (2 sigma_r^2))."""
    return lambda d: math.exp(-(d * d) / (2 * sigma_r * sigma_r))


def bilateral_filter(image: Sequence[Sequence[Num]], sigma_s: float = 1.0, sigma_r: float = 10.0,
                     radius: Optional[int] = None, spatial: Optional[Weight] = None,
                     rng_weight: Optional[RangeWeight] = None) -> Image:
    """The bilateral filter with Gaussian weights, or with the given weight functions.

    radius defaults to ceil(2 sigma_s). The weight functions must be positive at 0,
    so the center pixel keeps every denominator positive.
    Cost: O(WH R^2) time, O(WH) extra space.
    """
    h = len(image)
    w = len(image[0]) if h else 0
    if h == 0 or w == 0:
        return []
    if radius is None:
        radius = math.ceil(2 * sigma_s)
    ws = spatial if spatial is not None else gaussian_spatial(sigma_s)
    wr = rng_weight if rng_weight is not None else gaussian_range(sigma_r)
    num: List[List[Num]] = [[0] * w for _ in range(h)]
    den: List[List[Num]] = [[0] * w for _ in range(h)]
    for v in range(-radius, radius + 1):  # @line L1
        for u in range(-radius, radius + 1):
            spatial_w = ws(u, v)  # @line L2
            for y in range(max(0, -v), min(h, h - v)):  # @line L3
                for x in range(max(0, -u), min(w, w - u)):
                    fp, fq = image[y][x], image[y + v][x + u]
                    weight = spatial_w * wr(fq - fp)  # @line L4
                    num[y][x] = num[y][x] + weight * fq  # @line L5
                    den[y][x] = den[y][x] + weight
    out: Image = []
    for y in range(h):
        row = []
        for x in range(w):
            if isinstance(num[y][x], float) or isinstance(den[y][x], float):
                row.append(num[y][x] / den[y][x])  # @line L6
            else:
                row.append(Fraction(num[y][x]) / den[y][x])
        out.append(row)
    return out  # @line L7
