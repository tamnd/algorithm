# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lin-canny-closest-features/. The authors are listed in prov/PQTB3Y.jsonl.

"""The Lin-Canny closest feature walk for two convex polygons in the plane.

A polygon is a list of vertices in counterclockwise order, strictly convex (no three
consecutive vertices on a line). Its features are the vertices ("v", i) and the edges
("e", i), where edge i goes from vertex i to vertex i + 1. The walk starts from any pair of
features, for example the closest pair of the previous time step, and moves to a
neighboring feature while a Voronoi region test fails. Each move lowers the distance between
the two features, or keeps it and lowers the dimension, so the walk ends after at most
(2n)(2m) moves. With integer or Fraction input all tests are exact.

Precondition of the method: the polygons are disjoint. If they intersect, the walk stops
and reports it (separated is False). It does not compute a penetration depth.
"""

from __future__ import annotations

from dataclasses import dataclass

Point = tuple
Feature = tuple[str, int]


@dataclass
class Result:
    separated: bool
    fa: Feature
    fb: Feature
    dist2: object  # the squared distance, 0 if the polygons intersect
    pa: Point | None  # the closest point on A
    pb: Point | None  # the closest point on B
    steps: int


def _sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def _dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def _cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def closest_on_segment(p, a, b):
    """The point of the segment ab that is closest to p."""
    d = _sub(b, a)
    t = _dot(_sub(p, a), d) / _dot(d, d)
    if t <= 0:
        return a
    if t >= 1:
        return b
    return (a[0] + t * d[0], a[1] + t * d[1])


def segments_intersect(p1, p2, q1, q2) -> bool:
    """Closed segments p1p2 and q1q2 have a common point."""
    d1 = _cross(_sub(q2, q1), _sub(p1, q1))
    d2 = _cross(_sub(q2, q1), _sub(p2, q1))
    d3 = _cross(_sub(p2, p1), _sub(q1, p1))
    d4 = _cross(_sub(p2, p1), _sub(q2, p1))
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    def on(a, b, c):  # c on segment ab, given that a, b, c are collinear
        return min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])

    return (
        (d1 == 0 and on(q1, q2, p1))
        or (d2 == 0 and on(q1, q2, p2))
        or (d3 == 0 and on(p1, p2, q1))
        or (d4 == 0 and on(p1, p2, q2))
    )


def vertex_region_violation(P, i, x):
    """The edge of P behind a plane of the Voronoi region of vertex i that x violates, or None."""
    n = len(P)
    a = P[i]
    if _dot(_sub(x, a), _sub(P[i - 1], a)) > 0:
        return (i - 1) % n
    if _dot(_sub(x, a), _sub(P[(i + 1) % n], a)) > 0:
        return i
    return None


def _signed_key(P, k, x):
    """A number with the sign and the order of the signed distance of x to the line of edge k."""
    a, b = P[k], P[(k + 1) % len(P)]
    d = _sub(b, a)
    s = _cross(d, _sub(x, a))  # > 0 on the inner side for a counterclockwise polygon
    return -s * abs(s) / _dot(d, d)


def _vertex_edge(P, i, Q, j):
    """One step of the state (vertex i of P, edge j of Q).

    Returns ("edge", f) to replace the edge by f, ("vertex", f) to replace the vertex by f,
    ("intersect", None), or ("done", q) with q the closest point of the edge.
    """
    m = len(Q)
    v = P[i]
    e0, e1 = Q[j], Q[(j + 1) % m]
    d = _sub(e1, e0)
    if _dot(_sub(v, e0), d) < 0:  # @line L7
        return "edge", ("v", j)
    if _dot(_sub(v, e1), d) > 0:
        return "edge", ("v", (j + 1) % m)
    if _cross(d, _sub(v, e0)) >= 0:  # @line L8
        k = max(range(m), key=lambda k: _signed_key(Q, k, v))  # @line L9
        if _signed_key(Q, k, v) <= 0:  # @line L10
            return "intersect", None
        return "edge", ("e", k)  # @line L11
    q = closest_on_segment(v, e0, e1)  # @line L12
    k = vertex_region_violation(P, i, q)  # @line L13
    if k is not None:
        return "vertex", ("e", k)
    return "done", q  # @line L14


def lin_canny(A: list, B: list, fa: Feature = ("v", 0), fb: Feature = ("v", 0)) -> Result:
    """Walk from the features (fa, fb) to a closest pair of features of A and B."""
    limit = 4 * len(A) * len(B) + 1
    steps = 0
    while True:  # @line L1
        steps += 1
        if steps > limit:
            raise RuntimeError("no progress; the input is not strictly convex and counterclockwise")
        if fa[0] == "v" and fb[0] == "v":  # @line L2
            a, b = A[fa[1]], B[fb[1]]
            k = vertex_region_violation(A, fa[1], b)  # @line L3
            if k is not None:
                fa = ("e", k)
                continue
            k = vertex_region_violation(B, fb[1], a)  # @line L4
            if k is not None:
                fb = ("e", k)
                continue
            d2 = _dot(_sub(a, b), _sub(a, b))  # @line L5
            return Result(d2 > 0, fa, fb, d2, a, b, steps)
        if fa[0] != fb[0]:  # @line L6
            if fa[0] == "v":
                kind, f = _vertex_edge(A, fa[1], B, fb[1])
                if kind == "edge":
                    fb = f
                elif kind == "vertex":
                    fa = f
            else:
                kind, f = _vertex_edge(B, fb[1], A, fa[1])
                if kind == "edge":
                    fa = f
                elif kind == "vertex":
                    fb = f
            if kind == "intersect":
                return Result(False, fa, fb, 0, None, None, steps)
            if kind == "done":
                pa = A[fa[1]] if fa[0] == "v" else f
                pb = B[fb[1]] if fb[0] == "v" else f
                d2 = _dot(_sub(pa, pb), _sub(pa, pb))
                return Result(d2 > 0, fa, fb, d2, pa, pb, steps)
            continue
        i, j = fa[1], fb[1]
        a0, a1 = A[i], A[(i + 1) % len(A)]
        b0, b1 = B[j], B[(j + 1) % len(B)]
        if segments_intersect(a0, a1, b0, b1):  # @line L15
            return Result(False, fa, fb, 0, None, None, steps)
        cands = []  # @line L16
        for k, p in ((i, a0), ((i + 1) % len(A), a1)):
            c = closest_on_segment(p, b0, b1)
            cands.append((_dot(_sub(p, c), _sub(p, c)), ("v", k), fb))
        for k, p in ((j, b0), ((j + 1) % len(B), b1)):
            c = closest_on_segment(p, a0, a1)
            cands.append((_dot(_sub(p, c), _sub(p, c)), fa, ("v", k)))
        best = min(range(4), key=lambda t: cands[t][0])
        _, fa, fb = cands[best]
