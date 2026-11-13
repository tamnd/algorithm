# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/esprit/. The authors are listed in prov/X5EKAZ.jsonl.

"""ESPRIT: frequencies of d complex sinusoids from the shift invariance of the signal subspace.

The steering vector is a(w) = (1, e^{iw}, ..., e^{i(m-1)w}), w in radians per sample.
All linear algebra is written here: a cyclic complex Jacobi eigen solver for Hermitian
matrices, Gaussian elimination, and the Faddeev-LeVerrier characteristic polynomial with
Durand-Kerner roots for the small non-Hermitian matrix Phi.
"""

import cmath
import math
from typing import Sequence

Matrix = list[list[complex]]


def hermitian_eigen(a: Sequence[Sequence[complex]], tol: float = 1e-14, sweeps: int = 100) -> tuple[list[float], Matrix]:
    """Eigenvalues (descending) and eigenvectors (columns of V) of a Hermitian matrix. O(m^3) per sweep."""
    m = len(a)
    A = [[complex(v) for v in row] for row in a]
    V = [[complex(i == j) for j in range(m)] for i in range(m)]
    scale = math.sqrt(sum(abs(v) ** 2 for row in A for v in row)) or 1.0
    for _ in range(sweeps):
        off = math.sqrt(sum(abs(A[i][j]) ** 2 for i in range(m) for j in range(m) if i != j))
        if off <= tol * scale:
            break
        for p in range(m - 1):
            for q in range(p + 1, m):
                b = A[p][q]
                r = abs(b)
                if r <= 1e-300:
                    continue
                ph = b / r
                for k in range(m):
                    A[k][q] *= ph.conjugate()
                    V[k][q] *= ph.conjugate()
                for k in range(m):
                    A[q][k] *= ph
                theta = (A[q][q].real - A[p][p].real) / (2 * r)
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(m):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p], A[k][q] = c * akp - s * akq, s * akp + c * akq
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p], V[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
                for k in range(m):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k], A[q][k] = c * apk - s * aqk, s * apk + c * aqk
                A[p][q] = A[q][p] = 0j
    order = sorted(range(m), key=lambda i: -A[i][i].real)
    return [A[i][i].real for i in order], [[V[k][i] for i in order] for k in range(m)]


def solve(a: Matrix, b: Matrix) -> Matrix:
    """Solve a X = b (a square) by Gaussian elimination with partial pivoting."""
    n = len(a)
    w = len(b[0])
    M = [list(a[i]) + list(b[i]) for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if M[piv][col] == 0:
            raise ValueError("singular system")
        M[col], M[piv] = M[piv], M[col]
        for r in range(col + 1, n):
            f = M[r][col] / M[col][col]
            if f != 0:
                for c in range(col, n + w):
                    M[r][c] -= f * M[col][c]
    X = [[0j] * w for _ in range(n)]
    for r in range(n - 1, -1, -1):
        for j in range(w):
            s = M[r][n + j] - sum(M[r][c] * X[c][j] for c in range(r + 1, n))
            X[r][j] = s / M[r][r]
    return X


def characteristic_polynomial(A: Matrix) -> list[complex]:
    """Coefficients (1, c1, ..., cn) of det(zI - A) by the Faddeev-LeVerrier recursion. O(n^4)."""
    n = len(A)
    c = [1 + 0j]
    M = [[0j] * n for _ in range(n)]
    for k in range(1, n + 1):
        M = [[sum(A[i][l] * M[l][j] for l in range(n)) + (c[-1] if i == j else 0) for j in range(n)] for i in range(n)]
        AM_trace = sum(sum(A[i][l] * M[l][i] for l in range(n)) for i in range(n))
        c.append(-AM_trace / k)
    return c


def polynomial_roots(c: Sequence[complex], iterations: int = 500) -> list[complex]:
    """Roots of z^n + c[1] z^(n-1) + ... + c[n] by Durand-Kerner iteration."""
    n = len(c) - 1
    bound = 1 + max((abs(v) for v in c[1:]), default=0)
    z = [bound * (0.4 + 0.9j) ** i for i in range(n)]
    for _ in range(iterations):
        delta = 0.0
        new = []
        for i in range(n):
            val = 0j
            for v in c:
                val = val * z[i] + v
            den = 1 + 0j
            for j in range(n):
                if j != i:
                    den *= z[i] - z[j]
            step = val / den if den != 0 else 0
            new.append(z[i] - step)
            delta = max(delta, abs(step))
        z = new
        if delta < 1e-15 * bound:
            break
    return z


def eigenvalues(A: Matrix) -> list[complex]:
    """Eigenvalues of a small square complex matrix."""
    return polynomial_roots(characteristic_polynomial(A))


def steering(w: float, m: int) -> list[complex]:
    return [cmath.exp(1j * w * k) for k in range(m)]


def model_covariance(freqs: Sequence[float], powers: Sequence[float], noise: float, m: int) -> Matrix:
    """The exact covariance sum of P_k a(w_k) a(w_k)^H plus noise times I."""
    R = [[complex(noise if i == j else 0) for j in range(m)] for i in range(m)]
    for w, pw in zip(freqs, powers):
        a = steering(w, m)
        for i in range(m):
            for j in range(m):
                R[i][j] += pw * a[i] * a[j].conjugate()
    return R


def sample_covariance(x: Sequence[complex], m: int) -> Matrix:
    """(1/K) sum of y_t y_t^H over the K = N - m + 1 windows y_t = (x[t], ..., x[t + m - 1])."""
    k = len(x) - m + 1
    if m < 1 or k < 1:
        raise ValueError("need 1 <= m <= N")
    R = [[0j] * m for _ in range(m)]
    for t in range(k):
        y = x[t:t + m]
        for i in range(m):
            yi = y[i]
            for j in range(m):
                R[i][j] += yi * y[j].conjugate()
    return [[v / k for v in row] for row in R]


def rotation_operator(R: Sequence[Sequence[complex]], d: int) -> Matrix:
    """The d x d least-squares solution Phi of S1 Phi = S2 for the signal subspace S of R."""
    m = len(R)
    if not 0 < d < m:
        raise ValueError("need 0 < d < m")
    _, U = hermitian_eigen(R)  # @line L1
    S = [row[:d] for row in U]  # @line L2
    S1, S2 = S[:-1], S[1:]  # @line L3
    G = [[sum(S1[k][i].conjugate() * S1[k][j] for k in range(m - 1)) for j in range(d)] for i in range(d)]
    H = [[sum(S1[k][i].conjugate() * S2[k][j] for k in range(m - 1)) for j in range(d)] for i in range(d)]
    return solve(G, H)  # @line L4


def esprit(R: Sequence[Sequence[complex]], d: int) -> list[float]:
    """The d frequencies in [-pi, pi), sorted, as the arguments of the eigenvalues of Phi.

    Precondition: R is Hermitian m x m with 0 < d < m. Cost: O(m^3) for the eigenvectors,
    O(m d^2) for Phi and O(d^4) for its eigenvalues.
    """
    phi = eigenvalues(rotation_operator(R, d))  # @line L5
    return sorted(cmath.phase(v) for v in phi)  # @line L6
