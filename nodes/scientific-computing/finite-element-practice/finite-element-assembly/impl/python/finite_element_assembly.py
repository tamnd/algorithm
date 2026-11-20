# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finite-element-assembly/. The authors are listed in prov/AW3E0H.jsonl.

"""Finite element assembly for -(kappa u')' = f in 1D (P1, P2) and -div grad u = f in 2D (P1).

The global matrix is sparse: a list of dicts, one dict {column: value} per row.
Element matrices are computed by quadrature on the reference element. With
Fraction coordinates and the default rational rules, the element matrices and
the assembled matrix are exact.
"""

from fractions import Fraction as F

import scimat

# Quadrature rules on [0, 1]: lists of (point, weight).
# Boole's rule (closed Newton-Cotes, 5 points) is exact for degree <= 5 and rational.
BOOLE = [(F(0), F(7, 90)), (F(1, 4), F(32, 90)), (F(1, 2), F(12, 90)), (F(3, 4), F(32, 90)), (F(1), F(7, 90))]
_G5 = [(-0.9061798459386640, 0.2369268850561891), (-0.5384693101056831, 0.4786286704993665),
       (0.0, 0.5688888888888889), (0.5384693101056831, 0.4786286704993665),
       (0.9061798459386640, 0.2369268850561891)]
# 5-point Gauss-Legendre rule mapped to [0, 1], exact for degree <= 9.
GAUSS5 = [((1.0 + x) / 2.0, w / 2.0) for x, w in _G5]


def lagrange_basis_1d(k):
    """Return (phi, dphi): the Lagrange basis of degree k = 1 or 2 on [0, 1].

    The local nodes are in order along the interval: (0, 1) for k = 1 and
    (0, 1/2, 1) for k = 2.
    """
    if k == 1:
        phi = [lambda s: 1 - s, lambda s: s]
        dphi = [lambda s: -1, lambda s: 1]
    elif k == 2:
        phi = [lambda s: (1 - s) * (1 - 2 * s), lambda s: 4 * s * (1 - s), lambda s: s * (2 * s - 1)]
        dphi = [lambda s: 4 * s - 3, lambda s: 4 - 8 * s, lambda s: 4 * s - 1]
    else:
        raise ValueError("k must be 1 or 2")
    return phi, dphi


def element_1d(xl, xr, k, f=None, kappa=1, rule=BOOLE, load_rule=GAUSS5):
    """Return (A_K, M_K, b_K) on the interval [xl, xr] for Lagrange elements of degree k.

    A_K[i][j] = integral of kappa phi_j' phi_i', M_K[i][j] = integral of phi_j phi_i,
    b_K[i] = integral of f phi_i. A_K and M_K use `rule`; b_K uses `load_rule`
    (b_K is zero if f is None). kappa is a constant on the element.
    """
    h = xr - xl
    phi, dphi = lagrange_basis_1d(k)
    n = k + 1
    a = [[sum(w * kappa * dphi[j](s) * dphi[i](s) for s, w in rule) / h for j in range(n)] for i in range(n)]
    m = [[sum(w * phi[j](s) * phi[i](s) for s, w in rule) * h for j in range(n)] for i in range(n)]
    if f is None:
        b = [0] * n
    else:
        b = [sum(w * f(xl + s * h) * phi[i](s) for s, w in load_rule) * h for i in range(n)]
    return a, m, b


def mesh_1d(x, k):
    """Return (cells, coords) for the 1D mesh with vertices x[0] < ... < x[E] and degree k.

    Global dofs are numbered along the line: element e has the dofs
    k e, ..., k e + k. Each cell is (g, (xl, xr)) with g the local-to-global map.
    """
    cells = []
    coords = []
    for e in range(len(x) - 1):
        xl, xr = x[e], x[e + 1]
        g = tuple(k * e + i for i in range(k + 1))
        cells.append((g, (xl, xr)))
        coords.append(xl)
        if k == 2:
            coords.append((xl + xr) / 2)
    coords.append(x[-1])
    return cells, coords


