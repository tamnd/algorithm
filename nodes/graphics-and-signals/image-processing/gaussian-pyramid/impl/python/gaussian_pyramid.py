# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-pyramid/. The authors are listed in prov/5RH4SA.jsonl.

"""Gaussian pyramid with the Burt and Adelson 5-tap kernel.

An image is a list of rows. Pixel (x, y) is row y, column x, with its center
at (x + 1/2, y + 1/2). Values may be int or Fraction; the code does exact
arithmetic when the kernel is made of Fractions. REDUCE blurs with the
separable kernel and keeps the samples at even indices, so a level of
width W gives a level of width ceil(W / 2). The border rule is reflect-101:
index -1 reads index 1, and index W reads index W - 2.
"""

from fractions import Fraction


def burt_adelson_kernel(a) -> list[Fraction]:
    """The 5-tap generating kernel w(-2..2) with w(0) = a and equal contribution.

    Equal contribution means w(0) + 2 w(2) = 2 w(1), which with a sum of 1 gives
    w(1) = 1/4 and w(2) = 1/4 - a/2. a = 3/8 is the binomial [1, 4, 6, 4, 1] / 16.
    """
    a = Fraction(a)
    c = Fraction(1, 4) - a / 2
    return [c, Fraction(1, 4), a, Fraction(1, 4), c]


def reflect101(i: int, n: int) -> int:
    """Map any integer index to 0 .. n - 1 by mirror reflection without repeating the edge."""
    if n == 1:
        return 0
    period = 2 * n - 2
    i %= period
    return period - i if i >= n else i


def reduce_level(g: list[list], w: list) -> list[list]:
    """One REDUCE step: blur with w(m) w(n) and keep the even rows and columns."""
    h, wd = len(g), len(g[0])
    w2, h2 = (wd + 1) // 2, (h + 1) // 2  # @line L1
    rows = []
    for y in range(h):  # @line L2
        row = g[y]
        rows.append([sum(w[m + 2] * row[reflect101(2 * i + m, wd)] for m in range(-2, 3)) for i in range(w2)])  # @line L3
    out = []
    for j in range(h2):  # @line L4
        out.append([sum(w[n + 2] * rows[reflect101(2 * j + n, h)][i] for n in range(-2, 3)) for i in range(w2)])  # @line L5
    return out  # @line L6


def gaussian_pyramid(image: list[list], w: list, levels: int | None = None) -> list[list[list]]:
    """Return [G_0, G_1, ...]. Stop at a 1 x 1 level, or after `levels` levels when given."""
    pyr = [[list(r) for r in image]]  # @line L7
    while len(pyr[-1]) > 1 or len(pyr[-1][0]) > 1:  # @line L8
        if levels is not None and len(pyr) == levels:
            break
        pyr.append(reduce_level(pyr[-1], w))  # @line L9
    return pyr  # @line L10


def level_sizes(width: int, height: int) -> list[tuple[int, int]]:
    """The (width, height) of each level down to 1 x 1, with ceil halving."""
    sizes = [(width, height)]
    while sizes[-1] != (1, 1):
        x, y = sizes[-1]
        sizes.append(((x + 1) // 2, (y + 1) // 2))
    return sizes


def total_samples(width: int, height: int) -> int:
    """The number of samples in all levels together."""
    return sum(x * y for x, y in level_sizes(width, height))


def to_level_zero(x: int, y: int, level: int) -> tuple[int, int]:
    """Sample (x, y) of level l sits on sample (2^l x, 2^l y) of level 0."""
    return x << level, y << level
