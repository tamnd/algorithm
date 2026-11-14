# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alternating-sum-of-volumes/. The authors are listed in prov/7SFHP7.jsonl.

"""Alternating sum of volumes (ASV) of a simple polygon in the plane.

The ASV writes a region Q as its convex hull minus the regions between Q
and the hull, its pockets, and treats each pocket the same way:

    Q = CH(Q) -* (ASV(pocket_1) u ... u ASV(pocket_m)),

so that Q = H_0 - H_1 + H_2 - ... as a signed sum of convex hulls, one sign
per depth of the tree. A pocket is the region between a chain of the
boundary of Q and the hull: the chain runs between two consecutive vertices
of Q that lie on the boundary of the hull, and it has at least two edges.
The segment joining its ends, the lid, lies on the boundary of the hull.

Precondition: the polygon is simple, counterclockwise, with integer or
Fraction coordinates, and no three consecutive vertices are collinear.
Cost: a node with s vertices and h hull edges costs O(s log s) for the hull
and O(s h) for the simple touching test used here. The tree has at most
n - 2 levels, and the nodes of one level have O(n) vertices in total, so
the whole tree takes O(n^3) time with this test in the worst case, and
O(n^2 log n) with an O(s log s) touching test. Space is O(n^2). All
arithmetic is exact.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction

Point = tuple


def cross(o: Point, a: Point, b: Point):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points: list[Point]) -> list[Point]:
    """Andrew's monotone chain, counterclockwise, with no collinear vertices."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower: list[Point] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[Point] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def on_segment(a: Point, b: Point, p: Point) -> bool:
    return (cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def on_hull_boundary(hull: list[Point], p: Point) -> bool:
    h = len(hull)
    return any(on_segment(hull[k], hull[(k + 1) % h], p) for k in range(h))


def strictly_inside_convex(hull: list[Point], x, y) -> bool:
    h = len(hull)
    return h >= 3 and all(cross(hull[k], hull[(k + 1) % h], (x, y)) > 0 for k in range(h))


def area2(poly: list[Point]):
    """Twice the signed area."""
    n = len(poly)
    return sum(poly[k][0] * poly[(k + 1) % n][1] - poly[(k + 1) % n][0] * poly[k][1] for k in range(n))


@dataclass
class Node:
    region: list[Point]                 # the polygon this node stands for
    hull: list[Point]                   # its convex hull
    children: list["Node"] = field(default_factory=list)   # its pockets


def asv(poly: list[Point]) -> Node:
    """The ASV tree of a simple counterclockwise polygon."""
    n = len(poly)
    hull = convex_hull(poly)  # @line L1
    touch = [k for k in range(n) if on_hull_boundary(hull, poly[k])]  # @line L2
    node = Node(poly, hull)
    for t in range(len(touch)):
        i, j = touch[t], touch[(t + 1) % len(touch)]  # @line L3
        steps = (j - i) % n or n
        if steps < 2:
            continue  # @line L4
        chain = [poly[(i + s) % n] for s in range(steps + 1)]
        pocket = chain[::-1]  # @line L5
        node.children.append(asv(pocket))  # @line L6
    return node


def contains(node: Node, x, y) -> bool:
    """Membership in CH -* (union of the children), for a point on no edge of
    any hull or region in the tree."""
    if not strictly_inside_convex(node.hull, x, y):
        return False
    return not any(contains(c, x, y) for c in node.children)  # @line L7


def signed_hulls(node: Node, depth: int = 0) -> list[tuple[int, list[Point]]]:
    """The series as (sign, hull) pairs: Q = sum of sign * CH."""
    out = [((-1) ** depth, node.hull)]
    for c in node.children:
        out += signed_hulls(c, depth + 1)
    return out


def depth(node: Node) -> int:
    return 1 + max((depth(c) for c in node.children), default=0)


def series_value(node: Node, x, y) -> int:
    """The signed sum of the indicators of the hulls at (x, y)."""
    return sum(s for s, h in signed_hulls(node) if strictly_inside_convex(h, x, y))


def series_area(node: Node) -> Fraction:
    return sum((s * Fraction(area2(h), 2) for s, h in signed_hulls(node)), Fraction(0))