def assemble(n, cells, element):
    """Assemble the global sparse matrix and load vector.

    n is the number of global dofs. cells is a list of (g, data), where g is the
    local-to-global map of the element (g[i] is the global index of local dof i).
    element(data) returns (A_K, b_K). Return (A, b) with A a list of n dicts.
    """
    a = [dict() for _ in range(n)]  # @line L1
    b = [0] * n  # @line L1
    for cell in cells:  # @line L2
        g, data = cell  # @line L3
        a_k, b_k = element(data)  # @line L4
        for i in range(len(g)):  # @line L5
            b[g[i]] += b_k[i]  # @line L6
            row = a[g[i]]
            for j in range(len(g)):  # @line L7
                row[g[j]] = row.get(g[j], 0) + a_k[i][j]  # @line L8
    return a, b  # @line L9


def apply_dirichlet(a, b, values):
    """Impose u[j] = values[j] for the dofs j in values, keeping the matrix symmetric.

    The known values move to the right side (lines L10 and L11); then the row
    and the column of each Dirichlet dof become those of the identity (line L12).
    a and b are changed in place and returned.
    """
    for j, gj in values.items():  # @line L10
        for i in range(len(a)):  # @line L11
            if i not in values and j in a[i]:  # @line L11
                b[i] -= a[i][j] * gj  # @line L11
    for i, gi in values.items():  # @line L12
        for j in list(a[i]):  # @line L12
            if j != i:
                a[j].pop(i, None)
        a[i] = {i: 1}  # @line L12
        b[i] = gi  # @line L12
    return a, b  # @line L13


def to_dense(a):
    """Return the sparse matrix a (list of dicts) as a dense list of rows."""
    n = len(a)
    out = scimat.zeros(n, n)
    for i, row in enumerate(a):
        for j, v in row.items():
            out[i][j] = v
    return out


def solve_poisson_1d(x, k, f, g_left, g_right, kappa=1, rule=BOOLE, load_rule=GAUSS5):
    """Solve -(kappa u')' = f on [x[0], x[-1]] with u = g_left, g_right at the ends.

    Return (coords, U): the dof coordinates and the nodal values of u_h.
    """
    cells, coords = mesh_1d(x, k)
    n = len(coords)

    def element(data):
        a_k, _, b_k = element_1d(data[0], data[1], k, f, kappa, rule, load_rule)
        return a_k, b_k

    a, b = assemble(n, cells, element)
    apply_dirichlet(a, b, {0: g_left, n - 1: g_right})
    return coords, scimat.solve(to_dense(a), b)


def errors_1d(x, k, u_h, u, du):
    """Return (L2 error, H1 seminorm error) of the P_k solution u_h against u, u'.

    Both are computed with the 5-point Gauss rule on each element.
    """
    phi, dphi = lagrange_basis_1d(k)
    e0 = 0.0
    e1 = 0.0
    for e in range(len(x) - 1):
        xl, xr = float(x[e]), float(x[e + 1])
        h = xr - xl
        loc = [float(u_h[k * e + i]) for i in range(k + 1)]
        for s, w in GAUSS5:
            xs = xl + s * h
            uh = sum(loc[i] * phi[i](s) for i in range(k + 1))
            duh = sum(loc[i] * dphi[i](s) for i in range(k + 1)) / h
            e0 += w * h * (u(xs) - uh) ** 2
            e1 += w * h * (du(xs) - duh) ** 2
    return e0 ** 0.5, e1 ** 0.5


# ---------------------------------------------------------------- P1 on triangles


def p1_triangle(p0, p1, p2, f=None):
    """Return (A_K, M_K, b_K) for P1 on the triangle with vertices p0, p1, p2.

    The affine map is F_K(xhat) = p0 + B xhat with B = [p1 - p0, p2 - p0]. The
    reference gradients are (-1, -1), (1, 0), (0, 1), and grad phi_i = B^(-T)
    grad phihat_i. The load uses the edge midpoint rule (exact for degree 2).
    """
    b11, b12 = p1[0] - p0[0], p2[0] - p0[0]
    b21, b22 = p1[1] - p0[1], p2[1] - p0[1]
    det = b11 * b22 - b12 * b21
    if det == 0:
        raise ValueError("degenerate triangle")
    area = abs(det) / 2
    # B^(-T) = (1/det) [[b22, -b21], [-b12, b11]]
    grads = []
    for gx, gy in ((-1, -1), (1, 0), (0, 1)):
        grads.append(((b22 * gx - b21 * gy) / det, (-b12 * gx + b11 * gy) / det))
    a = [[area * (grads[i][0] * grads[j][0] + grads[i][1] * grads[j][1]) for j in range(3)] for i in range(3)]
    m = [[area * (F(2, 12) if i == j else F(1, 12)) for j in range(3)] for i in range(3)]
    if f is None:
        b = [0, 0, 0]
    else:
        pts = (p0, p1, p2)
        b = [0, 0, 0]
        for i in range(3):
            for j in range(3):
                if i != j:
                    # midpoint of edge (i, j): phi_i = 1/2 there; each midpoint has weight area / 3
                    mid = ((pts[i][0] + pts[j][0]) / 2, (pts[i][1] + pts[j][1]) / 2)
                    b[i] += area / 3 * f(mid[0], mid[1]) / 2
    return a, m, b


