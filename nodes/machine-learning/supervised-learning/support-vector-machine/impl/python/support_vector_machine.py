# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/support-vector-machine/. The authors are listed in prov/3V5V6X.jsonl.

"""The soft margin kernel support vector machine.

Training solves the dual problem

    maximize   sum_i a_i - 1/2 sum_ij a_i a_j y_i y_j K_ij
    subject to 0 <= a_i <= C, sum_i a_i y_i = 0

with an SMO type decomposition method that uses the second order working set
selection WSS3 of Fan, Chen and Lin (2005), the rule of LIBSVM. The solver
works on the general form min 1/2 b^T Q b + p^T b, z^T b = const,
0 <= b <= C, with z in {-1, +1}^n.
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


def solve_wss3(
    q: Sequence[Sequence[float]],
    p: Sequence[float],
    z: Sequence[int],
    c: float,
    eps: float = 1e-6,
    max_iter: int = 1_000_000,
) -> tuple[list[float], float, int]:
    """Minimize 1/2 b^T Q b + p^T b subject to z^T b = 0 and 0 <= b <= C, from b = 0.

    Returns (beta, threshold, iterations). The threshold is the value of
    -z_t G_t at the free variables, where G = Q beta + p is the gradient.
    """
    n = len(p)
    beta = [0.0] * n
    g = list(map(float, p))
    it = 0
    while it < max_iter:
        up = [t for t in range(n) if (beta[t] < c and z[t] == 1) or (beta[t] > 0 and z[t] == -1)]
        low = [t for t in range(n) if (beta[t] < c and z[t] == -1) or (beta[t] > 0 and z[t] == 1)]
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
        bij = gmax + z[j] * g[j]
        d = bij / (a if a > 0 else TAU)
        dmax = min(
            c - beta[i] if z[i] == 1 else beta[i],
            c - beta[j] if z[j] == -1 else beta[j],
        )
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
        up = [-z[t] * g[t] for t in range(n) if (beta[t] < c and z[t] == 1) or (beta[t] > 0 and z[t] == -1)]
        low = [-z[t] * g[t] for t in range(n) if (beta[t] < c and z[t] == -1) or (beta[t] > 0 and z[t] == 1)]
        thr = ((max(up) if up else 0.0) + (min(low) if low else 0.0)) / 2
    return beta, thr, it


class SVM:
    def __init__(self, k: Kernel, c: float, eps: float = 1e-6) -> None:
        self.k, self.c, self.eps = k, c, eps

    def fit(self, xs: Sequence[Vec], ys: Sequence[int]) -> "SVM":
        n = len(xs)
        gram = [[self.k(xs[i], xs[j]) for j in range(n)] for i in range(n)]  # @line L1
        q = [[ys[i] * ys[j] * gram[i][j] for j in range(n)] for i in range(n)]  # @line L2
        alpha, b, self.iterations = solve_wss3(q, [-1.0] * n, ys, self.c, self.eps)  # @line L3
        sv = [i for i in range(n) if alpha[i] > 0]  # @line L4
        self.alpha, self.b, self.gram = alpha, b, gram  # @line L5 (b is the mean over free SVs)
        self.sv = sv
        self.xs, self.ys = list(xs), list(ys)
        return self  # @line L6

    def decision(self, x: Vec) -> float:
        return sum(self.alpha[i] * self.ys[i] * self.k(self.xs[i], x) for i in self.sv) + self.b  # @line L7

    def predict(self, x: Vec) -> int:
        return 1 if self.decision(x) >= 0 else -1  # @line L8

    # ----- quantities used by the tests and the page -----

    def weight_vector(self) -> list[float]:
        """w = sum_i a_i y_i x_i, for the linear kernel only."""
        d = len(self.xs[0])
        return [sum(self.alpha[i] * self.ys[i] * self.xs[i][t] for i in self.sv) for t in range(d)]

    def norm_w_squared(self) -> float:
        a, y, g = self.alpha, self.ys, self.gram
        return sum(a[i] * a[j] * y[i] * y[j] * g[i][j] for i in self.sv for j in self.sv)

    def primal_objective(self) -> float:
        n = len(self.xs)
        f = [sum(self.alpha[j] * self.ys[j] * self.gram[i][j] for j in self.sv) + self.b for i in range(n)]
        slack = sum(max(0.0, 1 - y * fi) for y, fi in zip(self.ys, f))
        return 0.5 * self.norm_w_squared() + self.c * slack

    def dual_objective(self) -> float:
        return sum(self.alpha) - 0.5 * self.norm_w_squared()

    def kkt_violation(self) -> float:
        n = len(self.xs)
        worst = abs(sum(a * y for a, y in zip(self.alpha, self.ys)))
        for i in range(n):
            m = self.ys[i] * (sum(self.alpha[j] * self.ys[j] * self.gram[i][j] for j in self.sv) + self.b)
            a = self.alpha[i]
            if a == 0:
                worst = max(worst, 1 - m)
            elif a == self.c:
                worst = max(worst, m - 1)
            else:
                worst = max(worst, abs(m - 1))
        return worst
