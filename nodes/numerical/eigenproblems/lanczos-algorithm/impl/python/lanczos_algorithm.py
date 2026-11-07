# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lanczos-algorithm/. The authors are listed in prov/GKZVXW.jsonl.

"""Symmetric Lanczos algorithm with optional full reorthogonalization.

lanczos(matvec, b, k) returns (alpha, beta, q, breakdown): the diagonal alpha_1..alpha_m and
off-diagonal beta_1..beta_m of the tridiagonal T_m (beta_m couples to the next vector, so the
residual of a Ritz pair is beta_m |s_mi|), the orthonormal Lanczos vectors q_1..q_m, and whether
an invariant subspace was found (m < k). ritz(alpha, beta, q) returns the Ritz pairs with their
residual estimates. Standard library only; vectors are lists of floats.
"""

import math

U = 2.0 ** -53  # unit roundoff of IEEE double precision


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def norm2(x):
    return math.sqrt(dot(x, x))


def lanczos(matvec, b, k, reorth=True):
    """Run k steps of the Lanczos recurrence on the symmetric operator matvec, start vector b."""
    nb = norm2(b)
    if nb == 0.0:
        raise ValueError("start vector is zero")
    q = [[t / nb for t in b]]  # @line L1
    alpha, beta = [], []
    q_prev, b_prev = [0.0] * len(b), 0.0
    for j in range(k):  # @line L2
        w = matvec(q[j])
        w = [wi - b_prev * pi for wi, pi in zip(w, q_prev)]  # @line L3
        a = dot(q[j], w)  # @line L4
        w = [wi - a * qi for wi, qi in zip(w, q[j])]
        if reorth:  # @line L5: classical Gram-Schmidt, applied twice
            for _ in range(2):
                for qi in q:
                    h = dot(qi, w)
                    w = [wi - h * t for wi, t in zip(w, qi)]
        alpha.append(a)
        bj = norm2(w)  # @line L6
        beta.append(bj)
        scale = max(abs(a), b_prev, 1.0)
        if bj <= 10.0 * len(b) * U * scale:
            return alpha, beta, q, True
        if j + 1 < k:
            q_prev, b_prev = q[j], bj
            q.append([t / bj for t in w])  # @line L7
    return alpha, beta, q, False


def tridiag_eig(alpha, beta):
    """Eigenvalues and eigenvectors of the symmetric tridiagonal T (diagonal alpha, off-diagonal beta[:-1])
    by cyclic Jacobi on the dense matrix; adequate for the small T of Lanczos."""
    m = len(alpha)
    t = [[0.0] * m for _ in range(m)]
    for i in range(m):
        t[i][i] = alpha[i]
        if i + 1 < m:
            t[i][i + 1] = t[i + 1][i] = beta[i]
    s = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]
    for _ in range(60):
        rotated = False
        for p in range(m - 1):
            for r in range(p + 1, m):
                apq = t[p][r]
                if apq == 0.0 or abs(apq) <= U * math.sqrt(abs(t[p][p] * t[r][r])) * 0.5:
                    continue
                rotated = True
                tau = (t[r][r] - t[p][p]) / (2.0 * apq)
                tt = (1.0 if tau >= 0 else -1.0) / (abs(tau) + math.hypot(1.0, tau))
                c = 1.0 / math.hypot(1.0, tt)
                sn = tt * c
                t[p][p] -= tt * apq
                t[r][r] += tt * apq
                t[p][r] = t[r][p] = 0.0
                for i in range(m):
                    if i != p and i != r:
                        x, y = t[i][p], t[i][r]
                        t[i][p] = t[p][i] = c * x - sn * y
                        t[i][r] = t[r][i] = sn * x + c * y
                for i in range(m):
                    x, y = s[i][p], s[i][r]
                    s[i][p] = c * x - sn * y
                    s[i][r] = sn * x + c * y
        if not rotated:
            break
    order = sorted(range(m), key=lambda i: -t[i][i])
    return [t[i][i] for i in order], [[s[r][i] for r in range(m)] for i in order]


def ritz(alpha, beta, q):
    """Ritz values theta_1 >= ... >= theta_m, Ritz vectors y_i = Q_m s_i, and the residual
    estimates beta_m |s_mi| = ||A y_i - theta_i y_i||_2 (exact in exact arithmetic)."""
    m = len(alpha)
    theta, svecs = tridiag_eig(alpha, beta)  # @line L8
    n = len(q[0])
    ys = [[sum(q[j][r] * s[j] for j in range(m)) for r in range(n)] for s in svecs]
    est = [beta[m - 1] * abs(s[m - 1]) for s in svecs]
    return theta, ys, est
