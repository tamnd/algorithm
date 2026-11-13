# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-maximum-suppression/. The authors are listed in prov/9SMADY.jsonl.

"""Non-maximum suppression of a gradient field along the quantized gradient direction.

The input is two images gx and gy of the same size (lists of rows), with
pixel (x, y) at [y][x], x to the right and y downward. Values may be int
or float; with int inputs every decision is exact. The output keeps the
squared magnitude gx^2 + gy^2 at the pixels that survive and holds 0 elsewhere.
Pixels on the image border never survive.
"""

Number = int | float
Grid = list[list[Number]]

# The neighbor step d for each of the four direction sectors: 0, 45, 90 and 135 degrees.
STEPS = ((1, 0), (1, 1), (0, 1), (-1, 1))


def sector(gx: Number, gy: Number) -> int:
    """Return 0, 1, 2 or 3 for a gradient direction nearest to 0, 45, 90 or 135 degrees.

    The angle a of (gx, gy) is below 22.5 degrees from the x axis exactly when
    |gy| < tan(22.5 deg) |gx| = (2^(1/2) - 1) |gx|, that is when
    (|gx| + |gy|)^2 < 2 gx^2. The test uses only products, so it is exact on integers.
    """
    ax, ay = abs(gx), abs(gy)
    s = (ax + ay) * (ax + ay)
    if s < 2 * ax * ax:
        return 0
    if s < 2 * ay * ay:
        return 2
    return 1 if gx * gy > 0 else 3


def non_maximum_suppression(gx: Grid, gy: Grid) -> Grid:
    """Keep m(p) = gx^2 + gy^2 where m(p) > m(p - d) and m(p) >= m(p + d) along the sector step d."""
    h = len(gx)
    w = len(gx[0]) if h else 0
    m = [[gx[y][x] * gx[y][x] + gy[y][x] * gy[y][x] for x in range(w)] for y in range(h)]  # @line L1
    out: Grid = [[0] * w for _ in range(h)]
    for y in range(1, h - 1):  # @line L2
        for x in range(1, w - 1):
            mp = m[y][x]
            if mp == 0:  # @line L3
                continue
            dx, dy = STEPS[sector(gx[y][x], gy[y][x])]  # @line L4
            back = m[y - dy][x - dx]  # @line L5
            ahead = m[y + dy][x + dx]
            if mp > back and mp >= ahead:  # @line L6
                out[y][x] = mp  # @line L7
    return out
