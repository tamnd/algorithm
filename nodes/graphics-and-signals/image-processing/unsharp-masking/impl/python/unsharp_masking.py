# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unsharp-masking/. The authors are listed in prov/JCQW4C.jsonl.

"""Unsharp masking: g = f + amount * (f - blur(f)).

An image is a list of H rows of W numbers, image[y][x]. The blur is a
separable filter with a 1D kernel of odd length 2R+1 (a sampled Gaussian by
default). A pixel outside the image takes its value from the border rule:
"clamp", "mirror" (edge pixel repeated), "wrap" or "zero".

Without a threshold the result is one linear filter with the 2D kernel
(1 + amount) delta - amount K. With a threshold t, a pixel whose detail
|f - blur(f)| is below t is left as it is, so the filter is no longer linear.
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


def gaussian_kernel(sigma: float) -> List[float]:
    """The normalized sampled Gaussian of radius ceil(3 sigma)."""
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    rad = math.ceil(3 * sigma)
    raw = [math.exp(-(u * u) / (2 * sigma * sigma)) for u in range(-rad, rad + 1)]
    total = math.fsum(raw)
    return [w / total for w in raw]


def _line(line: Sequence[Num], kernel: Sequence[Num], border: str) -> List[Num]:
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


def separable_blur(image: Sequence[Sequence[Num]], kernel: Sequence[Num], border: str) -> Image:
    """Rows, then columns, with the same 1D kernel. O(WH R)."""
    if len(kernel) % 2 != 1:
        raise ValueError("the kernel must have odd length")
    h = len(image)
    w = len(image[0]) if h else 0
    if h == 0 or w == 0:
        return []
    rows = [_line(r, kernel, border) for r in image]
    cols = [_line([rows[y][x] for y in range(h)], kernel, border) for x in range(w)]
    return [[cols[x][y] for x in range(w)] for y in range(h)]


def unsharp_mask(image: Sequence[Sequence[Num]], amount: Num, kernel: Optional[Sequence[Num]] = None,
                 sigma: float = 1.0, border: str = "clamp", threshold: Optional[Num] = None,
                 low: Optional[Num] = None, high: Optional[Num] = None) -> Image:
    """Sharpen by adding `amount` times the detail image f - blur(f).

    kernel: a 1D blur kernel of odd length; when None, the Gaussian of `sigma`.
    threshold: when given, pixels with |detail| < threshold are not changed.
    low, high: when given, the result is clipped to [low, high].
    Cost: O(WH R) for the blur plus O(WH) for the rest.
    """
    if kernel is None:
        kernel = gaussian_kernel(sigma)
    blurred = separable_blur(image, kernel, border)  # @line L1
    out: Image = []
    for y, row in enumerate(image):  # @line L2
        new_row = []
        for x, f in enumerate(row):
            detail = f - blurred[y][x]  # @line L3
            if threshold is not None and abs(detail) < threshold:
                g = f
            else:
                g = f + amount * detail  # @line L4
            if low is not None and g < low:
                g = low
            if high is not None and g > high:
                g = high
            new_row.append(g)
        out.append(new_row)
    return out  # @line L5


def combined_kernel(kernel: Sequence[Num], amount: Num) -> List[List[Num]]:
    """The 2D kernel (1 + amount) delta - amount (k outer k) of the linear form."""
    n, c = len(kernel), len(kernel) // 2
    out = [[-amount * a * b for b in kernel] for a in kernel]
    out[c][c] = out[c][c] + 1 + amount
    assert len(out) == n
    return out
