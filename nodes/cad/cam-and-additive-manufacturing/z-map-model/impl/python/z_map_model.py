# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/z-map-model/. The authors are listed in prov/5REJ5X.jsonl.

"""A z-map stock model for 3-axis milling with a ball-end mill.

The stock is a grid of vertical columns. Column (i, j) stands at the point
(x0 + i h, y0 + j h) and holds one number, the height of the top of the stock
there. A ball-end mill of radius r with its shank pointing up (+z) moves on a
straight line, its ball center going from c0 to c1. The tool removes, on each
vertical line, every point at or above the lowest point of the swept tool, so
a cut sets H[i][j] to min(H[i][j], zlo), where zlo is that lowest point.

zlo comes in closed form. For the column at q, the ball center at time t is
c(t) = c0 + t (c1 - c0), its horizontal distance to q is d(t), and the lowest
point of the ball on the line is f(t) = cz(t) - sqrt(r^2 - d(t)^2), defined
where d(t) <= r. f is convex, so its minimum on the interval is its
stationary point, clamped to the interval.

Heights are floats: they are measured quantities. The tests check them
against an exact Fraction membership test, to a tolerance of 1e-9.
"""

from math import ceil, floor, sqrt


def lowest_point(q, c0, c1, r):
    """Lowest z of the ball-end tool swept from c0 to c1 on the vertical line at q.

    q is (x, y); c0 and c1 are ball centers (x, y, z). Returns None if the
    line misses the swept tool.
    """
    ax, ay = c0[0] - q[0], c0[1] - q[1]  # @line L6
    bx, by = c1[0] - c0[0], c1[1] - c0[1]  # @line L6
    s = c1[2] - c0[2]  # @line L6
    a2, k, b2 = ax * ax + ay * ay, ax * bx + ay * by, bx * bx + by * by  # @line L7
    r2 = r * r - a2  # @line L7
    if b2 == 0:  # @line L8
        if r2 < 0:  # @line L9
            return None  # @line L9
        t = 0 if s >= 0 else 1  # @line L10
        return c0[2] + t * s - sqrt(r2)  # @line L10
    disc = k * k + b2 * r2  # @line L11
    if disc < 0:  # @line L12
        return None  # @line L12
    root = sqrt(disc)
    lo, hi = max(0.0, (-k - root) / b2), min(1.0, (-k + root) / b2)  # @line L13
    if lo > hi:  # @line L14
        return None  # @line L14
    t = (-k - s * sqrt(disc / (b2 + s * s))) / b2  # @line L15
    t = min(max(t, lo), hi)  # @line L16
    dx, dy = ax + t * bx, ay + t * by
    return c0[2] + t * s - sqrt(max(0.0, r * r - dx * dx - dy * dy))  # @line L17


class ZMap:
    """Heights on an nx by ny grid with spacing h and lower-left point (x0, y0)."""

    def __init__(self, nx, ny, h, top, x0=0.0, y0=0.0, bottom=0.0):
        self.nx, self.ny, self.h = nx, ny, h
        self.x0, self.y0, self.bottom = x0, y0, bottom
        self.H = [[top] * ny for _ in range(nx)]

    def point(self, i, j):
        return (self.x0 + i * self.h, self.y0 + j * self.h)

    def cut_ball_move(self, c0, c1, r):
        """Remove the volume swept by a ball-end mill moving from c0 to c1."""
        xs = (min(c0[0], c1[0]) - r, max(c0[0], c1[0]) + r)  # @line L1
        ys = (min(c0[1], c1[1]) - r, max(c0[1], c1[1]) + r)
        i0, i1 = max(0, ceil((xs[0] - self.x0) / self.h)), min(self.nx - 1, floor((xs[1] - self.x0) / self.h))
        j0, j1 = max(0, ceil((ys[0] - self.y0) / self.h)), min(self.ny - 1, floor((ys[1] - self.y0) / self.h))
        for i in range(i0, i1 + 1):  # @line L2
            for j in range(j0, j1 + 1):  # @line L2
                z = lowest_point(self.point(i, j), c0, c1, r)  # @line L3
                if z is not None and z < self.H[i][j]:  # @line L4
                    self.H[i][j] = max(z, self.bottom)  # @line L5

    def cut_path(self, centers, r):
        """Cut a polyline toolpath given by its ball centers."""
        for c0, c1 in zip(centers, centers[1:]):
            self.cut_ball_move(c0, c1, r)

    def inside(self, i, j, z):
        """True when the point at column (i, j) and height z is stock."""
        return self.bottom <= z <= self.H[i][j]

    def volume(self):
        """Volume by the column rule: each column stands for an h by h cell."""
        return sum(H - self.bottom for col in self.H for H in col) * self.h * self.h
