# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/drizzle/. The authors are listed in prov/GWCHWD.jsonl.
"""Drizzle (variable-pixel linear reconstruction) for shifted frames.

Coordinates: an input pixel (i, j) of a frame covers the unit square
[j, j + 1] x [i, i + 1] of its own frame (x along the columns, y along the
rows). A frame with the shift (dx, dy) puts that square at
[j + dx, j + 1 + dx] x [i + dy, i + 1 + dy] in the output frame. The output
grid has pixels of side s (in input pixel units): output pixel (I, J) covers
[J s, (J + 1) s] x [I s, (I + 1) s].

Each input pixel is shrunk to a drop: a square of side p (the pixfrac times the
input pixel side) with the same center. The drop adds its value, times its
overlap area and its weight, to each output pixel it overlaps.

The values of an input frame are counts per input pixel. The output is in
counts per output pixel: I_o = s^2 (sum a w d) / (sum a w). Works with float
and with fractions.Fraction values; with Fractions all results are exact.
"""

import math


def overlap_1d(a0, a1, b0, b1):
    """The length of the intersection of the intervals [a0, a1] and [b0, b1]."""
    lo = a0 if a0 > b0 else b0
    hi = a1 if a1 < b1 else b1
    return hi - lo if hi > lo else 0 * (hi - lo)


def drop_footprint(i, j, shift, p):
    """The drop of input pixel (i, j) in the output frame: (x0, x1, y0, y1)."""
    dx, dy = shift
    mid = (1 + 0 * p) / 2  # 1/2, a Fraction when p is a Fraction
    cx = j + dx + mid
    cy = i + dy + mid
    half = p / 2
    return cx - half, cx + half, cy - half, cy + half


def drizzle(frames, shifts, s, p, out_shape, weights=None):
    """Drizzle the frames onto an output grid of out_shape = (M1, M2) pixels of side s.

    frames is a list of images; shifts[k] = (dx, dy) places frame k in the
    output frame; p is the drop side (pixfrac, in input pixel units);
    weights[k] is an optional weight image for frame k (0 marks a bad pixel).
    Returns (I, W): the output image in counts per output pixel, and the
    weight image W_o = sum a w. An output pixel with W_o = 0 gets the value 0.
    """
    m1, m2 = out_shape
    zero = 0 * s
    wsum = [[zero] * m2 for _ in range(m1)]  # @line L1
    vsum = [[zero] * m2 for _ in range(m1)]  # @line L1
    for k, frame in enumerate(frames):  # @line L2
        wk = weights[k] if weights is not None else None
        for i, row in enumerate(frame):  # @line L2
            for j, d in enumerate(row):  # @line L2
                w = 1 if wk is None else wk[i][j]
                if w == 0:
                    continue
                x0, x1, y0, y1 = drop_footprint(i, j, shifts[k], p)  # @line L3
                jlo = max(0, math.floor(x0 / s))  # @line L4
                jhi = min(m2 - 1, math.ceil(x1 / s) - 1)  # @line L4
                ilo = max(0, math.floor(y0 / s))  # @line L4
                ihi = min(m1 - 1, math.ceil(y1 / s) - 1)  # @line L4
                for oi in range(ilo, ihi + 1):  # @line L4
                    ly = overlap_1d(y0, y1, oi * s, (oi + 1) * s)
                    if ly == 0:
                        continue
                    for oj in range(jlo, jhi + 1):  # @line L4
                        lx = overlap_1d(x0, x1, oj * s, (oj + 1) * s)
                        if lx == 0:
                            continue
                        a = lx * ly  # @line L5
                        wsum[oi][oj] += a * w  # @line L6
                        vsum[oi][oj] += a * w * d  # @line L6
    s2 = s * s
    out = [[zero] * m2 for _ in range(m1)]
    for oi in range(m1):  # @line L7
        for oj in range(m2):  # @line L7
            if wsum[oi][oj] != 0:  # @line L8
                out[oi][oj] = s2 * vsum[oi][oj] / wsum[oi][oj]  # @line L8
    return out, wsum  # @line L9


def shift_and_add(frames, shifts, out_shape):
    """Place each pixel of each frame at the output pixel of its shifted position and average.

    The shifts must be integers. This is drizzle with s = p = 1.
    """
    m1, m2 = out_shape
    tot = [[0] * m2 for _ in range(m1)]
    cnt = [[0] * m2 for _ in range(m1)]
    for frame, (dx, dy) in zip(frames, shifts):
        for i, row in enumerate(frame):
            for j, d in enumerate(row):
                oi, oj = i + dy, j + dx
                if 0 <= oi < m1 and 0 <= oj < m2:
                    tot[oi][oj] += d
                    cnt[oi][oj] += 1
    return [[tot[i][j] / cnt[i][j] if cnt[i][j] else 0 * tot[i][j] for j in range(m2)] for i in range(m1)]


def total_flux(img, weights=None):
    """sum_o W_o I_o, or sum_o I_o if no weights are given."""
    if weights is None:
        return sum(v for row in img for v in row)
    return sum(w * v for rw, rv in zip(weights, img) for w, v in zip(rw, rv))
