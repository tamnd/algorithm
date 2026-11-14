# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selective-geometric-complex/. The authors are listed in prov/TH7Q2X.jsonl.

"""A planar selective geometric complex (SGC) with exact Boolean operations.

The plane is cut by a set of segments and points into cells: vertices, open
edges and faces, where a face is a connected component of the plane minus
all segments and points. Every cell has a mark, in or out, and the object
is the union of the marked cells. So an object may have any mix of
dimensions: areas with or without their boundary, cracks, dangling edges and
isolated points.

Booleans follow the three steps of Rossignac and O'Connor:
  subdivide  overlay the two complexes, so every new cell lies in one cell
             of each input;
  select     mark each new cell by the Boolean rule on its two parents,
             found from a point inside the new cell;
  simplify   remove the edges and vertices that separate cells with the
             same mark, and merge what they separated.
Interior, closure and boundary read the star of each cell: the cells whose
closure contains it.

All coordinates are Fractions, so every test is exact.

Precondition: segments have distinct endpoints.
Cost: for n segments and points with k crossings the complex has O(n + k)
cells. Building it takes O(n^2) for the crossings, O((n + k) log(n + k))
for the angular sorts, and O((n + k)^2) to place holes in faces and to find
a point inside each face. A Boolean or a simplification classifies one point
per cell in O(n + k) time each, so it takes O((n + k)^2) time.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Callable, Iterable, Sequence

Point = tuple[Fraction, Fraction]
Seg = tuple[Point, Point]


def P(x, y) -> Point:
    return (Fraction(x), Fraction(y))


def cross(o: Point, a: Point, b: Point) -> Fraction:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def on_segment(p: Point, a: Point, b: Point) -> bool:
    return (cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def seg_meet(a: Point, b: Point, c: Point, d: Point) -> Point | None:
    """The crossing point of two segments that are not parallel, if any."""
    den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
    if den == 0:
        return None
    t = ((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0])) / den
    u = ((c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0])) / den
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
    return None


def half_plane_of(d: Point) -> int:
    """0 for directions with angle in [0, pi), 1 for [pi, 2 pi)."""
    return 0 if d[1] > 0 or (d[1] == 0 and d[0] > 0) else 1


def angle_key(o: Point, p: Point):
    """A key that sorts the directions p - o counterclockwise from angle 0."""
    d = (p[0] - o[0], p[1] - o[1])
    h = half_plane_of(d)
    # within a half-plane, compare by the cotangent, which falls as the angle grows
    if d[1] == 0:
        return (h, -float("inf"), Fraction(0))
    return (h, Fraction(0), -d[0] / d[1])


def winding(p: Point, cyc: Sequence[Point]) -> int:
    """The winding number of a closed polygonal chain around p (p not on it)."""
    w = 0
    for i in range(len(cyc)):
        a, b = cyc[i], cyc[(i + 1) % len(cyc)]
        if a[1] <= p[1] < b[1] and cross(a, b, p) > 0:
            w += 1
        elif b[1] <= p[1] < a[1] and cross(a, b, p) < 0:
            w -= 1
    return w


def area2(cyc: Sequence[Point]) -> Fraction:
    return sum(cyc[i][0] * cyc[(i + 1) % len(cyc)][1] - cyc[(i + 1) % len(cyc)][0] * cyc[i][1]
               for i in range(len(cyc)))


Cell = tuple


def merge_collinear(edges: Iterable[tuple[Point, Point]]) -> list[Seg]:
    """Join edges that lie on one line and share an endpoint. The edges are
    given with their endpoints in sorted order and do not overlap."""
    groups: dict[tuple, list[tuple[Point, Point]]] = {}
    for u, v in edges:
        a, b = v[1] - u[1], u[0] - v[0]          # the line a x + b y = c
        k = a if a != 0 else b
        a, b = a / k, b / k
        groups.setdefault((a, b, a * u[0] + b * u[1]), []).append((u, v))
    out: list[Seg] = []
    for es in groups.values():
        es.sort()
        cur = list(es[0])
        for u, v in es[1:]:
            if u == cur[1]:
                cur[1] = v
            else:
                out.append((cur[0], cur[1]))
                cur = [u, v]
        out.append((cur[0], cur[1]))
    return out


class Complex:
    """The cells cut out by segments and points, with their stars."""

    def __init__(self, segments: Iterable[Seg], points: Iterable[Point] = ()):
        segs = [(P(*a), P(*b)) for a, b in segments]
        pts = {P(*p) for p in points}
        # 1. split every segment at endpoints, crossings and points on it
        edges: set[tuple[Point, Point]] = set()
        for i, (a, b) in enumerate(segs):
            cuts = {a, b}
            for j, (c, d) in enumerate(segs):
                if i == j:
                    continue
                m = seg_meet(a, b, c, d)
                if m is not None:
                    cuts.add(m)
                for e in (c, d):
                    if on_segment(e, a, b):
                        cuts.add(e)
            cuts |= {p for p in pts if on_segment(p, a, b)}
            cs = sorted(cuts)
            for u, v in zip(cs, cs[1:]):
                edges.add((u, v))
        self.edges = sorted(edges)
        verts = {v for e in self.edges for v in e} | pts
        self.vertices = sorted(verts)
        # 2. half-edges and the next pointer: face on the left
        out: dict[Point, list[Point]] = {v: [] for v in self.vertices}
        for u, v in self.edges:
            out[u].append(v)
            out[v].append(u)
        for v in out:
            out[v].sort(key=lambda w, v=v: angle_key(v, w))
        pos = {(v, w): i for v in out for i, w in enumerate(out[v])}

        def nxt(h):
            a, b = h
            i = pos[(b, a)]
            return (b, out[b][i - 1])

        # 3. trace the boundary cycles
        cyc_of: dict[tuple[Point, Point], int] = {}
        cycles: list[list[Point]] = []
        for u, v in self.edges:
            for h in ((u, v), (v, u)):
                if h in cyc_of:
                    continue
                k = len(cycles)
                cyc = []
                while h not in cyc_of:
                    cyc_of[h] = k
                    cyc.append(h[0])
                    h = nxt(h)
                cycles.append(cyc)
        # 4. faces: face 0 is unbounded; each counterclockwise cycle bounds one more
        outer = [k for k, c in enumerate(cycles) if area2(c) > 0]
        self.outer_cycles = {k + 1: cycles[c] for k, c in enumerate(outer)}
        face_of_cycle = {c: k + 1 for k, c in enumerate(outer)}
        for k, c in enumerate(cycles):
            if k not in face_of_cycle:
                face_of_cycle[k] = self._face_strictly_around(c[0], set(c))
        self.faces = [0] + sorted(self.outer_cycles)
        # 5. stars
        self.star: dict[Cell, set[Cell]] = {}
        self.side: dict[tuple[Point, Point], tuple[int, int]] = {}
        for u, v in self.edges:
            fl, fr = face_of_cycle[cyc_of[(u, v)]], face_of_cycle[cyc_of[(v, u)]]
            self.side[(u, v)] = (fl, fr)
            self.star[("e", (u, v))] = {("f", fl), ("f", fr)}
        for v in self.vertices:
            s: set[Cell] = set()
            if not out[v]:
                s.add(("f", self._face_strictly_around(v, {v})))
            for w in out[v]:
                e = (min(v, w), max(v, w))
                s.add(("e", e))
                s |= self.star[("e", e)]
            self.star[("v", v)] = s
        for f in self.faces:
            self.star[("f", f)] = set()

    def _face_strictly_around(self, p: Point, on: set[Point]) -> int:
        """The face whose outer cycle is the innermost one around p, among the
        cycles that do not pass through the points of `on`."""
        best, best_area = 0, None
        for f, cyc in self.outer_cycles.items():
            if on & set(cyc):
                continue
            if winding(p, cyc) != 0:
                a = area2(cyc)
                if best_area is None or a < best_area:
                    best, best_area = f, a
        return best

    def cells(self) -> list[Cell]:
        return ([("v", v) for v in self.vertices] + [("e", e) for e in self.edges]
                + [("f", f) for f in self.faces])

    def locate(self, p: Point) -> Cell:
        """The cell that contains p."""
        p = P(*p)
        if ("v", p) in self.star:
            return ("v", p)
        for u, v in self.edges:
            if on_segment(p, u, v):
                return ("e", (u, v))
        best, best_area = 0, None
        for f, cyc in self.outer_cycles.items():
            if winding(p, cyc) != 0:
                a = area2(cyc)
                if best_area is None or a < best_area:
                    best, best_area = f, a
        return ("f", best)

    def sample(self, c: Cell) -> Point:
        """A point inside the cell c."""
        kind, x = c
        if kind == "v":
            return x
        if kind == "e":
            return ((x[0][0] + x[1][0]) / 2, (x[0][1] + x[1][1]) / 2)
        if x == 0:
            if not self.vertices:
                return P(0, 0)
            return (max(v[0] for v in self.vertices) + 1, Fraction(0))
        cyc = self.outer_cycles[x]
        a, b = cyc[0], cyc[1]
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        n = (a[1] - b[1], b[0] - a[0])            # left normal of a -> b
        far = (m[0] + n[0], m[1] + n[1])
        hits = []
        for u, v in self.edges:
            if (u, v) in ((a, b), (b, a)):
                continue
            if cross(m, far, u) == 0 and cross(m, far, v) == 0:
                cand = [u, v]
            else:
                q = seg_meet(m, (m[0] + 4 * n[0] * 10**6, m[1] + 4 * n[1] * 10**6), u, v)
                cand = [q] if q is not None else []
            for q in cand:
                t = ((q[0] - m[0]) * n[0] + (q[1] - m[1]) * n[1]) / (n[0] ** 2 + n[1] ** 2)
                if t > 0:
                    hits.append(t)
        for v in self.vertices:
            if cross(m, far, v) == 0:
                t = ((v[0] - m[0]) * n[0] + (v[1] - m[1]) * n[1]) / (n[0] ** 2 + n[1] ** 2)
                if t > 0:
                    hits.append(t)
        t = min(hits) / 2 if hits else Fraction(1)
        return (m[0] + t * n[0], m[1] + t * n[1])


class SGC:
    """A selective geometric complex: a complex and its marked cells."""

    def __init__(self, cx: Complex, marks: Iterable[Cell]):
        self.cx = cx
        self.marks = frozenset(marks)

    # primitives
    @staticmethod
    def from_predicate(segments, points, pred: Callable[[Point], bool]) -> "SGC":
        cx = Complex(segments, points)
        return SGC(cx, [c for c in cx.cells() if pred(cx.sample(c))])

    @staticmethod
    def polygon(pts: Sequence, closed: bool) -> "SGC":
        """A simple polygon, with its boundary when closed."""
        q = [P(*p) for p in pts]
        segs = [(q[i], q[(i + 1) % len(q)]) for i in range(len(q))]

        def pred(p):
            if any(on_segment(p, a, b) for a, b in segs):
                return closed
            return winding(p, q) != 0
        return SGC.from_predicate(segs, [], pred)

    @staticmethod
    def segment(a, b, closed: bool) -> "SGC":
        a, b = P(*a), P(*b)
        return SGC.from_predicate([(a, b)], [], lambda p: on_segment(p, a, b) and (closed or p not in (a, b)))

    @staticmethod
    def point(p) -> "SGC":
        p = P(*p)
        return SGC.from_predicate([], [p], lambda q: q == p)

    # queries
    def contains(self, p) -> bool:
        return self.cx.locate(p) in self.marks

    def is_empty(self) -> bool:
        return not self.marks

    def count_by_dimension(self) -> tuple[int, int, int]:
        return tuple(sum(1 for c in self.marks if c[0] == k) for k in "vef")

    def size(self) -> tuple[int, int, int]:
        return (len(self.cx.vertices), len(self.cx.edges), len(self.cx.faces))

    # subdivide, select, simplify
    def combine(self, other: "SGC", op: Callable[[bool, bool], bool]) -> "SGC":
        segs = self.cx.edges + other.cx.edges  # @line L1
        pts = self.cx.vertices + other.cx.vertices
        cx = Complex(segs, pts)  # @line L2
        marks = []
        for c in cx.cells():  # @line L3
            p = cx.sample(c)  # @line L4
            if op(self.contains(p), other.contains(p)):  # @line L5
                marks.append(c)
        return SGC(cx, marks).simplify()  # @line L6

    def __or__(self, o):
        return self.combine(o, lambda x, y: x or y)

    def __and__(self, o):
        return self.combine(o, lambda x, y: x and y)

    def __sub__(self, o):
        return self.combine(o, lambda x, y: x and not y)

    def __xor__(self, o):
        return self.combine(o, lambda x, y: x != y)

    def complement(self) -> "SGC":
        return SGC(self.cx, [c for c in self.cx.cells() if c not in self.marks])

    def simplify(self) -> "SGC":
        """Drop every edge whose mark equals the marks of its two faces, and
        every vertex whose mark equals the marks of its whole star; rebuild
        the complex from what is left and copy the marks back."""
        m, cx = self.marks, self.cx
        keep_edges = []
        for e in cx.edges:  # @line L7
            mark = ("e", e) in m
            if any((("f", f) in m) != mark for f in cx.side[e]):
                keep_edges.append(e)
        kept = set(keep_edges)
        keep_points = []
        for v in cx.vertices:  # @line L8
            mark = ("v", v) in m
            es = [c[1] for c in cx.star[("v", v)] if c[0] == "e" and c[1] in kept]
            if not es:                           # alone in a face: needed if marked otherwise
                needed = any((c in m) != mark for c in cx.star[("v", v)])
            elif len(es) == 2:                   # inside a straight edge: needed if marked otherwise
                (a,), (b,) = [[x for x in e if x != v] for e in es]
                needed = cross(a, v, b) != 0 or any((("e", e) in m) != mark for e in es)
            else:
                needed = True
            if needed:
                keep_points.append(v)
        new = Complex(merge_collinear(keep_edges), keep_points)  # @line L9
        return SGC(new, [c for c in new.cells() if self.contains(new.sample(c))])  # @line L10

    def interior(self) -> "SGC":
        return SGC(self.cx, [c for c in self.marks if self.cx.star[c] <= self.marks]).simplify()

    def closure(self) -> "SGC":
        return SGC(self.cx, [c for c in self.cx.cells()
                             if c in self.marks or self.cx.star[c] & self.marks]).simplify()

    def boundary(self) -> "SGC":
        return self.closure() - self.interior()

    def regularization(self) -> "SGC":
        return self.interior().closure()
