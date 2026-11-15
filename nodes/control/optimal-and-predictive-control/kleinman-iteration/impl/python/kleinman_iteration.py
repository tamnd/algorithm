# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kleinman-iteration/. The authors are listed in prov/1GNVWG.jsonl.

"""Kleinman iteration: Newton's method for the algebraic Riccati equation.

Continuous time (Kleinman 1968). Start from a gain K_0 with A - B K_0
Hurwitz. For k = 0, 1, 2, ... solve the Lyapunov equation

    (A - B K_k)^T P_k + P_k (A - B K_k) + Q + K_k^T R K_k = 0

and set K_(k+1) = R^(-1) B^T P_k. If (Q^(1/2), A) is detectable, every
A - B K_k is Hurwitz, P_0 >= P_1 >= ... >= P, and P_k converges
quadratically to the stabilizing solution P of the CARE
A^T P + P A - P B R^(-1) B^T P + Q = 0.

Discrete time (Hewer 1971). Start from K_0 with A - B K_0 Schur, solve the
Stein equation P_k = (A - B K_k)^T P_k (A - B K_k) + Q + K_k^T R K_k and set
K_(k+1) = (R + B^T P_k B)^(-1) B^T P_k A.

Each linear matrix equation is solved in its Kronecker form, a dense linear
system of size n^2, which costs O(n^6). This is fine for small n; a
Bartels-Stewart solver brings one step down to O(n^3). With int or Fraction
data the iteration is exact.
"""

from ctlmat import add, charpoly, eye, kron, mul, polyroots, solve, sub, transpose, unvec, vec

__all__ = ["lyap", "stein", "kleinman", "hewer", "care_residual", "dare_residual"]


def _is_float(a):
    return any(isinstance(v, float) for row in a for v in row)


def _sym(p):
    if not _is_float(p):
        return p
    return [[(p[i][j] + p[j][i]) / 2 for j in range(len(p))] for i in range(len(p))]


def _maxabs(a):
    return max(abs(v) for row in a for v in row)


def lyap(F, W):
    """Return X with F^T X + X F + W = 0, from (I kron F^T + F^T kron I) vec X = -vec W.

    The solution is unique when no two eigenvalues of F sum to 0, for
    example when F is Hurwitz. Cost O(n^6).
    """
    n = len(F)
    ft = transpose(F)
    big = add(kron(eye(n), ft), kron(ft, eye(n)))
    return _sym(unvec(solve(big, [-v for v in vec(W)]), n))


def stein(F, W):
    """Return X with X = F^T X F + W, from (I - F^T kron F^T) vec X = vec W.

    The solution is unique when no product of two eigenvalues of F is 1, for
    example when F is Schur. Cost O(n^6).
    """
    n = len(F)
    ft = transpose(F)
    big = sub(eye(n * n), kron(ft, ft))
    return _sym(unvec(solve(big, vec(W)), n))


def _check_start(F, discrete):
    eigs = polyroots(charpoly(F))
    ok = all(abs(e) < 1 for e in eigs) if discrete else all(e.real < 0 for e in eigs)
    if not ok:
        raise ValueError("the initial gain K_0 does not stabilize A - B K_0")


def kleinman(A, B, Q, R, K0, tol=1e-13, max_iter=50, steps=None):
    """Return (P, K, Ps) by Kleinman's iteration for the CARE.

    Ps is the list P_0, P_1, ... of the cost matrices of the gains K_0,
    K_1, ...; P is the last of them and K = R^(-1) B^T P. The loop stops
    when the largest entry of P_k - P_(k-1) is at most tol times the largest
    entry of P_k, or after max_iter steps; with steps given it does exactly
    that many steps (useful with exact data). Precondition: R > 0 and
    A - B K0 Hurwitz (checked). Cost O(n^6 + n^2 m + m^3) per step with the
    Kronecker solve.
    """
    K = [list(row) for row in K0]  # @line L1
    _check_start(sub(A, mul(B, K)), False)
    bt = transpose(B)
    Ps = []
    limit = steps if steps is not None else max_iter
    for _ in range(limit):  # @line L2
        ak = sub(A, mul(B, K))  # @line L3
        P = lyap(ak, add(Q, mul(transpose(K), mul(R, K))))  # @line L4
        K = solve(R, mul(bt, P))  # @line L5
        Ps.append(P)
        if steps is None and len(Ps) > 1 and _maxabs(sub(P, Ps[-2])) <= tol * max(_maxabs(P), 1e-300):  # @line L6
            break
    return Ps[-1], K, Ps


def hewer(A, B, Q, R, K0, tol=1e-13, max_iter=50, steps=None):
    """Return (P, K, Ps) by Hewer's iteration for the DARE.

    Same conventions as kleinman. Precondition: R > 0 and A - B K0 Schur
    (checked). K = (R + B^T P B)^(-1) B^T P A for the last P.
    """
    K = [list(row) for row in K0]
    _check_start(sub(A, mul(B, K)), True)
    bt = transpose(B)
    Ps = []
    limit = steps if steps is not None else max_iter
    for _ in range(limit):
        ak = sub(A, mul(B, K))
        P = stein(ak, add(Q, mul(transpose(K), mul(R, K))))
        pb = mul(P, B)
        K = solve(add(R, mul(bt, pb)), mul(transpose(pb), A))
        Ps.append(P)
        if steps is None and len(Ps) > 1 and _maxabs(sub(P, Ps[-2])) <= tol * max(_maxabs(P), 1e-300):
            break
    return Ps[-1], K, Ps


def care_residual(A, B, Q, R, P):
    """Return A^T P + P A - P B R^(-1) B^T P + Q."""
    pb = mul(P, B)
    return add(sub(add(mul(transpose(A), P), mul(P, A)), mul(pb, solve(R, transpose(pb)))), Q)


def dare_residual(A, B, Q, R, P):
    """Return A^T P A - A^T P B (R + B^T P B)^(-1) B^T P A + Q - P."""
    pb = mul(P, B)
    k = solve(add(R, mul(transpose(B), pb)), mul(transpose(pb), A))
    at = transpose(A)
    return sub(add(sub(mul(at, mul(P, A)), mul(at, mul(pb, k))), Q), P)
