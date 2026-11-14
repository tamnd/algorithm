# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dexel-representation/. The authors are listed in prov/QH2CZJ.jsonl.

"""Dexel model: a grid of parallel rays, each with a sorted list of depth intervals.

A ray is a list of closed intervals [lo, hi] with lo < hi, sorted and pairwise
disjoint (they may not touch either; touching intervals are merged). The
Boolean operations are regularized: the result is the closure of the interior
of the pointwise result, so pieces of length zero disappear. They run by one
merge of the two endpoint lists, in time linear in the number of intervals.
With int or Fraction endpoints they are exact.

The cut of a ball-end mill along a straight move is a subtraction of one
interval per ray: the part of the ray inside the swept tool. With a shank the
interval goes up to infinity; without it the tool is the swept ball alone, a
capsule, and the stock that stays on a ray can be two intervals, an undercut.
That segment is computed in floating point and is a measured quantity.
"""

from math import ceil, floor, inf, sqrt


def _merge_sorted(xs, ys):
    """Merge two sorted lists into one sorted list without repeated values."""
    out, i, j = [], 0, 0
    while i < len(xs) or j < len(ys):
        if j == len(ys) or (i < len(xs) and xs[i] <= ys[j]):
            v, i = xs[i], i + 1
        else:
            v, j = ys[j], j + 1
        if not out or out[-1] != v:
            out.append(v)
    return out


def combine(I, J, op):
    """Regularized Boolean operation of two dexels.

    I and J are lists of (lo, hi) pairs, sorted, disjoint and not touching.
    op maps (in I, in J) to a bool, for example lambda a, b: a and not b.
    """
    ends_i = [e for iv in I for e in iv]
    ends_j = [e for iv in J for e in iv]
    P = _merge_sorted(ends_i, ends_j)  # @line L1
    out, i, j = [], 0, 0  # @line L2
    for p, p2 in zip(P, P[1:]):  # @line L3
        while i < len(I) and I[i][1] <= p:  # @line L4
            i += 1  # @line L4
        while j < len(J) and J[j][1] <= p:  # @line L5
            j += 1  # @line L5
        a = i < len(I) and I[i][0] <= p  # @line L6
        b = j < len(J) and J[j][0] <= p  # @line L6
        if op(a, b):  # @line L7
            if out and out[-1][1] == p:  # @line L8
                out[-1] = (out[-1][0], p2)  # @line L8
            else:
                out.append((p, p2))  # @line L9
    return out  # @line L10


def union(I, J):
    return combine(I, J, lambda a, b: a or b)


def intersection(I, J):
    return combine(I, J, lambda a, b: a and b)


def difference(I, J):
    return combine(I, J, lambda a, b: a and not b)


def _lowest(q, c0, c1, r):
    """Lowest z of the capsule swept by a ball of radius r from c0 to c1, on the vertical line at q."""
    ax, ay = c0[0] - q[0], c0[1] - q[1]
    bx, by, s = c1[0] - c0[0], c1[1] - c0[1], c1[2] - c0[2]
    k, b2, r2 = ax * bx + ay * by, bx * bx + by * by, r * r - ax * ax - ay * ay
    if b2 == 0:
        if r2 < 0:
            return None
        return c0[2] + (0 if s >= 0 else s) - sqrt(r2)
    disc = k * k + b2 * r2
    if disc < 0:
        return None
    lo, hi = max(0.0, (-k - sqrt(disc)) / b2), min(1.0, (-k + sqrt(disc)) / b2)
    if lo > hi:
        return None
    t = min(max((-k - s * sqrt(disc / (b2 + s * s))) / b2, lo), hi)
    dx, dy = ax + t * bx, ay + t * by
    return c0[2] + t * s - sqrt(max(0.0, r * r - dx * dx - dy * dy))


def tool_segment(q, c0, c1, r, shank):
    """The (lo, hi) part of the vertical line at q inside the swept tool, or None.

    The capsule is convex, so the part is one interval. Its top is the lowest
    point of the mirror image in the plane z = 0, negated. With a shank the
    top is infinity.
    """
    lo = _lowest(q, c0, c1, r)
    if lo is None:
        return None
    if shank:
        return (lo, inf)
    m0, m1 = (c0[0], c0[1], -c0[2]), (c1[0], c1[1], -c1[2])
    return (lo, -_lowest(q, m0, m1, r))


class DexelModel:
    """An nx by ny grid of vertical rays with spacing h; ray (i, j) is at (x0 + i h, y0 + j h)."""

    def __init__(self, nx, ny, h, x0=0.0, y0=0.0):
        self.nx, self.ny, self.h, self.x0, self.y0 = nx, ny, h, x0, y0
        self.rays = [[[] for _ in range(ny)] for _ in range(nx)]

    @classmethod
    def box(cls, nx, ny, h, zlo, zhi, x0=0.0, y0=0.0):
        m = cls(nx, ny, h, x0, y0)
        for i in range(nx):
            for j in range(ny):
                m.rays[i][j] = [(zlo, zhi)]
        return m

    def point(self, i, j):
        return (self.x0 + i * self.h, self.y0 + j * self.h)

    def inside(self, i, j, z):
        return any(lo <= z <= hi for lo, hi in self.rays[i][j])

    def boolean(self, other, op):
        """Apply op ray by ray to two models on the same grid."""
        out = DexelModel(self.nx, self.ny, self.h, self.x0, self.y0)
        for i in range(self.nx):
            for j in range(self.ny):
                out.rays[i][j] = combine(self.rays[i][j], other.rays[i][j], op)
        return out

    def cut_ball_move(self, c0, c1, r, shank=True):
        """Subtract the volume swept by a ball-end tool from c0 to c1 (ball centers)."""
        x_lo, x_hi = min(c0[0], c1[0]) - r, max(c0[0], c1[0]) + r
        y_lo, y_hi = min(c0[1], c1[1]) - r, max(c0[1], c1[1]) + r
        i0, i1 = max(0, ceil((x_lo - self.x0) / self.h)), min(self.nx - 1, floor((x_hi - self.x0) / self.h))
        j0, j1 = max(0, ceil((y_lo - self.y0) / self.h)), min(self.ny - 1, floor((y_hi - self.y0) / self.h))
        for i in range(i0, i1 + 1):  # @line L11
            for j in range(j0, j1 + 1):  # @line L11
                seg = tool_segment(self.point(i, j), c0, c1, r, shank)  # @line L12
                if seg is not None and seg[0] < seg[1]:  # @line L13
                    self.rays[i][j] = difference(self.rays[i][j], [seg])  # @line L13

    def volume(self):
        """Sum of interval lengths times h^2: the column estimate of the volume."""
        return sum(hi - lo for col in self.rays for ray in col for lo, hi in ray) * self.h * self.h

    def max_intervals(self):
        return max(len(ray) for col in self.rays for ray in col)
