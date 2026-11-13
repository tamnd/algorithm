# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euler-operators/. The authors are listed in prov/23HY3M.jsonl.

"""Euler operators on a half-edge boundary model (the topology only).

A face has an outer loop and a list of rings. A loop is a cycle of half-edges
linked by next and prev. A loop that is a single vertex has one lone half-edge
whose edge is None. An edge has two half-edges in opposite directions: he1 runs
from the first vertex to the second and he2 runs back. The twin of a half-edge
is the other half-edge of its edge.

Orientation: the loops of a face run so that the face is on the left seen from
outside the solid (the right-hand rule). The operators always give the two
half-edges of an edge opposite directions, so they keep a consistent
orientation. Points are stored but never used: the operators change only the
topology, and the caller must keep the geometry valid.

The operators and the change in (V, E, F, L, S, H):
    mvsf  (+1, 0, +1, +1, +1, 0)    kvsf   is the inverse
    mev   (+1, +1, 0, 0, 0, 0)      kev    is the inverse
    mef   (0, +1, +1, +1, 0, 0)     kef    is the inverse
    kemr  (0, -1, 0, +1, 0, 0)      mekr   is the inverse
    kfmrh (0, 0, -1, 0, 0, +1), or (0, 0, -1, 0, -1, 0) if it joins two shells;
                                    mfkrh  is the inverse
"""

from __future__ import annotations

from typing import Any, Optional


class EulerError(ValueError):
    """The arguments do not meet the precondition of the operator."""


class Vertex:
    __slots__ = ("id", "point")

    def __init__(self, vid: int, point: Any) -> None:
        self.id = vid
        self.point = point


class Edge:
    __slots__ = ("he1", "he2")


class HalfEdge:
    __slots__ = ("vertex", "loop", "edge", "next", "prev")

    def __init__(self, vertex: Vertex, edge: Optional[Edge]) -> None:
        self.vertex = vertex
        self.edge = edge
        self.loop: Loop
        self.next: HalfEdge = self
        self.prev: HalfEdge = self


class Loop:
    __slots__ = ("he", "face")

    def __init__(self, face: "Face") -> None:
        self.face = face
        self.he: HalfEdge


class Face:
    __slots__ = ("outer", "rings")

    def __init__(self) -> None:
        self.outer: Loop
        self.rings: list[Loop] = []

    def loops(self) -> list[Loop]:
        return [self.outer] + self.rings


def twin(h: HalfEdge) -> HalfEdge:
    """The other half-edge of the edge of h."""
    e = h.edge
    if e is None:
        raise EulerError("a lone half-edge has no twin")
    return e.he2 if e.he1 is h else e.he1


def is_lone(h: HalfEdge) -> bool:
    return h.edge is None


def walk(h: HalfEdge, stop: Optional[HalfEdge] = None) -> list[HalfEdge]:
    """The half-edges h, next[h], ... before stop (the whole cycle if stop is None).

    A lone half-edge gives the empty list, and walk(h, h) is empty.
    """
    if is_lone(h):
        return []
    if stop is h:
        return []
    out = [h]
    g = h.next
    while g is not h and g is not stop:
        out.append(g)
        g = g.next
    return out


