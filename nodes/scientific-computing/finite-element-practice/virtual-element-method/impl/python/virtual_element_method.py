# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/virtual-element-method/. The authors are listed in prov/EYHGHZ.jsonl.

"""Virtual element method of order 1 for -Laplace(u) = f in two dimensions.

The mesh is a list of polygons, each a counterclockwise list of vertex
indices. A polygon may have any number of vertices, collinear vertices
(hanging nodes) included. The local space has one unknown per vertex, the
value there. The basis functions are harmonic inside the polygon and are
never computed: the element matrices come from the elliptic projection onto
linear polynomials, which only needs the vertex values.
"""

import math
import random

import scimat

# Dunavant's 7 point rule on the reference triangle, exact up to degree 5 (barycentric, weight)
_T7 = [((1 / 3, 1 / 3, 1 / 3), 0.225)]
for _a, _b, _w in ((0.059715871789770, 0.470142064105115, 0.132394152788506),
                   (0.797426985353087, 0.101286507323456, 0.125939180544827)):
    _T7 += [((_a, _b, _b), _w), ((_b, _a, _b), _w), ((_b, _b, _a), _w)]


def polygon_area(pts):
    """Return the signed area of a polygon (positive when counterclockwise), by the shoelace formula."""
    m = len(pts)
    return sum(pts[i][0] * pts[(i + 1) % m][1] - pts[(i + 1) % m][0] * pts[i][1] for i in range(m)) / 2


def polygon_quadrature(pts):
    """Return (point, weight) pairs on a polygon that is star shaped with respect to its vertex centroid."""
    m = len(pts)
    cx, cy = sum(p[0] for p in pts) / m, sum(p[1] for p in pts) / m
    out = []
    for i in range(m):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % m]
        area = ((x1 - cx) * (y2 - cy) - (x2 - cx) * (y1 - cy)) / 2
        for (l0, l1, l2), w in _T7:
            out.append(((l0 * cx + l1 * x1 + l2 * x2, l0 * cy + l1 * y1 + l2 * y2), w * area))
    return out


def element_matrices(pts, tau=1.0):
    """Return (K, pstar, centre, h) for one polygon with counterclockwise vertices pts.

    pstar is the 3 x m matrix of the projection onto the scaled monomials
    1, (x - xc) / h, (y - yc) / h; K is the m x m local stiffness matrix.
    """
    m = len(pts)
    h = max(math.dist(p, q) for p in pts for q in pts)
    xc, yc = sum(p[0] for p in pts) / m, sum(p[1] for p in pts) / m  # @line L1
    d = [[1.0, (x - xc) / h, (y - yc) / h] for x, y in pts]  # @line L2
    b = [[1 / m] * m, [0.0] * m, [0.0] * m]
    for i in range(m):
        # (|e_{i-1}| n_{i-1} + |e_i| n_i) / 2, where |e| n of the edge from p to q is (q_y - p_y, p_x - q_x)
        (xp, yp), (xn, yn) = pts[i - 1], pts[(i + 1) % m]
        nx, ny = (yn - yp) / 2, (xp - xn) / 2
        b[1][i] = nx / h
        b[2][i] = ny / h  # @line L3
    g = scimat.matmul(b, d)
    pstar = scimat.solve(g, b)
    proj = scimat.matmul(d, pstar)  # @line L4
    gt = [[0.0] * 3] + g[1:]
    cons = scimat.matmul(scimat.transpose(pstar), scimat.matmul(gt, pstar))
    ip = scimat.sub(scimat.eye(m), proj)
    stab = scimat.matmul(scimat.transpose(ip), ip)
    k = scimat.add(cons, scimat.scale(tau, stab))  # @line L5
    return k, pstar, (xc, yc), h


def _projected(pstar, centre, h, values, x):
    """Return (value, gradient) at x of the linear projection of the given vertex values."""
    c = [sum(pstar[a][i] * v for i, v in enumerate(values)) for a in range(3)]
    return c[0] + c[1] * (x[0] - centre[0]) / h + c[2] * (x[1] - centre[1]) / h, (c[1] / h, c[2] / h)


