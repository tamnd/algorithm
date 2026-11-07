# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minres/. The authors are listed in prov/NAYDFS.jsonl.

"""MINRES (Paige and Saunders, 1975) for A x = b with A symmetric, possibly indefinite.

A matrix is a list of rows; row i is a list of (j, a_ij) pairs with a_ij != 0.
from_dense converts a list of lists. The method needs only products A v, so
any symmetric operator given as a function can be passed instead (see minres).
"""

import math
from typing import Callable

SparseRows = list[list[tuple[int, float]]]
MatVec = Callable[[list[float]], list[float]]


def from_dense(a: list[list[float]]) -> SparseRows:
    """Keep the nonzero entries of each row."""
    return [[(j, v) for j, v in enumerate(row) if v != 0] for row in a]


def matvec(rows: SparseRows, x: list[float]) -> list[float]:
    """y = A x, in 2 nnz(A) flops."""
    return [sum(v * x[j] for j, v in row) for row in rows]


def _dot(x: list[float], y: list[float]) -> float:
    return math.fsum(a * b for a, b in zip(x, y))


def minres(a, b: list[float], x0: list[float] | None = None, tol: float = 1e-10,
           maxiter: int | None = None, history: list[float] | None = None
           ) -> tuple[list[float], int, bool]:
    """Solve A x = b for symmetric A by minimizing ||b - A x_k||_2 over x0 + K_k(A, r0).

    a is SparseRows or a function v -> A v. Stops when the recurrence residual
    |eta| <= tol ||b||_2. Returns (x, k, converged); if history is a list, the
    recurrence residual norm after each step is appended to it.
    Cost per step: one product with A plus about 16n flops; 7 vectors of storage.
    A must be symmetric; this is not checked.
    """
    av: MatVec = a if callable(a) else (lambda v: matvec(a, v))
    n = len(b)
    if maxiter is None:
        maxiter = 10 * n
    x = list(x0) if x0 is not None else [0.0] * n
    ax = av(x)
    r = [bi - axi for bi, axi in zip(b, ax)]  # @line L1
    gamma = math.sqrt(_dot(r, r))
    nb = math.sqrt(_dot(b, b))
    target = tol * (nb if nb > 0 else 1.0)
    if gamma <= target:
        return x, 0, True
    v_old = [0.0] * n  # @line L2
    v = r
    w_old = [0.0] * n
    w = [0.0] * n
    eta = gamma
    c_old, c, s_old, s = 1.0, 1.0, 0.0, 0.0
    anorm = 0.0  # running estimate of ||A||_2 from the Lanczos coefficients
    small = 10.0 * n * 2.0 ** -53
    for k in range(1, maxiter + 1):  # @line L3
        v = [vi / gamma for vi in v]  # @line L4
        p = av(v)
        delta = _dot(p, v)
        v_new = [pi - delta * vi - gamma * voi for pi, vi, voi in zip(p, v, v_old)]  # @line L5
        gamma_new = math.sqrt(_dot(v_new, v_new))
        anorm = max(anorm, math.sqrt(gamma * gamma + delta * delta + gamma_new * gamma_new))
        a0 = c * delta - c_old * s * gamma  # @line L6
        a2 = s * delta + c_old * c * gamma
        a3 = s_old * gamma
        a1 = math.hypot(a0, gamma_new)
        if a1 <= small * anorm:  # T_k singular and K_k invariant: b is not in range(A)
            return x, k - 1, False
        c_new, s_new = a0 / a1, gamma_new / a1  # @line L7
        w_new = [(vi - a3 * woi - a2 * wi) / a1 for vi, woi, wi in zip(v, w_old, w)]  # @line L8
        x = [xi + c_new * eta * wi for xi, wi in zip(x, w_new)]  # @line L9
        eta = -s_new * eta
        if history is not None:
            history.append(abs(eta))
        if abs(eta) <= target:  # @line L10
            return x, k, True
        if gamma_new <= small * anorm:  # invariant subspace found: x is the exact minimizer
            return x, k, False
        v_old, v, gamma = v, v_new, gamma_new  # @line L11
        w_old, w = w, w_new
        c_old, c, s_old, s = c, c_new, s, s_new
    return x, maxiter, False  # @line L12


def residual_norm(a, b: list[float], x: list[float]) -> float:
    """||b - A x||_2 computed directly."""
    av: MatVec = a if callable(a) else (lambda v: matvec(a, v))
    return math.sqrt(_dot(*(2 * [[bi - y for bi, y in zip(b, av(x))]])))


def interval_bound(c_lo: float, d_hi: float, k: int) -> float:
    """Bound on ||r_k|| / ||r_0|| for spectrum in [-d, -c] U [c, d]: 2 ((d - c)/(d + c))^floor(k/2)."""
    q = (d_hi - c_lo) / (d_hi + c_lo)
    return 2.0 * q ** (k // 2)
