# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/medial-surface-of-a-solid/. The authors are listed in prov/B7FYY7.jsonl.

"""The seams and junctions of the medial surface of a convex polyhedron.

The polyhedron is P = {x : n_i . x <= b_i} with unit normals n_i whose
coordinates are rational, such as (1, 2, 2)/3, so that the distance
b_i - n_i . x from an inside point to the plane of face i is rational and
every computation is exact with Fraction.

For an inside point x of a convex polyhedron, the nearest boundary points
are the feet on the nearest face planes, so x is on the medial surface
exactly when two or more faces are nearest. The medial surface is made of
flat sheets (two faces nearest), seams (three or more faces nearest along a
line) and junctions (the ends of seams inside P). The code traces the seams
from the vertices of P, as Sherbrooke, Patrikalakis and Brisson trace seams
from the boundary in the general case. Degenerate ties, such as the centre
of a cube where six faces are nearest, are handled.

Cost: finding the vertices and faces of P by brute force takes O(F^4) for F
planes. Each junction with a tie set T tries O(|T|^3) directions, and each
seam takes O(F) time to find its end, so the trace takes O(J (|T|^3 + F))
for J junctions and vertices.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from typing import Sequence

Vec = tuple[Fraction, Fraction, Fraction]
Plane = tuple[Vec, Fraction]


def dot(a: Vec, b: Vec) -> Fraction:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def det3(a: Vec, b: Vec, c: Vec) -> Fraction:
    return dot(a, cross(b, c))


def solve3(rows: Sequence[Vec], rhs: Sequence[Fraction]) -> Vec | None:
    """Cramer's rule for a 3 by 3 system; None if it is singular."""
    d = det3(rows[0], rows[1], rows[2])
    if d == 0:
        return None
    cols = [tuple(r[k] for r in rows) for k in range(3)]
    out = []
    for k in range(3):
        c = list(cols)
        c[k] = tuple(rhs)
        out.append(det3(c[0], c[1], c[2]) / d)  # transpose has the same det
    return (out[0], out[1], out[2])


class ConvexPolyhedron:
    """P = {x : n_i . x <= b_i}. Precondition: every n_i has length 1, all
    data are Fractions, and P is bounded with nonempty interior."""

    def __init__(self, planes: Sequence[tuple[Sequence[Fraction], Fraction]]):
        self.planes: list[Plane] = [((Fraction(n[0]), Fraction(n[1]), Fraction(n[2])), Fraction(b))
                                    for n, b in planes]
        for n, _ in self.planes:
            if dot(n, n) != 1:
                raise ValueError("normals must be unit vectors")
        self.vertices = self._vertices()
        self.faces = self._faces()

    def dist(self, i: int, x: Vec) -> Fraction:
        n, b = self.planes[i]
        return b - dot(n, x)

    def inside(self, x: Vec) -> bool:
        return all(self.dist(i, x) >= 0 for i in range(len(self.planes)))

    def _vertices(self) -> list[Vec]:
        out: set[Vec] = set()
        for i, j, k in combinations(range(len(self.planes)), 3):
            x = solve3([self.planes[i][0], self.planes[j][0], self.planes[k][0]],
                       [self.planes[i][1], self.planes[j][1], self.planes[k][1]])
            if x is not None and self.inside(x):
                out.add(x)
        return sorted(out)

    def _faces(self) -> list[int]:
        """The planes that carry a facet: at least three vertices on the plane
        that are not on one line."""
        out = []
        for i in range(len(self.planes)):
            on = [v for v in self.vertices if self.dist(i, v) == 0]
            if any(cross(sub(b, a), sub(c, a)) != (0, 0, 0) for a, b, c in combinations(on, 3)):
                out.append(i)
        return out

    def nearest(self, x: Vec) -> tuple[Fraction, frozenset[int]]:
        """The distance from x to the boundary and the faces that attain it."""
        ds = {i: self.dist(i, x) for i in self.faces}
        r = min(ds.values())
        return r, frozenset(i for i, d in ds.items() if d == r)