def solve_vem(points, polygons, boundary, f, g, tau=1.0, tol=1e-14):
    """Assemble and solve the order 1 VEM system. Return (u, elements).

    u holds the vertex values; elements holds (pstar, centre, h) per polygon.
    boundary is the set of vertex indices where u = g(x, y) is imposed.
    """
    n = len(points)
    rows = [dict() for _ in range(n)]
    rhs = [0.0] * n
    elements = []
    for poly in polygons:
        pts = [points[i] for i in poly]
        k, pstar, centre, h = element_matrices(pts, tau)
        elements.append((pstar, centre, h))
        for (xq, wq) in polygon_quadrature(pts):
            fq = f(*xq) * wq
            for i, gi in enumerate(poly):
                phi = pstar[0][i] + pstar[1][i] * (xq[0] - centre[0]) / h + pstar[2][i] * (xq[1] - centre[1]) / h
                rhs[gi] += fq * phi
        for i, gi in enumerate(poly):
            for j, gj in enumerate(poly):
                rows[gi][gj] = rows[gi].get(gj, 0.0) + k[i][j]  # @line L6
    u = [g(*points[i]) if i in boundary else 0.0 for i in range(n)]
    free = [i for i in range(n) if i not in boundary]
    index = {gi: r for r, gi in enumerate(free)}
    a = [{index[j]: v for j, v in rows[i].items() if j in index} for i in free]
    b = [rhs[i] - sum(v * u[j] for j, v in rows[i].items() if j in boundary) for i in free]
    x = conjugate_gradient(a, b, tol)  # @line L7
    for r, gi in enumerate(free):
        u[gi] = x[r]
    return u, elements  # @line L8


def conjugate_gradient(a, b, tol=1e-14, maxit=None):
    """Solve a x = b for a symmetric positive definite matrix stored as a list of row dicts."""
    n = len(b)
    x = [0.0] * n
    r = list(b)
    p = list(r)
    rr = scimat.dot(r, r)
    stop = tol * tol * max(rr, 1e-300)
    for _ in range(maxit or 10 * n + 10):
        if rr <= stop:
            break
        ap = [sum(v * p[j] for j, v in row.items()) for row in a]
        alpha = rr / scimat.dot(p, ap)
        x = [xi + alpha * pi for xi, pi in zip(x, p)]
        r = [ri - alpha * api for ri, api in zip(r, ap)]
        rr_new = scimat.dot(r, r)
        p = [ri + rr_new / rr * pi for ri, pi in zip(r, p)]
        rr = rr_new
    return x


def errors(points, polygons, u, elements, exact, grad):
    """Return (L2 error, H1 seminorm error) of the projections of u_h, and the largest vertex error."""
    e0 = e1 = 0.0
    for poly, (pstar, centre, h) in zip(polygons, elements):
        pts = [points[i] for i in poly]
        vals = [u[i] for i in poly]
        for xq, wq in polygon_quadrature(pts):
            v, (gx, gy) = _projected(pstar, centre, h, vals, xq)
            ex, (ux, uy) = exact(*xq), grad(*xq)
            e0 += wq * (v - ex) ** 2
            e1 += wq * ((gx - ux) ** 2 + (gy - uy) ** 2)
    emax = max(abs(u[i] - exact(*p)) for i, p in enumerate(points))
    return math.sqrt(e0), math.sqrt(e1), emax


def polygon_mesh(n, seed=0, jitter=0.0, midpoint_prob=0.0):
    """Return (points, polygons, boundary) for the unit square.

    The square is cut into n x n cells, the interior grid nodes move by up to
    jitter * (1 / n) in each direction, and each cell edge gets a midpoint
    node with probability midpoint_prob. A cell then has 4 to 8 vertices.
    """
    rng = random.Random(seed)
    h = 1 / n
    points = []
    for j in range(n + 1):
        for i in range(n + 1):
            x, y = i * h, j * h
            if 0 < i < n and 0 < j < n:
                x += rng.uniform(-jitter, jitter) * h
                y += rng.uniform(-jitter, jitter) * h
            points.append((x, y))
    boundary = {i + j * (n + 1) for j in range(n + 1) for i in range(n + 1) if i in (0, n) or j in (0, n)}
    mids = {}

    def node(i, j):
        return i + j * (n + 1)

    def midpoint(p, q, on_boundary):
        key = (min(p, q), max(p, q))
        if key not in mids:
            if rng.random() < midpoint_prob:
                (x1, y1), (x2, y2) = points[p], points[q]
                points.append(((x1 + x2) / 2, (y1 + y2) / 2))
                mids[key] = len(points) - 1
                if on_boundary:
                    boundary.add(mids[key])
            else:
                mids[key] = None
        return mids[key]

    polygons = []
    for j in range(n):
        for i in range(n):
            corners = [node(i, j), node(i + 1, j), node(i + 1, j + 1), node(i, j + 1)]
            sides = [j == 0, i == n - 1, j == n - 1, i == 0]
            poly = []
            for s in range(4):
                p, q = corners[s], corners[(s + 1) % 4]
                poly.append(p)
                mid = midpoint(p, q, sides[s])
                if mid is not None:
                    poly.append(mid)
            polygons.append(poly)
    return points, polygons, boundary
