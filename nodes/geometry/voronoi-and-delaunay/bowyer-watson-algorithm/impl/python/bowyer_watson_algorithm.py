# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bowyer-watson-algorithm/. The authors are listed in prov/QVMB6E.jsonl.

Point = tuple[int, int]
Triangle = tuple[int, int, int]
GHOST = -1  # the vertex at infinity of the ghost triangles


def orient(a: Point, b: Point, c: Point) -> int:
    """Sign of (b - a) x (c - a): 1 for a left turn, -1 for a right turn, 0 when collinear."""
    d = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (d > 0) - (d < 0)


def incircle(a: Point, b: Point, c: Point, d: Point) -> int:
    """For a, b, c counterclockwise: 1 if d is strictly inside their circumcircle, 0 on it, -1 outside."""
    adx, ady = a[0] - d[0], a[1] - d[1]
    bdx, bdy = b[0] - d[0], b[1] - d[1]
    cdx, cdy = c[0] - d[0], c[1] - d[1]
    det = ((adx * adx + ady * ady) * (bdx * cdy - cdx * bdy)
           + (bdx * bdx + bdy * bdy) * (cdx * ady - adx * cdy)
           + (cdx * cdx + cdy * cdy) * (adx * bdy - bdx * ady))
    return (det > 0) - (det < 0)


def bowyer_watson(points: list[Point]) -> list[tuple[Point, Point, Point]]:
    """Return a Delaunay triangulation of the points, as counterclockwise triples of points.

    Duplicates are removed. If all points lie on one line (or there are fewer than three distinct points)
    there is no triangle and the result is empty. With four or more cocircular points the result is one of
    the Delaunay triangulations. Coordinates must be int (or Fraction) so that the predicates are exact.
    The triangles outside the hull are ghost triangles (a, b, GHOST); the ghost (a, b, GHOST) is in conflict
    with p when p is strictly right of the hull edge b -> a, or strictly inside the segment ab.
    Cost: O(n^2) time in the worst case (the conflict search of line L5 scans all triangles; the cavities
    have total size O(n^2) in the worst case and O(n) expected for a random insertion order); O(n) space.
    """
    pts = list(dict.fromkeys(points))  # @line L1
    n = len(pts)
    third = next((k for k in range(2, n) if orient(pts[0], pts[1], pts[k]) != 0), None)
    if third is None:  # @line L2
        return []
    a, b, c = (0, 1, third) if orient(pts[0], pts[1], pts[third]) > 0 else (0, third, 1)
    tri: dict[int, Triangle] = {}
    edge: dict[tuple[int, int], int] = {}  # directed edge -> the triangle that has it
    counter = [0]

    def add(t: Triangle) -> None:
        u, v, w = t
        if u == GHOST:
            u, v, w = v, w, u
        elif v == GHOST:
            u, v, w = w, u, v
        tid = counter[0]
        counter[0] += 1
        tri[tid] = (u, v, w)
        edge[(u, v)] = edge[(v, w)] = edge[(w, u)] = tid

    def remove(tid: int) -> None:
        u, v, w = tri.pop(tid)
        del edge[(u, v)], edge[(v, w)], edge[(w, u)]

    def in_conflict(t: Triangle, p: Point) -> bool:
        u, v, w = t
        if w != GHOST:
            return incircle(pts[u], pts[v], pts[w], p) > 0
        o = orient(pts[u], pts[v], p)
        if o != 0:
            return o > 0
        pu, pv = pts[u], pts[v]
        return (p[0] - pu[0]) * (p[0] - pv[0]) + (p[1] - pu[1]) * (p[1] - pv[1]) < 0

    for t in ((a, b, c), (b, a, GHOST), (c, b, GHOST), (a, c, GHOST)):  # @line L3
        add(t)
    for i in range(n):  # @line L4
        if i in (a, b, c):
            continue
        p = pts[i]
        start = next(tid for tid, t in tri.items() if in_conflict(t, p))  # @line L5
        cavity = {start}  # @line L6
        stack = [start]
        while stack:
            u, v, w = tri[stack.pop()]
            for x, y in ((u, v), (v, w), (w, u)):
                nb = edge[(y, x)]
                if nb not in cavity and in_conflict(tri[nb], p):
                    cavity.add(nb)
                    stack.append(nb)
        boundary = []  # @line L7
        for tid in cavity:
            u, v, w = tri[tid]
            for x, y in ((u, v), (v, w), (w, u)):
                if edge[(y, x)] not in cavity:
                    boundary.append((x, y))
        for tid in cavity:  # @line L8
            remove(tid)
        for x, y in boundary:  # @line L9
            add((x, y, i))
    return sorted((pts[u], pts[v], pts[w]) for u, v, w in tri.values() if w != GHOST)  # @line L10
