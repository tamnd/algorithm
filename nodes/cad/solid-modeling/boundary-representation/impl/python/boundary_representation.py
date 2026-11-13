# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-representation/. The authors are listed in prov/MR3WHM.jsonl.

"""A half-edge boundary representation (B-rep) of a polyhedral solid.

The topology is the hierarchy solid > shell > face > loop > half-edge > vertex.
A face is a list of loops: the first loop is the outer boundary and the other
loops are rings (holes in the face). Each loop is a list of vertex indices in
the order that keeps the face on the left when seen from outside the solid, so
the outer loop runs counterclockwise and the rings clockwise. This is the
right-hand rule: the fingers follow the loop and the thumb points out.

Coordinates are int or Fraction, and every geometric test is exact.
"""

from collections import Counter
from fractions import Fraction
from typing import Sequence, Union

Num = Union[int, Fraction]
Point = tuple[Num, Num, Num]


class InvalidBRep(ValueError):
    """The input does not describe a valid polyhedral solid."""


def _sub(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a: Point, b: Point) -> Num:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a: Point, b: Point) -> Point:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def newell(points: Sequence[Point]) -> Point:
    """Twice the vector area of a closed polygon: the sum of p_i x p_(i+1)."""
    sx = sy = sz = 0
    k = len(points)
    for i in range(k):
        c = _cross(points[i], points[(i + 1) % k])
        sx, sy, sz = sx + c[0], sy + c[1], sz + c[2]
    return (sx, sy, sz)


