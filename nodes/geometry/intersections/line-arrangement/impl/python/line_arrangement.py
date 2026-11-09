# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/line-arrangement/. The authors are listed in prov/FB22MJ.jsonl.
"""The arrangement of n lines as a doubly connected edge list, with exact arithmetic.

A line is a triple (a, b, c) of integers with (a, b) != (0, 0); it is the set of
points (x, y) with a*x + b*y = c. The structure clips the arrangement to a box
[-M, M]^2 that holds every vertex strictly inside, so each unbounded edge ends on
the box. Points are pairs of Fractions. Faces are on the left of their
half-edges; the outer face, outside the box, has id 0.
"""

from fractions import Fraction
from functools import cmp_to_key
from typing import Optional

Line = tuple[int, int, int]
Point = tuple[Fraction, Fraction]


def cross(u: tuple, v: tuple) -> Fraction:
    return u[0] * v[1] - u[1] * v[0]


def meet(l1: Line, l2: Line) -> Optional[Point]:
    """The common point of two lines, or None if they are parallel."""
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
    """+1, 0 or -1 as a*x + b*y - c is positive, zero or negative."""
    a, b, c = line
    s = a * p[0] + b * p[1] - c
    return (s > 0) - (s < 0)


def _half(v: tuple) -> int:
    return 0 if v[1] > 0 or (v[1] == 0 and v[0] > 0) else 1


def _angle_cmp(u: tuple, v: tuple) -> int:
    """Compare the polar angles of u and v in [0, 2*pi), exactly."""
    hu, hv = _half(u), _half(v)
    if hu != hv:
        return -1 if hu < hv else 1
    c = cross(u, v)
    return -1 if c > 0 else (1 if c < 0 else 0)


def box_hits(line: Line, m: int) -> list[Point]:
    """The two points where the line meets the boundary of [-m, m]^2."""
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
    return sorted(pts)


def _perimeter(p: Point, m: int) -> Fraction:
    x, y = p
    if y == -m:
        return x + m
    if x == m:
        return 2 * m + (y + m)
    if y == m:
        return 4 * m + (m - x)
    return 6 * m + (m - y)


