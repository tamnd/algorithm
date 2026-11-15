# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ida-pbc/. The authors are listed in prov/ST8SKY.jsonl.

"""Interconnection and damping assignment (IDA-PBC): the control at one point.

The plant is the port-Hamiltonian system

    x' = (J(x) - R(x)) grad H(x) + g(x) u,

and the design is a target system

    x' = (J_d(x) - R_d(x)) grad H_d(x),

with J_d = -J_d^T, R_d = R_d^T >= 0 and H_d with a strict minimum at the
target point. The target is reachable by u at x if and only if the matching
equation

    g(x) u = (J_d - R_d) grad H_d - (J - R) grad H

has a solution; when g has full column rank, the solution is
u = (g^T g)^(-1) g^T w with w the right side, and it solves the equation
exactly when the residual w - g u is zero.

matching_control evaluates this at one point. With int or Fraction inputs
and tol = 0 the result is exact; with floats, pass a small tol.
"""

from fractions import Fraction

__all__ = ["matching_control", "MatchingError"]


class MatchingError(ValueError):
    """The matching equation has no solution at this point."""


def _matvec(A, v):
    return [sum(a * b for a, b in zip(row, v)) for row in A]


def _div(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return Fraction(a, b)
    return a / b


def _solve(M, v):
    # Gauss-Jordan elimination with row pivoting on a small square system.
    n = len(M)
    A = [list(M[i]) + [v[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(A[i][c]))
        if A[p][c] == 0:
            raise ValueError("g must have full column rank")
        A[c], A[p] = A[p], A[c]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = _div(A[i][c], A[c][c])
                A[i] = [a - f * b for a, b in zip(A[i], A[c])]
    return [_div(A[i][n], A[i][i]) for i in range(n)]


def matching_control(jr, grad_h, g, jrd, grad_hd, tol=0):
    """Return u with g u = (J_d - R_d) grad H_d - (J - R) grad H.

    jr = J - R and jrd = J_d - R_d are n x n, g is n x m (a list of n rows),
    grad_h and grad_hd are vectors of length n, all evaluated at the same x.
    Raises MatchingError if the residual exceeds tol in some component.
    """
    n = len(grad_h)
    if len(g) != n or len(jr) != n or len(jrd) != n or len(grad_hd) != n:
        raise ValueError("dimensions do not match")
    m = len(g[0])
    a = _matvec(jr, grad_h)  # @line L1
    c = _matvec(jrd, grad_hd)  # @line L2
    w = [ci - ai for ci, ai in zip(c, a)]  # @line L3
    gtg = [[sum(g[k][i] * g[k][j] for k in range(n)) for j in range(m)] for i in range(m)]
    gtw = [sum(g[k][i] * w[k] for k in range(n)) for i in range(m)]
    u = _solve(gtg, gtw)  # @line L4
    rho = [wi - gi for wi, gi in zip(w, _matvec(g, u))]  # @line L5
    if any(abs(r) > tol for r in rho):  # @line L6
        raise MatchingError("the matching equation has no solution at this point")
    return u  # @line L7
