# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-zone-flatness/. The authors are listed in prov/5ZWKK1.jsonl.

"""Minimum zone flatness and straightness, exact.

The flatness of a set of points in 3D is the distance between the two closest
parallel planes that hold all the points between them, which is the width of
the set. The width is attained by a pair of parallel supporting planes of the
convex hull that touch a face and a vertex, or two edges (Houle and Toussaint
1988). The code builds the hull with an exact incremental method, then checks
every face against the farthest vertex and every pair of edges that admit
antipodal supporting planes.

All arithmetic is done with int and Fraction, so the result is exact. Floats
in the input are converted to the Fraction of their binary value.
"""

from fractions import Fraction
from math import sqrt


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _det(a, b, c):
    return _dot(_cross(a, b), c)


def _sign(x):
    return (x > 0) - (x < 0)


class Zone:
    """Two parallel planes lo <= normal . p <= hi that hold all points.

    The normal is exact and not normalized. width2 is the exact squared
    width (hi - lo)^2 / |normal|^2, and width is its float square root.
    kind is "face-vertex", "edge-edge" or "degenerate".
    """

    def __init__(self, normal, lo, hi, kind):
        self.normal = normal
        self.lo = lo
        self.hi = hi
        self.kind = kind
        nn = _dot(normal, normal)
        self.width2 = Fraction(0) if lo == hi else Fraction((hi - lo) ** 2) / nn
        self.width = sqrt(self.width2)

    def __repr__(self):
        return "Zone(width=%r, kind=%r)" % (self.width, self.kind)


def _exact(points, dim):
    out = []
    seen = set()
    for p in points:
        if len(p) != dim:
            raise ValueError("each point needs %d coordinates" % dim)
        q = tuple(Fraction(x) for x in p)
        if q not in seen:
            seen.add(q)
            out.append(q)
    return out


def convex_hull_3d(points):
    """Return the triangles (i, j, k) of the hull of the distinct points pts.

    The faces are oriented so that cross(pts[j] - pts[i], pts[k] - pts[i])
    points out of the hull. Coplanar adjacent triangles are allowed.
    Return None if the points are coplanar. Time O(n^2).
    """
    pts = points
    n = len(pts)
    if n < 4:
        return None
    i0 = 0
    i1 = next((i for i in range(n) if pts[i] != pts[i0]), None)
    if i1 is None:
        return None
    d01 = _sub(pts[i1], pts[i0])
    i2 = next((i for i in range(n) if _cross(d01, _sub(pts[i], pts[i0])) != (0, 0, 0)), None)
    if i2 is None:
        return None
    nrm = _cross(d01, _sub(pts[i2], pts[i0]))
    i3 = next((i for i in range(n) if _dot(nrm, _sub(pts[i], pts[i0])) != 0), None)
    if i3 is None:
        return None
    tet = (i0, i1, i2, i3)
    faces = []
    for skip in range(4):
        f = [tet[k] for k in range(4) if k != skip]
        if _orient(pts, f, pts[tet[skip]]) > 0:
            f[1], f[2] = f[2], f[1]
        faces.append(tuple(f))
    used = set(tet)
    for i in range(n):
        if i in used:
            continue
        p = pts[i]
        visible = [f for f in faces if _orient(pts, f, p) > 0]
        if not visible:
            continue
        vis_edges = set()
        for a, b, c in visible:
            vis_edges.update(((a, b), (b, c), (c, a)))
        horizon = [(a, b) for (a, b) in vis_edges if (b, a) not in vis_edges]
        vis_set = set(visible)
        faces = [f for f in faces if f not in vis_set]
        faces.extend((a, b, i) for (a, b) in horizon)
    return faces


def _orient(pts, f, p):
    a, b, c = pts[f[0]], pts[f[1]], pts[f[2]]
    return _det(_sub(b, a), _sub(c, a), _sub(p, a))


def _face_normal(pts, f):
    a, b, c = pts[f[0]], pts[f[1]], pts[f[2]]
    return _cross(_sub(b, a), _sub(c, a))


def _in_edge_cone(n1, n2, d, u):
    """True if u is a nonnegative combination of n1 and n2 (u is normal to d)."""
    t = _det(n1, n2, d)
    if t == 0:
        return _cross(n1, u) == (0, 0, 0) and _dot(n1, u) > 0
    s = _sign(t)
    return _sign(_det(n1, u, d)) in (0, s) and _sign(_det(u, n2, d)) in (0, s)


