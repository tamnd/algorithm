# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iteratively-regularized-gauss-newton/. The authors are listed in prov/KK6851.jsonl.
"""The iteratively regularized Gauss-Newton method (IRGNM) for F(x) = y with noisy data.

One step solves a Tikhonov problem for the linearization of F at x_k, with
the penalty centered at the initial guess x0:

    x_{k+1} = x_k + (J_k^T J_k + alpha_k I)^(-1) [J_k^T (y - F(x_k)) + alpha_k (x0 - x_k)],

where J_k = F'(x_k) and alpha_k = alpha0 q^k with 0 < q < 1. The method stops
by the discrepancy principle: at the first k with ||y - F(x_k)|| <= tau delta.

F returns a list and jac returns the Jacobian as a list of rows. The inner
system is solved by Gaussian elimination, which is exact on Fractions.
"""

import math

from imgla import matvec, solve


def _norm(v):
    return math.sqrt(sum(t * t for t in v))


def irgnm_step(jac_x, r, x, x0, alpha):
    """Solve (J^T J + alpha I) h = J^T r + alpha (x0 - x) and return x + h."""
    n = len(x)
    jt = [[jac_x[i][j] for i in range(len(jac_x))] for j in range(n)]
    m = [[sum(p * q for p, q in zip(jt[i], jt[j])) + (alpha if i == j else 0)
          for j in range(n)] for i in range(n)]
    jtr = [sum(p * q for p, q in zip(row, r)) for row in jt]
    rhs = [g + alpha * (a - b) for g, a, b in zip(jtr, x0, x)]
    h = solve(m, rhs)  # @line L5
    return [xi + hi for xi, hi in zip(x, h)]  # @line L6


class IRGNMResult:
    """x: the last iterate; k: steps done; iterates: x_0, ..., x_k; residuals:
    ||y - F(x_j)||; alphas: alpha_j used in step j; stopped: "discrepancy" or "maxit"."""

    def __init__(self, **kw):
        self.__dict__.update(kw)


def irgnm(f, jac, y, x0, alpha0, q=0.5, kmax=50, delta=None, tau=2.0):
    """Run at most kmax IRGNM steps from x0 with alpha_k = alpha0 q^k."""
    x = list(x0)
    alpha = alpha0  # @line L1
    iterates, residuals, alphas = [list(x)], [], []
    for k in range(kmax):  # @line L2
        r = [yi - fi for yi, fi in zip(y, f(x))]
        rn = _norm(r)
        residuals.append(rn)
        if delta is not None and rn <= tau * delta:  # @line L3
            return IRGNMResult(x=x, k=k, iterates=iterates, residuals=residuals,
                               alphas=alphas, stopped="discrepancy")
        jx = jac(x)  # @line L4
        x = irgnm_step(jx, r, x, x0, alpha)
        alphas.append(alpha)
        alpha = alpha * q  # @line L7
        iterates.append(list(x))
    residuals.append(_norm([yi - fi for yi, fi in zip(y, f(x))]))
    stopped = "discrepancy" if delta is not None and residuals[-1] <= tau * delta else "maxit"
    return IRGNMResult(x=x, k=kmax, iterates=iterates, residuals=residuals,  # @line L8
                       alphas=alphas, stopped=stopped)


def exp_integration_problem(n):
    """F(x) = A exp(x) with (A x)_i = h (x_1 + ... + x_i), h = 1 / n.

    This is a discrete form of F(x)(s) = int_0^s exp(x(t)) dt. Returns (F, F', A).
    """
    h = 1.0 / n
    a = [[h if j <= i else 0.0 for j in range(n)] for i in range(n)]

    def f(x):
        return matvec(a, [math.exp(t) for t in x])

    def jac(x):
        ex = [math.exp(t) for t in x]
        return [[row[j] * ex[j] for j in range(n)] for row in a]

    return f, jac, a
