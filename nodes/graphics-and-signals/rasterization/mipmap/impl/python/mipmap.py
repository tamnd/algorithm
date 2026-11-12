# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mipmap/. The authors are listed in prov/6V0FBJ.jsonl.

"""A mipmap: the chain of 2x2 box-filtered levels of a texture, with trilinear lookup.

A texture is H rows of W texels, texture[t][s], each texel a tuple of linear
channel values. W and H are powers of two. Level 0 is the texture; level k has
max(1, W >> k) columns and max(1, H >> k) rows. Texel (s, t) of any level has
its center at (s + 1/2, t + 1/2) in the texel units of that level, so the same
normalized coordinates (u, v) address every level. Lookups clamp to the edge.
Use fractions.Fraction values for exact results.
"""

import math
from fractions import Fraction
from typing import List, Sequence, Union

Num = Union[int, float, Fraction]
Texel = tuple
Image = List[List[Texel]]


def _is_power_of_two(n: int) -> bool:
    return n >= 1 and n & (n - 1) == 0


def mipmap(texture: Sequence[Sequence[Texel]]) -> List[Image]:
    """Build the mipmap levels M[0..L] of the texture by 2x2 box averages.

    Precondition: W and H are powers of two and all texels have the same
    channel count. Cost: Theta(W H c) time for c channels, and fewer than
    2 W H texels in total (exactly (4 W H - 1)/3 when W = H).
    """
    h0, w0 = len(texture), len(texture[0])
    if not (_is_power_of_two(w0) and _is_power_of_two(h0)):
        raise ValueError("the texture sides must be powers of two")
    levels: List[Image] = [[list(row) for row in texture]]  # @line L1
    while len(levels[-1]) > 1 or len(levels[-1][0]) > 1:  # @line L2
        prev = levels[-1]
        ph, pw = len(prev), len(prev[0])
        w, h = max(1, pw // 2), max(1, ph // 2)  # @line L3
        cur: Image = []
        for t in range(h):  # @line L4
            rows = [r for r in (2 * t, 2 * t + 1) if r < ph]
            row: List[Texel] = []
            for s in range(w):
                cols = [c for c in (2 * s, 2 * s + 1) if c < pw]
                block = [prev[r][c] for r in rows for c in cols]
                row.append(_mean(block))  # @line L5
            cur.append(row)
        levels.append(cur)  # @line L6
    return levels  # @line L7


def _mean(block: Sequence[Texel]) -> Texel:
    """Channel-wise mean of 1, 2 or 4 texels; exact for int and Fraction values."""
    n = len(block)
    out = []
    for ch in zip(*block):
        if all(isinstance(x, (int, Fraction)) for x in ch):
            out.append(Fraction(sum(ch), n))
        else:
            out.append(sum(ch) / n)
    return tuple(out)


def _wrap(i: int, n: int) -> int:
    return min(max(i, 0), n - 1)


def bilinear(level: Sequence[Sequence[Texel]], u: Num, v: Num) -> Texel:
    """Bilinear lookup in one level at normalized (u, v), clamp to edge. Cost: 4 texel reads."""
    h, w = len(level), len(level[0])
    half = Fraction(1, 2) if isinstance(u, (int, Fraction)) and isinstance(v, (int, Fraction)) else 0.5
    x, y = u * w - half, v * h - half
    i0, j0 = math.floor(x), math.floor(y)
    a, b = x - i0, y - j0
    s0, s1, t0, t1 = _wrap(i0, w), _wrap(i0 + 1, w), _wrap(j0, h), _wrap(j0 + 1, h)
    return tuple(
        (1 - a) * (1 - b) * c00 + a * (1 - b) * c10 + (1 - a) * b * c01 + a * b * c11
        for c00, c10, c01, c11 in zip(level[t0][s0], level[t0][s1], level[t1][s0], level[t1][s1])
    )


def level_of_detail(dudx: float, dvdx: float, dudy: float, dvdy: float, width: int, height: int) -> float:
    """Return lambda = log2(rho), rho the larger footprint side in level 0 texels.

    The derivatives are those of the normalized coordinates per pixel step.
    """
    rho_x = math.hypot(dudx * width, dvdx * height)
    rho_y = math.hypot(dudy * width, dvdy * height)
    rho = max(rho_x, rho_y)
    return -math.inf if rho == 0 else math.log2(rho)


def trilinear(levels: Sequence[Image], u: Num, v: Num, lam: Num) -> Texel:
    """Trilinear lookup: blend bilinear lookups in levels floor(lam) and floor(lam) + 1.

    Precondition: levels is the output of mipmap. lam is the level of detail
    log2(rho). Cost: at most 8 texel reads, Theta(1) for a fixed channel count.
    """
    top = len(levels) - 1
    if lam <= 0:  # @line L8
        return bilinear(levels[0], u, v)  # @line L9
    if lam >= top:  # @line L10
        return bilinear(levels[top], u, v)  # @line L11
    d = math.floor(lam)  # @line L12
    f = lam - d
    lo, hi = bilinear(levels[d], u, v), bilinear(levels[d + 1], u, v)  # @line L13
    return tuple((1 - f) * p + f * q for p, q in zip(lo, hi))  # @line L14


def storage(levels: Sequence[Image]) -> int:
    """Return the number of texels in all levels."""
    return sum(len(level) * len(level[0]) for level in levels)
