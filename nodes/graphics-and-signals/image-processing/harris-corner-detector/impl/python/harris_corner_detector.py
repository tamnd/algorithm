# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harris-corner-detector/. The authors are listed in prov/824PAC.jsonl.

"""Harris corner detector with exact integer arithmetic.

An image is a list of H rows of W numbers (one channel, any range, int or
Fraction); pixel (x, y) is img[y][x]. The border rule is clamp: a read
outside the image takes the nearest edge pixel. The gradients are the
central differences X = I(x + 1, y) - I(x - 1, y) and
Y = I(x, y + 1) - I(x, y - 1), so they are not divided by 2.

The structure tensor at a pixel is M = [[A, C], [C, B]] with
A = sum w X^2, B = sum w Y^2, C = sum w X Y over a window with binomial
weights (1, 2, 1 for radius 1). The response is R = det M - k (tr M)^2.
"""

import math
from fractions import Fraction


def binomial_row(radius):
    """Row radius of Pascal's triangle with 2 radius + 1 entries: (1, 2, 1) for radius 1."""
    row = [1]
    for _ in range(2 * radius):
        row = [a + b for a, b in zip([0] + row, row + [0])]
    return row


def _clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v


def gradients(img):
    """Return (X, Y) with integer central differences and the clamp border rule."""
    h, w = len(img), len(img[0])
    gx = [[img[y][_clamp(x + 1, 0, w - 1)] - img[y][_clamp(x - 1, 0, w - 1)] for x in range(w)] for y in range(h)]
    gy = [[img[_clamp(y + 1, 0, h - 1)][x] - img[_clamp(y - 1, 0, h - 1)][x] for x in range(w)] for y in range(h)]
    return gx, gy


def _window_sum(field, weights):
    """Separable weighted sum with the clamp border rule: rows first, then columns."""
    h, w = len(field), len(field[0])
    r = len(weights) // 2
    tmp = [[sum(weights[i] * field[y][_clamp(x + i - r, 0, w - 1)] for i in range(len(weights)))
             for x in range(w)] for y in range(h)]
    return [[sum(weights[j] * tmp[_clamp(y + j - r, 0, h - 1)][x] for j in range(len(weights)))
             for x in range(w)] for y in range(h)]


def structure_tensor(img, radius=1):
    """Return the tables (A, B, C) of the windowed structure tensor."""
    gx, gy = gradients(img)  # @line L1
    wts = binomial_row(radius)
    xx = [[a * a for a in r] for r in gx]  # @line L2
    yy = [[b * b for b in r] for r in gy]
    xy = [[a * b for a, b in zip(ra, rb)] for ra, rb in zip(gx, gy)]
    return _window_sum(xx, wts), _window_sum(yy, wts), _window_sum(xy, wts)  # @line L3


def harris_response(img, k=Fraction(1, 25), radius=1):
    """R = A B - C^2 - k (A + B)^2 per pixel. Exact when the input and k are int or Fraction."""
    a, b, c = structure_tensor(img, radius)
    h, w = len(img), len(img[0])
    out = []
    for y in range(h):  # @line L4
        out.append([a[y][x] * b[y][x] - c[y][x] * c[y][x] - k * (a[y][x] + b[y][x]) ** 2  # @line L5
                    for x in range(w)])
    return out


def shi_tomasi_response(img, radius=1):
    """The smaller eigenvalue of M, (A + B) / 2 - sqrt(((A - B) / 2)^2 + C^2), as a float."""
    a, b, c = structure_tensor(img, radius)
    h, w = len(img), len(img[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            aa, bb, cc = a[y][x], b[y][x], c[y][x]
            row.append((aa + bb) / 2 - math.sqrt(((aa - bb) / 2) ** 2 + cc * cc))
        out.append(row)
    return out


def local_maxima(resp, threshold=0):
    """Pixels (x, y) with resp > threshold and resp greater than each of the 8 neighbours inside the image."""
    h, w = len(resp), len(resp[0])
    found = []  # @line L6
    for y in range(h):
        for x in range(w):
            v = resp[y][x]
            if not v > threshold:  # @line L7
                continue
            ok = True
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if (dx or dy) and 0 <= x + dx < w and 0 <= y + dy < h and resp[y + dy][x + dx] >= v:  # @line L8
                        ok = False
            if ok:
                found.append((x, y))  # @line L9
    return found  # @line L10


def harris_corners(img, k=Fraction(1, 25), radius=1, threshold=0):
    """Corners: strict 8-neighbour maxima of R that are above threshold (threshold >= 0)."""
    return local_maxima(harris_response(img, k, radius), threshold)
