# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spatial-splits/. The authors are listed in prov/C37NSZ.jsonl.

"""A split BVH (SBVH) builder in the style of Stich, Friedrich and Dietrich (2009), in exact arithmetic.

At each node the builder rates the best object split and, when the two boxes of that split
overlap enough, the best spatial split, which cuts the references at a plane. A reference that
crosses the plane is clipped into two references with tighter boxes, one in each child, so a
triangle can be in several leaves. Triangles have integer vertices and all clipping uses
Fractions, so the boxes are exact.
"""

from dataclasses import dataclass
from fractions import Fraction
import math

Num = int | Fraction
Vec = tuple[Num, Num, Num]
Tri = tuple[Vec, Vec, Vec]
Box = tuple[Vec, Vec]
Ref = tuple[int, Vec, Vec]  # (triangle index, lo, hi of the clipped piece)


@dataclass
class Node:
    lo: Vec
    hi: Vec
    left: int = -1  # index of the left child, -1 for a leaf
    right: int = -1
    first: int = 0  # a leaf holds refs[first : first + count], as triangle indices
    count: int = 0
    size: int = 0  # number of references of the node when it was made


def union(a: Box | None, b: Box | None) -> Box | None:
    if a is None:
        return b
    if b is None:
        return a
    lo = tuple(min(a[0][i], b[0][i]) for i in range(3))
    hi = tuple(max(a[1][i], b[1][i]) for i in range(3))
    return lo, hi  # type: ignore[return-value]


def area(b: Box | None) -> Num:
    if b is None:
        return 0
    w = [b[1][i] - b[0][i] for i in range(3)]
    return 2 * (w[0] * w[1] + w[1] * w[2] + w[2] * w[0])


def clip_half(poly: list[Vec], axis: int, value: Num, keep_low: bool) -> list[Vec]:
    """Sutherland-Hodgman: the part of a convex polygon with x_axis <= value (or >= value). Cost: O(len(poly))."""
    out: list[Vec] = []
    side = (lambda p: value - p[axis]) if keep_low else (lambda p: p[axis] - value)
    for k in range(len(poly)):
        p, q = poly[k], poly[(k + 1) % len(poly)]
        sp, sq = side(p), side(q)
        if sp >= 0:
            out.append(p)
        if (sp > 0 and sq < 0) or (sp < 0 and sq > 0):
            t = Fraction(sp) / (sp - sq)
            out.append(tuple(p[i] + t * (q[i] - p[i]) for i in range(3)))  # type: ignore[arg-type]
    return out


def clip_box(tri: Tri, lo: Vec, hi: Vec) -> Box | None:
    """Box of the part of the triangle inside the closed box [lo, hi], or None if it is empty. Cost: O(1)."""
    poly: list[Vec] = list(tri)
    for a in range(3):
        poly = clip_half(poly, a, lo[a], keep_low=False)
        poly = clip_half(poly, a, hi[a], keep_low=True)
        if not poly:
            return None
    plo = tuple(min(p[a] for p in poly) for a in range(3))
    phi = tuple(max(p[a] for p in poly) for a in range(3))
    return plo, phi  # type: ignore[return-value]


def tri_box(t: Tri) -> Box:
    return tuple(min(p[a] for p in t) for a in range(3)), tuple(max(p[a] for p in t) for a in range(3))  # type: ignore[return-value]


def best_object_split(refs: list[Ref]) -> tuple[Num, list[Ref], list[Ref], Box, Box]:
    """Least A(L)|L| + A(R)|R| over the splits of the refs sorted by box center on each axis.

    Return (score, L, R, box of L, box of R). Precondition: len(refs) >= 2. Cost: O(n log n).
    """
    n = len(refs)
    best = None
    for a in range(3):
        order = sorted(refs, key=lambda r: r[1][a] + r[2][a])  # stable: ties keep the input order
        right: list[Box | None] = [None] * (n + 1)
        for i in range(n - 1, 0, -1):
            right[i] = union(right[i + 1], (order[i][1], order[i][2]))
        acc: Box | None = None
        for i in range(1, n):
            acc = union(acc, (order[i - 1][1], order[i - 1][2]))
            score = area(acc) * i + area(right[i]) * (n - i)
            if best is None or score < best[0]:
                best = (score, order[:i], order[i:], acc, right[i])
    assert best is not None
    return best  # type: ignore[return-value]


