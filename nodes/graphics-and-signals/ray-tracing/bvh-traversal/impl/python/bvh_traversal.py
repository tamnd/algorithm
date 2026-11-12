# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bvh-traversal/. The authors are listed in prov/2KJ4A7.jsonl.

"""Stack-based BVH traversal for closest-hit and any-hit queries, with exact arithmetic.

Coordinates are integers or Fractions. The nodes are in one list; a leaf has left == -1 and
holds refs[first : first + count].
"""

from dataclasses import dataclass, field
from fractions import Fraction
import math

Num = int | Fraction
Vec = tuple[Num, Num, Num]
Tri = tuple[Vec, Vec, Vec]


@dataclass
class Node:
    lo: Vec
    hi: Vec
    left: int = -1
    right: int = -1
    first: int = 0
    count: int = 0


@dataclass
class Counts:
    """Work done by one query: popped nodes, box tests and primitive tests."""

    nodes: int = 0
    boxes: int = 0
    prims: int = 0
    pops: list[int] = field(default_factory=list)


def hit_triangle(t: Tri, o: Vec, d: Vec) -> Fraction | None:
    """Exact Moller-Trumbore: the t >= 0 of the hit of o + t d with the closed triangle, or None."""
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


def slab_entry(lo: Vec, hi: Vec, o: Vec, d: Vec, tmax: Num | float) -> Fraction | None:
    """Exact slab method on the closed box, ray parameter in [0, tmax]: the entry t, or None."""
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


def closest_hit(
    nodes: list[Node], refs: list[int], tris: list[Tri], o: Vec, d: Vec, counts: Counts | None = None
) -> tuple[Fraction, int] | None:
    """The hit (t, triangle index) with the least t >= 0, or None.

    Precondition: each node box contains the triangles below it, and d is not zero.
    Children are visited near first, and a node whose box starts beyond the best hit is
    skipped. Cost: O(n) node visits and primitive tests in the worst case.
    """
    c = counts if counts is not None else Counts()
    best: tuple[Fraction, int] | None = None
    tmax: Num | float = math.inf  # @line L1
    c.boxes += 1
    t_root = slab_entry(nodes[0].lo, nodes[0].hi, o, d, tmax)  # @line L2
    if t_root is None:
        return None
    stack: list[tuple[int, Fraction]] = [(0, t_root)]  # @line L3
    while stack:  # @line L4
        v, tv = stack.pop()  # @line L5
        if tv > tmax:  # @line L6
            continue
        c.nodes += 1
        c.pops.append(v)
        nd = nodes[v]
        if nd.left < 0:  # @line L7
            for r in refs[nd.first : nd.first + nd.count]:
                c.prims += 1
                t = hit_triangle(tris[r], o, d)
                if t is not None and t <= tmax and (best is None or t < best[0]):  # @line L8
                    best, tmax = (t, r), t
            continue
        a, b = nodes[nd.left], nodes[nd.right]  # @line L9
        c.boxes += 2
        ta = slab_entry(a.lo, a.hi, o, d, tmax)  # @line L10
        tb = slab_entry(b.lo, b.hi, o, d, tmax)
        if ta is not None and tb is not None:  # @line L11
            if ta <= tb:
                stack.append((nd.right, tb))
                stack.append((nd.left, ta))
            else:
                stack.append((nd.left, ta))
                stack.append((nd.right, tb))
        elif ta is not None:  # @line L12
            stack.append((nd.left, ta))
        elif tb is not None:
            stack.append((nd.right, tb))
    return best  # @line L13


def any_hit(
    nodes: list[Node], refs: list[int], tris: list[Tri], o: Vec, d: Vec, tmax: Num | float, counts: Counts | None = None
) -> bool:
    """True if some triangle is hit with 0 <= t <= tmax. Returns at the first such hit; no ordering."""
    c = counts if counts is not None else Counts()
    c.boxes += 1
    if slab_entry(nodes[0].lo, nodes[0].hi, o, d, tmax) is None:
        return False
    stack = [0]
    while stack:
        v = stack.pop()
        c.nodes += 1
        c.pops.append(v)
        nd = nodes[v]
        if nd.left < 0:
            for r in refs[nd.first : nd.first + nd.count]:
                c.prims += 1
                t = hit_triangle(tris[r], o, d)
                if t is not None and t <= tmax:
                    return True
            continue
        for ch in (nd.right, nd.left):
            c.boxes += 1
            if slab_entry(nodes[ch].lo, nodes[ch].hi, o, d, tmax) is not None:
                stack.append(ch)
    return False
