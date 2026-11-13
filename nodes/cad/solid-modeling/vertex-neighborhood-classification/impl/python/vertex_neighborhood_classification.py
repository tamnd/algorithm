# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertex-neighborhood-classification/. The authors are listed in prov/QA5D08.jsonl.

"""Mantyla's Boolean operation by vertex neighborhood classification, in the plane.

This is the two-dimensional form of the algorithm. A solid is a simple polygon,
a list of points in counterclockwise order. Its boundary is a closed loop of
edges, and the neighborhood of a boundary vertex is a set of two sectors
between the incoming and the outgoing edge: the inside sector and the outside
sector. In three dimensions the sectors lie between the faces around a vertex,
and the same four steps apply: generate, classify, select, connect.

The result of boolean(A, B, op) is the boundary of the regularized set
A op* B, as a list of loops. Each loop is a list of points, the region is on
the left of every edge, so outer loops are counterclockwise and holes are
clockwise. Coordinates are int or Fraction, and every sign is exact.
"""

from fractions import Fraction
from typing import Union

Num = Union[int, Fraction]
Point = tuple

IN, OUT, ON_SAME, ON_OPPOSITE = "in", "out", "on-same", "on-opposite"

# Which edges each operation keeps: (classes kept from A, classes kept from B, B reversed?)
SELECT = {
    "union": ({OUT, ON_SAME}, {OUT}, False),
    "intersection": ({IN, ON_SAME}, {IN}, False),
    "difference": ({OUT, ON_OPPOSITE}, {IN}, True),
}


def cross(o: Point, a: Point, b: Point) -> Num:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def pseudo_angle(x: Num, y: Num) -> Fraction:
    """A rational number in [0, 4) that increases with the angle of (x, y)."""
    if y >= 0 and x > 0 or (x == 0 and y > 0):
        return Fraction(y) / (x + y)
    if x <= 0 and y >= 0:
        return 1 + Fraction(-x) / (-x + y)
    if x < 0 or (x == 0 and y < 0):
        return 2 + Fraction(-y) / (-x - y)
    return 3 + Fraction(x) / (x - y)


def turn(d0: Point, d1: Point) -> Fraction:
    """The counterclockwise rotation from direction d0 to direction d1, in (0, 4] pseudo-angle units."""
    r = (pseudo_angle(*d1) - pseudo_angle(*d0)) % 4
    return r if r != 0 else Fraction(4)


def _on_segment(p: Point, a: Point, b: Point) -> bool:
    return (cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def _meet(p: Point, q: Point, r: Point, s: Point) -> list:
    """The points where the segments pq and rs meet: none, one, or the two ends of an overlap."""
    d1, d2, d3, d4 = cross(r, s, p), cross(r, s, q), cross(p, q, r), cross(p, q, s)
    if d1 == d2 == 0:  # collinear: the ends that lie on the other segment
        return [x for x in (p, q, r, s) if _on_segment(x, p, q) and _on_segment(x, r, s)]
    if (d1 > 0) == (d2 > 0) and d1 != 0 and d2 != 0:
        return []
    if (d3 > 0) == (d4 > 0) and d3 != 0 and d4 != 0:
        return []
    t = Fraction(d1) / (d1 - d2)
    return [(p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))]


def generate(P: list, Q: list) -> list:
    """Split the edges of polygon P at every point where they meet the boundary of Q."""
    out = []
    n, m = len(P), len(Q)
    for i in range(n):
        p, q = P[i], P[(i + 1) % n]
        cuts = set()
        for j in range(m):
            cuts.update(_meet(p, q, Q[j], Q[(j + 1) % m]))
        d = (q[0] - p[0], q[1] - p[1])
        key = lambda x: (x[0] - p[0]) * d[0] + (x[1] - p[1]) * d[1]
        inner = sorted((x for x in cuts if x != p and x != q), key=key)
        out.append(p)
        out.extend(inner)
    return out


