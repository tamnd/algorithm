# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lbvh-construction/. The authors are listed in prov/PTNB7Y.jsonl.

"""Linear BVH construction: Morton codes, a radix sort, and the hierarchy of Karras (2012).

Every internal node is computed on its own from the sorted keys, so the loop over internal
nodes could run in parallel; here it runs in order. The boxes are then formed bottom up with
parent links and visit counters, as a GPU does with atomic counters. Coordinates are integers
or Fractions, so all boxes and hit tests are exact.
"""

from dataclasses import dataclass, field
from fractions import Fraction
import math

Num = int | Fraction
Vec = tuple[Num, Num, Num]
Tri = tuple[Vec, Vec, Vec]
Box = tuple[Vec, Vec]

BITS = 10  # bits per axis of the Morton code


def spread(x: int) -> int:
    """Put the 10 bits of x at the positions 0, 3, 6, ..., 27. Cost: O(1)."""
    r = 0
    for k in range(BITS):
        r |= ((x >> k) & 1) << (3 * k)
    return r


def morton3(x: int, y: int, z: int) -> int:
    """The 30-bit Morton code of a cell (x, y, z) in [0, 1024)^3, with x on the highest bit of each triple."""
    return (spread(x) << 2) | (spread(y) << 1) | spread(z)


def quantize(c: Num, lo: Num, hi: Num) -> int:
    """Cell index in [0, 1023] of c in [lo, hi]; 0 when lo = hi."""
    if hi == lo:
        return 0
    return min((1 << BITS) - 1, math.floor((1 << BITS) * Fraction(c - lo) / (hi - lo)))


def radix_sort(items: list[tuple[int, int]], key_bits: int, digit_bits: int = 8) -> list[tuple[int, int]]:
    """Stable LSD radix sort of (key, value) pairs with 0 <= key < 2^key_bits.

    Cost: O((key_bits / digit_bits) (n + 2^digit_bits)) time, O(n + 2^digit_bits) extra space.
    """
    mask = (1 << digit_bits) - 1
    shift = 0
    while shift < key_bits:
        count = [0] * (mask + 2)
        for k, _ in items:
            count[((k >> shift) & mask) + 1] += 1
        for i in range(mask + 1):
            count[i + 1] += count[i]
        out: list[tuple[int, int]] = [(0, 0)] * len(items)
        for k, v in items:
            dgt = (k >> shift) & mask
            out[count[dgt]] = (k, v)
            count[dgt] += 1
        items = out
        shift += digit_bits
    return items


@dataclass
class Hierarchy:
    """n leaves and n - 1 internal nodes; internal node 0 is the root when n >= 2.

    A child is a pair (is_leaf, index). Leaf k is the k-th primitive in sorted order.
    """

    left: list[tuple[bool, int]] = field(default_factory=list)
    right: list[tuple[bool, int]] = field(default_factory=list)
    span: list[tuple[int, int]] = field(default_factory=list)  # first and last leaf below each internal node
    parent_internal: list[int] = field(default_factory=list)
    parent_leaf: list[int] = field(default_factory=list)


def karras(keys: list[int], width: int) -> Hierarchy:
    """The binary radix tree of sorted distinct keys of `width` bits (Karras 2012).

    Precondition: len(keys) >= 2, keys strictly increasing.
    Cost: O(log n) per internal node in the worst case, O(n log n) in total; each node is independent.
    """
    n = len(keys)

    def delta(i: int, j: int) -> int:
        if j < 0 or j >= n:
            return -1
        return width - (keys[i] ^ keys[j]).bit_length()  # length of the common prefix

    h = Hierarchy([(False, 0)] * (n - 1), [(False, 0)] * (n - 1), [(0, 0)] * (n - 1), [-1] * (n - 1), [-1] * n)
    for i in range(n - 1):  # @line L4
        d = 1 if delta(i, i + 1) - delta(i, i - 1) > 0 else -1  # @line L5
        dmin = delta(i, i - d)  # @line L6
        lmax = 2
        while delta(i, i + lmax * d) > dmin:
            lmax *= 2
        l = 0  # @line L7
        t = lmax // 2
        while t >= 1:
            if delta(i, i + (l + t) * d) > dmin:
                l += t
            t //= 2
        j = i + l * d  # @line L8
        dnode = delta(i, j)
        s = 0  # @line L9
        t = l
        while True:
            t = (t + 1) // 2
            if delta(i, i + (s + t) * d) > dnode:
                s += t
            if t == 1:
                break
        gamma = i + s * d + min(d, 0)  # @line L10
        lo, hi = min(i, j), max(i, j)
        h.left[i] = (True, gamma) if lo == gamma else (False, gamma)  # @line L11
        h.right[i] = (True, gamma + 1) if hi == gamma + 1 else (False, gamma + 1)
        h.span[i] = (lo, hi)
        for is_leaf, c in (h.left[i], h.right[i]):
            if is_leaf:
                h.parent_leaf[c] = i
            else:
                h.parent_internal[c] = i
    return h


