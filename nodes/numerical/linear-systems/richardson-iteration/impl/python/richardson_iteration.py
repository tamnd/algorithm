# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/richardson-iteration/. The authors are listed in prov/5FXKP1.jsonl.

"""Richardson iteration x_{k+1} = x_k + omega_k (b - A x_k), with A stored by sparse rows.

A matrix is a list of rows; row i is a list of (j, a_ij) pairs. Entries may be
floats or Fractions. A constant omega gives the stationary method; a list of
omegas, used cyclically, gives the nonstationary (Chebyshev) method.
"""

import math
from fractions import Fraction
from typing import Sequence, TypeVar

T = TypeVar("T", float, Fraction)

SparseRows = list[list[tuple[int, T]]]


def from_dense(a: list[list[T]]) -> SparseRows:
    """Keep the nonzero entries of each row."""
    return [[(j, v) for j, v in enumerate(row) if v != 0] for row in a]


def residual(rows: SparseRows, b: list[T], x: list[T]) -> list[T]:
    """r = b - A x: one product with A, 2 nnz(A) flops."""
    return [b[i] - sum(v * x[j] for j, v in row) for i, row in enumerate(rows)]


def norm2(v: list[float]) -> float:
    return math.sqrt(sum(float(t) * float(t) for t in v))


def richardson(rows: SparseRows, b: list[T], omega: T | Sequence[T], x0: list[T] | None = None,
               tol: float = 1e-10, maxiter: int = 10000) -> tuple[list[T], int, bool]:
    """Iterate x <- x + omega_k r until ||r||_2 <= tol ||b||_2 or maxiter steps.

    omega is a number or a list of numbers used cyclically. Returns (x, steps, converged),
    where steps counts the updates made. With constant omega the error obeys
    e_{k+1} = (I - omega A) e_k, so it converges for every x0 iff rho(I - omega A) < 1;
    for symmetric positive definite A that is 0 < omega < 2 / lambda_max.
    Cost per step: one product with A (2 nnz(A) flops) and 4n more flops.
    """
    omegas = list(omega) if isinstance(omega, (list, tuple)) else [omega]
    n = len(rows)
    x = list(x0) if x0 is not None else [b[0] * 0] * n  # @line L1
    target = tol * (norm2(b) or 1.0)
    r = residual(rows, b, x)  # @line L2
    for k in range(maxiter + 1):  # @line L3
        if norm2(r) <= target:  # @line L4
            return x, k, True
        if k == maxiter:
            break
        w = omegas[k % len(omegas)]
        x = [xi + w * ri for xi, ri in zip(x, r)]  # @line L5
        r = residual(rows, b, x)  # @line L6
    return x, maxiter, False  # @line L7


def optimal_omega(lmin: float, lmax: float) -> float:
    """2 / (lambda_min + lambda_max): minimizes rho(I - omega A) over omega for SPD A; rho = (kappa - 1)/(kappa + 1)."""
    return 2.0 / (lmin + lmax)


def chebyshev_omegas(lmin: float, lmax: float, m: int) -> list[float]:
    """Reciprocals of the roots of the degree-m Chebyshev polynomial shifted to [lmin, lmax].

    m steps with these parameters make the residual polynomial the scaled Chebyshev
    polynomial, the optimal one for that interval. The natural order is used; it is
    stable for small m only.
    """
    c, h = (lmax + lmin) / 2.0, (lmax - lmin) / 2.0
    return [1.0 / (c + h * math.cos(math.pi * (2 * j + 1) / (2 * m))) for j in range(m)]
