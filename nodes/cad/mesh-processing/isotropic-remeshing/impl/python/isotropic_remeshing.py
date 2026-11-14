# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isotropic-remeshing/. The authors are listed in prov/0E9HMJ.jsonl.

"""Isotropic remeshing in the style of Botsch and Kobbelt (SGP 2004).

Each round, for a target edge length L:
1. split the longest edge while it is longer than 4/3 L,
2. collapse edges shorter than 4/5 L into their midpoint, when the collapse is
   safe (link condition, no border vertex, no new edge longer than 4/3 L, no
   flipped face),
3. flip edges while a flip lowers the valence excess (target 6 inside,
   4 on the border),
4. move each inner vertex toward the centroid of its neighbours, inside its
   tangent plane, and
5. optionally project the vertices onto a reference surface.

Border vertices never move and border edges are never collapsed or flipped, so
the border keeps its shape (border edges may still be split at their midpoints).
The mesh is a small half-edge-like structure: directed edge -> face, and
vertex -> faces.
"""

import heapq
from math import sqrt
from typing import Callable, Optional, Sequence

Vec = tuple


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def length(a):
    return sqrt(dot(a, a))


def mid(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2)


class Mesh:
    def __init__(self, points: Sequence[Sequence[float]], faces: Sequence[Sequence[int]]):
        self.P: list[Vec] = [tuple(p) for p in points]
        self.F: dict[int, tuple[int, int, int]] = {}
        self.he: dict[tuple[int, int], int] = {}
        self.vf: list[set[int]] = [set() for _ in self.P]
        self.next_id = 0
        for f in faces:
            self.add_face(*f)

    # ---- basic operations ----

    def add_face(self, a, b, c) -> int:
        fid = self.next_id
        self.next_id += 1
        self.F[fid] = (a, b, c)
        for u, v in ((a, b), (b, c), (c, a)):
            if (u, v) in self.he:
                raise ValueError("non-manifold or badly oriented: directed edge used twice")
            self.he[(u, v)] = fid
        for v in (a, b, c):
            self.vf[v].add(fid)
        return fid

    def remove_face(self, fid):
        a, b, c = self.F.pop(fid)
        for u, v in ((a, b), (b, c), (c, a)):
            del self.he[(u, v)]
        for v in (a, b, c):
            self.vf[v].discard(fid)

    def opposite(self, u, v):
        """The third vertex of the face with the directed edge u -> v, or None."""
        fid = self.he.get((u, v))
        if fid is None:
            return None
        f = self.F[fid]
        return next(w for w in f if w != u and w != v)

    def neighbours(self, v) -> set[int]:
        return {w for fid in self.vf[v] for w in self.F[fid] if w != v}

    def is_border_edge(self, u, v) -> bool:
        return ((u, v) in self.he) != ((v, u) in self.he)

    def is_border_vertex(self, v) -> bool:
        return any(self.is_border_edge(v, w) for w in self.neighbours(v))

    def edges(self) -> list[tuple[int, int]]:
        return sorted({(min(u, v), max(u, v)) for u, v in self.he})

    def elen(self, u, v) -> float:
        return length(sub(self.P[u], self.P[v]))

    def face_normal(self, f, P=None):
        P = P or self.P
        a, b, c = f
        return cross(sub(P[b], P[a]), sub(P[c], P[a]))

    def valence_target(self, v) -> int:
        return 4 if self.is_border_vertex(v) else 6

    # ---- the three local operators ----

    def split(self, u, v) -> int:
        """Split the edge u-v at its midpoint m; each face (u, v, w) becomes (u, m, w) and (m, v, w)."""
        m = len(self.P)
        self.P.append(mid(self.P[u], self.P[v]))
        self.vf.append(set())
        for a, b in ((u, v), (v, u)):
            fid = self.he.get((a, b))
            if fid is not None:
                w = self.opposite(a, b)
                self.remove_face(fid)
                self.add_face(a, m, w)
                self.add_face(m, b, w)
        return m

    def can_collapse(self, u, v, high) -> bool:
        if self.is_border_edge(u, v) or self.is_border_vertex(u) or self.is_border_vertex(v):
            return False
        c, d = self.opposite(u, v), self.opposite(v, u)
        if self.neighbours(u) & self.neighbours(v) != {c, d}:             # the link condition
            return False
        if len(self.neighbours(c)) <= 3 or len(self.neighbours(d)) <= 3:
            return False
        p = mid(self.P[u], self.P[v])
        if any(length(sub(p, self.P[w])) > high for w in (self.neighbours(u) | self.neighbours(v)) - {u, v}):
            return False
        P = list(self.P)
        P[u] = P[v] = p
        for fid in self.vf[u] | self.vf[v]:
            f = self.F[fid]
            if u in f and v in f:
                continue
            if dot(self.face_normal(f), self.face_normal(f, P)) <= 0:      # the face would flip or degenerate
                return False
        return True

    def collapse(self, u, v):
        """Merge v into u at the midpoint. The two faces of the edge disappear."""
        p = mid(self.P[u], self.P[v])
        old = [self.F[fid] for fid in self.vf[v]]
        for fid in list(self.vf[v]):
            self.remove_face(fid)
        for f in old:
            if u not in f:
                self.add_face(*(u if w == v else w for w in f))
        self.P[u] = p

    def flip_gain(self, u, v) -> int:
        """How much a flip of u-v lowers the valence excess at its four vertices (0 if not allowed)."""
        if self.is_border_edge(u, v):
            return 0
        c, d = self.opposite(u, v), self.opposite(v, u)
        if c == d or d in self.neighbours(c):
            return 0
        val = {w: len(self.neighbours(w)) for w in (u, v, c, d)}
        if val[u] <= 3 or val[v] <= 3:
            return 0
        tgt = {w: self.valence_target(w) for w in (u, v, c, d)}
        before = sum(abs(val[w] - tgt[w]) for w in (u, v, c, d))
        after = (abs(val[u] - 1 - tgt[u]) + abs(val[v] - 1 - tgt[v]) +
                 abs(val[c] + 1 - tgt[c]) + abs(val[d] + 1 - tgt[d]))
        if after >= before:
            return 0
        n_old = tuple(x + y for x, y in zip(self.face_normal((u, v, c)), self.face_normal((v, u, d))))
        for f in ((u, d, c), (d, v, c)):
            if dot(self.face_normal(f), n_old) <= 0:                         # the new face would fold over
                return 0
        return before - after

    def flip(self, u, v):
        """Faces (u, v, c) and (v, u, d) become (u, d, c) and (d, v, c)."""
        c, d = self.opposite(u, v), self.opposite(v, u)
        self.remove_face(self.he[(u, v)])
        self.remove_face(self.he[(v, u)])
        self.add_face(u, d, c)
        self.add_face(d, v, c)

    # ---- output ----

    def compact(self) -> tuple[list[Vec], list[tuple[int, int, int]]]:
        used = sorted({w for f in self.F.values() for w in f})
        new = {v: i for i, v in enumerate(used)}
        return [self.P[v] for v in used], [tuple(new[w] for w in self.F[fid]) for fid in sorted(self.F)]