class LineArrangement:
    """A static arrangement of distinct lines, built in O(n^2 log n) time."""

    def __init__(self, lines: list[Line]) -> None:
        for i, l in enumerate(lines):  # @line L1
            if l[0] == 0 and l[1] == 0:
                raise ValueError("a line needs (a, b) != (0, 0)")
            for j in range(i):
                if same_line(lines[j], l):
                    raise ValueError("the lines must be distinct")
        self.lines = list(lines)
        n = len(lines)
        crossings = [[meet(lines[i], lines[j]) for j in range(n)] for i in range(n)]
        big = 0  # @line L2
        for i in range(n):
            big = max(big, abs(lines[i][2]))
            for j in range(n):
                p = crossings[i][j]
                if p is not None:
                    big = max(big, abs(p[0]), abs(p[1]))
        self.m = m = int(big) + 1
        segments: list[tuple[Point, Point, int]] = []
        boundary: set[Point] = {(Fraction(-m), Fraction(-m)), (Fraction(m), Fraction(-m)),
                                (Fraction(m), Fraction(m)), (Fraction(-m), Fraction(m))}
        for i, (a, b, _) in enumerate(lines):  # @line L3
            hits = box_hits(lines[i], m)
            boundary.update(hits)
            pts = set(hits) | {p for p in crossings[i] if p is not None}
            order = sorted(pts, key=lambda p: -b * p[0] + a * p[1])
            for p, q in zip(order, order[1:]):
                segments.append((p, q, i))
        ring = sorted(boundary, key=lambda p: _perimeter(p, m))  # @line L4
        for p, q in zip(ring, ring[1:] + ring[:1]):
            segments.append((p, q, -1))
        self.points: list[Point] = []  # @line L5
        index: dict[Point, int] = {}
        self.origin: list[int] = []
        self.twin: list[int] = []
        self.line_of: list[int] = []
        for p, q, i in segments:
            for r in (p, q):
                if r not in index:
                    index[r] = len(self.points)
                    self.points.append(r)
            e = len(self.origin)
            self.origin += [index[p], index[q]]
            self.twin += [e + 1, e]
            self.line_of += [i, i]
        h = len(self.origin)
        around: list[list[int]] = [[] for _ in self.points]  # @line L6
        for e in range(h):
            around[self.origin[e]].append(e)
        self.rotation: list[list[int]] = []
        for v, out in enumerate(around):
            out.sort(key=cmp_to_key(lambda e, f: _angle_cmp(self._vec(e), self._vec(f))))
            self.rotation.append(out)
        self.next = [0] * h  # @line L7
        self.prev = [0] * h
        place = {}
        for v, out in enumerate(self.rotation):
            for k, e in enumerate(out):
                place[e] = k
        for e in range(h):
            t = self.twin[e]
            out = self.rotation[self.origin[t]]
            f = out[(place[t] - 1) % len(out)]
            self.next[e] = f
            self.prev[f] = e
        self.face = [-1] * h  # @line L8
        cycles: list[list[int]] = []
        for e in range(h):
            if self.face[e] == -1:
                cyc, g = [], e
                while self.face[g] == -1:
                    self.face[g] = len(cycles)
                    cyc.append(g)
                    g = self.next[g]
                cycles.append(cyc)
        outer = next(k for k, cyc in enumerate(cycles) if self._area2(cyc) < 0)
        order = [outer] + [k for k in range(len(cycles)) if k != outer]
        rename = {old: new for new, old in enumerate(order)}
        self.cycles = [cycles[k] for k in order]
        self.face = [rename[f] for f in self.face]

    def _vec(self, e: int) -> Point:
        p, q = self.points[self.origin[e]], self.points[self.origin[self.twin[e]]]
        return (q[0] - p[0], q[1] - p[1])

    def _area2(self, cyc: list[int]) -> Fraction:
        s = Fraction(0)
        for e in cyc:
            p, q = self.points[self.origin[e]], self.points[self.origin[self.twin[e]]]
            s += cross(p, q)
        return s

    def _inside_box(self, p: Point) -> bool:
        return -self.m < p[0] < self.m and -self.m < p[1] < self.m

    def counts(self) -> tuple[int, int, int]:
        """The numbers of vertices, edges and faces of the arrangement itself."""
        v = sum(1 for p in self.points if self._inside_box(p))
        e = sum(1 for k in range(0, len(self.origin), 2) if self.line_of[k] >= 0)
        return v, e, len(self.cycles) - 1

    def face_boundary(self, f: int) -> list[Point]:
        """The vertices of face f (1 <= f) clipped to the box, counterclockwise."""
        return [self.points[self.origin[e]] for e in self.cycles[f]]  # @line L9

    def locate(self, p: Point) -> Optional[int]:
        """The face that holds p strictly inside, or None if p is on a line.

        p must lie strictly inside the box [-m, m]^2. This is the simple
        O(n^2) scan over all face boundaries."""
        if not self._inside_box(p):
            raise ValueError("the point must lie strictly inside the box")
        if any(side(l, p) == 0 for l in self.lines):  # @line L10
            return None
        for f in range(1, len(self.cycles)):  # @line L11
            if all(cross(self._vec(e), (p[0] - self.points[self.origin[e]][0],
                                        p[1] - self.points[self.origin[e]][1])) > 0
                   for e in self.cycles[f]):
                return f
        raise AssertionError("no face holds the point")

    def check_invariant(self) -> None:
        h = len(self.origin)
        for e in range(h):
            t = self.twin[e]
            assert t != e and self.twin[t] == e
            assert self.origin[self.next[e]] == self.origin[t]
            assert self.prev[self.next[e]] == e and self.next[self.prev[e]] == e
            assert self.face[self.next[e]] == self.face[e]
            assert self.line_of[e] == self.line_of[t]
        for v, out in enumerate(self.rotation):
            assert len(out) >= 2
            for e in out:
                assert self.origin[e] == v
            for k in range(len(out)):
                assert _angle_cmp(self._vec(out[k - 1]), self._vec(out[k])) < 0 or k == 0
            p = self.points[v]
            if self._inside_box(p):
                assert all(self.line_of[e] >= 0 for e in out)
                lines_here = [l for l in self.lines if side(l, p) == 0]
                assert len(lines_here) >= 2 and len(out) == 2 * len(lines_here)
        nv, ne, nf = len(self.points), h // 2, len(self.cycles)
        assert nv - ne + nf == 2  # Euler's formula, outer face included
        assert self._area2(self.cycles[0]) < 0
        for cyc in self.cycles[1:]:
            assert self._area2(cyc) > 0
            for e in cyc:
                assert cross(self._vec(e), self._vec(self.next[e])) > 0  # strictly convex
