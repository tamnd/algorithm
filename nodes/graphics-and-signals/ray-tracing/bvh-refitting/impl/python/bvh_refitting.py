# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bvh-refitting/. The authors are listed in prov/5ASM9T.jsonl.

"""BVH refitting: new boxes for a BVH of fixed shape after its triangles move.

The tree comes from a binned SAH build (the same as on the bvh-construction page). The
nodes are stored in one list in which a node comes before its children, so a pass over the
list in reverse order visits the children before the parents. Coordinates are integers or
Fractions, so all boxes, costs and hit tests are exact.
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
    lo: Vec
    hi: Vec
    left: int = -1  # index of the left child, -1 for a leaf
    right: int = -1  # index of the right child, -1 for a leaf
    first: int = 0  # a leaf holds refs[first : first + count]
    count: int = 0


def tri_box(t: Tri) -> Box:
    lo = tuple(min(p[a] for p in t) for a in range(3))
    hi = tuple(max(p[a] for p in t) for a in range(3))
    return lo, hi  # type: ignore[return-value]


def union(a: Box | None, b: Box) -> Box:
    if a is None:
        return b
    lo = tuple(min(a[0][i], b[0][i]) for i in range(3))
    hi = tuple(max(a[1][i], b[1][i]) for i in range(3))
    return lo, hi  # type: ignore[return-value]


def area(b: Box | None) -> Num:
    """Surface area of a box; 0 for the empty box (None)."""
    if b is None:
        return 0
    w = [b[1][i] - b[0][i] for i in range(3)]
    return 2 * (w[0] * w[1] + w[1] * w[2] + w[2] * w[0])


def bin_of(c: Num, lo: Num, hi: Num, k: int) -> int:
    return min(k - 1, math.floor(k * Fraction(c - lo) / (hi - lo)))


def build(tris: list[Tri], bins: int = 16, max_leaf: int = 4) -> tuple[list[Node], list[int]]:
    """Binned SAH build with c_trav = c_isect = 1. Return (nodes, refs); nodes[0] is the root.

    Precondition: tris is not empty. Cost: O(n log n) when the depth is O(log n), O(n^2) worst case.
    """
    n = len(tris)
    boxes = [tri_box(t) for t in tris]
    cen = [tuple(sum(p[a] for p in t) for a in range(3)) for t in tris]
    refs = list(range(n))
    nodes: list[Node] = []
    stack = [(0, n, -1, False)]
    while stack:
        first, count, parent, is_right = stack.pop()
        part = refs[first : first + count]
        box: Box | None = None
        for r in part:
            box = union(box, boxes[r])
        assert box is not None
        idx = len(nodes)
        nodes.append(Node(box[0], box[1], first=first, count=count))
        if parent >= 0:
            if is_right:
                nodes[parent].right = idx
            else:
                nodes[parent].left = idx
        clo = [min(cen[r][a] for r in part) for a in range(3)]
        chi = [max(cen[r][a] for r in part) for a in range(3)]
        if count == 1 or clo == chi:
            continue
        best: tuple[Num, int, int] | None = None
        for a in range(3):
            if clo[a] == chi[a]:
                continue
            bbox: list[Box | None] = [None] * bins
            bcnt = [0] * bins
            for r in part:
                k = bin_of(cen[r][a], clo[a], chi[a], bins)
                bbox[k] = union(bbox[k], boxes[r])
                bcnt[k] += 1
            right_area: list[Num] = [0] * bins
            acc: Box | None = None
            cnt = 0
            for j in range(bins - 1, 0, -1):
                acc = union(acc, bbox[j]) if bbox[j] is not None else acc
                cnt += bcnt[j]
                right_area[j] = area(acc) * cnt
            acc, cnt = None, 0
            for j in range(1, bins):
                acc = union(acc, bbox[j - 1]) if bbox[j - 1] is not None else acc
                cnt += bcnt[j - 1]
                if cnt == 0 or cnt == count:
                    continue
                score = area(acc) * cnt + right_area[j]
                if best is None or score < best[0]:
                    best = (score, a, j)
        assert best is not None
        score, axis, j = best
        a_box = area(box)
        cost = 1 + Fraction(score) / a_box if a_box > 0 else None
        if count <= max_leaf and (cost is None or count <= cost):
            continue
        left = [r for r in part if bin_of(cen[r][axis], clo[axis], chi[axis], bins) < j]
        right = [r for r in part if bin_of(cen[r][axis], clo[axis], chi[axis], bins) >= j]
        refs[first : first + count] = left + right
        nodes[idx].count = 0
        stack.append((first + len(left), len(right), idx, True))
        stack.append((first, len(left), idx, False))
    return nodes, refs


def refit(nodes: list[Node], refs: list[int], tris: list[Tri]) -> None:
    """Set every box of the tree to the tight box of the triangles below it, at their current positions.

    Precondition: each node comes before its children in nodes, and refs is the leaf order of the build.
    The shape of the tree and the triangles in each leaf stay the same.
    Cost: O(n) time for n triangles (the tree has at most 2n - 1 nodes), O(n) extra space.
    """
    boxes = [tri_box(t) for t in tris]  # @line L1
    for i in range(len(nodes) - 1, -1, -1):  # @line L2
        nd = nodes[i]
        if nd.left < 0:  # @line L3
            box: Box | None = None
            for r in refs[nd.first : nd.first + nd.count]:
                box = union(box, boxes[r])
            assert box is not None
        else:  # @line L4
            box = union((nodes[nd.left].lo, nodes[nd.left].hi), (nodes[nd.right].lo, nodes[nd.right].hi))
        nd.lo, nd.hi = box


def needs_rebuild(nodes: list[Node], cost_at_build: Fraction, rho: Num) -> bool:
    """True when the SAH cost of the refitted tree is more than rho times its cost after the last build."""
    return sah_cost(nodes) > rho * cost_at_build  # @line L5


def parents_and_leaves(nodes: list[Node], refs: list[int]) -> tuple[list[int], dict[int, int]]:
    """The parent of each node (-1 for the root) and the leaf of each triangle. Cost: O(n)."""
    parent = [-1] * len(nodes)
    leaf_of: dict[int, int] = {}
    for i, nd in enumerate(nodes):
        if nd.left >= 0:
            parent[nd.left] = i
            parent[nd.right] = i
        else:
            for r in refs[nd.first : nd.first + nd.count]:
                leaf_of[r] = i
    return parent, leaf_of


def refit_moved(
    nodes: list[Node], refs: list[int], tris: list[Tri], moved: list[int], parent: list[int], leaf_of: dict[int, int]
) -> int:
    """Refit only the paths from the leaves of the moved triangles to the root.

    A walk stops at a node whose box does not change, since its ancestors then stay correct.
    Precondition: before the motion every box was tight. Return the number of nodes recomputed.
    Cost: O(k h) for k moved triangles and a tree of height h, and never more than O(n) per walk.
    """
    work = 0
    for r in moved:
        i = leaf_of[r]
        while i >= 0:
            nd = nodes[i]
            if nd.left < 0:
                box: Box | None = None
                for q in refs[nd.first : nd.first + nd.count]:
                    box = union(box, tri_box(tris[q]))
                assert box is not None
            else:
                box = union((nodes[nd.left].lo, nodes[nd.left].hi), (nodes[nd.right].lo, nodes[nd.right].hi))
            work += 1
            if box == (nd.lo, nd.hi):
                break
            nd.lo, nd.hi = box
            i = parent[i]
    return work


def sah_cost(nodes: list[Node], c_trav: Num = 1, c_isect: Num = 1) -> Fraction:
    """SAH cost of a tree over the area of its root. Precondition: the root box has positive area."""
    total = Fraction(0)
    for nd in nodes:
        a = area((nd.lo, nd.hi))
        total += c_trav * a if nd.left >= 0 else c_isect * a * nd.count
    return total / area((nodes[0].lo, nodes[0].hi))


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


def closest_hit(nodes: list[Node], refs: list[int], tris: list[Tri], o: Vec, d: Vec) -> tuple[Fraction, int] | None:
    """The nearest hit (t, triangle index) of the ray o + t d, t >= 0, or None. Cost: O(n) worst case."""
    best: tuple[Fraction, int] | None = None
    tmax: Num | float = math.inf
    stack = [0]
    while stack:
        nd = nodes[stack.pop()]
        if box_entry(nd.lo, nd.hi, o, d, tmax) is None:
            continue
        if nd.left < 0:
            for r in refs[nd.first : nd.first + nd.count]:
                t = hit_triangle(tris[r], o, d)
                if t is not None and t <= tmax and (best is None or t < best[0]):
                    best, tmax = (t, r), t
        else:
            stack.append(nd.right)
            stack.append(nd.left)
    return best


def any_hit(nodes: list[Node], refs: list[int], tris: list[Tri], o: Vec, d: Vec, tmax: Num | float) -> bool:
    """True if the ray o + t d meets a triangle with 0 <= t <= tmax. Cost: O(n) worst case."""
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
