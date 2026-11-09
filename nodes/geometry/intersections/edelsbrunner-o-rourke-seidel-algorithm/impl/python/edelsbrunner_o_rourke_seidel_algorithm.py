# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/edelsbrunner-o-rourke-seidel-algorithm/. The authors are listed in prov/SQSS70.jsonl.
"""Incremental construction of a line arrangement by zone walks, in O(n^2) time.

A line is a triple (a, b, c) of integers with (a, b) != (0, 0); it is the set of
points (x, y) with a*x + b*y = c, directed by d = (b, -a). The arrangement is a
doubly connected edge list clipped to a box [-M, M]^2 that holds every crossing
strictly inside. Faces lie on the left of their half-edges; face 0 is the
outside of the box. All points are pairs of Fractions.
"""

from fractions import Fraction
from typing import Optional

Line = tuple[int, int, int]
Point = tuple[Fraction, Fraction]


def cross(u: tuple, v: tuple) -> Fraction:
    return u[0] * v[1] - u[1] * v[0]


def meet(l1: Line, l2: Line) -> Optional[Point]:
    a1, b1, c1 = l1
    a2, b2, c2 = l2
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None
    return (Fraction(c1 * b2 - c2 * b1, det), Fraction(a1 * c2 - a2 * c1, det))


def same_line(l1: Line, l2: Line) -> bool:
    a1, b1, c1 = l1
    a2, b2, c2 = l2
    return a1 * b2 == a2 * b1 and a1 * c2 == a2 * c1 and b1 * c2 == b2 * c1


def side(line: Line, p: Point) -> int:
    """+1 left of the directed line, 0 on it, -1 right of it."""
    a, b, c = line
    s = a * p[0] + b * p[1] - c
    return (s > 0) - (s < 0)


def _half(v: tuple) -> int:
    return 0 if v[1] > 0 or (v[1] == 0 and v[0] > 0) else 1


def _relative(h: tuple, v: tuple) -> tuple:
    """v in a frame where h points along the positive x-axis (scaled by |h|)."""
    return (h[0] * v[0] + h[1] * v[1], cross(h, v))


def _angle_less(u: tuple, v: tuple) -> bool:
    hu, hv = _half(u), _half(v)
    if hu != hv:
        return hu < hv
    return cross(u, v) > 0


def box_hits(line: Line, m: int) -> list[Point]:
    a, b, c = line
    pts = set()
    if b != 0:
        for x in (-m, m):
            y = Fraction(c - a * x, b)
            if -m <= y <= m:
                pts.add((Fraction(x), y))
    if a != 0:
        for y in (-m, m):
            x = Fraction(c - b * y, a)
            if -m <= x <= m:
                pts.add((x, Fraction(y)))
    return list(pts)


def box_size(lines: list[Line]) -> int:
    big = Fraction(0)
    for i, l in enumerate(lines):
        big = max(big, abs(l[2]))
        for k in lines[:i]:
            p = meet(l, k)
            if p is not None:
                big = max(big, abs(p[0]), abs(p[1]))
    return int(big) + 1


