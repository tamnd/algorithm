# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplace-approximation/. The authors are listed in prov/M8AVZX.jsonl.
"""The Laplace approximation of a posterior and of its normalizing constant.

The input is the unnormalized log posterior l(theta) = log f(x | theta) + log pi(theta)
with its gradient and Hessian. laplace() finds the mode by Newton's method with a
Cholesky solve and step halving, then returns the mode, the covariance H^-1 with
H = -Hessian at the mode, and

    log Z_hat = l(theta_hat) + (d/2) log(2 pi) - (1/2) log det H,

the Laplace approximation of log Z = log of the integral of exp(l). The relative error
of Z_hat is O(1/n) for n observations under the conditions on the page.

The other functions are the worked examples of the page: the beta-binomial model in
the probability scale and in the logit scale, Stirling's formula as the Laplace
approximation of Gamma(n + 1), and the Tierney-Kadane approximation of a posterior mean.

Cost: each Newton step costs one gradient, one Hessian and a Cholesky factorization,
Theta(d^3) arithmetic for d parameters. Newton converges quadratically near the mode.
"""

import math
from typing import Callable, Sequence

Vector = list[float]
Matrix = list[list[float]]

LOG_2PI = math.log(2.0 * math.pi)


def cholesky(a: Sequence[Sequence[float]]) -> Matrix:
    """Lower triangular L with L L^T = a. Raises ValueError if a is not positive definite.

    Cost: Theta(d^3) for a d by d matrix.
    """
    d = len(a)
    low = [[0.0] * d for _ in range(d)]
    for i in range(d):
        for j in range(i + 1):
            s = a[i][j] - math.fsum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                if s <= 0.0:
                    raise ValueError("matrix is not positive definite")
                low[i][i] = math.sqrt(s)
            else:
                low[i][j] = s / low[j][j]
    return low


def cholesky_solve(low: Matrix, b: Sequence[float]) -> Vector:
    """Solve L L^T y = b by forward and back substitution. Cost: Theta(d^2)."""
    d = len(b)
    z = [0.0] * d
    for i in range(d):
        z[i] = (b[i] - math.fsum(low[i][k] * z[k] for k in range(i))) / low[i][i]
    y = [0.0] * d
    for i in reversed(range(d)):
        y[i] = (z[i] - math.fsum(low[k][i] * y[k] for k in range(i + 1, d))) / low[i][i]
    return y


def inverse_from_cholesky(low: Matrix) -> Matrix:
    """(L L^T)^-1, column by column. Cost: Theta(d^3)."""
    d = len(low)
    cols = [cholesky_solve(low, [1.0 if r == c else 0.0 for r in range(d)]) for c in range(d)]
    return [[cols[c][r] for c in range(d)] for r in range(d)]


def laplace(
    logpost: Callable[[Vector], float],
    grad: Callable[[Vector], Vector],
    hess: Callable[[Vector], Matrix],
    theta0: Sequence[float],
    tol: float = 1e-12,
    max_iter: int = 200,
) -> tuple[Vector, Matrix, float]:
    """Return (theta_hat, covariance, log_z_hat) for the unnormalized log posterior logpost.

    Precondition: logpost has a unique interior maximum, and -hess is positive definite
    at every point where Newton steps are taken (the code raises ValueError otherwise).
    """
    theta = [float(t) for t in theta0]  # @line L1
    d = len(theta)
    for _ in range(max_iter):  # @line L2
        g = grad(theta)  # @line L3
        h = [[-v for v in row] for row in hess(theta)]
        low = cholesky(h)  # @line L4
        step = cholesky_solve(low, g)  # @line L5
        t, base = 1.0, logpost(theta)  # @line L6
        while True:
            trial = [theta[i] + t * step[i] for i in range(d)]
            val = logpost(trial)
            if val >= base or t < 1e-12:
                break
            t *= 0.5
        theta = trial  # @line L7
        if max(abs(t * s) for s in step) <= tol * (1.0 + max(abs(v) for v in theta)):  # @line L8
            break
    h = [[-v for v in row] for row in hess(theta)]  # @line L9
    low = cholesky(h)
    log_det_h = 2.0 * math.fsum(math.log(low[i][i]) for i in range(d))
    log_z = logpost(theta) + 0.5 * d * LOG_2PI - 0.5 * log_det_h  # @line L10
    return theta, inverse_from_cholesky(low), log_z  # @line L11


