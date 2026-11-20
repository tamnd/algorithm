# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zienkiewicz-zhu-estimator/. The authors are listed in prov/4WBQ50.jsonl.

"""Zienkiewicz-Zhu error estimator for P1 triangles in 2D.

The P1 solution u_h has a constant gradient on each triangle. The estimator
recovers a continuous piecewise linear gradient G from it and returns
eta_K = ||G - grad u_h||_{L2(K)} on every triangle. Two recoveries are here:
- superconvergent patch recovery (SPR, Zienkiewicz and Zhu 1992): at each
  interior vertex, fit a linear polynomial to the element gradients at the
  centroids of the patch by least squares, and evaluate it at the vertex;
  a boundary vertex takes the mean of the fits of the interior patches
  that contain it;
- simple averaging (Zienkiewicz and Zhu 1987): the area-weighted mean of
  the element gradients around each vertex.

A mesh is (coords, elements) with coords a list of (x, y) and elements a
list of vertex triples. Cost: O(M) for M triangles of bounded vertex degree
(real-RAM), after the solve.
"""

import math

import scisparse


def square_grid(m):
    """Return (coords, elements) of the unit square with m by m squares, each cut by the diagonal from (x, y) to (x + h, y + h)."""
    coords = [(i / m, j / m) for j in range(m + 1) for i in range(m + 1)]
    elements = []
    for j in range(m):
        for i in range(m):
            a = i + (m + 1) * j
            b, c, d = a + 1, a + m + 2, a + m + 1
            elements.append([a, b, c])
            elements.append([a, c, d])
    return coords, elements


def boundary_nodes(coords, elements):
    """Return the set of vertices on edges that belong to one element only."""
    count = {}
    for z in elements:
        for r in range(3):
            e = tuple(sorted((z[r], z[(r + 1) % 3])))
            count[e] = count.get(e, 0) + 1
    return {v for e, c in count.items() if c == 1 for v in e}


def _geometry(coords, z):
    (x0, y0), (x1, y1), (x2, y2) = coords[z[0]], coords[z[1]], coords[z[2]]
    d = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
    grads = [((y1 - y2) / d, (x2 - x1) / d), ((y2 - y0) / d, (x0 - x2) / d),
             ((y0 - y1) / d, (x1 - x0) / d)]
    return abs(d) / 2, grads


def solve_p1(coords, elements, f, g, tol=1e-11):
    """Return nodal values of the P1 solution of -Laplacian(u) = f, u = g on the boundary.

    The load uses the edge midpoint rule (exact for quadratics).
    """
    n = len(coords)
    bnd = boundary_nodes(coords, elements)
    U = [0.0] * n
    for v in bnd:
        U[v] = g(*coords[v])
    free = [v for v in range(n) if v not in bnd]
    index = {v: i for i, v in enumerate(free)}
    A = [dict() for _ in free]
    b = [0.0] * len(free)
    for z in elements:
        area, grads = _geometry(coords, z)
        mids = []
        for r in range(3):
            p, q = coords[z[(r + 1) % 3]], coords[z[(r + 2) % 3]]
            mids.append(f((p[0] + q[0]) / 2, (p[1] + q[1]) / 2))
        for r in range(3):
            i = index.get(z[r])
            if i is None:
                continue
            # phi_r is 1/2 at the midpoints of the two edges at vertex r, 0 at the third
            b[i] += area / 3 * 0.5 * (mids[(r + 1) % 3] + mids[(r + 2) % 3])
            for s in range(3):
                val = area * (grads[r][0] * grads[s][0] + grads[r][1] * grads[s][1])
                j = index.get(z[s])
                if j is None:
                    b[i] -= val * U[z[s]]
                else:
                    A[i][j] = A[i].get(j, 0.0) + val
    if free:
        x, _ = scisparse.cg(A, b, tol=tol, maxit=20 * len(free) + 100)
        for v, val in zip(free, x):
            U[v] = val
    return U


def element_gradients(coords, elements, U):
    """Return the constant gradient of the P1 function U on each element."""
    out = []
    for z in elements:
        _, grads = _geometry(coords, z)
        out.append((sum(U[z[r]] * grads[r][0] for r in range(3)),
                    sum(U[z[r]] * grads[r][1] for r in range(3))))
    return out


def _fit_linear(points, values):
    """Least squares fit of a + b x + c y to the values at the points; return (a, b, c) or None."""
    s = [[0.0] * 3 for _ in range(3)]
    t = [0.0] * 3
    for (x, y), v in zip(points, values):
        row = (1.0, x, y)
        for i in range(3):
            t[i] += row[i] * v
            for j in range(3):
                s[i][j] += row[i] * row[j]
    det = (s[0][0] * (s[1][1] * s[2][2] - s[1][2] * s[2][1])
           - s[0][1] * (s[1][0] * s[2][2] - s[1][2] * s[2][0])
           + s[0][2] * (s[1][0] * s[2][1] - s[1][1] * s[2][0]))
    scale = max(abs(s[i][j]) for i in range(3) for j in range(3))
    if abs(det) <= 1e-12 * scale ** 3:
        return None
    out = []
    for k in range(3):  # Cramer's rule
        m = [[t[i] if j == k else s[i][j] for j in range(3)] for i in range(3)]
        dk = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
              - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
              + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
        out.append(dk / det)
    return tuple(out)


