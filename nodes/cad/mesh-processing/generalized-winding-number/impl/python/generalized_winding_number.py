# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-winding-number/. The authors are listed in prov/CVGJTP.jsonl.

"""Generalized winding number of a triangle mesh (Jacobson, Kavan and Sorkine-Hornung 2013).

w(p) = (1 / 4 pi) * sum over triangles of the signed solid angle of the
triangle seen from p. Faces are oriented so that the outward normal follows
the right-hand rule, so w = 1 inside and w = 0 outside a closed mesh.

The solid angle uses the formula of Van Oosterom and Strackee (1983): with
a, b, c the corners minus p and |a|, |b|, |c| their lengths,

    tan(Omega / 2) = det[a b c] / (|a||b||c| + (a.b)|c| + (a.c)|b| + (b.c)|a|).

The tree version groups faces into patches with a bounding box. For a query
outside the box of a patch, the patch has the same winding number as a fan
over its boundary loops, which has fewer triangles.

The evaluation is in floating point. exact_ray_winding is an exact
reference: a signed count of ray crossings in rational arithmetic.
"""

import math
import random
from fractions import Fraction

from mp3geom import cross, dot, sub


def solid_angle(a, b, c, p):
    """Signed solid angle of the triangle abc seen from p, in (-2 pi, 2 pi)."""
    a, b, c = (tuple(float(x) - float(y) for x, y in zip(q, p)) for q in (a, b, c))
    la, lb, lc = (math.sqrt(dot(q, q)) for q in (a, b, c))
    det = dot(a, cross(b, c))  # @line L3
    den = la * lb * lc + dot(a, b) * lc + dot(a, c) * lb + dot(b, c) * la  # @line L4
    return 2 * math.atan2(det, den)  # @line L5


def winding_number(points, faces, p):
    """Direct sum over all faces."""
    total = 0.0  # @line L1
    for f in faces:  # @line L2
        total += solid_angle(points[f[0]], points[f[1]], points[f[2]], p)
    return total / (4 * math.pi)  # @line L6


def boundary_edges(faces):
    """Directed edges (i, j) of the faces whose reverse (j, i) is not an edge of the faces, with multiplicity."""
    count = {}
    for f in faces:
        for k in range(3):
            e = (f[k], f[(k + 1) % 3])
            count[e] = count.get(e, 0) + 1
    out = []
    for (i, j), m in count.items():
        net = m - count.get((j, i), 0)
        out += [(i, j)] * max(net, 0)
    return out


class Node:
    __slots__ = ("lo", "hi", "faces", "children", "cap")


def build_tree(points, faces, leaf_size=8):
    """A tree of patches with bounding boxes and closing fans."""

    def make(ids):
        node = Node()
        pts = [points[v] for i in ids for v in faces[i]]
        node.lo = tuple(min(float(q[k]) for q in pts) for k in range(3))
        node.hi = tuple(max(float(q[k]) for q in pts) for k in range(3))
        node.faces = ids
        node.children = []
        edges = boundary_edges([faces[i] for i in ids])
        node.cap = None
        if edges:
            centre = edges[0][0]
            node.cap = [(centre, i, j) for i, j in edges if centre not in (i, j)]
        else:
            node.cap = []
        if len(ids) > leaf_size:
            axis = max(range(3), key=lambda k: node.hi[k] - node.lo[k])
            key = lambda i: sum(float(points[v][axis]) for v in faces[i])
            s = sorted(ids, key=key)
            half = len(s) // 2
            node.children = [make(s[:half]), make(s[half:])]
        return node

    return make(list(range(len(faces))))


def winding_number_tree(points, faces, tree, p):
    """The same value as winding_number, with closing fans for patches whose box does not contain p."""
    q = tuple(float(x) for x in p)
    stack, total = [tree], 0.0
    while stack:
        node = stack.pop()
        inside = all(node.lo[k] <= q[k] <= node.hi[k] for k in range(3))
        if not inside and len(node.cap) < len(node.faces):
            for f in node.cap:
                total += solid_angle(points[f[0]], points[f[1]], points[f[2]], p)
        elif node.children:
            stack.extend(node.children)
        else:
            for i in node.faces:
                f = faces[i]
                total += solid_angle(points[f[0]], points[f[1]], points[f[2]], p)
    return total / (4 * math.pi)


def exact_ray_winding(points, faces, p, rng=None):
    """Exact winding number of a closed mesh at p (not on the mesh), by a signed ray crossing count.

    A ray from p in a random rational direction d crosses a triangle with
    normal n; the crossing counts sign(d . n). If the ray hits an edge, a
    vertex or lies in the plane of a triangle, another direction is tried.
    """
    rng = rng or random.Random(0)
    p = tuple(Fraction(x) for x in p)
    while True:
        d = tuple(Fraction(rng.randint(-10**6, 10**6), 10**6) for _ in range(3))
        if d == (0, 0, 0):
            continue
        total, ok = 0, True
        for f in faces:
            a, b, c = (tuple(Fraction(x) for x in points[v]) for v in f)
            e1, e2 = sub(b, a), sub(c, a)
            n = cross(e1, e2)
            den = dot(d, n)
            if den == 0:
                if dot(sub(p, a), n) == 0:
                    ok = False
                    break
                continue
            t = dot(sub(a, p), n) / den
            if t < 0:
                continue
            x = tuple(pi + t * di for pi, di in zip(p, d))
            # barycentric signs of x in abc, by the orientation of sub-triangles against n
            s = [dot(cross(sub(v, x), sub(w, x)), n) for v, w in ((b, c), (c, a), (a, b))]
            if t == 0:
                if all(v >= 0 for v in s):
                    raise ValueError("p is on the mesh")
                continue
            if any(v == 0 for v in s):
                ok = False
                break
            if all(v > 0 for v in s):
                total += 1 if den > 0 else -1
        if ok:
            return total
