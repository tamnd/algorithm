# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thomas-algorithm/. The authors are listed in prov/V8X0CR.jsonl.

"""The Thomas algorithm: Gaussian elimination without pivoting for tridiagonal systems.

The matrix has subdiagonal a[1..n-1] (a[0] is ignored), diagonal b[0..n-1] and
superdiagonal c[0..n-2] (c[n-1] is ignored). Row i reads
a[i] x[i-1] + b[i] x[i] + c[i] x[i+1] = d[i]. Entries may be floats or Fractions.
"""

from fractions import Fraction
from typing import TypeVar

T = TypeVar("T", float, Fraction)


class ZeroPivot(ValueError):
    """Raised when a pivot u_i is zero, so elimination without pivoting cannot continue."""


def thomas_factor(a: list[T], b: list[T], c: list[T]) -> tuple[list[T], list[T]]:
    """Return (l, u): multipliers l[1..n-1] (l[0] = 0) and pivots u[0..n-1] with A = L U.

    L is unit lower bidiagonal with subdiagonal l, U is upper bidiagonal with
    diagonal u and superdiagonal c. Raises ZeroPivot. Cost: 3(n - 1) flops.
    """
    n = len(b)
    l = [b[0] * 0] * n
    u = [b[0]] * n
    for i in range(1, n):
        if u[i - 1] == 0:
            raise ZeroPivot("zero pivot at row %d" % (i - 1))
        l[i] = a[i] / u[i - 1]
        u[i] = b[i] - l[i] * c[i - 1]
    if u[n - 1] == 0:
        raise ZeroPivot("zero pivot at row %d" % (n - 1))
    return l, u


def thomas(a: list[T], b: list[T], c: list[T], d: list[T]) -> list[T]:
    """Solve the tridiagonal system without pivoting.

    Precondition: all pivots nonzero (true for matrices diagonally dominant by rows
    or columns, symmetric positive definite, or M-matrices). Raises ZeroPivot.
    Cost: 8n - 7 flops and 4n numbers of storage.
    """
    n = len(b)
    u = [b[0]] * n  # @line L1
    y = [d[0]] * n
    for i in range(1, n):  # @line L2
        if u[i - 1] == 0:
            raise ZeroPivot("zero pivot at row %d" % (i - 1))
        li = a[i] / u[i - 1]  # @line L3
        u[i] = b[i] - li * c[i - 1]  # @line L4
        y[i] = d[i] - li * y[i - 1]  # @line L5
    if u[n - 1] == 0:
        raise ZeroPivot("zero pivot at row %d" % (n - 1))
    x = [y[0]] * n
    x[n - 1] = y[n - 1] / u[n - 1]  # @line L6
    for i in range(n - 2, -1, -1):  # @line L7
        x[i] = (y[i] - c[i] * x[i + 1]) / u[i]
    return x  # @line L8


def thomas_cyclic(a: list[T], b: list[T], c: list[T], d: list[T], alpha: T, beta: T) -> list[T]:
    """Solve a cyclic tridiagonal system: the tridiagonal matrix plus A[0][n-1] = alpha and A[n-1][0] = beta.

    Uses the Sherman-Morrison formula A = T' + u v^T with u = (g, 0, ..., 0, beta),
    v = (1, 0, ..., 0, alpha/g) and g = -b[0], and two Thomas solves with T'. Precondition: n >= 3,
    and the modified tridiagonal matrix and the scalar 1 + v^T z are nonzero pivots.
    Cost: about 17n flops.
    """
    n = len(b)
    gamma = -b[0] if b[0] != 0 else b[0] * 0 - 1
    bb = list(b)
    bb[0] = b[0] - gamma
    bb[n - 1] = b[n - 1] - alpha * beta / gamma
    y = thomas(a, bb, c, d)
    uvec = [b[0] * 0] * n
    uvec[0] = gamma
    uvec[n - 1] = beta
    z = thomas(a, bb, c, uvec)
    vy = y[0] + alpha / gamma * y[n - 1]
    vz = z[0] + alpha / gamma * z[n - 1]
    if 1 + vz == 0:
        raise ZeroPivot("the cyclic matrix is singular")
    f = vy / (1 + vz)
    return [y[i] - f * z[i] for i in range(n)]
