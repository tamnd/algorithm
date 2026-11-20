# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regularization-by-denoising/. The authors are listed in prov/K86DXS.jsonl.
"""Regularization by denoising (RED) of Romano, Elad and Milanfar.

The denoiser is given: a function denoiser(x). RED uses the residual
x - D(x) in place of the gradient of R(x) = (1/2) x^T (x - D(x)). This is
the true gradient only when D is locally homogeneous and has a symmetric
Jacobian. Matrices are lists of rows; vectors are lists of floats.
"""


def matvec(a, x):
    return [sum(p * q for p, q in zip(row, x)) for row in a]


def rmatvec(a, r):
    return [sum(a[i][j] * r[i] for i in range(len(a))) for j in range(len(a[0]))]


def red_gradient_descent(a, y, denoiser, lam, step, x0, iters):
    """Steps x <- x - step (A^T (A x - y) + lam (x - D(x)))."""
    x = list(x0)  # @line L1
    for _ in range(iters):  # @line L2
        d = denoiser(x)  # @line L3
        r = [p - q for p, q in zip(matvec(a, x), y)]
        g = [p + lam * (xi - di) for p, xi, di in zip(rmatvec(a, r), x, d)]  # @line L4
        x = [xi - step * gi for xi, gi in zip(x, g)]  # @line L5
    return x  # @line L6


def solve(m, b):
    """Solve m x = b by Gaussian elimination with partial pivoting."""
    n = len(b)
    t = [list(row) + [bi] for row, bi in zip(m, b)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(t[r][c]))
        t[c], t[p] = t[p], t[c]
        for r in range(c + 1, n):
            f = t[r][c] / t[c][c]
            for k in range(c, n + 1):
                t[r][k] -= f * t[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (t[r][n] - sum(t[r][k] * x[k] for k in range(r + 1, n))) / t[r][r]
    return x


def red_fixed_point(a, y, denoiser, lam, x0, iters):
    """Steps x <- (A^T A + lam I)^{-1} (A^T y + lam D(x)), the fixed point variant."""
    n = len(x0)
    m = [[sum(a[i][j] * a[i][k] for i in range(len(a))) + (lam if j == k else 0.0)
          for k in range(n)] for j in range(n)]
    aty = rmatvec(a, y)
    x = list(x0)
    for _ in range(iters):
        x = solve(m, [p + lam * q for p, q in zip(aty, denoiser(x))])
    return x


def red_regularizer(x, denoiser):
    """R(x) = (1/2) x^T (x - D(x))."""
    return 0.5 * sum(xi * (xi - di) for xi, di in zip(x, denoiser(x)))


def red_regularizer_gradient(x, denoiser, denoiser_vjp):
    """The true gradient x - (1/2) D(x) - (1/2) J_D(x)^T x of R."""
    d, jt = denoiser(x), denoiser_vjp(x, x)
    return [xi - 0.5 * di - 0.5 * ji for xi, di, ji in zip(x, d, jt)]
