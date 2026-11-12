# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kd-tree-traversal/. The authors are listed in prov/AK1SG3.jsonl.

"""Front-to-back ray traversal of a spatial kd-tree over triangles, in exact arithmetic.

The tree splits space, not the set of triangles: each node has a cell, an inner node cuts its
cell with an axis-aligned plane into two closed cells, and a triangle is stored in every leaf
whose cell its bounding box overlaps. The traversal visits the leaves that the ray passes
through in the order of t and stops at the first leaf that has a hit inside its own cell.
"""

from dataclasses import dataclass, field
from fractions import Fraction
import math

Num = int | Fraction
Vec = tuple[Num, Num, Num]
Tri = tuple[Vec, Vec, Vec]
Box = tuple[Vec, Vec]


@dataclass
class Node:
    axis: int = -1  # -1 for a leaf
    split: Num = 0
    left: int = -1  # the cell with coordinate <= split on axis
    right: int = -1  # the cell with coordinate >= split on axis
    tris: list[int] = field(default_factory=list)  # the triangles of a leaf


@dataclass
class KdTree:
    nodes: list[Node]
    lo: Vec  # the cell of the root: the scene box
    hi: Vec


def tri_box(t: Tri) -> Box:
    lo = tuple(min(p[a] for p in t) for a in range(3))
    hi = tuple(max(p[a] for p in t) for a in range(3))
    return lo, hi  # type: ignore[return-value]


def build(tris: list[Tri], max_leaf: int = 2, max_depth: int = 16) -> KdTree:
    """A spatial median kd-tree: split each cell at the middle of its longest side.

    A triangle goes to each child whose closed cell its box overlaps on the split axis, so a
    triangle that crosses the plane, or touches it, is in both. A node is a leaf when it has at
    most max_leaf triangles, at depth max_depth, or when both children would get all of them.
    Precondition: tris is not empty. Cost: O(n) per level for the triangles of the level.
    """
    boxes = [tri_box(t) for t in tris]
    lo = tuple(min(b[0][a] for b in boxes) for a in range(3))
    hi = tuple(max(b[1][a] for b in boxes) for a in range(3))
    nodes: list[Node] = []
    stack = [(list(range(len(tris))), list(lo), list(hi), 0, -1, False)]
    while stack:
        part, clo, chi, depth, parent, is_right = stack.pop()
        idx = len(nodes)
        nodes.append(Node(tris=part))
        if parent >= 0:
            if is_right:
                nodes[parent].right = idx
            else:
                nodes[parent].left = idx
        if len(part) <= max_leaf or depth >= max_depth:
            continue
        a = max(range(3), key=lambda k: chi[k] - clo[k])
        if chi[a] == clo[a]:
            continue
        p = Fraction(clo[a] + chi[a], 2)
        if p.denominator == 1:
            p = p.numerator
        left = [r for r in part if boxes[r][0][a] <= p]
        right = [r for r in part if boxes[r][1][a] >= p]
        if len(left) == len(part) and len(right) == len(part):
            continue
        nodes[idx] = Node(axis=a, split=p)
        stack.append((right, clo[:a] + [p] + clo[a + 1 :], chi, depth + 1, idx, True))
        stack.append((left, clo, chi[:a] + [p] + chi[a + 1 :], depth + 1, idx, False))
    return KdTree(nodes, lo, hi)  # type: ignore[arg-type]


def box_interval(lo: Vec, hi: Vec, o: Vec, d: Vec, tmax: Num | float) -> tuple[Num, Num | float] | None:
    """The exact slab method: the t in [0, tmax] with o + t d in the closed box, or None."""
    t0: Num = 0
    t1: Num | float = tmax
    for a in range(3):
        if d[a] == 0:
            if o[a] < lo[a] or o[a] > hi[a]:
                return None
            continue
        ta = Fraction(lo[a] - o[a]) / d[a]
        tb = Fraction(hi[a] - o[a]) / d[a]
        if ta > tb:
            ta, tb = tb, ta
        t0 = max(t0, ta)
        t1 = min(t1, tb)
        if t0 > t1:
            return None
    return t0, t1


def hit_triangle(t: Tri, o: Vec, d: Vec) -> Fraction | None:
    """Exact Moller-Trumbore with integer or Fraction input: the t >= 0 of the hit, or None."""
    a, b, c = t
    e1 = [b[i] - a[i] for i in range(3)]
    e2 = [c[i] - a[i] for i in range(3)]
    p = [d[1] * e2[2] - d[2] * e2[1], d[2] * e2[0] - d[0] * e2[2], d[0] * e2[1] - d[1] * e2[0]]
    det = sum(e1[i] * p[i] for i in range(3))
    if det == 0:
        return None
    s = [o[i] - a[i] for i in range(3)]
    u = sum(s[i] * p[i] for i in range(3))
    q = [s[1] * e1[2] - s[2] * e1[1], s[2] * e1[0] - s[0] * e1[2], s[0] * e1[1] - s[1] * e1[0]]
    v = sum(d[i] * q[i] for i in range(3))
    w = sum(e2[i] * q[i] for i in range(3))
    if det < 0:
        det, u, v, w = -det, -u, -v, -w
    if u < 0 or v < 0 or u + v > det or w < 0:
        return None
    return Fraction(w) / det