def recover_average(coords, elements, U):
    """Return the recovered nodal gradients by area-weighted averaging (ZZ 1987)."""
    n = len(coords)
    gsum = [[0.0, 0.0] for _ in range(n)]
    wsum = [0.0] * n
    for z, (gx, gy) in zip(elements, element_gradients(coords, elements, U)):
        area, _ = _geometry(coords, z)
        for v in z:
            gsum[v][0] += area * gx
            gsum[v][1] += area * gy
            wsum[v] += area
    return [(gsum[v][0] / wsum[v], gsum[v][1] / wsum[v]) if wsum[v] else (0.0, 0.0) for v in range(n)]


def recover_spr(coords, elements, U):
    """Return the recovered nodal gradients by superconvergent patch recovery (ZZ 1992)."""
    n = len(coords)
    grads = element_gradients(coords, elements, U)
    patch = [[] for _ in range(n)]
    for t, z in enumerate(elements):
        for v in z:
            patch[v].append(t)
    bnd = boundary_nodes(coords, elements)
    G = [None] * n
    acc = {v: [0.0, 0.0, 0] for v in bnd}
    for v in range(n):  # @line L6
        if v in bnd:
            continue
        xv, yv = coords[v]
        pts, gxs, gys = [], [], []
        for t in patch[v]:
            z = elements[t]
            pts.append((sum(coords[w][0] for w in z) / 3 - xv, sum(coords[w][1] for w in z) / 3 - yv))
            gxs.append(grads[t][0])
            gys.append(grads[t][1])
        px, py = _fit_linear(pts, gxs), _fit_linear(pts, gys)  # @line L7
        if px is None or py is None:
            continue
        G[v] = (px[0], py[0])  # @line L8
        for w in {w for t in patch[v] for w in elements[t]} & bnd:  # @line L9
            dx, dy = coords[w][0] - xv, coords[w][1] - yv
            a = acc[w]
            a[0] += px[0] + px[1] * dx + px[2] * dy
            a[1] += py[0] + py[1] * dx + py[2] * dy
            a[2] += 1
    fallback = recover_average(coords, elements, U)
    for v in range(n):
        if v in bnd and acc[v][2] > 0:
            G[v] = (acc[v][0] / acc[v][2], acc[v][1] / acc[v][2])  # @line L10
        elif G[v] is None:
            G[v] = fallback[v]
    return G  # @line L11


def zz_estimator(coords, elements, U, recovery="spr"):
    """Return the list of indicators eta_K = ||G - grad u_h||_K and the total eta."""
    G = recover_spr(coords, elements, U) if recovery == "spr" else recover_average(coords, elements, U)  # @line L1
    grads = element_gradients(coords, elements, U)
    eta = []
    for t, z in enumerate(elements):  # @line L2
        area, _ = _geometry(coords, z)
        gx, gy = grads[t]
        s = 0.0
        for r in range(3):  # edge midpoint rule, exact for the quadratic integrand  # @line L3
            a, b = z[(r + 1) % 3], z[(r + 2) % 3]
            dx = (G[a][0] + G[b][0]) / 2 - gx
            dy = (G[a][1] + G[b][1]) / 2 - gy
            s += area / 3 * (dx * dx + dy * dy)
        eta.append(math.sqrt(s))  # @line L4
    return eta, math.sqrt(sum(e * e for e in eta))  # @line L5


# 7-point rule of degree 5 on the reference triangle, in barycentric coordinates.
_A1, _B1 = 0.059715871789770, 0.470142064105115
_A2, _B2 = 0.797426985353087, 0.101286507323456
_W0, _W1, _W2 = 0.225, 0.132394152788506, 0.125939180544827
QUAD7 = [((1 / 3, 1 / 3, 1 / 3), _W0),
         ((_A1, _B1, _B1), _W1), ((_B1, _A1, _B1), _W1), ((_B1, _B1, _A1), _W1),
         ((_A2, _B2, _B2), _W2), ((_B2, _A2, _B2), _W2), ((_B2, _B2, _A2), _W2)]


def energy_error(coords, elements, U, grad_u):
    """Return |u - u_h|_1 computed with the 7-point rule on each element."""
    total = 0.0
    for z, (gx, gy) in zip(elements, element_gradients(coords, elements, U)):
        area, _ = _geometry(coords, z)
        for lam, w in QUAD7:
            x = sum(lam[r] * coords[z[r]][0] for r in range(3))
            y = sum(lam[r] * coords[z[r]][1] for r in range(3))
            ux, uy = grad_u(x, y)
            total += w * area * ((ux - gx) ** 2 + (uy - gy) ** 2)
    return math.sqrt(total)
