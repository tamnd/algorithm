# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-contouring/. The authors are listed in prov/B0HXQ1.jsonl.

"""Dual contouring of Hermite data on a uniform grid (Ju, Losasso, Schaefer, Warren 2002).

The input is a function f and its gradient, sampled on the grid points
origin + h * (i, j, k), 0 <= i, j, k <= n. A point is inside when f < c.
Hermite data is computed for each grid edge with a sign change: the point
where f = c (by bisection) and the unit normal there (the normalized
gradient). Each cell with such an edge gets one vertex, the minimizer of
the quadratic error function (QEF) sum (n_i . (x - p_i))^2 that is closest to
the mass point of the p_i, with small singular values truncated. Each
interior edge with a sign change gives one quadrilateral that joins the
vertices of the four cells around it.
"""

import math
from typing import Callable

Vec = tuple[float, float, float]
Field = Callable[[float, float, float], float]
Grad = Callable[[float, float, float], Vec]


def _jacobi_eigen(m: list[list[float]]) -> tuple[list[float], list[list[float]]]:
    """Eigen decomposition of a symmetric 3 by 3 matrix by cyclic Jacobi rotations.

    Returns (values, vectors) with vectors[k] the unit eigenvector for values[k].
    """
    a = [row[:] for row in m]
    v = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    for _ in range(50):
        off = a[0][1] ** 2 + a[0][2] ** 2 + a[1][2] ** 2
        if off < 1e-30 * (1.0 + sum(a[i][i] ** 2 for i in range(3))):
            break
        for p, q in ((0, 1), (0, 2), (1, 2)):
            if abs(a[p][q]) < 1e-300:
                continue
            theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
            t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
            cs = 1.0 / math.sqrt(t * t + 1.0)
            sn = t * cs
            for k in range(3):  # rotate columns p and q
                akp, akq = a[k][p], a[k][q]
                a[k][p] = cs * akp - sn * akq
                a[k][q] = sn * akp + cs * akq
            for k in range(3):  # rotate rows p and q
                apk, aqk = a[p][k], a[q][k]
                a[p][k] = cs * apk - sn * aqk
                a[q][k] = sn * apk + cs * aqk
            for k in range(3):
                vkp, vkq = v[k][p], v[k][q]
                v[k][p] = cs * vkp - sn * vkq
                v[k][q] = sn * vkp + cs * vkq
    values = [a[i][i] for i in range(3)]
    vectors = [[v[k][i] for k in range(3)] for i in range(3)]
    return values, vectors


def solve_qef(points: list[Vec], normals: list[Vec], tol: float = 0.1) -> Vec:
    """Minimizer of sum (n_i . (x - p_i))^2 closest to the mass point of the p_i.

    The normal equations are (A^T A) x = A^T b with rows n_i of A and
    b_i = n_i . p_i. They are solved as x = m + pinv(A^T A) (A^T b - A^T A m),
    where m is the mass point and pinv drops the eigenvalues of A^T A below
    (tol * largest singular value of A)^2, which keeps the vertex near m
    along directions that the normals do not constrain.
    """
    k = len(points)
    m = tuple(sum(p[i] for p in points) / k for i in range(3))
    ata = [[sum(n[i] * n[j] for n in normals) for j in range(3)] for i in range(3)]
    r = [sum(n[i] * (n[0] * (p[0] - m[0]) + n[1] * (p[1] - m[1]) + n[2] * (p[2] - m[2]))
             for n, p in zip(normals, points)) for i in range(3)]  # A^T (b - A m)
    values, vectors = _jacobi_eigen(ata)
    top = max(values)
    x = list(m)
    for lam, e in zip(values, vectors):
        if top > 0 and lam > tol * tol * top:
            s = (e[0] * r[0] + e[1] * r[1] + e[2] * r[2]) / lam
            for i in range(3):
                x[i] += s * e[i]
    return (x[0], x[1], x[2])


