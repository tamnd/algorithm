# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constant-engagement-toolpath/. The authors are listed in prov/X9MBE5.jsonl.

"""A constant engagement toolpath, generated step by step from a pixel stock.

The stock is a grid of square pixels of side d; a pixel holds material until
the tool removes it. The tool is a disk of radius R. Its engagement angle at
the center c, moving in the direction psi, is the angle of the front half of
the tool circle (the points within 90 degrees of the feed direction) that
lies in material. It is sampled at n points of the front half circle.

For a straight cut with radial depth a, the engagement is arccos(1 - a/R).
For a tool on a circle of radius rho, cutting into material outside the
circle of radius Rb around the same center, it is
arccos((Rb^2 - rho^2 - R^2) / (2 rho R)).

The generator moves the tool by a step s at a time. At each step it chooses
the new heading within max_turn of the old one so that the engagement at
the new position equals the target, by bisection, then removes the swept
capsule from the stock. The material lies on the side `side` of the path:
+1 for the left, -1 for the right.
"""

import math


class Stock:
    """A pixel stock on [x0, x0 + nx d] x [y0, y0 + ny d]."""

    def __init__(self, x0, y0, d, nx, ny, material):
        self.x0, self.y0, self.d, self.nx, self.ny = x0, y0, d, nx, ny
        self.cells = bytearray(nx * ny)
        for j in range(ny):
            y = y0 + (j + 0.5) * d
            for i in range(nx):
                if material(x0 + (i + 0.5) * d, y):
                    self.cells[j * nx + i] = 1

    def has(self, x, y):
        i = math.floor((x - self.x0) / self.d)
        j = math.floor((y - self.y0) / self.d)
        if 0 <= i < self.nx and 0 <= j < self.ny:
            return self.cells[j * self.nx + i] == 1
        return False

    def cut_capsule(self, a, b, r):
        """Remove the pixels whose centers are within r of the segment from a to b."""
        d = self.d
        i0 = max(0, math.floor((min(a[0], b[0]) - r - self.x0) / d))
        i1 = min(self.nx - 1, math.floor((max(a[0], b[0]) + r - self.x0) / d))
        j0 = max(0, math.floor((min(a[1], b[1]) - r - self.y0) / d))
        j1 = min(self.ny - 1, math.floor((max(a[1], b[1]) + r - self.y0) / d))
        ex, ey = b[0] - a[0], b[1] - a[1]
        ee = ex * ex + ey * ey
        rr = r * r
        for j in range(j0, j1 + 1):
            y = self.y0 + (j + 0.5) * d
            row = j * self.nx
            for i in range(i0, i1 + 1):
                x = self.x0 + (i + 0.5) * d
                px, py = x - a[0], y - a[1]
                t = 0.0 if ee == 0 else min(1.0, max(0.0, (px * ex + py * ey) / ee))
                qx, qy = px - t * ex, py - t * ey
                if qx * qx + qy * qy <= rr:
                    self.cells[row + i] = 0


def front_points(c, psi, R, n=60):
    """The n sample points of the front half of the tool circle, at the centers of n equal arcs."""
    pts = []
    for k in range(n):
        t = psi - math.pi / 2 + math.pi * (k + 0.5) / n
        pts.append((c[0] + R * math.cos(t), c[1] + R * math.sin(t)))
    return pts


def engagement(stock, c, psi, R, n=60):
    """The engagement angle in degrees, from n samples of the front half circle."""
    return 180.0 * sum(1 for x, y in front_points(c, psi, R, n) if stock.has(x, y)) / n


def straight_engagement(a, R):
    """Closed form for a straight cut of radial depth a, 0 <= a <= 2R, in degrees."""
    return math.degrees(math.acos(1 - a / R))


def circle_engagement(rho, Rb, R):
    """Closed form for a tool on a circle of radius rho with material outside radius Rb."""
    c = (Rb * Rb - rho * rho - R * R) / (2 * rho * R)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def constant_engagement_path(stock, c, psi, R, target, step, max_turn, n_steps, side=-1, n=60):
    """Generate n_steps tool moves that hold the engagement at target (degrees).

    Returns a list of (center, heading, engagement) after each move. The
    stock is cut as the tool moves.
    """
    path = []

    def E(phi):  # @line L2
        p = (c[0] + step * math.cos(phi), c[1] + step * math.sin(phi))
        return engagement(stock, p, phi, R, n)

    for _ in range(n_steps):  # @line L1
        toward, away = psi + side * max_turn, psi - side * max_turn  # @line L3
        if E(away) >= target:  # @line L4
            phi = away
        elif E(toward) <= target:  # @line L5
            phi = toward
        else:  # @line L6
            lo, hi = toward, away
            for _ in range(12):
                mid = (lo + hi) / 2
                if E(mid) > target:
                    lo = mid
                else:
                    hi = mid
            phi = (lo + hi) / 2
        e = E(phi)
        nc = (c[0] + step * math.cos(phi), c[1] + step * math.sin(phi))
        stock.cut_capsule(c, nc, R)  # @line L7
        path.append((nc, phi, e))  # @line L8
        c, psi = nc, phi
    return path  # @line L9


def follow_path(stock, centers, R, n=60):
    """Cut along a given list of centers and record the engagement at each one."""
    out = []
    for a, b in zip(centers, centers[1:]):
        psi = math.atan2(b[1] - a[1], b[0] - a[0])
        out.append(engagement(stock, b, psi, R, n))
        stock.cut_capsule(a, b, R)
    return out
