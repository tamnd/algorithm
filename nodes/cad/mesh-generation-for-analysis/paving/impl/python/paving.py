# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paving/. The authors are listed in prov/AS3MCY.jsonl.

"""The core step of paving: lay one row of quads inside a closed front.

This is one step of Blacker and Stephenson's paving, not the whole mesher.
The front is a closed polygon in counterclockwise order around the region that
is still empty. Each front node is classified by its interior angle:

* a row end, if the angle is below END_ANGLE: the node gets no new node, and
  one quad (prev, node, next, q) covers both of its edges, with
  q = prev + next - node, the fourth corner of a parallelogram;
* a row side, otherwise: the node gets a new node at the distance h from the
  lines of both of its edges, inside, where h is the mean length of the two
  edges.

The new nodes of the two neighbours of a row end are merged into q. The row is
accepted only if every quad is strictly convex and counterclockwise and the
new front is a simple polygon, tested exactly on the float coordinates (each
float converts to a Fraction without rounding). Otherwise the step reports
failure. The angle thresholds are parameters of this code; paving as published
uses its own classification with more node types (row corners and reversals),
smoothing, seaming and closure, which are not here.
"""

import math
from typing import List, Optional, Sequence, Tuple

from mg3geom import exact, is_valid_planar_mesh, orient2d, twice_area

Vec = Tuple[float, float]
END_ANGLE = 3 * math.pi / 4
MAX_SIDE_ANGLE = 4 * math.pi / 3


def interior_angle(p: Vec, q: Vec, r: Vec) -> float:
    """The interior angle at q of a counterclockwise polygon with edges pq, qr."""
    u = (p[0] - q[0], p[1] - q[1])
    v = (r[0] - q[0], r[1] - q[1])
    a = math.atan2(u[0] * v[1] - u[1] * v[0], u[0] * v[0] + u[1] * v[1])
    # angle from v to u counterclockwise is the interior angle for a CCW polygon
    return (-a) % (2 * math.pi)


def classify(front: Sequence[Vec]) -> List[str]:
    n = len(front)
    out = []
    for i in range(n):
        a = interior_angle(front[i - 1], front[i], front[(i + 1) % n])
        out.append("end" if a < END_ANGLE else "side" if a < MAX_SIDE_ANGLE else "other")
    return out


def inward_offset(p: Vec, q: Vec, r: Vec, h: float) -> Vec:
    """The point inside a counterclockwise polygon at the distance h from the
    lines pq and qr, on the bisector at q."""
    def unit_in(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        return (-dy / L, dx / L)   # left normal, inward for a CCW polygon
    na, nb = unit_in(p, q), unit_in(q, r)
    s = 1.0 + na[0] * nb[0] + na[1] * nb[1]
    return (q[0] + h * (na[0] + nb[0]) / s, q[1] + h * (na[1] + nb[1]) / s)


def is_simple_polygon(poly: Sequence) -> bool:
    """Exact test: non-adjacent closed edges do not meet, adjacent edges do not fold back."""
    def on(p, q, x):
        return min(p[0], q[0]) <= x[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= x[1] <= max(p[1], q[1])

    def meet(a, b, c, d):
        o1, o2, o3, o4 = orient2d(a, b, c), orient2d(a, b, d), orient2d(c, d, a), orient2d(c, d, b)
        if o1 * o2 < 0 and o3 * o4 < 0:
            return True
        return ((o1 == 0 and on(a, b, c)) or (o2 == 0 and on(a, b, d))
                or (o3 == 0 and on(c, d, a)) or (o4 == 0 and on(c, d, b)))
    n = len(poly)
    if n < 3:
        return False
    for i in range(n):
        a, b, c = poly[i], poly[(i + 1) % n], poly[(i + 2) % n]
        if orient2d(a, b, c) == 0 and (a[0] - b[0]) * (c[0] - b[0]) + (a[1] - b[1]) * (c[1] - b[1]) > 0:
            return False
        for j in range(i + 2, n):
            if not (i == 0 and j == n - 1) and meet(poly[i], poly[(i + 1) % n], poly[j], poly[(j + 1) % n]):
                return False
    return True


def pave_row(front: Sequence[Vec]):
    """One row of paving. Returns (points, quads, new_front, None) on success,
    where points = front + new nodes, quads are counterclockwise index 4-tuples
    and new_front is a list of indices into points; or (None, None, None, reason)."""
    n = len(front)
    kind = classify(front)  # @line L1
    if "other" in kind:
        return None, None, None, "a reflex node needs a row corner or reversal, not handled here"
    ends = [i for i in range(n) if kind[i] == "end"]
    for a in ends:
        for b in ends:
            if a != b and min((a - b) % n, (b - a) % n) < 3:
                return None, None, None, "two row ends are too close"
    points: List[Vec] = list(front)
    new_index = [None] * n
    for c in ends:  # @line L2
        p, q, r = front[c - 1], front[c], front[(c + 1) % n]
        points.append((p[0] + r[0] - q[0], p[1] + r[1] - q[1]))
        new_index[c - 1] = new_index[(c + 1) % n] = len(points) - 1
    for i in range(n):  # @line L3
        if kind[i] == "side" and new_index[i] is None:
            p, q, r = front[i - 1], front[i], front[(i + 1) % n]
            h = (math.dist(p, q) + math.dist(q, r)) / 2
            points.append(inward_offset(p, q, r, h))
            new_index[i] = len(points) - 1
    quads: List[Tuple[int, int, int, int]] = []
    for i in range(n):  # @line L4
        j = (i + 1) % n
        if kind[j] == "end":
            quads.append((i, j, (j + 1) % n, new_index[i]))
        elif kind[i] != "end":
            quads.append((i, j, new_index[j], new_index[i]))
    new_front: List[int] = []
    for i in range(n - 1, -1, -1):  # @line L5
        if kind[i] == "end":
            continue
        k = new_index[i]
        if not new_front or new_front[-1] != k:
            new_front.append(k)
    if len(new_front) > 1 and new_front[0] == new_front[-1]:
        new_front.pop()
    new_front.reverse()
    E = [exact(p) for p in points]
    if not is_valid_planar_mesh(E, quads):  # @line L6
        return None, None, None, "a quad of the row is not strictly convex"
    inner = [E[k] for k in new_front]
    if not is_simple_polygon(inner) or twice_area(inner) <= 0:  # @line L7
        return None, None, None, "the new front is not simple"
    return points, quads, new_front, None  # @line L8


def quad_count_parity(quads: Sequence[Sequence[int]]) -> Tuple[int, int, int]:
    """(4 Q, interior edges, boundary edges) of a quad mesh, by counting edge sides."""
    sides = {}
    for q in quads:
        for s in range(4):
            e = frozenset((q[s], q[(s + 1) % 4]))
            sides[e] = sides.get(e, 0) + 1
    return 4 * len(quads), sum(1 for v in sides.values() if v == 2), sum(1 for v in sides.values() if v == 1)