def _bisect(f: Field, pa: Vec, pb: Vec, c: float, iters: int = 60) -> Vec:
    """The point on the segment pa pb where f = c; f(pa) < c <= f(pb)."""
    lo, hi = 0.0, 1.0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        p = tuple(pa[i] + mid * (pb[i] - pa[i]) for i in range(3))
        if f(*p) < c:
            lo = mid
        else:
            hi = mid
    t = 0.5 * (lo + hi)
    return (pa[0] + t * (pb[0] - pa[0]), pa[1] + t * (pb[1] - pa[1]), pa[2] + t * (pb[2] - pa[2]))


def dual_contouring(f: Field, grad: Grad, origin: Vec, h: float, n: int, c: float = 0.0,
                    tol: float = 0.1, clamp: bool = True) -> tuple[list[Vec], list[tuple[int, int, int, int]]]:
    """Return (vertices, quads) of the surface f = c on an n by n by n cell grid.

    Grid point (i, j, k) is at origin + h * (i, j, k), 0 <= i, j, k <= n.
    Each quad is oriented with its normal (right-hand rule) toward the
    outside, where f >= c. With clamp, each vertex is clamped into its cell.
    The quad mesh is closed when every border sample is outside, but it can
    have non-manifold edges and vertices where a cell or a face is ambiguous.
    """
    def pos(g: tuple[int, int, int]) -> Vec:
        return (origin[0] + h * g[0], origin[1] + h * g[1], origin[2] + h * g[2])

    s = n + 1
    val = [[[f(*pos((i, j, k))) for k in range(s)] for j in range(s)] for i in range(s)]
    inside = [[[val[i][j][k] < c for k in range(s)] for j in range(s)] for i in range(s)]
    hermite: dict[tuple[int, int, int, int], tuple[Vec, Vec]] = {}
    cell_data: dict[tuple[int, int, int], tuple[list[Vec], list[Vec]]] = {}
    for i in range(s):  # @line L1
        for j in range(s):
            for k in range(s):
                for axis in range(3):
                    g2 = [i, j, k]
                    g2[axis] += 1
                    if g2[axis] > n or inside[i][j][k] == inside[g2[0]][g2[1]][g2[2]]:
                        continue
                    a, b = (i, j, k), (g2[0], g2[1], g2[2])
                    lo, hi = (a, b) if inside[i][j][k] else (b, a)
                    p = _bisect(f, pos(lo), pos(hi), c)  # @line L2
                    gx = grad(*p)
                    ln = math.sqrt(gx[0] ** 2 + gx[1] ** 2 + gx[2] ** 2)
                    nrm = (gx[0] / ln, gx[1] / ln, gx[2] / ln)  # @line L3
                    hermite[(i, j, k, axis)] = (p, nrm)
                    b1, b2 = (axis + 1) % 3, (axis + 2) % 3
                    for o1 in (-1, 0):
                        for o2 in (-1, 0):
                            cell = [i, j, k]
                            cell[b1] += o1
                            cell[b2] += o2
                            if all(0 <= cell[t] < n for t in range(3)):
                                pts, nms = cell_data.setdefault((cell[0], cell[1], cell[2]), ([], []))
                                pts.append(p)
                                nms.append(nrm)
    verts: list[Vec] = []
    index: dict[tuple[int, int, int], int] = {}
    for cell, (pts, nms) in sorted(cell_data.items()):  # @line L4
        x = solve_qef(pts, nms, tol)  # @line L5
        if clamp:  # @line L6
            lo3 = pos(cell)
            x = tuple(min(max(x[t], lo3[t]), lo3[t] + h) for t in range(3))
        index[cell] = len(verts)
        verts.append(x)
    quads: list[tuple[int, int, int, int]] = []
    for (i, j, k, axis) in sorted(hermite):  # @line L7
        b1, b2 = (axis + 1) % 3, (axis + 2) % 3
        ring = []
        for o1, o2 in ((0, 0), (-1, 0), (-1, -1), (0, -1)):  # @line L8
            cell = [i, j, k]
            cell[b1] += o1
            cell[b2] += o2
            ring.append((cell[0], cell[1], cell[2]))
        if not all(0 <= cl[t] < n for cl in ring for t in range(3)):
            continue  # an edge on the border of the box
        q = [index[cl] for cl in ring]
        if not inside[i][j][k]:  # @line L9
            q.reverse()
        quads.append((q[0], q[1], q[2], q[3]))  # @line L10
    return verts, quads  # @line L11
