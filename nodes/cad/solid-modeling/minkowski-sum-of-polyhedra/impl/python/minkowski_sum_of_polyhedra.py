# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minkowski-sum-of-polyhedra/. The authors are listed in prov/EBNP81.jsonl.

"""The Minkowski sum of two convex polytopes in R^3, by support faces.

The facets of P + Q have the outer normals of the facets of P, the outer
normals of the facets of Q, and the normals e x f of pairs of non-parallel
edges e of P and f of Q whose Gauss arcs cross. For each candidate normal u
the face of the sum in direction u is F(P, u) + F(Q, u), so a candidate is
a facet exactly when that sum spans a plane. This is the step that the
Gaussian map overlay of Fogel and Halperin does in one sweep; here every
candidate is tested with the support function.

All arithmetic is on Python integers, so every sign is exact. The polytopes
are given as finite point sets with integer coordinates whose convex hull is
three-dimensional; points that are not vertices are allowed.

Cost: O(F_P + F_Q + E_P E_Q) candidates, each tested in O(n + m) time, where
n and m are the input sizes. Finding the facets and edges of the inputs from
point sets takes O(n^4) and O(m^4) time by brute force; a B-rep would give
them directly.
"""

from __future__ import annotations

from math import gcd
from typing import Iterable, Sequence

Vec = tuple[int, int, int]


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def dot(a: Vec, b: Vec) -> int:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def primitive(u: Vec) -> Vec:
    g = gcd(gcd(abs(u[0]), abs(u[1])), abs(u[2]))
    return (u[0] // g, u[1] // g, u[2] // g)


def support(points: Sequence[Vec], u: Vec) -> int:
    """h(u) = max of u . x over the points."""
    return max(dot(u, p) for p in points)


def face(points: Sequence[Vec], u: Vec) -> list[Vec]:
    """F(P, u): the points of P that attain h_P(u)."""
    h = support(points, u)
    return [p for p in points if dot(u, p) == h]


def affine_dim(points: Sequence[Vec]) -> int:
    """The dimension of the affine hull of a nonempty point set."""
    o = points[0]
    vs = [sub(p, o) for p in points[1:] if p != o]
    if not vs:
        return 0
    a = vs[0]
    b = next((v for v in vs if cross(a, v) != (0, 0, 0)), None)
    if b is None:
        return 1
    n = cross(a, b)
    return 3 if any(dot(n, v) != 0 for v in vs) else 2


def facet_normals(points: Sequence[Vec]) -> set[Vec]:
    """The primitive outer normals of the facets of conv(points). O(n^4)."""
    pts = list(dict.fromkeys(points))
    out: set[Vec] = set()
    k = len(pts)
    for i in range(k):
        for j in range(i + 1, k):
            for l in range(j + 1, k):
                n = cross(sub(pts[j], pts[i]), sub(pts[l], pts[i]))
                if n == (0, 0, 0):
                    continue
                n = primitive(n)
                c = dot(n, pts[i])
                s = [dot(n, p) - c for p in pts]
                if all(v <= 0 for v in s):
                    out.add(n)
                elif all(v >= 0 for v in s):
                    out.add((-n[0], -n[1], -n[2]))
    return out


def edge_directions(points: Sequence[Vec], normals: Iterable[Vec]) -> list[Vec]:
    """The directions of the edges of conv(points): for two facet normals
    u1, u2 the face F(P, u1 + u2) is the common edge when the facets are
    adjacent. O(F^2 n)."""
    ns = list(normals)
    out: set[Vec] = set()
    for i in range(len(ns)):
        for j in range(i + 1, len(ns)):
            w = add(ns[i], ns[j])
            if w == (0, 0, 0):
                continue
            f = face(points, w)
            if affine_dim(f) == 1:
                a = min(f)
                b = max(f)
                out.add(primitive(sub(b, a)))
    return sorted(out)


def hull_2d_in_plane(points: Sequence[Vec], u: Vec) -> list[Vec]:
    """The vertices of the convex polygon conv(points), which lie in a plane
    with normal u, in counterclockwise order seen from the side u points to."""
    pts = sorted(set(points))
    # drop the coordinate where u is largest, project, take the hull
    k = max(range(3), key=lambda i: abs(u[i]))
    ax = [i for i in range(3) if i != k]

    def pr(p: Vec) -> tuple[int, int]:
        return (p[ax[0]], p[ax[1]])

    def turn(o: Vec, a: Vec, b: Vec) -> int:
        oo, aa, bb = pr(o), pr(a), pr(b)
        return (aa[0] - oo[0]) * (bb[1] - oo[1]) - (aa[1] - oo[1]) * (bb[0] - oo[0])

    pts.sort(key=pr)
    if len(pts) <= 2:
        return pts
    lower: list[Vec] = []
    for p in pts:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[Vec] = []
    for p in reversed(pts):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    # the projection keeps orientation when u[k] > 0 for the cyclic axes
    sign = u[k] if k != 1 else -u[k]
    if sign < 0:
        hull.reverse()
    return hull


def minkowski_sum_convex(P: Sequence[Vec], Q: Sequence[Vec]) -> dict[Vec, list[Vec]]:
    """The facets of conv(P) + conv(Q): a map from each primitive outer
    normal to the vertex cycle of the facet. Precondition: both hulls are
    three-dimensional and all coordinates are integers."""
    fp, fq = facet_normals(P), facet_normals(Q)
    cand: set[Vec] = set(fp) | set(fq)  # @line L1
    for e in edge_directions(P, fp):  # @line L2
        for f in edge_directions(Q, fq):
            c = cross(e, f)
            if c != (0, 0, 0):
                c = primitive(c)  # @line L3
                cand.add(c)
                cand.add((-c[0], -c[1], -c[2]))
    facets: dict[Vec, list[Vec]] = {}  # @line L4
    for u in sorted(cand):  # @line L5
        a, b = face(P, u), face(Q, u)  # @line L6
        s = [add(x, y) for x in a for y in b]
        if affine_dim(s) == 2:  # @line L7
            facets[u] = hull_2d_in_plane(s, u)  # @line L8
    return facets  # @line L9


def vertices_of(facets: dict[Vec, list[Vec]]) -> set[Vec]:
    return {v for cyc in facets.values() for v in cyc}


def euler_characteristic(facets: dict[Vec, list[Vec]]) -> int:
    """V - E + F of the boundary given by the facet cycles."""
    edges = set()
    for cyc in facets.values():
        for i in range(len(cyc)):
            a, b = cyc[i], cyc[(i + 1) % len(cyc)]
            edges.add((min(a, b), max(a, b)))
    return len(vertices_of(facets)) - len(edges) + len(facets)
