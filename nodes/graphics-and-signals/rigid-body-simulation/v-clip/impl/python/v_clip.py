# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/v-clip/. The authors are listed in prov/D7J6QE.jsonl.

"""V-Clip for two convex polygons in the plane.

A polygon is a list of vertices in counterclockwise order, strictly convex. Its features are
the vertices ("v", i) and the edges ("e", i), where edge i goes from vertex i to vertex i + 1.
The walk is the one of Mirtich's V-Clip in 2D: in a vertex-edge state the edge is clipped
against the Voronoi region of the vertex, and the sign of the derivative of the distance at the
clip points chooses the next feature. A vertex behind an edge goes to the local minimum handler,
which either finds a closer edge or reports penetration. There are no tolerances: with integer or
Fraction input every test is exact, and the walk always ends, after at most (2n)(2m) moves.

The result is either "disjoint" with a closest pair of features and points, or "penetration"
with a pair of features that witness the intersection (touching counts as penetration).
"""

from __future__ import annotations

from dataclasses import dataclass

Feature = tuple[str, int]


@dataclass
class Result:
    status: str  # "disjoint" or "penetration"
    fa: Feature | None  # None for the whole polygon A
    fb: Feature | None
    dist2: object
    pa: tuple | None
    pb: tuple | None
    steps: int


def _sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def _dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def _cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def _point(e0, e1, t):
    return (e0[0] + t * (e1[0] - e0[0]), e0[1] + t * (e1[1] - e0[1]))


def closest_on_segment(p, a, b):
    d = _sub(b, a)
    t = _dot(_sub(p, a), d) / _dot(d, d)
    if t <= 0:
        return a
    if t >= 1:
        return b
    return _point(a, b, t)


def segments_intersect(p1, p2, q1, q2) -> bool:
    d1 = _cross(_sub(q2, q1), _sub(p1, q1))
    d2 = _cross(_sub(q2, q1), _sub(p2, q1))
    d3 = _cross(_sub(p2, p1), _sub(q1, p1))
    d4 = _cross(_sub(p2, p1), _sub(q2, p1))
    if ((d1 > 0 > d2) or (d1 < 0 < d2)) and ((d3 > 0 > d4) or (d3 < 0 < d4)):
        return True

    def on(a, b, c):
        return min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])

    return (
        (d1 == 0 and on(q1, q2, p1))
        or (d2 == 0 and on(q1, q2, p2))
        or (d3 == 0 and on(p1, p2, q1))
        or (d4 == 0 and on(p1, p2, q2))
    )


def _vertex_planes(P, i):
    """The two planes of the Voronoi region of vertex i: (direction to the neighbor, edge index)."""
    n = len(P)
    a = P[i]
    return [(_sub(P[i - 1], a), (i - 1) % n), (_sub(P[(i + 1) % n], a), i)]


def _vertex_violation(P, i, x):
    for u, k in _vertex_planes(P, i):
        if _dot(_sub(x, P[i]), u) > 0:
            return k
    return None


def _signed_key(P, k, x):
    """Has the sign and the order of the signed distance of x to the line of edge k."""
    a, b = P[k], P[(k + 1) % len(P)]
    d = _sub(b, a)
    s = _cross(d, _sub(x, a))
    return -s * abs(s) / _dot(d, d)


def handle_local_min(Q, v):
    """The edge of Q with the largest signed distance to v, or None if v is in Q."""
    k = max(range(len(Q)), key=lambda k: _signed_key(Q, k, v))  # @line L18
    if _signed_key(Q, k, v) <= 0:  # @line L19
        return None
    return k  # @line L20


def clip_edge(P, i, e0, e1):
    """Clip the segment e0e1 against the Voronoi region of vertex i of P.

    Returns (lam_l, lam_u, n_l, n_u, simple) where n_l and n_u are the edges behind the
    clipping planes (or None) and simple is the edge whose plane excludes the whole segment.
    """
    lam_l, lam_u, n_l, n_u = 0, 1, None, None
    a = P[i]
    for u, k in _vertex_planes(P, i):
        f0 = _dot(_sub(e0, a), u)  # > 0 means outside this plane
        f1 = _dot(_sub(e1, a), u)
        if f0 > 0 and f1 > 0:
            return lam_l, lam_u, n_l, n_u, k
        if f0 > 0:
            t = f0 / (f0 - f1)
            if t > lam_l:
                lam_l, n_l = t, k
        elif f1 > 0:
            t = f0 / (f0 - f1)
            if t < lam_u:
                lam_u, n_u = t, k
    return lam_l, lam_u, n_l, n_u, None


