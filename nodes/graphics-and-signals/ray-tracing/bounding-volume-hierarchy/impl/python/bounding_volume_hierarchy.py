# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounding-volume-hierarchy/. The authors are listed in prov/NZ1MVD.jsonl.

"""A bounding volume hierarchy of axis-aligned boxes over triangles, with exact arithmetic.

Coordinates are integers or Fractions, so every box test and triangle test is exact.
The nodes are stored in one list in depth-first order: a node comes before its children.
"""

from dataclasses import dataclass
from fractions import Fraction
import math

Num = int | Fraction
Vec = tuple[Num, Num, Num]
Tri = tuple[Vec, Vec, Vec]


@dataclass
class Node:
    lo: Vec
    hi: Vec
    left: int = -1  # index of the left child, -1 for a leaf
    right: int = -1  # index of the right child, -1 for a leaf
    first: int = 0  # a leaf holds refs[first : first + count]
    count: int = 0


def tri_box(t: Tri) -> tuple[Vec, Vec]:
    lo = tuple(min(p[a] for p in t) for a in range(3))
    hi = tuple(max(p[a] for p in t) for a in range(3))
    return lo, hi  # type: ignore[return-value]


def union(a: tuple[Vec, Vec], b: tuple[Vec, Vec]) -> tuple[Vec, Vec]:
    lo = tuple(min(a[0][i], b[0][i]) for i in range(3))
    hi = tuple(max(a[1][i], b[1][i]) for i in range(3))
    return lo, hi  # type: ignore[return-value]


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


def box_entry(lo: Vec, hi: Vec, o: Vec, d: Vec, tmax: Num | float) -> Fraction | None:
    """Exact slab test of the closed box against o + t d, t in [0, tmax]: the entry t or None."""
    t0: Fraction = Fraction(0)
    t1 = tmax
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
    return t0


def build(tris: list[Tri], leaf_size: int = 2) -> tuple[list[Node], list[int]]:
    """Top-down build with the object median split on the longest axis of the centroid box.

    Precondition: tris is not empty. Return (nodes, refs); nodes[0] is the root.
    Cost: O(n log^2 n) time with a sort per node, O(n) space.
    """
    n = len(tris)
    boxes = [tri_box(t) for t in tris]
    cen = [tuple(sum(p[a] for p in t) for a in range(3)) for t in tris]  # 3 times the centroid
    refs = list(range(n))  # @line L1
    nodes: list[Node] = []
    stack = [(0, n, -1, False)]  # (first, count, parent, is right child)
    while stack:  # @line L2
        first, count, parent, is_right = stack.pop()
        box = boxes[refs[first]]
        for r in refs[first + 1 : first + count]:
            box = union(box, boxes[r])
        idx = len(nodes)
        nodes.append(Node(box[0], box[1], first=first, count=count))  # @line L3
        if parent >= 0:
            if is_right:
                nodes[parent].right = idx
            else:
                nodes[parent].left = idx
        if count <= leaf_size:  # @line L4
            continue
        part = refs[first : first + count]
        clo = [min(cen[r][a] for r in part) for a in range(3)]
        chi = [max(cen[r][a] for r in part) for a in range(3)]
        axis = max(range(3), key=lambda a: chi[a] - clo[a])  # @line L5
        if chi[axis] == clo[axis]:
            continue  # all centroids coincide: keep a leaf
        part.sort(key=lambda r: cen[r][axis])  # @line L6
        refs[first : first + count] = part
        half = count // 2
        nodes[idx].count = 0
        stack.append((first + half, count - half, idx, True))  # @line L7
        stack.append((first, half, idx, False))  # @line L8
    return nodes, refs


def closest_hit(nodes: list[Node], refs: list[int], tris: list[Tri], o: Vec, d: Vec) -> tuple[Fraction, int] | None:
    """The nearest hit (t, triangle index) of the ray o + t d, t >= 0, or None.

    Cost: O(n) node visits in the worst case; a box farther than the best hit is skipped.
    """
    best: tuple[Fraction, int] | None = None
    tmax: Num | float = math.inf
    stack = [0]  # @line L9
    while stack:  # @line L10
        i = stack.pop()
        nd = nodes[i]
        if box_entry(nd.lo, nd.hi, o, d, tmax) is None:  # @line L11
            continue
        if nd.left < 0:  # @line L12
            for r in refs[nd.first : nd.first + nd.count]:
                t = hit_triangle(tris[r], o, d)
                if t is not None and t <= tmax and (best is None or t < best[0]):  # @line L13
                    best, tmax = (t, r), t
        else:
            stack.append(nd.right)  # @line L14
            stack.append(nd.left)
    return best  # @line L15


def any_hit(nodes: list[Node], refs: list[int], tris: list[Tri], o: Vec, d: Vec, tmax: Num | float) -> bool:
    """True if the ray o + t d meets a triangle with 0 <= t <= tmax. Stops at the first such hit."""
    stack = [0]
    while stack:
        nd = nodes[stack.pop()]
        if box_entry(nd.lo, nd.hi, o, d, tmax) is None:
            continue
        if nd.left < 0:
            for r in refs[nd.first : nd.first + nd.count]:
                t = hit_triangle(tris[r], o, d)
                if t is not None and t <= tmax:
                    return True
        else:
            stack.append(nd.right)
            stack.append(nd.left)
    return False


def refit(nodes: list[Node], refs: list[int], tris: list[Tri]) -> None:
    """Recompute every box bottom up after the triangles moved. The tree shape is kept.

    Precondition: each node comes before its children in the list. Cost: O(n).
    """
    for i in range(len(nodes) - 1, -1, -1):  # @line L16
        nd = nodes[i]
        if nd.left < 0:  # @line L17
            box = tri_box(tris[refs[nd.first]])
            for r in refs[nd.first + 1 : nd.first + nd.count]:
                box = union(box, tri_box(tris[r]))
        else:
            a, b = nodes[nd.left], nodes[nd.right]
            box = union((a.lo, a.hi), (b.lo, b.hi))  # @line L18
        nd.lo, nd.hi = box
