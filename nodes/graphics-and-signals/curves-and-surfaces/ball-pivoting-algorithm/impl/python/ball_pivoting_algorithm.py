# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ball-pivoting-algorithm/. The authors are listed in prov/S69GHG.jsonl.

"""The ball-pivoting algorithm (Bernardini, Mittleman, Rushmeier, Silva, Taubin 1999).

The input is a list of points with outward unit normals and a ball radius
rho. A triangle is made when a ball of radius rho touches its three points
and contains no other point, with the ball on the side of the normals. The
algorithm finds a seed triangle, then keeps a front of directed boundary
edges and pivots the ball around each one, keeping contact with its two end
points, until it touches a new point. It starts a new seed when the front is
empty. The output triangles are oriented with the normals.
"""

import math
from typing import Optional

Vec = tuple[float, float, float]
EPS = 1e-9


def _sub(p: Vec, q: Vec) -> Vec:
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def _cross(u: Vec, v: Vec) -> Vec:
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def _dot(u: Vec, v: Vec) -> float:
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def ball_center(pa: Vec, pb: Vec, pc: Vec, rho: float) -> Optional[Vec]:
    """Center of the ball of radius rho through pa, pb, pc on the side of the
    normal (pb - pa) x (pc - pa), or None if the circumradius exceeds rho."""
    ab, ac = _sub(pb, pa), _sub(pc, pa)
    n = _cross(ab, ac)
    nn = _dot(n, n)
    if nn < 1e-24:
        return None
    # circumcenter: pa + ((|ac|^2 (n x ab)) + (|ab|^2 (ac x n))) / (2 |n|^2)
    t1 = _cross(n, ab)
    t2 = _cross(ac, n)
    lab, lac = _dot(ab, ab), _dot(ac, ac)
    off = tuple((lac * t1[i] + lab * t2[i]) / (2 * nn) for i in range(3))
    r2 = _dot(off, off)
    if r2 > rho * rho:
        return None
    h = math.sqrt(rho * rho - r2) / math.sqrt(nn)
    return (pa[0] + off[0] + h * n[0], pa[1] + off[1] + h * n[1], pa[2] + off[2] + h * n[2])


class _Grid:
    """Uniform grid of cell size 2 rho for neighbor queries."""

    def __init__(self, pts: list[Vec], size: float):
        self.pts, self.size = pts, size
        self.cells: dict[tuple[int, int, int], list[int]] = {}
        for i, p in enumerate(pts):
            self.cells.setdefault(self._key(p), []).append(i)

    def _key(self, p: Vec) -> tuple[int, int, int]:
        return (math.floor(p[0] / self.size), math.floor(p[1] / self.size), math.floor(p[2] / self.size))

    def near(self, p: Vec, r: float) -> list[int]:
        kx, ky, kz = self._key(p)
        out = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for i in self.cells.get((kx + dx, ky + dy, kz + dz), ()):
                        d = _sub(self.pts[i], p)
                        if _dot(d, d) <= r * r:
                            out.append(i)
        return out


