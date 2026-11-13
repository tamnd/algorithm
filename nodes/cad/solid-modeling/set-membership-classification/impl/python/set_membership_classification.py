# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/set-membership-classification/. The authors are listed in prov/E1CR69.jsonl.

"""Tilove's set membership classification in the plane, with exact neighborhoods.

A solid is a CSG tree. A leaf is a convex polygon, given by its vertices in
counterclockwise order. An inner node is a tuple (op, left, right) with op in
"union", "intersection" and "difference"; the operations are the regularized
ones. Coordinates are int or Fraction, and every test is exact.

A neighborhood of a point p is a pair (dirs, labels). dirs is a list of
directions sorted by angle, and labels[i] tells whether the open sector from
dirs[i] counterclockwise to dirs[i + 1] lies inside the solid near p. With no
directions, labels has one entry for the whole disk around p.
"""

from fractions import Fraction
from functools import cmp_to_key
from typing import Sequence, Union

Num = Union[int, Fraction]
Vec = tuple[Num, Num]
Polygon = Sequence[Vec]
Tree = Union[Polygon, tuple]
Neighborhood = tuple[list[Vec], list[bool]]

IN, ON, OUT = "in", "on", "out"
OPS = {
    "union": lambda a, b: a or b,
    "intersection": lambda a, b: a and b,
    "difference": lambda a, b: a and not b,
}


def cross(u: Vec, v: Vec) -> Num:
    return u[0] * v[1] - u[1] * v[0]


def _upper(d: Vec) -> bool:
    return d[1] > 0 or (d[1] == 0 and d[0] > 0)


def _angle_cmp(u: Vec, v: Vec) -> int:
    hu, hv = _upper(u), _upper(v)
    if hu != hv:
        return -1 if hu else 1
    c = cross(u, v)
    return -1 if c > 0 else (1 if c < 0 else 0)


def _same_dir(u: Vec, v: Vec) -> bool:
    return cross(u, v) == 0 and u[0] * v[0] + u[1] * v[1] > 0


def sector_sample(u: Vec, v: Vec) -> Vec:
    """A direction strictly inside the open sector from u counterclockwise to v."""
    c = cross(u, v)
    if _same_dir(u, v):
        return (-u[0], -u[1])  # the sector is the full turn minus one ray
    if c > 0:
        return (u[0] + v[0], u[1] + v[1])
    if c == 0:
        return (-u[1], u[0])  # a half turn: rotate u by a quarter turn
    return (-(u[0] + v[0]), -(u[1] + v[1]))


def contains(nb: Neighborhood, d: Vec) -> bool:
    """Is the direction d, which is not a breakpoint, in an inside sector?"""
    dirs, labels = nb
    if not dirs:
        return labels[0]
    k = len(dirs)
    if k == 1:
        return labels[0]
    for i in range(k):
        u, v = dirs[i], dirs[(i + 1) % k]
        cu, cv, cuv = cross(u, d), cross(d, v), cross(u, v)
        inside = (cu > 0 and cv > 0) if cuv > 0 else (cu > 0 or cv > 0) if cuv < 0 else cu > 0
        if inside:
            return labels[i]
    raise ValueError("direction is a breakpoint")


def _simplify(dirs: list[Vec], labels: list[bool]) -> Neighborhood:
    """Remove the breakpoints that have the same label on both sides."""
    if len(set(labels)) <= 1:
        return [], [labels[0] if labels else False]
    k = len(dirs)
    keep = [i for i in range(k) if labels[i - 1] != labels[i]]
    return [dirs[i] for i in keep], [labels[i] for i in keep]


def leaf_neighborhood(p: Vec, poly: Polygon) -> Neighborhood:
    """The neighborhood of p in a convex polygon given counterclockwise."""
    k = len(poly)
    tight: list[Vec] = []
    for i in range(k):
        a, b = poly[i], poly[(i + 1) % k]
        e = (b[0] - a[0], b[1] - a[1])
        s = cross(e, (p[0] - a[0], p[1] - a[1]))
        if s < 0:
            return [], [False]  # strictly outside one edge line
        if s == 0:
            tight.append(e)
    if not tight:
        return [], [True]  # strictly inside
    dirs: list[Vec] = []
    for e in tight:
        for d in (e, (-e[0], -e[1])):
            if not any(_same_dir(d, x) for x in dirs):
                dirs.append(d)
    dirs.sort(key=cmp_to_key(_angle_cmp))
    labels = []
    for i in range(len(dirs)):
        w = sector_sample(dirs[i], dirs[(i + 1) % len(dirs)])
        labels.append(all(cross(e, w) > 0 for e in tight))
    return _simplify(dirs, labels)