def bin_of(x: Num, lo: Num, hi: Num, k: int) -> int:
    return min(k - 1, math.floor(k * Fraction(x - lo) / (hi - lo)))


def best_spatial_split(tris: list[Tri], refs: list[Ref], box: Box, bins: int) -> tuple[Num, int, Fraction] | None:
    """Least A(L) N(L) + A(R) N(R) over the planes between `bins` equal bins of the node box on each axis.

    Only splits that leave each side with fewer references than the node are valid.
    Return (score, axis, plane) or None. Cost: O(n bins) clipping work.
    """
    n = len(refs)
    best = None
    for a in range(3):
        lo_a, hi_a = box[0][a], box[1][a]
        if lo_a == hi_a:
            continue
        planes = [lo_a + Fraction(k * (hi_a - lo_a), bins) for k in range(bins + 1)]
        bbox: list[Box | None] = [None] * bins
        enter, leave = [0] * bins, [0] * bins
        for t, rlo, rhi in refs:  # @line L3
            k0, k1 = bin_of(rlo[a], lo_a, hi_a, bins), bin_of(rhi[a], lo_a, hi_a, bins)
            enter[k0] += 1
            leave[k1] += 1
            for k in range(k0, k1 + 1):
                slo = tuple(planes[k] if i == a else rlo[i] for i in range(3))
                shi = tuple(planes[k + 1] if i == a else rhi[i] for i in range(3))
                piece = clip_box(tris[t], max_vec(slo, rlo), min_vec(shi, rhi))
                bbox[k] = union(bbox[k], piece)
        right: list[Box | None] = [None] * (bins + 1)
        n_right = [0] * (bins + 1)
        for j in range(bins - 1, 0, -1):
            right[j] = union(right[j + 1], bbox[j])
            n_right[j] = n_right[j + 1] + leave[j]
        acc: Box | None = None
        n_left = 0
        for j in range(1, bins):  # @line L4
            acc = union(acc, bbox[j - 1])
            n_left += enter[j - 1]
            if n_left == 0 or n_right[j] == 0 or n_left >= n or n_right[j] >= n:
                continue
            score = area(acc) * n_left + area(right[j]) * n_right[j]
            if best is None or score < best[0]:  # @line L5
                best = (score, a, planes[j])
    return best


def max_vec(p: Vec, q: Vec) -> Vec:
    return tuple(max(p[i], q[i]) for i in range(3))  # type: ignore[return-value]


def min_vec(p: Vec, q: Vec) -> Vec:
    return tuple(min(p[i], q[i]) for i in range(3))  # type: ignore[return-value]


def split_refs(tris: list[Tri], refs: list[Ref], axis: int, plane: Fraction, box: Box, bins: int) -> tuple[list[Ref], list[Ref]]:
    """Partition the refs at the plane x_axis = plane; a ref that crosses it is clipped into both sides.

    The side of a ref follows its first and last bin, as in best_spatial_split. Cost: O(n).
    """
    lo_a, hi_a = box[0][axis], box[1][axis]
    j = bin_of(plane, lo_a, hi_a, bins)  # the plane is the lower face of bin j
    left: list[Ref] = []
    right: list[Ref] = []
    for t, rlo, rhi in refs:
        k0, k1 = bin_of(rlo[axis], lo_a, hi_a, bins), bin_of(rhi[axis], lo_a, hi_a, bins)
        if k1 < j:
            left.append((t, rlo, rhi))
        elif k0 >= j:
            right.append((t, rlo, rhi))
        else:  # @line L7
            lb = clip_box(tris[t], rlo, tuple(plane if i == axis else rhi[i] for i in range(3)))  # type: ignore[arg-type]
            rb = clip_box(tris[t], tuple(plane if i == axis else rlo[i] for i in range(3)), rhi)  # type: ignore[arg-type]
            assert lb is not None and rb is not None
            left.append((t, lb[0], lb[1]))
            right.append((t, rb[0], rb[1]))
    return left, right


