# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-evaluation/. The authors are listed in prov/G7ANN6.jsonl.

"""Boundary evaluation of a CSG solid by generate and classify, with exact arithmetic.

A primitive is a bounded convex polyhedron with nonempty interior, given as a
list of half-spaces (a, b) that mean a . x <= b. An inner node of the tree is
a tuple (op, left, right) with op in "union", "intersection" and "difference",
and the operations are the regularized ones. Coordinates are int or Fraction.

The result is a list of planar convex polygons, each a list of 3D points in
counterclockwise order seen from outside the solid (the right-hand rule gives
the outward normal). The polygons cover the boundary of the solid, and their
relative interiors are disjoint. Coplanar neighbors are not merged into one
face, and no adjacency is built: that is the job of a B-rep structure.
"""

from fractions import Fraction
from functools import cmp_to_key
from typing import Union

Num = Union[int, Fraction]
Vec = tuple
HalfSpace = tuple
Polygon = list

OPS = {
    "union": lambda a, b: a or b,
    "intersection": lambda a, b: a and b,
    "difference": lambda a, b: a and not b,
}


def dot(a: Vec, b: Vec) -> Num:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def is_node(tree) -> bool:
    return isinstance(tree, tuple) and len(tree) == 3 and isinstance(tree[0], str)


def primitives(tree) -> list:
    """The leaves of the tree, left to right. Their positions are the primitive indices."""
    return primitives(tree[1]) + primitives(tree[2]) if is_node(tree) else [tree]


def _solve3(p: HalfSpace, q: HalfSpace, r: HalfSpace):
    """The common point of three planes, or None if they do not meet in one point (Cramer)."""
    (a1, b1), (a2, b2), (a3, b3) = p, q, r
    c23 = cross(a2, a3)
    det = dot(a1, c23)
    if det == 0:
        return None
    c31, c12 = cross(a3, a1), cross(a1, a2)
    return tuple(Fraction(b1 * c23[k] + b2 * c31[k] + b3 * c12[k]) / det for k in range(3))


def _same_plane(p: HalfSpace, q: HalfSpace) -> bool:
    (a, b), (c, e) = p, q
    return cross(a, c) == (0, 0, 0) and dot(a, c) > 0 and b * dot(c, c) == e * dot(a, c)


def convex_faces(prim: list) -> list:
    """The faces of a convex polyhedron as (polygon, outward normal), counterclockwise from outside."""
    faces = []
    for i, (a, b) in enumerate(prim):
        if any(_same_plane((a, b), prim[j]) for j in range(i)):
            continue
        pts = set()
        others = [h for j, h in enumerate(prim) if j != i]
        for j in range(len(others)):
            for k in range(j + 1, len(others)):
                x = _solve3((a, b), others[j], others[k])
                if x is not None and all(dot(c, x) <= e for c, e in prim):
                    pts.add(x)
        if len(pts) < 3:
            continue
        poly = _sort_ccw(list(pts), a)
        if _area_vector(poly) != (0, 0, 0):
            faces.append((poly, a))
    return faces


def _sort_ccw(pts: list, n: Vec) -> list:
    """Sort coplanar points of a convex polygon counterclockwise around the normal n."""
    m = len(pts)
    c = tuple(sum(p[k] for p in pts) / Fraction(m) for k in range(3))
    u = sub(pts[0], c)
    v = cross(n, u)

    def half(p):
        w = sub(p, c)
        y, x = dot(w, v), dot(w, u)
        return 0 if (y > 0 or (y == 0 and x > 0)) else 1

    def cmp(p, q):
        hp, hq = half(p), half(q)
        if hp != hq:
            return hp - hq
        s = dot(cross(sub(p, c), sub(q, c)), n)
        return -1 if s > 0 else (1 if s < 0 else 0)

    return sorted(pts, key=cmp_to_key(cmp))


