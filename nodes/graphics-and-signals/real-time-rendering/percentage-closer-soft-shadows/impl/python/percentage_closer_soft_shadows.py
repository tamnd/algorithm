# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/percentage-closer-soft-shadows/. The authors are listed in prov/EXXNC3.jsonl.

"""Percentage-closer soft shadows (Fernando 2005).

The light is a square of side w_light in the plane d = 0 of the light frame,
centered on the light's axis. The shadow map is a perspective view from the
center of the light. It stores linear depth d (the distance along the light's
axis, not the nonlinear clip depth), and its image plane is the near plane at
d = n. A texel is a square of side h in near-plane units. The map s is a list
of rows of depths, s[j][i]; texel (i, j) has its center at (i + 1/2, j + 1/2)
in texel units. A receiver is given by its map position (x, y) in texels and
its depth d_r. Every function returns the lit fraction.
"""

from math import ceil, floor


def region(s, x, y, r):
    """The texels whose centers lie in the square of half-width r texels
    around (x, y). If there is none, the texel that holds (x, y)."""
    hh, ww = len(s), len(s[0])
    i0, i1 = max(ceil(x - r - 0.5), 0), min(floor(x + r - 0.5), ww - 1)
    j0, j1 = max(ceil(y - r - 0.5), 0), min(floor(y + r - 0.5), hh - 1)
    out = [(i, j) for j in range(j0, j1 + 1) for i in range(i0, i1 + 1)]
    if not out:
        i, j = min(max(floor(x), 0), ww - 1), min(max(floor(y), 0), hh - 1)
        out = [(i, j)]
    return out


def search_half_width(d_r, w_light, n, h):
    """Half-width in texels of the region that holds every possible blocker."""
    return w_light * (d_r - n) / (2 * d_r * h)


def blocker_search(s, x, y, d_r, w_light, n, h, bias):
    """The average depth and the count of the texels nearer than the receiver."""
    rs = search_half_width(d_r, w_light, n, h)  # @line L1
    found = [s[j][i] for i, j in region(s, x, y, rs) if s[j][i] < d_r - bias]  # @line L2
    if not found:
        return None, 0
    return sum(found) / len(found), len(found)  # @line L4


def penumbra_width(d_r, d_b, w_light):
    """The penumbra width at the receiver, for parallel planes."""
    return (d_r - d_b) * w_light / d_b  # @line L5


def pcf(s, x, y, d_r, r, bias):
    """Box PCF over the texels of the square of half-width r texels."""
    taps = region(s, x, y, r)
    lit = sum(1 for i, j in taps if d_r - bias <= s[j][i])
    return lit / len(taps)


def pcss(s, x, y, d_r, w_light, n, h, bias=0.0):
    d_b, count = blocker_search(s, x, y, d_r, w_light, n, h, bias)
    if count == 0:  # @line L3
        return 1.0
    w_p = penumbra_width(d_r, d_b, w_light)
    rf = w_p * n / (2 * d_r * h)  # @line L6
    return pcf(s, x, y, d_r, rf, bias)  # @line L7


def flatland_map(width, h, n, d_b, d_r, rows=3):
    """A map of a half-plane blocker at depth d_b over x < 0 above a receiver
    plane at depth d_r. The map is centered on the light's axis, so texel i
    covers [(i - width/2) h, (i - width/2 + 1) h] on the near plane."""
    row = [d_b if (i - width / 2 + 0.5) * h < 0 else d_r for i in range(width)]
    return [row[:] for _ in range(rows)]


def exact_visibility(xw, d_b, d_r, w_light):
    """The visible fraction of the light segment from the receiver point at
    world position xw, for the half-plane blocker x < 0 at depth d_b."""
    lo = -xw * d_b / (d_r - d_b)  # the light points with x >= lo are visible
    return min(max((w_light / 2 - lo) / w_light, 0.0), 1.0)
