# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fortunes-algorithm/. The authors are listed in prov/A89AWB.jsonl.

import heapq
from fractions import Fraction

Point = tuple[int, int]
FPoint = tuple[Fraction, Fraction]


def _sign(v) -> int:
    return (v > 0) - (v < 0)


def orient(a: Point, b: Point, c: Point) -> int:
    """Sign of (b - a) x (c - a): 1 for a left turn, -1 for a right turn, 0 when collinear."""
    return _sign((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))


def sign_plus_root(p, q, r) -> int:
    """Exact sign of p + q * r^(1/2) for rationals p, q and r >= 0."""
    sp, sq = _sign(p), (_sign(q) if r != 0 else 0)
    if sq == 0 or sp == sq:
        return sp if sp != 0 else sq
    if sp == 0:
        return sq
    return sp * _sign(p * p - q * q * r)


def circumcenter(a: Point, b: Point, c: Point) -> FPoint:
    """Exact circumcenter of three points that are not collinear."""
    bx, by = b[0] - a[0], b[1] - a[1]
    cx, cy = c[0] - a[0], c[1] - a[1]
    d = 2 * (bx * cy - by * cx)
    ux = Fraction(cy * (bx * bx + by * by) - by * (cx * cx + cy * cy), d)
    uy = Fraction(bx * (cx * cx + cy * cy) - cx * (bx * bx + by * by), d)
    return (a[0] + ux, a[1] + uy)


class Event:
    """A site event (r2 = 0) or a circle event at height y = ya - r2^(1/2) and abscissa x."""

    __slots__ = ("ya", "r2", "x", "kind", "seq", "site", "arc", "valid")

    def __init__(self, ya, r2, x, kind: int, seq: int, site: int = -1, arc=None) -> None:
        self.ya, self.r2, self.x, self.kind, self.seq = ya, r2, x, kind, seq
        self.site, self.arc, self.valid = site, arc, True

    def __lt__(self, o: "Event") -> bool:
        # higher y first: compare ya - r2^(1/2) with o.ya - o.r2^(1/2) exactly
        u = self.ya - o.ya
        s = sign_plus_root(u, 1, o.r2)
        if self.r2 != 0:
            s = -1 if s <= 0 else sign_plus_root(u * u + o.r2 - self.r2, 2 * u, o.r2)
        if s != 0:
            return s > 0
        return (self.x, self.kind, self.seq) < (o.x, o.kind, o.seq)


class Trace:
    """The part of a Voronoi edge traced by one breakpoint. start: ('inf',), ('vertex', V) or ('split', P)."""

    __slots__ = ("pair", "start", "end", "twin")

    def __init__(self, i: int, j: int, start: tuple) -> None:
        self.pair, self.start, self.end, self.twin = frozenset((i, j)), start, None, None


class Arc:
    __slots__ = ("site", "prev", "next", "event", "right")

    def __init__(self, site: int) -> None:
        self.site, self.prev, self.next, self.event, self.right = site, None, None, None, None


def breakpoint_side(sx: int, p: Point, q: Point, ly: int) -> int:
    """Sign of sx - b, where b is the x of the breakpoint between the arc of p (left) and of q (right)
    when the sweep line is at y = ly (ly <= py, ly <= qy, not both equal unless py = qy)."""
    if p[1] == q[1]:
        return _sign(2 * sx - p[0] - q[0])
    dp, dq = p[1] - ly, q[1] - ly
    a = q[1] - p[1]
    bh = dq * p[0] - dp * q[0]
    c = dq * p[0] * p[0] - dp * q[0] * q[0] + dp * dq * (p[1] - q[1])
    disc = bh * bh - a * c
    # the breakpoint is (bh + disc^(1/2)) / a in both cases py > qy and py < qy
    return _sign(a) * sign_plus_root(a * sx - bh, -1, disc)