def _degenerate_zone(pts):
    """Zone of width 0 for coplanar or collinear points."""
    if len(pts) <= 1:
        return Zone((0, 0, 1), Fraction(0), Fraction(0), "degenerate")
    p0 = pts[0]
    d = _sub(pts[1], p0)
    for q in pts[2:]:
        nrm = _cross(d, _sub(q, p0))
        if nrm != (0, 0, 0):
            v = _dot(nrm, p0)
            return Zone(nrm, v, v, "degenerate")
    for axis in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        nrm = _cross(d, axis)
        if nrm != (0, 0, 0):
            v = _dot(nrm, p0)
            return Zone(nrm, v, v, "degenerate")
    raise AssertionError("unreachable")


def minimum_zone_flatness(points):
    """Return the Zone of least width that holds the 3D points.

    The zone width is the flatness of the points in the minimum zone sense.
    """
    pts = _exact(points, 3)
    faces = convex_hull_3d(pts)  # @line L2
    if faces is None:
        return _degenerate_zone(pts)  # @line L1
    verts = sorted({i for f in faces for i in f})
    best = None  # @line L3
    normals = [_face_normal(pts, f) for f in faces]
    # Face against the farthest vertex.
    for f, nf in zip(faces, normals):  # @line L4
        hi = _dot(nf, pts[f[0]])
        lo = min(_dot(nf, pts[v]) for v in verts)
        z = Zone(nf, lo, hi, "face-vertex")
        if best is None or z.width2 < best.width2:  # @line L5
            best = z
    # Edge against edge, when the two edges admit antipodal supporting planes.
    side = {}
    for k, (a, b, c) in enumerate(faces):
        side[(a, b)] = k
        side[(b, c)] = k
        side[(c, a)] = k
    edges = []
    for (a, b), k in side.items():
        if a < b:
            d = _sub(pts[b], pts[a])
            edges.append((pts[a], d, normals[k], normals[side[(b, a)]]))
    for i in range(len(edges)):  # @line L6
        pa, da, na1, na2 = edges[i]
        for j in range(i + 1, len(edges)):
            pb, db, nb1, nb2 = edges[j]
            n = _cross(da, db)  # @line L7
            if n == (0, 0, 0):
                continue
            for u in (n, (-n[0], -n[1], -n[2])):  # @line L8
                neg = (-u[0], -u[1], -u[2])
                if _in_edge_cone(na1, na2, da, u) and _in_edge_cone(nb1, nb2, db, neg):  # @line L9
                    z = Zone(u, _dot(u, pb), _dot(u, pa), "edge-edge")
                    if z.width2 < best.width2:  # @line L10
                        best = z
                    break
    return best  # @line L11


def convex_hull_2d(points):
    """Andrew's monotone chain on distinct exact points, counterclockwise."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def turn(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def minimum_zone_straightness(points):
    """Return (width2, normal, lo, hi) of the thinnest strip that holds 2D points.

    The width of a planar set is attained by a hull edge and the farthest
    hull vertex, so each hull edge is checked against all hull vertices.
    Time O(n log n + h^2) for h hull vertices.
    """
    pts = _exact(points, 2)
    hull = convex_hull_2d(pts)
    if len(hull) <= 1:
        return Fraction(0), (0, 1), Fraction(0), Fraction(0)
    if len(hull) == 2:
        (x0, y0), (x1, y1) = hull
        nrm = (y0 - y1, x1 - x0)
        v = nrm[0] * x0 + nrm[1] * y0
        return Fraction(0), nrm, v, v
    best = None
    h = len(hull)
    for i in range(h):
        (x0, y0), (x1, y1) = hull[i], hull[(i + 1) % h]
        nrm = (y1 - y0, x0 - x1)
        hi = nrm[0] * x0 + nrm[1] * y0
        lo = min(nrm[0] * x + nrm[1] * y for x, y in hull)
        w2 = Fraction((hi - lo) ** 2) / (nrm[0] ** 2 + nrm[1] ** 2)
        if best is None or w2 < best[0]:
            best = (w2, nrm, lo, hi)
    return best


if __name__ == "__main__":
    tet = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
    print(minimum_zone_flatness(tet))
    lp = [(1, 2, 2), (0, 0, 1), (4, 3, 10), (3, 3, 7), (1, 3, 4)]
    z = minimum_zone_flatness(lp)
    print(z, z.width2, z.normal)
