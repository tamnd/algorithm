# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-tool-offset/. The authors are listed in prov/RAY63F.jsonl.

"""Inverse tool offset (ITO) on a height grid.

The part is a height field sampled on a square grid: f[i][j] is the height
of the part at (i d, j d), with grid spacing d. The tool points straight
down. Its shape is a function T(o) >= 0 for offsets o in its footprint: the
height of the tool surface above its tip at the horizontal offset o. A ball
end mill of radius r has T(o) = r - sqrt(r^2 - |o|^2), and a flat end mill
has T = 0 on its disk.

The cutter location of the tip at the grid point p is the lowest height at
which the tool touches no sample from above:

    Z[p] = max over samples q in the footprint of p of  f[q] - T(q - p).

The ITO method computes Z by scattering: it puts the tool upside down at each
sample q, so that its surface is the height f[q] - T(o) at p = q + o, and
keeps the highest value at each grid point, like a z-buffer. For a symmetric
tool, T(q - p) = T(p - q), so the scatter and the gather give the same Z.

Heights may be int, float or Fraction. With Fractions and a flat tool, every
step is exact.
"""

import math


def footprint(r, d):
    """The grid offsets (a, b) of the tool disk of radius r on a grid of spacing d."""
    if r <= 0 or d <= 0:
        raise ValueError("the radius and the spacing must be positive")
    k = int(r // d)
    return [(a, b) for a in range(-k, k + 1) for b in range(-k, k + 1) if (a * a + b * b) * d * d <= r * r]


def ball_tool(r, d):
    """The inverted ball end mill: offset -> height of the tool surface above the tip."""
    return {(a, b): r - math.sqrt(r * r - (a * a + b * b) * d * d) for a, b in footprint(r, d)}


def flat_tool(r, d):
    """The flat end mill: height 0 on the whole disk."""
    return {o: 0 for o in footprint(r, d)}


def inverse_tool_offset(f, tool):
    """Cutter location heights Z of the tool tip at every grid point, by scattering.

    A grid point whose footprint holds no sample keeps the value None, which
    cannot happen when the footprint holds the offset (0, 0).
    """
    nx, ny = len(f), len(f[0])
    z = [[None] * ny for _ in range(nx)]  # @line L1
    for i in range(nx):  # @line L2
        for j in range(ny):
            h = f[i][j]
            for (a, b), t in tool.items():  # @line L3
                p, q = i + a, j + b  # @line L4
                if 0 <= p < nx and 0 <= q < ny:
                    v = h - t
                    if z[p][q] is None or v > z[p][q]:  # @line L5
                        z[p][q] = v
    return z  # @line L6
