# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounding-interval-hierarchy/. The authors are listed in prov/P0KNZR.jsonl.

"""Bounding interval hierarchy (Waechter and Keller 2006) over triangles, in exact arithmetic.

An inner node stores one axis and two clip planes: the largest coordinate of the objects of the
left child on that axis, and the least coordinate of the objects of the right child. The box
of a node is not stored; it is the scene box cut by the clip planes on the path from the root.
The split planes come from halving a candidate box that starts as the scene box, and each object
goes to the side of the plane that holds the center of its bounding box.
"""

from dataclasses import dataclass
from fractions import Fraction
import math

Num = int | Fraction
Vec = tuple[Num, Num, Num]
Tri = tuple[Vec, Vec, Vec]
Box = tuple[Vec, Vec]


@dataclass
class Node:
    axis: int = -1  # -1 for a leaf
    lclip: Num = 0  # the largest coordinate on axis of the objects in the left child
    rclip: Num = 0  # the least coordinate on axis of the objects in the right child
    left: int = -1
    right: int = -1
    first: int = 0  # a leaf holds refs[first : first + count]
    count: int = 0


@dataclass
class BIH:
    nodes: list[Node]
    refs: list[int]
    lo: Vec  # the scene box
    hi: Vec


def tri_box(t: Tri) -> Box:
    lo = tuple(min(p[a] for p in t) for a in range(3))
    hi = tuple(max(p[a] for p in t) for a in range(3))
    return lo, hi  # type: ignore[return-value]


def build(tris: list[Tri], max_leaf: int = 1) -> BIH:
    """Build a BIH with global candidate planes. Precondition: tris is not empty, max_leaf >= 1.

    Cost: O(count) per candidate plane at a node, so O(n h) in total, where h is the depth
    counted with the halvings that leave one side empty; O(n log n) for well spread input.
    O(n) space: each triangle is in one leaf and the tree has at most 2n - 1 nodes.
    """
    n = len(tris)
    boxes = [tri_box(t) for t in tris]
    cen2 = [tuple(boxes[r][0][a] + boxes[r][1][a] for a in range(3)) for r in range(n)]  # 2 times the box center
    slo = tuple(min(b[0][a] for b in boxes) for a in range(3))
    shi = tuple(max(b[1][a] for b in boxes) for a in range(3))
    refs = list(range(n))  # @line L1
    nodes: list[Node] = []
    stack: list[tuple[int, int, list[Num], list[Num], int, bool]] = [(0, n, list(slo), list(shi), -1, False)]
    while stack:  # @line L2
        first, count, vlo, vhi, parent, is_right = stack.pop()
        idx = len(nodes)
        nodes.append(Node(first=first, count=count))
        if parent >= 0:
            if is_right:
                nodes[parent].right = idx
            else:
                nodes[parent].left = idx
        part = refs[first : first + count]
        if count <= max_leaf or all(cen2[r] == cen2[part[0]] for r in part):  # @line L3
            continue
        while True:
            a = max(range(3), key=lambda k: vhi[k] - vlo[k])  # @line L4
            p2 = vlo[a] + vhi[a]  # 2 times the middle of the candidate box
            left = [r for r in part if cen2[r][a] < p2]  # @line L5
            right = [r for r in part if cen2[r][a] >= p2]
            if left and right:
                break
            if left:  # @line L6
                vhi = vhi[:a] + [Fraction(p2, 2)] + vhi[a + 1 :]
            else:
                vlo = vlo[:a] + [Fraction(p2, 2)] + vlo[a + 1 :]
        node = nodes[idx]
        node.axis, node.count = a, 0
        node.lclip = max(boxes[r][1][a] for r in left)  # @line L7
        node.rclip = min(boxes[r][0][a] for r in right)
        refs[first : first + count] = left + right
        mid = Fraction(p2, 2)
        stack.append((first + len(left), len(right), vlo[:a] + [mid] + vlo[a + 1 :], vhi, idx, True))  # @line L8
        stack.append((first, len(left), vlo, vhi[:a] + [mid] + vhi[a + 1 :], idx, False))
    return BIH(nodes, refs, slo, shi)  # type: ignore[arg-type]