def build(
    tris: list[Tri],
    bins: int = 8,
    max_leaf: int = 2,
    alpha: Fraction = Fraction(0),
    c_trav: Num = 1,
    c_isect: Num = 1,
    log: list[tuple[int, str, Num]] | None = None,
) -> tuple[list[Node], list[Ref]]:
    """Build an SBVH. Return (nodes, refs); a leaf holds refs[first : first + count].

    Spatial splits are tried when the boxes of the best object split overlap in a box of area
    greater than alpha times the area of the root; alpha >= 1 gives a plain object-split BVH.
    log gets (node, "object" or "spatial", cost) for each split.
    Precondition: tris is not empty and the root box has positive area.
    Cost: O(n log n) per node for the sweeps plus O(n bins) for the clipping; O(r) space for r refs.
    """
    root: Box | None = None
    for t in tris:
        root = union(root, tri_box(t))
    assert root is not None
    a_root = area(root)
    nodes: list[Node] = []
    out: list[Ref] = []
    stack: list[tuple[list[Ref], int, bool]] = [([(i, *tri_box(t)) for i, t in enumerate(tris)], -1, False)]
    while stack:
        rs, parent, is_right = stack.pop()
        box: Box | None = None
        for _, rlo, rhi in rs:
            box = union(box, (rlo, rhi))
        assert box is not None
        idx = len(nodes)
        nodes.append(Node(box[0], box[1], size=len(rs)))
        if parent >= 0:
            if is_right:
                nodes[parent].right = idx
            else:
                nodes[parent].left = idx
        n = len(rs)
        a_box = area(box)
        if n == 1 or a_box == 0:
            nodes[idx].first, nodes[idx].count = len(out), n
            out.extend(rs)
            continue
        o_score, o_left, o_right, o_lbox, o_rbox = best_object_split(rs)  # @line L1
        best = (o_score, "object")
        ov_lo, ov_hi = max_vec(o_lbox[0], o_rbox[0]), min_vec(o_lbox[1], o_rbox[1])
        overlap = (ov_lo, ov_hi) if all(ov_lo[i] <= ov_hi[i] for i in range(3)) else None
        s = None
        if area(overlap) > alpha * a_root:  # @line L2
            s = best_spatial_split(tris, rs, box, bins)
            if s is not None and s[0] < o_score:
                best = (s[0], "spatial")
        cost = c_trav + c_isect * Fraction(best[0]) / a_box  # @line L6
        if n <= max_leaf and c_isect * n <= cost:
            nodes[idx].first, nodes[idx].count = len(out), n
            out.extend(rs)
            continue
        if log is not None:
            log.append((idx, best[1], cost))
        if best[1] == "spatial":
            assert s is not None
            left, right = split_refs(tris, rs, s[1], s[2], box, bins)
        else:
            left, right = o_left, o_right
        stack.append((right, idx, True))
        stack.append((left, idx, False))
    return nodes, out


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


def closest_hit(nodes: list[Node], refs: list[Ref], tris: list[Tri], o: Vec, d: Vec) -> tuple[Fraction, int] | None:
    """Nearest hit (t, triangle) of o + t d, t >= 0. A leaf tests the whole triangle of each of its refs."""
    best: tuple[Fraction, int] | None = None
    tmax: Num | float = math.inf
    stack = [0]
    while stack:
        nd = nodes[stack.pop()]
        if box_entry(nd.lo, nd.hi, o, d, tmax) is None:
            continue
        if nd.left < 0:
            for r, _, _ in refs[nd.first : nd.first + nd.count]:
                t = hit_triangle(tris[r], o, d)
                if t is not None and t <= tmax and (best is None or t < best[0]):
                    best, tmax = (t, r), t
        else:
            stack.append(nd.right)
            stack.append(nd.left)
    return best


def any_hit(nodes: list[Node], refs: list[Ref], tris: list[Tri], o: Vec, d: Vec, tmax: Num | float) -> bool:
    """True if o + t d meets a triangle with 0 <= t <= tmax."""
    stack = [0]
    while stack:
        nd = nodes[stack.pop()]
        if box_entry(nd.lo, nd.hi, o, d, tmax) is None:
            continue
        if nd.left < 0:
            for r, _, _ in refs[nd.first : nd.first + nd.count]:
                t = hit_triangle(tris[r], o, d)
                if t is not None and t <= tmax:
                    return True
        else:
            stack.append(nd.right)
            stack.append(nd.left)
    return False


def sah_cost(nodes: list[Node], c_trav: Num = 1, c_isect: Num = 1) -> Fraction:
    """SAH cost of the tree; a leaf counts each of its references. Precondition: root area > 0."""
    total = Fraction(0)
    for nd in nodes:
        a = area((nd.lo, nd.hi))
        total += c_trav * a if nd.left >= 0 else c_isect * a * nd.count
    return total / area((nodes[0].lo, nodes[0].hi))
