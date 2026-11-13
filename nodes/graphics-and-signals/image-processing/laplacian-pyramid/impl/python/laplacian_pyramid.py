# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplacian-pyramid/. The authors are listed in prov/KYWMGX.jsonl.

"""Laplacian pyramid of Burt and Adelson, with exact reconstruction.

An image is a list of rows; pixel (x, y) is row y, column x. REDUCE blurs
with the separable 5-tap kernel w and keeps the even rows and columns, so a
level of width W gives one of width ceil(W / 2). EXPAND puts the coarse
samples on the even positions of a zero grid of the finer size and blurs
with 2 w in each direction. Both use the reflect-101 border. With int or
Fraction values and a Fraction kernel, every step is exact.
"""

from fractions import Fraction


def burt_adelson_kernel(a) -> list[Fraction]:
    """w(-2..2) = [1/4 - a/2, 1/4, a, 1/4, 1/4 - a/2]."""
    a = Fraction(a)
    c = Fraction(1, 4) - a / 2
    return [c, Fraction(1, 4), a, Fraction(1, 4), c]


def reflect101(i: int, n: int) -> int:
    """Mirror an index into 0 .. n - 1 without repeating the edge sample."""
    if n == 1:
        return 0
    period = 2 * n - 2
    i %= period
    return period - i if i >= n else i


def reduce_level(g: list[list], w: list) -> list[list]:
    """Blur with w(m) w(n) and keep the samples at even indices."""
    h, wd = len(g), len(g[0])
    w2, h2 = (wd + 1) // 2, (h + 1) // 2
    rows = [[sum(w[m + 2] * r[reflect101(2 * i + m, wd)] for m in range(-2, 3)) for i in range(w2)] for r in g]
    return [[sum(w[n + 2] * rows[reflect101(2 * j + n, h)][i] for n in range(-2, 3)) for i in range(w2)] for j in range(h2)]


def gaussian_pyramid(image: list[list], w: list) -> list[list[list]]:
    """G_0 = image, G_(l+1) = REDUCE(G_l), down to a 1 x 1 level."""
    pyr = [[list(r) for r in image]]
    while len(pyr[-1]) > 1 or len(pyr[-1][0]) > 1:
        pyr.append(reduce_level(pyr[-1], w))
    return pyr


def expand(g: list[list], width: int, height: int, w: list) -> list[list]:
    """EXPAND g to width x height: zeros between samples, then blur with 2 w per axis."""
    z = [[0] * width for _ in range(height)]  # @line L1
    for j, row in enumerate(g):
        for i, v in enumerate(row):
            z[2 * j][2 * i] = v
    # An axis of length 1 has no zeros to fill, so EXPAND leaves it as it is.
    gx = 1 if width == 1 else 2
    gy = 1 if height == 1 else 2
    r = [[sum(gx * w[m + 2] * zr[reflect101(x - m, width)] for m in range(-2, 3)) for x in range(width)] for zr in z]  # @line L2
    e = [[sum(gy * w[n + 2] * r[reflect101(y - n, height)][x] for n in range(-2, 3)) for x in range(width)] for y in range(height)]  # @line L3
    return e  # @line L4


def subtract(a: list[list], b: list[list]) -> list[list]:
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def add(a: list[list], b: list[list]) -> list[list]:
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def laplacian_pyramid(image: list[list], w: list, expand_fn=expand, levels=None) -> list[list[list]]:
    """Return [L_0, ..., L_N] with L_l = G_l - EXPAND(G_(l+1)) and L_N = G_N.

    expand_fn may be any deterministic function (g, width, height, w) -> image;
    reconstruct must get the same one. levels may give the Gaussian levels.
    """
    gp = levels if levels is not None else gaussian_pyramid(image, w)  # @line L5
    lap = []
    for lvl in range(len(gp) - 1):  # @line L6
        fine = gp[lvl]
        lap.append(subtract(fine, expand_fn(gp[lvl + 1], len(fine[0]), len(fine), w)))
    lap.append(gp[-1])  # @line L7
    return lap  # @line L8


def reconstruct(lap: list[list[list]], w: list, expand_fn=expand) -> list[list]:
    """Undo laplacian_pyramid: g = L_N, then g = L_l + EXPAND(g) for l = N - 1 down to 0."""
    g = lap[-1]  # @line L9
    for lvl in range(len(lap) - 2, -1, -1):  # @line L10
        band = lap[lvl]
        g = add(band, expand_fn(g, len(band[0]), len(band), w))
    return g  # @line L11