def clip(o: Vec, d: Vec, a: int, bound: Num, below: bool, tn: Num, tf: Num | float) -> tuple[Num, Num | float] | None:
    """[tn, tf] cut to the t with o[a] + t d[a] <= bound (below) or >= bound; None if empty."""
    if d[a] == 0:
        inside = o[a] <= bound if below else o[a] >= bound
        return (tn, tf) if inside else None
    t = Fraction(bound - o[a]) / d[a]
    if (d[a] > 0) == below:  # the half-space is t <= that value
        tf = min(tf, t)
    else:
        tn = max(tn, t)
    return (tn, tf) if tn <= tf else None


def scene_interval(bih: BIH, o: Vec, d: Vec, tmax: Num | float) -> tuple[Num, Num | float] | None:
    """The ray against the scene box on [0, tmax]: the exact slab method."""
    tn: Num = 0
    tf: Num | float = tmax
    for a in range(3):
        for bound, below in ((bih.hi[a], True), (bih.lo[a], False)):
            r = clip(o, d, a, bound, below, tn, tf)
            if r is None:
                return None
            tn, tf = r
    return tn, tf


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


def closest_hit(bih: BIH, tris: list[Tri], o: Vec, d: Vec) -> tuple[Fraction, int] | None:
    """The nearest hit (t, triangle) of o + t d, t >= 0, or None.

    The children of a node can overlap, so the walk does not stop at the first leaf with a hit;
    it skips a node whose interval starts after the best hit. Cost: O(n) per ray in the worst case.
    """
    best: tuple[Fraction, int] | None = None
    start = scene_interval(bih, o, d, math.inf)  # @line L9
    if start is None:
        return None
    stack = [(0, start[0], start[1])]  # @line L10
    while stack:
        i, tn, tf = stack.pop()  # @line L11
        if best is not None:
            if tn > best[0]:
                continue
            tf = min(tf, best[0])
        nd = bih.nodes[i]
        if nd.axis < 0:  # @line L12
            for r in bih.refs[nd.first : nd.first + nd.count]:
                t = hit_triangle(tris[r], o, d)
                if t is not None and (best is None or t < best[0]):
                    best = (t, r)
            continue
        a = nd.axis
        near_left = d[a] >= 0
        li = clip(o, d, a, nd.lclip, True, tn, tf)  # @line L13
        ri = clip(o, d, a, nd.rclip, False, tn, tf)
        near, far = ((nd.left, li), (nd.right, ri)) if near_left else ((nd.right, ri), (nd.left, li))
        if far[1] is not None:  # @line L14
            stack.append((far[0], far[1][0], far[1][1]))
        if near[1] is not None:
            stack.append((near[0], near[1][0], near[1][1]))
    return best  # @line L15


def any_hit(bih: BIH, tris: list[Tri], o: Vec, d: Vec, tmax: Num | float) -> bool:
    """True if o + t d meets a triangle with 0 <= t <= tmax. Cost: O(n) per ray in the worst case."""
    start = scene_interval(bih, o, d, tmax)
    if start is None:
        return False
    stack = [(0, start[0], start[1])]
    while stack:
        i, tn, tf = stack.pop()
        nd = bih.nodes[i]
        if nd.axis < 0:
            for r in bih.refs[nd.first : nd.first + nd.count]:
                t = hit_triangle(tris[r], o, d)
                if t is not None and t <= tmax:
                    return True
            continue
        a = nd.axis
        for bound, below, child in ((nd.lclip, True, nd.left), (nd.rclip, False, nd.right)):
            r = clip(o, d, a, bound, below, tn, tf)
            if r is not None:
                stack.append((child, r[0], r[1]))
    return False


def implicit_boxes(bih: BIH) -> list[Box]:
    """The box of each node: the scene box cut by the clip planes on its path. Cost: O(number of nodes)."""
    out: list[Box | None] = [None] * len(bih.nodes)
    stack = [(0, list(bih.lo), list(bih.hi))]
    while stack:
        i, lo, hi = stack.pop()
        out[i] = (tuple(lo), tuple(hi))  # type: ignore[assignment]
        nd = bih.nodes[i]
        if nd.axis >= 0:
            a = nd.axis
            stack.append((nd.left, lo, hi[:a] + [min(hi[a], nd.lclip)] + hi[a + 1 :]))
            stack.append((nd.right, lo[:a] + [max(lo[a], nd.rclip)] + lo[a + 1 :], hi))
    return out  # type: ignore[return-value]
