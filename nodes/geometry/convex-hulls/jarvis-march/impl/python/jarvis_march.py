# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jarvis-march/. The authors are listed in prov/JTX14G.jsonl.

from collections import deque

Point = tuple[int, int]
Point3 = tuple[int, int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of the triangle pqr: positive for a left turn, zero when collinear."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def _dist2(p: Point, q: Point) -> int:
    return (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2


def jarvis_march(points: list[Point]) -> list[Point]:
    """Return the vertices of the convex hull of points in counterclockwise order.

    The first vertex is the lexicographically smallest point. Only strictly convex vertices are
    returned: duplicates and points in the middle of a hull edge are dropped. With all points
    collinear the result is the two end points. Coordinates must be int or Fraction (exact).
    Cost: O(n h) time for h hull vertices, O(n) extra space.
    """
    s = list(set(points))  # @line L1
    if len(s) <= 1:  # @line L2
        return s
    start = min(s)  # @line L3
    hull: list[Point] = []  # @line L4
    p = start
    while True:  # @line L5
        hull.append(p)  # @line L6
        q = s[0] if s[0] != p else s[1]  # @line L7
        for r in s:  # @line L8
            if r == p:
                continue
            o = orient(p, q, r)
            if o < 0 or (o == 0 and _dist2(p, r) > _dist2(p, q)):  # @line L9
                q = r
        p = q  # @line L10
        if p == start:  # @line L11
            break
    return hull  # @line L12


def orient3(a: Point3, b: Point3, c: Point3, d: Point3) -> int:
    """det(b - a, c - a, d - a): positive when d sees a, b, c in counterclockwise order."""
    ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
    wx, wy, wz = d[0] - a[0], d[1] - a[1], d[2] - a[2]
    return ux * (vy * wz - vz * wy) - uy * (vx * wz - vz * wx) + uz * (vx * wy - vy * wx)


def gift_wrapping_3d(points: list[Point3]) -> set[tuple[int, int, int]]:
    """Return the facets of the convex hull of points in R^3 by gift wrapping.

    Each facet is a triple of indices (i, j, k) into points, counterclockwise seen from outside
    (every other point d has orient3 < 0), rotated so that the smallest index comes first.
    Precondition (general position): n >= 4, no four points coplanar, and no three of the
    projections (x, y) collinear (so the first edge found in the projection is a hull edge).
    Cost: O(n) per facet, O(n h) in total for h hull vertices; O(n) extra space besides the output.
    """
    n = len(points)
    pts = points
    a = min(range(n), key=lambda i: pts[i])
    # first edge: one 2D gift-wrapping step in the projection to the (x, y) plane
    b = 0 if a != 0 else 1
    for r in range(n):
        if r != a and orient(pts[a][:2], pts[b][:2], pts[r][:2]) < 0:
            b = r
    # first facet: pivot a plane around the edge (a, b)
    c = next(i for i in range(n) if i not in (a, b))
    for r in range(n):
        if r not in (a, b, c) and orient3(pts[a], pts[b], pts[c], pts[r]) > 0:
            c = r

    def norm(f: tuple[int, int, int]) -> tuple[int, int, int]:
        i = f.index(min(f))
        return (f[i], f[(i + 1) % 3], f[(i + 2) % 3])

    facets = {norm((a, b, c))}
    done_edges: set[tuple[int, int]] = set()
    todo = deque([(a, b), (b, c), (c, a)])
    while todo:
        u, v = todo.popleft()
        if (u, v) in done_edges:
            continue
        done_edges.add((u, v))
        # the neighbor facet across (u, v) contains the directed edge (v, u)
        w = next(i for i in range(n) if i not in (u, v))
        for r in range(n):
            if r not in (u, v, w) and orient3(pts[v], pts[u], pts[w], pts[r]) > 0:
                w = r
        facets.add(norm((v, u, w)))
        done_edges.add((v, u))  # its twin (u, v) is the facet we came from
        for e in ((u, w), (w, v)):
            if e not in done_edges:
                todo.append(e)
    return facets
