# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bilinear-filtering/. The authors are listed in prov/85PFVB.jsonl.

"""Bilinear texture filtering with texel centers at half-integers.

A texture is H rows of W texels, texture[t][s], each texel a tuple of channel
values. Normalized coordinates (u, v) map to texel space (u W, v H), and texel
(s, t) has its center at (s + 1/2, t + 1/2). The wrap mode defines texels
outside the grid: "clamp" (clamp to the edge texel), "repeat" or "mirror".
Use fractions.Fraction coordinates for exact results.
"""

import math
from fractions import Fraction
from typing import Sequence, Union

Num = Union[int, float, Fraction]
Texel = tuple


def wrap_index(i: int, n: int, mode: str) -> int:
    """Map an integer texel index to [0, n) by the wrap mode."""
    if mode == "clamp":
        return min(max(i, 0), n - 1)
    if mode == "repeat":
        return i % n
    if mode == "mirror":
        m = i % (2 * n)
        return m if m < n else 2 * n - 1 - m
    raise ValueError(f"unknown wrap mode {mode!r}")


def bilinear_filtering(texture: Sequence[Sequence[Texel]], u: Num, v: Num, mode: str = "clamp") -> Texel:
    """Return the bilinearly filtered texture value at (u, v).

    Precondition: the texture has W >= 1 columns and H >= 1 rows, and all
    texels have the same channel count. Cost: 4 texel reads and O(c) arithmetic
    for c channels.
    """
    h, w = len(texture), len(texture[0])
    x = u * w - Fraction(1, 2) if isinstance(u, (int, Fraction)) else u * w - 0.5
    y = v * h - Fraction(1, 2) if isinstance(v, (int, Fraction)) else v * h - 0.5
    i0, j0 = math.floor(x), math.floor(y)
    a, b = x - i0, y - j0  # fractional offsets in [0, 1)
    s0, s1 = wrap_index(i0, w, mode), wrap_index(i0 + 1, w, mode)
    t0, t1 = wrap_index(j0, h, mode), wrap_index(j0 + 1, h, mode)
    t00, t10 = texture[t0][s0], texture[t0][s1]
    t01, t11 = texture[t1][s0], texture[t1][s1]
    return tuple(
        (1 - a) * (1 - b) * c00 + a * (1 - b) * c10 + (1 - a) * b * c01 + a * b * c11
        for c00, c10, c01, c11 in zip(t00, t10, t01, t11)
    )


def nearest_filtering(texture: Sequence[Sequence[Texel]], u: Num, v: Num, mode: str = "clamp") -> Texel:
    """Return the texel whose cell [s, s+1) x [t, t+1) contains (u W, v H)."""
    h, w = len(texture), len(texture[0])
    return texture[wrap_index(math.floor(v * h), h, mode)][wrap_index(math.floor(u * w), w, mode)]
