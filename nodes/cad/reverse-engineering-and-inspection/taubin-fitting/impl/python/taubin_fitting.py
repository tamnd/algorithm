# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/taubin-fitting/. The authors are listed in prov/4TBMTK.jsonl.

"""Taubin's gradient-weighted algebraic fit (Taubin, 1991).

The model is an implicit curve or surface f(x) = sum_j a_j phi_j(x) = 0, with
fixed polynomial basis functions phi_j. The fit minimizes

    sum_i f(x_i)^2 / sum_i |grad f(x_i)|^2 = a^T M a / a^T N a,

with M = sum_i phi(x_i) phi(x_i)^T and N = sum_i J(x_i) J(x_i)^T, where J is
the Jacobian of phi. The minimum is the smallest eigenvalue of M a = lambda N a.
N is singular when the basis holds a constant function, so the constant
coefficient is eliminated first (a Schur complement of M), and the rest is a
symmetric eigenproblem after a Cholesky factorization of N.

A basis function is a polynomial, stored as a dict from exponent tuples to
coefficients: {(2, 0): 1, (0, 2): 1} is x^2 + y^2.
"""

from typing import Dict, List, Sequence, Tuple

from re1lin import cholesky, dot, jacobi_eigen, lower_solve, norm, transpose, upper_solve_t

Poly = Dict[Tuple[int, ...], object]


def monomials(dim: int, degree: int) -> List[Poly]:
    """All monomials of total degree at most degree in dim variables, highest degree first, the constant last."""
    out: List[Tuple[int, ...]] = []

    def rec(prefix: Tuple[int, ...], left: int, k: int) -> None:
        if k == dim - 1:
            out.append(prefix + (left,))
            return
        for e in range(left, -1, -1):
            rec(prefix + (e,), left - e, k + 1)

    for total in range(degree, -1, -1):
        rec((), total, 0)
    return [{e: 1} for e in out]


def conic_basis() -> List[Poly]:
    """x^2, xy, y^2, x, y, 1: the general conic."""
    return monomials(2, 2)


def circle_basis(dim: int = 2) -> List[Poly]:
    """|x|^2, x_1, ..., x_dim, 1: circles (dim 2) or spheres (dim 3), with lines or planes as limits."""
    sq = {tuple(2 if k == j else 0 for k in range(dim)): 1 for j in range(dim)}
    lin = [{tuple(1 if k == j else 0 for k in range(dim)): 1} for j in range(dim)]
    return [sq] + lin + [{tuple([0] * dim): 1}]


def evaluate(p: Poly, x: Sequence):
    total = 0
    for e, c in p.items():
        t = c
        for xk, ek in zip(x, e):
            if ek:
                t = t * xk ** ek
        total += t
    return total


def gradient(p: Poly, x: Sequence) -> list:
    g = []
    for k in range(len(x)):
        s = 0
        for e, c in p.items():
            if e[k] == 0:
                continue
            t = c * e[k]
            for j, (xj, ej) in enumerate(zip(x, e)):
                ej = ej - 1 if j == k else ej
                if ej:
                    t = t * xj ** ej
            s += t
        g.append(s)
    return g


def implicit_value(a: Sequence[float], basis: List[Poly], x: Sequence) -> float:
    """f(x) = sum_j a_j phi_j(x)."""
    return sum(aj * evaluate(p, x) for aj, p in zip(a, basis))


def first_order_distance(a: Sequence[float], basis: List[Poly], x: Sequence) -> float:
    """|f(x)| / |grad f(x)|, the first-order approximation of the distance from x to f = 0."""
    g = [0.0] * len(x)
    for aj, p in zip(a, basis):
        for k, v in enumerate(gradient(p, x)):
            g[k] += aj * v
    return abs(float(implicit_value(a, basis, x))) / norm(g)


def taubin_fit(points: Sequence[Sequence], basis: List[Poly]) -> Tuple[List[float], float]:
    """Taubin's fit of the implicit curve sum_j a_j phi_j(x) = 0 to the points.

    Precondition: the basis functions are linearly independent, at most one of
    them is a constant and then it is the last one, and no nonzero combination
    of the nonconstant ones has a zero gradient at every point (N restricted to
    them is positive definite); otherwise ValueError. Points may be int,
    Fraction or float; M and N are then exact, the eigen step is in floats.
    Returns (a, lam): unit coefficients and the smallest eigenvalue lam, the
    minimum of sum f^2 / sum |grad f|^2.
    Cost: Theta(m n^2 d) to build M and N for m points, n basis functions in
    dimension d, plus Theta(n^3) per Jacobi sweep.
    """
    n = len(basis)
    consts = [j for j, p in enumerate(basis) if all(sum(e) == 0 for e in p)]
    if len(consts) > 1 or (consts and consts[0] != n - 1):
        raise ValueError("at most one constant basis function, placed last")
    M = [[0] * n for _ in range(n)]                                     # @line L1
    N = [[0] * n for _ in range(n)]
    for x in points:                                                    # @line L2
        u = [evaluate(p, x) for p in basis]
        J = [gradient(p, x) for p in basis]
        for j in range(n):
            for k in range(n):
                M[j][k] += u[j] * u[k]                                  # @line L3
                N[j][k] += dot(J[j], J[k])                              # @line L4
    nb = n - 1 if consts else n                                         # @line L5
    if consts:
        mcc = float(M[n - 1][n - 1])
        Mp = [[float(M[j][k]) - float(M[j][n - 1]) * float(M[n - 1][k]) / mcc for k in range(nb)]
              for j in range(nb)]                                       # @line L6
    else:
        Mp = [[float(M[j][k]) for k in range(nb)] for j in range(nb)]
    Nb = [[float(N[j][k]) for k in range(nb)] for j in range(nb)]
    L = cholesky(Nb, 1e-12)                                             # @line L7
    X = transpose([lower_solve(L, col) for col in Mp])  # X = L^-1 M', solved column by column (M' is symmetric)
    C = [lower_solve(L, row) for row in X]              # column k of C^T is L^-1 (row k of X), so C = L^-1 M' L^-T
    C = [[(C[j][k] + C[k][j]) / 2 for k in range(nb)] for j in range(nb)]
    vals, vecs = jacobi_eigen(C)                                        # @line L8
    lam, y = vals[0], vecs[0]
    b = upper_solve_t(L, y)                                             # @line L9
    a = list(b)
    if consts:
        a.append(-sum(float(M[n - 1][k]) * b[k] for k in range(nb)) / mcc)
    s = norm(a)
    return [v / s for v in a], max(lam, 0.0)                            # @line L10