def ball_pivoting(pts: list[Vec], normals: list[Vec], rho: float) -> list[tuple[int, int, int]]:
    """Return the triangles (i, j, k), counterclockwise seen from the normals.

    Every output triangle has an empty ball of radius rho through its three
    points (no point strictly inside), on the side of the normals, so it is
    a face of the alpha shape of the points with alpha = rho. Each directed
    edge is used at most once, so every edge is in at most two triangles.
    """
    grid = _Grid(pts, 2 * rho)
    used = [False] * len(pts)
    edges: set[tuple[int, int]] = set()       # directed edges of the output triangles
    front: dict[tuple[int, int], int] = {}    # open edge (i, j) -> the third vertex of its triangle
    open_at = [0] * len(pts)                  # number of open edges at each vertex
    tris: list[tuple[int, int, int]] = []

    def empty(c: Vec, skip: tuple[int, ...]) -> bool:
        return all(i in skip or _dot(_sub(pts[i], c), _sub(pts[i], c)) >= rho * rho - EPS
                   for i in grid.near(c, rho))

    def agrees(a: int, b: int, c: int) -> bool:
        n = _cross(_sub(pts[b], pts[a]), _sub(pts[c], pts[a]))
        return all(_dot(n, normals[v]) > 0 for v in (a, b, c))

    def add_triangle(a: int, b: int, c: int) -> None:
        tris.append((a, b, c))
        for v in (a, b, c):
            used[v] = True
        for u, v, w in ((a, b, c), (b, c, a), (c, a, b)):
            edges.add((u, v))
            if (v, u) in front:            # glue: the edge now has its second triangle
                del front[(v, u)]
                open_at[u] -= 1
                open_at[v] -= 1
            else:
                front[(u, v)] = w
                open_at[u] += 1
                open_at[v] += 1

    next_seed = [0]  # a point that failed as a seed fails again later, as fewer points are unused

    def find_seed() -> Optional[tuple[int, int, int]]:
        for a in range(next_seed[0], len(pts)):  # @line L2
            next_seed[0] = a
            if used[a]:
                continue
            # the other two points may be used, but then they must be on the front
            nb = sorted((i for i in grid.near(pts[a], 2 * rho) if i != a and (not used[i] or open_at[i] > 0)),
                        key=lambda i: _dot(_sub(pts[i], pts[a]), _sub(pts[i], pts[a])))
            for x in range(len(nb)):
                for y in range(x + 1, len(nb)):
                    b, c = nb[x], nb[y]
                    if not agrees(a, b, c):
                        b, c = c, b
                        if not agrees(a, b, c):
                            continue
                    if (b, c) in edges:
                        continue
                    ctr = ball_center(pts[a], pts[b], pts[c], rho)
                    if ctr is not None and empty(ctr, (a, b, c)):  # @line L3
                        return (a, b, c)
        return None

    def pivot(i: int, j: int, o: int) -> Optional[tuple[int, Vec]]:
        """Rotate the ball of triangle (i, j, o) about the edge i -> j; return the first point hit."""
        pi, pj = pts[i], pts[j]
        c0 = ball_center(pi, pj, pts[o], rho)
        m = tuple((pi[t] + pj[t]) / 2 for t in range(3))
        e = _sub(pj, pi)
        u = tuple(x / math.sqrt(_dot(e, e)) for x in e)
        a = _sub(c0, m)
        best: Optional[tuple[float, int, Vec]] = None
        for k in grid.near(m, 2 * rho):  # @line L7
            if k in (i, j, o):
                continue
            ck = ball_center(pj, pi, pts[k], rho)  # the ball of the new triangle (j, i, k)
            if ck is None:
                continue
            b = _sub(ck, m)
            theta = math.atan2(_dot(u, _cross(a, b)), _dot(a, b)) % (2 * math.pi)  # @line L8
            if theta < 1e-12:
                continue
            if best is None or theta < best[0]:
                best = (theta, k, ck)
        return None if best is None else (best[1], best[2])

    while True:
        seed = find_seed()  # @line L1
        if seed is None:  # @line L4
            break
        add_triangle(*seed)
        a, b, c = seed
        stack = [x for x in ((a, b), (b, c), (c, a)) if x in front]
        while stack:  # @line L5
            i, j = stack.pop()
            if (i, j) not in front:
                continue
            o = front[(i, j)]
            hit = pivot(i, j, o)  # @line L6
            if hit is None:
                continue  # a boundary edge: it stays open
            k, ck = hit
            ok = (not used[k] or open_at[k] > 0) and (i, k) not in edges and (k, j) not in edges  # @line L9
            if ok and agrees(j, i, k) and empty(ck, (i, j, k)):
                add_triangle(j, i, k)  # @line L10
                stack.extend(x for x in ((i, k), (k, j)) if x in front)  # @line L11
    return tris  # @line L12
