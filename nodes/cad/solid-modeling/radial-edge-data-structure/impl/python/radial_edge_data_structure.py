# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radial-edge-data-structure/. The authors are listed in prov/X79HMJ.jsonl.

"""Weiler's radial edge structure for a non-manifold polyhedral boundary.

Each face f has two faceuses, one for each side: f+ on the side of its normal N
and f- on the other side. Each faceuse has a loop of edgeuses. The edgeuses of
f+ follow the vertex list of f, which is counterclockwise seen from the tip of
N, and those of f- go the other way. For an edgeuse x:

- mate(x) is the edgeuse of the same edge on the other side of the same face;
- radial(x) is the edgeuse of the next face around the edge that faces the
  same wedge of space as x.

Around an edge e from v0 to v1, the faces are kept in counterclockwise order
about the direction v1 - v0. The edgeuse that runs from v0 to v1 faces the
wedge counterclockwise of its face. All tests are exact on integer points.
An edge can have any number of faces, also one (a free edge of a sheet), and
an edge with no face is a wire edge.
"""

from __future__ import annotations

from typing import Optional, Sequence

Vec = tuple[int, int, int]


class RadialEdgeError(ValueError):
    """The input does not fit the structure."""


def sub(p: Vec, q: Vec) -> Vec:
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a: Vec, b: Vec) -> int:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def det(a: Vec, b: Vec, d: Vec) -> int:
    """The sign of det[a, b, d] says if b is counterclockwise of a about d."""
    return dot(cross(a, b), d)


def inside_wedge(a: Vec, b: Vec, w: Vec, d: Vec) -> bool:
    """Is w strictly inside the wedge that turns counterclockwise about d from
    the fin a to the fin b? The fins are perpendicular to d, and w has neither
    the direction of a nor of b. If a and b have the same direction, the wedge
    is the full turn."""
    ab = det(a, b, d)
    if ab == 0 and dot(a, b) > 0:
        return True
    if ab > 0:
        return det(a, w, d) > 0 and det(w, b, d) > 0
    if ab == 0:
        return det(a, w, d) > 0
    return not (det(b, w, d) > 0 and det(w, a, d) > 0)


def same_direction(a: Vec, b: Vec) -> bool:
    return cross(a, b) == (0, 0, 0) and dot(a, b) > 0


class Face:
    __slots__ = ("id", "verts", "normal", "use")

    def __init__(self, fid: int, verts: list[int], normal: Vec) -> None:
        self.id, self.verts, self.normal = fid, verts, normal
        self.use: Optional[FaceUse] = None  # the faceuse f+


class FaceUse:
    __slots__ = ("face", "side", "mate", "eu")

    def __init__(self, face: Face, side: int) -> None:
        self.face, self.side = face, side
        self.mate: Optional[FaceUse] = None
        self.eu: Optional[EdgeUse] = None  # one edgeuse of the loop


class Edge:
    __slots__ = ("id", "v0", "v1", "eu", "n_faces")

    def __init__(self, eid: int, v0: int, v1: int) -> None:
        self.id, self.v0, self.v1 = eid, v0, v1
        self.eu: Optional[EdgeUse] = None  # an edgeuse that runs from v0 to v1
        self.n_faces = 0


class EdgeUse:
    __slots__ = ("id", "edge", "vertex", "fu", "next", "prev", "mate", "radial")

    def __init__(self, uid: int, edge: Edge, vertex: int, fu: Optional[FaceUse]) -> None:
        self.id, self.edge, self.vertex, self.fu = uid, edge, vertex, fu
        self.next: Optional[EdgeUse] = None
        self.prev: Optional[EdgeUse] = None
        self.mate: Optional[EdgeUse] = None
        self.radial: Optional[EdgeUse] = None

    def head(self) -> int:
        return self.edge.v1 if self.vertex == self.edge.v0 else self.edge.v0


