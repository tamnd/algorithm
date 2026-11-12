# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mercer-theorem/. The authors are listed in prov/Z2X9JZ.jsonl.

"""Numerical checks of Mercer's theorem.

The module has a small cyclic Jacobi eigenvalue solver for symmetric matrices,
Gram matrices of a few kernels, and the closed form Mercer expansion of the
kernel min(x, z) on [0, 1] with the Lebesgue measure:

    min(x, z) = sum_{j >= 1} lam_j e_j(x) e_j(z),
    lam_j = 1 / ((j - 1/2)^2 pi^2),  e_j(x) = sqrt(2) sin((j - 1/2) pi x).
"""

import math
from typing import Callable, Sequence

Matrix = list[list[float]]


def jacobi_eigen(a: Sequence[Sequence[float]], tol: float = 1e-14, max_sweeps: int = 100) -> tuple[list[float], Matrix]:
    """Eigenvalues and eigenvectors of a symmetric matrix by cyclic Jacobi rotations.

    Returns (values, v), where column j of v is a unit eigenvector for
    values[j]. Each rotation zeroes one off-diagonal pair (p, q); a sweep
    visits every pair once. The sum of squares of the off-diagonal entries
    decreases at every rotation, and the method stops when it is below
    tol^2 times the squared Frobenius norm.
    """
    n = len(a)
    m = [[float(a[i][j]) for j in range(n)] for i in range(n)]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    total = sum(m[i][j] ** 2 for i in range(n) for j in range(n))
    for _ in range(max_sweeps):
        off = sum(m[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off <= tol * tol * total:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if m[p][q] == 0.0:
                    continue
                theta = (m[q][q] - m[p][p]) / (2 * m[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):  # rotate columns p and q
                    mkp, mkq = m[k][p], m[k][q]
                    m[k][p], m[k][q] = c * mkp - s * mkq, s * mkp + c * mkq
                for k in range(n):  # rotate rows p and q
                    mpk, mqk = m[p][k], m[q][k]
                    m[p][k], m[q][k] = c * mpk - s * mqk, s * mpk + c * mqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    return [m[i][i] for i in range(n)], v


def gram(xs: Sequence[float], k: Callable[[float, float], float]) -> Matrix:
    return [[k(a, b) for b in xs] for a in xs]


def gaussian(sigma: float) -> Callable[[float, float], float]:
    return lambda x, z: math.exp(-((x - z) ** 2) / (2 * sigma * sigma))


def brownian(x: float, z: float) -> float:
    return min(x, z)


def brownian_eigenvalue(j: int) -> float:
    return 1.0 / (((j - 0.5) * math.pi) ** 2)


def brownian_eigenfunction(j: int, x: float) -> float:
    return math.sqrt(2) * math.sin((j - 0.5) * math.pi * x)


def brownian_partial_sum(n_terms: int, x: float, z: float) -> float:
    return sum(
        brownian_eigenvalue(j) * brownian_eigenfunction(j, x) * brownian_eigenfunction(j, z)
        for j in range(1, n_terms + 1)
    )


def nystrom_eigenvalues(k: Callable[[float, float], float], n: int) -> list[float]:
    """Eigenvalues of K/n on the midpoints of n equal cells of [0, 1], largest first.

    K/n is the matrix of the integral operator f -> int k(., z) f(z) dz with
    the midpoint rule, so its eigenvalues approach those of the operator.
    """
    xs = [(i + 0.5) / n for i in range(n)]
    vals, _ = jacobi_eigen([[k(a, b) / n for b in xs] for a in xs])
    return sorted(vals, reverse=True)
