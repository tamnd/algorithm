# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distmesh/. The authors are listed in prov/M30YY9.jsonl.

"""DistMesh in the plane, after Persson and Strang, for a uniform size h0.

The domain is {x : fd(x) <= 0} for a signed distance function fd. Points start
on an equilateral grid, then move by the forces of a truss of repulsive
springs, are projected back onto the boundary when they leave the domain, and
are retriangulated by Delaunay when they have moved far enough. There is no
proof that the iteration stops, so it has an iteration cap.

Positions are floats. Each Delaunay triangulation is computed exactly: the
points are rounded to integers on the grid of step 2**-BITS, and the orientation
and in-circle tests run on Python integers. The returned points are those
rounded points, so the returned triangles are exactly Delaunay for them.
"""

import math
from typing import Callable, Dict, List, Sequence, Tuple

from mg3geom import incircle, orient2d

BITS = 24
Vec = Tuple[float, float]
Tri = Tuple[int, int, int]


def to_int(p: Vec) -> Tuple[int, int]:
    return (round(p[0] * (1 << BITS)), round(p[1] * (1 << BITS)))


def from_int(q: Tuple[int, int]) -> Vec:
    return (q[0] / (1 << BITS), q[1] / (1 << BITS))


def delaunay(pts: Sequence[Tuple[int, int]]) -> List[Tri]:
    """Bowyer-Watson with exact integer predicates. The points must be distinct.
    A large super triangle is used; triangles that touch it are dropped. Every
    returned triangle has an empty circumcircle with respect to all points."""
    n = len(pts)
    if len(set(pts)) != n:
        raise ValueError("two points round to the same grid point")
    span = max(max(abs(c) for c in p) for p in pts) + 1
    big = 64 * span
    P = list(pts) + [(-big, -big), (big, -big), (0, big)]
    tris: Dict[Tri, None] = {(n, n + 1, n + 2): None}
    owner: Dict[Tuple[int, int], Tri] = {(n, n + 1): (n, n + 1, n + 2), (n + 1, n + 2): (n, n + 1, n + 2),
                                         (n + 2, n): (n, n + 1, n + 2)}

    def add(t: Tri):
        tris[t] = None
        a, b, c = t
        owner[(a, b)] = owner[(b, c)] = owner[(c, a)] = t

    def remove(t: Tri):
        del tris[t]
        a, b, c = t
        for e in ((a, b), (b, c), (c, a)):
            if owner.get(e) == t:
                del owner[e]

    for v in range(n):
        p = P[v]
        start = None
        for t in tris:
            a, b, c = t
            if orient2d(P[a], P[b], p) >= 0 and orient2d(P[b], P[c], p) >= 0 and orient2d(P[c], P[a], p) >= 0:
                start = t
                break
        # the cavity: triangles whose circumcircle contains p, grown from start
        bad = {start}
        stack = [start]
        while stack:
            a, b, c = stack.pop()
            for x, y in ((a, b), (b, c), (c, a)):
                u = owner.get((y, x))
                if u is not None and u not in bad and incircle(P[u[0]], P[u[1]], P[u[2]], p) > 0:
                    bad.add(u)
                    stack.append(u)
        boundary = []
        for a, b, c in bad:
            for x, y in ((a, b), (b, c), (c, a)):
                if owner.get((y, x)) not in bad:
                    boundary.append((x, y))
        for t in bad:
            remove(t)
        for x, y in boundary:
            add((x, y, v))
    return [t for t in tris if max(t) < n]


