# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-empirical-interpolation-method/. The authors are listed in prov/RHRTRM.jsonl.
"""The discrete empirical interpolation method (DEIM) of Chaturantabut and Sorensen.

A basis U = [u_1 .. u_m] of R^n is given as a list of m columns. DEIM chooses m row indices
p_1..p_m, and the DEIM approximation of a vector f is U (P^T U)^-1 P^T f, which needs only the
m entries f[p_1], .., f[p_m]. The POD basis of the example is computed from the Gram matrix of
the snapshots with the cyclic Jacobi eigenvalue method.
"""

import math

Vector = list[float]
Matrix = list[list[float]]


def argmax_abs(v: Vector) -> int:
    """Index of the largest |v_i|; ties go to the first index."""
    best = 0
    for i in range(1, len(v)):
        if abs(v[i]) > abs(v[best]):
            best = i
    return best


def gauss_solve(a: Matrix, b: Vector) -> Vector:
    """Solve a x = b by Gaussian elimination with partial pivoting."""
    n = len(b)
    m = [list(row) + [bi] for row, bi in zip(a, b)]
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(m[i][k]))
        if m[p][k] == 0.0:
            raise ValueError("P^T U is singular")
        m[k], m[p] = m[p], m[k]
        for i in range(k + 1, n):
            f = m[i][k] / m[k][k]
            for j in range(k, n + 1):
                m[i][j] -= f * m[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))) / m[i][i]
    return x


def deim(u: list[Vector]) -> list[int]:
    """Return the DEIM indices of the basis u (a list of m linearly independent columns)."""
    p = [argmax_abs(u[0])]  # @line L1
    for l in range(1, len(u)):  # @line L2
        a = [[u[j][pi] for j in range(l)] for pi in p]  # the l by l matrix P^T U
        c = gauss_solve(a, [u[l][pi] for pi in p])  # @line L3: (P^T U) c = P^T u_l
        r = [u[l][i] - sum(c[j] * u[j][i] for j in range(l)) for i in range(len(u[0]))]  # @line L4
        p.append(argmax_abs(r))  # @line L5: the new index, where r is largest
    return p  # @line L6


def deim_approx(u: list[Vector], p: list[int], fp: Vector) -> Vector:
    """The DEIM approximation U (P^T U)^-1 (f at p), from the m values fp = P^T f."""
    a = [[u[j][pi] for j in range(len(u))] for pi in p]
    c = gauss_solve(a, fp)
    return [sum(cj * uj[i] for cj, uj in zip(c, u)) for i in range(len(u[0]))]


def jacobi_eigh(a: Matrix, tol: float = 1e-15, sweeps: int = 60) -> tuple[Vector, Matrix]:
    """Eigenvalues (in decreasing order) and eigenvectors (as columns of v) of a symmetric a."""
    n = len(a)
    a = [list(row) for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        scale = math.sqrt(sum(a[i][i] ** 2 for i in range(n))) or 1.0
        if off <= tol * scale:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    order = sorted(range(n), key=lambda i: -a[i][i])
    return [a[i][i] for i in order], [[v[k][i] for i in order] for k in range(n)]


def pod(snaps: list[Vector], m: int) -> tuple[list[Vector], Vector]:
    """The first m POD modes (orthonormal columns) and all singular values of the snapshots,
    by the method of snapshots: eigenvectors of the Gram matrix S^T S."""
    k = len(snaps)
    gram = [[sum(a * b for a, b in zip(snaps[i], snaps[j])) for j in range(k)] for i in range(k)]
    lam, w = jacobi_eigh(gram)
    sig = [math.sqrt(max(t, 0.0)) for t in lam]
    modes = []
    for j in range(m):
        col = [sum(w[i][j] * snaps[i][x] for i in range(k)) / sig[j] for x in range(len(snaps[0]))]
        nrm = math.sqrt(sum(t * t for t in col))
        modes.append([t / nrm for t in col])
    return modes, sig


def inv_norm2(a: Matrix) -> float:
    """The spectral norm of a^-1, that is 1 / sigma_min(a), from the eigenvalues of a^T a."""
    n = len(a)
    ata = [[sum(a[k][i] * a[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    lam, _ = jacobi_eigh(ata)
    return 1.0 / math.sqrt(lam[-1])
