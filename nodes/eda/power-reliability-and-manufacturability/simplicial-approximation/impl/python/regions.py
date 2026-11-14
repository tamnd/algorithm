# SPDX-License-Identifier: MIT
# Shared helper of the pr3 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Plane regions with exact line search oracles, for the simplicial approximation tests.

Each region has inside(p), exit_point(x, d) and area. exit_point returns the
point where the ray x + t d, t >= 0, first leaves the closed region, for x
in the region; a point on the boundary that moves outward exits at t = 0.
"""

import math


class Ellipse:
    """(x - cx)^2 / a^2 + (y - cy)^2 / b^2 <= 1; a = b gives a disc."""

    def __init__(self, cx, cy, a, b):
        self.cx, self.cy, self.a, self.b = cx, cy, a, b
        self.area = math.pi * a * b

    def inside(self, p, eps=1e-9):
        return ((p[0] - self.cx) / self.a) ** 2 + ((p[1] - self.cy) / self.b) ** 2 <= 1 + eps

    def exit_point(self, x, d):
        u = ((x[0] - self.cx) / self.a, (x[1] - self.cy) / self.b)
        e = (d[0] / self.a, d[1] / self.b)
        qa = e[0] ** 2 + e[1] ** 2
        qb = 2 * (u[0] * e[0] + u[1] * e[1])
        qc = min(u[0] ** 2 + u[1] ** 2 - 1, 0.0)
        t = (-qb + math.sqrt(max(qb * qb - 4 * qa * qc, 0.0))) / (2 * qa)
        return (x[0] + t * d[0], x[1] + t * d[1])


class ConvexPolygon:
    """The intersection of the half-planes n . p <= c of its edges; vertices counterclockwise."""

    def __init__(self, vertices):
        self.vertices = vertices
        self.halfplanes = []
        for i, a in enumerate(vertices):
            b = vertices[(i + 1) % len(vertices)]
            dx, dy = b[0] - a[0], b[1] - a[1]
            n = (dy / math.hypot(dx, dy), -dx / math.hypot(dx, dy))
            self.halfplanes.append((n, n[0] * a[0] + n[1] * a[1]))
        self.area = abs(shoelace(vertices))

    def inside(self, p, eps=1e-9):
        return all(n[0] * p[0] + n[1] * p[1] <= c + eps for n, c in self.halfplanes)

    def exit_time(self, x, d):
        t = math.inf
        for n, c in self.halfplanes:
            nd = n[0] * d[0] + n[1] * d[1]
            if nd > 1e-15:
                t = min(t, max((c - n[0] * x[0] - n[1] * x[1]) / nd, 0.0))
        return t

    def exit_point(self, x, d):
        t = self.exit_time(x, d)
        return (x[0] + t * d[0], x[1] + t * d[1])


class Union:
    """A union of convex polygons, possibly nonconvex, with the exact first exit along a ray."""

    def __init__(self, pieces, area):
        self.pieces, self.area = pieces, area

    def inside(self, p, eps=1e-9):
        return any(q.inside(p, eps) for q in self.pieces)

    def exit_point(self, x, d):
        t = 0.0
        while True:
            p = (x[0] + t * d[0], x[1] + t * d[1])
            nxt = max((t + q.exit_time(p, d) for q in self.pieces if q.inside(p)), default=t)
            if nxt <= t + 1e-15:
                return p
            t = nxt


def shoelace(vertices):
    return sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(vertices, vertices[1:] + vertices[:1])) / 2
