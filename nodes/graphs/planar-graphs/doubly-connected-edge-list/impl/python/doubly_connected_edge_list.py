# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/doubly-connected-edge-list/. The authors are listed in prov/69ZYTE.jsonl.

"""A doubly connected edge list (half-edge structure) for a connected plane graph.

The embedding is given combinatorially, as a rotation system: for each vertex
the list of its neighbours in counterclockwise order. No coordinates are used.
Half-edges are numbered so that the twin of half-edge h is h ^ 1.
"""


class DCEL:
    """Half-edge structure of a connected plane graph (no loops, no parallel edges)."""

    def __init__(self) -> None:
        """Make the plane graph with one vertex, no edges and one face."""
        self.origin: list[int] = []  # origin[h]: the vertex where h starts
        self.next: list[int] = []  # next[h]: the half-edge after h on its face
        self.prev: list[int] = []  # prev[h]: the half-edge before h on its face
        self.face: list[int] = []  # face[h]: the face to the left of h
        self.vertex_edge: list[int] = [-1]  # one half-edge out of each vertex, or -1
        self.face_edge: list[int] = [-1]  # one half-edge of each face, -1 for no edge, -2 for deleted

    # ------------------------------------------------------------------ build

    @classmethod
    def from_rotation(cls, rot: list[list[int]]) -> "DCEL":
        """Build the structure from a rotation system of a connected graph.

        rot[u] lists the neighbours of u in counterclockwise order. Time and
        space O(n + m).
        """
        d = cls()
        n = len(rot)
        d.vertex_edge = [-1] * n
        d.face_edge = []
        half = {}  # (u, v) -> half-edge id
        for u in range(n):  # @line L1
            for v in rot[u]:
                if (u, v) in half:
                    continue
                h = len(d.origin)
                half[(u, v)], half[(v, u)] = h, h ^ 1  # @line L2
                d.origin += [u, v]
                d.vertex_edge[u] = h
                d.vertex_edge[v] = h ^ 1
        m2 = len(d.origin)
        d.next, d.prev, d.face = [-1] * m2, [-1] * m2, [-1] * m2
        pos = [{v: i for i, v in enumerate(rot[u])} for u in range(n)]
        for (u, v), h in half.items():  # @line L3
            r = rot[v]
            w = r[(pos[v][u] - 1) % len(r)]  # the neighbour before u around v
            nh = half[(v, w)]
            d.next[h] = nh  # @line L4
            d.prev[nh] = h
        for h in range(m2):  # @line L5
            if d.face[h] != -1:
                continue
            f = len(d.face_edge)
            d.face_edge.append(h)
            g = h
            while d.face[g] == -1:  # @line L6
                d.face[g] = f
                g = d.next[g]
        if n == 1 and m2 == 0:
            d.face_edge = [-1]
        return d

    # ------------------------------------------------------------- queries

    def twin(self, h: int) -> int:
        """The opposite half-edge of h."""
        return h ^ 1

    def num_vertices(self) -> int:
        return len(self.vertex_edge)

    def num_edges(self) -> int:
        return len(self.origin) // 2

    def faces(self) -> list[int]:
        """The ids of the faces that exist."""
        return [f for f, e in enumerate(self.face_edge) if e != -2]

    def face_boundary(self, f: int) -> list[int]:
        """The half-edges of face f in order. Time O(length of the boundary)."""
        h0 = self.face_edge[f]  # @line L9
        if h0 < 0:
            return []
        out, h = [], h0
        while True:
            out.append(h)
            h = self.next[h]
            if h == h0:
                return out

    def neighbors(self, v: int) -> list[int]:
        """The neighbours of v in counterclockwise order. Time O(degree)."""
        h0 = self.vertex_edge[v]  # @line L7
        if h0 < 0:
            return []
        out, h = [], h0
        while True:
            out.append(self.origin[h ^ 1])
            # the next half-edge out of v, counterclockwise
            h = self.prev[h] ^ 1  # @line L8
            if h == h0:
                return out

    # ----------------------------------------------------------- updates

    def _new_pair(self, u: int, v: int) -> int:
        h = len(self.origin)
        self.origin += [u, v]
        self.next += [-1, -1]
        self.prev += [-1, -1]
        self.face += [-1, -1]
        return h

    def _link(self, a: int, b: int) -> None:
        self.next[a] = b
        self.prev[b] = a

    def add_leaf(self, a: int) -> int:
        """Add a new vertex w and the edge from u = origin[a] to w, in the face of a.

        If the graph has no edge, a must be -1 and u is vertex 0. The new edge
        comes just before a around the face. Returns the half-edge u -> w. O(1).
        """
        w = len(self.vertex_edge)
        self.vertex_edge.append(-1)
        if a == -1:
            u, f = 0, 0
            h = self._new_pair(u, w)
            self._link(h, h ^ 1)
            self._link(h ^ 1, h)
        else:
            u, f = self.origin[a], self.face[a]
            h = self._new_pair(u, w)
            p = self.prev[a]  # @line L13
            self._link(p, h)
            self._link(h, h ^ 1)
            self._link(h ^ 1, a)
        self.face[h] = self.face[h ^ 1] = f
        self.face_edge[f] = h
        self.vertex_edge[u] = h
        self.vertex_edge[w] = h ^ 1
        return h

    def split_face(self, a: int, b: int) -> int:
        """Add the edge from origin[a] to origin[b] through the common face of a and b.

        Precondition: a != b, face[a] == face[b], origin[a] != origin[b], and the
        two vertices are not yet adjacent. The face is split in two. Returns the
        new half-edge h from origin[a] to origin[b]; its face is the new face.
        Time O(length of the new face).
        """
        f = self.face[a]
        u, v = self.origin[a], self.origin[b]
        h = self._new_pair(u, v)  # @line L10
        t = h ^ 1
        pa, pb = self.prev[a], self.prev[b]
        self._link(pa, h)  # @line L11
        self._link(h, b)
        self._link(pb, t)
        self._link(t, a)
        g = len(self.face_edge)  # @line L12
        self.face_edge.append(h)
        self.face_edge[f] = t
        x = h
        while True:
            self.face[x] = g
            x = self.next[x]
            if x == h:
                break
        self.face[t] = f
        return h

    def join_faces(self, h: int) -> None:
        """Delete the edge of h when its two sides are different faces; merge the faces.

        The face of h ^ 1 survives. Time O(length of the face of h).
        """
        t = h ^ 1
        f, g = self.face[t], self.face[h]
        if f == g:
            raise ValueError("the two sides of the edge are the same face")
        x = self.next[h]  # @line L14
        while x != h:
            self.face[x] = f
            x = self.next[x]
        self._link(self.prev[h], self.next[t])  # @line L15
        self._link(self.prev[t], self.next[h])
        u, v = self.origin[h], self.origin[t]
        if self.vertex_edge[u] == h:
            self.vertex_edge[u] = self.prev[h] ^ 1
        if self.vertex_edge[v] == t:
            self.vertex_edge[v] = self.prev[t] ^ 1
        self.face_edge[f] = self.next[t]
        self.face_edge[g] = -2
        # the two half-edges stay in the arrays but are unlinked
        for y in (h, t):
            self.next[y] = self.prev[y] = self.face[y] = -1
            self.origin[y] = -1

    # -------------------------------------------------------------- check

    def check_invariant(self) -> None:
        """Raise AssertionError if a pointer invariant or Euler's formula fails."""
        live = [h for h in range(len(self.origin)) if self.origin[h] != -1]
        for h in live:
            assert self.origin[h ^ 1] != -1
            assert self.prev[self.next[h]] == h and self.next[self.prev[h]] == h
            assert self.origin[self.next[h]] == self.origin[h ^ 1]
            assert self.face[self.next[h]] == self.face[h]
            assert self.face_edge[self.face[h]] >= 0
        for v, h in enumerate(self.vertex_edge):
            assert h == -1 or self.origin[h] == v
        fs = self.faces()
        seen = 0
        for f in fs:
            b = self.face_boundary(f)
            assert all(self.face[x] == f for x in b)
            seen += len(b)
        assert seen == len(live)
        n, m = self.num_vertices(), len(live) // 2
        assert n - m + len(fs) == 2
