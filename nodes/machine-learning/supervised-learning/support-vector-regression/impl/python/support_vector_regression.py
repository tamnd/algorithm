# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/support-vector-regression/. The authors are listed in prov/9APN7H.jsonl.

"""Epsilon support vector regression, trained by an SMO type method with WSS3.

The dual problem of Smola and Schölkopf (2004) is

    minimize   1/2 (a - a*)^T K (a - a*) + eps sum_i (a_i + a*_i) - y^T (a - a*)
    subject to sum_i (a_i - a*_i) = 0,  0 <= a_i, a*_i <= C.

With beta = (a, a*), z = (+1, ..., +1, -1, ..., -1), Q_st = z_s z_t K and
p = (eps - y, eps + y) this is min 1/2 beta^T Q beta + p^T beta subject to
z^T beta = 0 and 0 <= beta <= C, the same form as the SVM dual. LIBSVM solves
it the same way. The solver below picks the pair of variables by the second
order rule WSS3 of Fan, Chen and Lin (2005) and solves each two-variable
subproblem in closed form.
"""

import math
from typing import Callable, Sequence

Vec = Sequence[float]
Kernel = Callable[[Vec, Vec], float]
TAU = 1e-12


def linear_kernel(x: Vec, z: Vec) -> float:
    return sum(a * b for a, b in zip(x, z))


def gaussian_kernel(sigma: float) -> Kernel:
    return lambda x, z: math.exp(-sum((a - b) ** 2 for a, b in zip(x, z)) / (2 * sigma * sigma))


def eps_insensitive(r: float, eps: float) -> float:
    """The epsilon-insensitive loss |r|_eps = max(0, |r| - eps)."""
    return max(0.0, abs(r) - eps)


def _in_up(beta: float, z: int, c: float) -> bool:
    return (beta < c and z == 1) or (beta > 0 and z == -1)


def _in_low(beta: float, z: int, c: float) -> bool:
    return (beta < c and z == -1) or (beta > 0 and z == 1)


def solve_wss3(q, p, z, c, eps=1e-8, max_iter=1_000_000):
    """Minimize 1/2 b^T Q b + p^T b subject to z^T b = 0 and 0 <= b <= C, from b = 0.

    Returns (beta, gradient, threshold, iterations). The threshold is the
    common value of -z_t G_t at the free variables, which is the bias b.
    """
    n = len(p)
    beta = [0.0] * n
    g = [float(v) for v in p]
    it = 0
    while it < max_iter:
        up = [t for t in range(n) if _in_up(beta[t], z[t], c)]
        low = [t for t in range(n) if _in_low(beta[t], z[t], c)]
        if not up or not low:
            break
        i = max(up, key=lambda t: -z[t] * g[t])
        gmax = -z[i] * g[i]
        gmin = min(-z[t] * g[t] for t in low)
        if gmax - gmin < eps:
            break
        best, j = math.inf, -1
        for t in low:  # second order choice of j
            bt = gmax + z[t] * g[t]
            if bt > 0:
                at = q[i][i] + q[t][t] - 2 * z[i] * z[t] * q[i][t]
                val = -bt * bt / (at if at > 0 else TAU)
                if val < best:
                    best, j = val, t
        a = q[i][i] + q[j][j] - 2 * z[i] * z[j] * q[i][j]
        d = (gmax + z[j] * g[j]) / (a if a > 0 else TAU)
        dmax = min(c - beta[i] if z[i] == 1 else beta[i], c - beta[j] if z[j] == -1 else beta[j])
        d = min(d, dmax)
        di, dj = z[i] * d, -z[j] * d
        beta[i] += di
        beta[j] += dj
        for t in (i, j):  # snap onto the bounds after rounding
            if beta[t] < 1e-12 * c:
                beta[t] = 0.0
            elif beta[t] > c * (1 - 1e-12):
                beta[t] = c
        for t in range(n):
            g[t] += q[t][i] * di + q[t][j] * dj
        it += 1
    free = [-z[t] * g[t] for t in range(n) if 0 < beta[t] < c]
    if free:
        thr = sum(free) / len(free)
    else:
        up = [-z[t] * g[t] for t in range(n) if _in_up(beta[t], z[t], c)]
        low = [-z[t] * g[t] for t in range(n) if _in_low(beta[t], z[t], c)]
        thr = ((max(up) if up else 0.0) + (min(low) if low else 0.0)) / 2
    return beta, g, thr, it


class SVR:
    def __init__(self, k: Kernel, c: float, epsilon: float, tol: float = 1e-8) -> None:
        self.k, self.c, self.epsilon, self.tol = k, c, epsilon, tol

    def fit(self, xs: Sequence[Vec], ys: Sequence[float]) -> "SVR":
        n, e = len(xs), self.epsilon
        gram = [[self.k(xs[i], xs[j]) for j in range(n)] for i in range(n)]  # @line L1
        z = [1] * n + [-1] * n  # @line L2
        q = [[z[s] * z[t] * gram[s % n][t % n] for t in range(2 * n)] for s in range(2 * n)]
        p = [e - y for y in ys] + [e + y for y in ys]
        beta, _, b, self.iterations = solve_wss3(q, p, z, self.c, self.tol)  # @line L3
        self.a, self.a_star = beta[:n], beta[n:]
        self.theta = [self.a[i] - self.a_star[i] for i in range(n)]  # @line L4
        self.b = b  # @line L5
        self.sv = [i for i in range(n) if self.theta[i] != 0.0]  # @line L6
        self.xs, self.ys, self.gram = list(xs), list(ys), gram
        return self

    def predict(self, x: Vec) -> float:
        return sum(self.theta[i] * self.k(self.xs[i], x) for i in self.sv) + self.b  # @line L7

    # ----- quantities used by the tests and the page -----

    def fitted(self) -> list[float]:
        n = len(self.xs)
        return [sum(self.theta[j] * self.gram[i][j] for j in self.sv) + self.b for i in range(n)]

    def norm_w_squared(self) -> float:
        t, g = self.theta, self.gram
        return sum(t[i] * t[j] * g[i][j] for i in self.sv for j in self.sv)

    def primal_objective(self) -> float:
        loss = sum(eps_insensitive(y - f, self.epsilon) for y, f in zip(self.ys, self.fitted()))
        return 0.5 * self.norm_w_squared() + self.c * loss

    def dual_objective(self) -> float:
        e = self.epsilon
        return (-0.5 * self.norm_w_squared() - e * sum(a + s for a, s in zip(self.a, self.a_star))
                + sum(y * t for y, t in zip(self.ys, self.theta)))

    def kkt_violation(self) -> float:
        """Largest violation of the KKT conditions of the page, with r_i = y_i - f(x_i)."""
        c, e = self.c, self.epsilon
        worst = abs(sum(self.theta))
        for a, s, y, f in zip(self.a, self.a_star, self.ys, self.fitted()):
            r = y - f
            worst = max(worst, min(a, s))  # a_i a*_i = 0
            if a == 0:
                worst = max(worst, r - e)  # r <= eps
            elif a == c:
                worst = max(worst, e - r)  # r >= eps
            else:
                worst = max(worst, abs(r - e))  # r = eps
            if s == 0:
                worst = max(worst, -r - e)  # r >= -eps
            elif s == c:
                worst = max(worst, r + e)  # r <= -eps
            else:
                worst = max(worst, abs(r + e))  # r = -eps
        return worst
