# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greiner-hormann-algorithm/. The authors are listed in prov/34CRJR.jsonl.

from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


class DegenerateError(ValueError):
    """The boundaries touch at a vertex or overlap along a segment; perturb the input and retry."""


class Node:
    __slots__ = ("p", "next", "prev", "neighbor", "alpha", "intersect", "entry", "visited")

    def __init__(self, p: Point, intersect: bool = False, alpha: Fraction = Fraction(0)) -> None:
        self.p = p
        self.next: Optional["Node"] = None
        self.prev: Optional["Node"] = None
        self.neighbor: Optional["Node"] = None
        self.alpha = alpha
        self.intersect = intersect
        self.entry = False
        self.visited = False


def orient(p: Point, q: Point, r: Point) -> Number:
    """Twice the signed area of the triangle pqr: positive for a left turn, zero when collinear."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def point_in_polygon(polygon: list[Point], p: Point) -> bool:
    """Even-odd rule by crossing number, for a point that is not on the boundary."""
    inside = False
    n = len(polygon)
    for i in range(n):
        a, b = polygon[i], polygon[(i + 1) % n]
        if (a[1] > p[1]) != (b[1] > p[1]):
            # the edge crosses the horizontal line through p; is the crossing to the right of p?
            if (orient(a, b, p) > 0) == (b[1] > a[1]):
                inside = not inside
    return inside


def _check_polygon(polygon: list[Point], name: str) -> None:
    if len(polygon) < 3 or len(set(polygon)) != len(polygon):
        raise ValueError(f"{name} needs at least 3 distinct vertices")
    n = len(polygon)
    if sum(orient((0, 0), polygon[i], polygon[(i + 1) % n]) for i in range(n)) == 0:
        raise ValueError(f"{name} has zero area")


def _segment_hit(a: Point, b: Point, c: Point, d: Point) -> Optional[tuple[Fraction, Fraction]]:
    """Parameters (s, t) of a crossing of ab and cd strictly inside both; None if they miss.

    Raises DegenerateError if the closed segments meet in any other way.
    """
    den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
    if den == 0:
        if orient(a, b, c) != 0:
            return None  # parallel, on different lines
        # collinear: do the closed segments share a point?
        k = 0 if a[0] != b[0] else 1
        lo1, hi1 = sorted((a[k], b[k]))
        lo2, hi2 = sorted((c[k], d[k]))
        if max(lo1, lo2) <= min(hi1, hi2):
            raise DegenerateError("two edges overlap or touch along a line")
        return None
    sn = (c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0])
    tn = (c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0])
    s, t = Fraction(sn) / den, Fraction(tn) / den
    if 0 < s < 1 and 0 < t < 1:
        return s, t
    if 0 <= s <= 1 and 0 <= t <= 1:
        raise DegenerateError("the boundaries meet at a vertex")
    return None


def _ring(polygon: list[Point]) -> list[Node]:
    nodes = [Node(p) for p in polygon]
    n = len(nodes)
    for i in range(n):
        nodes[i].next = nodes[(i + 1) % n]
        nodes[i].prev = nodes[i - 1]
    return nodes


def _insert(start: Node, items: list[tuple[Fraction, Node]]) -> None:
    """Insert intersection nodes after the vertex start, in increasing order of alpha."""
    end = start.next
    prev = start
    for _, node in sorted(items, key=lambda it: it[0]):
        node.prev, node.next = prev, end
        prev.next = node
        end.prev = node
        prev = node


def _mark(first: Node, other: list[Point]) -> None:
    inside = point_in_polygon(other, first.p)
    node = first
    while True:
        if node.intersect:
            node.entry = not inside
            inside = not inside
        node = node.next
        if node is first:
            break


def greiner_hormann(subject: list[Point], clip: list[Point], op: str = "intersection") -> list[list[Point]]:
    """Boolean operation of two simple polygons by the Greiner-Hormann algorithm.

    subject and clip are lists of vertices in either orientation, with int or Fraction coordinates.
    op is "intersection", "union" or "difference" (subject minus clip). The result is a list of
    closed rings; a point is in the result when it lies inside an odd number of rings (holes are
    rings inside other rings). Raises DegenerateError when the two boundaries meet at a vertex of
    either polygon or overlap along a segment. Cost: O(n m) time for n and m vertices, plus
    O(k log k) to sort the k intersection points.
    """
    if op not in ("intersection", "union", "difference"):
        raise ValueError("op must be intersection, union or difference")
    _check_polygon(subject, "subject")
    _check_polygon(clip, "clip")
    sv, cv = _ring(subject), _ring(clip)
    n, m = len(subject), len(clip)
    on_s: list[list[tuple[Fraction, Node]]] = [[] for _ in range(n)]
    on_c: list[list[tuple[Fraction, Node]]] = [[] for _ in range(m)]
    count = 0
    for i in range(n):  # @line L1
        a, b = subject[i], subject[(i + 1) % n]
        for j in range(m):
            c, d = clip[j], clip[(j + 1) % m]
            hit = _segment_hit(a, b, c, d)
            if hit is None:
                continue
            s, t = hit
            p = (a[0] + s * (b[0] - a[0]), a[1] + s * (b[1] - a[1]))
            u, w = Node(p, True, s), Node(p, True, t)
            u.neighbor, w.neighbor = w, u
            on_s[i].append((s, u))
            on_c[j].append((t, w))
            count += 1
    if count == 0:  # @line L2
        return _no_crossing(subject, clip, op)
    for i in range(n):  # @line L3
        _insert(sv[i], on_s[i])
    for j in range(m):
        _insert(cv[j], on_c[j])
    _mark(sv[0], clip)  # @line L4
    _mark(cv[0], subject)
    flip_s = op in ("union", "difference")  # @line L5
    flip_c = op == "union"
    for first, flip in ((sv[0], flip_s), (cv[0], flip_c)):
        node = first
        while True:
            if node.intersect and flip:
                node.entry = not node.entry
            node = node.next
            if node is first:
                break
    rings: list[list[Point]] = []
    node = sv[0]
    pending = []
    while True:
        if node.intersect:
            pending.append(node)
        node = node.next
        if node is sv[0]:
            break
    for start in pending:  # @line L6
        if start.visited:
            continue
        ring = [start.p]
        cur = start
        while True:
            cur.visited = cur.neighbor.visited = True  # @line L7
            if cur.entry:  # @line L8
                while True:
                    cur = cur.next
                    ring.append(cur.p)
                    if cur.intersect:
                        break
            else:  # @line L9
                while True:
                    cur = cur.prev
                    ring.append(cur.p)
                    if cur.intersect:
                        break
            cur = cur.neighbor  # @line L10
            if cur.visited:  # @line L11
                break
        if ring[-1] == ring[0]:
            ring.pop()
        rings.append(ring)
    return rings


def _no_crossing(subject: list[Point], clip: list[Point], op: str) -> list[list[Point]]:
    """The boundaries do not meet: the polygons are nested or disjoint."""
    s_in_c = point_in_polygon(clip, subject[0])
    c_in_s = point_in_polygon(subject, clip[0])
    if op == "intersection":
        return [list(subject)] if s_in_c else [list(clip)] if c_in_s else []
    if op == "union":
        return [list(clip)] if s_in_c else [list(subject)] if c_in_s else [list(subject), list(clip)]
    if s_in_c:
        return []
    return [list(subject), list(clip)] if c_in_s else [list(subject)]


def ring_area2(ring: list[Point]) -> Number:
    """Twice the signed area of a ring by the shoelace formula."""
    n = len(ring)
    return sum(ring[i][0] * ring[(i + 1) % n][1] - ring[(i + 1) % n][0] * ring[i][1] for i in range(n))
