# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometry-clipmaps/. The authors are listed in prov/03429S.jsonl.

"""Geometry clipmaps: nested square grids around the viewer.

Domain points are integer pairs (x, y) in units of the finest grid; the
height is a separate value. Level l has n x n vertices (n = 2^k - 1) with
spacing s_l = 2^l. Its window is the square of side (n - 1) s_l whose lower
corner, the origin, is a multiple of s_(l+1), so the grid of level l + 1 is
every other vertex of level l. Each level keeps its heights in an n x n
array with wraparound (toroidal) addressing.
"""

from fractions import Fraction
from math import floor


def origin(v, n, l):
    """The lower corner of the window of level l for the viewer v."""
    s, s2 = 2 ** l, 2 ** (l + 1)
    return tuple(s2 * floor(Fraction(c - Fraction((n - 1) * s, 2), s2) + Fraction(1, 2)) for c in v)  # @line L1


def window(o, n, l):
    s = 2 ** l
    return (o[0], o[1], o[0] + (n - 1) * s, o[1] + (n - 1) * s)


def points(o, n, l):
    s = 2 ** l
    return [(o[0] + i * s, o[1] + j * s) for i in range(n) for j in range(n)]


class Level:
    """The height array of one level with toroidal addressing."""

    def __init__(self, n, l, height, o):
        self.n, self.l, self.height = n, l, height
        self.o = o
        self.t = [[None] * n for _ in range(n)]
        for p in points(o, n, l):
            self._store(p)

    def _index(self, p):
        s = 2 ** self.l
        return (p[0] // s) % self.n, (p[1] // s) % self.n

    def _store(self, p):
        i, j = self._index(p)
        self.t[i][j] = self.height(p)  # @line L3

    def get(self, p):
        i, j = self._index(p)
        return self.t[i][j]

    def move(self, o):
        """Shift the window to origin o. Returns the number of samples written."""
        old = set(points(self.o, self.n, self.l))
        count = 0
        for p in points(o, self.n, self.l):  # @line L2
            if p not in old:
                self._store(p)
                count += 1
        self.o = o  # @line L4
        return count


def coarse_parents(p, l):
    """The ends of the level l + 1 edge whose midpoint is p, or (p, p) on the level l + 1 grid."""
    s = 2 ** l
    ox, oy = (p[0] // s) % 2, (p[1] // s) % 2
    if ox and oy:
        return (p[0] - s, p[1] - s), (p[0] + s, p[1] + s)
    if ox:
        return (p[0] - s, p[1]), (p[0] + s, p[1])
    if oy:
        return (p[0], p[1] - s), (p[0], p[1] + s)
    return p, p


def morph_height(p, l, win, height, w, last):
    """z' = (1 - alpha) z_f + alpha z_c, alpha = 1 on the window border and 0 from w cells inward."""
    s = 2 ** l
    if last:
        return Fraction(height(p))
    b = Fraction(min(p[0] - win[0], win[2] - p[0], p[1] - win[1], win[3] - p[1]), s)
    alpha = min(max(1 - b / w, Fraction(0)), Fraction(1))
    a, c = coarse_parents(p, l)
    zc = Fraction(height(a) + height(c), 2)
    return (1 - alpha) * height(p) + alpha * zc  # @line L7


def mesh(v, n, levels, height, w):
    """Triangles as ((level, point), ...) triples, counterclockwise, and the zero-area
    triangles that close the T-junctions on the outer border of each finer level."""
    wins = [window(origin(v, n, l), n, l) for l in range(levels)]
    for l in range(1, levels):
        f, c = wins[l - 1], wins[l]
        assert c[0] < f[0] and c[1] < f[1] and f[2] < c[2] and f[3] < c[3]
    tris, degenerate = [], []
    for l in range(levels):
        s = 2 ** l
        x0, y0, x1, y1 = wins[l]
        for x in range(x0, x1, s):
            for y in range(y0, y1, s):
                if l > 0:
                    f = wins[l - 1]
                    if f[0] <= x and x + s <= f[2] and f[1] <= y and y + s <= f[3]:
                        continue
                a, b, c, d = (x, y), (x + s, y), (x + s, y + s), (x, y + s)
                tris.append(((l, a), (l, b), (l, c)))  # @line L5
                tris.append(((l, a), (l, c), (l, d)))
        if l > 0:
            f0, g0, f1, g1 = wins[l - 1]
            corners = [(f0, g0), (f1, g0), (f1, g1), (f0, g1)]
            for k in range(4):
                p, q = corners[k], corners[(k + 1) % 4]
                steps = max(abs(q[0] - p[0]), abs(q[1] - p[1])) // s
                dx, dy = (q[0] - p[0]) // steps, (q[1] - p[1]) // steps
                for i in range(steps):
                    a = (p[0] + i * dx, p[1] + i * dy)
                    b = (a[0] + dx, a[1] + dy)
                    o = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
                    degenerate.append(((l, a), (l, b), (l - 1, o)))  # @line L6
    heights = {}
    for l in range(levels):
        for p in points(origin(v, n, l), n, l):
            heights[(l, p)] = morph_height(p, l, wins[l], height, w, l == levels - 1)
    return tris, degenerate, heights, wins
