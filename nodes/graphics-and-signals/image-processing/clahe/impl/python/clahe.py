# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clahe/. The authors are listed in prov/KNVCNG.jsonl.

"""Contrast-limited adaptive histogram equalization (CLAHE).

The image is a list of rows of integers in 0 .. levels - 1. It is cut into
nx by ny tiles of equal size. Each tile gets a histogram, clipped at a limit,
and an equalization table. Each pixel takes a bilinear blend of the tables of
the four nearest tile centers, which the code computes in exact integers.
"""

import math


def clip_histogram(hist: list[int], limit: int) -> list[int]:
    """Clip each bin at limit and spread the excess over all bins.

    Each bin gets q = E // L more counts, and r = E mod L bins spread over
    the range get one more, so the total count is unchanged. A bin can end
    above the limit by at most q + 1. Cost: O(L).
    """
    levels = len(hist)
    excess = sum(max(v - limit, 0) for v in hist)  # @line L4
    out = [min(v, limit) for v in hist]
    q, r = divmod(excess, levels)  # @line L5
    out = [v + q for v in out]
    for m in range(r):  # @line L6
        out[m * levels // r] += 1
    return out


def equalization_table(hist: list[int]) -> list[int]:
    """T[k] = round((L - 1) c(k) / n) with halves up, where c is the cumulative sum."""
    levels, n = len(hist), sum(hist)
    table, c = [0] * levels, 0
    for k in range(levels):
        c += hist[k]
        table[k] = (2 * (levels - 1) * c + n) // (2 * n)
    return table


def clip_limit(alpha: float, tile_pixels: int, levels: int) -> int:
    """beta = max(1, floor(alpha * n / L)); alpha = math.inf means no clipping."""
    if math.isinf(alpha):
        return tile_pixels
    return max(1, math.floor(alpha * tile_pixels / levels))


def _axis(x: int, size: int, count: int) -> tuple[int, int, int, int]:
    """Tiles a0, a1 around pixel x and the weight of a1 as num / den.

    The tile coordinate is u = (x + 1/2) / size - 1/2 = (2x + 1 - size) / (2 size).
    """
    num, den = 2 * x + 1 - size, 2 * size
    fl = num // den  # floor(u)
    s_num = num - fl * den  # s = u - floor(u) = s_num / den
    a0 = min(max(fl, 0), count - 1)
    a1 = min(max(fl + 1, 0), count - 1)
    return a0, a1, s_num, den


def clahe(
    image: list[list[int]],
    levels: int = 256,
    tiles_x: int = 8,
    tiles_y: int = 8,
    alpha: float = 4.0,
) -> list[list[int]]:
    """Return the CLAHE result.

    Precondition: the width is a multiple of tiles_x, the height is a multiple
    of tiles_y, each value is in 0 .. levels - 1, and alpha >= 1 (or math.inf
    for adaptive equalization with no clip). Cost: O(W H + tiles_x tiles_y L)
    time and O(tiles_x tiles_y L) extra space.
    """
    height, width = len(image), len(image[0]) if image else 0
    if height == 0 or width == 0:
        raise ValueError("the image has no pixels")
    if width % tiles_x or height % tiles_y:
        raise ValueError("the image size must be a multiple of the tile counts")
    tw, th = width // tiles_x, height // tiles_y
    n = tw * th
    beta = clip_limit(alpha, n, levels)
    tables = [[[0] * levels for _ in range(tiles_x)] for _ in range(tiles_y)]
    for b in range(tiles_y):  # @line L1
        for a in range(tiles_x):
            hist = [0] * levels  # @line L2
            for y in range(b * th, (b + 1) * th):
                for x in range(a * tw, (a + 1) * tw):
                    hist[image[y][x]] += 1
            limit = beta  # @line L3
            clipped = clip_histogram(hist, limit)
            tables[b][a] = equalization_table(clipped)  # @line L7
    out = [[0] * width for _ in range(height)]
    cols = [_axis(x, tw, tiles_x) for x in range(width)]
    rows = [_axis(y, th, tiles_y) for y in range(height)]
    for y in range(height):  # @line L8
        b0, b1, t_num, dy = rows[y]  # @line L9
        for x in range(width):
            a0, a1, s_num, dx = cols[x]  # @line L10
            g = image[y][x]  # @line L11
            total = (
                (dx - s_num) * (dy - t_num) * tables[b0][a0][g]
                + s_num * (dy - t_num) * tables[b0][a1][g]
                + (dx - s_num) * t_num * tables[b1][a0][g]
                + s_num * t_num * tables[b1][a1][g]
            )
            den = dx * dy
            out[y][x] = (2 * total + den) // (2 * den)  # @line L12
    return out  # @line L13
