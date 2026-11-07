# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jacobi-eigenvalue-algorithm/. The authors are listed in prov/HTTEGG.jsonl.

"""Cyclic Jacobi eigenvalue algorithm for a real symmetric matrix.

jacobi(a) returns (lam, v, sweeps, rotations, converged) with A v_i = lam_i v_i,
v orthogonal (columns are the eigenvectors), and lam in the order of the final
diagonal (not sorted). Standard library only; a is a list of lists of floats.
"""

import math

U = 2.0 ** -53  # unit roundoff of IEEE double precision


def off(a):
    """Frobenius norm of the off-diagonal part."""
    n = len(a)
    return math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j))


def rotation(app, aqq, apq):
    """Return (c, s, t) with t = s / c the smaller root, so that the rotation zeroes a_pq."""
    tau = (aqq - app) / (2.0 * apq)
    if tau >= 0.0:
        t = 1.0 / (tau + math.hypot(1.0, tau))
    else:
        t = -1.0 / (-tau + math.hypot(1.0, tau))
    c = 1.0 / math.hypot(1.0, t)
    return c, t * c, t


def rotate(a, v, p, q, c, s, t):
    """A <- J^T A J and V <- V J for the rotation J in the (p, q) plane."""
    n = len(a)
    apq = a[p][q]
    a[p][p] -= t * apq
    a[q][q] += t * apq
    a[p][q] = a[q][p] = 0.0
    for r in range(n):
        if r != p and r != q:
            arp, arq = a[r][p], a[r][q]
            a[r][p] = a[p][r] = c * arp - s * arq
            a[r][q] = a[q][r] = s * arp + c * arq
    for r in range(n):
        vrp, vrq = v[r][p], v[r][q]
        v[r][p] = c * vrp - s * vrq
        v[r][q] = s * vrp + c * vrq


def jacobi(a, tol=None, max_sweeps=60):
    """Cyclic-by-row Jacobi with the relative threshold |a_pq| <= tol sqrt(|a_pp a_qq|)."""
    n = len(a)
    a = [[float(t) for t in row] for row in a]
    if tol is None:
        tol = n * U
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]  # @line L1
    rotations = 0
    for sweep in range(1, max_sweeps + 1):  # @line L2
        done = True
        for p in range(n - 1):  # @line L3
            for q in range(p + 1, n):
                apq = a[p][q]
                if apq == 0.0 or abs(apq) <= tol * math.sqrt(abs(a[p][p] * a[q][q])):  # @line L4
                    continue
                done = False
                c, s, t = rotation(a[p][p], a[q][q], apq)  # @line L5
                rotate(a, v, p, q, c, s, t)  # @line L6: also V <- V J
                rotations += 1
        if done:  # @line L7
            return [a[i][i] for i in range(n)], v, sweep - 1, rotations, True
    return [a[i][i] for i in range(n)], v, max_sweeps, rotations, False  # @line L8


def jacobi_classical(a, tol=None, max_rotations=100000):
    """Classical Jacobi: rotate on the largest off-diagonal entry; return the history of off(A)."""
    n = len(a)
    a = [[float(t) for t in row] for row in a]
    if tol is None:
        tol = n * U
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    scale = math.sqrt(sum(t * t for row in a for t in row))
    history = [off(a)]
    while len(history) <= max_rotations and history[-1] > tol * scale:
        best, p, q = -1.0, 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > best:
                    best, p, q = abs(a[i][j]), i, j
        c, s, t = rotation(a[p][p], a[q][q], a[p][q])
        rotate(a, v, p, q, c, s, t)
        history.append(off(a))
    return [a[i][i] for i in range(n)], v, history
