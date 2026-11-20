# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pod-galerkin-reduced-model/. The authors are listed in prov/9GPP7P.jsonl.
"""POD-Galerkin reduced-order model of x' = A x + f, with the method of snapshots and backward Euler steps."""

import math

from scimat import eye, inv, matmul, matvec, scale, sub, transpose

Matrix = list[list[float]]
Vector = list[float]


def heat_matrix(n: int) -> Matrix:
    """Return A = (n+1)^2 tridiag(1, -2, 1), the central difference form of u_xx on (0, 1) with u = 0 at both ends."""
    h2 = float((n + 1) ** 2)
    a = [[0.0] * n for _ in range(n)]
    for i in range(n):
        a[i][i] = -2.0 * h2
        if i > 0:
            a[i][i - 1] = h2
        if i < n - 1:
            a[i][i + 1] = h2
    return a


def backward_euler(a: Matrix, f: Vector, x0: Vector, dt: float, steps: int) -> list[Vector]:
    """Return the states x_0, ..., x_K of (I - dt A) x_(k+1) = x_k + dt f, with K = steps."""
    m = inv(sub(eye(len(a)), scale(dt, a)))
    xs = [list(x0)]
    for _ in range(steps):
        xs.append(matvec(m, [x + dt * g for x, g in zip(xs[-1], f)]))
    return xs


def jacobi_eigen(c: Matrix, tol: float = 1e-15, max_sweeps: int = 60) -> tuple[Vector, list[Vector]]:
    """Return the eigenvalues of the symmetric matrix c in non-increasing order and their orthonormal eigenvectors.

    Cyclic Jacobi rotations: each rotation sets one off-diagonal entry to zero.
    """
    m = len(c)
    a = [[float(x) for x in row] for row in c]
    v = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]
    total = sum(a[i][j] ** 2 for i in range(m) for j in range(m))
    for _ in range(max_sweeps):
        off = sum(a[i][j] ** 2 for i in range(m) for j in range(m) if i != j)
        if off <= tol * tol * total:
            break
        for p in range(m - 1):
            for q in range(p + 1, m):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0.0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                cs = 1.0 / math.sqrt(t * t + 1.0)
                sn = t * cs
                for k in range(m):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = cs * akp - sn * akq
                    a[k][q] = sn * akp + cs * akq
                for k in range(m):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = cs * apk - sn * aqk
                    a[q][k] = sn * apk + cs * aqk
                for k in range(m):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = cs * vkp - sn * vkq
                    v[k][q] = sn * vkp + cs * vkq
    order = sorted(range(m), key=lambda i: -a[i][i])
    return [a[i][i] for i in order], [[v[k][i] for k in range(m)] for i in order]


def pod_basis(s: Matrix, r: int, rank_tol: float = 1e-13) -> tuple[Matrix, Vector]:
    """Return the n by r POD basis V of the snapshot matrix s (one column per snapshot) and all eigenvalues of S^T S.

    Raise ValueError if r < 1 or if lambda_r is not above rank_tol * lambda_1.
    """
    st = transpose(s)
    c = matmul(st, s)  # @line L1: the m by m correlation matrix C = S^T S
    lam, w = jacobi_eigen(c)  # @line L2
    if r < 1 or r > len(lam) or lam[r - 1] <= rank_tol * max(lam[0], 0.0):
        raise ValueError("r must be between 1 and the numerical rank of S")
    cols = []
    for i in range(r):  # @line L3: v_i = S w_i / sqrt(lambda_i)
        sw = matvec(s, w[i])
        cols.append([x / math.sqrt(lam[i]) for x in sw])
    return transpose(cols), lam


def pod_galerkin(a: Matrix, f: Vector, x0: Vector, dt: float, steps: int, s: Matrix, r: int) -> tuple[list[Vector], Matrix, Vector]:
    """Run the rank-r POD-Galerkin model of x' = A x + f for K = steps backward Euler steps.

    Return the lifted states V z_0, ..., V z_K, the basis V and the eigenvalues of S^T S.
    """
    v, lam = pod_basis(s, r)
    vt = transpose(v)
    ar = matmul(vt, matmul(a, v))  # @line L4: offline, A_r = V^T A V, f_r = V^T f, z_0 = V^T x_0
    fr = matvec(vt, f)
    z = matvec(vt, x0)
    mr = inv(sub(eye(r), scale(dt, ar)))  # the r by r inverse, formed once
    zs = [z]
    for _ in range(steps):  # @line L5
        z = matvec(mr, [zi + dt * gi for zi, gi in zip(z, fr)])  # @line L6
        zs.append(z)
    return [matvec(v, zk) for zk in zs], v, lam  # @line L7: lift x~_k = V z_k
