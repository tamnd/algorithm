# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beier-neely-morphing/. The authors are listed in prov/QXNMEN.jsonl.
"""Feature-based image metamorphosis (Beier and Neely 1992).

Points are (x, y) tuples, with x the column and y the row of a pixel. An
image is a list of rows of numbers. A line is a pair (P, Q) of points. The
warp is a reverse map: for each pixel X of the destination image, it finds the
point X' of the source image to sample. Line i of the destination is
(P_i, Q_i) and the matching line of the source is (P'_i, Q'_i). For one line,

    u = (X - P) . (Q - P) / |Q - P|^2,
    v = (X - P) . perp(Q - P) / |Q - P|,
    X' = P' + u (Q' - P') + v perp(Q' - P') / |Q' - P'|,

where perp(x, y) = (-y, x). For several lines, the displacements X'_i - X are
averaged with the weights (length^p / (a + dist))^b, where dist is the
distance from X to the segment P_i Q_i. A morph at the time t interpolates
the line endpoints, warps both images to the interpolated lines and
cross-dissolves the two warped images.
"""

import math


def perp(v):
    """Return v turned by 90 degrees, with the same length."""
    return (-v[1], v[0])


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def warp_point(x, dst_lines, src_lines, a=1e-3, b=1.0, p=0.0):
    """Return the source point X' for the destination point x.

    dst_lines and src_lines are lists of matching lines (P, Q). a > 0
    keeps the weights finite; with a = 0 a point on a line maps exactly
    to the matching point of the source line.
    """
    if len(dst_lines) != len(src_lines) or not dst_lines:
        raise ValueError("need the same positive number of destination and source lines")
    dx = dy = 0.0  # @line L1
    wsum = 0.0
    for (p0, q0), (p1, q1) in zip(dst_lines, src_lines):  # @line L2
        d = _sub(q0, p0)
        dd = _dot(d, d)
        if dd == 0.0:
            raise ValueError("a destination line has zero length")
        e = _sub(q1, p1)
        ee = math.sqrt(_dot(e, e))
        if ee == 0.0:
            raise ValueError("a source line has zero length")
        xp = _sub(x, p0)
        length = math.sqrt(dd)
        u = _dot(xp, d) / dd  # @line L3
        v = _dot(xp, perp(d)) / length  # @line L4
        pe = perp(e)
        xs = (p1[0] + u * e[0] + v * pe[0] / ee, p1[1] + u * e[1] + v * pe[1] / ee)  # @line L5
        if u <= 0.0:  # @line L6
            dist = math.sqrt(_dot(xp, xp))
        elif u >= 1.0:
            xq = _sub(x, q0)
            dist = math.sqrt(_dot(xq, xq))
        else:
            dist = abs(v)
        if a + dist == 0.0:
            return xs
        w = (length**p / (a + dist)) ** b  # @line L7
        dx += w * (xs[0] - x[0])  # @line L8
        dy += w * (xs[1] - x[1])
        wsum += w
    return (x[0] + dx / wsum, x[1] + dy / wsum)  # @line L9


def sample_bilinear(img, x, y):
    """Bilinear sample of img at (x, y), with the coordinates clamped to the image."""
    h, w = len(img), len(img[0])
    x = min(max(x, 0.0), w - 1.0)
    y = min(max(y, 0.0), h - 1.0)
    x0, y0 = min(int(x), w - 2) if w > 1 else 0, min(int(y), h - 2) if h > 1 else 0
    fx, fy = x - x0, y - y0
    x1, y1 = min(x0 + 1, w - 1), min(y0 + 1, h - 1)
    top = (1 - fx) * img[y0][x0] + fx * img[y0][x1]
    bottom = (1 - fx) * img[y1][x0] + fx * img[y1][x1]
    return (1 - fy) * top + fy * bottom


def warp_image(src, src_lines, dst_lines, a=1e-3, b=1.0, p=0.0):
    """Return the image of the size of src whose lines dst_lines show the features of src_lines in src."""
    h, w = len(src), len(src[0])
    out = []
    for yy in range(h):
        row = []
        for xx in range(w):
            sx, sy = warp_point((float(xx), float(yy)), dst_lines, src_lines, a, b, p)
            row.append(sample_bilinear(src, sx, sy))
        out.append(row)
    return out


def interpolate_lines(lines0, lines1, t):
    """Return the lines with the endpoints (1 - t) L0 + t L1."""
    out = []
    for (p0, q0), (p1, q1) in zip(lines0, lines1):
        out.append(
            (
                ((1 - t) * p0[0] + t * p1[0], (1 - t) * p0[1] + t * p1[1]),
                ((1 - t) * q0[0] + t * q1[0], (1 - t) * q0[1] + t * q1[1]),
            )
        )
    return out


def morph(img0, img1, lines0, lines1, t, a=1e-3, b=1.0, p=0.0):
    """Return the frame of the morph from img0 to img1 at the time t in [0, 1]."""
    if len(img0) != len(img1) or len(img0[0]) != len(img1[0]):
        raise ValueError("the two images must have the same size")
    lines_t = interpolate_lines(lines0, lines1, t)  # @line L10
    h, w = len(img0), len(img0[0])
    out = []
    for yy in range(h):  # @line L11
        row = []
        for xx in range(w):
            x = (float(xx), float(yy))
            s0 = warp_point(x, lines_t, lines0, a, b, p)  # @line L12
            s1 = warp_point(x, lines_t, lines1, a, b, p)
            c0 = sample_bilinear(img0, s0[0], s0[1])
            c1 = sample_bilinear(img1, s1[0], s1[1])
            row.append((1 - t) * c0 + t * c1)  # @line L13
        out.append(row)
    return out  # @line L14
