# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-matching-stereo/. The authors are listed in prov/VSCW79.jsonl.
"""Block matching stereo: the sum of absolute (or squared) differences over
a square window, and winner-takes-all over the disparities.

An image is a list of rows of integers; the value at pixel (u, v), column u
and row v, is img[v][u]. The pair is rectified and the right camera is to
the right of the left one, so the left pixel (u, v) matches the right
pixel (u - d, v) with d >= 0.

Definitions used by both the fast and the brute force code:
- e_d(u, v) = |L(u, v) - R(max(u - d, 0), v)| (or its square): the cost of
  one pixel. A right column left of the image takes the value of column 0.
- The window cost S_d(u, v) is the sum of e_d over the (2r + 1) x (2r + 1)
  window centered on (u, v), where a position outside the image takes the
  value of e_d at the nearest border pixel (the coordinates are clamped).
- The disparity of (u, v) is the least d in [0, D) with the least S_d(u, v).
"""

from __future__ import annotations

from typing import List, Sequence


def _clamp(x: int, lo: int, hi: int) -> int:
    return lo if x < lo else hi if x > hi else x


def pixel_cost(left: Sequence[Sequence[int]], right: Sequence[Sequence[int]],
               d: int, squared: bool = False) -> List[List[int]]:
    """The image e_d of the costs of single pixels at disparity d."""
    h, w = len(left), len(left[0])
    out = []
    for v in range(h):
        lrow, rrow = left[v], right[v]
        row = []
        for u in range(w):
            x = lrow[u] - rrow[u - d if u >= d else 0]
            row.append(x * x if squared else abs(x))
        out.append(row)
    return out


def padded_integral(e: Sequence[Sequence[int]], r: int) -> List[List[int]]:
    """The integral image S of e padded by r pixels on each side by
    copying the border. S has (H + 2r + 1) rows and (W + 2r + 1) columns,
    and S[y][x] is the sum of the padded image over rows < y and columns
    < x."""
    h, w = len(e), len(e[0])
    ph, pw = h + 2 * r, w + 2 * r
    S = [[0] * (pw + 1) for _ in range(ph + 1)]
    for y in range(ph):
        src = e[_clamp(y - r, 0, h - 1)]
        acc = 0
        above, cur = S[y], S[y + 1]
        for x in range(pw):
            acc += src[_clamp(x - r, 0, w - 1)]
            cur[x + 1] = above[x + 1] + acc
    return S


def block_match(left: Sequence[Sequence[int]], right: Sequence[Sequence[int]],
                D: int, r: int, squared: bool = False) -> List[List[int]]:
    """The disparity map of block matching with a (2r + 1) x (2r + 1)
    window and D disparities, in Theta(W H D) time."""
    if D < 1 or r < 0:
        raise ValueError("need D >= 1 and r >= 0")
    h, w = len(left), len(left[0])
    k = 2 * r + 1
    best = [[None] * w for _ in range(h)]  # @line L1
    disp = [[0] * w for _ in range(h)]  # @line L1
    for d in range(D):  # @line L2
        e = pixel_cost(left, right, d, squared)  # @line L3
        S = padded_integral(e, r)  # @line L4
        for v in range(h):  # @line L5
            top, bot = S[v], S[v + k]
            brow, drow = best[v], disp[v]
            for u in range(w):  # @line L5
                c = bot[u + k] - top[u + k] - bot[u] + top[u]  # @line L6
                if brow[u] is None or c < brow[u]:  # @line L7
                    brow[u] = c  # @line L7
                    drow[u] = d  # @line L7
    return disp  # @line L8


def window_cost(left: Sequence[Sequence[int]], right: Sequence[Sequence[int]],
                u: int, v: int, d: int, r: int, squared: bool = False) -> int:
    """S_d(u, v) by the definition, in Theta(r^2) time."""
    h, w = len(left), len(left[0])
    s = 0
    for dv in range(-r, r + 1):
        y = _clamp(v + dv, 0, h - 1)
        for du in range(-r, r + 1):
            x = _clamp(u + du, 0, w - 1)
            diff = left[y][x] - right[y][x - d if x >= d else 0]
            s += diff * diff if squared else abs(diff)
    return s


def block_match_brute(left: Sequence[Sequence[int]], right: Sequence[Sequence[int]],
                      D: int, r: int, squared: bool = False) -> List[List[int]]:
    """The same disparity map by the definition, in Theta(W H D r^2) time."""
    h, w = len(left), len(left[0])
    out = []
    for v in range(h):
        row = []
        for u in range(w):
            costs = [window_cost(left, right, u, v, d, r, squared) for d in range(D)]
            row.append(costs.index(min(costs)))
        out.append(row)
    return out
