# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tetrahedral-delaunay-refinement/. The authors are listed in prov/VNAEW7.jsonl.

"""Shewchuk's tetrahedral Delaunay refinement (1998) for a box domain.

The input piecewise linear complex (PLC) is an axis-aligned box [0, a] x [0, b]
x [0, c] with integer sides, its 8 corners, 12 edges (segments) and 6 faces
(facets), plus optional input vertices inside the box. All its input angles are
90 degrees, so it satisfies Shewchuk's projection condition, and the refinement
terminates for every bound B >= 2 on the radius-edge ratio.

Coordinates are integers in units of 1/SCALE. A new vertex (a midpoint or a
circumcenter) is computed exactly and rounded once to this grid. Rounding keeps
a point on its box edge or face, since those coordinates are integers already.
Every predicate (orientation, insphere, encroachment, radius-edge test) is exact.

The domain is convex, so the faces of the tetrahedralization that lie on the box
are the subfacets: a face on the hull of a Delaunay tetrahedralization has an
empty circumcircle within its plane, so these faces form a 2D Delaunay
triangulation of each facet, as Shewchuk's algorithm keeps.
"""

from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Set, Tuple

from mg2geom import circumcenter3, dist2, dot, insphere, orient3d, radius_edge2, sub, tri_circumcenter3

SCALE = 1 << 20

Tet = Tuple[int, int, int, int]
Face = Tuple[int, int, int]
Seg = Tuple[int, int]


def _round(p: Sequence[Fraction]) -> tuple:
    return tuple(int(round(x)) for x in p)


