# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/csg-ray-casting/. The authors are listed in prov/K0WQSY.jsonl.

"""Roth's ray casting of a CSG solid, with exact rational ray parameters.

A primitive is a bounded convex polyhedron, given as a list of half-spaces
(a, b) that mean a . x <= b, with a a 3-vector. An inner node is a tuple
(op, left, right) with op in "union", "intersection" and "difference". A ray
is o + t d. Coordinates are int or Fraction.

The result of casting is a sorted list of disjoint closed intervals
(t0, t1), t0 < t1, of the parameter t on the whole line: the regularized
classification of the line against the solid. Intervals of length zero
(a ray that only grazes an edge or a vertex) are dropped.
"""

from fractions import Fraction
from typing import Optional, Sequence, Union

Num = Union[int, Fraction]
Vec3 = tuple[Num, Num, Num]
HalfSpace = tuple[Vec3, Num]
Primitive = list[HalfSpace]
Tree = Union[Primitive, tuple]
Intervals = list[tuple[Fraction, Fraction]]

OPS = {
    "union": lambda a, b: a or b,
    "intersection": lambda a, b: a and b,
    "difference": lambda a, b: a and not b,
}


def _dot(a: Sequence[Num], b: Sequence[Num]) -> Num:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _is_node(tree: Tree) -> bool:
    return isinstance(tree, tuple) and len(tree) == 3 and isinstance(tree[0], str)


def ray_primitive(o: Vec3, d: Vec3, prim: Primitive) -> Intervals:
    """The interval of the line o + t d inside a bounded convex polyhedron."""
    lo: Optional[Fraction] = None
    hi: Optional[Fraction] = None
    for a, b in prim:
        s = _dot(a, d)
        r = b - _dot(a, o)
        if s == 0:
            if r < 0:
                return []  # the line is parallel to the plane and outside it
            continue
        t = Fraction(r) / s
        if s > 0:
            hi = t if hi is None or t < hi else hi
        else:
            lo = t if lo is None or t > lo else lo
    if lo is None or hi is None:
        raise ValueError("the primitive is not bounded along the ray")
    return [(lo, hi)] if lo < hi else []


def _inside(intervals: Intervals, t: Fraction) -> bool:
    return any(t0 < t < t1 for t0, t1 in intervals)


def merge(A: Intervals, B: Intervals, op: str) -> Intervals:
    """Combine two interval lists by a regularized operation on the line."""
    f = OPS[op]
    E = sorted({t for iv in A + B for t in iv})  # @line L5
    out: Intervals = []
    for e0, e1 in zip(E, E[1:]):  # @line L6
        m = (e0 + e1) / 2  # @line L7
        if f(_inside(A, m), _inside(B, m)):
            if out and out[-1][1] == e0:  # @line L8
                out[-1] = (out[-1][0], e1)  # touching pieces join: no interval of length zero between
            else:
                out.append((e0, e1))
    return out


def cast(o: Vec3, d: Vec3, tree: Tree) -> Intervals:
    """The intervals of the line o + t d inside the solid. Cost: O(k log k) per node for k end points."""
    if not _is_node(tree):  # @line L1
        return ray_primitive(o, d, tree)  # @line L2
    op, left, right = tree
    A, B = cast(o, d, left), cast(o, d, right)  # @line L3
    return merge(A, B, op)  # @line L4


def first_hit(o: Vec3, d: Vec3, tree: Tree) -> Optional[Fraction]:
    """The least t >= 0 with o + t d in the solid, or None. It is 0 if o is in the solid."""
    R = cast(o, d, tree)  # @line L9
    for t0, t1 in R:  # @line L10
        if t1 >= 0:
            return max(t0, Fraction(0))  # @line L11
    return None  # @line L12


def box(x0: Num, y0: Num, z0: Num, x1: Num, y1: Num, z1: Num) -> Primitive:
    """The box [x0, x1] x [y0, y1] x [z0, z1] as six half-spaces."""
    return [((1, 0, 0), x1), ((-1, 0, 0), -x0), ((0, 1, 0), y1), ((0, -1, 0), -y0),
            ((0, 0, 1), z1), ((0, 0, -1), -z0)]
