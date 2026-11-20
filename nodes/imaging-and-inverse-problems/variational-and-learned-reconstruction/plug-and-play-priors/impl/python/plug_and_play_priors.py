# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plug-and-play-priors/. The authors are listed in prov/S92WZQ.jsonl.
"""Plug-and-play ADMM of Venkatakrishnan, Bouman and Wohlberg.

The denoiser is given: a function denoiser(z) that returns a denoised copy
of z. The data term enters through prox_f(z), the minimizer of
f(x) + (rho / 2) ||x - z||^2. The method alternates the two and a dual
update. Matrices are lists of rows; vectors are lists of floats.
"""

import math


def pnp_admm(prox_f, denoiser, v0, iters):
    """Run iters steps of PnP-ADMM from v = v0, u = 0 and return (x, v, u)."""
    v, u = list(v0), [0.0] * len(v0)  # @line L1
    x = list(v0)
    for _ in range(iters):  # @line L2
        x = prox_f([a - b for a, b in zip(v, u)])  # @line L3
        v = denoiser([a + b for a, b in zip(x, u)])  # @line L4
        u = [a + b - c for a, b, c in zip(u, x, v)]  # @line L5
    return x, v, u  # @line L6


def solve(m, b):
    """Solve m x = b by Gaussian elimination with partial pivoting."""
    n = len(b)
    a = [list(row) + [bi] for row, bi in zip(m, b)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        a[c], a[p] = a[p], a[c]
        for r in range(c + 1, n):
            f = a[r][c] / a[c][c]
            for k in range(c, n + 1):
                a[r][k] -= f * a[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (a[r][n] - sum(a[r][k] * x[k] for k in range(r + 1, n))) / a[r][r]
    return x


def matvec(a, x):
    return [sum(p * q for p, q in zip(row, x)) for row in a]


def rmatvec(a, r):
    return [sum(a[i][j] * r[i] for i in range(len(a))) for j in range(len(a[0]))]


def least_squares_prox(a, y, rho):
    """z -> argmin (1/2)||A x - y||^2 + (rho/2)||x - z||^2, by a linear solve."""
    n = len(a[0])
    m = [[sum(a[i][j] * a[i][k] for i in range(len(a))) + (rho if j == k else 0.0)
          for k in range(n)] for j in range(n)]
    aty = rmatvec(a, y)
    return lambda z: solve(m, [p + rho * q for p, q in zip(aty, z)])


def soft(v, theta):
    """Soft thresholding, the proximal map of theta ||.||_1."""
    return [math.copysign(max(abs(t) - theta, 0.0), t) for t in v]


def haar_matrix(n):
    """The orthonormal Haar transform of length n (a power of 2), as rows."""
    if n == 1:
        return [[1.0]]
    h = haar_matrix(n // 2)
    s = 1.0 / math.sqrt(2.0)
    top = [[s * h[i][j // 2] for j in range(n)] for i in range(n // 2)]
    bottom = [[s if j == 2 * i else (-s if j == 2 * i + 1 else 0.0) for j in range(n)]
              for i in range(n // 2)]
    return top + bottom


def haar_soft_denoiser(n, theta):
    """z -> H^T soft(H z, theta), the proximal map of theta ||H .||_1."""
    h = haar_matrix(n)
    return lambda z: rmatvec(h, soft(matvec(h, z), theta))


def linear_denoiser(w):
    """z -> W z for a given matrix W."""
    return lambda z: matvec(w, z)
