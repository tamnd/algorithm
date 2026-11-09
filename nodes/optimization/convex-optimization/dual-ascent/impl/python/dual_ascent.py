# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-ascent/. The authors are listed in prov/CHE5ZR.jsonl.

"""Dual ascent (projected gradient ascent on the Lagrange dual) for a strongly convex problem.

    minimize f(x)  subject to  a_i^T x = b_i (i not in I),  a_i^T x <= b_i (i in I).

The Lagrangian is L(x, y) = f(x) + y^T (A x - b), with y_i >= 0 for i in I, and the dual function is
d(y) = min_x L(x, y). If f is mu-strongly convex, the minimizer x(y) is unique, d is differentiable
with gradient A x(y) - b, and the gradient is Lipschitz with constant ||A||^2 / mu. One iteration:

    x <- argmin_x L(x, y),   g <- A x - b,   y <- y + alpha g,   y_i <- max(0, y_i) for i in I.

With 0 < alpha <= mu / ||A||^2 (alpha = mu / ||A||_F^2 is a safe, computable choice), for each
dual optimal y* and each k >= 1:
    d* - d(y_k) <= ||y_0 - y*||^2 / (2 alpha k)   and   ||x_k - x*||^2 <= 2 (d* - d(y_k)) / mu.

Cost of one iteration: one minimization of L(., y) plus O(m n) for A x and the update.
"""

from dataclasses import dataclass, field


@dataclass
class DualAscentResult:
    x: list
    y: list
    steps: list = field(default_factory=list)  # (y_k, x_k, g_k) for k = 0, 1, ..., with x_k = x(y_k)


def dual_ascent(argmin_lagrangian, a, b, ineq, y0, alpha, eps=0, max_iter=1000) -> DualAscentResult:
    """argmin_lagrangian(y) returns the minimizer over x of f(x) + y^T (A x - b).

    ineq[i] is True when row i is an inequality a_i^T x <= b_i. Stops when ||y_new - y|| <= alpha eps,
    which for equality rows only is ||A x - b|| <= eps. The result holds x = x(y), so d(y) = L(x, y).
    """
    y = list(y0)
    res = DualAscentResult(None, y)
    for _ in range(max_iter):  # @line L1
        x = argmin_lagrangian(y)  # @line L2
        g = [sum(aij * xj for aij, xj in zip(row, x)) - bi for row, bi in zip(a, b)]  # @line L3
        res.x, res.y = x, y
        res.steps.append((y, x, g))
        yn = [max(0, yi + alpha * gi) if q else yi + alpha * gi for yi, gi, q in zip(y, g, ineq)]  # @line L4
        if sum((u - v) ** 2 for u, v in zip(yn, y)) <= (alpha * eps) ** 2:  # @line L5
            return res
        y = yn  # @line L6
    return res


def solve(m, r):
    """Gaussian elimination with pivoting on the largest entry; exact for Fraction input."""
    k = len(r)
    t = [list(row) + [r[i]] for i, row in enumerate(m)]
    for col in range(k):
        piv = max(range(col, k), key=lambda i: abs(t[i][col]))
        if t[piv][col] == 0:
            raise ValueError("singular matrix")
        t[col], t[piv] = t[piv], t[col]
        for i in range(col + 1, k):
            f = t[i][col] / t[col][col]
            for j in range(col, k + 1):
                t[i][j] -= f * t[col][j]
    x = [0] * k
    for i in range(k - 1, -1, -1):
        x[i] = (t[i][k] - sum(t[i][j] * x[j] for j in range(i + 1, k))) / t[i][i]
    return x


def quadratic_argmin(q, c, a):
    """The x-step for f(x) = x^T Q x / 2 + c^T x with Q positive definite: solve Q x = -c - A^T y."""
    n = len(c)

    def argmin_lagrangian(y):
        rhs = [-c[i] - sum(row[i] * yk for row, yk in zip(a, y)) for i in range(n)]
        return solve(q, rhs)

    return argmin_lagrangian
