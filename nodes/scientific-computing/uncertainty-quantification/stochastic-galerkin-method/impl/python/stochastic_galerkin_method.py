# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-galerkin-method/. The authors are listed in prov/850TYY.jsonl.
"""Stochastic Galerkin method for a linear system with an affine random matrix.

The model is A(xi) u(xi) = f, with

    A(xi) = A_0 + xi_1 A_1 + ... + xi_d A_d,

where xi_1..xi_d are independent and uniform on [-1, 1] and f is a fixed
vector. The solution is sought as u(xi) = sum_a c_a Psi_a(xi), where Psi_a
are the orthonormal Legendre chaos polynomials of total degree at most p.
The Galerkin conditions E[(A(xi) u(xi) - f) Psi_b(xi)] = 0 for every b in
the basis give one block system K c = F with

    K = sum_k G_k (x) A_k,   G_k[a][b] = E[xi_k Psi_a Psi_b]  (xi_0 = 1),

and F = e_0 (x) f. The block system is solved with scimat.solve.
"""

import math

from scimat import solve

Vector = list[float]
Matrix = list[list[float]]


def total_degree_set(d: int, p: int) -> list[tuple[int, ...]]:
    """All a in N^d with |a| <= p, sorted by total degree; the zero index is first."""
    out: list[tuple[int, ...]] = []

    def rec(prefix: list[int], left: int) -> None:
        if len(prefix) == d:
            out.append(tuple(prefix))
            return
        for v in range(left, -1, -1):
            rec(prefix + [v], left - v)

    rec([], p)
    out.sort(key=lambda a: (sum(a), [-v for v in a]))
    return out


def legendre_xi_product(m: int, n: int) -> float:
    """E[xi psi_m(xi) psi_n(xi)] for orthonormal Legendre psi_n = sqrt(2n+1) P_n, xi uniform on [-1, 1]."""
    if n == m + 1:
        return (m + 1) / math.sqrt((2 * m + 1) * (2 * m + 3))
    if m == n + 1:
        return (n + 1) / math.sqrt((2 * n + 1) * (2 * n + 3))
    return 0.0


def galerkin_matrices(index: list[tuple[int, ...]], d: int) -> list[Matrix]:
    """G_0 = identity and G_k[a][b] = E[xi_k Psi_a Psi_b] for k = 1..d."""
    size = len(index)
    g = [[[0.0] * size for _ in range(size)] for _ in range(d + 1)]
    for i in range(size):
        g[0][i][i] = 1.0
    for k in range(d):
        for i, a in enumerate(index):
            for j, b in enumerate(index):
                if all(a[t] == b[t] for t in range(d) if t != k):
                    g[k + 1][i][j] = legendre_xi_product(a[k], b[k])
    return g


def stochastic_galerkin(a_mats: list[Matrix], f: Vector, p: int) -> tuple[list[tuple[int, ...]], list[Vector]]:
    """Solve the Galerkin system; return the index set and one coefficient vector per index."""
    d = len(a_mats) - 1
    n = len(f)
    index = total_degree_set(d, p)  # @line L1
    size = len(index)
    g = galerkin_matrices(index, d)  # @line L2
    big = [[0.0] * (size * n) for _ in range(size * n)]
    for k in range(d + 1):  # @line L3
        for i in range(size):
            for j in range(size):
                gij = g[k][i][j]
                if gij == 0.0:
                    continue
                for r in range(n):
                    row = big[i * n + r]
                    ak = a_mats[k][r]
                    for s in range(n):
                        row[j * n + s] += gij * ak[s]
    rhs = [0.0] * (size * n)  # @line L4
    rhs[:n] = [float(v) for v in f]
    sol = solve(big, rhs)  # @line L5
    coeffs = [sol[i * n:(i + 1) * n] for i in range(size)]
    return index, coeffs  # @line L7


def mean_and_variance(coeffs: list[Vector]) -> tuple[Vector, Vector]:
    """Mean c_0 and variance sum_{a != 0} c_a^2, component by component."""
    mean = list(coeffs[0])  # @line L6
    var = [sum(c[r] ** 2 for c in coeffs[1:]) for r in range(len(mean))]
    return mean, var


def legendre_basis(x: float, p: int) -> list[float]:
    """Orthonormal Legendre values psi_0(x)..psi_p(x)."""
    vals = [1.0, x]
    for k in range(2, p + 1):
        vals.append(((2 * k - 1) * x * vals[-1] - (k - 1) * vals[-2]) / k)
    return [vals[k] * math.sqrt(2 * k + 1) for k in range(p + 1)]


def evaluate(index: list[tuple[int, ...]], coeffs: list[Vector], xi: list[float]) -> Vector:
    """The surrogate u_p(xi) = sum_a c_a Psi_a(xi)."""
    p = max(sum(a) for a in index)
    tables = [legendre_basis(x, p) for x in xi]
    out = [0.0] * len(coeffs[0])
    for a, c in zip(index, coeffs):
        w = 1.0
        for t, at in enumerate(a):
            w *= tables[t][at]
        for r in range(len(out)):
            out[r] += w * c[r]
    return out


def diffusion_matrices(n_el: int, amp: float) -> list[Matrix]:
    """Linear finite elements for -(a u')' = 1 on (0, 1), u(0) = u(1) = 0.

    The coefficient is a = 1 + amp xi_1 on (0, 1/2) and 1 + amp xi_2 on (1/2, 1);
    n_el is even. Return [A_0, A_1, A_2] for the n_el - 1 interior nodes.
    """
    h = 1.0 / n_el
    n = n_el - 1
    left = [[0.0] * n for _ in range(n)]
    right = [[0.0] * n for _ in range(n)]
    for e in range(n_el):
        target = left if e < n_el // 2 else right
        nodes = [e - 1, e]
        for a_i, i in enumerate(nodes):
            for a_j, j in enumerate(nodes):
                if 0 <= i < n and 0 <= j < n:
                    target[i][j] += (1.0 if a_i == a_j else -1.0) / h
    a0 = [[left[i][j] + right[i][j] for j in range(n)] for i in range(n)]
    a1 = [[amp * v for v in row] for row in left]
    a2 = [[amp * v for v in row] for row in right]
    return [a0, a1, a2]


def load_vector(n_el: int) -> Vector:
    """The load F_i = integral of the hat function i, which is h for f = 1."""
    return [1.0 / n_el] * (n_el - 1)
