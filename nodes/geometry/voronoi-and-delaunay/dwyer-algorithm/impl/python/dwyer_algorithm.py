# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dwyer-algorithm/. The authors are listed in prov/FFZ2TD.jsonl.

import math

Point = tuple[int, int]


def orient(a: Point, b: Point, c: Point) -> int:
    """Sign of (b - a) x (c - a): 1 for a left turn, -1 for a right turn, 0 when collinear."""
    d = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (d > 0) - (d < 0)


def incircle(a: Point, b: Point, c: Point, d: Point) -> int:
    """For a, b, c counterclockwise: 1 if d is strictly inside their circumcircle, 0 on it, -1 outside."""
    adx, ady = a[0] - d[0], a[1] - d[1]
    bdx, bdy = b[0] - d[0], b[1] - d[1]
    cdx, cdy = c[0] - d[0], c[1] - d[1]
    det = ((adx * adx + ady * ady) * (bdx * cdy - cdx * bdy)
           + (bdx * bdx + bdy * bdy) * (cdx * ady - adx * cdy)
           + (cdx * cdx + cdy * cdy) * (adx * bdy - bdx * ady))
    return (det > 0) - (det < 0)


class QuadEdge:
    """The quad-edge structure of Guibas and Stolfi, stored in flat lists.

    Edge e = 4 q + r is the r-th rotation of quad q: r = 0 and r = 2 are the two directions of a primal edge,
    r = 1 and r = 3 those of its dual. nxt[e] is Onext(e); org[e] is the origin of a primal edge.
    """

    def __init__(self, pts: list[Point]) -> None:
        self.pts = pts
        self.nxt: list[int] = []
        self.org: list[int] = []
        self.alive: list[bool] = []
        self.free: list[int] = []  # quads of deleted edges, reused so that the space stays O(n)

    @staticmethod
    def rot(e: int) -> int:
        return (e & ~3) | ((e + 1) & 3)

    @staticmethod
    def sym(e: int) -> int:
        return e ^ 2

    @staticmethod
    def rot_inv(e: int) -> int:
        return (e & ~3) | ((e + 3) & 3)

    def onext(self, e: int) -> int:
        return self.nxt[e]

    def oprev(self, e: int) -> int:
        return self.rot(self.nxt[self.rot(e)])

    def lnext(self, e: int) -> int:
        return self.rot(self.nxt[self.rot_inv(e)])

    def rprev(self, e: int) -> int:
        return self.nxt[self.sym(e)]

    def dest(self, e: int) -> int:
        return self.org[e ^ 2]

    def make_edge(self, a: int, b: int) -> int:
        if self.free:
            q = self.free.pop()
            self.nxt[q:q + 4] = [q, q + 3, q + 2, q + 1]
            self.org[q:q + 4] = [a, -1, b, -1]
            self.alive[q:q + 4] = [True] * 4
            return q
        q = len(self.nxt)
        self.nxt += [q, q + 3, q + 2, q + 1]
        self.org += [a, -1, b, -1]
        self.alive += [True] * 4
        return q

    def splice(self, a: int, b: int) -> None:
        alpha, beta = self.rot(self.nxt[a]), self.rot(self.nxt[b])
        self.nxt[a], self.nxt[b] = self.nxt[b], self.nxt[a]
        self.nxt[alpha], self.nxt[beta] = self.nxt[beta], self.nxt[alpha]

    def connect(self, a: int, b: int) -> int:
        """A new edge from the destination of a to the origin of b, in the face left of both."""
        e = self.make_edge(self.dest(a), self.org[b])
        self.splice(e, self.lnext(a))
        self.splice(self.sym(e), b)
        return e

    def delete(self, e: int) -> None:
        self.splice(e, self.oprev(e))
        self.splice(self.sym(e), self.oprev(self.sym(e)))
        for k in range(4):
            self.alive[(e & ~3) + k] = False
        self.free.append(e & ~3)

    def triangles(self) -> list[tuple[int, int, int]]:
        """The bounded faces with three edges and positive area, as counterclockwise index triples."""
        out = set()
        for e in range(0, len(self.nxt), 2):
            if not self.alive[e]:
                continue
            a, b = self.org[e], self.dest(e)
            f = self.lnext(e)
            c = self.dest(f)
            if self.dest(self.lnext(f)) == a and orient(self.pts[a], self.pts[b], self.pts[c]) > 0:
                k = min(range(3), key=lambda i: (a, b, c)[i])
                t = (a, b, c)
                out.add(t[k:] + t[:k])
        return sorted(out)


def _right_of(qe: QuadEdge, x: int, e: int) -> bool:
    p = qe.pts
    return orient(p[x], p[qe.dest(e)], p[qe.org[e]]) > 0


def _left_of(qe: QuadEdge, x: int, e: int) -> bool:
    p = qe.pts
    return orient(p[x], p[qe.org[e]], p[qe.dest(e)]) > 0


def _base(qe: QuadEdge, s: list[int]) -> tuple[int, int]:
    """Two or three points: one edge, a path or a triangle. Returns (le, re)."""
    p = qe.pts
    a = qe.make_edge(s[0], s[1])
    if len(s) == 2:
        return a, qe.sym(a)
    b = qe.make_edge(s[1], s[2])
    qe.splice(qe.sym(a), b)
    o = orient(p[s[0]], p[s[1]], p[s[2]])
    if o > 0:
        qe.connect(b, a)
        return a, qe.sym(b)
    if o < 0:
        c = qe.connect(b, a)
        return qe.sym(c), c
    return a, qe.sym(b)


