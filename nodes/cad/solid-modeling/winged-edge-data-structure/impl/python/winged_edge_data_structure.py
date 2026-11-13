# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winged-edge-data-structure/. The authors are listed in prov/4Q9BTY.jsonl.

"""Baumgart's winged-edge structure for a closed polyhedral surface.

Each edge e runs from v_start[e] to v_end[e]. Seen from outside the solid and
walking from v_start to v_end, the face f_left[e] is on the left and f_right[e]
on the right. The faces run counterclockwise seen from outside (the right-hand
rule), so f_left[e] traverses e from start to end and f_right[e] from end to
start. The four wings are the edges before and after e in the counterclockwise
loop of each face: left_prev, left_next, right_prev and right_next.

Each vertex and each face stores one edge. The faces are disks without rings,
and the two faces of an edge are different.
"""

from __future__ import annotations

from typing import Optional, Sequence

FIELDS = ("v_start", "v_end", "f_left", "f_right", "left_prev", "left_next", "right_prev", "right_next")


class WingedEdgeError(ValueError):
    """The input or the arguments do not fit the structure."""


class WingedEdge:
    def __init__(self, n_vertices: int, faces: Sequence[Sequence[int]]) -> None:
        """Build from faces given as counterclockwise lists of vertex ids 0..n-1.

        Time O(n) expected for n = the sum of the face sizes, with one hash map.
        """
        self.v_start: list[int] = []
        self.v_end: list[int] = []
        self.f_left: list[int] = []
        self.f_right: list[int] = []
        self.left_prev: list[int] = []
        self.left_next: list[int] = []
        self.right_prev: list[int] = []
        self.right_next: list[int] = []
        self.vertex_edge: list[int] = [-1] * n_vertices
        self.face_edge: list[int] = []
        self.alive_e: list[bool] = []
        self.alive_f: list[bool] = []
        key: dict[tuple[int, int], int] = {}  # (u, v) with u < v -> edge
        for f, cyc in enumerate(faces):
            k = len(cyc)
            if k < 3 or len(set(cyc)) != k:
                raise WingedEdgeError("a face needs at least 3 distinct vertices")
            self.face_edge.append(-1)
            self.alive_f.append(True)
            for i in range(k):
                u, v = cyc[i], cyc[(i + 1) % k]
                e = key.get((min(u, v), max(u, v)))
                if e is None:
                    e = self._new_edge(u, v, f, -1)
                    key[(min(u, v), max(u, v))] = e
                elif self.v_start[e] == v and self.f_right[e] == -1:
                    self.f_right[e] = f
                else:
                    raise WingedEdgeError("an edge is used twice in one direction or by more than two faces")
            self.face_edge[f] = key[(min(cyc[0], cyc[1]), max(cyc[0], cyc[1]))]
        for e in range(len(self.v_start)):
            if self.f_right[e] == -1:
                raise WingedEdgeError("an edge has only one face")
            if self.f_left[e] == self.f_right[e]:
                raise WingedEdgeError("an edge has the same face on both sides")
        for f, cyc in enumerate(faces):
            k = len(cyc)
            es = [key[(min(cyc[i], cyc[(i + 1) % k]), max(cyc[i], cyc[(i + 1) % k]))] for i in range(k)]
            for i, e in enumerate(es):
                self._set_prev(e, f, es[i - 1])
                self._set_next(e, f, es[(i + 1) % k])
        for e in range(len(self.v_start)):
            for v in (self.v_start[e], self.v_end[e]):
                if self.vertex_edge[v] == -1:
                    self.vertex_edge[v] = e
        if -1 in self.vertex_edge:
            raise WingedEdgeError("a vertex is on no face")
        self._check_fans()

    def _check_fans(self) -> None:
        """Each vertex walk must meet every edge at the vertex: one fan of faces."""
        degree = [0] * len(self.vertex_edge)
        for e in self.edges():
            degree[self.v_start[e]] += 1
            degree[self.v_end[e]] += 1
        for v in range(len(self.vertex_edge)):
            if len(self.vertex_edges(v)) != degree[v]:
                raise WingedEdgeError(f"vertex {v} has more than one fan of faces")

    # ----- O(1) helpers: the wing of e on the side of face f -----

    def _new_edge(self, u: int, v: int, fl: int, fr: int) -> int:
        for name, val in zip(FIELDS, (u, v, fl, fr, -1, -1, -1, -1)):
            getattr(self, name).append(val)
        self.alive_e.append(True)
        return len(self.v_start) - 1

    def _side(self, e: int, f: int) -> bool:
        """True if f is the left face of e, False if it is the right face."""
        if self.f_left[e] == f:
            return True
        if self.f_right[e] == f:
            return False
        raise WingedEdgeError(f"face {f} is not on edge {e}")

    def _next(self, e: int, f: int) -> int:
        return self.left_next[e] if self._side(e, f) else self.right_next[e]

    def _prev(self, e: int, f: int) -> int:
        return self.left_prev[e] if self._side(e, f) else self.right_prev[e]

    def _set_next(self, e: int, f: int, x: int) -> None:
        if self._side(e, f):
            self.left_next[e] = x
        else:
            self.right_next[e] = x

    def _set_prev(self, e: int, f: int, x: int) -> None:
        if self._side(e, f):
            self.left_prev[e] = x
        else:
            self.right_prev[e] = x

    def _set_face(self, e: int, old: int, new: int) -> None:
        if self._side(e, old):
            self.f_left[e] = new
        else:
            self.f_right[e] = new

    def _tail(self, e: int, f: int) -> int:
        """The vertex where the loop of f enters e."""
        return self.v_start[e] if self._side(e, f) else self.v_end[e]

    # ----- queries -----

    def edge_vertices(self, e: int) -> tuple[int, int]:
        return self.v_start[e], self.v_end[e]

    def edge_faces(self, e: int) -> tuple[int, int]:
        """(left face, right face), O(1)."""
        return self.f_left[e], self.f_right[e]

    def face_edges(self, f: int) -> list[int]:
        """The edges of f in counterclockwise order seen from outside."""
        out = []
        e0 = self.face_edge[f]  # @line L1
        e = e0
        while True:
            out.append(e)  # @line L2
            e = self.left_next[e] if self.f_left[e] == f else self.right_next[e]  # @line L3
            if e == e0:  # @line L4
                break
        return out

    def face_vertices(self, f: int) -> list[int]:
        return [self._tail(e, f) for e in self.face_edges(f)]

    def vertex_edges(self, v: int) -> list[int]:
        """The edges at v in counterclockwise order seen from outside."""
        out = []
        e0 = self.vertex_edge[v]  # @line L5
        e = e0
        while True:
            out.append(e)  # @line L6
            e = self.left_prev[e] if self.v_start[e] == v else self.right_prev[e]  # @line L7
            if e == e0:  # @line L8
                break
        return out

    def neighbors(self, v: int) -> list[int]:
        return [self.v_end[e] if self.v_start[e] == v else self.v_start[e] for e in self.vertex_edges(v)]

    def vertex_faces(self, v: int) -> list[int]:
        """The faces at v, counterclockwise: the face on the left of each edge out of v."""
        return [self.f_left[e] if self.v_start[e] == v else self.f_right[e] for e in self.vertex_edges(v)]

    def edges(self) -> list[int]:
        return [e for e in range(len(self.v_start)) if self.alive_e[e]]

    def faces(self) -> list[int]:
        return [f for f in range(len(self.face_edge)) if self.alive_f[f]]

    # ----- updates -----

    def split_edge(self, e: int) -> int:
        """Put a new vertex m inside e. Afterwards e runs from v_start to m and a
        new edge runs from m to the old v_end. Returns m. O(1)."""
        a, b = self.v_start[e], self.v_end[e]
        fl, fr = self.f_left[e], self.f_right[e]
        x = self.left_next[e]  # after e in fl
        y = self.right_prev[e]  # before e in fr
        m = len(self.vertex_edge)
        self.vertex_edge.append(e)
        e2 = self._new_edge(m, b, fl, fr)
        self.v_end[e] = m
        self.left_next[e2], self.left_prev[e2] = x, e
        self.left_next[e] = e2
        self.right_next[e2], self.right_prev[e2] = e, y
        self.right_prev[e] = e2
        self._set_prev(x, fl, e2)
        self._set_next(y, fr, e2)
        if self.vertex_edge[b] == e:
            self.vertex_edge[b] = e2
        return m

    def split_face(self, f: int, u: int, w: int) -> tuple[int, int]:
        """Add an edge n from u to w across f, two vertices of f that are not
        joined by an edge. The part of f from w around to u stays f; the part
        from u to w becomes a new face g. Returns (n, g). O(size of f + degree of u)."""
        es = self.face_edges(f)  # @line L9
        tails = [self._tail(e, f) for e in es]
        if u not in tails or w not in tails:
            raise WingedEdgeError("u and w must be vertices of f")
        iu, iw = tails.index(u), tails.index(w)
        k = len(es)
        if u == w or (iu + 1) % k == iw or (iw + 1) % k == iu:
            raise WingedEdgeError("u and w must be different and not next to each other")
        if w in self.neighbors(u):
            raise WingedEdgeError("u and w are already joined by an edge")
        a_out, a_in = es[iu], es[iu - 1]
        b_out, b_in = es[iw], es[iw - 1]
        g = len(self.face_edge)
        self.face_edge.append(-1)
        self.alive_f.append(True)
        n = self._new_edge(u, w, f, g)  # @line L10
        self.left_prev[n], self.left_next[n] = a_in, b_out  # @line L11
        self.right_prev[n], self.right_next[n] = b_in, a_out
        i = iu
        while i != iw:  # @line L12
            self._set_face(es[i], f, g)
            i = (i + 1) % k
        self._set_next(a_in, f, n)  # @line L13
        self._set_prev(b_out, f, n)
        self._set_next(b_in, g, n)
        self._set_prev(a_out, g, n)
        self.face_edge[f] = n  # @line L14
        self.face_edge[g] = n
        return n, g

    def join_faces(self, n: int) -> int:
        """Remove the edge n and join its right face into its left face. The two
        faces must have only the two ends of n in common, and each end of n must
        have at least 3 edges. Returns the deleted face. O(size of the faces)."""
        f, g = self.f_left[n], self.f_right[n]
        u, w = self.v_start[n], self.v_end[n]
        vf, vg = set(self.face_vertices(f)), set(self.face_vertices(g))
        if vf & vg != {u, w}:
            raise WingedEdgeError("the two faces must meet only along the edge")
        if len(self.vertex_edges(u)) < 3 or len(self.vertex_edges(w)) < 3:
            raise WingedEdgeError("each end must keep at least 2 edges")
        a_in, b_out = self.left_prev[n], self.left_next[n]
        b_in, a_out = self.right_prev[n], self.right_next[n]
        for e in self.face_edges(g):
            if e != n:
                self._set_face(e, g, f)
        self._set_next(a_in, f, a_out)
        self._set_prev(a_out, f, a_in)
        self._set_next(b_in, f, b_out)
        self._set_prev(b_out, f, b_in)
        if self.vertex_edge[u] == n:
            self.vertex_edge[u] = a_out
        if self.vertex_edge[w] == n:
            self.vertex_edge[w] = b_out
        self.face_edge[f] = a_out
        self.alive_e[n] = False
        self.alive_f[g] = False
        self.face_edge[g] = -1
        return g

    def check(self) -> None:
        """Check that the wings agree with the faces and the vertices."""
        for e in self.edges():
            for f, nxt, prv in ((self.f_left[e], self.left_next[e], self.left_prev[e]), (self.f_right[e], self.right_next[e], self.right_prev[e])):
                if not self.alive_e[nxt] or not self.alive_e[prv]:
                    raise WingedEdgeError("a wing points to a deleted edge")
                if self._prev(nxt, f) != e or self._next(prv, f) != e:
                    raise WingedEdgeError("the wings of two edges do not agree")
                head = self.v_end[e] if f == self.f_left[e] else self.v_start[e]
                if self._tail(nxt, f) != head:
                    raise WingedEdgeError("the next edge does not start where e ends")
            if self.f_left[e] == self.f_right[e]:
                raise WingedEdgeError("an edge has the same face on both sides")
        for v, e in enumerate(self.vertex_edge):
            if v not in (self.v_start[e], self.v_end[e]):
                raise WingedEdgeError("a vertex edge does not touch the vertex")
        for f in self.faces():
            if f not in self.edge_faces(self.face_edge[f]):
                raise WingedEdgeError("a face edge does not touch the face")
        self._check_fans()
