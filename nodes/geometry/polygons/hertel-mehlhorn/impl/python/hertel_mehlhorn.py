# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hertel-mehlhorn/. The authors are listed in prov/F65KA1.jsonl.

from fractions import Fraction
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
    counterclockwise triple of vertex indices with positive area. This is the starting
    triangulation for hertel_mehlhorn; any other triangulation works as well.
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


def hertel_mehlhorn(polygon: list[Point], triangles: list[tuple[int, int, int]]) -> list[list[int]]:
    """Convex partition of a simple polygon by deleting inessential diagonals of a triangulation.

    polygon is a list of vertices in counterclockwise order with int or Fraction coordinates, and
    triangles is any triangulation of it, as triples of vertex indices with positive area. The
    result is a list of convex pieces, each a counterclockwise list of vertex indices starting at
    its smallest index, sorted. Every diagonal that remains is essential: deleting it would make an
    angle greater than pi. There are at most 2r + 1 pieces for r reflex vertices, which is less than
    4 times the fewest possible with diagonals. Cost: O(n) time and space.
    """
    nxt: dict[tuple[int, int], tuple[int, int]] = {}
    prv: dict[tuple[int, int], tuple[int, int]] = {}
    order = []
    for t in triangles:  # @line L1
        a, b, c = t
        if orient(polygon[a], polygon[b], polygon[c]) < 0:
            a, b, c = a, c, b
        if orient(polygon[a], polygon[b], polygon[c]) == 0:
            raise ValueError("a triangle has zero area")
        hs = [(a, b), (b, c), (c, a)]
        for k in range(3):
            if hs[k] in nxt:
                raise ValueError("two triangles share a directed edge: not a triangulation")
            nxt[hs[k]] = hs[(k + 1) % 3]
            prv[hs[k]] = hs[k - 1]
            order.append(hs[k])
    for h in order:  # @line L2
        u, v = h
        t = (v, u)
        if t not in nxt or u > v or h not in nxt:
            continue  # a polygon edge, or the other copy of a diagonal, or already deleted
        at_u = orient(polygon[prv[h][0]], polygon[u], polygon[nxt[t][1]])  # @line L3
        at_v = orient(polygon[prv[t][0]], polygon[v], polygon[nxt[h][1]])  # @line L4
        if at_u >= 0 and at_v >= 0:  # @line L5
            ph, nh, pt, nt = prv[h], nxt[h], prv[t], nxt[t]  # @line L6
            nxt[ph], prv[nt] = nt, ph
            nxt[pt], prv[nh] = nh, pt
            for e in (h, t):
                del nxt[e]
                del prv[e]
    pieces = []
    seen = set()
    for h in nxt:  # @line L7
        if h in seen:
            continue
        face = []
        e = h
        while e not in seen:
            seen.add(e)
            face.append(e[0])
            e = nxt[e]
        k = face.index(min(face))
        pieces.append(face[k:] + face[:k])
    pieces.sort()
    return pieces


def convex_partition(polygon: list[Point]) -> list[list[int]]:
    """Ear clipping followed by Hertel-Mehlhorn."""
    return hertel_mehlhorn(polygon, ear_clipping(polygon))
