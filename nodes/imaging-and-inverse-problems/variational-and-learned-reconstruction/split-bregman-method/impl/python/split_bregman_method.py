# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-bregman-method/. The authors are listed in prov/4TK5JZ.jsonl.
"""The split Bregman method of Goldstein and Osher (2009).

It solves min_x (1/2)||A x - y||^2 + lam ||Phi x||_1 (anisotropic) or with the
isotropic group norm sum_i |((Phi x)_i, (Phi x)_{i+g})|, by introducing
d = Phi x and applying Bregman iteration to the constraint d = Phi x with one
alternating sweep per step. A and Phi are dense matrices (lists of rows).
The x-step solves (A^T A + mu Phi^T Phi) x = A^T y + mu Phi^T (d - b) with a
Cholesky factor computed once.
"""

import math

Mat = list[list[float]]
Vec = list[float]


def mat_vec(M: Mat, x: Vec) -> Vec:
    return [sum(a * b for a, b in zip(row, x)) for row in M]


def mat_t_vec(M: Mat, y: Vec) -> Vec:
    n = len(M[0])
    out = [0.0] * n
    for row, v in zip(M, y):
        if v != 0.0:
            for j in range(n):
                out[j] += row[j] * v
    return out


def cholesky(M: Mat) -> Mat:
    """Lower triangular L with L L^T = M. Precondition: M symmetric positive definite. Cost O(n^3)."""
    n = len(M)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = M[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                if s <= 0.0:
                    raise ValueError("matrix is not positive definite: ker A and ker Phi meet")
                L[i][i] = math.sqrt(s)
            else:
                L[i][j] = s / L[j][j]
    return L


def chol_solve(L: Mat, r: Vec) -> Vec:
    n = len(r)
    z = [0.0] * n
    for i in range(n):
        z[i] = (r[i] - sum(L[i][k] * z[k] for k in range(i))) / L[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (z[i] - sum(L[k][i] * x[k] for k in range(i + 1, n))) / L[i][i]
    return x


def shrink(v: Vec, t: float, group: int = 0) -> Vec:
    """Soft thresholding by t; with group = g > 0, entries i and i + g form one 2-vector (isotropic)."""
    if group == 0:
        return [math.copysign(max(abs(a) - t, 0.0), a) for a in v]
    out = v[:]
    for i in range(group):
        r = math.hypot(v[i], v[i + group])
        s = max(r - t, 0.0) / r if r > 0.0 else 0.0
        out[i], out[i + group] = v[i] * s, v[i + group] * s
    return out


def split_bregman(A: Mat, y: Vec, Phi: Mat, lam: float, mu: float, iters: int,
                  group: int = 0) -> tuple[Vec, Vec, Vec]:
    """Return (x, d, b) after iters steps.

    Precondition: lam > 0, mu > 0, and A and Phi have no common null vector,
    so that A^T A + mu Phi^T Phi is positive definite. The iterates converge
    to a minimizer for every mu > 0 (it is ADMM). At a limit, mu b is a dual
    certificate: A^T (A x - y) + Phi^T (mu b) = 0 and mu b in lam d||.||_1(Phi x).
    Cost: O(n^3) once for the factor, then O(n^2 + (m + q) n) per step.
    """
    n, q = len(Phi[0]), len(Phi)
    M = [[sum(A[k][i] * A[k][j] for k in range(len(A))) + mu * sum(Phi[k][i] * Phi[k][j] for k in range(q))
          for j in range(n)] for i in range(n)]
    L = cholesky(M)  # @line L1
    d, b = [0.0] * q, [0.0] * q
    aty = mat_t_vec(A, y)
    x = [0.0] * n
    for _ in range(iters):  # @line L2
        rhs = [a + mu * c for a, c in zip(aty, mat_t_vec(Phi, [di - bi for di, bi in zip(d, b)]))]
        x = chol_solve(L, rhs)  # @line L3
        phx = mat_vec(Phi, x)
        d = shrink([a + c for a, c in zip(phx, b)], lam / mu, group)  # @line L4
        b = [bi + a - di for bi, a, di in zip(b, phx, d)]  # @line L5
    return x, d, b  # @line L6


def objective(A: Mat, y: Vec, Phi: Mat, lam: float, x: Vec, group: int = 0) -> float:
    r = [a - c for a, c in zip(mat_vec(A, x), y)]
    p = mat_vec(Phi, x)
    reg = sum(abs(a) for a in p) if group == 0 else sum(math.hypot(p[i], p[i + group]) for i in range(group))
    return 0.5 * sum(a * a for a in r) + lam * reg


def difference_matrix(n: int) -> Mat:
    """The (n-1) x n forward difference matrix."""
    return [[(-1.0 if j == i else 1.0 if j == i + 1 else 0.0) for j in range(n)] for i in range(n - 1)]


def gradient_matrix(n1: int, n2: int) -> Mat:
    """The 2N x N forward difference gradient with a Neumann border (zero rows at the border)."""
    N = n1 * n2
    G = [[0.0] * N for _ in range(2 * N)]
    for i in range(n1):
        for j in range(n2):
            k = i * n2 + j
            if i < n1 - 1:
                G[k][k], G[k][k + n2] = -1.0, 1.0
            if j < n2 - 1:
                G[N + k][k], G[N + k][k + 1] = -1.0, 1.0
    return G
