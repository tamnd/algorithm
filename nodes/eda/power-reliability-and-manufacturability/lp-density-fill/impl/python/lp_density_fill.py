# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lp-density-fill/. The authors are listed in prov/6QQEE4.jsonl.
"""Min-variation dummy fill on a fixed r-dissection, solved exactly as a linear program.

The layout is cut into an m by m grid of tiles. area[i][j] is the feature area in tile
(i, j) and slack[i][j] is the area in which fill may go. A window is an r by r block of
tiles, of area w2. The linear program is

    maximize M
    subject to  0 <= p[i][j] <= slack[i][j]                      for every tile,
                sum over W of p <= U * w2 - area(W)              for every window W,
                M - sum over W of p <= area(W)                   for every window W.

It is solved by a dense simplex method in exact rational arithmetic with Bland's rule.
All inputs may be ints or Fractions; outputs are Fractions.
"""

from fractions import Fraction


def windows(m, r):
    """The top-left tiles of all r by r blocks of an m by m grid."""
    return [(i, j) for i in range(m - r + 1) for j in range(m - r + 1)]


def window_tiles(i0, j0, r):
    return [(i, j) for i in range(i0, i0 + r) for j in range(j0, j0 + r)]


def simplex_max(c, A, b):
    """Maximize c.x subject to A x <= b and x >= 0, where every b_i >= 0.

    The origin is feasible, so the slack basis starts the method. Bland's rule
    (smallest index enters, smallest basic index leaves among ties) prevents cycling.
    Returns (value, x, y) where y is an optimal dual solution, or None if unbounded.
    """
    n, k = len(c), len(A)
    width = n + k + 1
    rows = []
    for i in range(k):
        row = [Fraction(v) for v in A[i]] + [Fraction(0)] * k + [Fraction(b[i])]
        row[n + i] = Fraction(1)
        rows.append(row)
    obj = [-Fraction(v) for v in c] + [Fraction(0)] * (k + 1)
    basis = [n + i for i in range(k)]
    while True:
        enter = next((j for j in range(n + k) if obj[j] < 0), None)
        if enter is None:
            break
        leave, best = None, None
        for i in range(k):
            a = rows[i][enter]
            if a > 0:
                ratio = rows[i][-1] / a
                if best is None or ratio < best or (ratio == best and basis[i] < basis[leave]):
                    leave, best = i, ratio
        if leave is None:
            return None
        piv = rows[leave]
        a = piv[enter]
        piv = [v / a for v in piv]
        rows[leave] = piv
        nz = [j for j in range(width) if piv[j] != 0]
        for i in range(k):
            if i != leave and rows[i][enter] != 0:
                f = rows[i][enter]
                row = rows[i]
                for j in nz:
                    row[j] -= f * piv[j]
        f = obj[enter]
        for j in nz:
            obj[j] -= f * piv[j]
        basis[leave] = enter
    x = [Fraction(0)] * n
    for i, v in enumerate(basis):
        if v < n:
            x[v] = rows[i][-1]
    y = [obj[n + i] for i in range(k)]
    return obj[-1], x, y


def build_lp(area, slack, r, U, w2):
    """The constraint matrix of the Min-Var program; variables are the tiles row by row, then M."""
    m = len(area)
    n = m * m + 1
    A, b = [], []
    for i in range(m):
        for j in range(m):
            row = [0] * n
            row[i * m + j] = 1
            A.append(row)
            b.append(Fraction(slack[i][j]))  # @line L4
    wins = windows(m, r)
    for i0, j0 in wins:
        tiles = window_tiles(i0, j0, r)
        feat = sum(Fraction(area[i][j]) for i, j in tiles)
        row = [0] * n
        for i, j in tiles:
            row[i * m + j] = 1
        A.append(row)
        b.append(Fraction(U) * w2 - feat)  # @line L5
    for i0, j0 in wins:
        tiles = window_tiles(i0, j0, r)
        feat = sum(Fraction(area[i][j]) for i, j in tiles)
        row = [0] * n
        for i, j in tiles:
            row[i * m + j] = -1
        row[-1] = 1
        A.append(row)
        b.append(feat)  # @line L6
    c = [0] * (n - 1) + [1]  # @line L3
    return c, A, b


def lp_density_fill(area, slack, r, U, w2):
    """Optimal min-variation fill on the fixed r-dissection.

    Returns (density, p) where density is the largest possible minimum window
    density and p[i][j] the fill area of each tile, or None if some window already
    has feature density above U.
    """
    m = len(area)
    for i0, j0 in windows(m, r):
        if sum(Fraction(area[i][j]) for i, j in window_tiles(i0, j0, r)) > Fraction(U) * w2:  # @line L1
            return None
    c, A, b = build_lp(area, slack, r, U, w2)  # @line L2
    value, x, _ = simplex_max(c, A, b)  # @line L7
    p = [[x[i * m + j] for j in range(m)] for i in range(m)]
    return value / Fraction(w2), p  # @line L8


def window_densities(area, p, r, w2):
    """The density of every fixed window under fill p."""
    m = len(area)
    return [sum(Fraction(area[i][j]) + p[i][j] for i, j in window_tiles(i0, j0, r)) / Fraction(w2) for i0, j0 in windows(m, r)]


def floating_error(r):
    """The largest density difference between a floating window and every fixed window (Theorem 8)."""
    return Fraction(1, r) - Fraction(1, 4 * r * r)