def square_mesh(m, perturb=None):
    """Return (points, triangles) for the unit square cut into m by m cells.

    Each cell is cut by its diagonal from the lower left to the upper right
    corner. Point (i, j) has index j (m + 1) + i. perturb(i, j) may return a
    shift (dx, dy) for interior points.
    """
    pts = []
    for j in range(m + 1):
        for i in range(m + 1):
            x, y = F(i, m), F(j, m)
            if perturb is not None and 0 < i < m and 0 < j < m:
                dx, dy = perturb(i, j)
                x, y = x + dx, y + dy
            pts.append((x, y))
    tris = []
    for j in range(m):
        for i in range(m):
            v00 = j * (m + 1) + i
            v10, v01, v11 = v00 + 1, v00 + m + 1, v00 + m + 2
            tris.append((v00, v10, v11))
            tris.append((v00, v11, v01))
    return pts, tris


def boundary_points(m):
    """Return the indices of the points of square_mesh(m) on the boundary."""
    out = []
    for j in range(m + 1):
        for i in range(m + 1):
            if i in (0, m) or j in (0, m):
                out.append(j * (m + 1) + i)
    return out


def solve_poisson_2d(pts, tris, boundary, f, g):
    """Solve -div grad u = f with u = g on the boundary points, by P1 elements.

    Return the nodal values of u_h.
    """
    cells = [(t, t) for t in tris]

    def element(t):
        a_k, _, b_k = p1_triangle(pts[t[0]], pts[t[1]], pts[t[2]], f)
        return a_k, b_k

    a, b = assemble(len(pts), cells, element)
    apply_dirichlet(a, b, {v: g(*pts[v]) for v in boundary})
    return scimat.solve(to_dense(a), b)


def errors_2d(pts, tris, u_h, u, grad_u):
    """Return (L2 error, H1 seminorm error) of the P1 solution, by a collapsed Gauss rule.

    The rule maps the square [0, 1]^2 to the reference triangle by
    (s, t) -> (s, t (1 - s)), with the factor (1 - s), and uses 5 by 5 Gauss points.
    """
    e0 = 0.0
    e1 = 0.0
    for t in tris:
        p0, p1, p2 = (tuple(float(c) for c in pts[v]) for v in t)
        b11, b12 = p1[0] - p0[0], p2[0] - p0[0]
        b21, b22 = p1[1] - p0[1], p2[1] - p0[1]
        det = b11 * b22 - b12 * b21
        loc = [float(u_h[v]) for v in t]
        # constant gradient of u_h on the triangle
        gx = sum(loc[i] * (b22 * gxh - b21 * gyh) / det for i, (gxh, gyh) in enumerate(((-1, -1), (1, 0), (0, 1))))
        gy = sum(loc[i] * (-b12 * gxh + b11 * gyh) / det for i, (gxh, gyh) in enumerate(((-1, -1), (1, 0), (0, 1))))
        for s, ws in GAUSS5:
            for r, wr in GAUSS5:
                xh, yh = s, r * (1 - s)
                w = ws * wr * (1 - s) * abs(det)
                x = p0[0] + b11 * xh + b12 * yh
                y = p0[1] + b21 * xh + b22 * yh
                uh = loc[0] * (1 - xh - yh) + loc[1] * xh + loc[2] * yh
                ux, uy = grad_u(x, y)
                e0 += w * (u(x, y) - uh) ** 2
                e1 += w * ((ux - gx) ** 2 + (uy - gy) ** 2)
    return e0 ** 0.5, e1 ** 0.5