class RadialEdge:
    def __init__(self, points: Sequence[Sequence[int]]) -> None:
        self.points: list[Vec] = [tuple(p) for p in points]  # type: ignore[misc]
        self.edges: list[Edge] = []
        self.faces: list[Face] = []
        self.edgeuses: list[EdgeUse] = []
        self.key: dict[frozenset[int], Edge] = {}
        self.vertex_uses: list[list[EdgeUse]] = [[] for _ in self.points]  # edgeuses that start at v

    # ----- geometry -----

    def newell(self, verts: Sequence[int]) -> Vec:
        """Twice the vector area of the polygon, exact."""
        n = (0, 0, 0)
        k = len(verts)
        for i in range(k):
            c = cross(self.points[verts[i]], self.points[verts[(i + 1) % k]])
            n = (n[0] + c[0], n[1] + c[1], n[2] + c[2])
        return n

    def fin(self, x: EdgeUse) -> Vec:
        """The direction from the edge of x into the face of x, perpendicular to the edge."""
        face = x.fu.face
        p, q = x.vertex, x.head()
        if x.fu.side < 0:
            p, q = q, p  # the direction in which f+ uses the edge
        return cross(face.normal, sub(self.points[q], self.points[p]))

    def axis(self, e: Edge) -> Vec:
        return sub(self.points[e.v1], self.points[e.v0])

    # ----- building -----

    def _new_edge(self, u: int, v: int) -> Edge:
        e = Edge(len(self.edges), u, v)
        self.edges.append(e)
        self.key[frozenset((u, v))] = e
        return e

    def _new_use(self, e: Edge, vertex: int, fu: Optional[FaceUse]) -> EdgeUse:
        x = EdgeUse(len(self.edgeuses), e, vertex, fu)
        self.edgeuses.append(x)
        self.vertex_uses[vertex].append(x)
        return x

    def add_wire(self, u: int, v: int) -> int:
        """Add a wire edge, an edge with no face. Returns the edge id."""
        if u == v or frozenset((u, v)) in self.key:
            raise RadialEdgeError("a wire edge needs two vertices that have no edge yet")
        e = self._new_edge(u, v)
        a, b = self._new_use(e, u, None), self._new_use(e, v, None)
        a.next = a.prev = b
        b.next = b.prev = a
        a.mate = a.radial = b
        b.mate = b.radial = a
        e.eu = a
        return e.id

    def add_face(self, verts: Sequence[int]) -> int:
        """Add a planar face given counterclockwise about its normal, and put it
        into the radial order of each of its edges. Returns the face id."""
        verts = list(verts)
        k = len(verts)
        if k < 3 or len(set(verts)) != k:
            raise RadialEdgeError("a face needs at least 3 distinct vertices")
        normal = self.newell(verts)
        if normal == (0, 0, 0):
            raise RadialEdgeError("the face has zero area")
        p0 = self.points[verts[0]]
        if any(dot(normal, sub(self.points[v], p0)) != 0 for v in verts):
            raise RadialEdgeError("the face is not planar")
        # check every edge before any change, so that a failure leaves the structure as it was
        for i in range(k):
            p, q = verts[i], verts[(i + 1) % k]
            e = self.key.get(frozenset((p, q)))
            if e is None:
                continue
            if e.n_faces == 0:
                raise RadialEdgeError("a face cannot use a wire edge")
            w = cross(normal, sub(self.points[q], self.points[p]))
            for x in self._edge_uses_forward(e):
                if same_direction(self.fin(x), w):
                    raise RadialEdgeError("two faces lie on the same half-plane at an edge")

        face = Face(len(self.faces), verts, normal)
        self.faces.append(face)
        plus, minus = FaceUse(face, 1), FaceUse(face, -1)
        plus.mate, minus.mate = minus, plus
        face.use = plus
        ups, downs = [], []
        for i in range(k):  # @line L5
            p, q = verts[i], verts[(i + 1) % k]
            e = self.key.get(frozenset((p, q))) or self._new_edge(p, q)
            ups.append(self._new_use(e, p, plus))
            downs.append(self._new_use(e, q, minus))
        for i in range(k):
            ups[i].next, ups[i].prev = ups[(i + 1) % k], ups[i - 1]
            downs[i].next, downs[i].prev = downs[i - 1], downs[(i + 1) % k]
            ups[i].mate, downs[i].mate = downs[i], ups[i]
        plus.eu, minus.eu = ups[0], downs[0]

        for i in range(k):  # @line L6
            e = ups[i].edge  # @line L7
            p, q = verts[i], verts[(i + 1) % k]
            x, y = (ups[i], downs[i]) if p == e.v0 else (downs[i], ups[i])  # @line L8
            w = cross(normal, sub(self.points[q], self.points[p]))
            if e.n_faces == 0:  # @line L9
                x.radial, y.radial = y, x
                e.eu = x
            else:
                d = self.axis(e)
                u = e.eu  # @line L10
                while not inside_wedge(self.fin(u), self.fin(u.radial), w, d):  # @line L11
                    u = u.radial.mate
                z = u.radial  # @line L12
                u.radial, y.radial = y, u
                x.radial, z.radial = z, x
            e.n_faces += 1
        return face.id

    def _edge_uses_forward(self, e: Edge) -> list[EdgeUse]:
        """The edgeuses of e that run from v0 to v1, one per face, in radial order."""
        out = []
        u0 = e.eu  # @line L1
        u = u0
        while True:
            out.append(u)  # @line L2
            u = u.radial.mate  # @line L3
            if u is u0:  # @line L4
                break
        return out

    # ----- queries -----

    def edge(self, u: int, v: int) -> Optional[int]:
        e = self.key.get(frozenset((u, v)))
        return None if e is None else e.id

    def edge_vertices(self, eid: int) -> tuple[int, int]:
        e = self.edges[eid]
        return e.v0, e.v1

    def radial_faces(self, eid: int) -> list[int]:
        """The faces at the edge, counterclockwise about v1 - v0. O(number of faces)."""
        e = self.edges[eid]
        if e.n_faces == 0:
            return []
        return [x.fu.face.id for x in self._edge_uses_forward(e)]

    def is_wire(self, eid: int) -> bool:
        return self.edges[eid].n_faces == 0

    def face_vertices(self, fid: int) -> list[int]:
        out = []
        x0 = self.faces[fid].use.eu
        x = x0
        while True:
            out.append(x.vertex)
            x = x.next
            if x is x0:
                break
        return out

    def face_edges(self, fid: int) -> list[int]:
        out = []
        x0 = self.faces[fid].use.eu
        x = x0
        while True:
            out.append(x.edge.id)
            x = x.next
            if x is x0:
                break
        return out

    def vertex_edges(self, v: int) -> list[int]:
        return sorted({x.edge.id for x in self.vertex_uses[v]})

    def vertex_faces(self, v: int) -> list[int]:
        return sorted({x.fu.face.id for x in self.vertex_uses[v] if x.fu is not None})

    def shells(self) -> list[set[tuple[int, int]]]:
        """The faceuses (face id, side) joined across edges by radial: each set
        is the part of the boundary of one region that is connected through
        edges. Wire edges are not in any set."""
        parent: dict[tuple[int, int], tuple[int, int]] = {}

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        for f in self.faces:
            parent[(f.id, 1)] = (f.id, 1)
            parent[(f.id, -1)] = (f.id, -1)
        for x in self.edgeuses:
            if x.fu is not None:
                a = find((x.fu.face.id, x.fu.side))
                b = find((x.radial.fu.face.id, x.radial.fu.side))
                parent[a] = b
        groups: dict[tuple[int, int], set[tuple[int, int]]] = {}
        for a in parent:
            groups.setdefault(find(a), set()).add(a)
        return list(groups.values())

    def check(self) -> None:
        """Check the pointers and the radial order."""
        for x in self.edgeuses:
            if x.mate.mate is not x or x.radial.radial is not x:
                raise RadialEdgeError("mate and radial must be involutions")
            if x.mate.edge is not x.edge or x.radial.edge is not x.edge:
                raise RadialEdgeError("mate and radial must stay on the edge")
            if x.mate.vertex == x.vertex or x.radial.vertex == x.vertex:
                raise RadialEdgeError("mate and radial must run the other way")
            if x.next.prev is not x or x.next.vertex != x.head():
                raise RadialEdgeError("the loop links do not agree")
            if x.fu is not None:
                if x.mate.fu is not x.fu.mate or x.next.fu is not x.fu:
                    raise RadialEdgeError("an edgeuse is on the wrong faceuse")
        for e in self.edges:
            if e.eu.vertex != e.v0:
                raise RadialEdgeError("the edge must point to a use from v0 to v1")
            if e.n_faces == 0:
                continue
            uses = self._edge_uses_forward(e)
            if len(uses) != e.n_faces or len({x.fu.face.id for x in uses}) != e.n_faces:
                raise RadialEdgeError("the radial cycle must meet each face once")
            d = self.axis(e)
            fins = [self.fin(x) for x in uses]
            m = len(fins)
            for i in range(m):
                if m > 1 and any(inside_wedge(fins[i], fins[(i + 1) % m], fins[j], d) for j in range(m) if j not in (i, (i + 1) % m)):
                    raise RadialEdgeError("the radial order is not counterclockwise")
