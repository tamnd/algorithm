# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/integrated-nested-laplace-approximation/. The authors are listed in prov/VKP2D8.jsonl.
"""Integrated nested Laplace approximation (Rue, Martino and Chopin 2009) for a latent
Gaussian model

    theta ~ pi(theta),   x | theta ~ N(0, Q(theta)^-1),   y_j | x ~ p(y_j | x_j),

with one hyperparameter theta on a given grid. Dense matrices, so it suits small n; the
real method uses a sparse Cholesky factor of Q + D, which is the only change needed.

lik(j, v) returns (log p(y_j | x_j = v), first derivative, second derivative) in v.
The second derivative must be negative (log-concave likelihood terms).
"""

import math
from typing import Callable, Sequence

Matrix = list[list[float]]


def cholesky(a: Matrix) -> Matrix:
    """Lower triangular L with a = L L^T. Raises ValueError if a is not positive definite."""
    n = len(a)
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - math.fsum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                if s <= 0:
                    raise ValueError("matrix is not positive definite")
                low[i][i] = math.sqrt(s)
            else:
                low[i][j] = s / low[j][j]
    return low


def chol_solve(low: Matrix, b: Sequence[float]) -> list[float]:
    n = len(low)
    z = [0.0] * n
    for i in range(n):
        z[i] = (b[i] - math.fsum(low[i][k] * z[k] for k in range(i))) / low[i][i]
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (z[i] - math.fsum(low[k][i] * x[k] for k in range(i + 1, n))) / low[i][i]
    return x


def log_det(low: Matrix) -> float:
    return 2.0 * math.fsum(math.log(low[i][i]) for i in range(len(low)))


def quad_form(q: Matrix, x: Sequence[float]) -> float:
    return math.fsum(x[i] * q[i][j] * x[j] for i in range(len(x)) for j in range(len(x)))


def log_joint(q: Matrix, lik: Callable, x: Sequence[float]) -> float:
    """-1/2 x^T Q x + sum_j log p(y_j | x_j): log pi(x, y | theta) up to terms in theta only."""
    return -0.5 * quad_form(q, x) + math.fsum(lik(j, v)[0] for j, v in enumerate(x))


def inner_mode(q: Matrix, lik: Callable, x0: Sequence[float], fixed: dict | None = None,
               tol: float = 1e-12, max_iter: int = 100) -> tuple[list[float], Matrix]:
    """Newton's method for the mode of log_joint over the free coordinates.

    Coordinates in `fixed` (index -> value) are held. Each step solves (Q + D) x = b on
    the free coordinates, with D = diag(-second derivatives) and b = D x + gradient terms,
    and halves the step while the objective does not increase. Returns the mode and the
    Cholesky factor of the precision Q + D of the free coordinates at the mode.
    """
    fixed = fixed or {}
    n = len(q)
    free = [i for i in range(n) if i not in fixed]
    x = [fixed.get(i, x0[i]) for i in range(n)]
    f = log_joint(q, lik, x)
    for _ in range(max_iter):
        terms = [lik(j, x[j]) for j in range(n)]
        p = [[q[a][b] for b in free] for a in free]
        for r, a in enumerate(free):
            p[r][r] -= terms[a][2]
        rhs = [-terms[a][2] * x[a] + terms[a][1] - math.fsum(q[a][b] * fixed[b] for b in fixed) for a in free]
        low = cholesky(p)
        target = chol_solve(low, rhs)
        step = 1.0
        while True:
            y = list(x)
            for r, a in enumerate(free):
                y[a] = x[a] + step * (target[r] - x[a])
            fy = log_joint(q, lik, y)
            if fy >= f - 1e-14 or step < 1e-10:
                break
            step /= 2
        done = max((abs(y[a] - x[a]) for a in free), default=0.0) < tol
        x, f = y, fy
        if done:
            break
    terms = [lik(j, x[j]) for j in range(n)]
    p = [[q[a][b] for b in free] for a in free]
    for r, a in enumerate(free):
        p[r][r] -= terms[a][2]
    return x, cholesky(p)


def _trapezoid(z: Sequence[float], f: Sequence[float]) -> float:
    return math.fsum((z[g + 1] - z[g]) * (f[g] + f[g + 1]) / 2 for g in range(len(z) - 1))


