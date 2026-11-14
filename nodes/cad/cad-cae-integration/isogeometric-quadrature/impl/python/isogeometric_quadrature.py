# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isogeometric-quadrature/. The authors are listed in prov/61XER4.jsonl.

"""Quadrature for isogeometric Galerkin matrices in one parametric dimension.

- assemble: element loop with the n-point Gauss-Legendre rule per element
  (n = p + 1 is the default), for a B-spline or NURBS basis and a spline
  geometry map x(xi), giving the mass and stiffness matrices.
- half_point_rule: the rule of Hughes, Reali and Sangalli for splines of degree
  p and smoothness C^(p-1) on a uniform mesh, one point per two elements.
- weighted_quadrature_weights: the row-wise rule of Calabro, Sangalli and Tani
  for periodic uniform splines, with the knots and midpoints as points.
"""

import math
from fractions import Fraction


def gauss_legendre(n):
    """Nodes and weights of the n-point Gauss-Legendre rule on [0, 1] (floats)."""
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1) if n > 1 else 1.0
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        p0, p1 = 1.0, x
        for k in range(2, n + 1):
            p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
        dp = n * (x * p1 - p0) / (x * x - 1) if n > 1 else 1.0
        xs.append((1 - x) / 2)
        ws.append(1 / ((1 - x * x) * dp * dp))
    return xs, ws


def basis_and_derivative(t, p, k, u):
    """Values and first derivatives of N_{k-p..k, p} at u in span k (de Boor's table)."""
    left, right = [0] * (p + 1), [0] * (p + 1)
    ndu = [[0] * (p + 1) for _ in range(p + 1)]
    ndu[0][0] = 1
    for j in range(1, p + 1):
        left[j] = u - t[k + 1 - j]
        right[j] = t[k + j] - u
        saved = 0
        for r in range(j):
            ndu[j][r] = right[r + 1] + left[j - r]
            tmp = ndu[r][j - 1] / ndu[j][r]
            ndu[r][j] = saved + right[r + 1] * tmp
            saved = left[j - r] * tmp
        ndu[j][j] = saved
    N = [ndu[r][p] for r in range(p + 1)]
    if p == 0:
        return N, [0]
    dN = []
    for r in range(p + 1):
        a = ndu[r - 1][p - 1] / ndu[p][r - 1] if r >= 1 else 0
        b = ndu[r][p - 1] / ndu[p][r] if r <= p - 1 else 0
        dN.append(p * (a - b))
    return N, dN


def spans(t):
    return [k for k in range(len(t) - 1) if t[k] < t[k + 1]]


def assemble(t, p, X, w=None, n_gauss=None, rule=None):
    """Mass and stiffness matrices of the basis on t, with geometry x = sum R_i X_i.

    X are scalar control points of the map, w the weights (None for B-splines).
    rule gives (nodes, weights) on [0, 1]; the default is Gauss with n_gauss points.
    """
    n = len(t) - p - 1
    w = w or [1] * n
    nodes, weights = rule or gauss_legendre(n_gauss or p + 1)
    M = [[0.0] * n for _ in range(n)]
    K = [[0.0] * n for _ in range(n)]
    for k in spans(t):  # @line L1
        a, b = t[k], t[k + 1]
        for s, ws in zip(nodes, weights):  # @line L2
            u = a + (b - a) * s
            N, dN = basis_and_derivative(t, p, k, u)  # @line L3
            loc = range(k - p, k + 1)
            W = sum(w[i] * Ni for i, Ni in zip(loc, N))
            dW = sum(w[i] * di for i, di in zip(loc, dN))
            R = [w[i] * Ni / W for i, Ni in zip(loc, N)]
            dR = [w[i] * (di * W - Ni * dW) / W**2 for i, Ni, di in zip(loc, N, dN)]
            jac = sum(X[i] * di for i, di in zip(loc, dR))  # @line L4
            dx = ws * (b - a) * jac
            for ra, ia in enumerate(loc):  # @line L5
                for rb, ib in enumerate(loc):
                    M[ia][ib] += R[ra] * R[rb] * dx
                    K[ia][ib] += (dR[ra] / jac) * (dR[rb] / jac) * dx
    return M, K  # @line L6


def cardinal_bspline(p, x):
    """The uniform B-spline of degree p with knots 0, 1, ..., p + 1, exactly."""
    x = Fraction(x)
    if x < 0 or x >= p + 1:
        return Fraction(0)
    s = Fraction(0)
    for j in range(p + 2):
        if x - j > 0:
            s += (-1) ** j * math.comb(p + 1, j) * (x - j) ** p
    return s / math.factorial(p)


def half_point_rule(p, h, lo, hi):
    """Points and weights of the half-point rule on [lo, hi], a uniform mesh of size h.

    p even: every other knot; p odd: the midpoint of every other element.
    The weight is 2h. The rule integrates every spline of degree p, C^(p-1),
    on the uniform knots of the whole line, whose support lies in [lo, hi].
    """
    start = Fraction(0) if p % 2 == 0 else Fraction(1, 2)
    pts, x = [], lo + start * h
    while x <= hi:
        pts.append(x)
        x += 2 * h
    return pts, [2 * h] * len(pts)


def solve(A, b):
    """Exact Gauss-Jordan elimination for a square nonsingular system."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = next(i for i in range(c, n) if M[i][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        f = M[c][c]
        M[c] = [v / f for v in M[c]]
        for i in range(n):
            if i != c and M[i][c] != 0:
                g = M[i][c]
                M[i] = [x - g * y for x, y in zip(M[i], M[c])]
    return [M[i][n] for i in range(n)]


def periodic_bspline(p, n, i, x):
    """B-spline i of degree p on the periodic uniform mesh of [0, n] with h = 1."""
    x = Fraction(x) % n
    return sum(cardinal_bspline(p, x - i + n * s) for s in (-2, -1, 0, 1))


def bspline_product_integral(p, d):
    """Exact integral of N(x) N(x - d) for the cardinal B-spline of degree p."""
    total = Fraction(0)
    for a in range(-1, p + 2):
        # on [a, a + 1] the product is a polynomial of degree 2p; Simpson-type
        # exact rule: integrate the interpolant at 2p + 1 equispaced points
        m = 2 * p
        nodes = [a + Fraction(j, m) if m else Fraction(a) for j in range(m + 1)]
        vals = [cardinal_bspline(p, x) * cardinal_bspline(p, x - d) for x in nodes]
        total += newton_cotes(m, vals)
    return total


def newton_cotes(m, vals):
    """Closed Newton-Cotes rule with m + 1 points on an interval of length 1, exact."""
    if m == 0:
        return vals[0]
    xs = [Fraction(j, m) for j in range(m + 1)]
    A = [[x**k for x in xs] for k in range(m + 1)]
    b = [Fraction(1, k + 1) for k in range(m + 1)]
    wts = solve(A, b)
    return sum(wq * v for wq, v in zip(wts, vals))


def weighted_quadrature_weights(p, n, i):
    """Weights of the rule for the test function B_i on the periodic mesh of [0, n].

    The points are the knots and midpoints in the support of B_i, 2p + 1 of them.
    The weights solve sum_q w_q B_j(x_q) = integral of B_i B_j for the 2p + 1
    functions B_j whose support meets the support of B_i.
    """
    pts = [Fraction(i) + Fraction(q, 2) for q in range(1, 2 * p + 2)]
    js = [i + d for d in range(-p, p + 1)]
    A = [[periodic_bspline(p, n, j % n, x) for x in pts] for j in js]
    b = [bspline_product_integral(p, j - i) for j in js]
    return pts, solve(A, b)