class Arrangement:
    """A doubly connected edge list that starts as the box and grows by INSERT."""

    def __init__(self, m: int) -> None:
        self.m = m
        self.lines: list[Line] = []
        self.points: list[Point] = []
        self.on_box: list[bool] = []
        self.out: list[int] = []  # one outgoing half-edge per vertex
        self.origin: list[int] = []
        self.twin: list[int] = []
        self.next: list[int] = []
        self.prev: list[int] = []
        self.face: list[int] = []
        self.line_of: list[int] = []
        self.face_edge: list[int] = [1, 0]  # face 0 is outside, face 1 inside
        self.steps = 0
        corners = [(-m, -m), (m, -m), (m, m), (-m, m)]
        for x, y in corners:
            self._new_vertex((Fraction(x), Fraction(y)), True)
        for k in range(4):  # half-edge 2k runs counterclockwise, 2k + 1 back
            self._new_pair(k, (k + 1) % 4, -1)
        for k in range(4):
            e, t = 2 * k, 2 * k + 1
            self.next[e], self.prev[e], self.face[e] = 2 * ((k + 1) % 4), 2 * ((k - 1) % 4), 1
            self.next[t], self.prev[t], self.face[t] = 2 * ((k - 1) % 4) + 1, 2 * ((k + 1) % 4) + 1, 0
            self.out[k] = e

    def _new_vertex(self, p: Point, on_box: bool) -> int:
        self.points.append(p)
        self.on_box.append(on_box)
        self.out.append(-1)
        return len(self.points) - 1

    def _new_pair(self, u: int, v: int, line: int) -> int:
        e = len(self.origin)
        self.origin += [u, v]
        self.twin += [e + 1, e]
        self.next += [-1, -1]
        self.prev += [-1, -1]
        self.face += [-1, -1]
        self.line_of += [line, line]
        return e

    def head(self, e: int) -> int:
        return self.origin[self.twin[e]]

    def vec(self, e: int) -> tuple:
        p, q = self.points[self.origin[e]], self.points[self.head(e)]
        return (q[0] - p[0], q[1] - p[1])

    def split(self, g: int, q: Point, on_box: bool) -> int:
        """Split the edge of half-edge g = a->b at the point q inside it."""
        t = self.twin[g]
        w = self._new_vertex(q, on_box)
        g2 = self._new_pair(w, self.origin[t], self.line_of[g])  # g2: w->b, t2 = g2 + 1: b->w
        t2 = g2 + 1
        # Keep g as a->w and t as b->a's first part; rewire t to be w->a.
        gn = self.next[g]
        self.origin[t] = w
        self.twin[g], self.twin[t] = t, g
        # g (a->w) pairs with t (w->a); g2 (w->b) pairs with t2 (b->w).
        self.next[g], self.prev[g2] = g2, g
        self.next[g2], self.prev[gn] = gn, g2
        tp = self.prev[t]
        self.next[tp], self.prev[t2] = t2, tp
        self.next[t2], self.prev[t] = t, t2
        self.face[g2], self.face[t2] = self.face[g], self.face[t]
        self.out[w] = g2
        b = self.origin[t2]
        if self.out[b] == t:
            self.out[b] = t2
        return w

    def _leaving_toward(self, u: int, d: tuple) -> int:
        """The half-edge h out of u with d strictly between h and the next one counterclockwise."""
        h = self.out[u]
        while True:
            self.steps += 1
            h2 = self.twin[self.prev[h]]  # the next half-edge counterclockwise around u
            kd, k2 = _relative(self.vec(h), d), _relative(self.vec(h), self.vec(h2))
            if not (kd[1] == 0 and kd[0] > 0) and _angle_less(kd, k2):
                return h
            h = h2

    def insert(self, line: Line) -> None:
        idx = len(self.lines)
        self.lines.append(line)
        a, b, _ = line
        d = (b, -a)
        hits = sorted(box_hits(line, self.m), key=lambda p: d[0] * p[0] + d[1] * p[1])
        p = hits[0]  # @line L4
        e = 1  # the outer face cycle runs clockwise along the box
        while True:
            self.steps += 1
            if self.points[self.origin[e]] == p:
                u = self.origin[e]
                break
            q0, q1 = self.points[self.origin[e]], self.points[self.head(e)]
            if cross((q1[0] - q0[0], q1[1] - q0[1]), (p[0] - q0[0], p[1] - q0[1])) == 0 and \
                    min(q0[0], q1[0]) <= p[0] <= max(q0[0], q1[0]) and \
                    min(q0[1], q1[1]) <= p[1] <= max(q0[1], q1[1]) and p != q1:
                u = self.split(e, p, True)  # @line L5
                break
            e = self.next[e]
        while True:  # @line L6
            h = self._leaving_toward(u, d)  # @line L7
            g = h
            while side(line, self.points[self.head(g)]) < 0:  # @line L8
                self.steps += 1
                g = self.next[g]
            if side(line, self.points[self.head(g)]) == 0:  # @line L9
                w = self.head(g)
            else:
                w = self.split(g, meet(line, self._line_through(g)), self.line_of[g] < 0)
            f, hp, gn = self.face[h], self.prev[h], self.next[g]  # @line L10
            x = self._new_pair(u, w, idx)
            y = x + 1
            self.next[g], self.prev[y] = y, g
            self.next[y], self.prev[h] = h, y
            self.next[hp], self.prev[x] = x, hp
            self.next[x], self.prev[gn] = gn, x
            self.face[y] = f
            self.face_edge[f] = y
            nf = len(self.face_edge)
            self.face_edge.append(x)
            k = x
            while True:
                self.steps += 1
                self.face[k] = nf
                k = self.next[k]
                if k == x:
                    break
            u = w  # @line L11
            if self.on_box[u]:  # @line L12
                return

    def _line_through(self, g: int) -> Line:
        if self.line_of[g] >= 0:
            return self.lines[self.line_of[g]]
        p, q = self.points[self.origin[g]], self.points[self.head(g)]
        if p[0] == q[0]:
            return (1, 0, int(p[0]))
        return (0, 1, int(p[1]))

    def cycle(self, f: int) -> list[int]:
        out, e = [], self.face_edge[f]
        while True:
            out.append(e)
            e = self.next[e]
            if e == self.face_edge[f]:
                return out

    def face_boundary(self, f: int) -> list[Point]:
        return [self.points[self.origin[e]] for e in self.cycle(f)]

    def counts(self) -> tuple[int, int, int]:
        """Vertices, edges and faces of the arrangement itself, without the box."""
        v = sum(1 for k in range(len(self.points)) if not self.on_box[k])
        e = sum(1 for k in range(0, len(self.origin), 2) if self.line_of[k] >= 0)
        return v, e, len(self.face_edge) - 1

    def check_invariant(self) -> None:
        h = len(self.origin)
        for e in range(h):
            t = self.twin[e]
            assert t != e and self.twin[t] == e
            assert self.origin[self.next[e]] == self.origin[t]
            assert self.prev[self.next[e]] == e and self.next[self.prev[e]] == e
            assert self.face[self.next[e]] == self.face[e]
        seen = set()
        for f in range(len(self.face_edge)):
            cyc = self.cycle(f)
            assert all(self.face[e] == f for e in cyc)
            seen.update(cyc)
            area = sum(cross(self.points[self.origin[e]], self.points[self.head(e)]) for e in cyc)
            if f == 0:
                assert area < 0
            else:
                assert area > 0
                for e in cyc:
                    assert cross(self.vec(e), self.vec(self.next[e])) > 0
        assert len(seen) == h
        for v in range(len(self.points)):
            assert self.origin[self.out[v]] == v
        assert len(self.points) - h // 2 + len(self.face_edge) == 2


def eos_arrangement(lines: list[Line]) -> Arrangement:
    for i, l in enumerate(lines):
        if l[0] == 0 and l[1] == 0:
            raise ValueError("a line needs (a, b) != (0, 0)")
        if any(same_line(k, l) for k in lines[:i]):
            raise ValueError("the lines must be distinct")
    arr = Arrangement(box_size(lines))  # @line L1
    for l in lines:  # @line L2
        arr.insert(l)
    return arr  # @line L3
