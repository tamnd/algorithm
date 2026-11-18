# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/percentage-closer-filtering/. The authors are listed in prov/CF3C6M.jsonl.

"""Percentage-closer filtering (Reeves, Salesin and Cook 1987).

A shadow map s is a list of h rows of w depths, s[j][i], with i the column
(x to the right) and j the row (y down). Texel (i, j) has its center at
(i + 1/2, j + 1/2) in texel units. Depth is in [0, 1] (the Direct3D clip
range), smaller is nearer to the light. A tap is lit when z - b <= s[j][i];
a tap outside the map counts as lit. Every function returns the lit fraction.
With int or Fraction input the result is exact.
"""

from fractions import Fraction
from math import floor


def lit_tap(s, i, j, z, b):
    """1 if the tap (i, j) is lit for the receiver depth z and the bias b, else 0."""
    if j < 0 or j >= len(s) or i < 0 or i >= len(s[0]):
        return 1
    return 1 if z - b <= s[j][i] else 0


def pcf(s, x, y, z, b, kernel):
    """Weighted PCF. kernel maps the offset (u, v) to a weight >= 0."""
    i, j = floor(x), floor(y)  # @line L1
    acc, wsum = 0, 0  # @line L2
    for (u, v), wt in kernel.items():  # @line L3
        if wt <= 0:
            continue
        t = lit_tap(s, i + u, j + v, z, b)  # @line L4
        acc += wt * t  # @line L5
        wsum += wt  # @line L6
    return Fraction(acc) / wsum if isinstance(acc, int) else acc / wsum  # @line L7


def box_kernel(r):
    """The (2r + 1) x (2r + 1) box with weight 1 per tap."""
    return {(u, v): 1 for u in range(-r, r + 1) for v in range(-r, r + 1)}


def tent_kernel(r):
    """The separable tent with weights (r + 1 - |u|) (r + 1 - |v|)."""
    return {(u, v): (r + 1 - abs(u)) * (r + 1 - abs(v))
            for u in range(-r, r + 1) for v in range(-r, r + 1)}


def pcf_bilinear(s, x, y, z, b):
    """The 2 x 2 bilinear PCF of graphics hardware."""
    fx, fy = x - Fraction(1, 2), y - Fraction(1, 2)
    i, j = floor(fx), floor(fy)  # @line L8
    f, g = fx - i, fy - j
    c00 = lit_tap(s, i, j, z, b)  # @line L9
    c10 = lit_tap(s, i + 1, j, z, b)
    c01 = lit_tap(s, i, j + 1, z, b)
    c11 = lit_tap(s, i + 1, j + 1, z, b)
    return ((1 - f) * (1 - g) * c00 + f * (1 - g) * c10  # @line L10
            + (1 - f) * g * c01 + f * g * c11)


def filter_depths_then_compare(s, x, y, z, b, r):
    """The wrong order: average the depths in the box, then compare once.

    It returns 0 or 1, so it does not soften the edge. It is here for the
    tests and the page, not as a method to use.
    """
    i, j = floor(x), floor(y)
    taps = [s[j + v][i + u] for u in range(-r, r + 1) for v in range(-r, r + 1)
            if 0 <= j + v < len(s) and 0 <= i + u < len(s[0])]
    mean = Fraction(sum(Fraction(t) for t in taps)) / len(taps)
    return 1 if z - b <= mean else 0


def box_scene(w, h, floor_depth, box_depth, x0, y0, x1, y1):
    """A light-space depth map: a floor at floor_depth and the top of a box
    at box_depth over the texels with x0 <= i < x1 and y0 <= j < y1."""
    return [[box_depth if x0 <= i < x1 and y0 <= j < y1 else floor_depth
             for i in range(w)] for j in range(h)]