class Model:
    """A set of shells. The counts V, E, F and L are the sizes of the stores, S is
    found by a search, and H is kept by kfmrh and mfkrh."""

    def __init__(self) -> None:
        # dicts used as ordered sets, so that iteration does not depend on id()
        self.vertices: dict[int, Vertex] = {}
        self.edges: dict[Edge, None] = {}
        self.faces: dict[Face, None] = {}
        self.loops: dict[Loop, None] = {}
        self.holes = 0
        self._fresh = 0

    # ----- helpers -----

    def _vertex(self, point: Any, vid: Optional[int]) -> Vertex:
        if vid is None:
            vid = self._fresh
        if vid in self.vertices:
            raise EulerError(f"vertex id {vid} is in use")
        self._fresh = max(self._fresh, vid + 1)
        v = Vertex(vid, point)
        self.vertices[vid] = v
        return v

    def _edge(self, u: Vertex, w: Vertex) -> tuple[HalfEdge, HalfEdge]:
        e = Edge()
        a, b = HalfEdge(u, e), HalfEdge(w, e)
        e.he1, e.he2 = a, b
        self.edges[e] = None
        return a, b

    def _relink(self, loop: Loop, hs: list[HalfEdge], vertex: Vertex) -> None:
        """Make hs the cycle of loop. An empty hs gives a lone half-edge at vertex."""
        if not hs:
            hs = [HalfEdge(vertex, None)]
        k = len(hs)
        for i, h in enumerate(hs):
            h.next = hs[(i + 1) % k]
            h.prev = hs[i - 1]
            h.loop = loop
        loop.he = hs[0]

    def _check_he(self, h: HalfEdge) -> None:
        if getattr(h, "loop", None) not in self.loops:
            raise EulerError("the half-edge is not in the model")

    def shell(self, f: Face) -> set[Face]:
        """The faces of the shell of f: a search across the edges."""
        seen = {f}
        stack = [f]
        while stack:
            g = stack.pop()
            for loop in g.loops():
                for h in walk(loop.he):
                    k = twin(h).loop.face
                    if k not in seen:
                        seen.add(k)
                        stack.append(k)
        return seen

    def shells(self) -> list[set[Face]]:
        out: list[set[Face]] = []
        done: set[Face] = set()
        for f in self.faces:
            if f not in done:
                s = self.shell(f)
                done |= s
                out.append(s)
        return out

    def counts(self) -> dict[str, int]:
        return {
            "V": len(self.vertices),
            "E": len(self.edges),
            "F": len(self.faces),
            "L": len(self.loops),
            "S": len(self.shells()),
            "H": self.holes,
        }

    # ----- make and kill vertex, shell and face -----

    def mvsf(self, point: Any = None, vid: Optional[int] = None) -> Face:
        """Make vertex, shell and face: a new shell with one vertex and one face
        whose only loop is that vertex. Returns the face."""
        v = self._vertex(point, vid)  # @line L1
        f = Face()
        loop = Loop(f)
        f.outer = loop
        self.faces[f] = None
        self.loops[loop] = None
        self._relink(loop, [], v)
        return f

    def kvsf(self, f: Face) -> Vertex:
        """Kill vertex, shell and face: the inverse of mvsf. Returns the vertex."""
        if f not in self.faces or f.rings or not is_lone(f.outer.he):
            raise EulerError("kvsf needs a face whose only loop is a lone vertex")
        v = f.outer.he.vertex
        del self.vertices[v.id]
        del self.loops[f.outer]
        del self.faces[f]
        return v

    # ----- make and kill edge and vertex -----

    def mev(self, h: HalfEdge, point: Any = None, vid: Optional[int] = None) -> HalfEdge:
        """Make edge and vertex: a new edge from v = h.vertex to a new vertex w, in
        the corner of v before h. Returns the half-edge from v to w."""
        self._check_he(h)
        v = h.vertex
        w = self._vertex(point, vid)
        a, b = self._edge(v, w)  # @line L2
        loop = h.loop
        if is_lone(h):  # @line L3
            self._relink(loop, [a, b], v)
        else:
            p = h.prev
            p.next, a.prev = a, p
            a.next, b.prev = b, a
            b.next, h.prev = h, b
            a.loop = b.loop = loop
        return a

    def kev(self, a: HalfEdge) -> HalfEdge:
        """Kill edge and vertex: a runs from v to w, and w has no other edge.
        Returns the half-edge h with mev(h) as the inverse."""
        self._check_he(a)
        b = twin(a)
        if a.next is not b:
            raise EulerError("kev needs an edge whose far vertex has degree 1")
        v, w = a.vertex, b.vertex
        loop = a.loop
        if b.next is a:
            self._relink(loop, [], v)
            h = loop.he
        else:
            p, h = a.prev, b.next
            p.next, h.prev = h, p
            loop.he = h
        del self.edges[a.edge]
        del self.vertices[w.id]
        return h

    # ----- make and kill edge and face -----

    def mef(self, h1: HalfEdge, h2: HalfEdge) -> HalfEdge:
        """Make edge and face: h1 and h2 lie in one loop. A new edge runs from
        h1.vertex to h2.vertex, and the half-edges h1, ..., prev(h2) go to a new
        face. Returns the new half-edge a in the old face; twin(a) is in the new face."""
        self._check_he(h1)
        self._check_he(h2)
        loop = h1.loop
        if h2.loop is not loop:
            raise EulerError("mef needs two half-edges of one loop")
        x = walk(h1, h2)  # @line L4
        y = walk(h1) if h1 is h2 else walk(h2, h1)
        a, b = self._edge(h1.vertex, h2.vertex)  # @line L5
        f2 = Face()  # @line L6
        loop2 = Loop(f2)
        f2.outer = loop2
        self.faces[f2] = None
        self.loops[loop2] = None
        self._relink(loop, y + [a], h1.vertex)
        self._relink(loop2, x + [b], h2.vertex)
        return a

    def kef(self, a: HalfEdge) -> tuple[HalfEdge, HalfEdge]:
        """Kill edge and face: the faces of a and twin(a) differ. The face of
        twin(a) is deleted and its other loops become rings of the face of a.
        Returns (h1, h2) with mef(h1, h2) as the inverse, if the loop of a was
        longer than a alone."""
        self._check_he(a)
        b = twin(a)
        la, lb = a.loop, b.loop
        f1, f2 = la.face, lb.face
        if f1 is f2:
            raise EulerError("kef needs an edge between two faces")
        x = walk(b.next, b) if b.next is not b else []
        y = walk(a.next, a) if a.next is not a else []
        self._relink(la, x + y, a.vertex)
        for ring in f2.loops():
            if ring is not lb:
                ring.face = f1
                f1.rings.append(ring)
        del self.edges[a.edge]
        del self.loops[lb]
        del self.faces[f2]
        h1 = x[0] if x else (y[0] if y else la.he)
        h2 = y[0] if y else h1
        return h1, h2

    # ----- kill edge make ring, and its inverse -----

    def kemr(self, a: HalfEdge) -> tuple[HalfEdge, HalfEdge]:
        """Kill edge, make ring: a and twin(a) lie in one loop (a, X, b, Y). The loop
        keeps Y, and X becomes a new ring of the same face. Returns (h1, h2) with
        mekr(h1, h2) as the inverse."""
        self._check_he(a)
        b = twin(a)
        loop = a.loop
        if b.loop is not loop:
            raise EulerError("kemr needs an edge with both half-edges in one loop")
        x = walk(a.next, b)  # @line L7
        y = walk(b.next, a)
        v, w = a.vertex, b.vertex
        f = loop.face
        ring = Loop(f)
        f.rings.append(ring)
        self.loops[ring] = None
        del self.edges[a.edge]
        self._relink(loop, y, v)
        self._relink(ring, x, w)
        return loop.he, ring.he

    def mekr(self, h1: HalfEdge, h2: HalfEdge) -> HalfEdge:
        """Make edge, kill ring: h1 and h2 lie in two loops of one face. A new edge
        joins h1.vertex to h2.vertex, and the two loops become one. Returns the new
        half-edge from h1.vertex to h2.vertex."""
        self._check_he(h1)
        self._check_he(h2)
        l1, l2 = h1.loop, h2.loop
        f = l1.face
        if l1 is l2 or l2.face is not f:
            raise EulerError("mekr needs two loops of one face")
        a, b = self._edge(h1.vertex, h2.vertex)
        hs = [a] + walk(h2) + [b] + walk(h1)
        if f.outer is l2:
            f.rings.remove(l1)
            f.outer = l1
        else:
            f.rings.remove(l2)
        del self.loops[l2]
        self._relink(l1, hs, h1.vertex)
        return a

    # ----- kill face make ring and hole, and its inverse -----

    def kfmrh(self, f1: Face, f2: Face) -> Loop:
        """Kill face, make ring and hole: the only loop of f2 becomes a ring of f1.
        If f1 and f2 are in one shell, the genus grows by 1; otherwise two shells
        become one. Returns the new ring."""
        if f1 not in self.faces or f2 not in self.faces or f1 is f2:
            raise EulerError("kfmrh needs two faces")
        if f2.rings:
            raise EulerError("kfmrh needs a face f2 with one loop")
        same = f2 in self.shell(f1)  # @line L8
        ring = f2.outer  # @line L9
        ring.face = f1
        f1.rings.append(ring)
        del self.faces[f2]
        if same:  # @line L10
            self.holes += 1
        return ring

    def mfkrh(self, ring: Loop) -> Face:
        """Make face, kill ring and hole: a ring of a face becomes the outer loop of
        a new face. Returns the new face."""
        if ring not in self.loops or ring.face.outer is ring:
            raise EulerError("mfkrh needs a ring")
        f1 = ring.face
        f1.rings.remove(ring)
        f2 = Face()
        f2.outer = ring
        ring.face = f2
        self.faces[f2] = None
        if f2 in self.shell(f1):
            self.holes -= 1
        return f2

    # ----- the check -----

    def check(self) -> dict[str, int]:
        """Check the structure and return the counts. Raises EulerError if a
        pointer is wrong, a vertex is not one fan, or a shell has an Euler
        characteristic that is odd or greater than 2, or if the holes do not add up."""
        out_of: dict[Vertex, list[HalfEdge]] = {v: [] for v in self.vertices.values()}
        on_edge: dict[Edge, int] = {e: 0 for e in self.edges}
        for f in self.faces:
            for loop in f.loops():
                if loop not in self.loops or loop.face is not f:
                    raise EulerError("a loop and its face do not agree")
        n_loops = sum(len(f.loops()) for f in self.faces)
        if n_loops != len(self.loops):
            raise EulerError("a loop has no face")
        for loop in self.loops:
            h = loop.he
            k = 0
            while True:
                if h.loop is not loop or h.next.prev is not h:
                    raise EulerError("next, prev and loop do not agree")
                if h.vertex not in out_of:
                    raise EulerError("a half-edge has no vertex")
                out_of[h.vertex].append(h)
                if is_lone(h):
                    if h.next is not h:
                        raise EulerError("a lone half-edge is not alone in its loop")
                else:
                    if h.edge not in on_edge:
                        raise EulerError("a half-edge has no edge")
                    on_edge[h.edge] += 1
                    if twin(h).vertex is not h.next.vertex:
                        raise EulerError("the twins of an edge do not run in opposite directions")
                k += 1
                h = h.next
                if h is loop.he:
                    break
        for e, c in on_edge.items():
            if c != 2 or e.he1.edge is not e or e.he2.edge is not e:
                raise EulerError("an edge is not used by its two half-edges")
        for v, hs in out_of.items():
            if not hs:
                raise EulerError("a vertex has no half-edge")
            if any(is_lone(h) for h in hs):
                if len(hs) != 1:
                    raise EulerError("a lone vertex has edges")
                continue
            fan = {hs[0]}
            g = twin(hs[0].prev)
            while g is not hs[0]:
                fan.add(g)
                g = twin(g.prev)
            if len(fan) != len(hs):
                raise EulerError("the faces at a vertex do not make one fan")
        genus = 0
        for s in self.shells():
            hs_ = [h for f in s for loop in f.loops() for h in walk(loop.he)]
            verts = {h.vertex for f in s for loop in f.loops() for h in [loop.he] + walk(loop.he)}
            nv = len(verts)
            ne = len(hs_) // 2
            nf = len(s)
            nr = sum(len(f.rings) for f in s)
            chi = nv - ne + nf - nr
            if chi > 2 or chi % 2:
                raise EulerError("a shell has an impossible Euler characteristic")
            genus += (2 - chi) // 2
        if genus != self.holes:
            raise EulerError("the holes do not add up")
        return self.counts()