Seam = tuple[Vec, Vec, frozenset[int]]


def medial_seams(P: ConvexPolyhedron) -> tuple[dict[Vec, tuple[Fraction, frozenset[int]]], list[Seam]]:
    """Trace the seam graph of the medial surface of P.

    Returns the junctions and vertices of P, each with its radius and its set
    of nearest faces, and the seams as (start, end, faces nearest along it)."""
    queue: list[Vec] = list(P.vertices)  # @line L1
    junctions: dict[Vec, tuple[Fraction, frozenset[int]]] = {}  # @line L2
    seams: dict[tuple[frozenset[Vec], frozenset[int]], Seam] = {}
    while queue:  # @line L3
        x = queue.pop()  # @line L4
        if x in junctions:  # @line L5
            continue
        rho, T = P.nearest(x)  # @line L6
        junctions[x] = (rho, T)
        ns = {i: P.planes[i][0] for i in P.faces}
        for i, j, k in combinations(sorted(T), 3):  # @line L7
            w = cross(sub(ns[i], ns[j]), sub(ns[i], ns[k]))
            if w == (0, 0, 0):
                continue
            for v in (w, (-w[0], -w[1], -w[2])):
                r = max(dot(ns[l], v) for l in T)  # @line L8
                S = frozenset(l for l in T if dot(ns[l], v) == r)
                if dot(ns[i], v) != r or not (rho > 0 or r < 0):  # @line L9
                    continue
                # along x + t v the faces of S are at distance rho - t r
                best = rho / r if r > 0 else None  # @line L10
                for l in P.faces:
                    if l in S:
                        continue
                    a = dot(ns[l], v)
                    if a > r:
                        t = (P.dist(l, x) - rho) / (a - r)
                        if best is None or t < best:
                            best = t
                assert best is not None and best > 0, "P must be bounded"
                y = (x[0] + best * v[0], x[1] + best * v[1], x[2] + best * v[2])  # @line L11
                key = (frozenset((x, y)), S)
                if key not in seams:
                    seams[key] = (x, y, S)
                queue.append(y)
    return junctions, list(seams.values())  # @line L12


def sheet_points(junctions: dict[Vec, tuple[Fraction, frozenset[int]]], i: int, j: int) -> list[Vec]:
    """The corners of the sheet of faces i and j: the traced points whose
    nearest faces include both. The sheet is their convex hull."""
    return sorted(x for x, (_, T) in junctions.items() if i in T and j in T)


def in_convex_hull_planar(pts: Sequence[Vec], x: Vec) -> bool:
    """Is x in the convex hull of the coplanar points pts? Exact, by
    projection to the coordinate plane where the points are not degenerate."""
    if not pts:
        return False
    if len(pts) == 1:
        return x == pts[0]
    a = pts[0]
    # the plane (or line) of the points
    b = next((p for p in pts if p != a), None)
    if b is None:
        return x == a
    c = next((p for p in pts if cross(sub(b, a), sub(p, a)) != (0, 0, 0)), None)
    if c is None:  # collinear: a segment
        d = sub(b, a)
        if cross(d, sub(x, a)) != (0, 0, 0):
            return False
        ts = [dot(sub(p, a), d) for p in pts]
        tx = dot(sub(x, a), d)
        return min(ts) <= tx <= max(ts)
    n = cross(sub(b, a), sub(c, a))
    if dot(n, sub(x, a)) != 0:
        return False
    k = max(range(3), key=lambda q: abs(n[q]))
    ax = [q for q in range(3) if q != k]
    pr = sorted({(p[ax[0]], p[ax[1]]) for p in pts})
    q = (x[ax[0]], x[ax[1]])

    def turn(o, p1, p2):
        return (p1[0] - o[0]) * (p2[1] - o[1]) - (p1[1] - o[1]) * (p2[0] - o[0])

    lower: list = []
    for p in pr:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list = []
    for p in reversed(pr):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    return all(turn(hull[m], hull[(m + 1) % len(hull)], q) >= 0 for m in range(len(hull)))
