# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lee-preparata-algorithm/. The authors are listed in prov/A26CZG.jsonl.

"""Lee and Preparata's shortest path between two points of a simple polygon.

The polygon is triangulated, the triangles from the one that holds s to the one
that holds t are found in the dual tree (the sleeve), and the funnel of shortest
paths to the two ends of each crossed diagonal is pushed through the sleeve.
All decisions are signs of exact orientation tests, so coordinates should be
int or Fraction. Only path_length uses floating point.
"""

from collections import deque
from fractions import Fraction
from math import hypot
from typing import Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


def orient(a: Point, b: Point, c: Point) -> Number:
    """Twice the signed area of abc: > 0 for a left turn, 0 when collinear."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def in_closed_triangle(a: Point, b: Point, c: Point, p: Point) -> bool:
    """p lies in the closed counterclockwise triangle abc."""
    return orient(a, b, p) >= 0 and orient(b, c, p) >= 0 and orient(c, a, p) >= 0


def triangulate(poly: list[Point]) -> list[tuple[int, int, int]]:
    """Ear clipping for a simple counterclockwise polygon; straight vertices are allowed.

    Returns n - 2 counterclockwise index triples of positive area. The scan is
    O(n^2) per clipped ear in the worst case, which is enough for the tests.
    """
    n = len(poly)
    twice = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    if n < 3 or twice <= 0:
        raise ValueError("need a counterclockwise polygon with at least 3 vertices")
    live = list(range(n))
    tris = []
    while len(live) > 3:
        m = len(live)
        for k in range(m):
            i, j, l = live[k - 1], live[k], live[(k + 1) % m]
            a, b, c = poly[i], poly[j], poly[l]
            if orient(a, b, c) > 0 and not any(
                in_closed_triangle(a, b, c, poly[x]) for x in live if x not in (i, j, l)
            ):
                tris.append((i, j, l))
                del live[k]
                break
        else:
            raise ValueError("no ear: the polygon is not simple")
    i, j, l = live
    if orient(poly[i], poly[j], poly[l]) <= 0:
        raise ValueError("no ear: the polygon is not simple")
    tris.append((i, j, l))
    return tris


def portals_between(poly: list[Point], tris: list[tuple[int, int, int]], s: Point, t: Point) -> list[tuple[int, int]]:
    """The diagonals crossed on the dual tree path from a triangle of s to a triangle of t.

    Each portal is (left, right), as seen when walking from s to t.
    """
    owner = {}
    for k, (a, b, c) in enumerate(tris):  # @line L2
        for e in ((a, b), (b, c), (c, a)):
            owner[e] = k

    def holders(p: Point) -> list[int]:
        return [k for k, (a, b, c) in enumerate(tris) if in_closed_triangle(poly[a], poly[b], poly[c], p)]

    start, goal = holders(s), set(holders(t))  # @line L3
    if not start or not goal:
        raise ValueError("s and t must lie in the closed polygon")
    came = {k: None for k in start}  # @line L4
    queue = deque(start)
    k = None
    while queue:
        k = queue.popleft()
        if k in goal:
            break
        a, b, c = tris[k]
        for u, w in ((a, b), (b, c), (c, a)):
            nxt = owner.get((w, u))
            if nxt is not None and nxt not in came:
                came[nxt] = (k, u, w)
                queue.append(nxt)
    out = []
    while came[k] is not None:  # @line L5
        k, u, w = came[k]
        out.append((w, u))  # u -> w is a counterclockwise edge of the earlier triangle, so w is on the left
    out.reverse()
    return out


def shortest_path(poly: list[Point], s: Point, t: Point, tris: list[tuple[int, int, int]] | None = None) -> list[Point]:
    """The shortest path from s to t in the closed simple polygon poly (counterclockwise).

    Returns s, the reflex vertices where the path bends, and t. tris may give any
    triangulation of poly; by default the polygon is triangulated by ear clipping.
    """
    if s == t:
        return [s]
    if tris is None:
        tris = triangulate(poly)  # @line L1
    else:
        tris = [(a, b, c) if orient(poly[a], poly[b], poly[c]) > 0 else (a, c, b) for a, b, c in tris]
    portals = portals_between(poly, tris, s, t)
    events: list[tuple[int, Point]] = []  # side 0 = left, side 1 = right
    for k, (left, right) in enumerate(portals):  # @line L6
        if k == 0:
            events += [(0, poly[left]), (1, poly[right])]
        elif left != portals[k - 1][0]:
            events.append((0, poly[left]))
        else:
            events.append((1, poly[right]))
    events.append((1, t))
    done: list[Point] = []
    chain = (deque([s]), deque([s]))  # @line L7
    for side, v in events:  # @line L8
        own, other = chain[side], chain[1 - side]
        sg = 1 if side == 1 else -1
        while len(own) >= 2 and sg * orient(own[-2], own[-1], v) >= 0:  # @line L9
            own.pop()
        if len(own) == 1:  # @line L10
            while len(other) >= 2 and sg * orient(other[0], other[1], v) > 0:
                done.append(other.popleft())
                own[0] = other[0]
        own.append(v)  # @line L11
    out = done + list(chain[1])  # @line L12
    path = [out[0]]
    for p in out[1:]:
        if p != path[-1]:
            path.append(p)
    return path


def path_length(path: list[Point]) -> float:
    return sum(hypot(float(b[0] - a[0]), float(b[1] - a[1])) for a, b in zip(path, path[1:]))
