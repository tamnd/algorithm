# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hp-finite-element-method/. The authors are listed in prov/9VWB60.jsonl.

"""hp finite element method in 1D with a geometric mesh and a linear degree vector.

Model problem: -u'' = f on (0, 1), u(0) = u(1) = 0. Element i is
[x_{i-1}, x_i] with length h_i and degree p_i >= 1. The basis is the hat
function at each interior node plus the integrated Legendre bubbles

    psi_k(xi) = (P_k(xi) - P_{k-2}(xi)) / sqrt(2 (2k - 1)),  k = 2..p_i,

on each element, with xi in [-1, 1] the local coordinate. Then
psi_k' = sqrt((2k - 1) / 2) P_{k-1}, the bubbles are orthogonal to each other
and to the hats in the energy product, and the bubble stiffness is the
diagonal 2 / h_i. Only the hats are coupled, by a tridiagonal matrix.

The load is given through the exact solution u: the right side of the
Galerkin system is a(u, v) = int u' v', which equals int f v. So the caller
gives u (for the hats) and the moments M_j = int_{-1}^{1} u'(x(xi)) P_j(xi) dxi
(for the bubbles). The energy error is then |u - u_h|_1^2 = |u|_1^2 - b^T U.

Cost: O(N) for N unknowns after the loads (Thomas algorithm for the hats).
"""

import math

import scisparse


def legendre(j, x):
    """Return P_j(x) by the three-term recurrence."""
    if j == 0:
        return 1.0
    p0, p1 = 1.0, x
    for k in range(2, j + 1):
        p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
    return p1


def gauss_legendre(n):
    """Return the n Gauss-Legendre nodes and weights on [-1, 1] (Newton on P_n)."""
    nodes, weights = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        p0, p1 = 1.0, x
        for k in range(2, n + 1):
            p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
        dp = n * (x * p1 - p0) / (x * x - 1)
        nodes.append(x)
        weights.append(2 / ((1 - x * x) * dp * dp))
    return nodes, weights


def geometric_mesh(n, sigma):
    """Return the nodes 0, sigma^(n-1), ..., sigma, 1: n elements graded toward 0."""
    return [0.0] + [sigma ** (n - i) for i in range(1, n + 1)]


def linear_degrees(n, mu):
    """Return the degree vector p_i = max(1, ceil(mu * i)), i = 1..n, from the singular end."""
    return [max(1, math.ceil(mu * i - 1e-12)) for i in range(1, n + 1)]


def solve_hp(nodes, degrees, u, moment):
    """Solve the Galerkin system; return (V, C, bTU).

    V: values at the interior nodes; C[i]: the bubble coefficients of
    element i (k = 2..p_i); bTU: b^T U, so that |u - u_h|_1^2 = |u|_1^2 - bTU.
    moment(a, b, j) must return int_{-1}^{1} u'(x(xi)) P_j(xi) dxi on [a, b].
    """
    n = len(nodes) - 1
    h = [nodes[i + 1] - nodes[i] for i in range(n)]
    m = n - 1  # interior nodes 1..n-1
    sub, diag, sup, rhs = [0.0] * m, [0.0] * m, [0.0] * m, [0.0] * m
    for i in range(n):  # element i joins nodes i and i + 1  # @line L3
        s = (u(nodes[i + 1]) - u(nodes[i])) / h[i]  # int_K u' phi' for the two hats
        for r, node in ((0, i), (1, i + 1)):
            j = node - 1
            if 0 <= j < m:
                diag[j] += 1 / h[i]
                rhs[j] += -s if r == 0 else s
        if 1 <= i <= m - 1:  # both nodes of the element are interior
            sub[i] = -1 / h[i]
            sup[i - 1] = -1 / h[i]
    V = scisparse.thomas(sub, diag, sup, rhs) if m else []  # @line L4
    bTU = sum(r * v for r, v in zip(rhs, V))
    C = []
    for i in range(n):
        ci = []
        for k in range(2, degrees[i] + 1):
            bk = math.sqrt((2 * k - 1) / 2) * moment(nodes[i], nodes[i + 1], k - 1)
            ci.append(h[i] / 2 * bk)  # @line L5
            bTU += h[i] / 2 * bk * bk
        C.append(ci)
    return V, C, bTU  # @line L6


def evaluate(nodes, V, C, x):
    """Return u_h(x)."""
    n = len(nodes) - 1
    i = 0
    while i < n - 1 and x > nodes[i + 1]:
        i += 1
    a, b = nodes[i], nodes[i + 1]
    va = V[i - 1] if i >= 1 else 0.0
    vb = V[i] if i < n - 1 else 0.0
    xi = 2 * (x - a) / (b - a) - 1
    val = va * (1 - xi) / 2 + vb * (1 + xi) / 2
    for k, c in enumerate(C[i], start=2):
        val += c * (legendre(k, xi) - legendre(k - 2, xi)) / math.sqrt(2 * (2 * k - 1))
    return val


def quadrature_moment(du, npts=40):
    """Return a moment function for a smooth u' by Gauss-Legendre quadrature."""
    xs, ws = gauss_legendre(npts)

    def moment(a, b, j):
        return sum(w * du(a + (b - a) * (t + 1) / 2) * legendre(j, t) for t, w in zip(xs, ws))
    return moment


def corner_model(alpha):
    """Return (u, moment, energy) for u = x^alpha - x, singular at 0 for 1/2 < alpha < 1.

    On the element at 0, int_0^1 t^beta P_j(2t - 1) dt
    = beta (beta - 1) ... (beta - j + 1) / ((beta + 1) ... (beta + j + 1)) is used,
    which is exact. Elsewhere u' is analytic on the element and Gauss quadrature is used.
    """
    beta = alpha - 1

    def u(x):
        return x ** alpha - x

    def du(x):
        return alpha * x ** beta - 1

    smooth = quadrature_moment(du)

    def moment(a, b, j):
        if a > 0:
            return smooth(a, b, j)
        num, den = 1.0, beta + 1
        for k in range(j):
            num *= beta - k
            den *= beta + 2 + k
        exact = 2 * alpha * b ** beta * num / den  # x = b t, dxi = 2 dt
        return exact - (2.0 if j == 0 else 0.0)

    energy = alpha * alpha / (2 * alpha - 1) - 1  # |u|_1^2
    return u, moment, energy


def energy_error(energy, bTU):
    """Return |u - u_h|_1 from |u|_1^2 and b^T U (clipped at 0 against rounding)."""
    return math.sqrt(max(energy - bTU, 0.0))


def hp_geometric(n, sigma, mu, u, moment):
    """Geometric mesh with n layers toward 0 and linear degrees; return (N, V, C, bTU)."""
    nodes = geometric_mesh(n, sigma)  # @line L1
    degrees = linear_degrees(n, mu)  # @line L2
    V, C, bTU = solve_hp(nodes, degrees, u, moment)
    N = len(V) + sum(len(c) for c in C)
    return N, V, C, bTU
