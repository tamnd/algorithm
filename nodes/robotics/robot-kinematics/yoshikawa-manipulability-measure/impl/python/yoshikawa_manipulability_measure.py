# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yoshikawa-manipulability-measure/. The authors are listed in prov/WRDGRM.jsonl.
"""Yoshikawa's manipulability measure w = sqrt(det(J J^T)) and related numbers.

J is an m by n Jacobian with m <= n. w is the product of the m singular
values of J, and it is zero exactly when J has rank below m.

- manipulability(j) computes w from the determinant of J J^T.
- singular_values(j) computes the singular values as the square roots of
  the eigenvalues of J J^T, by the cyclic Jacobi eigenvalue method.
- condition_number(j) is sigma_max / sigma_min (infinite at a singularity).

Matrices are lists of rows.
"""

import math

import rbm


def manipulability(j):
    """Return sqrt(det(J J^T)); raise ValueError if J has more rows than columns."""
    if len(j) > len(j[0]):
        raise ValueError("w is defined for m <= n only")
    a = rbm.mul(j, rbm.transpose(j))  # @line L1
    d = rbm.det(a)  # @line L2
    return math.sqrt(max(d, 0.0))  # @line L3


def sym_eigenvalues(a, sweeps=50):
    """Return the eigenvalues of the symmetric matrix a by cyclic Jacobi rotations."""
    n = len(a)
    m = [list(map(float, row)) for row in a]
    for _ in range(sweeps):
        off = sum(m[i][k] ** 2 for i in range(n) for k in range(n) if i != k)
        if off <= 1e-30 * max(1.0, sum(m[i][i] ** 2 for i in range(n))):
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if m[p][q] == 0.0:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    mkp, mkq = m[k][p], m[k][q]
                    m[k][p] = c * mkp - s * mkq
                    m[k][q] = s * mkp + c * mkq
                for k in range(n):
                    mpk, mqk = m[p][k], m[q][k]
                    m[p][k] = c * mpk - s * mqk
                    m[q][k] = s * mpk + c * mqk
    return sorted((m[i][i] for i in range(n)), reverse=True)


def singular_values(j):
    """Return the min(m, n) singular values of J, largest first."""
    if len(j) <= len(j[0]):
        a = rbm.mul(j, rbm.transpose(j))
    else:
        a = rbm.mul(rbm.transpose(j), j)
    return [math.sqrt(max(x, 0.0)) for x in sym_eigenvalues(a)]


def condition_number(j):
    """Return sigma_max / sigma_min, or infinity if sigma_min is zero."""
    s = singular_values(j)
    return math.inf if s[-1] == 0.0 else s[0] / s[-1]