class Refiner:
    def __init__(self, sides: Sequence[int], inner: Sequence[Sequence] = (), B=2, max_vertices: int = 5000):
        if len(sides) != 3 or min(sides) <= 0 or any(int(s) != s for s in sides):
            raise ValueError("need three positive integer sides")
        self.L = tuple(int(s) * SCALE for s in sides)
        self.B2 = Fraction(B) ** 2
        if self.B2 < 1:
            raise ValueError("B must be at least 1")
        self.max_vertices = max_vertices
        self.pts: List[tuple] = []
        self.kind: List[str] = []
        self.r2: List[Optional[int]] = []  # squared insertion radius, None for input vertices
        self.tets: Set[Tet] = set()
        self.face_tets: Dict[Face, Set[Tet]] = {}
        self.subsegs: Set[Seg] = set()
        self.subfacets: Dict[Face, tuple] = {}  # face -> (circumcenter, R^2, (axis, value))
        self.enc_segs: Set[Seg] = set()  # subsegments found encroached (a superset; checked again on use)
        self.enc_facets: Set[Face] = set()
        self.skinny: List[Tet] = []
        self.rejected = 0
        corners = [(x, y, z) for x in (0, self.L[0]) for y in (0, self.L[1]) for z in (0, self.L[2])]
        for p in corners:
            self._add_point(p, "input", None)
        # the 8 corners are cospherical, so any triangulation of the box is Delaunay:
        # take the 6 tetrahedra around the diagonal from corner 0 to corner 7
        for path in ((1, 3), (1, 5), (2, 3), (2, 6), (4, 5), (4, 6)):
            self._add_tet((0, path[0], path[1], 7))
        for i in range(3):  # the 12 box edges are the first subsegments
            for p in range(8):
                q = p | (4 >> i)
                if q != p:
                    self._add_subseg((p, q))
        for p in inner:
            q = tuple(Fraction(x) * SCALE for x in p)
            if len(q) != 3 or any(x.denominator != 1 for x in q) or not all(0 < q[k] < self.L[k] for k in range(3)):
                raise ValueError("inner vertices must lie strictly inside the box, on the 1/SCALE grid")
            q = tuple(int(x) for x in q)
            if q in self.pts:
                raise ValueError("repeated inner vertex")
            self.insert(q, "input")

    # bookkeeping
    def _add_point(self, p: tuple, kind: str, r2) -> int:
        self.pts.append(p)
        self.kind.append(kind)
        self.r2.append(r2)
        return len(self.pts) - 1

    def plane(self, f: Face) -> Optional[Tuple[int, int]]:
        """The box face (axis, value) that contains the triangle f, if any."""
        P = [self.pts[v] for v in f]
        for k in range(3):
            for s in (0, self.L[k]):
                if all(p[k] == s for p in P):
                    return (k, s)
        return None

    def _add_subseg(self, s: Seg) -> None:
        s = tuple(sorted(s))
        self.subsegs.add(s)
        if any(self.seg_encroached_by(s, p) for p in self.pts):
            self.enc_segs.add(s)

    def _add_tet(self, t: Tet) -> None:
        P = [self.pts[v] for v in t]
        if orient3d(*P) < 0:
            t = (t[1], t[0], t[2], t[3])
        self.tets.add(t)
        for f in faces_of(t):
            self.face_tets.setdefault(f, set()).add(t)
            if f not in self.subfacets:
                pl = self.plane(f)
                if pl is not None:
                    cc = tri_circumcenter3(*[self.pts[v] for v in f])
                    self.subfacets[f] = (cc, dist2(cc, self.pts[f[0]]), pl)
                    if any(self.facet_encroached_by(f, p) for p in self.pts):
                        self.enc_facets.add(f)
        if radius_edge2(*[self.pts[v] for v in t]) > self.B2:
            self.skinny.append(t)

    def _remove_tet(self, t: Tet) -> None:
        self.tets.discard(t)
        for f in faces_of(t):
            s = self.face_tets[f]
            s.discard(t)
            if not s:
                del self.face_tets[f]
                self.subfacets.pop(f, None)

    # encroachment: a vertex inside or on the diametral sphere of a subsegment,
    # or inside or on the equatorial sphere of a subfacet and off its plane
    def seg_encroached_by(self, s: Seg, p: tuple) -> bool:
        a, b = self.pts[s[0]], self.pts[s[1]]
        return p != a and p != b and dot(sub(p, a), sub(p, b)) <= 0

    def facet_encroached_by(self, f: Face, p: tuple) -> bool:
        cc, R2, (k, s) = self.subfacets[f]
        return p[k] != s and dist2(p, cc) <= R2

    def encroached_subseg(self) -> Optional[Seg]:
        while self.enc_segs:
            s = min(self.enc_segs)
            if s in self.subsegs and any(self.seg_encroached_by(s, p) for p in self.pts):
                return s
            self.enc_segs.discard(s)
        return None

    def encroached_subfacet(self) -> Optional[Face]:
        while self.enc_facets:
            f = min(self.enc_facets)
            if f in self.subfacets and any(self.facet_encroached_by(f, p) for p in self.pts):
                return f
            self.enc_facets.discard(f)
        return None

    # Bowyer-Watson insertion
    def locate_conflict(self, p: tuple) -> Tet:
        for t in self.tets:
            if insphere(*[self.pts[v] for v in t], p) > 0:
                return t
        raise AssertionError("no tetrahedron in conflict")

    def insert(self, p: tuple, kind: str, start: Optional[Tet] = None) -> int:
        if not all(0 <= p[k] <= self.L[k] for k in range(3)):
            raise AssertionError("point outside the domain")
        r2 = min(dist2(p, q) for q in self.pts)
        if r2 == 0:
            raise AssertionError("duplicate point")
        if len(self.pts) >= self.max_vertices:
            raise RuntimeError("too many vertices")
        if start is None or start not in self.tets or insphere(*[self.pts[v] for v in start], p) <= 0:
            start = self.locate_conflict(p)
        cavity = {start}
        stack = [start]
        while stack:  # @line L13
            t = stack.pop()
            for f in faces_of(t):
                for u in self.face_tets[f]:
                    if u not in cavity and insphere(*[self.pts[v] for v in u], p) > 0:
                        cavity.add(u)
                        stack.append(u)
        boundary = []
        for t in cavity:
            for f in faces_of(t):
                if not any(u in cavity for u in self.face_tets[f] if u != t):
                    boundary.append(f)
        v = self._add_point(p, kind, None if kind == "input" else r2)
        for t in cavity:
            self._remove_tet(t)
        for f in boundary:
            if orient3d(*[self.pts[w] for w in f], p) == 0:
                # p lies in the plane of this face; it can only be a face on the box boundary
                if self.plane(f) is None:
                    raise AssertionError("cavity is not star-shaped")
                continue
            self._add_tet(f + (v,))
        # subsegments that contain the new vertex are split in two
        for s in [s for s in self.subsegs if between(self.pts[s[0]], p, self.pts[s[1]])]:
            self.subsegs.discard(s)
            self._add_subseg((s[0], v))
            self._add_subseg((v, s[1]))
        # the new vertex may encroach old subsegments and subfacets
        for s in self.subsegs:
            if self.seg_encroached_by(s, p):
                self.enc_segs.add(s)
        for f in self.subfacets:
            if self.facet_encroached_by(f, p):
                self.enc_facets.add(f)
        return v

    def tet_with_edge(self, s: Seg) -> Optional[Tet]:
        for t in self.tets:
            if s[0] in t and s[1] in t:
                return t
        return None

    # the refinement loop
    def split_subseg(self, s: Seg) -> None:
        a, b = self.pts[s[0]], self.pts[s[1]]
        m = _round(tuple(Fraction(x + y, 2) for x, y in zip(a, b)))
        self.insert(m, "segment", self.tet_with_edge(s))  # @line L3

    def split_subfacet(self, f: Face) -> None:
        c = _round(self.subfacets[f][0])  # @line L5
        enc = [s for s in sorted(self.subsegs) if self.seg_encroached_by(s, c)]
        if enc:  # @line L6
            self.rejected += 1
            self.split_subseg(enc[0])
            return
        self.insert(c, "facet", next(iter(self.face_tets[f])))  # @line L7

    def step(self) -> bool:
        s = self.encroached_subseg()
        if s is not None:
            self.split_subseg(s)
            return True
        f = self.encroached_subfacet()  # @line L4
        if f is not None:
            self.split_subfacet(f)
            return True
        while self.skinny:  # @line L8
            t = self.skinny.pop(0)
            if t not in self.tets:
                continue
            c = _round(circumcenter3(*[self.pts[v] for v in t]))  # @line L9
            enc = [s for s in sorted(self.subsegs) if self.seg_encroached_by(s, c)]
            encf = [g for g in sorted(self.subfacets) if self.facet_encroached_by(g, c)]
            if enc or encf:  # @line L10
                self.rejected += 1
                self.skinny.append(t)
                if enc:
                    self.split_subseg(enc[0])
                else:
                    self.split_subfacet(self.pick_subfacet(encf, c))
                return True
            self.insert(c, "tet", t)  # @line L11
            return True
        return False  # @line L12

    def pick_subfacet(self, encf: List[Face], c: tuple) -> Face:
        """Prefer an encroached subfacet that contains the projection of c, as in Shewchuk's analysis."""
        for g in encf:
            k, _ = self.subfacets[g][2]
            P = [self.pts[v] for v in g]
            q = list(c)
            q[k] = P[0][k]
            i, j = [x for x in range(3) if x != k]
            o = [orient2(P[a], P[(a + 1) % 3], q, i, j) for a in range(3)]
            if all(x >= 0 for x in o) or all(x <= 0 for x in o):
                return g
        return encf[0]

    def run(self) -> None:
        while self.step():  # @line L2
            pass

    # results in the original units
    def points(self) -> List[Tuple[Fraction, ...]]:
        return [tuple(Fraction(x, SCALE) for x in p) for p in self.pts]


def orient2(a, b, c, i, j):
    return (b[i] - a[i]) * (c[j] - a[j]) - (b[j] - a[j]) * (c[i] - a[i])


def between(a, p, b) -> bool:
    """True if p lies strictly between a and b on the segment ab."""
    d = sub(b, a)
    e = sub(p, a)
    cr = (d[1] * e[2] - d[2] * e[1], d[2] * e[0] - d[0] * e[2], d[0] * e[1] - d[1] * e[0])
    if cr != (0, 0, 0):
        return False
    t = dot(e, d)
    return 0 < t < dot(d, d)


def faces_of(t: Tet) -> List[Face]:
    return [tuple(sorted(t[:i] + t[i + 1 :])) for i in range(4)]


def delaunay_refine(sides: Sequence[int], inner: Sequence[Sequence] = (), B=2, max_vertices: int = 5000) -> Refiner:
    """Refine the box with the given integer sides until no subsegment or subfacet is
    encroached and every tetrahedron has radius-edge ratio at most B.

    Returns the Refiner; its fields pts (in units of 1/SCALE) and tets hold the mesh.
    """
    r = Refiner(sides, inner, B, max_vertices)  # @line L1
    r.run()
    return r