def combine(n1: Neighborhood, n2: Neighborhood, op: str) -> Neighborhood:
    """The neighborhood in (A op B) from the neighborhoods in A and B."""
    f = OPS[op]
    dirs: list[Vec] = []
    for d in n1[0] + n2[0]:  # @line L5
        if not any(_same_dir(d, x) for x in dirs):
            dirs.append(d)
    dirs.sort(key=cmp_to_key(_angle_cmp))
    if not dirs:
        return [], [f(n1[1][0], n2[1][0])]
    labels = []
    for i in range(len(dirs)):  # @line L6
        w = sector_sample(dirs[i], dirs[(i + 1) % len(dirs)])  # @line L7
        labels.append(f(contains(n1, w), contains(n2, w)))  # @line L8
    return _simplify(dirs, labels)  # @line L9


def classify_neighborhood(p: Vec, tree: Tree) -> Neighborhood:
    """The neighborhood of p in the solid of the tree. Cost: O(size of the tree times the breakpoints)."""
    if not (isinstance(tree, tuple) and tree and isinstance(tree[0], str)):  # @line L1
        return leaf_neighborhood(p, tree)  # @line L2
    op, left, right = tree
    nl, nr = classify_neighborhood(p, left), classify_neighborhood(p, right)  # @line L3
    return combine(nl, nr, op)  # @line L4


def classify_point(p: Vec, tree: Tree) -> str:
    """Point membership classification: IN, ON or OUT of the regularized solid."""
    dirs, labels = classify_neighborhood(p, tree)  # @line L10
    if all(labels):  # @line L11
        return IN
    if not any(labels):  # @line L12
        return OUT
    return ON  # @line L13


def _leaves(tree: Tree) -> list[Polygon]:
    if isinstance(tree, tuple) and tree and isinstance(tree[0], str):
        return _leaves(tree[1]) + _leaves(tree[2])
    return [tree]


Pieces = list[tuple[Fraction, Fraction, str]]


def classify_segment(a: Vec, b: Vec, tree: Tree) -> Pieces:
    """Classify the segment from a to b (a != b) against the solid.

    The segment is split at the crossings with the edge lines of all leaves.
    On each open piece every leaf neighborhood is constant, so one point of the
    piece gives its class. Returns pieces (t0, t1, class) in the parameter t of
    a + t (b - a), in order: a piece with t0 == t1 is a single point, the
    others are open intervals. Points with the same class as both neighbors
    are merged away. Cost: O(m) point classifications for m edges in all.
    """
    ts = {Fraction(0), Fraction(1)}
    d = (b[0] - a[0], b[1] - a[1])
    for poly in _leaves(tree):  # the breakpoints of each leaf: crossings with its edge lines
        k = len(poly)
        for i in range(k):
            u, v = poly[i], poly[(i + 1) % k]
            e = (v[0] - u[0], v[1] - u[1])
            den = cross(e, d)
            if den != 0:
                t = Fraction(cross(e, (u[0] - a[0], u[1] - a[1])), den)
                if 0 < t < 1:
                    ts.add(t)
    ts_sorted = sorted(ts)
    point_at = lambda t: (a[0] + t * d[0], a[1] + t * d[1])
    points = [(t, t, classify_point(point_at(t), tree)) for t in ts_sorted]
    opens = [(t0, t1, classify_point(point_at((t0 + t1) / 2), tree))
             for t0, t1 in zip(ts_sorted, ts_sorted[1:])]
    out: Pieces = [points[0]]
    cur = opens[0]
    for pt, nxt in zip(points[1:-1], opens[1:]):
        if cur[2] == pt[2] == nxt[2]:
            cur = (cur[0], nxt[1], cur[2])  # drop the point and join the two intervals
        else:
            out.extend([cur, pt])
            cur = nxt
    out.extend([cur, points[-1]])
    return out


def segment_class_at(pieces: Pieces, t: Fraction) -> str:
    """The class of the point with parameter t, read from the output of classify_segment."""
    for t0, t1, c in pieces:
        if t0 == t1 == t or t0 < t < t1:
            return c
    raise ValueError("t is outside [0, 1]")