def _area_vector(poly: Polygon) -> Vec:
    """Twice the vector area of a planar polygon (Newell)."""
    s = (0, 0, 0)
    for k in range(len(poly)):
        p, q = poly[k], poly[(k + 1) % len(poly)]
        s = tuple(s[t] + w for t, w in enumerate(cross(p, q)))
    return s


def split(poly: Polygon, a: Vec, b: Num) -> list:
    """Cut a convex polygon by the plane a . x = b. Returns the parts of positive area (one or two)."""
    vals = [dot(a, p) - b for p in poly]
    if all(v >= 0 for v in vals) or all(v <= 0 for v in vals):
        return [poly]
    lo, hi = [], []
    for k in range(len(poly)):
        p, q = poly[k], poly[(k + 1) % len(poly)]
        vp, vq = vals[k], vals[(k + 1) % len(poly)]
        if vp <= 0:
            lo.append(p)
        if vp >= 0:
            hi.append(p)
        if (vp < 0 < vq) or (vq < 0 < vp):
            t = Fraction(vp) / (vp - vq)
            x = tuple(p[i] + t * (q[i] - p[i]) for i in range(3))
            lo.append(x)
            hi.append(x)
    return [part for part in (lo, hi) if len(part) >= 3]


def side_member(prim: list, c: Vec, n: Vec, s: int) -> bool:
    """Is c + s*eps*n inside the primitive, for every small enough eps > 0?"""
    for a, b in prim:
        v = dot(a, c) - b
        if v > 0 or (v == 0 and s * dot(a, n) >= 0):
            return False
    return True


def on_boundary(prim: list, c: Vec) -> bool:
    vals = [dot(a, c) - b for a, b in prim]
    return all(v <= 0 for v in vals) and any(v == 0 for v in vals)


def evaluate(tree, leaf_value) -> bool:
    """The Boolean formula of the tree, with leaf_value(k) for the k-th primitive."""
    counter = [0]

    def go(t):
        if not is_node(t):
            counter[0] += 1
            return leaf_value(counter[0] - 1)
        op, l, r = t
        x = go(l)
        y = go(r)
        return OPS[op](x, y)

    return go(tree)


def boundary_evaluation(tree) -> list:
    """The oriented boundary polygons of the regularized solid of a CSG tree."""
    prims = primitives(tree)
    K = []  # @line L1
    for i, P in enumerate(prims):  # @line L2
        for f, n in convex_faces(P):
            Q = [f]  # @line L3
            for j, Pj in enumerate(prims):  # @line L4
                if j == i:
                    continue
                for a, b in Pj:
                    Q = [part for g in Q for part in split(g, a, b)]  # @line L5
            for g in Q:  # @line L6
                c = tuple(sum(p[k] for p in g) / Fraction(len(g)) for k in range(3))  # @line L7
                if any(on_boundary(prims[j], c) for j in range(i)):  # @line L8
                    continue  # a coplanar copy, kept from the primitive of least index
                front = evaluate(tree, lambda k: side_member(prims[k], c, n, +1))  # @line L9
                back = evaluate(tree, lambda k: side_member(prims[k], c, n, -1))
                if back and not front:  # @line L10
                    K.append(g)
                elif front and not back:  # @line L11
                    K.append(g[::-1])
    return K  # @line L12


def volume(faces: list) -> Fraction:
    """The volume enclosed by closed oriented polygons, by the divergence theorem."""
    six_v = Fraction(0)
    for poly in faces:
        for k in range(1, len(poly) - 1):
            six_v += dot(poly[0], cross(poly[k], poly[k + 1]))
    return six_v / 6


def box(x0: Num, y0: Num, z0: Num, x1: Num, y1: Num, z1: Num) -> list:
    """The box [x0, x1] x [y0, y1] x [z0, z1] as six half-spaces."""
    return [((1, 0, 0), x1), ((-1, 0, 0), -x0), ((0, 1, 0), y1), ((0, -1, 0), -y0),
            ((0, 0, 1), z1), ((0, 0, -1), -z0)]
