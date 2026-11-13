# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-filter/. The authors are listed in prov/T1ZJ15.jsonl.

"""The Gaussian filter: a sampled, truncated and normalized Gaussian kernel applied in two 1D passes.

An image is a list of H rows of W numbers, image[y][x], with the pixel centers
at integer coordinates. A pixel outside the image takes its value from the
border rule: "clamp", "mirror" (edge pixel repeated), "wrap" or "zero".

gaussian_filter costs O(WH R) for the radius R = ceil(3 sigma). The module also
gives the repeated box approximation (Wells 1986): n box passes of radius r by
running sums, O(n WH) for any r, whose kernel has variance n r (r + 1) / 3.
"""

import math
from fractions import Fraction
from typing import List, Optional, Sequence, Union

Num = Union[int, float, Fraction]
Image = List[List[Num]]
BORDERS = ("clamp", "mirror", "wrap", "zero")


def border_index(i: int, n: int, border: str) -> Optional[int]:
    """Map an index i of an axis of length n to 0..n-1, or None for a zero pixel."""
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


def gaussian_kernel(sigma: float, radius: Optional[int] = None) -> List[float]:
    """The 2R+1 weights exp(-u^2 / (2 sigma^2)) for |u| <= R, divided by their sum.

    R defaults to ceil(3 sigma). Precondition: sigma > 0.
    """
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    if radius is None:
        radius = math.ceil(3 * sigma)  # @line L1
    raw = [math.exp(-(u * u) / (2 * sigma * sigma)) for u in range(-radius, radius + 1)]  # @line L2
    total = math.fsum(raw)
    return [w / total for w in raw]  # @line L3


def _line_filter(line: Sequence[Num], kernel: Sequence[Num], border: str) -> List[Num]:
    """One 1D pass: out[x] = sum over u of kernel[u + R] * line[x + u]."""
    n, rad = len(line), len(kernel) // 2
    out = []
    for x in range(n):
        acc: Num = 0
        for u in range(-rad, rad + 1):
            j = border_index(x + u, n, border)
            if j is not None:
                acc = acc + kernel[u + rad] * line[j]
        out.append(acc)
    return out


def separable_filter(image: Sequence[Sequence[Num]], kernel: Sequence[Num], border: str = "clamp") -> Image:
    """Filter the rows with the 1D kernel, then the columns of the result.

    Precondition: the kernel has odd length 2R+1 and is centered at index R.
    Cost: 2(2R+1) multiplications per pixel, O(WH R) in total.
    """
    if len(kernel) % 2 != 1:
        raise ValueError("the kernel must have odd length")
    height = len(image)
    width = len(image[0]) if height else 0
    if height == 0 or width == 0:
        return []
    g = [_line_filter(row, kernel, border) for row in image]  # @line L4
    cols = [_line_filter([g[y][x] for y in range(height)], kernel, border) for x in range(width)]  # @line L5
    return [[cols[x][y] for x in range(width)] for y in range(height)]


def gaussian_filter(image: Sequence[Sequence[Num]], sigma: float, border: str = "clamp",
                    radius: Optional[int] = None) -> Image:
    """The Gaussian filter of standard deviation sigma (in pixels), in two passes. O(WH sigma)."""
    kernel = gaussian_kernel(sigma, radius)
    return separable_filter(image, kernel, border)  # @line L6


def _box_line(line: Sequence[Num], r: int, border: str) -> List[Num]:
    """Running window sums of radius r along one line, O(n + r)."""
    n = len(line)

    def at(i: int) -> Num:
        j = border_index(i, n, border)
        return 0 if j is None else line[j]

    s = sum(at(u) for u in range(-r, r + 1))
    out = [s]
    for x in range(1, n):
        s = s + at(x + r) - at(x - r - 1)
        out.append(s)
    return out


def box_cascade_sum(image: Sequence[Sequence[Num]], r: int, passes: int, border: str = "wrap") -> Image:
    """Apply `passes` box sums of radius r along the rows and along the columns.

    The result is not divided; divide by (2r+1)^(2 passes) for the blur. The border
    rule is applied again at each pass, so the result equals one convolution with
    the composite kernel only for "wrap", or away from the border.
    Cost: O(passes (WH + (W + H) r)).
    """
    height = len(image)
    width = len(image[0]) if height else 0
    if height == 0 or width == 0:
        return []
    cur = [list(row) for row in image]
    for _ in range(passes):
        cur = [_box_line(row, r, border) for row in cur]
    for _ in range(passes):
        cols = [_box_line([cur[y][x] for y in range(height)], r, border) for x in range(width)]
        cur = [[cols[x][y] for x in range(width)] for y in range(height)]
    return cur


def box_cascade_kernel(r: int, passes: int) -> List[int]:
    """The 1D kernel of `passes` box sums of radius r: integer weights of length 2 passes r + 1."""
    kernel = [1]
    box = [1] * (2 * r + 1)
    for _ in range(passes):
        nxt = [0] * (len(kernel) + 2 * r)
        for i, a in enumerate(kernel):
            for j, b in enumerate(box):
                nxt[i + j] += a * b
        kernel = nxt
    return kernel


def box_cascade_sigma(r: int, passes: int) -> float:
    """The standard deviation of the normalized cascade kernel, (passes r (r + 1) / 3)^(1/2)."""
    return math.sqrt(passes * r * (r + 1) / 3)
