# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/guided-filter/. The authors are listed in prov/4HSCV2.jsonl.

"""The guided filter of He, Sun and Tang (2010), with box means from integral images.

Inputs are a guidance image I and a filtering input p, both lists of H rows of
W numbers. In each window w_k of radius r the filter fits q = a_k I + b_k to p
by least squares with the penalty eps a_k^2, then averages the fits of all
windows that hold a pixel. Border rule: every window is cut at the image
border, and every mean divides by the number of pixels in the cut window
(the normalization N = BOX(1) of the paper).

Each box mean costs O(1) per pixel through an integral image, so the filter
costs O(WH) for any radius r.
"""

from fractions import Fraction
from typing import List, Sequence, Union

Num = Union[int, float, Fraction]
Image = List[List[Num]]


def box_mean(image: Sequence[Sequence[Num]], r: int) -> Image:
    """The mean over the (2r+1) x (2r+1) window of each pixel, cut at the border. O(WH)."""
    h = len(image)
    w = len(image[0]) if h else 0
    s: List[List[Num]] = [[0] * (w + 1) for _ in range(h + 1)]
    for y in range(h):
        run: Num = 0
        for x in range(w):
            run = run + image[y][x]
            s[y + 1][x + 1] = s[y][x + 1] + run
    out: Image = []
    for y in range(h):
        y0, y1 = max(0, y - r), min(h, y + r + 1)
        row = []
        for x in range(w):
            x0, x1 = max(0, x - r), min(w, x + r + 1)
            total = s[y1][x1] - s[y0][x1] - s[y1][x0] + s[y0][x0]
            n = (x1 - x0) * (y1 - y0)
            row.append(total / n if isinstance(total, float) else Fraction(total) / n)
        out.append(row)
    return out


def _mul(a: Sequence[Sequence[Num]], b: Sequence[Sequence[Num]]) -> Image:
    return [[p * q for p, q in zip(ra, rb)] for ra, rb in zip(a, b)]


def guided_filter(guide: Sequence[Sequence[Num]], src: Sequence[Sequence[Num]], r: int, eps: Num) -> Image:
    """Algorithm 1 of He, Sun and Tang. Precondition: eps > 0, guide and src have the same size.

    With integer or Fraction inputs and a Fraction eps the result is exact.
    Cost: six box means and O(1) work per pixel, so O(WH) for any r.
    """
    if eps <= 0:
        raise ValueError("eps must be positive")
    h = len(guide)
    w = len(guide[0]) if h else 0
    if h == 0 or w == 0:
        return []
    if len(src) != h or any(len(row) != w for row in src):
        raise ValueError("guide and src must have the same size")
    mean_i = box_mean(guide, r)  # @line L1
    mean_p = box_mean(src, r)
    corr_ii = box_mean(_mul(guide, guide), r)
    corr_ip = box_mean(_mul(guide, src), r)
    a: Image = []
    b: Image = []
    for y in range(h):
        ra, rb = [], []
        for x in range(w):
            var_i = corr_ii[y][x] - mean_i[y][x] * mean_i[y][x]  # @line L2
            cov_ip = corr_ip[y][x] - mean_i[y][x] * mean_p[y][x]
            ak = cov_ip / (var_i + eps)  # @line L3
            ra.append(ak)
            rb.append(mean_p[y][x] - ak * mean_i[y][x])
        a.append(ra)
        b.append(rb)
    mean_a = box_mean(a, r)  # @line L4
    mean_b = box_mean(b, r)
    return [[mean_a[y][x] * guide[y][x] + mean_b[y][x] for x in range(w)] for y in range(h)]  # @line L5
