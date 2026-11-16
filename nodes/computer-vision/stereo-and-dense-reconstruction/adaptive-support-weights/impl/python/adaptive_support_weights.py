# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-support-weights/. The authors are listed in prov/WDQMCM.jsonl.
"""Adaptive support weights for stereo (Yoon and Kweon, 2006).

An image is a list of rows of RGB triples with values in 0..255; the value
at pixel (u, v), column u and row v, is img[v][u]. The pair is rectified
and the left pixel (u, v) matches the right pixel (u - d, v), d >= 0.

The weight of a pixel q in the window of a pixel p is

    w(p, q) = exp(-(dc(p, q) / gamma_c + dg(p, q) / gamma_p)),

where dc is the Euclidean distance of the two colors in CIELab and dg the
Euclidean distance of the two pixel positions. The cost of disparity d at
the left pixel p, with pd = p - (d, 0), is

    E(p, d) = sum_q w(p, q) w(pd, qd) e(q, qd) / sum_q w(p, q) w(pd, qd),

over the offsets o with |o_u|, |o_v| <= r such that q = p + o is in the left
image and qd = q - (d, 0) is in the right image. The raw cost e is the sum
over the three channels of the absolute RGB differences, truncated at T.
The disparity of p is the least d in [0, D) with d <= u that has the least
E(p, d).
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

Color = Tuple[float, float, float]


def _lin(c: float) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _f(t: float) -> float:
    e = 6.0 / 29.0
    return t ** (1.0 / 3.0) if t > e ** 3 else t / (3 * e * e) + 4.0 / 29.0


def rgb_to_lab(rgb: Sequence[float]) -> Color:
    """CIELab of an sRGB color with channels in 0..255 (D65 white)."""
    r, g, b = (_lin(float(c)) for c in rgb)
    x = 0.4124 * r + 0.3576 * g + 0.1805 * b
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = 0.0193 * r + 0.1192 * g + 0.9505 * b
    fx, fy, fz = _f(x / 0.95047), _f(y / 1.0), _f(z / 1.08883)
    return (116.0 * fy - 16.0, 500.0 * (fx - fy), 200.0 * (fy - fz))


def support_weights(lab: Sequence[Sequence[Color]], u: int, v: int, r: int,
                    gamma_c: float, gamma_p: float) -> List[Optional[float]]:
    """The weights w(p, p + o) of the pixel p = (u, v) for the offsets o of
    the window in row-major order; None for an offset outside the image."""
    h, w = len(lab), len(lab[0])
    c0 = lab[v][u]
    out: List[Optional[float]] = []
    for dv in range(-r, r + 1):
        for du in range(-r, r + 1):
            x, y = u + du, v + dv
            if 0 <= x < w and 0 <= y < h:
                dc = math.dist(c0, lab[y][x])
                dg = math.hypot(du, dv)
                out.append(math.exp(-(dc / gamma_c + dg / gamma_p)))
            else:
                out.append(None)
    return out


def asw_disparity(left: Sequence[Sequence[Sequence[int]]], right: Sequence[Sequence[Sequence[int]]],
                  D: int, r: int = 17, gamma_c: float = 5.0, gamma_p: float = 17.5,
                  T: float = 40.0) -> List[List[int]]:
    """The winner-takes-all disparity map of the adaptive support weight
    cost, in O(W H D r^2) time."""
    if D < 1 or r < 0:
        raise ValueError("need D >= 1 and r >= 0")
    h, w = len(left), len(left[0])
    lab_l = [[rgb_to_lab(c) for c in row] for row in left]
    lab_r = [[rgb_to_lab(c) for c in row] for row in right]
    wl = [[support_weights(lab_l, u, v, r, gamma_c, gamma_p) for u in range(w)] for v in range(h)]
    wr = [[support_weights(lab_r, u, v, r, gamma_c, gamma_p) for u in range(w)] for v in range(h)]
    offs = [(du, dv) for dv in range(-r, r + 1) for du in range(-r, r + 1)]
    out = []
    for v in range(h):  # @line L1
        row = []
        for u in range(w):  # @line L1
            best, bd = math.inf, 0
            for d in range(min(D - 1, u) + 1):  # @line L2
                num = den = 0.0  # @line L3
                a, b = wl[v][u], wr[v][u - d]
                for k, (du, dv) in enumerate(offs):  # @line L4
                    if a[k] is None or b[k] is None:  # @line L4
                        continue
                    wt = a[k] * b[k]  # @line L5
                    cl = left[v + dv][u + du]
                    cr = right[v + dv][u + du - d]
                    e = min(abs(cl[0] - cr[0]) + abs(cl[1] - cr[1]) + abs(cl[2] - cr[2]), T)  # @line L6
                    num += wt * e  # @line L6
                    den += wt  # @line L6
                cost = num / den  # @line L7
                if cost < best:  # @line L8
                    best, bd = cost, d  # @line L8
            row.append(bd)  # @line L8
        out.append(row)
    return out  # @line L9


def asw_cost_brute(left, right, u: int, v: int, d: int, r: int, gamma_c: float,
                   gamma_p: float, T: float) -> float:
    """E(p, d) straight from the definition, for the tests."""
    h, w = len(left), len(left[0])
    lp, lpd = rgb_to_lab(left[v][u]), rgb_to_lab(right[v][u - d])
    num = den = 0.0
    for dv in range(-r, r + 1):
        for du in range(-r, r + 1):
            x, y = u + du, v + dv
            if not (0 <= y < h and 0 <= x < w and 0 <= x - d < w):
                continue
            g = math.sqrt(du * du + dv * dv)
            w1 = math.exp(-(math.dist(lp, rgb_to_lab(left[y][x])) / gamma_c + g / gamma_p))
            w2 = math.exp(-(math.dist(lpd, rgb_to_lab(right[y][x - d])) / gamma_c + g / gamma_p))
            e = min(sum(abs(p - q) for p, q in zip(left[y][x], right[y][x - d])), T)
            num += w1 * w2 * e
            den += w1 * w2
    return num / den