def log_beta(a: float, b: float) -> float:
    """log B(a, b) = log Gamma(a) + log Gamma(b) - log Gamma(a + b)."""
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def beta_binomial_log_z(x: int, n: int, a: float, b: float) -> float:
    """Exact log Z for x successes in n Bernoulli trials with prior Beta(a, b).

    Z = integral of p^x (1 - p)^(n - x) Beta(p; a, b) dp = B(a + x, b + n - x) / B(a, b).
    """
    return log_beta(a + x, b + n - x) - log_beta(a, b)


def beta_binomial_laplace_p(x: int, n: int, a: float, b: float) -> float:
    """Laplace log Z in the probability scale p. Needs a + x > 1 and b + n - x > 1."""
    al, be = a + x - 1.0, b + n - x - 1.0
    lb = log_beta(a, b)

    def lp(v: Vector) -> float:
        p = v[0]
        if not 0.0 < p < 1.0:
            return -math.inf
        return al * math.log(p) + be * math.log1p(-p) - lb

    def gr(v: Vector) -> Vector:
        p = v[0]
        return [al / p - be / (1.0 - p)]

    def he(v: Vector) -> Matrix:
        p = v[0]
        return [[-al / p**2 - be / (1.0 - p) ** 2]]

    return laplace(lp, gr, he, [(al + 0.5) / (al + be + 1.0)])[2]


def beta_binomial_laplace_logit(x: int, n: int, a: float, b: float) -> float:
    """Laplace log Z in the logit scale theta = log(p / (1 - p)), Jacobian p (1 - p) included."""
    al, be = a + x, b + n - x
    lb = log_beta(a, b)

    def lp(v: Vector) -> float:
        t = v[0]
        # log sigma(t) = -log(1 + e^-t), log(1 - sigma(t)) = -log(1 + e^t)
        return -al * _log1pexp(-t) - be * _log1pexp(t) - lb

    def gr(v: Vector) -> Vector:
        p = _sigmoid(v[0])
        return [al - (al + be) * p]

    def he(v: Vector) -> Matrix:
        p = _sigmoid(v[0])
        return [[-(al + be) * p * (1.0 - p)]]

    return laplace(lp, gr, he, [0.0])[2]


def _sigmoid(t: float) -> float:
    if t >= 0:
        return 1.0 / (1.0 + math.exp(-t))
    e = math.exp(t)
    return e / (1.0 + e)


def _log1pexp(t: float) -> float:
    """log(1 + e^t) without overflow."""
    if t > 0:
        return t + math.log1p(math.exp(-t))
    return math.log1p(math.exp(t))


def stirling_log(n: float) -> float:
    """Laplace approximation of log Gamma(n + 1) = log of the integral of t^n e^-t dt.

    With t = n s the integrand is n^(n+1) exp(n (log s - s)); the maximum is at s = 1
    with -h''(1) = 1, which gives n^(n+1) e^-n sqrt(2 pi / n) = sqrt(2 pi n) n^n e^-n.
    """
    return 0.5 * math.log(2.0 * math.pi * n) + n * math.log(n) - n


def tierney_kadane_beta_mean(al: float, be: float) -> float:
    """Tierney-Kadane approximation of E[p] for p ~ Beta(al, be), in the logit scale.

    E[p] = (integral of p * p^al (1 - p)^be dtheta) / (integral of p^al (1 - p)^be dtheta)
    in the logit scale theta. Each integral gets its own Laplace approximation (the fully
    exponential form), so the mode moves for the numerator. The exact answer is
    al / (al + be). The relative error is O(1/n^2) when al and be grow like n.
    """

    def log_z(a1: float, b1: float) -> float:
        # Laplace for the integral of sigma^a1 (1 - sigma)^b1 dtheta: mode p = a1/(a1 + b1),
        # curvature (a1 + b1) p (1 - p).
        p = a1 / (a1 + b1)
        return a1 * math.log(p) + b1 * math.log1p(-p) + 0.5 * LOG_2PI - 0.5 * math.log((a1 + b1) * p * (1 - p))

    return math.exp(log_z(al + 1.0, be) - log_z(al, be))


def gaussian_log_z(mu: Sequence[float], prec: Sequence[Sequence[float]], c: float) -> float:
    """Exact log of the integral of exp(c - (theta - mu)^T Q (theta - mu) / 2)."""
    low = cholesky(prec)
    d = len(mu)
    return c + 0.5 * d * LOG_2PI - math.fsum(math.log(low[i][i]) for i in range(d))