def tri_box(t: Tri) -> Box:
    return tuple(min(p[a] for p in t) for a in range(3)), tuple(max(p[a] for p in t) for a in range(3))  # type: ignore[return-value]


def union(a: Box, b: Box) -> Box:
    lo = tuple(min(a[0][i], b[0][i]) for i in range(3))
    hi = tuple(max(a[1][i], b[1][i]) for i in range(3))
    return lo, hi  # type: ignore[return-value]


@dataclass
class LBVH:
    order: list[int]  # order[k]: the primitive of leaf k
    keys: list[int]  # sorted augmented keys
    tree: Hierarchy | None  # None when there is one primitive
    leaf_box: list[Box]
    box: list[Box]  # boxes of the internal nodes


def build(tris: list[Tri]) -> LBVH:
    """Linear BVH of the triangles. Precondition: tris is not empty.

    Cost: O(n) for the codes and the radix sort, O(n log n) worst case for the hierarchy, O(n) for the boxes.
    """
    n = len(tris)
    cen = [tuple(sum(p[a] for p in t) for a in range(3)) for t in tris]  # 3 times the centroid
    clo = [min(c[a] for c in cen) for a in range(3)]
    chi = [max(c[a] for c in cen) for a in range(3)]
    codes = [morton3(*(quantize(c[a], clo[a], chi[a]) for a in range(3))) for c in cen]  # @line L1
    b = max(1, (n - 1).bit_length())
    width = 3 * BITS + b
    items = [((codes[p] << b) | p, p) for p in range(n)]  # @line L2
    items = radix_sort(items, width)  # @line L3
    order = [p for _, p in items]
    keys = [k for k, _ in items]
    leaf_box = [tri_box(tris[p]) for p in order]
    if n == 1:
        return LBVH(order, keys, None, leaf_box, [])
    tree = karras(keys, width)
    box: list[Box | None] = [None] * (n - 1)
    visits = [0] * (n - 1)
    for k in range(n):  # @line L12
        i = tree.parent_leaf[k]
        while i >= 0:
            visits[i] += 1
            if visits[i] == 1:
                break  # the first arrival stops; the second one has both children ready
            boxes = []
            for is_leaf, c in (tree.left[i], tree.right[i]):
                boxes.append(leaf_box[c] if is_leaf else box[c])
            box[i] = union(boxes[0], boxes[1])  # type: ignore[arg-type]
            i = tree.parent_internal[i]
    return LBVH(order, keys, tree, leaf_box, box)  # type: ignore[arg-type]


def radix_tree_reference(keys: list[int], width: int) -> set[tuple[int, int, int]]:
    """Top-down reference: (first, last, split) of each internal node, split at the highest differing bit."""
    out = set()
    stack = [(0, len(keys) - 1)]
    while stack:
        f, l = stack.pop()
        if f == l:
            continue
        bit = (keys[f] ^ keys[l]).bit_length() - 1
        m = f
        while (keys[m + 1] >> bit) & 1 == (keys[f] >> bit) & 1:
            m += 1
        out.add((f, l, m))
        stack.append((f, m))
        stack.append((m + 1, l))
    return out


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


def closest_hit(bvh: LBVH, tris: list[Tri], o: Vec, d: Vec) -> tuple[Fraction, int] | None:
    """Nearest hit (t, triangle) of o + t d, t >= 0, or None. Cost: O(n) worst case."""
    best: tuple[Fraction, int] | None = None
    tmax: Num | float = math.inf
    stack = [(True, 0)] if bvh.tree is None else [(False, 0)]
    while stack:
        is_leaf, i = stack.pop()
        lo, hi = bvh.leaf_box[i] if is_leaf else bvh.box[i]
        if box_entry(lo, hi, o, d, tmax) is None:
            continue
        if is_leaf:
            p = bvh.order[i]
            t = hit_triangle(tris[p], o, d)
            if t is not None and t <= tmax and (best is None or t < best[0]):
                best, tmax = (t, p), t
        else:
            assert bvh.tree is not None
            stack.append(bvh.tree.right[i])
            stack.append(bvh.tree.left[i])
    return best


def any_hit(bvh: LBVH, tris: list[Tri], o: Vec, d: Vec, tmax: Num | float) -> bool:
    """True if o + t d meets a triangle with 0 <= t <= tmax."""
    stack = [(True, 0)] if bvh.tree is None else [(False, 0)]
    while stack:
        is_leaf, i = stack.pop()
        lo, hi = bvh.leaf_box[i] if is_leaf else bvh.box[i]
        if box_entry(lo, hi, o, d, tmax) is None:
            continue
        if is_leaf:
            t = hit_triangle(tris[bvh.order[i]], o, d)
            if t is not None and t <= tmax:
                return True
        else:
            assert bvh.tree is not None
            stack.append(bvh.tree.right[i])
            stack.append(bvh.tree.left[i])
    return False
