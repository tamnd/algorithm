# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/q-morph/. The authors are listed in prov/D6Y61V.jsonl.

"""The core step of Owen's Q-Morph: turn triangles next to one front edge into a quad.

The input is a conforming triangle mesh, given as counterclockwise index
triples over exact points (int or Fraction), and a front edge a -> b whose left
side is a triangle. The step

1. picks a side edge at a and at b: the existing mesh edge whose direction is
   closest to the ideal direction, here the inward normal of ab;
2. recovers the top edge c d between the far ends of the side edges, by
   flipping triangle edges that cross the segment c d;
3. merges the triangles inside the quad a, b, d, c into one quad.

Every test is exact. The whole of Q-Morph also smooths, swaps or splits edges
to improve the side edges, classifies front edges by the state of their ends,
and closes the front; none of that is here. The step returns None and a reason
when it cannot form a strictly convex quad.
"""

import math
from typing import Dict, List, Optional, Sequence, Tuple

from mg3geom import orient2d, segments_cross

Tri = Tuple[int, int, int]


def directed_owner(tris: Sequence[Tri]) -> Dict[Tuple[int, int], int]:
    m = {}
    for k, (a, b, c) in enumerate(tris):
        for e in ((a, b), (b, c), (c, a)):
            m[e] = k
    return m


def undirected_edges(tris: Sequence[Tri]):
    return {(min(x, y), max(x, y)) for t in tris for x, y in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0]))}


def neighbours(tris: Sequence[Tri], v: int):
    return sorted({w for t in tris if v in t for w in t if w != v})


def angle_between(u, v) -> float:
    return abs(math.atan2(float(u[0] * v[1] - u[1] * v[0]), float(u[0] * v[0] + u[1] * v[1])))


def side_edge(P, tris, a: int, b: int, at: int) -> int:
    """The neighbour w of `at` (not a or b) for which the edge at -> w is closest in
    angle to the inward normal of the front edge a -> b."""
    ideal = (-(P[b][1] - P[a][1]), P[b][0] - P[a][0])
    best = None
    for w in neighbours(tris, at):
        if w in (a, b):
            continue
        d = (P[w][0] - P[at][0], P[w][1] - P[at][1])
        key = (angle_between(ideal, d), w)
        if best is None or key < best:
            best = key
    if best is None:
        raise ValueError("no side edge")
    return best[1]


def flip(P, tris: List[Tri], u: int, v: int) -> Optional[List[Tri]]:
    """Flip the edge uv if its two triangles form a strictly convex quad."""
    own = directed_owner(tris)
    if (u, v) not in own or (v, u) not in own:
        return None
    t1, t2 = own[(u, v)], own[(v, u)]
    k = next(x for x in tris[t1] if x not in (u, v))
    l = next(x for x in tris[t2] if x not in (u, v))
    if orient2d(P[k], P[u], P[l]) <= 0 or orient2d(P[l], P[v], P[k]) <= 0:
        return None
    rest = [t for i, t in enumerate(tris) if i not in (t1, t2)]
    return rest + [(k, u, l), (l, v, k)]


def recover_edge(P, tris: List[Tri], c: int, d: int, cap: int = 1000):
    """Flip edges that cross the open segment cd until cd is an edge.
    Returns (triangles, number of flips) or (None, reason)."""
    for v in range(len(P)):
        if v not in (c, d) and orient2d(P[c], P[d], P[v]) == 0 and \
                min(P[c][0], P[d][0]) <= P[v][0] <= max(P[c][0], P[d][0]) and \
                min(P[c][1], P[d][1]) <= P[v][1] <= max(P[c][1], P[d][1]):
            return None, "a vertex lies on the top edge"
    flips = 0
    while True:
        crossing = [e for e in sorted(undirected_edges(tris)) if segments_cross(P[c], P[d], P[e[0]], P[e[1]])]  # @line L5
        if not crossing:
            break
        if flips >= cap:
            return None, "flip cap reached"
        done = None
        for prefer in (True, False):  # @line L6
            for u, v in crossing:
                new = flip(P, tris, u, v)
                if new is None:
                    continue
                k, l = new[-2][0], new[-2][2]
                if prefer and segments_cross(P[c], P[d], P[k], P[l]):
                    continue
                done = new
                break
            if done is not None:
                break
        if done is None:
            return None, "no crossing edge can be flipped"
        tris = done
        flips += 1
    if (min(c, d), max(c, d)) not in undirected_edges(tris):
        return None, "the top edge is not in the mesh"
    return tris, flips


def triangles_in_quad(tris: Sequence[Tri], a: int, b: int, d: int, c: int) -> List[int]:
    """The triangles reached from the triangle left of a -> b without crossing the
    quad edges ab, bd, dc, ca."""
    own = directed_owner(tris)
    wall = {frozenset(e) for e in ((a, b), (b, d), (d, c), (c, a))}
    start = own[(a, b)]
    seen, stack = {start}, [start]
    while stack:
        t = tris[stack.pop()]
        for x, y in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            if frozenset((x, y)) in wall:
                continue
            u = own.get((y, x))
            if u is not None and u not in seen:
                seen.add(u)
                stack.append(u)
    return sorted(seen)


def qmorph_step(P, tris: List[Tri], a: int, b: int):
    """One Q-Morph quad on the front edge a -> b. Returns
    (quad, remaining triangles, flips) or (None, reason, 0)."""
    if (a, b) not in directed_owner(tris):
        return None, "a -> b is not an edge with a triangle on its left", 0
    c = side_edge(P, tris, a, b, a)  # @line L1
    d = side_edge(P, tris, a, b, b)  # @line L2
    if c == d:  # @line L3
        return None, "both side edges end at the same vertex", 0
    quad = (a, b, d, c)
    if any(orient2d(P[quad[s]], P[quad[(s + 1) % 4]], P[quad[(s + 2) % 4]]) <= 0 for s in range(4)):  # @line L4
        return None, "the quad a, b, d, c is not strictly convex", 0
    tris, flips = recover_edge(P, list(tris), c, d)
    if tris is None:
        return None, flips, 0
    inside = triangles_in_quad(tris, a, b, d, c)  # @line L7
    covered = sum(orient2d(P[t[0]], P[t[1]], P[t[2]]) for t in (tris[i] for i in inside))
    if covered != orient2d(P[a], P[b], P[d]) + orient2d(P[a], P[d], P[c]):  # @line L8
        return None, "the quad covers a hole of the mesh", 0
    rest = [t for i, t in enumerate(tris) if i not in set(inside)]  # @line L9
    return quad, rest, flips  # @line L10
