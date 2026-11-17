# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-convex-decomposition/. The authors are listed in prov/1SYCDG.jsonl.

"""Approximate convex decomposition of a simple polygon, in exact rational arithmetic.

The concavity of a vertex is its distance to the bridge of its pocket: the convex hull edge that
spans the chain of the polygon that holds the vertex. Hull vertices have concavity 0. The
concavity of a polygon is the largest concavity of its vertices.

While a piece has a concavity above the tolerance tau, the code cuts its reflex vertex of
largest concavity. The cut extends one of the two edges at that vertex beyond it, to the first
point where it meets the boundary, and the code keeps the shorter of the two cuts. This cut
rule is a choice of this page. The paper of Lien and Amato picks the cut by a score.

All coordinates are Fractions, so the areas, the hulls, the cuts and the comparisons with tau are
exact. Distances are compared as squares.
"""

from __future__ import annotations

import math
from fractions import Fraction

Point = tuple


def _pt(p) -> Point:
    return (Fraction(p[0]), Fraction(p[1]))


def cross(o: Point, a: Point, b: Point):
    """The z part of (a - o) x (b - o): positive for a left turn o, a, b."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def area2(P: list) -> Fraction:
    """Twice the signed area of the polygon P, positive if P is counterclockwise."""
    n = len(P)
    return sum((P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1] for i in range(n)), Fraction(0))


def convex_hull(points: list) -> list:
    """Andrew's monotone chain: the hull vertices in counterclockwise order, without collinear points."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower: list = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def is_reflex(P: list, i: int) -> bool:
    n = len(P)
    return cross(P[i - 1], P[i], P[(i + 1) % n]) < 0


def reflex_count(P: list) -> int:
    return sum(is_reflex(P, i) for i in range(len(P)))


def seg_dist2(p: Point, a: Point, b: Point) -> Fraction:
    """The squared distance of p to the segment ab."""
    ab = (b[0] - a[0], b[1] - a[1])
    ap = (p[0] - a[0], p[1] - a[1])
    L = ab[0] * ab[0] + ab[1] * ab[1]
    t = (ap[0] * ab[0] + ap[1] * ab[1]) / L if L else Fraction(0)
    t = min(max(t, Fraction(0)), Fraction(1))
    dx, dy = ap[0] - t * ab[0], ap[1] - t * ab[1]
    return dx * dx + dy * dy


def vertex_concavities(P: list) -> list:
    """The squared concavity of each vertex of the counterclockwise simple polygon P."""
    n = len(P)
    hull = set(convex_hull(P))
    idx = [i for i in range(n) if P[i] in hull]
    conc = [Fraction(0)] * n
    for k, a in enumerate(idx):
        b = idx[(k + 1) % len(idx)]
        j = (a + 1) % n
        while j != b:  # the pocket between the hull vertices a and b, with the bridge P[a] P[b]
            conc[j] = seg_dist2(P[j], P[a], P[b])
            j = (j + 1) % n
    return conc


def concavity(P: list) -> float:
    """The concavity of the polygon P (a float, the square root of the exact square)."""
    P = normalize(P)
    return math.sqrt(max(vertex_concavities(P)))


def normalize(P: list) -> list:
    """Fractions, counterclockwise, and no vertex with a straight angle."""
    P = [_pt(p) for p in P]
    if area2(P) < 0:
        P.reverse()
    changed = True
    while changed and len(P) > 3:
        changed = False
        for i in range(len(P)):
            if cross(P[i - 1], P[i], P[(i + 1) % len(P)]) == 0:
                del P[i]
                changed = True
                break
    return P


def first_hit(P: list, i: int, d: Point):
    """The first point where the ray from P[i] in the direction d meets an edge not at P[i].

    Returns (q, j, u): the point, the index j of the edge P[j] P[j+1], and the parameter u of q on it.
    """
    n = len(P)
    r = P[i]
    best = None
    for j in range(n):
        if j == i or (j + 1) % n == i:
            continue
        a, b = P[j], P[(j + 1) % n]
        e = (b[0] - a[0], b[1] - a[1])
        ar = (a[0] - r[0], a[1] - r[1])
        den = d[0] * e[1] - d[1] * e[0]
        cands = []
        if den != 0:
            s = (ar[0] * e[1] - ar[1] * e[0]) / den
            u = (ar[0] * d[1] - ar[1] * d[0]) / den
            if s > 0 and 0 <= u <= 1:
                cands.append((s, u))
        elif ar[0] * d[1] - ar[1] * d[0] == 0:  # the edge is on the line of the ray
            dd = d[0] * d[0] + d[1] * d[1]
            for u, x in ((Fraction(0), a), (Fraction(1), b)):
                s = ((x[0] - r[0]) * d[0] + (x[1] - r[1]) * d[1]) / dd
                if s > 0:
                    cands.append((s, u))
        for s, u in cands:
            if best is None or s < best[0]:
                best = (s, j, u)
    s, j, u = best
    q = (r[0] + s * d[0], r[1] + s * d[1])
    return q, j, u


def _chain(V: list, a: int, b: int) -> list:
    out = [V[a]]
    k = a
    while k != b:
        k = (k + 1) % len(V)
        out.append(V[k])
    return out


def split(P: list, i: int, q: Point, j: int, u: Fraction):
    """Split P along the segment from P[i] to q, where q is on the edge P[j] P[j+1] at the parameter u."""
    n = len(P)
    V = list(P)
    if u == 0:
        k = j
    elif u == 1:
        k = (j + 1) % n
    else:
        V.insert(j + 1, q)
        k = j + 1
        if k <= i:
            i += 1
    return normalize(_chain(V, i, k)), normalize(_chain(V, k, i))


def best_cut(P: list, i: int):
    """The shorter of the two cuts that extend an edge at the reflex vertex P[i] beyond it."""
    n = len(P)
    r, prev, nxt = P[i], P[i - 1], P[(i + 1) % n]
    best = None
    for d in ((r[0] - prev[0], r[1] - prev[1]), (r[0] - nxt[0], r[1] - nxt[1])):
        q, j, u = first_hit(P, i, d)
        L = (q[0] - r[0]) ** 2 + (q[1] - r[1]) ** 2
        if best is None or L < best[0]:
            best = (L, q, j, u)
    return best[1:]


def approximate_convex_decomposition(P: list, tau) -> list:
    """Pieces of the simple polygon P, each with a concavity of at most tau.

    The pieces are counterclockwise lists of Fraction points. Their interiors are disjoint and
    their union is P. With tau = 0 the pieces are convex.
    """
    tau2 = Fraction(tau) ** 2
    queue = [normalize(P)]  # @line L1
    done: list = []
    while queue:  # @line L2
        X = queue.pop()  # @line L3
        conc = vertex_concavities(X)  # @line L4
        if max(conc) <= tau2:  # @line L5
            done.append(X)
            continue
        i = max((k for k in range(len(X)) if is_reflex(X, k)), key=lambda k: (conc[k], -k))  # @line L6
        q, j, u = best_cut(X, i)  # @line L7
        A, B = split(X, i, q, j, u)  # @line L8
        assert reflex_count(A) + reflex_count(B) < reflex_count(X)
        queue += [B, A]
    return done  # @line L9