def distmesh(fd: Callable[[Vec], float], h0: float, bbox: Tuple[float, float, float, float],
             pfix: Sequence[Vec] = (), max_iter: int = 1000):
    """Returns (points, triangles, iterations, converged). Parameters as in
    Persson and Strang: Fscale 1.2, deltat 0.2, geps 0.001 h0, ttol 0.1,
    dptol 0.001, and a numerical gradient step sqrt(machine eps) h0."""
    fscale, deltat, geps, ttol, dptol = 1.2, 0.2, 0.001 * h0, 0.1, 0.001
    deps = math.sqrt(2.0 ** -52) * h0
    x0, y0, x1, y1 = bbox
    pts: List[Vec] = []
    j = 0
    while y0 + j * h0 * math.sqrt(3) / 2 <= y1 + 1e-12:  # @line L1
        y = y0 + j * h0 * math.sqrt(3) / 2
        i = 0
        while x0 + (i + (j % 2) / 2) * h0 <= x1 + 1e-12:
            p = (x0 + (i + (j % 2) / 2) * h0, y)
            if fd(p) < geps:  # @line L2
                pts.append(p)
            i += 1
        j += 1
    fixed = [from_int(to_int(p)) for p in pfix]
    nfix = len(fixed)
    pts = fixed + [p for p in pts if all(math.hypot(p[0] - q[0], p[1] - q[1]) > 1e-12 for q in fixed)]
    old = None
    tris: List[Tri] = []
    converged = False
    it = 0
    for it in range(1, max_iter + 1):  # @line L3
        if old is None or max(math.hypot(p[0] - q[0], p[1] - q[1]) for p, q in zip(pts, old)) / h0 > ttol:  # @line L4
            pts = [from_int(to_int(p)) for p in pts]
            old = list(pts)
            tris = [t for t in delaunay([to_int(p) for p in pts])  # @line L5
                    if fd(((pts[t[0]][0] + pts[t[1]][0] + pts[t[2]][0]) / 3,
                           (pts[t[0]][1] + pts[t[1]][1] + pts[t[2]][1]) / 3)) < -geps]
            bars = sorted({(min(a, b), max(a, b)) for t in tris for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0]))})
        lengths = [math.hypot(pts[a][0] - pts[b][0], pts[a][1] - pts[b][1]) for a, b in bars]  # @line L6
        l0 = fscale * math.sqrt(sum(l * l for l in lengths) / len(lengths))
        force = [[0.0, 0.0] for _ in pts]
        for (a, b), l in zip(bars, lengths):
            f = max(l0 - l, 0.0)  # @line L7
            fx, fy = f * (pts[a][0] - pts[b][0]) / l, f * (pts[a][1] - pts[b][1]) / l
            force[a][0] += fx
            force[a][1] += fy
            force[b][0] -= fx
            force[b][1] -= fy
        for k in range(nfix):
            force[k] = [0.0, 0.0]
        pts = [(p[0] + deltat * f[0], p[1] + deltat * f[1]) for p, f in zip(pts, force)]  # @line L8
        new = []
        for k, p in enumerate(pts):
            d = fd(p)
            if d > 0 and k >= nfix:  # @line L9
                gx = (fd((p[0] + deps, p[1])) - d) / deps
                gy = (fd((p[0], p[1] + deps)) - d) / deps
                p = (p[0] - d * gx, p[1] - d * gy)
            new.append(p)
        pts = new
        moves = [deltat * math.hypot(*f) for p, f in zip(pts, force) if fd(p) < -geps]
        if not moves or max(moves) / h0 < dptol:  # @line L10
            converged = True
            break
    pts = [from_int(to_int(p)) for p in pts]  # @line L11
    tris = [t for t in delaunay([to_int(p) for p in pts])
            if fd(((pts[t[0]][0] + pts[t[1]][0] + pts[t[2]][0]) / 3,
                   (pts[t[0]][1] + pts[t[1]][1] + pts[t[2]][1]) / 3)) < -geps]
    return pts, tris, it, converged  # @line L12


def disk(p: Vec) -> float:
    """Signed distance to the unit circle."""
    return math.hypot(p[0], p[1]) - 1.0


def square(p: Vec) -> float:
    """Signed distance function of the square [-1, 1]^2 as in Persson and Strang
    (exact inside, and outside except near the corners)."""
    return -min(min(min(1.0 + p[1], 1.0 - p[1]), 1.0 + p[0]), 1.0 - p[0])
