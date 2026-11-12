# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/principal-component-analysis/. The authors are listed in prov/45RF44.jsonl.

"""Principal component analysis by the eigenvectors of the covariance matrix.

The eigenproblem is solved by the cyclic Jacobi method, written here with the
standard library only. The data matrix X has the points as rows (n x d).
"""

import math
from dataclasses import dataclass

Matrix = list[list[float]]


def jacobi_eigen(a: Matrix, tol: float = 1e-12, max_sweeps: int = 100) -> tuple[list[float], Matrix]:
    """Eigenvalues and eigenvectors of a symmetric matrix by cyclic Jacobi.

    Returns (values, vectors) with vectors[j] the unit eigenvector of
    values[j], sorted so that values are non-increasing. Each sweep costs
    O(d^3) operations; the number of sweeps is small in practice because the
    method converges quadratically. Precondition: a is symmetric.
    """
    d = len(a)
    m = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
    scale = math.sqrt(sum(x * x for row in a for x in row)) or 1.0
    for _ in range(max_sweeps):
        off = math.sqrt(sum(m[p][q] ** 2 for p in range(d) for q in range(d) if p != q))
        if off <= tol * scale:
            break
        for p in range(d - 1):
            for q in range(p + 1, d):
                if abs(m[p][q]) <= 1e-300:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(d):  # columns p and q of m and of v
                    mkp, mkq = m[k][p], m[k][q]
                    m[k][p], m[k][q] = c * mkp - s * mkq, s * mkp + c * mkq
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
                for k in range(d):  # rows p and q of m
                    mpk, mqk = m[p][k], m[q][k]
                    m[p][k], m[q][k] = c * mpk - s * mqk, s * mpk + c * mqk
    order = sorted(range(d), key=lambda j: -m[j][j])
    values = [m[j][j] for j in order]
    vectors = []
    for j in order:
        col = [v[i][j] for i in range(d)]
        big = max(range(d), key=lambda i: abs(col[i]))
        sign = 1.0 if col[big] >= 0 else -1.0  # fix the sign: largest entry positive
        vectors.append([sign * x for x in col])
    return values, vectors


@dataclass
class PCAResult:
    mean: list[float]
    components: Matrix  # k unit vectors in R^d, the principal directions
    eigenvalues: list[float]  # all d eigenvalues of the covariance, non-increasing
    scores: Matrix  # n x k, the coordinates of the centered points


def pca(x: Matrix, k: int, ddof: int = 0) -> PCAResult:
    """Rank-k PCA of the rows of x.

    The covariance uses the divisor n - ddof (ddof = 0 is the 1/n
    convention). Cost: O(n d^2) for the covariance and O(d^3) per Jacobi
    sweep. Precondition: 0 <= k <= d and n > ddof.
    """
    n, d = len(x), len(x[0])
    mean = [sum(row[j] for row in x) / n for j in range(d)]  # @line L1
    xc = [[row[j] - mean[j] for j in range(d)] for row in x]  # @line L2
    cov = [[sum(r[a] * r[b] for r in xc) / (n - ddof) for b in range(d)] for a in range(d)]  # @line L3
    values, vectors = jacobi_eigen(cov)  # @line L4
    w = vectors[:k]  # @line L5
    scores = [[sum(r[j] * c[j] for j in range(d)) for c in w] for r in xc]  # @line L6
    return PCAResult(mean, w, values, scores)  # @line L7


def reconstruct(res: PCAResult) -> Matrix:
    """Map the scores back: x_hat = mean + sum_j z_j w_j."""
    d = len(res.mean)
    return [
        [res.mean[j] + sum(z[c] * res.components[c][j] for c in range(len(z))) for j in range(d)]
        for z in res.scores
    ]
