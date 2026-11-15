# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/infinite-horizon-lqr/. The authors are listed in prov/G9RNJT.jsonl.

"""Infinite-horizon linear quadratic regulator, as the limit of the finite horizon.

Discrete time: x_(k+1) = A x_k + B u_k, cost sum_(k>=0) x_k^T Q x_k + u_k^T R u_k.
The finite-horizon cost matrices of horizon j, computed by the backward
Riccati recursion from P = P0 (default 0), converge to the stabilizing
solution of the DARE

    P = Q + A^T P A - A^T P B (R + B^T P B)^(-1) B^T P A

when (A, B) is stabilizable and (Q^(1/2), A) is detectable. The gain is
K = (R + B^T P B)^(-1) B^T P A, the control is u = -K x, and A - B K is Schur.

Continuous time: x' = A x + B u, cost integral of x^T Q x + u^T R u. The
Riccati differential equation dP/dtau = A^T P + P A - P B R^(-1) B^T P + Q
in the backward time tau is integrated from P(0) = P0 with RK4 until the
CARE residual is small. The gain is K = R^(-1) B^T P and A - B K is Hurwitz.

Both functions check the closed loop at the end and raise ValueError if it
is not Schur (or Hurwitz). This happens, for example, when (Q^(1/2), A) is
not detectable and the iteration from 0 stops at a solution that does not
stabilize.
"""

from ctlmat import add, charpoly, mul, polyroots, scale, solve, sub, transpose

__all__ = ["dlqr", "lqr", "dare_residual", "care_residual", "closed_loop_eigs"]


def _fro(a):
    return sum(abs(v) ** 2 for row in a for v in row) ** 0.5


def _sym(p):
    return [[(p[i][j] + p[j][i]) / 2 for j in range(len(p))] for i in range(len(p))]


def _float(a):
    return [[float(v) for v in row] for row in a]


def closed_loop_eigs(A, B, K):
    """Return the eigenvalues of A - B K, from its characteristic polynomial."""
    return polyroots(charpoly(sub(A, mul(B, K))))


def _dgain(A, B, R, P):
    pb = mul(P, B)
    return solve(add(R, mul(transpose(B), pb)), mul(transpose(pb), A))


def dare_residual(A, B, Q, R, P):
    """Return Q + A^T P A - A^T P B (R + B^T P B)^(-1) B^T P A - P."""
    k = _dgain(A, B, R, P)
    at = transpose(A)
    return sub(sub(add(Q, mul(at, mul(P, A))), mul(at, mul(mul(P, B), k))), P)


def care_residual(A, B, Q, R, P):
    """Return A^T P + P A - P B R^(-1) B^T P + Q."""
    pb = mul(P, B)
    return add(add(mul(transpose(A), P), mul(P, A)), sub(Q, mul(pb, solve(R, transpose(pb)))))


def dlqr(A, B, Q, R, P0=None, tol=1e-14, max_iter=100000):
    """Return (P, K, iterations) for the discrete-time infinite-horizon problem."""
    A, B, Q, R = _float(A), _float(B), _float(Q), _float(R)
    n = len(A)
    p = [[0.0] * n for _ in range(n)] if P0 is None else _float(P0)  # @line L1
    at = transpose(A)
    for it in range(1, max_iter + 1):  # @line L2
        k = _dgain(A, B, R, p)  # @line L3
        new = _sym(sub(add(Q, mul(at, mul(p, A))), mul(at, mul(mul(p, B), k))))  # @line L4
        delta = _fro(sub(new, p))  # @line L5
        p = new
        if delta <= tol * max(_fro(p), 1e-300):  # @line L6
            break
    else:
        raise ValueError("the Riccati recursion did not converge")
    k = _dgain(A, B, R, p)  # @line L7
    if max(abs(z) for z in closed_loop_eigs(A, B, k)) >= 1:  # @line L8
        raise ValueError("A - B K is not Schur: no stabilizing limit from this start")
    return p, k, it


def lqr(A, B, Q, R, P0=None, tol=1e-13, h=None, max_steps=200000):
    """Return (P, K, steps) for the continuous-time infinite-horizon problem.

    h is the RK4 step in the backward time. The default is
    0.5 / (1 + ||H||_inf) for the Hamiltonian matrix H, so that h times
    every eigenvalue of the linearized flow near the solution stays inside
    the stability region of RK4.
    """
    A, B, Q, R = _float(A), _float(B), _float(Q), _float(R)
    n = len(A)
    g = mul(B, solve(R, transpose(B)))
    if h is None:
        rows = [sum(abs(v) for v in A[i]) + sum(abs(v) for v in g[i]) for i in range(n)]
        rows += [sum(abs(v) for v in Q[i]) + sum(abs(A[j][i]) for j in range(n)) for i in range(n)]
        h = 0.5 / (1.0 + max(rows))
    p = [[0.0] * n for _ in range(n)] if P0 is None else _float(P0)

    def f(m):
        return care_residual(A, B, Q, R, m)

    scale_q = _fro(Q) + _fro(A) + _fro(g) + 1e-300
    for step in range(1, max_steps + 1):
        k1 = f(p)
        size = scale_q * (1.0 + _fro(p)) ** 2
        if _fro(k1) <= tol * size:
            break
        k2 = f(add(p, scale(h / 2, k1)))
        k3 = f(add(p, scale(h / 2, k2)))
        k4 = f(add(p, scale(h, k3)))
        p = _sym(add(p, scale(h / 6, add(add(k1, scale(2, k2)), add(scale(2, k3), k4)))))
    else:
        raise ValueError("the Riccati differential equation did not reach a steady state")
    k = solve(R, mul(transpose(B), p))
    if max(z.real for z in closed_loop_eigs(A, B, k)) >= 0:
        raise ValueError("A - B K is not Hurwitz: no stabilizing limit from this start")
    return p, k, step
