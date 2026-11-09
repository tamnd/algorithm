# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/barrier-method/. The authors are listed in prov/0ZMXKV.jsonl.

"""The logarithmic barrier method for a linear objective under a linear matrix inequality.

The program is the inequality form of a semidefinite program:

    minimize c^T x  subject to  F(x) = F_0 + x_1 F_1 + ... + x_n F_n  is positive semidefinite,

with symmetric p x p matrices F_i. A linear program min c^T x, A x <= b is the case of diagonal
matrices F_0 = diag(b), F_i = -diag(column i of A). The barrier is phi(x) = -log det F(x), a
self-concordant barrier with parameter nu = p. The method minimizes t c^T x + phi(x) by Newton's
method with backtracking (centering), then multiplies t by mu, until nu / t <= eps.

At a point x on the central path, Z = F(x)^-1 / t is feasible for the dual
    maximize -tr(F_0 Z)  subject to  tr(F_i Z) = c_i,  Z positive semidefinite,
and the duality gap c^T x + tr(F_0 Z) = tr(F(x) Z) equals p / t.

Cost of one Newton step: n solves with F(x) (O(n p^3)), the Hessian entries tr(F^-1 F_i F^-1 F_j)
(O(n^2 p^2)) and one n x n solve (O(n^3)).
"""

import math
from dataclasses import dataclass, field

Matrix = list[list[float]]


@dataclass
class BarrierResult:
    x: list[float]
    z: Matrix  # the dual point F(x)^-1 / t of the last centering
    t: float
    outer: list[tuple[float, float, int]] = field(default_factory=list)  # (t, c^T x, Newton steps) per centering


def cholesky(a: Matrix) -> Matrix | None:
    """Lower triangular L with L L^T = a, or None if a is not positive definite."""
    k = len(a)
    low = [[0.0] * k for _ in range(k)]
    for i in range(k):
        for j in range(i + 1):
            v = a[i][j] - sum(low[i][r] * low[j][r] for r in range(j))
            if i == j:
                if v <= 0.0:
                    return None
                low[i][i] = math.sqrt(v)
            else:
                low[i][j] = v / low[j][j]
    return low


def chol_solve(low: Matrix, r: list[float]) -> list[float]:
    k = len(r)
    w = [0.0] * k
    for i in range(k):
        w[i] = (r[i] - sum(low[i][j] * w[j] for j in range(i))) / low[i][i]
    z = [0.0] * k
    for i in range(k - 1, -1, -1):
        z[i] = (w[i] - sum(low[j][i] * z[j] for j in range(i + 1, k))) / low[i][i]
    return z


def lmi(f: list[Matrix], x: list[float]) -> Matrix:
    """F(x) = F_0 + sum x_i F_i."""
    p = len(f[0])
    return [[f[0][r][s] + sum(x[i] * f[i + 1][r][s] for i in range(len(x))) for s in range(p)] for r in range(p)]


def inverse(low: Matrix) -> Matrix:
    p = len(low)
    cols = [chol_solve(low, [1.0 if r == j else 0.0 for r in range(p)]) for j in range(p)]
    return [[cols[j][r] for j in range(p)] for r in range(p)]


def phi_t(c: list[float], f: list[Matrix], x: list[float], t: float) -> float:
    """t c^T x - log det F(x), or +inf outside the domain."""
    low = cholesky(lmi(f, x))
    if low is None:
        return math.inf
    return t * sum(ci * xi for ci, xi in zip(c, x)) - 2.0 * sum(math.log(low[i][i]) for i in range(len(low)))


def center(c, f, x, t, eps_nt=1e-12, alpha=0.25, beta=0.5, max_steps=500):
    """Newton's method with backtracking on t c^T x + phi(x). Returns (x, Newton steps)."""
    n, p = len(x), len(f[0])
    steps = 0
    while steps < max_steps:
        low = cholesky(lmi(f, x))
        finv = inverse(low)
        mats = [[[sum(finv[r][q] * f[i + 1][q][s] for q in range(p)) for s in range(p)] for r in range(p)] for i in range(n)]
        g = [t * c[i] - sum(mats[i][r][r] for r in range(p)) for i in range(n)]  # @line L7
        h = [[sum(mats[i][r][s] * mats[j][s][r] for r in range(p) for s in range(p)) for j in range(n)] for i in range(n)]
        dx = [-v for v in chol_solve(cholesky(h), g)]  # @line L8
        lam2 = -sum(g[i] * dx[i] for i in range(n))
        if lam2 / 2.0 <= eps_nt:  # @line L9
            break
        s, val = 1.0, phi_t(c, f, x, t)  # @line L10
        while True:
            xn = [x[i] + s * dx[i] for i in range(n)]
            if phi_t(c, f, xn, t) <= val - alpha * s * lam2:
                break
            s *= beta
            if s < 1e-12:  # rounding hides any decrease: x is as central as floats allow
                return x, steps
        if xn == x:  # the step is below the spacing of floats
            return x, steps
        x = xn  # @line L11
        steps += 1
    return x, steps


def barrier_method(c, f, x0, t0=1.0, mu=10.0, eps=1e-8) -> BarrierResult:
    """Minimize c^T x subject to F(x) psd, from a strictly feasible x0 (F(x0) positive definite).

    f = [F_0, F_1, ..., F_n]. Stops when the duality gap p / t is at most eps."""
    if cholesky(lmi(f, x0)) is None:
        raise ValueError("x0 is not strictly feasible")
    p = len(f[0])
    x, t = list(map(float, x0)), float(t0)  # @line L1
    res = BarrierResult(x, [], t)
    while True:  # @line L2
        x, steps = center(c, f, x, t)  # @line L3
        res.outer.append((t, sum(ci * xi for ci, xi in zip(c, x)), steps))
        if p / t <= eps:  # @line L4
            break
        t *= mu  # @line L5
    finv = inverse(cholesky(lmi(f, x)))
    res.x, res.t = x, t
    res.z = [[v / t for v in row] for row in finv]  # @line L6
    return res


def newton_bound(nu: float, mu: float, eps_nt: float = 1e-12, alpha: float = 0.25, beta: float = 0.5) -> float:
    """Boyd and Vandenberghe's bound on the Newton steps of one centering after t grows by mu."""
    gamma = alpha * beta * (1 - 2 * alpha) ** 2 / (20 - 8 * alpha)
    return nu * (mu - 1 - math.log(mu)) / gamma + math.log2(math.log2(1 / eps_nt))
