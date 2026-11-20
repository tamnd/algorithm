# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-element-method/. The authors are listed in prov/6Q7T79.jsonl.

"""Spectral element method in 1D with Gauss-Lobatto-Legendre (GLL) nodes.

Model problem: -u'' + c u = f on (a, b), u(a) = u(b) = 0, c >= 0.
The interval is cut into elements; on each element u_h is a polynomial of
degree N, stored by its values at the N + 1 GLL nodes. All integrals use
the GLL rule on the same nodes, so the mass matrix is diagonal:
M_e = (h_e / 2) diag(w). The stiffness is K_e = (2 / h_e) D^T diag(w) D,
with D the derivative matrix at the nodes.

The global system is solved densely with scimat.solve. This is fine for the
small sizes here; real codes use a matrix-free conjugate gradient method.
"""

import math

import scimat


def _legendre_pair(n, x):
    """Return (P_{n-1}(x), P_n(x))."""
    p0, p1 = 1.0, x
    if n == 0:
        return 0.0, 1.0
    for k in range(2, n + 1):
        p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
    return p0, p1


def gll(n):
    """Return the n + 1 GLL nodes on [-1, 1] (increasing) and their weights.

    The nodes are -1, 1 and the roots of P_n'. The iteration
    x <- x - (x P_n - P_{n-1}) / ((n + 1) P_n) starts at the Chebyshev-Lobatto points.
    """
    if n < 1:
        raise ValueError("gll needs n >= 1")
    xs = []
    for j in range(n + 1):
        x = -math.cos(math.pi * j / n)
        for _ in range(100):
            pm, p = _legendre_pair(n, x)
            dx = (x * p - pm) / ((n + 1) * p)
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(x)
    xs[0], xs[-1] = -1.0, 1.0
    ws = []
    for x in xs:
        _, p = _legendre_pair(n, x)
        ws.append(2.0 / (n * (n + 1) * p * p))
    return xs, ws


def derivative_matrix(xs):
    """Return D with D[i][j] = l_j'(x_i) for the Lagrange basis on the nodes xs."""
    n = len(xs)
    # barycentric weights
    lam = [1.0 / math.prod(xs[j] - xs[k] for k in range(n) if k != j) for j in range(n)]
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                D[i][j] = lam[j] / lam[i] / (xs[i] - xs[j])
        D[i][i] = -sum(D[i][j] for j in range(n) if j != i)  # rows sum to 0
    return D


def lagrange_eval(xs, values, x):
    """Return the interpolating polynomial through (xs, values) at x (barycentric form)."""
    n = len(xs)
    lam = [1.0 / math.prod(xs[j] - xs[k] for k in range(n) if k != j) for j in range(n)]
    num = den = 0.0
    for j in range(n):
        if x == xs[j]:
            return values[j]
        t = lam[j] / (x - xs[j])
        num += t * values[j]
        den += t
    return num / den


def sem_solve(breaks, n, f, c=0.0):
    """Solve -u'' + c u = f with zero end values; return (points, U) at all nodes."""
    xs, ws = gll(n)  # @line L1
    D = derivative_matrix(xs)
    E = len(breaks) - 1
    size = E * n + 1
    A = scimat.zeros(size)
    F = [0.0] * size
    points = [0.0] * size
    for e in range(E):  # @line L2
        a, b = breaks[e], breaks[e + 1]
        h = b - a
        for i in range(n + 1):  # @line L3
            gi = e * n + i
            x = a + h * (xs[i] + 1) / 2
            points[gi] = x
            for j in range(n + 1):
                kij = 2 / h * sum(ws[q] * D[q][i] * D[q][j] for q in range(n + 1))
                A[gi][e * n + j] += kij  # @line L4
            A[gi][gi] += c * h / 2 * ws[i]  # the diagonal mass
            F[gi] += h / 2 * ws[i] * f(x)
    inner = list(range(1, size - 1))
    Ai = [[A[i][j] for j in inner] for i in inner]
    Ui = scimat.solve(Ai, [F[i] for i in inner]) if inner else []  # @line L5
    U = [0.0] + list(Ui) + [0.0]
    return points, U  # @line L6


def evaluate(breaks, n, U, x):
    """Return u_h(x) from the nodal values U of sem_solve."""
    xs, _ = gll(n)
    E = len(breaks) - 1
    e = 0
    while e < E - 1 and x > breaks[e + 1]:
        e += 1
    a, b = breaks[e], breaks[e + 1]
    return lagrange_eval(xs, U[e * n: e * n + n + 1], 2 * (x - a) / (b - a) - 1)