def inla(
    q_of: Callable[[float], Matrix],
    log_prior: Callable[[float], float],
    lik: Callable,
    thetas: Sequence[float],
    index: int,
    zs: Sequence[float],
    strategy: str = "laplace",
) -> dict:
    """INLA on a grid of equally spaced hyperparameter values.

    Returns a dict with
      'weights'  : normalized weights of the grid values thetas (they approximate pi(theta | y) * spacing),
      'log_post' : unnormalized log pi~(theta_k | y),
      'modes'    : the inner modes x*(theta_k),
      'density'  : pi~(x_index = z | y) on the points zs,
      'mean', 'sd': the mean and standard deviation of x_index under that density.
    strategy 'gaussian' uses the marginal of the Gaussian approximation in L6;
    'laplace' re-optimizes the other coordinates for every z (the full Laplace strategy).
    """
    n = len(q_of(thetas[0]))
    x0 = [0.0] * n
    log_post, modes, dens = [], [], []
    for th in thetas:  # @line L1
        q = q_of(th)
        x_star, low_p = inner_mode(q, lik, x0)  # @line L2
        x0 = x_star  # warm start for the next grid value
        low_q = cholesky(q)  # @line L3
        lp = log_prior(th) + 0.5 * log_det(low_q) + log_joint(q, lik, x_star) - 0.5 * log_det(low_p)  # @line L4
        log_post.append(lp)
        modes.append(x_star)
        if strategy == "gaussian":
            e = [0.0] * n
            e[index] = 1.0
            var = chol_solve(low_p, e)[index]
            f = [math.exp(-0.5 * (z - x_star[index]) ** 2 / var) for z in zs]
        else:
            logs = []
            start = x_star
            for z in zs:  # @line L5
                y, low_c = inner_mode(q, lik, start, fixed={index: z})
                start = y
                logs.append(log_joint(q, lik, y) - 0.5 * log_det(low_c))  # @line L6
            top = max(logs)
            f = [math.exp(v - top) for v in logs]
        tot = _trapezoid(zs, f)
        dens.append([v / tot for v in f])  # @line L7
    top = max(log_post)
    w = [math.exp(v - top) for v in log_post]
    tot = math.fsum(w)
    w = [v / tot for v in w]  # @line L8
    mix = [math.fsum(w[k] * dens[k][g] for k in range(len(thetas))) for g in range(len(zs))]  # @line L9
    mean = _trapezoid(zs, [z * f for z, f in zip(zs, mix)])
    var = _trapezoid(zs, [(z - mean) ** 2 * f for z, f in zip(zs, mix)])
    return {"weights": w, "log_post": log_post, "modes": modes, "density": mix,  # @line L10
            "mean": mean, "sd": math.sqrt(var)}


# Likelihood terms: (log p, d/dx, d2/dx2) for one observation given its latent value v.

def poisson_log_link(ys: Sequence[int]) -> Callable:
    def lik(j: int, v: float) -> tuple[float, float, float]:
        mu = math.exp(v)
        return ys[j] * v - mu - math.lgamma(ys[j] + 1), ys[j] - mu, -mu
    return lik


def bernoulli_logit(ys: Sequence[int]) -> Callable:
    def lik(j: int, v: float) -> tuple[float, float, float]:
        p = 1 / (1 + math.exp(-v))
        lp = -math.log1p(math.exp(-v)) if v > 0 else v - math.log1p(math.exp(v))
        return ys[j] * v - (v - lp), ys[j] - p, -p * (1 - p)
    return lik


def gaussian(ys: Sequence[float], s2: float) -> Callable:
    def lik(j: int, v: float) -> tuple[float, float, float]:
        return -0.5 * (ys[j] - v) ** 2 / s2 - 0.5 * math.log(2 * math.pi * s2), (ys[j] - v) / s2, -1 / s2
    return lik


def rw_precision(n: int, tau: float, kappa: float = 1.0) -> Matrix:
    """tau times the tridiagonal matrix with kappa + 2 (kappa + 1 at the ends) and -1 off the diagonal."""
    q = [[0.0] * n for _ in range(n)]
    for i in range(n):
        q[i][i] = tau * (kappa + (2.0 if 0 < i < n - 1 else 1.0))
        if i + 1 < n:
            q[i][i + 1] = q[i + 1][i] = -tau
    return q
