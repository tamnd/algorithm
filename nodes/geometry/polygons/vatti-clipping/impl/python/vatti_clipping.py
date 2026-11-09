# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vatti-clipping/. The authors are listed in prov/AT6FZP.jsonl.

"""Boolean operations on general polygons by a scanbeam sweep, in the style of Vatti.

This version keeps Vatti's sweep (scanbeams between vertex heights, crossings found by
sorting the active edges, winding numbers of both polygons tracked along each beam) but
builds the output in a separate pass: it emits the result as trapezoids per sub-beam and
then links their boundaries into contours. Vatti's paper builds the contours during the
sweep instead, with left and right bounds that start at local minima and join at local
maxima.
"""

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]

FILL_RULES = ("evenodd", "nonzero")
OPERATIONS = ("intersection", "union", "difference", "xor")


def filled(w: int, rule: str) -> bool:
    return w % 2 == 1 if rule == "evenodd" else w != 0


def combine(a: bool, b: bool, op: str) -> bool:
    if op == "intersection":
        return a and b
    if op == "union":
        return a or b
    if op == "difference":
        return a and not b
    return a != b


class Edge:
    """A non-horizontal edge stored from its lower to its upper end."""

    __slots__ = ("x0", "y0", "x1", "y1", "poly", "w")

    def __init__(self, p: Point, q: Point, poly: int) -> None:
        # w is the change of the winding number when a point moves from left to right across
        # the edge: +1 for a downward edge, -1 for an upward edge.
        if p[1] < q[1]:
            self.x0, self.y0, self.x1, self.y1, self.w = p[0], p[1], q[0], q[1], -1
        else:
            self.x0, self.y0, self.x1, self.y1, self.w = q[0], q[1], p[0], p[1], 1
        self.poly = poly

    def x_at(self, y: Number) -> Number:
        if y == self.y0:
            return self.x0
        if y == self.y1:
            return self.x1
        return self.x0 + Fraction(self.x1 - self.x0) * (y - self.y0) / (self.y1 - self.y0)

    def crossing_y(self, other: "Edge", ya: Number, yb: Number) -> Fraction:
        """Height where two edges cross inside (ya, yb); x - x' is linear in y."""
        da = self.x_at(ya) - other.x_at(ya)
        db = self.x_at(yb) - other.x_at(yb)
        return ya + Fraction(da) * (yb - ya) / (da - db)


def contours_edges(contours: Sequence[Sequence[Point]], poly: int) -> list[Edge]:
    edges = []
    for c in contours:
        n = len(c)
        for i in range(n):
            p, q = c[i], c[(i + 1) % n]
            if p[1] != q[1]:
                edges.append(Edge(p, q, poly))
    return edges


def covered(intervals: list[tuple[Number, Number]], x: Number) -> bool:
    return any(lo < x < hi for lo, hi in intervals)


def link(segments: list[tuple[Point, Point]]) -> list[list[Point]]:
    """Join directed segments, balanced at every point, into closed contours."""
    out_of: dict[Point, list[Point]] = {}
    for a, b in segments:
        out_of.setdefault(a, []).append(b)
    contours = []
    for start in list(out_of):
        while out_of[start]:
            cycle, p = [start], out_of[start].pop()
            while p != start:
                cycle.append(p)
                p = out_of[p].pop()
            contours.append(drop_collinear(cycle))
    return [c for c in contours if len(c) >= 3]


def drop_collinear(cycle: list[Point]) -> list[Point]:
    changed = True
    while changed and len(cycle) >= 3:
        changed = False
        for i in range(len(cycle)):
            a, b, c = cycle[i - 1], cycle[i], cycle[(i + 1) % len(cycle)]
            cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            dot = (b[0] - a[0]) * (c[0] - b[0]) + (b[1] - a[1]) * (c[1] - b[1])
            if cross == 0 and dot > 0:
                del cycle[i]
                changed = True
                break
    return cycle


def vatti_clip(
    subject: Sequence[Sequence[Point]],
    clip: Sequence[Sequence[Point]],
    op: str = "intersection",
    rule: str = "nonzero",
) -> list[list[Point]]:
    """Boolean operation of two sets of contours.

    subject and clip are lists of closed contours; each may be self-intersecting, and holes are
    given as further contours. rule ("nonzero" or "evenodd") decides which points each input
    covers, from its winding number. op is "intersection", "union", "difference" or "xor".
    The result is a list of closed contours whose winding numbers add up to 1 at every point of
    the result and to 0 elsewhere, off the boundaries. Contours may touch at vertices.
    Time O((n + k) n log n) for n input vertices and k edge crossings.
    """
    if op not in OPERATIONS or rule not in FILL_RULES:
        raise ValueError("unknown operation or fill rule")
    edges = contours_edges(subject, 0) + contours_edges(clip, 1)
    ys = sorted({e.y0 for e in edges} | {e.y1 for e in edges})  # @line L1
    beams: list[tuple[Number, Number, list[tuple[Edge, Edge]]]] = []
    for y0, y1 in zip(ys, ys[1:]):  # @line L2
        active = [e for e in edges if e.y0 <= y0 and e.y1 >= y1]
        active.sort(key=lambda e: (e.x_at(y0), e.x_at(y1)))  # @line L3
        cuts = {y0, y1}
        top = [e.x_at(y1) for e in active]
        for i in range(1, len(active)):  # @line L4
            j = i
            while j > 0 and top[j - 1] > top[j]:
                cuts.add(active[j - 1].crossing_y(active[j], y0, y1))
                active[j - 1], active[j] = active[j], active[j - 1]
                top[j - 1], top[j] = top[j], top[j - 1]
                j -= 1
        cuts = sorted(cuts)
        for ya, yb in zip(cuts, cuts[1:]):  # @line L5
            ym = (ya + yb) / 2
            order = sorted(active, key=lambda e: e.x_at(ym))
            ws = wc = 0
            spans: list[tuple[Edge, Edge]] = []
            left = None
            i = 0
            while i < len(order):  # @line L6
                x = order[i].x_at(ym)
                was_in = combine(filled(ws, rule), filled(wc, rule), op)
                first = order[i]
                while i < len(order) and order[i].x_at(ym) == x:
                    if order[i].poly == 0:
                        ws += order[i].w
                    else:
                        wc += order[i].w
                    i += 1
                now_in = combine(filled(ws, rule), filled(wc, rule), op)
                if now_in and not was_in:  # @line L7
                    left = first
                elif was_in and not now_in:
                    spans.append((left, first))
            beams.append((ya, yb, spans))

    segments: list[tuple[Point, Point]] = []
    levels: dict[Number, list[list[tuple[Number, Number]]]] = {}
    for ya, yb, spans in beams:
        levels.setdefault(ya, [[], []])[1].extend((l.x_at(ya), r.x_at(ya)) for l, r in spans)
        levels.setdefault(yb, [[], []])[0].extend((l.x_at(yb), r.x_at(yb)) for l, r in spans)
        for l, r in spans:  # @line L8
            segments.append(((r.x_at(ya), ya), (r.x_at(yb), yb)))
            segments.append(((l.x_at(yb), yb), (l.x_at(ya), ya)))
    for y, (below, above) in levels.items():  # @line L9
        xs = sorted({x for iv in below + above for x in iv})
        for xa, xb in zip(xs, xs[1:]):
            xm = (xa + xb) / 2
            up, down = covered(above, xm), covered(below, xm)
            if up and not down:
                segments.append(((xa, y), (xb, y)))
            elif down and not up:
                segments.append(((xb, y), (xa, y)))
    return link(segments)  # @line L10
