# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/canonical-correlation-analysis/. The authors are listed in prov/2S7QFD.jsonl.

"""Canonical correlation analysis by the SVD of C_XX^(-1/2) C_XY C_YY^(-1/2).

The covariances use the divisor n. Ridge terms kx and ky give regularized CCA:
C_XX + kx I and C_YY + ky I replace the two covariance blocks. The SVD of the
small p x q matrix T comes from a Jacobi eigensolver applied to T T^T.
"""

import math

Vector = list[float]
Matrix = list[list[float]]


def transpose(a: Matrix) -> Matrix:
    return [list(col) for col in zip(*a)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def jacobi_eigh(a: Matrix, tol: float = 1e-14, max_sweeps: int = 100) -> tuple[Vector, Matrix]:
    """Eigenvalues (descending) and eigenvectors (as columns) of a symmetric matrix."""
    d = len(a)
    m = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
    for _ in range(max_sweeps):
        off = sum(m[i][j] ** 2 for i in range(d) for j in range(d) if i != j)
        scale = sum(m[i][i] ** 2 for i in range(d)) + off
        if off <= tol * tol * max(scale, 1e-300):
            break
        for p in range(d - 1):
            for q in range(p + 1, d):
                if m[p][q] == 0.0:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(d):
                    m[k][p], m[k][q] = c * m[k][p] - s * m[k][q], s * m[k][p] + c * m[k][q]
                for k in range(d):
                    m[p][k], m[q][k] = c * m[p][k] - s * m[q][k], s * m[p][k] + c * m[q][k]
                for k in range(d):
                    v[k][p], v[k][q] = c * v[k][p] - s * v[k][q], s * v[k][p] + c * v[k][q]
    order = sorted(range(d), key=lambda i: -m[i][i])
    return [m[i][i] for i in order], [[v[r][i] for i in order] for r in range(d)]


def inv_sqrt(a: Matrix) -> Matrix:
    """The symmetric inverse square root of a symmetric positive definite matrix."""
    lam, vec = jacobi_eigh(a)
    if lam[-1] <= 0.0:
        raise ValueError("covariance block is not positive definite; add a ridge term")
    d = len(a)
    return [[sum(vec[i][t] * vec[j][t] / math.sqrt(lam[t]) for t in range(d)) for j in range(d)] for i in range(d)]


def centre(xs: list[Vector]) -> list[Vector]:
    n, d = len(xs), len(xs[0])
    m = [sum(x[j] for x in xs) / n for j in range(d)]
    return [[x[j] - m[j] for j in range(d)] for x in xs]


def cross_cov(xs: list[Vector], ys: list[Vector]) -> Matrix:
    n = len(xs)
    return [[sum(x[i] * y[j] for x, y in zip(xs, ys)) / n for j in range(len(ys[0]))] for i in range(len(xs[0]))]


def cca(xs: list[Vector], ys: list[Vector], kx: float = 0.0, ky: float = 0.0) -> tuple[Vector, list[Vector], list[Vector]]:
    """Return the canonical correlations rho_1 >= rho_2 >= ... and the weight vectors a_i, b_i.

    The weights satisfy a_i^T C_XX a_j = [i == j] and b_i^T C_YY b_j = [i == j]
    (with the ridge terms included in C_XX and C_YY).
    """
    xc, yc = centre(xs), centre(ys)  # @line L1
    p, q = len(xs[0]), len(ys[0])
    cxx = cross_cov(xc, xc)
    cyy = cross_cov(yc, yc)
    cxy = cross_cov(xc, yc)  # @line L2
    for i in range(p):
        cxx[i][i] += kx
    for j in range(q):
        cyy[j][j] += ky  # @line L3
    rx, ry = inv_sqrt(cxx), inv_sqrt(cyy)  # @line L4
    t = matmul(matmul(rx, cxy), ry)  # @line L5
    if p > q:  # work with the smaller side, then swap back
        rho, b_dirs, a_dirs = _svd_pairs(transpose(t), ry, rx)
        return rho, a_dirs, b_dirs
    return _svd_pairs(t, rx, ry)


def _svd_pairs(t: Matrix, rx: Matrix, ry: Matrix) -> tuple[Vector, list[Vector], list[Vector]]:
    """t is p x q with p <= q. Return the singular values and the mapped singular vectors."""
    p, q = len(t), len(t[0])
    lam, u = jacobi_eigh(matmul(t, transpose(t)))  # @line L6
    rho, a_dirs, b_dirs = [], [], []
    for k in range(p):
        s = math.sqrt(max(lam[k], 0.0))
        if s <= 1e-12:
            break
        uk = [u[i][k] for i in range(p)]
        vk = [sum(t[i][j] * uk[i] for i in range(p)) / s for j in range(q)]
        rho.append(s)
        a_dirs.append([sum(rx[i][j] * uk[j] for j in range(p)) for i in range(p)])  # @line L7
        b_dirs.append([sum(ry[i][j] * vk[j] for j in range(q)) for i in range(q)])
    return rho, a_dirs, b_dirs  # @line L8


def correlation(xs: list[Vector], ys: list[Vector], a: Vector, b: Vector) -> float:
    """The sample correlation of a^T x and b^T y."""
    u = [sum(ai * xi for ai, xi in zip(a, x)) for x in xs]
    v = [sum(bi * yi for bi, yi in zip(b, y)) for y in ys]
    n = len(u)
    mu, mv = sum(u) / n, sum(v) / n
    suv = sum((x - mu) * (y - mv) for x, y in zip(u, v))
    suu = sum((x - mu) ** 2 for x in u)
    svv = sum((y - mv) ** 2 for y in v)
    return suv / math.sqrt(suu * svv)
