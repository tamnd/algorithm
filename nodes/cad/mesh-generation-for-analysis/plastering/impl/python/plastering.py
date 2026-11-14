# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plastering/. The authors are listed in prov/ZETKKR.jsonl.

"""One layer of plastering on a convex axis-aligned box.

The front is a closed quad mesh, each quad listed counterclockwise seen from
outside the solid. Each front vertex v gets an inward offset: v' = v - h n_v,
where n_v is the sum of the outward unit normals of the box faces that contain
v. One hex joins each front quad (a, b, c, d) to its offset quad
(a', b', c', d'), and the offset quads are the new front. This is the core step
of plastering, without seams, wedges or the closure of the last void.
With int or Fraction input every value and sign is exact.
"""

from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

from mg4geom import corners_positive, det3, sub

Point = Tuple


def box_front(xs: Sequence, ys: Sequence, zs: Sequence):
    """The boundary quad mesh of the grid box with the given strictly increasing breakpoints.

    Returns (points, quads). Every quad is counterclockwise seen from outside.
    """
    grids = (list(xs), list(ys), list(zs))
    ids: Dict[Point, int] = {}
    quads = []
    for axis in range(3):
        a1, a2 = [t for t in range(3) if t != axis]
        for side, sign in ((0, -1), (-1, 1)):
            normal = tuple(sign if t == axis else 0 for t in range(3))
            g1, g2 = grids[a1], grids[a2]
            for i in range(len(g1) - 1):
                for j in range(len(g2) - 1):
                    q = []
                    for di, dj in ((0, 0), (1, 0), (1, 1), (0, 1)):
                        p = [0, 0, 0]
                        p[axis] = grids[axis][side]
                        p[a1], p[a2] = g1[i + di], g2[j + dj]
                        q.append(tuple(Fraction(c) for c in p))
                    if det3(sub(q[1], q[0]), sub(q[3], q[0]), normal) < 0:
                        q = [q[0], q[3], q[2], q[1]]
                    quads.append(tuple(ids.setdefault(p, len(ids)) for p in q))
    points = sorted(ids, key=ids.get)
    return points, quads


def box_normals(points: Sequence[Point], low: Sequence, high: Sequence) -> List[Point]:
    """For each point, the sum of the outward unit normals of the box faces that contain it."""
    out = []
    for p in points:
        out.append(tuple((1 if p[t] == high[t] else 0) - (1 if p[t] == low[t] else 0) for t in range(3)))
    return out


def plaster_layer(points: Sequence[Point], quads: Sequence[Tuple[int, int, int, int]], normals: Sequence[Point], h):
    """Advance the front by one layer of hexes of thickness h.

    Returns (new_points, hexes, ok): new_points[v] is the offset of points[v], the new
    front has the same quads with the new points, hexes[i] joins the offset of
    quads[i] (bottom) to quads[i] (top), and ok tells whether every hex has 8
    positive corner Jacobians. Cost: O(V + Q) for V vertices and Q quads.
    """
    new_points = []
    for v, p in enumerate(points):  # @line L1
        n = normals[v]  # @line L2
        new_points.append(tuple(p[t] - h * n[t] for t in range(3)))  # @line L3
    hexes = []  # @line L4
    for a, b, c, d in quads:  # @line L5
        hexes.append([new_points[a], new_points[b], new_points[c], new_points[d], points[a], points[b], points[c], points[d]])  # @line L6
    ok = all(corners_positive(hx) for hx in hexes)  # @line L7
    return new_points, hexes, ok  # @line L8


def safe_thickness(xs: Sequence, ys: Sequence, zs: Sequence):
    """g = the least of the first spacing, the last spacing and half the length, over the three axes."""
    g = None
    for grid in (xs, ys, zs):
        cands = [Fraction(grid[1] - grid[0]), Fraction(grid[-1] - grid[-2]), Fraction(grid[-1] - grid[0], 2)]
        m = min(cands)
        g = m if g is None else min(g, m)
    return g
