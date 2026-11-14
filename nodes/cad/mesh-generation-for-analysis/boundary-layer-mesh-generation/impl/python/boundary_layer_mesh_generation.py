# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-layer-mesh-generation/. The authors are listed in prov/H3T7WW.jsonl.

"""Boundary layer meshing in the plane by advancing layers of quads.

The wall is a simple polygon with counterclockwise vertices (a body), and the
layers grow outward into the flow. Each wall vertex moves along a miter
vector: the sum of the unit outward normals of its two edges, scaled so that
the point at height d is at distance d from both edge lines. The heights grow
geometrically: d_k = h1 (r^k - 1) / (r - 1), so layer k has thickness h1 r^(k-1).

A layer is accepted only if every new quad is strictly convex and
counterclockwise and the new front is a simple polygon, tested exactly on the
float coordinates (each float converts to a Fraction without rounding). The
growth stops at the first layer that fails. Positions are floats.
"""

import math
from fractions import Fraction
from typing import List, Sequence, Tuple

from mg3geom import exact, is_valid_planar_mesh, orient2d

Vec = Tuple[float, float]


def outward_normal(a: Vec, b: Vec) -> Vec:
    """Unit normal of the edge ab of a counterclockwise polygon, pointing out."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    return (dy / n, -dx / n)


def miter(na: Vec, nb: Vec) -> Vec:
    """The vector m with m . na = m . nb = 1."""
    s = 1.0 + na[0] * nb[0] + na[1] * nb[1]
    if s < 1e-9:
        raise ValueError("a corner of nearly 360 degrees has no miter vector")
    return ((na[0] + nb[0]) / s, (na[1] + nb[1]) / s)


def layer_heights(h1, r, n: int) -> List:
    """d_0 = 0 and d_k = h1 (1 + r + ... + r^(k-1)); exact for Fraction input."""
    d = [h1 * 0]
    for k in range(n):
        d.append(d[-1] + h1 * r ** k)
    return d


def segments_meet(a, b, c, d) -> bool:
    """Exact test whether the closed segments ab and cd have a common point."""
    def on(p, q, x):
        return (min(p[0], q[0]) <= x[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= x[1] <= max(p[1], q[1]))
    o1, o2, o3, o4 = orient2d(a, b, c), orient2d(a, b, d), orient2d(c, d, a), orient2d(c, d, b)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    return ((o1 == 0 and on(a, b, c)) or (o2 == 0 and on(a, b, d))
            or (o3 == 0 and on(c, d, a)) or (o4 == 0 and on(c, d, b)))


def is_simple_polygon(poly: Sequence) -> bool:
    """Exact test: non-adjacent edges do not meet and adjacent edges do not fold back."""
    n = len(poly)
    for i in range(n):
        a, b, c = poly[i], poly[(i + 1) % n], poly[(i + 2) % n]
        if orient2d(a, b, c) == 0 and (a[0] - b[0]) * (c[0] - b[0]) + (a[1] - b[1]) * (c[1] - b[1]) > 0:
            return False
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            if segments_meet(poly[i], poly[(i + 1) % n], poly[j], poly[(j + 1) % n]):
                return False
    return True


def grow_layers(wall: Sequence[Vec], h1: float, r: float, nlayers: int):
    """Returns (points, quads, layers, reason). points[k * n + i] is wall vertex i
    at height d_k; quads are counterclockwise index 4-tuples; layers is the
    number of accepted layers; reason is None or why the growth stopped."""
    n = len(wall)
    normals = [outward_normal(wall[i], wall[(i + 1) % n]) for i in range(n)]  # @line L1
    m = [miter(normals[i - 1], normals[i]) for i in range(n)]  # @line L2
    d = layer_heights(h1, r, nlayers)  # @line L3
    points: List[Vec] = list(wall)
    quads: List[Tuple[int, int, int, int]] = []
    E = [exact(p) for p in points]
    for k in range(1, nlayers + 1):  # @line L4
        new = [(wall[i][0] + d[k] * m[i][0], wall[i][1] + d[k] * m[i][1]) for i in range(n)]  # @line L5
        lo, hi = (k - 1) * n, k * n
        layer = [(lo + (i + 1) % n, lo + i, hi + i, hi + (i + 1) % n) for i in range(n)]  # @line L6
        En = E + [exact(p) for p in new]
        if not is_valid_planar_mesh(En, layer):  # @line L7
            return points, quads, k - 1, "a quad of layer %d is not strictly convex" % k
        if not is_simple_polygon(En[hi:]):  # @line L8
            return points, quads, k - 1, "the front of layer %d is not simple" % k
        points += new  # @line L9
        E = En
        quads += layer
    return points, quads, nlayers, None  # @line L10


def collapse_height(wall: Sequence[Vec], i: int) -> float:
    """The height at which the offset of edge i reaches length zero, from the
    formula length(d) = L + d (tan(a/2) + tan(b/2)), with a, b the signed turning
    angles at its two ends; infinity if the length does not shrink."""
    n = len(wall)
    a, b = wall[i], wall[(i + 1) % n]
    L = math.hypot(b[0] - a[0], b[1] - a[1])

    def turn(j):
        p, q, s = wall[j - 1], wall[j], wall[(j + 1) % n]
        u = (q[0] - p[0], q[1] - p[1])
        v = (s[0] - q[0], s[1] - q[1])
        return math.atan2(u[0] * v[1] - u[1] * v[0], u[0] * v[0] + u[1] * v[1])
    rate = math.tan(turn(i) / 2) + math.tan(turn((i + 1) % n) / 2)
    return math.inf if rate >= 0 else L / -rate


def area2(points, quads) -> Fraction:
    """Twice the total signed area of the quads, exact."""
    total = Fraction(0)
    for q in quads:
        P = [exact(points[i]) for i in q]
        total += orient2d(P[0], P[1], P[2]) + orient2d(P[0], P[2], P[3])
    return total
