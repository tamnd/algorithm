# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/element-free-galerkin-method/. The authors are listed in prov/MYQ8NE.jsonl.

"""Element-free Galerkin method in one dimension.

Solves -u'' = f on [a, b] with u(a) = ua and u(b) = ub. The shape functions
are moving least squares (MLS) functions built from scattered nodes with a
polynomial basis of degree 1 or 2 and the cubic spline weight. They do not
satisfy phi_I(x_J) = delta_IJ, so the boundary conditions are imposed with
Lagrange multipliers. Integration uses Gauss points on background cells.
"""

import math

import scimat


def gauss_legendre(n):
    """Return the n Gauss-Legendre points and weights on [-1, 1]."""
    pts, wts = [], []
    for k in range(n):
        x = math.cos(math.pi * (k + 0.75) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for j in range(2, n + 1):
                p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        pts.append(x)
        wts.append(2 / ((1 - x * x) * dp * dp))
    return pts, wts


def cubic_spline_weight(r):
    """Return (w, dw/dr) of the cubic spline weight for r = |x - x_I| / d_I >= 0."""
    if r <= 0.5:
        return 2 / 3 - 4 * r * r + 4 * r ** 3, -8 * r + 12 * r * r
    if r < 1:
        return 4 / 3 - 4 * r + 4 * r * r - 4 / 3 * r ** 3, -4 + 8 * r - 4 * r * r
    return 0.0, 0.0


def _basis(x, degree):
    if degree == 1:
        return [1.0, x], [0.0, 1.0]
    return [1.0, x, x * x], [0.0, 1.0, 2 * x]


def mls_shape(x, nodes, radii, degree=1):
    """Return (idx, phi, dphi): the nodes whose support covers x and their MLS values and derivatives."""
    idx, w, dw = [], [], []
    for i, (xi, di) in enumerate(zip(nodes, radii)):
        r = abs(x - xi) / di
        if r < 1:
            wi, dwr = cubic_spline_weight(r)
            sign = 1.0 if x >= xi else -1.0
            idx.append(i)
            w.append(wi)
            dw.append(dwr * sign / di)
    m = degree + 1
    p, dp = _basis(x, degree)
    a = scimat.zeros(m)
    da = scimat.zeros(m)
    pis = [_basis(nodes[i], degree)[0] for i in idx]
    for wi, dwi, pi in zip(w, dw, pis):
        for r in range(m):
            for c in range(m):
                a[r][c] += wi * pi[r] * pi[c]
                da[r][c] += dwi * pi[r] * pi[c]
    # gamma = A^{-1} p, so phi_I = gamma . (w_I p_I); dgamma = A^{-1} (dp - dA gamma)
    gamma = scimat.solve(a, p)
    dgamma = scimat.solve(a, scimat.sub(dp, scimat.matvec(da, gamma)))
    phi = [wi * scimat.dot(gamma, pi) for wi, pi in zip(w, pis)]
    dphi = [dwi * scimat.dot(gamma, pi) + wi * scimat.dot(dgamma, pi) for wi, dwi, pi in zip(w, dw, pis)]
    return idx, phi, dphi


def quadrature_points(a, b, ncells, order):
    """Return Gauss points and weights on ncells equal background cells of [a, b]."""
    gp, gw = gauss_legendre(order)
    h = (b - a) / ncells
    out = []
    for c in range(ncells):
        x0 = a + c * h
        for t, wt in zip(gp, gw):
            out.append((x0 + (t + 1) * h / 2, wt * h / 2))
    return out


class EFG1D:
    """An EFG discretization of -u'' = f on [nodes[0], nodes[-1]] with Dirichlet ends."""

    def __init__(self, nodes, support, f, ua, ub, ncells=None, order=3, degree=1, quadrature=None):
        self.nodes = list(nodes)
        n = len(self.nodes)
        self.radii = [support] * n if not isinstance(support, list) else support
        self.degree = degree
        a, b = self.nodes[0], self.nodes[-1]
        if quadrature is None:
            quadrature = quadrature_points(a, b, ncells or (n - 1), order)
        k = scimat.zeros(n)
        rhs = [0.0] * n
        for xq, wq in quadrature:  # @line L1
            idx, phi, dphi = mls_shape(xq, self.nodes, self.radii, degree)  # @line L2
            fq = f(xq)  # @line L3
            for ii, i in enumerate(idx):
                rhs[i] += wq * phi[ii] * fq
                for jj, j in enumerate(idx):
                    k[i][j] += wq * dphi[ii] * dphi[jj]  # @line L4
        # Lagrange multipliers for u(a) = ua and u(b) = ub
        big = [row + [0.0, 0.0] for row in k] + [[0.0] * (n + 2) for _ in range(2)]
        for col, (xb, g) in enumerate(((a, ua), (b, ub))):
            idx, phi, _ = mls_shape(xb, self.nodes, self.radii, degree)
            for ii, i in enumerate(idx):
                big[i][n + col] = phi[ii]  # @line L5
                big[n + col][i] = phi[ii]
            rhs.append(g)
        sol = scimat.solve(big, rhs)  # @line L6
        self.coef = sol[:n]
        self.multipliers = sol[n:]
        self.stiffness = k

    def value(self, x):
        """Return (u_h(x), u_h'(x))."""
        idx, phi, dphi = mls_shape(x, self.nodes, self.radii, self.degree)
        u = sum(p * self.coef[i] for p, i in zip(phi, idx))  # @line L7
        du = sum(p * self.coef[i] for p, i in zip(dphi, idx))
        return u, du  # @line L8


def nodal_quadrature(nodes):
    """Return the trapezoid weights at the nodes, the simplest nodal integration."""
    out = []
    for i, x in enumerate(nodes):
        left = nodes[i] - nodes[i - 1] if i > 0 else 0.0
        right = nodes[i + 1] - nodes[i] if i + 1 < len(nodes) else 0.0
        out.append((x, (left + right) / 2))
    return out


def errors(model, u, du, a, b, ncells=64, order=5):
    """Return the L2 error and the H1 seminorm error of model against u and du."""
    e0 = e1 = 0.0
    for xq, wq in quadrature_points(a, b, ncells, order):
        uh, duh = model.value(xq)
        e0 += wq * (uh - u(xq)) ** 2
        e1 += wq * (duh - du(xq)) ** 2
    return math.sqrt(e0), math.sqrt(e1)
