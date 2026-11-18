# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/texture-clipmap/. The authors are listed in prov/NPGSAB.jsonl.

"""A texture clipmap: a mipmap whose levels larger than C keep a C x C window.

Texel coordinates are integers, level 0 is the finest level of side N, and
level l has side N / 2^l. The clip center c is a level 0 texel. A level of
the clip stack stores its window in a C x C array with toroidal addressing;
the levels of side C or less (the clip pyramid) are kept whole. Sample
points (u, v) are in level 0 texel units, with texel centers at i + 1/2.
Values are exact fractions.
"""

from fractions import Fraction
from math import floor


def build_mipmap(tex):
    """All levels of a square power-of-two texture, by 2 x 2 box averages."""
    levels = [[[Fraction(x) for x in row] for row in tex]]
    while len(levels[-1]) > 1:
        a = levels[-1]
        m = len(a) // 2
        levels.append(
            [[Fraction(a[2 * i][2 * j] + a[2 * i + 1][2 * j] + a[2 * i][2 * j + 1] + a[2 * i + 1][2 * j + 1], 4) for j in range(m)] for i in range(m)]
        )
    return levels


def window(c, l, C):
    """The half-open window (x0, y0, x1, y1) of level l for the clip center c."""
    cx, cy = c[0] // 2 ** l, c[1] // 2 ** l
    return (cx - C // 2, cy - C // 2, cx + C // 2, cy + C // 2)


def in_window(w, t):
    return w[0] <= t[0] < w[2] and w[1] <= t[1] < w[3]


def texel_counts(N, C):
    """The texels of the clipmap and of the full mipmap of an N x N texture."""
    sides = []
    s = N
    while s >= 1:
        sides.append(s)
        s //= 2
    return sum(min(s, C) ** 2 for s in sides), sum(s * s for s in sides)


def taps(size, u, v, l):
    """The bilinear taps of level l at (u, v), with clamp addressing, and the weights."""
    x = Fraction(u) / 2 ** l - Fraction(1, 2)
    y = Fraction(v) / 2 ** l - Fraction(1, 2)
    i0, j0 = floor(x), floor(y)
    fx, fy = x - i0, y - j0

    def cl(k):
        return min(max(k, 0), size - 1)

    return (cl(i0), cl(i0 + 1)), (cl(j0), cl(j0 + 1)), fx, fy


def bilinear(get, size, u, v, l):
    (i0, i1), (j0, j1), fx, fy = taps(size, u, v, l)
    return (
        (1 - fx) * (1 - fy) * get(l, i0, j0)
        + fx * (1 - fy) * get(l, i1, j0)
        + (1 - fx) * fy * get(l, i0, j1)
        + fx * fy * get(l, i1, j1)
    )


def trilinear(get, sizes, u, v, lam):
    """The trilinear sample at the level of detail lam >= 0."""
    a = min(floor(lam), len(sizes) - 1)
    f = Fraction(lam) - a if a < len(sizes) - 1 else Fraction(0)
    s = bilinear(get, sizes[a], u, v, a)
    if f == 0:
        return s
    return (1 - f) * s + f * bilinear(get, sizes[a + 1], u, v, a + 1)


def mip_sample(mip, u, v, lam):
    """The reference: a trilinear sample of the full mipmap."""
    return trilinear(lambda l, i, j: mip[l][i][j], [len(a) for a in mip], u, v, lam)


class Clipmap:
    def __init__(self, mip, C, c):
        self.mip = mip  # the full texture, on disk or in main memory
        self.C = C
        self.sizes = [len(a) for a in mip]
        self.k = sum(1 for s in self.sizes if s > C)  # the levels of the clip stack
        self.S = [[[None] * C for _ in range(C)] for _ in range(self.k)]
        self.win = [None] * self.k
        self.recenter(c)

    def recenter(self, c):
        """Move the clip center to c. Returns the number of texels written."""
        C = self.C
        count = 0
        for l in range(self.k):  # @line L1
            new = window(c, l, C)  # @line L2
            old = self.win[l]
            for tx in range(new[0], new[2]):
                for ty in range(new[1], new[3]):  # @line L3
                    if old is not None and in_window(old, (tx, ty)):
                        continue
                    inside = 0 <= tx < self.sizes[l] and 0 <= ty < self.sizes[l]
                    self.S[l][tx % C][ty % C] = self.mip[l][tx][ty] if inside else None  # @line L4
                    count += 1
            self.win[l] = new  # @line L5
        return count

    def get(self, l, i, j):
        if l >= self.k:
            return self.mip[l][i][j]
        if not in_window(self.win[l], (i, j)):
            raise KeyError((l, i, j))
        return self.S[l][i % self.C][j % self.C]

    def holds(self, u, v, l):
        """Does level l hold the bilinear footprint of (u, v)?"""
        if l >= self.k:
            return True
        (i0, i1), (j0, j1), _, _ = taps(self.sizes[l], u, v, l)
        return all(in_window(self.win[l], (i, j)) for i in (i0, i1) for j in (j0, j1))

    def finest_level(self, u, v):
        """The smallest l such that the levels l, l + 1, ... all hold the footprint."""
        l = len(self.sizes) - 1
        while l > 0 and self.holds(u, v, l - 1):  # @line L6
            l -= 1
        return l

    def lookup(self, u, v, lam):
        l = max(Fraction(lam), self.finest_level(u, v))  # @line L7
        return trilinear(self.get, self.sizes, u, v, l)  # @line L8
