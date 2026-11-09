# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/funnel-algorithm/. The authors are listed in prov/GH08T5.jsonl.

from collections import deque
from fractions import Fraction
from math import hypot
from typing import Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


def orient(p: Point, q: Point, r: Point) -> Number:
    """Twice the signed area of the triangle pqr: positive for a left turn, zero when collinear."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def twice_area(polygon: list[Point]) -> Number:
    n = len(polygon)
    return sum(polygon[i][0] * polygon[(i + 1) % n][1] - polygon[(i + 1) % n][0] * polygon[i][1] for i in range(n))


def in_closed_triangle(a: Point, b: Point, c: Point, p: Point) -> bool:
    """True when p is in the closed triangle abc, which is counterclockwise."""
    return orient(a, b, p) >= 0 and orient(b, c, p) >= 0 and orient(c, a, p) >= 0


def ear_clipping(polygon: list[Point]) -> list[tuple[int, int, int]]:
    """Triangulate a simple counterclockwise polygon by clipping ears, in O(n^3) worst case time.

    Straight vertices (three collinear consecutive vertices) are allowed. Each triangle is a
    counterclockwise triple of vertex indices with positive area.
    """
    n = len(polygon)
    if n < 3 or twice_area(polygon) <= 0:
        raise ValueError("the polygon must have at least 3 vertices in counterclockwise order")
    idx = list(range(n))
    out = []
    while len(idx) > 3:
        m = len(idx)
        for k in range(m):
            i, j, l = idx[k - 1], idx[k], idx[(k + 1) % m]
            a, b, c = polygon[i], polygon[j], polygon[l]
            if orient(a, b, c) <= 0:
                continue
            if any(in_closed_triangle(a, b, c, polygon[x]) for x in idx if x not in (i, j, l)):
                continue
            out.append((i, j, l))
            del idx[k]
            break
        else:
            raise ValueError("no ear found: the polygon is not simple")
    i, j, l = idx
    if orient(polygon[i], polygon[j], polygon[l]) <= 0:
        raise ValueError("no ear found: the polygon is not simple")
    out.append((i, j, l))
    return out


def sleeve(polygon: list[Point], triangles: list[tuple[int, int, int]], s: Point, t: Point) -> list[tuple[int, int]]:
    """The portals crossed by the dual tree path from a triangle containing s to one containing t.

    Each portal is a pair (left, right) of vertex indices, as seen when walking from s to t.
    """
    tris = []
    for a, b, c in triangles:
        if orient(polygon[a], polygon[b], polygon[c]) < 0:
            b, c = c, b
        if orient(polygon[a], polygon[b], polygon[c]) == 0:
            raise ValueError("a triangle has zero area")
        tris.append((a, b, c))
    by_edge: dict[tuple[int, int], int] = {}
    for k, (a, b, c) in enumerate(tris):
        for e in ((a, b), (b, c), (c, a)):
            by_edge[e] = k

    def locate(p: Point) -> list[int]:
        return [k for k, (a, b, c) in enumerate(tris) if in_closed_triangle(polygon[a], polygon[b], polygon[c], p)]

    starts, ends = locate(s), locate(t)
    if not starts or not ends:
        raise ValueError("s and t must lie in the closed polygon")
    goal = set(ends)
    parent = {k: None for k in starts}  # @line L2
    queue = deque(starts)
    while queue:
        k = queue.popleft()
        if k in goal:
            break
        a, b, c = tris[k]
        for u, v in ((a, b), (b, c), (c, a)):
            m = by_edge.get((v, u))
            if m is not None and m not in parent:
                parent[m] = (k, u, v)
                queue.append(m)
    portals = []
    while parent[k] is not None:  # @line L3
        k, u, v = parent[k]
        portals.append((v, u))  # u -> v is a counterclockwise edge of the earlier triangle: v is on the left
    portals.reverse()
    return portals


def funnel(polygon: list[Point], portals: list[tuple[int, int]], s: Point, t: Point) -> list[Point]:
    """Lee and Preparata's funnel: the shortest path from s to t through a sequence of portals.

    portals are (left, right) index pairs of consecutive diagonals, each sharing one endpoint with
    the next, as returned by sleeve. Each point enters and leaves a chain at most once, so the
    loop takes O(k) time for k portals.
    """
    events: list[tuple[int, Point]] = []  # (side, point), side 0 = left, 1 = right
    prev = None
    for left, right in portals:  # @line L4
        if prev is None:
            events += [(0, polygon[left]), (1, polygon[right])]
        elif left != prev[0]:
            events.append((0, polygon[left]))
        elif right != prev[1]:
            events.append((1, polygon[right]))
        else:
            raise ValueError("two consecutive portals are equal")
        prev = (left, right)
    events.append((1, t))
    path: list[Point] = []
    chains = (deque([s]), deque([s]))  # @line L5
    for side, v in events:  # @line L6
        mine, other = chains[side], chains[1 - side]
        sign = 1 if side == 1 else -1  # mirror the tests for the left chain
        while len(mine) >= 2 and sign * orient(mine[-2], mine[-1], v) >= 0:  # @line L7
            mine.pop()
        if len(mine) == 1:
            while len(other) >= 2 and sign * orient(other[0], other[1], v) > 0:  # @line L8
                path.append(other.popleft())
                mine[0] = other[0]
        mine.append(v)  # @line L9
    right = chains[1]
    out = path + list(right)  # @line L10
    clean = [out[0]]
    for p in out[1:]:
        if p != clean[-1]:
            clean.append(p)
    return clean


def shortest_path(polygon: list[Point], triangles: list[tuple[int, int, int]], s: Point, t: Point) -> list[Point]:
    """Shortest path from s to t inside a triangulated simple polygon, as a list of points.

    polygon is a counterclockwise list of vertices with int or Fraction coordinates, triangles is
    any triangulation of it as triples of vertex indices, and s and t lie in the closed polygon.
    The inner points of the path are reflex vertices of the polygon. Cost: O(n) time and space after
    the triangulation, apart from locating s and t, which this simple version does in O(n) by
    testing every triangle.
    """
    if s == t:
        return [s]
    portals = sleeve(polygon, triangles, s, t)  # @line L1
    return funnel(polygon, portals, s, t)


def path_length(path: list[Point]) -> float:
    return sum(hypot(float(b[0] - a[0]), float(b[1] - a[1])) for a, b in zip(path, path[1:]))
