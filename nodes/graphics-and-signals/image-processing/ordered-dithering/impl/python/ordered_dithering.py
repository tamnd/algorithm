# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ordered-dithering/. The authors are listed in prov/ZXEC5M.jsonl.

"""Ordered dithering with a Bayer index matrix.

The Bayer matrix of side n = 2^K holds each of 0, ..., n^2 - 1 once. It is
built from M_1 = [[0]] by M_2s[y][x] = 4 M_s[y mod s][x mod s] + D[y div s][x div s]
with D = [[0, 2], [3, 1]], which gives the blocks [[4M, 4M + 2], [4M + 3, 4M + 1]].
The image is a list of rows of values in [0, 1]. Pixel (x, y) is set to 1 when
its value is above the threshold (M[y mod n][x mod n] + 1/2) / n^2, and to 0
otherwise.
"""

from fractions import Fraction

D = ((0, 2), (3, 1))


def bayer(n):
    """The Bayer index matrix of side n, a power of two, as a list of rows."""
    m, s = [[0]], 1  # @line L1
    while s < n:  # @line L2
        m = [[4 * m[y % s][x % s] + D[y // s][x // s] for x in range(2 * s)] for y in range(2 * s)]  # @line L3
        s *= 2
    return m


def thresholds(n):
    """The threshold matrix (M + 1/2) / n^2."""
    return [[Fraction(2 * v + 1, 2 * n * n) for v in row] for row in bayer(n)]  # @line L4


def ordered_dither(image, n):
    t = thresholds(n)
    out = []
    for y, row in enumerate(image):  # @line L5
        out.append([1 if v > t[y % n][x % n] else 0 for x, v in enumerate(row)])  # @line L6
    return out  # @line L7
