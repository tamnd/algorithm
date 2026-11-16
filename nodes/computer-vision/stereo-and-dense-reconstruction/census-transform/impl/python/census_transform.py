# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/census-transform/. The authors are listed in prov/GZ7T8F.jsonl.
"""The census transform of Zabih and Woodfill (1994) and the census
matching cost for rectified stereo.

An image is a list of rows of integers (or of any values that can be
ordered); the value at pixel (u, v), column u and row v, is img[v][u].

The census string of pixel p with radius r has one bit for each pixel q of
the (2r + 1) x (2r + 1) window centered on p, except p itself. The bit is 1
if I(q) < I(p) and 0 otherwise. The bits are taken in row-major order of
the offsets (dv, du), from (-r, -r) to (r, r), and the first offset gives
the most significant bit. A neighbor outside the image takes the value of
the nearest border pixel (the coordinates are clamped).

The cost of matching the left pixel (u, v) with the right pixel
(u - d, v) is the Hamming distance of their census strings, the number of
bits in which they differ.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple


def _clamp(x: int, lo: int, hi: int) -> int:
    return lo if x < lo else hi if x > hi else x


def window_offsets(r: int) -> List[Tuple[int, int]]:
    """The offsets (du, dv) of the census window of radius r, without
    (0, 0), in the order of the bits (most significant first)."""
    return [(du, dv) for dv in range(-r, r + 1) for du in range(-r, r + 1)
            if (du, dv) != (0, 0)]


def census(img: Sequence[Sequence[int]], r: int = 2) -> List[List[int]]:
    """The census transform of img with window radius r >= 1. Each entry
    is an integer of (2r + 1)^2 - 1 bits."""
    if r < 1:
        raise ValueError("the radius must be at least 1")
    h, w = len(img), len(img[0])
    offs = window_offsets(r)
    out = []
    for v in range(h):  # @line L1
        row = []
        for u in range(w):  # @line L1
            c = 0  # @line L2
            center = img[v][u]
            for du, dv in offs:  # @line L3
                q = img[_clamp(v + dv, 0, h - 1)][_clamp(u + du, 0, w - 1)]
                c = (c << 1) | (1 if q < center else 0)  # @line L4
            row.append(c)  # @line L5
        out.append(row)
    return out  # @line L6


def popcount(x: int) -> int:
    """The number of 1 bits of the integer x >= 0."""
    return bin(x).count("1")


def hamming(a: int, b: int) -> int:
    """The Hamming distance of two census strings."""
    return popcount(a ^ b)  # @line L7


def census_cost_volume(left: Sequence[Sequence[int]], right: Sequence[Sequence[int]],
                       D: int, r: int = 2) -> List[List[List[int]]]:
    """The census cost C[v][u][d] = hamming(TL[v][u], TR[v][u - d]) for
    0 <= d < D. If u - d < 0 the right pixel does not exist, and the cost
    is the number of bits n + 1, larger than any real cost."""
    tl, tr = census(left, r), census(right, r)
    n = (2 * r + 1) ** 2 - 1
    h, w = len(left), len(left[0])
    return [[[hamming(tl[v][u], tr[v][u - d]) if u - d >= 0 else n + 1
              for d in range(D)] for u in range(w)] for v in range(h)]


def census_disparity(left: Sequence[Sequence[int]], right: Sequence[Sequence[int]],
                     D: int, r: int = 2, a: int = 0) -> List[List[int]]:
    """The winner-takes-all disparity map of the census cost, summed over a
    (2a + 1) x (2a + 1) box (a = 0: no sum). The box is clamped to the
    image. Ties go to the smallest disparity."""
    cv = census_cost_volume(left, right, D, r)
    h, w = len(left), len(left[0])
    out = []
    for v in range(h):
        row = []
        for u in range(w):
            best, bd = None, 0
            for d in range(D):
                s = 0
                for y in range(max(v - a, 0), min(v + a, h - 1) + 1):
                    for x in range(max(u - a, 0), min(u + a, w - 1) + 1):
                        s += cv[y][x][d]
                if best is None or s < best:
                    best, bd = s, d
            row.append(bd)
        out.append(row)
    return out


def rank(img: Sequence[Sequence[int]], r: int = 2) -> List[List[int]]:
    """The rank transform: the number of neighbors in the window that are
    less than the center, which is the popcount of the census string."""
    return [[popcount(c) for c in row] for row in census(img, r)]