def split_long_edges(mesh: Mesh, high: float) -> int:
    """Split the longest edge while it is longer than high. Returns the number of splits."""
    heap = [(-mesh.elen(u, v), u, v) for u, v in mesh.edges() if mesh.elen(u, v) > high]
    heapq.heapify(heap)
    count = 0
    while heap:
        neg, u, v = heapq.heappop(heap)
        if ((u, v) not in mesh.he and (v, u) not in mesh.he) or mesh.elen(u, v) != -neg:
            continue
        m = mesh.split(u, v)
        count += 1
        for w in mesh.neighbours(m):
            if mesh.elen(m, w) > high:
                heapq.heappush(heap, (-mesh.elen(m, w), min(m, w), max(m, w)))
    return count


def collapse_short_edges(mesh: Mesh, low: float, high: float) -> int:
    count = 0
    changed = True
    while changed:
        changed = False
        for u, v in mesh.edges():
            if (u, v) not in mesh.he and (v, u) not in mesh.he:
                continue
            if mesh.elen(u, v) < low and mesh.can_collapse(u, v, high):
                mesh.collapse(u, v)
                count += 1
                changed = True
    return count


def equalize_valences(mesh: Mesh) -> int:
    count = 0
    changed = True
    while changed:
        changed = False
        for u, v in mesh.edges():
            if (u, v) not in mesh.he:
                u, v = v, u
            if (u, v) in mesh.he and mesh.flip_gain(u, v) > 0:
                mesh.flip(u, v)
                count += 1
                changed = True
    return count


def tangential_relaxation(mesh: Mesh, project: Optional[Callable] = None):
    live = sorted({w for f in mesh.F.values() for w in f})
    new = {}
    for v in live:
        if mesh.is_border_vertex(v):
            continue
        nb = mesh.neighbours(v)
        q = tuple(sum(mesh.P[w][k] for w in nb) / len(nb) for k in range(3))
        n = (0.0, 0.0, 0.0)
        for fid in mesh.vf[v]:
            n = tuple(x + y for x, y in zip(n, mesh.face_normal(mesh.F[fid])))
        ln = length(n)
        d = sub(q, mesh.P[v])
        if ln > 0:
            n = tuple(x / ln for x in n)
            d = tuple(d[k] - dot(d, n) * n[k] for k in range(3))
        p = tuple(mesh.P[v][k] + d[k] for k in range(3))
        new[v] = project(p) if project else p
    for v, p in new.items():
        mesh.P[v] = p


def isotropic_remeshing(points: Sequence[Sequence[float]], faces: Sequence[Sequence[int]], target: float,
                        iterations: int = 5, project: Optional[Callable] = None):
    """Remesh toward edges of length `target`. Returns (points, faces) of the new mesh."""
    mesh = Mesh(points, faces)
    low, high = 4 * target / 5, 4 * target / 3
    for _ in range(iterations):                                     # @line L1
        split_long_edges(mesh, high)                                # @line L2
        collapse_short_edges(mesh, low, high)                       # @line L3
        equalize_valences(mesh)                                     # @line L4
        tangential_relaxation(mesh, project)                        # @line L5
    return mesh.compact()                                           # @line L6