def fortune(points: list[Point]) -> tuple[list[FPoint], dict[frozenset, tuple]]:
    """Voronoi diagram of the points by Fortune's sweep, with exact arithmetic.

    Returns (vertices, edges). vertices is the sorted list of Voronoi vertices (pairs of Fractions; a vertex
    shared by four or more cocircular sites appears once). edges maps frozenset({p, q}) of two sites with a
    common edge of positive length to its two ends, sorted, where None stands for an end at infinity.
    Duplicates are removed. Coordinates must be int.
    Cost: O(n log n) events and heap operations; this version finds the arc above a site by walking the beach
    line, which is O(n) per site, so O(n^2) time in the worst case; O(n) space.
    """
    pts = sorted(set(points), key=lambda p: (-p[1], p[0]))  # @line L1
    n = len(pts)
    traces: list[Trace] = []
    vertices: set[FPoint] = set()
    if n == 0:
        return [], {}
    top = sum(1 for p in pts if p[1] == pts[0][1])
    head = last = Arc(0)  # the top row: arcs side by side, vertical edges that come from infinity
    for i in range(1, top):
        node = Arc(i)
        last.next, node.prev = node, last
        last.right = Trace(i - 1, i, ("inf",))
        traces.append(last.right)
        last = node
    queue: list[Event] = [Event(pts[i][1], 0, pts[i][0], 1, i, site=i) for i in range(top, n)]  # @line L2
    heapq.heapify(queue)
    seq = [n]

    def check_circle(b: Arc) -> None:
        a, c = b.prev, b.next
        if a is None or c is None or a.site == c.site:
            return
        pa, pb, pc = pts[a.site], pts[b.site], pts[c.site]
        if orient(pa, pb, pc) >= 0:
            return
        cx, cy = circumcenter(pa, pb, pc)
        r2 = (cx - pa[0]) ** 2 + (cy - pa[1]) ** 2
        seq[0] += 1
        b.event = Event(cy, r2, cx, 0, seq[0], arc=b)
        heapq.heappush(queue, b.event)

    def drop_event(b: Arc | None) -> None:
        if b is not None and b.event is not None:
            b.event.valid = False
            b.event = None

    while queue:  # @line L3
        ev = heapq.heappop(queue)
        if not ev.valid:
            continue
        if ev.kind == 1:  # @line L4
            s = ev.site
            sx, sy = pts[s]
            a = head
            while a.next is not None and breakpoint_side(sx, pts[a.site], pts[a.next.site], sy) > 0:  # @line L5
                a = a.next
            drop_event(a)  # @line L6
            ax, ay = pts[a.site]
            split = (Fraction(sx), Fraction((sx - ax) ** 2 + ay * ay - sy * sy, 2 * (ay - sy)))
            node, a2 = Arc(s), Arc(a.site)  # @line L7
            a2.next, a2.right = a.next, a.right
            if a.next is not None:
                a.next.prev = a2
            a.next, node.prev, node.next, a2.prev = node, a, a2, node
            t1, t2 = Trace(a.site, s, ("split", split)), Trace(s, a.site, ("split", split))
            t1.twin, t2.twin = t2, t1
            a.right, node.right = t1, t2
            traces += [t1, t2]
            check_circle(a)  # @line L8
            check_circle(a2)
        else:  # @line L9
            b = ev.arc
            a, c = b.prev, b.next
            v = (ev.x, ev.ya)
            vertices.add(v)  # @line L10
            a.right.end = v
            b.right.end = v
            a.right = Trace(a.site, c.site, ("vertex", v))  # @line L11
            traces.append(a.right)
            a.next, c.prev = c, a  # @line L12
            drop_event(a)
            drop_event(c)
            check_circle(a)  # @line L13
            check_circle(c)
    edges: dict[frozenset, tuple] = {}  # @line L14
    done: set[int] = set()
    for t in traces:
        if id(t) in done:
            continue
        if t.twin is not None:
            done.add(id(t.twin))
            ends = [t.end, t.twin.end]
        else:
            ends = [t.start[1] if t.start[0] == "vertex" else None, t.end]
        if ends[0] is not None and ends[0] == ends[1]:
            continue  # an edge of length zero at a vertex of four or more cocircular sites
        key = frozenset(pts[i] for i in t.pair)
        assert key not in edges
        edges[key] = tuple(sorted(ends, key=lambda e: (e is None, e)))
    return sorted(vertices), edges
