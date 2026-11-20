# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bregman-iteration/. The authors are listed in prov/3BKXGP.jsonl.
"""Bregman iteration of Osher, Burger, Goldfarb, Xu and Yin (2005).

Each outer step solves the variational problem
    x^{k+1} = argmin_x (1/2)||A x - y^k||^2 + lam R(x)
and then adds the residual back to the data: y^{k+1} = y^k + (y - A x^{k+1}).
The caller gives the inner solver. Three inner solvers are included:
soft thresholding (A = I, R = ||.||_1, exact), 1D total variation denoising
(A = I, R = TV, by an accelerated dual projected gradient) and the LASSO
(R = ||.||_1, general A, by FISTA).
"""

import math
from typing import Callable

Vec = list[float]


def norm(v: Vec) -> float:
    return math.sqrt(sum(a * a for a in v))


def bregman_iteration(solve: Callable[[Vec], Vec], A: Callable[[Vec], Vec], y: Vec, iters: int,
                      delta: float | None = None, tau: float = 1.0) -> tuple[Vec, list[Vec], list[Vec]]:
    """Return (x, xs, ys): the final iterate, all iterates x^1.. and all data y^0...

    solve(d) must return argmin_x (1/2)||A x - d||^2 + lam R(x) for a fixed lam.
    With delta set, stop at the first k with ||A x^k - y|| <= tau delta
    (the discrepancy principle; use tau >= 1). Precondition: R convex and
    the inner problem has a minimizer. Cost: iters inner solves plus
    iters products with A.
    """
    yk = y[:]  # @line L1
    xs: list[Vec] = []
    ys: list[Vec] = [yk[:]]
    x: Vec = []
    for _ in range(iters):  # @line L2
        x = solve(yk)  # @line L3
        xs.append(x)
        r = [a - b for a, b in zip(y, A(x))]  # @line L4
        if delta is not None and norm(r) <= tau * delta:  # @line L5
            break
        yk = [a + b for a, b in zip(yk, r)]  # @line L6
        ys.append(yk[:])
    return x, xs, ys  # @line L7


def soft_threshold(lam: float) -> Callable[[Vec], Vec]:
    """Exact inner solver for A = I, R = ||.||_1: argmin (1/2)||x - d||^2 + lam ||x||_1."""
    return lambda d: [math.copysign(max(abs(a) - lam, 0.0), a) for a in d]


def tv1d(lam: float, tol: float = 1e-13, max_iter: int = 200000) -> Callable[[Vec], Vec]:
    """Inner solver for A = I, R = sum |x_{i+1} - x_i| on a signal.

    It runs FISTA on the dual problem min_{|p_i| <= 1} (1/2)||d - lam D^T p||^2
    with the step 1/(4 lam^2) and stops when the duality gap is at most tol.
    Then ||x - x*||^2 <= 2 tol. Cost O(n) per step.
    """
    def solve(d: Vec) -> Vec:
        n = len(d)
        if n == 1:
            return d[:]

        def DT(p: Vec) -> Vec:  # D^T p, with (D x)_i = x_{i+1} - x_i
            out = [0.0] * n
            for i, v in enumerate(p):
                out[i] -= v
                out[i + 1] += v
            return out

        p = [0.0] * (n - 1)
        q = p[:]
        t = 1.0
        x = d[:]
        for it in range(max_iter):
            w = DT(q)
            x = [a - lam * b for a, b in zip(d, w)]
            g = [x[i + 1] - x[i] for i in range(n - 1)]  # minus the dual gradient / lam
            p_new = [min(1.0, max(-1.0, a + b / (4.0 * lam))) for a, b in zip(q, g)]
            t_new = (1.0 + math.sqrt(1.0 + 4.0 * t * t)) / 2.0
            q = [a + (t - 1.0) / t_new * (a - b) for a, b in zip(p_new, p)]
            p, t = p_new, t_new
            if it % 20 == 0:
                x = [a - lam * b for a, b in zip(d, DT(p))]
                primal = 0.5 * sum((a - b) ** 2 for a, b in zip(x, d)) + lam * sum(abs(x[i + 1] - x[i]) for i in range(n - 1))
                dual = 0.5 * sum(a * a for a in d) - 0.5 * sum(a * a for a in x)
                if primal - dual <= tol:
                    return x
        return [a - lam * b for a, b in zip(d, DT(p))]
    return solve


def lasso_fista(A: list[list[float]], lam: float, iters: int = 3000) -> Callable[[Vec], Vec]:
    """Inner solver for R = ||.||_1 and a matrix A: FISTA with step 1/||A||_F^2. Cost O(iters m n)."""
    m, n = len(A), len(A[0])
    L = sum(a * a for row in A for a in row)

    def solve(d: Vec) -> Vec:
        x = [0.0] * n
        z = x[:]
        t = 1.0
        for _ in range(iters):
            r = [sum(A[i][j] * z[j] for j in range(n)) - d[i] for i in range(m)]
            g = [sum(A[i][j] * r[i] for i in range(m)) for j in range(n)]
            v = [a - b / L for a, b in zip(z, g)]
            x_new = [math.copysign(max(abs(a) - lam / L, 0.0), a) for a in v]
            t_new = (1.0 + math.sqrt(1.0 + 4.0 * t * t)) / 2.0
            z = [a + (t - 1.0) / t_new * (a - b) for a, b in zip(x_new, x)]
            x, t = x_new, t_new
        return x
    return solve


def matvec(A: list[list[float]]) -> Callable[[Vec], Vec]:
    return lambda x: [sum(a * b for a, b in zip(row, x)) for row in A]