def merge(qe: QuadEdge, ldo: int, ldi: int, rdi: int, rdo: int) -> tuple[int, int]:
    """Merge the Delaunay triangulations of a left set and a right set (every left point lexicographically
    smaller than every right point). ldo, ldi and rdi, rdo are the (le, re) handles of the halves."""
    p = qe.pts
    while True:  # lower common tangent
        if _left_of(qe, qe.org[rdi], ldi):
            ldi = qe.lnext(ldi)
        elif _right_of(qe, qe.org[ldi], rdi):
            rdi = qe.rprev(rdi)
        else:
            break
    basel = qe.connect(qe.sym(rdi), ldi)
    if qe.org[ldi] == qe.org[ldo]:
        ldo = qe.sym(basel)
    if qe.org[rdi] == qe.org[rdo]:
        rdo = basel
    while True:
        lcand = qe.onext(qe.sym(basel))
        if _right_of(qe, qe.dest(lcand), basel):
            while incircle(p[qe.dest(basel)], p[qe.org[basel]], p[qe.dest(lcand)],
                           p[qe.dest(qe.onext(lcand))]) > 0:
                t = qe.onext(lcand)
                qe.delete(lcand)
                lcand = t
        rcand = qe.oprev(basel)
        if _right_of(qe, qe.dest(rcand), basel):
            while incircle(p[qe.dest(basel)], p[qe.org[basel]], p[qe.dest(rcand)],
                           p[qe.dest(qe.oprev(rcand))]) > 0:
                t = qe.oprev(rcand)
                qe.delete(rcand)
                rcand = t
        lvalid = _right_of(qe, qe.dest(lcand), basel)
        rvalid = _right_of(qe, qe.dest(rcand), basel)
        if not lvalid and not rvalid:
            break
        if not lvalid or (rvalid and incircle(p[qe.dest(lcand)], p[qe.org[lcand]], p[qe.org[rcand]],
                                              p[qe.dest(rcand)]) > 0):
            basel = qe.connect(rcand, qe.sym(basel))
        else:
            basel = qe.connect(qe.sym(basel), qe.sym(lcand))
    return ldo, rdo


def _build(qe: QuadEdge, s: list[int]) -> tuple[int, int]:
    if len(s) <= 3:
        return _base(qe, s)
    mid = len(s) // 2
    ldo, ldi = _build(qe, s[:mid])
    rdi, rdo = _build(qe, s[mid:])
    return merge(qe, ldo, ldi, rdi, rdo)


def x_handles(qe: QuadEdge, e: int) -> tuple[int, int]:
    """Given the le handle of a triangulation (a hull edge with the outer face on its right), return the
    handles (le, re) for the (x, y) order: the counterclockwise hull edge out of the lexicographically
    smallest vertex and the clockwise hull edge out of the largest one. Walks the hull once."""
    p = qe.pts
    walk = []
    x = qe.sym(e)
    while True:
        walk.append(x)
        x = qe.lnext(x)
        if x == qe.sym(e):
            break
    le = qe.sym(min(walk, key=lambda f: p[qe.dest(f)]))
    re = max(walk, key=lambda f: p[qe.org[f]])
    return le, re


def strip_count(n: int) -> int:
    """About (n / log n)^(1/2) strips, each with at least two points."""
    if n < 4:
        return 1
    return max(1, min(n // 2, math.isqrt(int(n / math.log2(n)))))


def dwyer(points: list[Point], strips: int | None = None) -> list[tuple[Point, Point, Point]]:
    """Return a Delaunay triangulation of the points by Dwyer's strip method, as counterclockwise triples.

    The points sorted by (x, y) are cut into k vertical strips (k = strip_count(n) unless strips
    is given) of consecutive points. Each strip is
    triangulated by the Guibas-Stolfi recursion with cuts across the strip (points sorted by (-y, x), a
    rotation by 90 degrees, which changes no predicate). Then the strips are merged left to right in a
    balanced way. Duplicates are removed; collinear input gives []; coordinates must be int or Fraction.
    Cost: O(n log n) time in the worst case. Dwyer's analysis gives O(n log log n) average time for points
    uniform in a square when the sorts are bucket sorts; this code uses sorted(), which costs O(n log n).
    """
    pts = sorted(set(points))  # @line L1
    n = len(pts)
    if n < 2:
        return []
    qe = QuadEdge(pts)
    k = strip_count(n) if strips is None else max(1, min(strips, n // 2))  # @line L2
    bounds = [n * j // k for j in range(k + 1)]
    handles = []
    for j in range(k):  # @line L3
        strip = sorted(range(bounds[j], bounds[j + 1]), key=lambda i: (-pts[i][1], pts[i][0]))  # @line L4
        le, _ = _build(qe, strip)  # @line L5
        handles.append(x_handles(qe, le))  # @line L6
    while len(handles) > 1:  # @line L7
        nxt = []
        for j in range(0, len(handles) - 1, 2):
            (ldo, ldi), (rdi, rdo) = handles[j], handles[j + 1]
            nxt.append(merge(qe, ldo, ldi, rdi, rdo))  # @line L8
        if len(handles) % 2:
            nxt.append(handles[-1])
        handles = nxt
    return sorted((pts[a], pts[b], pts[c]) for a, b, c in qe.triangles())  # @line L9
