# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/portal-culling/. The authors are listed in prov/52EA3Z.jsonl.

"""Cell-and-portal culling in the plane, with exact view cones.

The scene is a set of convex cells. A portal is a segment of the boundary of
a cell through which the next cell can be seen; the rest of the boundary is
wall. For each cell, its portals are listed as (p, q, neighbour) with p -> q
counterclockwise around the cell, so the cell is on the left of p -> q.

A cone with apex E is a pair (a, b) of nonzero vectors with cross(a, b) > 0;
it holds the directions d with cross(a, d) >= 0 and cross(d, b) >= 0, which
is the angle from a counterclockwise to b, less than 180 degrees. The search
walks from the cell of the eye through the portals and narrows the cone at
each portal. With int or Fraction input every test is exact.
"""

from typing import Hashable, Optional, Sequence

Cone = tuple  # (a, b), two 2D vectors


def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def inside(cone: Cone, d) -> bool:
    a, b = cone
    return cross(a, d) >= 0 and cross(d, b) >= 0


def meet(k1: Cone, k2: Cone) -> Optional[Cone]:
    """The intersection of two cones, or None if it has no interior."""
    cands = [v for v in (k1[0], k1[1], k2[0], k2[1]) if inside(k1, v) and inside(k2, v)]
    if not cands:
        return None
    start = next(c for c in cands if all(cross(c, d) >= 0 for d in cands))
    end = next(c for c in cands if all(cross(d, c) >= 0 for d in cands))
    if cross(start, end) <= 0:  # empty, or a single ray
        return None
    return start, end


def portal_cull(portals: dict, start: Hashable, eye: Sequence, view: Cone):
    """Return (visible, visits): the set of cells reached, and each (cell, cone) pushed.

    `portals[c]` lists the portals (p, q, c2) of cell c. `start` is the cell that
    holds `eye` in its interior, and `view` is the view cone.
    """
    ex, ey = eye
    visible = {start}  # @line L1
    visits = [(start, view)]
    stack = [(start, view)]
    while stack:  # @line L2
        c, cone = stack.pop()  # @line L3
        for p, q, c2 in portals.get(c, ()):  # @line L4
            a, b = (p[0] - ex, p[1] - ey), (q[0] - ex, q[1] - ey)
            if cross(a, b) <= 0:  # @line L5
                continue  # the eye is not strictly on the side of c: the portal faces away
            narrowed = meet(cone, (a, b))  # @line L6
            if narrowed is None:  # @line L7
                continue
            visible.add(c2)  # @line L8
            visits.append((c2, narrowed))
            stack.append((c2, narrowed))
    return visible, visits  # @line L9


def grid_portals(width: int, height: int, doors) -> dict:
    """Portals of a grid of unit square cells (x, y); `doors` is a set of open edges.

    An edge is ('v', x, y), the segment from (x, y) to (x, y + 1) between the
    cells (x - 1, y) and (x, y), or ('h', x, y), the segment from (x, y) to
    (x + 1, y) between the cells (x, y - 1) and (x, y).
    """
    out: dict = {}
    for x in range(width):
        for y in range(height):
            sides = [
                (('h', x, y), (x, y), (x + 1, y), (x, y - 1)),
                (('v', x + 1, y), (x + 1, y), (x + 1, y + 1), (x + 1, y)),
                (('h', x, y + 1), (x + 1, y + 1), (x, y + 1), (x, y + 1)),
                (('v', x, y), (x, y + 1), (x, y), (x - 1, y)),
            ]
            out[(x, y)] = [(p, q, n) for e, p, q, n in sides if e in doors
                           and 0 <= n[0] < width and 0 <= n[1] < height]
    return out