class BRep:
    """Half-edge B-rep. Half-edge h has origin, twin, next, prev and loop."""

    def __init__(self, points: Sequence[Point], faces: Sequence[Sequence[Sequence[int]]]) -> None:
        """Build the structure from vertex points and faces given as lists of loops.

        Raises InvalidBRep if a directed edge is used twice (a face is reversed
        or more than two faces meet at an edge) or if an edge has only one face.
        Time O(n) expected for n half-edges, with one hash map.
        """
        self.points: list[Point] = [tuple(p) for p in points]
        self.origin: list[int] = []
        self.twin: list[int] = []
        self.next: list[int] = []
        self.prev: list[int] = []
        self.loop: list[int] = []
        self.loop_face: list[int] = []  # the face of each loop
        self.loop_edge: list[int] = []  # one half-edge of each loop
        self.face_loops: list[list[int]] = []  # the loops of each face, outer loop first
        self.out: list[int] = [-1] * len(self.points)  # one half-edge out of each vertex
        self.key: dict[tuple[int, int], int] = {}
        for f, loops in enumerate(faces):  # @line L1
            if not loops:
                raise InvalidBRep(f"face {f} has no loop")
            self.face_loops.append([])
            for verts in loops:
                k = len(verts)
                if k < 3 or len(set(verts)) != k:
                    raise InvalidBRep(f"face {f} has a loop with fewer than 3 distinct vertices")
                lp = len(self.loop_face)
                self.loop_face.append(f)
                self.face_loops[f].append(lp)
                first = len(self.origin)
                self.loop_edge.append(first)
                for i, u in enumerate(verts):  # @line L2
                    v = verts[(i + 1) % k]
                    if not (0 <= u < len(self.points)):
                        raise InvalidBRep(f"vertex {u} does not exist")
                    if (u, v) in self.key:
                        raise InvalidBRep(f"the directed edge {u}->{v} is used twice")
                    h = len(self.origin)  # @line L3
                    self.key[(u, v)] = h
                    self.origin.append(u)
                    self.loop.append(lp)
                    self.twin.append(-1)
                    self.next.append(first + (i + 1) % k)  # @line L4
                    self.prev.append(first + (i - 1) % k)
        for (u, v), h in self.key.items():  # @line L5
            t = self.key.get((v, u))
            if t is None:
                raise InvalidBRep(f"the edge {u}-{v} has only one face")
            self.twin[h] = t
        for h, u in enumerate(self.origin):  # @line L6
            if self.out[u] < 0:
                self.out[u] = h

    # ------------------------------------------------------------ queries

    def face(self, h: int) -> int:
        """The face on the left of half-edge h. O(1)."""
        return self.loop_face[self.loop[h]]

    def loop_vertices(self, lp: int) -> list[int]:
        """The vertices of loop lp in order. O(length of the loop)."""
        out = []
        h = self.loop_edge[lp]
        while True:
            out.append(self.origin[h])
            h = self.next[h]
            if h == self.loop_edge[lp]:
                return out

    def face_boundary(self, f: int) -> list[list[int]]:
        """The loops of face f as vertex lists, outer loop first."""
        return [self.loop_vertices(lp) for lp in self.face_loops[f]]

    def edge_faces(self, u: int, v: int) -> tuple[int, int]:
        """The faces on the left and on the right of the edge from u to v. O(1) expected."""
        h = self.key[(u, v)]
        return self.face(h), self.face(self.twin[h])

    def outgoing(self, v: int) -> list[int]:
        """The half-edges out of v, counterclockwise seen from outside. O(degree)."""
        start = self.out[v]
        if start < 0:
            return []
        res = []
        h = start
        while True:  # @line L7
            res.append(h)
            h = self.twin[self.prev[h]]
            if h == start:
                return res

    def faces_around(self, v: int) -> list[int]:
        """The faces at vertex v in cyclic order (a face is listed once per corner)."""
        return [self.face(h) for h in self.outgoing(v)]

    def neighbors(self, v: int) -> list[int]:
        """The vertices joined to v by an edge, in cyclic order."""
        return [self.origin[self.twin[h]] for h in self.outgoing(v)]

    def adjacent_faces(self, f: int) -> set[int]:
        """The faces that share an edge with face f."""
        res = set()
        for lp in self.face_loops[f]:
            h = self.loop_edge[lp]
            while True:
                res.add(self.face(self.twin[h]))
                h = self.next[h]
                if h == self.loop_edge[lp]:
                    break
        return res

    def shells(self) -> list[list[int]]:
        """The shells: the components of the faces, linked across edges."""
        seen = [False] * len(self.face_loops)
        res = []
        for f0 in range(len(self.face_loops)):
            if seen[f0]:
                continue
            seen[f0] = True
            comp, stack = [], [f0]
            while stack:
                f = stack.pop()
                comp.append(f)
                for g in self.adjacent_faces(f):
                    if not seen[g]:
                        seen[g] = True
                        stack.append(g)
            res.append(sorted(comp))
        return res

    def volume(self) -> Fraction:
        """The signed volume, (1/6) sum over faces of q_f . (sum of p_i x p_(i+1)) over all loops."""
        total = 0
        for f in range(len(self.face_loops)):
            loops = [[self.points[v] for v in vs] for vs in self.face_boundary(f)]
            q = loops[0][0]
            for pts in loops:
                total += _dot(q, newell(pts))
        return Fraction(total, 6)

    # ------------------------------------------------------------ validity

    def validate(self) -> dict[str, int]:
        """Check the topology and the exact geometry; return the counts V, E, F, L, R, S, H.

        Raises InvalidBRep on the first failed check. It does not test that
        faces of different shells, or far-apart faces, do not intersect.
        """
        n = len(self.origin)
        for h in range(n):  # @line L8
            t = self.twin[h]
            if self.twin[t] != h or t == h or self.origin[t] != self.origin[self.next[h]]:
                raise InvalidBRep(f"half-edge {h} has a bad twin")
        degree = Counter(self.origin)
        for v in range(len(self.points)):  # @line L9
            if degree[v] == 0:
                raise InvalidBRep(f"vertex {v} is on no face")
            if len(self.outgoing(v)) != degree[v]:
                raise InvalidBRep(f"vertex {v} is non-manifold: its faces make more than one fan")
        shells = self.shells()  # @line L10
        holes = 0
        for comp in shells:  # @line L11
            loops = sum(len(self.face_loops[f]) for f in comp)
            hs = [self.loop_edge[lp] for f in comp for lp in self.face_loops[f]]
            half = []
            for h in hs:
                g = h
                while True:
                    half.append(g)
                    g = self.next[g]
                    if g == h:
                        break
            verts = {self.origin[h] for h in half}
            chi = len(verts) - len(half) // 2 + len(comp) - (loops - len(comp))
            if chi > 2 or chi % 2:
                raise InvalidBRep(f"a shell has V - E + F - R = {chi}, which is not 2 - 2g")
            holes += (2 - chi) // 2
        for f in range(len(self.face_loops)):  # @line L12
            loops = [[self.points[v] for v in vs] for vs in self.face_boundary(f)]
            nrm = newell(loops[0])
            if nrm == (0, 0, 0):
                raise InvalidBRep(f"face {f} has a degenerate outer loop")
            q = loops[0][0]
            for i, pts in enumerate(loops):
                if any(_dot(nrm, _sub(p, q)) != 0 for p in pts):
                    raise InvalidBRep(f"face {f} is not planar")
                if i > 0 and _dot(nrm, newell(pts)) >= 0:
                    raise InvalidBRep(f"a ring of face {f} has the orientation of the outer loop")
        for comp in shells:  # @line L13
            sub = 0
            for f in comp:
                loops = [[self.points[v] for v in vs] for vs in self.face_boundary(f)]
                sub += sum(_dot(loops[0][0], newell(pts)) for pts in loops)
            if sub == 0:
                raise InvalidBRep("a shell encloses no volume")
        if self.volume() <= 0:
            raise InvalidBRep("the solid has no positive volume: the faces point inward")
        nf = len(self.face_loops)
        nl = len(self.loop_face)
        return {"V": len(self.points), "E": n // 2, "F": nf, "L": nl, "R": nl - nf, "S": len(shells), "H": holes}
