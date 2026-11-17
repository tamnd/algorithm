# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sphere-tree/. The authors are listed in prov/0FMTPB.jsonl.

"""A tree of circles over the triangles of a 2D object, with a breadth-first overlap query that can stop at a level.

Each node stores the smallest circle that holds the vertices of the triangles below it, found
by Welzl's randomized algorithm with a fixed seed. A circle does not change when the object
turns, so the query moves only the centers. The query goes down both trees one level at a time.
If it stops at a level limit, it returns the exact pairs found so far and the pairs of nodes
whose circles still overlap, which cover every contact that it has not yet resolved. This is
the interruptible query of Hubbard. Hubbard built the circles from the medial axis; this code
builds them top down, which is simpler and gives a valid tree.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

EPS = 1e-9  # each radius grows by EPS times the scale, so that rounding cannot remove a contact


def apply(R, t, p):
    return (R[0][0] * p[0] + R[0][1] * p[1] + t[0], R[1][0] * p[0] + R[1][1] * p[1] + t[1])


def rotation(angle):
    c, s = math.cos(angle), math.sin(angle)
    return ((c, -s), (s, c))


def _circle2(a, b):
    c = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    return c, math.dist(a, c)


def _circle3(a, b, c):
    bx, by = b[0] - a[0], b[1] - a[1]
    cx, cy = c[0] - a[0], c[1] - a[1]
    d = 2 * (bx * cy - by * cx)
    if d == 0:  # collinear: the circle on the farthest pair
        return max((_circle2(p, q) for p, q in ((a, b), (a, c), (b, c))), key=lambda x: x[1])
    ux = (cy * (bx * bx + by * by) - by * (cx * cx + cy * cy)) / d
    uy = (bx * (cx * cx + cy * cy) - cx * (bx * bx + by * by)) / d
    o = (a[0] + ux, a[1] + uy)
    return o, max(math.dist(o, a), math.dist(o, b), math.dist(o, c))


def _inside(circle, p):
    c, r = circle
    return math.dist(c, p) <= r * (1 + 1e-12) + 1e-12


def min_enclosing_circle(points, seed=0):
    """The smallest circle that holds the points: Welzl's algorithm, written as three loops."""
    P = list(points)
    random.Random(seed).shuffle(P)
    circle = (P[0], 0.0)
    for i in range(1, len(P)):
        if _inside(circle, P[i]):
            continue
        circle = (P[i], 0.0)
        for j in range(i):
            if _inside(circle, P[j]):
                continue
            circle = _circle2(P[i], P[j])
            for k in range(j):
                if not _inside(circle, P[k]):
                    circle = _circle3(P[i], P[j], P[k])
    return circle


def triangles_overlap(T, U) -> bool:
    """Separating axis test on the 6 edge normals: True if the closed triangles meet."""
    for P in (T, U):
        for i in range(3):
            a, b = P[i], P[(i + 1) % 3]
            n = (a[1] - b[1], b[0] - a[0])
            p1 = [n[0] * x[0] + n[1] * x[1] for x in T]
            p2 = [n[0] * x[0] + n[1] * x[1] for x in U]
            if max(p1) < min(p2) or max(p2) < min(p1):
                return False
    return True


@dataclass
class Node:
    center: tuple
    radius: float
    tris: list
    left: "Node | None" = None
    right: "Node | None" = None

    @property
    def leaf(self):
        return self.left is None


def build(tris) -> Node:
    """The sphere tree over the triangles, one triangle per leaf, split at the median."""
    return _build(tris, list(range(len(tris))))


def _build(tris, idx) -> Node:
    pts = [p for i in idx for p in tris[i]]
    c, r = min_enclosing_circle(pts)  # @line L1
    scale = max(1.0, max(abs(x) for p in pts for x in p))
    node = Node(c, r + EPS * scale, idx)
    if len(idx) == 1:  # @line L2
        return node
    cent = {i: (sum(p[0] for p in tris[i]) / 3, sum(p[1] for p in tris[i]) / 3) for i in idx}
    spread = [max(cent[i][a] for i in idx) - min(cent[i][a] for i in idx) for a in (0, 1)]
    axis = 0 if spread[0] >= spread[1] else 1  # @line L3
    s = sorted(idx, key=lambda i: cent[i][axis])
    h = len(s) // 2
    node.left, node.right = _build(tris, s[:h]), _build(tris, s[h:])  # @line L4
    return node


def overlap_pairs(A: Node, trisA, B: Node, trisB, R=((1.0, 0.0), (0.0, 1.0)), t=(0.0, 0.0), max_level=None):
    """Breadth-first overlap query of A and of B moved by x -> R x + t.

    Returns (pairs, possible, tests): the pairs (i, j) of triangles that meet and were resolved,
    the pairs of nodes whose circles overlap at the level limit, and the number of circle tests.
    With max_level=None the query runs to the leaves and possible is empty.
    """
    moved = {}

    def center(b):
        if id(b) not in moved:
            moved[id(b)] = apply(R, t, b.center)  # @line L5
        return moved[id(b)]

    pairs, possible, tests = set(), [], 0
    level, frontier = 0, [(A, B)]
    while frontier:  # @line L6
        nxt = []
        for a, b in frontier:
            tests += 1
            if math.dist(a.center, center(b)) > a.radius + b.radius:  # @line L7
                continue
            if a.leaf and b.leaf:  # @line L8
                i, j = a.tris[0], b.tris[0]
                if triangles_overlap(trisA[i], tuple(apply(R, t, p) for p in trisB[j])):
                    pairs.add((i, j))
            elif max_level is not None and level == max_level:  # @line L9
                possible.append((a, b))
            elif b.leaf or (not a.leaf and a.radius >= b.radius):  # @line L10
                nxt += [(a.left, b), (a.right, b)]
            else:
                nxt += [(a, b.left), (a, b.right)]
        frontier, level = nxt, level + 1
    return pairs, possible, tests
