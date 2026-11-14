# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nef-polyhedron/. The authors are listed in prov/Q616YB.jsonl.

"""Nef polygons: plane sets built from half-planes by Boolean operations.

A Nef polygon over a finite set of lines is a union of faces of the line
arrangement: vertices, open edges and open cells. A face is named by its
sign vector, the signs of a x + b y + c at its points for every line, and
the set is stored as the set of marked sign vectors. This is the selective
idea behind the plane maps of Seel and the selective Nef complexes of
Hachenberger and Kettner, without their geometric maps: the faces here are
found from the lines, and the incidences come with them.

Booleans overlay the two arrangements and combine the marks. Interior,
closure and boundary look at the star of each face: the faces whose closure
contains it. All arithmetic is exact with Fraction.

Precondition: lines have rational coefficients and (a, b) != (0, 0).
Cost: an arrangement of n lines has O(n^2) faces and is built in O(n^3)
time, since each sign vector has n entries. A Boolean operation builds the
arrangement of the union of the two line sets, so it takes O((n1 + n2)^3).
Interior, closure and boundary take time linear in the total size of the
stars, O(n^3) in all. Point membership takes O(n).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Callable, Iterable, Sequence

Line = tuple[Fraction, Fraction, Fraction]
Point = tuple[Fraction, Fraction]
SV = tuple[int, ...]


def sign(v: Fraction) -> int:
    return (v > 0) - (v < 0)


def canonical(a, b, c) -> tuple[Line, int]:
    """Scale a x + b y + c so that its first nonzero coefficient of (a, b)
    is 1. Returns the line and the sign of the factor removed."""
    a, b, c = Fraction(a), Fraction(b), Fraction(c)
    k = a if a != 0 else b
    if k == 0:
        raise ValueError("not a line")
    return (a / k, b / k, c / k), sign(k)


def side(line: Line, p: Point) -> int:
    return sign(line[0] * p[0] + line[1] * p[1] + line[2])


class Arrangement:
    """The faces of the arrangement of distinct lines, by sign vector, with
    their dimension and the set of faces above each one (its star)."""

    def __init__(self, lines: Sequence[Line]):
        self.lines: list[Line] = list(lines)
        self.index = {l: i for i, l in enumerate(self.lines)}
        self.dim: dict[SV, int] = {}
        self.up: dict[SV, set[SV]] = {}
        n = len(self.lines)
        if n == 0:
            self.dim[()] = 2
            self.up[()] = set()
            return
        on_line: list[list[Point]] = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                p = self._meet(self.lines[i], self.lines[j])
                if p is not None:
                    on_line[i].append(p)
                    on_line[j].append(p)
        for i, (a, b, c) in enumerate(self.lines):
            d = (-b, a)
            vs = sorted(set(on_line[i]), key=lambda p: p[0] * d[0] + p[1] * d[1])
            if vs:
                reps = [(vs[0][0] - d[0], vs[0][1] - d[1], None, vs[0])]
                reps += [((u[0] + w[0]) / 2, (u[1] + w[1]) / 2, u, w) for u, w in zip(vs, vs[1:])]
                reps.append((vs[-1][0] + d[0], vs[-1][1] + d[1], vs[-1], None))
            else:
                p0 = (Fraction(0), -c / b) if b != 0 else (-c / a, Fraction(0))
                reps = [(p0[0], p0[1], None, None)]
            for x, y, u, w in reps:
                e = self.sv((x, y))
                cells = [e[:i] + (s,) + e[i + 1:] for s in (1, -1)]
                self.dim[e] = 1
                self.up.setdefault(e, set()).update(cells)
                for f in cells:
                    self.dim[f] = 2
                    self.up.setdefault(f, set())
                for v in (u, w):
                    if v is not None:
                        vv = self.sv(v)
                        self.dim[vv] = 0
                        self.up.setdefault(vv, set()).update([e] + cells)

    @staticmethod
    def _meet(l1: Line, l2: Line) -> Point | None:
        det = l1[0] * l2[1] - l1[1] * l2[0]
        if det == 0:
            return None
        return ((l1[1] * l2[2] - l1[2] * l2[1]) / det, (l1[2] * l2[0] - l1[0] * l2[2]) / det)

    def sv(self, p: Point) -> SV:
        return tuple(side(l, p) for l in self.lines)

    def faces(self) -> list[SV]:
        return sorted(self.dim)


class NefPolygon:
    """A Nef polygon: an arrangement and the set of its marked faces."""

    def __init__(self, arr: Arrangement, marks: Iterable[SV]):
        self.arr = arr
        self.marks = frozenset(marks)

    # construction
    @staticmethod
    def halfplane(a, b, c, closed: bool) -> "NefPolygon":
        """{(x, y) : a x + b y + c > 0}, or >= 0 when closed."""
        line, s = canonical(a, b, c)
        arr = Arrangement([line])
        return NefPolygon(arr, [f for f in arr.faces() if s * f[0] > 0 or (closed and f[0] == 0)])

    @staticmethod
    def empty() -> "NefPolygon":
        return NefPolygon(Arrangement([]), [])

    @staticmethod
    def plane() -> "NefPolygon":
        return NefPolygon(Arrangement([]), [()])

    # queries
    def contains(self, p: Sequence) -> bool:
        return self.arr.sv((Fraction(p[0]), Fraction(p[1]))) in self.marks  # @line L1

    def is_empty(self) -> bool:
        return not self.marks

    # Boolean operations
    def _combine(self, other: "NefPolygon", op: Callable[[bool, bool], bool]) -> "NefPolygon":
        lines = list(dict.fromkeys(self.arr.lines + other.arr.lines))  # @line L2
        arr = Arrangement(lines)  # @line L3
        ia = [arr.index[l] for l in self.arr.lines]
        ib = [arr.index[l] for l in other.arr.lines]
        marks = []
        for f in arr.faces():  # @line L4
            fa = tuple(f[k] for k in ia)  # @line L5
            fb = tuple(f[k] for k in ib)
            if op(fa in self.marks, fb in other.marks):  # @line L6
                marks.append(f)
        return NefPolygon(arr, marks)  # @line L7

    def __or__(self, other):
        return self._combine(other, lambda x, y: x or y)

    def __and__(self, other):
        return self._combine(other, lambda x, y: x and y)

    def __sub__(self, other):
        return self._combine(other, lambda x, y: x and not y)

    def __xor__(self, other):
        return self._combine(other, lambda x, y: x != y)

    def complement(self) -> "NefPolygon":
        return NefPolygon(self.arr, [f for f in self.arr.faces() if f not in self.marks])

    # topological operations
    def interior(self) -> "NefPolygon":
        m = self.marks
        return NefPolygon(self.arr, [f for f in m if self.arr.up[f] <= m])  # @line L8

    def closure(self) -> "NefPolygon":
        m = self.marks
        return NefPolygon(self.arr, [f for f in self.arr.faces()
                                     if f in m or any(g in m for g in self.arr.up[f])])  # @line L9

    def boundary(self) -> "NefPolygon":
        return self.closure() - self.interior()  # @line L10

    def regularization(self) -> "NefPolygon":
        return self.interior().closure()

    def simplify(self) -> "NefPolygon":
        """Drop lines on which the set does not depend: line i goes when the
        mark of every face is a function of its signs on the other lines."""
        cur = self
        changed = True
        while changed:
            changed = False
            for i in range(len(cur.arr.lines)):
                seen: dict[SV, bool] = {}
                ok = True
                for f in cur.arr.faces():
                    g = f[:i] + f[i + 1:]
                    if seen.setdefault(g, f in cur.marks) != (f in cur.marks):
                        ok = False
                        break
                if ok:
                    arr = Arrangement(cur.arr.lines[:i] + cur.arr.lines[i + 1:])
                    cur = NefPolygon(arr, [g for g, mk in seen.items() if mk])
                    changed = True
                    break
        return cur

    def count_by_dimension(self) -> tuple[int, int, int]:
        c = [0, 0, 0]
        for f in self.marks:
            c[self.arr.dim[f]] += 1
        return (c[0], c[1], c[2])
