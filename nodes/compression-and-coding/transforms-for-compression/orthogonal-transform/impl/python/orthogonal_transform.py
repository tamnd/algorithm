# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orthogonal-transform/. The authors are listed in prov/56ZDC1.jsonl.

"""Orthogonal and unitary transforms as matrices, in pure Python.

A real square matrix A is orthogonal when A^T A = I; a complex one is unitary
when A^H A = I. The inverse is the (conjugate) transpose, and the transform
keeps the Euclidean norm and the squared error.
"""

import cmath
import math
from typing import List, Sequence, Union

Number = Union[float, complex]
Vector = List[Number]
Matrix = List[List[Number]]


def apply(a: Matrix, x: Sequence[Number]) -> Vector:
    """y = A x. Cost Theta(n^2)."""
    return [sum(row[i] * x[i] for i in range(len(x))) for row in a]


def adjoint(a: Matrix) -> Matrix:
    """Conjugate transpose A^H (the transpose for a real matrix)."""
    return [[a[i][j].conjugate() if isinstance(a[i][j], complex) else a[i][j] for i in range(len(a))] for j in range(len(a[0]))]


def inverse_apply(a: Matrix, y: Sequence[Number]) -> Vector:
    """x = A^H y, the inverse of an orthogonal or unitary A."""
    return apply(adjoint(a), y)


def energy(x: Sequence[Number]) -> float:
    """Squared Euclidean norm sum |x_i|^2."""
    return sum(abs(v) ** 2 for v in x)


def is_orthogonal(a: Matrix, tol: float = 1e-12) -> bool:
    """True when A^H A = I within tol in each entry (A square)."""
    n = len(a)
    if any(len(row) != n for row in a):
        return False
    for i in range(n):
        for j in range(n):
            s = sum((a[k][i].conjugate() if isinstance(a[k][i], complex) else a[k][i]) * a[k][j] for k in range(n))
            if abs(s - (1.0 if i == j else 0.0)) > tol:
                return False
    return True


def householder(v: Sequence[float]) -> Matrix:
    """The reflection I - 2 v v^T / (v^T v), an orthogonal and symmetric matrix. v is not zero."""
    n = len(v)
    vv = sum(t * t for t in v)
    return [[(1.0 if i == j else 0.0) - 2.0 * v[i] * v[j] / vv for j in range(n)] for i in range(n)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    """Matrix product A B."""
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def walsh_hadamard(n: int) -> Matrix:
    """Orthonormal Walsh-Hadamard matrix of order n (a power of two), natural (Sylvester) order."""
    h: List[List[float]] = [[1.0]]
    while len(h) < n:
        h = [r + r for r in h] + [r + [-t for t in r] for r in h]
    s = 1.0 / math.sqrt(n)
    return [[t * s for t in r] for r in h]


def unitary_dft(n: int) -> Matrix:
    """Unitary DFT matrix F[k][j] = exp(-2 pi i j k / n) / sqrt(n)."""
    s = 1.0 / math.sqrt(n)
    return [[cmath.exp(-2j * math.pi * j * k / n) * s for j in range(n)] for k in range(n)]


def dct_ii(n: int) -> Matrix:
    """Orthonormal DCT-II matrix of order n."""
    return [[(math.sqrt(1.0 / n) if k == 0 else math.sqrt(2.0 / n)) * math.cos(math.pi * (2 * i + 1) * k / (2 * n)) for i in range(n)] for k in range(n)]
