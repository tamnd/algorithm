# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-delaunay-triangulation/. The authors are listed in prov/CQ85FC.jsonl.

"""Optimal Delaunay triangulation (ODT) smoothing in the plane, after Chen and Xu.

The energy of a triangulation T of a convex polygon is the interpolation error

    E(T) = integral over the polygon of (f_I - f),  f(x) = |x|^2,

where f_I is the piecewise linear interpolant of f on T. On one triangle with
area A and edge lengths l1, l2, l3 the error is A (l1^2 + l2^2 + l3^2) / 12.

One sweep moves each interior vertex toward the minimiser of E over its star
(the area-weighted mean of the circumcentres of its triangles), with
backtracking so that the star stays valid and E goes down, and then restores
the Delaunay property by Lawson flips. Every decision is exact: coordinates are
Fractions on a dyadic grid, and orientation and in-circle tests are exact.
"""

from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

from mg3geom import incircle, orient2d, to_grid

Point = Tuple[Fraction, Fraction]
Tri = Tuple[int, int, int]


def triangle_error(a: Point, b: Point, c: Point) -> Fraction:
    """The L1 error of the linear interpolant of |x|^2 on the triangle abc."""
    s = sum((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for p, q in ((a, b), (b, c), (c, a)))
    return Fraction(orient2d(a, b, c), 2) * s / 12


def energy(points: Sequence[Point], tris: Sequence[Tri]) -> Fraction:
    """E(T), the sum of the triangle errors, exact."""
    return sum((triangle_error(points[i], points[j], points[k]) for i, j, k in tris), Fraction(0))


def _locate(points, tris, p):
    """Index of a triangle that contains p in its closed interior, and the
    number of its edges that p lies on."""
    for t, (i, j, k) in enumerate(tris):
        o = [orient2d(points[i], points[j], p), orient2d(points[j], points[k], p), orient2d(points[k], points[i], p)]
        if min(o) >= 0:
            return t, o
    raise ValueError("point outside the domain")


def lawson_flips(points: Sequence[Point], tris: List[Tri]) -> int:
    """Flip edges that are not locally Delaunay until none is left. Returns the
    number of flips. The triangles are changed in place."""
    flips = 0
    changed = True
    while changed:
        changed = False
        owner: Dict[Tuple[int, int], int] = {}
        for t, (i, j, k) in enumerate(tris):
            owner[(i, j)] = t
            owner[(j, k)] = t
            owner[(k, i)] = t
        for (i, j), t in owner.items():
            u = owner.get((j, i))
            if u is None or u < t:
                continue
            a = [v for v in tris[t] if v not in (i, j)][0]
            b = [v for v in tris[u] if v not in (i, j)][0]
            if incircle(points[i], points[j], points[a], points[b]) > 0:  # @line L9
                # an edge that is not locally Delaunay is always flippable
                tris[t] = (a, i, b)  # @line L10
                tris[u] = (b, j, a)
                flips += 1
                changed = True
                break
    return flips


def delaunay(points: Sequence[Point], n_corners: int) -> List[Tri]:
    """A Delaunay triangulation of the points. points[:n_corners] are the
    corners of a convex polygon in counterclockwise order, and every other
    point lies in the closed polygon."""
    tris: List[Tri] = [(0, k, k + 1) for k in range(1, n_corners - 1)]
    for v in range(n_corners, len(points)):
        t, o = _locate(points, tris, points[v])
        i, j, k = tris[t]
        on = [e for e, s in zip(((i, j), (j, k), (k, i)), o) if s == 0]
        if not on:
            tris[t] = (i, j, v)
            tris.extend([(j, k, v), (k, i, v)])
            continue
        # v lies on the edge (x, y) of triangle t: split t and its neighbour
        x, y = on[0]
        z = [w for w in (i, j, k) if w not in (x, y)][0]
        tris[t] = (x, v, z)
        tris.append((v, y, z))
        for u, tri in enumerate(tris):
            if u != t and y in tri and x in tri:
                w = [q for q in tri if q not in (x, y)][0]
                tris[u] = (y, v, w)
                tris.append((v, x, w))
                break
    lawson_flips(points, tris)
    return tris


def star_energy(x: Point, link: Sequence[Tuple[Point, Point]]) -> Fraction:
    """3 times the part of the integral of f_I that depends on the free vertex x,
    for the star triangles (x, a, b): sum of area * (|x|^2 + |a|^2 + |b|^2)."""
    total = Fraction(0)
    for a, b in link:
        area = Fraction(orient2d(x, a, b), 2)
        total += area * (x[0] ** 2 + x[1] ** 2 + a[0] ** 2 + a[1] ** 2 + b[0] ** 2 + b[1] ** 2)
    return total


def odt_target(link: Sequence[Tuple[Point, Point]]) -> Point:
    """The minimiser of star_energy over x, with the star kept as it is:
    x* = -(1 / (2 |Omega|)) * sum of grad(area) * (|a|^2 + |b|^2).
    It is the area-weighted mean of the circumcentres of the star triangles."""
    omega = Fraction(0)
    gx = Fraction(0)
    gy = Fraction(0)
    for a, b in link:
        omega += Fraction(a[0] * b[1] - a[1] * b[0], 2)   # area of the link polygon
        s = a[0] ** 2 + a[1] ** 2 + b[0] ** 2 + b[1] ** 2
        gx += Fraction(a[1] - b[1], 2) * s
        gy += Fraction(b[0] - a[0], 2) * s
    return (-gx / (2 * omega), -gy / (2 * omega))


def move_vertex(points: List[Point], tris: Sequence[Tri], v: int, bits: int = 20, tries: int = 30) -> bool:
    """Move the free vertex v toward odt_target with backtracking. A move is
    accepted only if every star triangle stays counterclockwise and the star
    energy goes strictly down, both tested exactly. Returns True if v moved."""
    link = []
    for i, j, k in tris:
        if i == v:
            link.append((points[j], points[k]))
        elif j == v:
            link.append((points[k], points[i]))
        elif k == v:
            link.append((points[i], points[j]))
    x = points[v]
    target = odt_target(link)  # @line L4
    e0 = star_energy(x, link)
    t = Fraction(1)
    for _ in range(tries):  # @line L5
        y = (to_grid(float(x[0] + t * (target[0] - x[0])), bits),  # @line L6
             to_grid(float(x[1] + t * (target[1] - x[1])), bits))
        if y != x and all(orient2d(y, a, b) > 0 for a, b in link) and star_energy(y, link) < e0:  # @line L7
            points[v] = y  # @line L8
            return True
        t /= 2
    return False


def odt_smooth(corners: Sequence[Point], others: Sequence[Point], sweeps: int = 10):
    """ODT smoothing of the convex polygon `corners` (counterclockwise). The
    points of `others` lie in the closed polygon; those on its sides stay fixed
    and those inside are free. Returns (points, triangles, energies), where
    energies[s] is E after s sweeps."""
    points: List[Point] = [(Fraction(p[0]), Fraction(p[1])) for p in list(corners) + list(others)]
    nc = len(corners)
    tris = delaunay(points, nc)  # @line L1
    n = len(corners)
    free = [v for v in range(nc, len(points))
            if all(orient2d(corners[s], corners[(s + 1) % n], points[v]) > 0 for s in range(n))]
    energies = [energy(points, tris)]
    for _ in range(sweeps):  # @line L2
        for v in free:  # @line L3
            move_vertex(points, tris, v)
        lawson_flips(points, tris)
        energies.append(energy(points, tris))
    return points, tris, energies  # @line L11
