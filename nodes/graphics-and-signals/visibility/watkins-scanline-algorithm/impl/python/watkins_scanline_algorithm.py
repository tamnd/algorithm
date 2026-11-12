# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/watkins-scanline-algorithm/. The authors are listed in prov/Z8FKJW.jsonl.

"""Watkins' scanline visible surface algorithm (Watkins 1970).

A triangle is ((x0, y0, z0), (x1, y1, z1), (x2, y2, z2)) in pixel units, x to
the right, y down, smaller z nearer. Scanline j is the line y = j + 1/2,
through the pixel centers of row j. Precondition: no vertex has y = j + 1/2,
so a scanline never passes through a vertex or along an edge. On a scanline a
triangle covers the half-open interval [xl, xr), which is the top-left rule
there. Each pixel gets the triangle nearest at its center (the earlier one on
a tie), or the background.
"""

from fractions import Fraction
from math import ceil, floor

HALF = Fraction(1, 2)


class Edge:
    __slots__ = ("k", "x", "dx", "j_last")

    def __init__(self, k, x, dx, j_last):
        self.k, self.x, self.dx, self.j_last = k, x, dx, j_last


def _plane(tri):
    """Return (a, b, c) with z = a x + b y + c on the plane of the triangle."""
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = tri
    ux, uy, uz = x1 - x0, y1 - y0, z1 - z0
    vx, vy, vz = x2 - x0, y2 - y0, z2 - z0
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    a, b = Fraction(-nx, nz), Fraction(-ny, nz)
    return a, b, z0 - a * x0 - b * y0


def watkins(width, height, triangles, background=None):
    """Return a height x width grid of triangle indices (or background) and the
    number of span splits made at depth crossings."""
    for t in triangles:
        for v in t:
            if v[1] - HALF == floor(v[1] - HALF):
                raise ValueError("a vertex lies on a scanline")
    planes = {}
    edge_table = {}
    for k, t in enumerate(triangles):  # @line L1: bucket the edges by first scanline
        (x0, y0, _), (x1, y1, _), (x2, y2, _) = t
        if (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0) == 0:
            continue
        planes[k] = _plane(t)
        for (ax, ay), (bx, by) in (((x0, y0), (x1, y1)), ((x1, y1), (x2, y2)), ((x2, y2), (x0, y0))):
            if ay > by:
                ax, ay, bx, by = bx, by, ax, ay
            j_first, j_last = ceil(ay - HALF), floor(by - HALF)
            if j_first > j_last:
                continue  # the edge crosses no scanline
            dx = Fraction(bx - ax) / (by - ay)
            edge_table.setdefault(j_first, []).append(Edge(k, ax + dx * (j_first + HALF - ay), dx, j_last))
    image = [[background] * width for _ in range(height)]
    splits = 0
    active = []  # the active edge list, sorted by x
    for j in range(min(edge_table, default=height), height):  # @line L2
        active.extend(edge_table.get(j, ()))  # @line L3
        for p in range(1, len(active)):  # @line L4: insertion sort, nearly sorted input
            e, q = active[p], p - 1
            while q >= 0 and active[q].x > e.x:
                active[q + 1] = active[q]
                q -= 1
            active[q + 1] = e
        if j >= 0:
            splits += _scanline(j + HALF, width, active, planes, image[j])
        for e in active:  # @line L10: step each edge to the next scanline
            e.x += e.dx
        active = [e for e in active if e.j_last > j]
    return image, splits


def _scanline(y, width, active, planes, row):
    """Sweep the sorted crossings of one scanline. Between two neighbor
    crossings the set of covering triangles is fixed: that is a span."""
    inside = set()
    splits = 0
    for n, e in enumerate(active):  # @line L5: enter or leave triangle e.k
        inside ^= {e.k}
        if not inside or n + 1 == len(active):
            continue
        a, b = e.x, active[n + 1].x  # @line L6: the span [a, b)
        i0, i1 = max(0, ceil(a - HALF)), min(width - 1, ceil(b - HALF) - 1)
        if i0 > i1:
            continue
        slope = {k: planes[k][0] for k in inside}
        base = {k: planes[k][1] * y + planes[k][2] for k in inside}

        def nearest(i):
            return min(inside, key=lambda m: (slope[m] * (i + HALF) + base[m], m))

        stack = [(i0, i1)]
        while stack:  # @line L7: Watkins' span subdivision
            lo, hi = stack.pop()
            p, q = nearest(lo), nearest(hi)
            if p == q:  # @line L8: one triangle is nearest on the whole span
                for i in range(lo, hi + 1):
                    row[i] = p
                continue
            # @line L9: cut where the depth lines of p and q cross.
            x_star = (base[q] - base[p]) / (slope[p] - slope[q])
            cut = ceil(x_star - HALF)  # the first center at or right of x_star
            if cut + HALF == x_star and p < q:
                cut += 1  # p wins the tie at x_star
            splits += 1
            stack.append((cut, hi))
            stack.append((lo, cut - 1))
    return splits