def closest_hit(
    tree: KdTree, tris: list[Tri], o: Vec, d: Vec, tmax: Num | float = math.inf, check_cell: bool = True
) -> tuple[Fraction, int] | None:
    """The nearest hit (t, triangle) of o + t d with 0 <= t <= tmax, or None.

    Precondition: d is not the zero vector. check_cell=False drops the test t <= t_far of line
    L12, which is wrong, and is only there to show the pitfall.
    Cost: O(N) per ray in the worst case for a tree with N nodes and leaf entries.
    """
    span = box_interval(tree.lo, tree.hi, o, d, tmax)  # @line L1
    if span is None:
        return None
    stack = [(0, span[0], span[1])]  # @line L2
    while stack:  # @line L3
        i, tn, tf = stack.pop()
        nd = tree.nodes[i]
        while nd.axis >= 0:  # @line L4
            a, p = nd.axis, nd.split
            if o[a] < p or (o[a] == p and d[a] <= 0):  # @line L5
                near, far = nd.left, nd.right
            else:
                near, far = nd.right, nd.left
            if d[a] == 0:  # @line L6
                nd = tree.nodes[near]
                continue
            ts = Fraction(p - o[a]) / d[a]  # @line L7
            if ts > tf or ts <= 0:  # @line L8
                nd = tree.nodes[near]
            elif ts < tn:  # @line L9
                nd = tree.nodes[far]
            else:  # @line L10
                stack.append((far, ts, tf))
                nd = tree.nodes[near]
                tf = ts
        best: tuple[Fraction, int] | None = None  # @line L11
        for r in nd.tris:
            t = hit_triangle(tris[r], o, d)
            if t is not None and t <= tmax and (best is None or t < best[0]):
                best = (t, r)
        if best is not None and (best[0] <= tf or not check_cell):  # @line L12
            return best
    return None  # @line L13


def any_hit(tree: KdTree, tris: list[Tri], o: Vec, d: Vec, tmax: Num | float) -> bool:
    """True if o + t d meets a triangle with 0 <= t <= tmax: the same walk, stopping at any such hit."""
    span = box_interval(tree.lo, tree.hi, o, d, tmax)
    if span is None:
        return False
    stack = [(0, span[0], span[1])]
    while stack:
        i, tn, tf = stack.pop()
        nd = tree.nodes[i]
        while nd.axis >= 0:
            a, p = nd.axis, nd.split
            if o[a] < p or (o[a] == p and d[a] <= 0):
                near, far = nd.left, nd.right
            else:
                near, far = nd.right, nd.left
            if d[a] == 0:
                nd = tree.nodes[near]
                continue
            ts = Fraction(p - o[a]) / d[a]
            if ts > tf or ts <= 0:
                nd = tree.nodes[near]
            elif ts < tn:
                nd = tree.nodes[far]
            else:
                stack.append((far, ts, tf))
                nd = tree.nodes[near]
                tf = ts
        for r in nd.tris:
            t = hit_triangle(tris[r], o, d)
            if t is not None and t <= tmax:
                return True
    return False


def leaf_cells(tree: KdTree) -> list[tuple[int, Box]]:
    """Each leaf with its cell. Cost: O(number of nodes)."""
    out = []
    stack = [(0, list(tree.lo), list(tree.hi))]
    while stack:
        i, lo, hi = stack.pop()
        nd = tree.nodes[i]
        if nd.axis < 0:
            out.append((i, (tuple(lo), tuple(hi))))
        else:
            a = nd.axis
            stack.append((nd.left, lo, hi[:a] + [nd.split] + hi[a + 1 :]))
            stack.append((nd.right, lo[:a] + [nd.split] + lo[a + 1 :], hi))
    return out  # type: ignore[return-value]


def visited_leaves(tree: KdTree, o: Vec, d: Vec) -> list[tuple[int, Num, Num | float]]:
    """The leaves of the walk without the early stop, with their intervals, in the order of the walk."""
    span = box_interval(tree.lo, tree.hi, o, d, math.inf)
    if span is None:
        return []
    out = []
    stack = [(0, span[0], span[1])]
    while stack:
        i, tn, tf = stack.pop()
        while tree.nodes[i].axis >= 0:
            nd = tree.nodes[i]
            a, p = nd.axis, nd.split
            if o[a] < p or (o[a] == p and d[a] <= 0):
                near, far = nd.left, nd.right
            else:
                near, far = nd.right, nd.left
            if d[a] == 0:
                i = near
                continue
            ts = Fraction(p - o[a]) / d[a]
            if ts > tf or ts <= 0:
                i = near
            elif ts < tn:
                i = far
            else:
                stack.append((far, ts, tf))
                i, tf = near, ts
        out.append((i, tn, tf))
    return out
