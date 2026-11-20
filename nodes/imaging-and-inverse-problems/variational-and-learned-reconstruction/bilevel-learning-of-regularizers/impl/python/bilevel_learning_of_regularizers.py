# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bilevel-learning-of-regularizers/. The authors are listed in prov/VE2JDY.jsonl.
"""Bilevel learning of a regularization weight.

Upper level: L(alpha) = (1/N) sum_i ||x_alpha(y_i) - x_i||^2 over training
pairs (x_i, y_i). Lower level: x_alpha(y) minimizes the variational energy
with weight alpha. The lower-level solver and the derivative of its solution
in alpha are given functions. For Tikhonov regularization both are exact.
Matrices are lists of rows; vectors are lists of floats.
"""


def bilevel_learn(pairs, lower, lower_vjp, alpha0, step, iters):
    """Projected gradient descent on alpha >= 0. Return (alpha, losses).

    lower(alpha, y) returns x_alpha(y).
    lower_vjp(alpha, y, x, v) returns <dx_alpha(y)/dalpha, v> for x = x_alpha(y).
    Each step calls lower and lower_vjp once per pair.
    """
    n_pairs = len(pairs)
    alpha = alpha0  # @line L1
    losses = []
    for _ in range(iters):  # @line L2
        g, loss = 0.0, 0.0  # @line L3
        for x_true, y in pairs:  # @line L4
            x = lower(alpha, y)  # @line L5
            r = [p - q for p, q in zip(x, x_true)]
            loss += sum(v * v for v in r) / n_pairs
            g += 2.0 * lower_vjp(alpha, y, x, r) / n_pairs  # @line L6
        losses.append(loss)
        alpha = max(alpha - step * g, 0.0)  # @line L7
    return alpha, losses  # @line L8


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


def rmatvec(a, y):
    return [sum(a[r][j] * y[r] for r in range(len(a))) for j in range(len(a[0]))]


def tikhonov(a):
    """Return (lower, lower_vjp) for x_alpha = argmin ||Ax - y||^2 + alpha ||x||^2.

    x_alpha solves (A^T A + alpha I) x = A^T y. Differentiating in alpha gives
    (A^T A + alpha I) dx/dalpha = -x_alpha, so <dx/dalpha, v> = -<p, x_alpha>
    with the adjoint solve (A^T A + alpha I) p = v.
    """
    n = len(a[0])
    ata = [[sum(a[r][i] * a[r][j] for r in range(len(a))) for j in range(n)]
           for i in range(n)]

    def system(alpha):
        return [[ata[i][j] + (alpha if i == j else 0.0) for j in range(n)]
                for i in range(n)]

    def lower(alpha, y):
        return solve(system(alpha), rmatvec(a, y))

    def lower_vjp(alpha, y, x, v):
        p = solve(system(alpha), v)
        return -sum(pi * xi for pi, xi in zip(p, x))

    return lower, lower_vjp


def upper_loss(pairs, lower, alpha):
    """L(alpha), the mean squared reconstruction error on the pairs."""
    total = 0.0
    for x_true, y in pairs:
        x = lower(alpha, y)
        total += sum((p - q) ** 2 for p, q in zip(x, x_true))
    return total / len(pairs)
