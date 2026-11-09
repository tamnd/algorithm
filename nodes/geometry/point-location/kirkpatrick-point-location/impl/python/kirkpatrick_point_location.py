# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kirkpatrick-point-location/. The authors are listed in prov/KVYDDR.jsonl.

"""Kirkpatrick's hierarchy of triangulations for planar point location.

Input: the corners A, B, C of the outer triangle in counterclockwise order, and a list of
triangles (each a triple of integer points) that triangulates the closed triangle ABC. Every
other vertex lies strictly inside ABC.

Each round removes an independent set of inner vertices of degree at most 8 and fills each
hole with new triangles by ear clipping. A new triangle points to the triangles of the removed
star whose interiors overlap it; together they cover it. The last level is the single triangle ABC. A query descends from it.

A query returns one of
    ("vertex", p)        q is the vertex p
    ("edge", (a, b))     q is in the relative interior of the edge ab, with a < b in lexicographic order
    ("triangle", i)      q is in the open triangle i of the input
    ("outside",)         q is outside the closed triangle ABC
"""

Point = tuple[int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of p, q, r: positive for a counterclockwise turn."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def ccw(t: tuple[Point, Point, Point]) -> tuple[Point, Point, Point]:
    a, b, c = t
    o = orient(a, b, c)
    if o == 0:
        raise ValueError("degenerate triangle")
    return (a, b, c) if o > 0 else (a, c, b)


def in_closed(t: tuple[Point, Point, Point], q: Point) -> bool:
    a, b, c = t
    return orient(a, b, q) >= 0 and orient(b, c, q) >= 0 and orient(c, a, q) >= 0


def in_closed_tri(a: Point, b: Point, c: Point, q: Point) -> bool:
    return orient(a, b, q) >= 0 and orient(b, c, q) >= 0 and orient(c, a, q) >= 0


class Tri:
    __slots__ = ("pts", "children", "index")

    def __init__(self, pts, children=None, index=-1):
        self.pts = pts  # counterclockwise
        self.children = children or []  # the triangles of the level below that cover it
        self.index = index  # input index for level 0, else -1


def interiors_overlap(s, t) -> bool:
    """True if two counterclockwise triangles share interior points (no edge line separates them)."""
    for u, w in ((s, t), (t, s)):
        for k in range(3):
            a, b = u[k], u[(k + 1) % 3]
            if all(orient(a, b, p) <= 0 for p in w):
                return False
    return True


def ear_clip(poly: list[Point]) -> list[tuple[Point, Point, Point]]:
    """Triangulate a simple counterclockwise polygon (collinear vertices allowed) by ear clipping.

    An ear tip u_i needs orient(u_{i-1}, u_i, u_{i+1}) > 0 and no other vertex in the closed
    triangle. Such an ear exists in every simple polygon (two ears theorem).
    """
    poly = list(poly)
    out = []
    while len(poly) > 3:
        m = len(poly)
        for i in range(m):
            a, b, c = poly[i - 1], poly[i], poly[(i + 1) % m]
            if orient(a, b, c) <= 0:
                continue
            if any(in_closed_tri(a, b, c, w) for w in poly if w not in (a, b, c)):
                continue
            out.append((a, b, c))
            del poly[i]
            break
        else:
            raise RuntimeError("no ear found: the polygon is not simple")
    if orient(*poly) <= 0:
        raise RuntimeError("degenerate last triangle")
    out.append(tuple(poly))
    return out


class KirkpatrickLocator:
    def __init__(self, outer: tuple[Point, Point, Point], triangles: list[tuple[Point, Point, Point]], max_degree: int = 8) -> None:
        self.outer = ccw(outer)
        protected = set(self.outer)
        level = [Tri(ccw(t), index=i) for i, t in enumerate(triangles)]
        self.input_triangles = [lv.pts for lv in level]
        star: dict[Point, set[Tri]] = {}
        for t in level:
            for p in t.pts:
                star.setdefault(p, set()).add(t)
        self.level_sizes = [len(level)]  # number of triangles in each level
        self.removed_per_round: list[int] = []
        current = set(level)
        order = sorted(star)  # sorted once; each round filters it, which keeps the build linear
        while len(current) > 1:  # @line L1
            order = [v for v in order if v in star]
            # degree of an inner vertex = the number of triangles around it
            chosen: list[Point] = []
            blocked: set[Point] = set()
            for v in order:  # @line L2
                if v in protected or v in blocked or len(star[v]) > max_degree:
                    continue
                chosen.append(v)
                blocked.add(v)
                for t in star[v]:
                    blocked.update(t.pts)
            if not chosen:
                raise RuntimeError("no removable vertex: the input is not a triangulation of ABC")
            for v in chosen:  # @line L3
                old = star.pop(v)
                nxt = {}
                for t in old:
                    a, b, c = t.pts
                    i = (a, b, c).index(v)
                    u, w = t.pts[(i + 1) % 3], t.pts[(i + 2) % 3]
                    nxt[u] = w  # the link polygon runs counterclockwise around v
                start = min(nxt)
                poly = [start]
                while nxt[poly[-1]] != start:
                    poly.append(nxt[poly[-1]])
                children = sorted(old, key=lambda t: t.pts)  # a fixed order makes the runs repeatable
                for t in old:
                    current.discard(t)
                    for p in t.pts:
                        if p != v:
                            star[p].discard(t)
                for pts in ear_clip(poly):  # @line L4
                    nt = Tri(pts, [c for c in children if interiors_overlap(c.pts, pts)])  # @line L5
                    current.add(nt)
                    for p in pts:
                        star[p].add(nt)
            self.removed_per_round.append(len(chosen))
            self.level_sizes.append(len(current))
        (self.top,) = current
        self.tests = 0

    def depth(self) -> int:
        return len(self.level_sizes) - 1

    def size(self) -> int:
        """The number of triangle records over all levels (shared ones counted once)."""
        seen = set()
        stack = [self.top]
        while stack:
            t = stack.pop()
            if id(t) in seen:
                continue
            seen.add(id(t))
            stack.extend(t.children)
        return len(seen)

    def find_triangle(self, q: Point) -> "Tri | None":
        t = self.top
        if not in_closed(t.pts, q):  # @line L6
            return None
        while t.children:  # @line L7
            for c in t.children:  # @line L8
                self.tests += 1
                if in_closed(c.pts, q):
                    t = c
                    break
            else:
                raise AssertionError("children do not cover the parent")
        return t  # @line L9

    def locate(self, q: Point):
        t = self.find_triangle(q)
        if t is None:
            return ("outside",)
        return classify(t.pts, t.index, q)


def classify(pts, index, q):
    """The answer for a point q in the closed triangle pts."""
    for p in pts:
        if q == p:
            return ("vertex", p)
    for k in range(3):
        a, b = pts[k], pts[(k + 1) % 3]
        if orient(a, b, q) == 0:
            return ("edge", (a, b) if a < b else (b, a))
    return ("triangle", index)
