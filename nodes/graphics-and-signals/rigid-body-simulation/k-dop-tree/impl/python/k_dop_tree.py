# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-dop-tree/. The authors are listed in prov/ZJ32AH.jsonl.

"""A tree of 8-DOPs over the triangles of a 2D object, and the overlap query of two such trees.

An 8-DOP is the intersection of 4 slabs with the fixed normals (1, 0), (0, 1), (1, 1) and (1, -1).
It is stored as 4 intervals, one per normal. Two 8-DOPs overlap only if all 4 pairs of intervals
overlap. In 2D the edge normals of an 8-DOP are among the 4 normals, so this test is exact. In 3D
the interval test of k/2 pairs is only conservative.

When the object B turns, its stored 8-DOPs are no longer aligned with the fixed normals. As in the
paper of Klosowski and others, the query computes the exact 8-DOP of the moved geometry at the
root of B, and at the other nodes the 8-DOP of the moved corners of the stored 8-DOP, which is
cheaper and looser.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

DIRS = ((1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, -1.0))
EPS = 1e-9  # each interval grows by EPS times the scale, so that rounding cannot remove a contact


def _dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def apply(R, t, p):
    return (R[0][0] * p[0] + R[0][1] * p[1] + t[0], R[1][0] * p[0] + R[1][1] * p[1] + t[1])


def rotation(angle):
    c, s = math.cos(angle), math.sin(angle)
    return ((c, -s), (s, c))


def dop_of_points(points, margin=True):
    """The 8-DOP of the points: the interval of the projections on each of the 4 normals."""
    scale = max(1.0, max(abs(x) for p in points for x in p)) if margin else 0.0
    out = []
    for d in DIRS:
        pr = [_dot(d, p) for p in points]
        out.append((min(pr) - EPS * scale, max(pr) + EPS * scale))
    return tuple(out)


def dop_overlap(P, Q) -> bool:
    """True if all 4 pairs of intervals overlap."""
    return all(p[0] <= q[1] and q[0] <= p[1] for p, q in zip(P, Q))


def _clip(poly, d, c, keep_below):
    """Clip a convex polygon to the half-plane d . x <= c (or >= c)."""
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        fa, fb = _dot(d, a) - c, _dot(d, b) - c
        if not keep_below:
            fa, fb = -fa, -fb
        if fa <= 0:
            out.append(a)
        if (fa < 0 < fb) or (fb < 0 < fa):
            s = fa / (fa - fb)
            out.append((a[0] + s * (b[0] - a[0]), a[1] + s * (b[1] - a[1])))
    return out


def dop_corners(D):
    """The corners of the 8-DOP D as a convex polygon, counterclockwise."""
    (x0, x1), (y0, y1) = D[0], D[1]
    poly = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for k in (2, 3):
        poly = _clip(poly, DIRS[k], D[k][0], keep_below=False)
        poly = _clip(poly, DIRS[k], D[k][1], keep_below=True)
    return poly


def moved_dop(D, R, t):
    """The 8-DOP of the corners of D moved by x -> R x + t: it contains the moved D."""
    return dop_of_points([apply(R, t, c) for c in dop_corners(D)])


def triangles_overlap(T, U) -> bool:
    """Separating axis test on the 6 edge normals: True if the closed triangles meet."""
    for P in (T, U):
        for i in range(3):
            a, b = P[i], P[(i + 1) % 3]
            n = (a[1] - b[1], b[0] - a[0])
            p1 = [_dot(n, x) for x in T]
            p2 = [_dot(n, x) for x in U]
            if max(p1) < min(p2) or max(p2) < min(p1):
                return False
    return True


@dataclass
class Node:
    dop: tuple
    tris: list
    left: "Node | None" = None
    right: "Node | None" = None

    @property
    def leaf(self):
        return self.left is None


def build(tris) -> Node:
    """The 8-DOP tree over the triangles, one triangle per leaf, split at the median."""
    return _build(tris, list(range(len(tris))))


def _build(tris, idx) -> Node:
    node = Node(dop_of_points([p for i in idx for p in tris[i]]), idx)  # @line L1
    if len(idx) == 1:  # @line L2
        return node
    cent = {i: ((tris[i][0][0] + tris[i][1][0] + tris[i][2][0]) / 3, (tris[i][0][1] + tris[i][1][1] + tris[i][2][1]) / 3) for i in idx}

    def spread(d):
        pr = [_dot(d, cent[i]) for i in idx]
        return (max(pr) - min(pr)) / math.hypot(*d)

    d = max(DIRS, key=spread)  # @line L3
    s = sorted(idx, key=lambda i: _dot(d, cent[i]))
    h = len(s) // 2
    node.left, node.right = _build(tris, s[:h]), _build(tris, s[h:])  # @line L4
    return node


def overlap_pairs(A: Node, trisA, B: Node, trisB, R=((1.0, 0.0), (0.0, 1.0)), t=(0.0, 0.0)):
    """The pairs (i, j) such that triangle i of A meets triangle j of B moved by x -> R x + t.

    Returns the set of pairs and the number of 8-DOP tests.
    """
    moved_tris = {j: tuple(apply(R, t, p) for p in T) for j, T in enumerate(trisB)}
    world = {id(B): dop_of_points([p for j in B.tris for p in moved_tris[j]])}  # @line L5

    def dop_of(b):
        if id(b) not in world:
            world[id(b)] = moved_dop(b.dop, R, t)  # @line L6
        return world[id(b)]

    pairs = set()
    tests = 0
    stack = [(A, B)]
    while stack:  # @line L7
        a, b = stack.pop()
        tests += 1
        if not dop_overlap(a.dop, dop_of(b)):  # @line L8
            continue
        if a.leaf and b.leaf:  # @line L9
            i, j = a.tris[0], b.tris[0]
            if triangles_overlap(trisA[i], moved_tris[j]):
                pairs.add((i, j))
        elif b.leaf or (not a.leaf and len(a.tris) >= len(b.tris)):  # @line L10
            stack += [(a.left, b), (a.right, b)]
        else:
            stack += [(a, b.left), (a, b.right)]
    return pairs, tests