def _vertex_edge(P, i, Q, j):
    """One step of the state (vertex i of P, edge j of Q). See V-CLIP lines L10 to L17."""
    m = len(Q)
    v = P[i]
    e0, e1 = Q[j], Q[(j + 1) % m]
    d = _sub(e1, e0)
    if _dot(_sub(v, e0), d) < 0:  # @line L10
        return "edge", ("v", j)
    if _dot(_sub(v, e1), d) > 0:
        return "edge", ("v", (j + 1) % m)
    if _cross(d, _sub(v, e0)) >= 0:  # @line L11
        k = handle_local_min(Q, v)
        if k is None:
            return "penetration", None
        return "edge", ("e", k)
    lam_l, lam_u, n_l, n_u, simple = clip_edge(P, i, e0, e1)  # @line L12
    if simple is not None:  # @line L13
        return "vertex", ("e", simple)
    if lam_l > lam_u:  # @line L14
        return "vertex", ("e", _vertex_violation(P, i, closest_on_segment(v, e0, e1)))
    if n_l is not None and _dot(_sub(_point(e0, e1, lam_l), v), d) > 0:  # @line L15
        return "vertex", ("e", n_l)
    if n_u is not None and _dot(_sub(_point(e0, e1, lam_u), v), d) < 0:  # @line L16
        return "vertex", ("e", n_u)
    return "done", closest_on_segment(v, e0, e1)  # @line L17


def v_clip(A: list, B: list, fa: Feature = ("v", 0), fb: Feature = ("v", 0)) -> Result:
    """Walk from (fa, fb) to a closest pair of features, or to a witness of penetration."""
    limit = 4 * len(A) * len(B) + 1
    steps = 0
    while True:  # @line L1
        steps += 1
        if steps > limit:
            raise RuntimeError("no progress; the input is not strictly convex and counterclockwise")
        if fa[0] == "v" and fb[0] == "v":  # @line L2
            a, b = A[fa[1]], B[fb[1]]
            k = _vertex_violation(A, fa[1], b)  # @line L3
            if k is not None:
                fa = ("e", k)
                continue
            k = _vertex_violation(B, fb[1], a)  # @line L4
            if k is not None:
                fb = ("e", k)
                continue
            d2 = _dot(_sub(a, b), _sub(a, b))  # @line L5
            return Result("disjoint" if d2 > 0 else "penetration", fa, fb, d2, a, b, steps)
        if fa[0] == "e" and fb[0] == "e":  # @line L6
            i, j = fa[1], fb[1]
            a0, a1 = A[i], A[(i + 1) % len(A)]
            b0, b1 = B[j], B[(j + 1) % len(B)]
            if segments_intersect(a0, a1, b0, b1):  # @line L7
                return Result("penetration", fa, fb, 0, None, None, steps)
            cands = []  # @line L8
            for k, p in ((i, a0), ((i + 1) % len(A), a1)):
                c = closest_on_segment(p, b0, b1)
                cands.append((_dot(_sub(p, c), _sub(p, c)), ("v", k), fb))
            for k, p in ((j, b0), ((j + 1) % len(B), b1)):
                c = closest_on_segment(p, a0, a1)
                cands.append((_dot(_sub(p, c), _sub(p, c)), fa, ("v", k)))
            _, fa, fb = cands[min(range(4), key=lambda t: cands[t][0])]
            continue
        vertex_is_a = fa[0] == "v"  # @line L9
        if vertex_is_a:
            kind, f = _vertex_edge(A, fa[1], B, fb[1])
        else:
            kind, f = _vertex_edge(B, fb[1], A, fa[1])
        if kind == "penetration":
            if vertex_is_a:
                return Result("penetration", fa, None, 0, None, None, steps)
            return Result("penetration", None, fb, 0, None, None, steps)
        if kind == "done":
            if vertex_is_a:
                pa, pb = A[fa[1]], f
            else:
                pa, pb = f, B[fb[1]]
            return Result("disjoint", fa, fb, _dot(_sub(pa, pb), _sub(pa, pb)), pa, pb, steps)
        if (kind == "edge") == vertex_is_a:  # the edge side is B when the vertex is in A
            fb = f
        else:
            fa = f