def point_in_polygon(x: Point, P: list) -> bool:
    """Crossing number test for a point that is not on the boundary of P."""
    inside = False
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        if (a[1] > x[1]) != (b[1] > x[1]):
            if (cross(a, b, x) > 0) == (b[1] > a[1]):
                inside = not inside
    return inside


def classify(P: list, Q: list) -> list:
    """The class of each edge of the split loop P with respect to the split loop Q."""
    n, m = len(P), len(Q)
    edges_q = {(Q[j], Q[(j + 1) % m]) for j in range(m)}
    where = {Q[j]: j for j in range(m)}
    cls = [None] * n
    starts = [i for i in range(n) if P[i] in where]
    if not starts:  # the loops do not meet: one containment test for the whole loop
        mid = tuple((P[0][k] + P[1][k]) / Fraction(2) for k in range(2))
        return [IN if point_in_polygon(mid, Q) else OUT] * n
    for step in range(n):
        i = (starts[0] + step) % n
        u, w = P[i], P[(i + 1) % n]
        if (u, w) in edges_q:  # @line L3
            cls[i] = ON_SAME
        elif (w, u) in edges_q:
            cls[i] = ON_OPPOSITE
        elif u in where:  # @line L4
            j = where[u]
            nxt, prv = Q[(j + 1) % m], Q[j - 1]
            d_out = (nxt[0] - u[0], nxt[1] - u[1])
            d_back = (prv[0] - u[0], prv[1] - u[1])
            d = (w[0] - u[0], w[1] - u[1])
            cls[i] = IN if turn(d_out, d) < turn(d_out, d_back) else OUT  # the inside sector of Q at u
        else:
            cls[i] = cls[i - 1]  # @line L5
    return cls


def connect(edges: list) -> list:
    """Join directed edges into loops; at a vertex with two exits take the first one clockwise."""
    out_of = {}
    for e in edges:
        out_of.setdefault(e[0], []).append(e)
    used = set()
    loops = []
    for e in edges:  # @line L8
        if e in used:
            continue
        loop, cur = [e[0]], e  # @line L9
        used.add(e)
        while True:
            v = cur[1]
            back = (cur[0][0] - v[0], cur[0][1] - v[1])
            nxt = min(out_of[v], key=lambda f: turn((f[1][0] - v[0], f[1][1] - v[1]), back))  # @line L10
            if nxt == e:  # @line L11
                break
            if nxt in used:
                raise ValueError("the selected edges do not form loops")
            loop.append(v)
            used.add(nxt)
            cur = nxt
        loops.append(loop)
    return loops


def boolean(A: list, B: list, op: str) -> list:
    """The boundary loops of A op* B for counterclockwise simple polygons A and B."""
    SA, SB = generate(A, B), generate(B, A)  # @line L1
    ca, cb = classify(SA, SB), classify(SB, SA)  # @line L2
    keep_a, keep_b, reverse_b = SELECT[op]
    S = [(SA[i], SA[(i + 1) % len(SA)]) for i in range(len(SA)) if ca[i] in keep_a]  # @line L6
    for i in range(len(SB)):
        if cb[i] in keep_b:
            u, w = SB[i], SB[(i + 1) % len(SB)]
            S.append((w, u) if reverse_b else (u, w))
    return connect(S)  # @line L7


def winding_number(x: Point, loops: list) -> int:
    """The winding number of the loops around a point that is on none of them."""
    w = 0
    for P in loops:
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            if a[1] <= x[1] < b[1] and cross(a, b, x) > 0:
                w += 1
            elif b[1] <= x[1] < a[1] and cross(a, b, x) < 0:
                w -= 1
    return w


def area(loops: list) -> Fraction:
    """The signed area of the region bounded by the loops (shoelace formula)."""
    s = Fraction(0)
    for P in loops:
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            s += a[0] * b[1] - a[1] * b[0]
    return s / 2
