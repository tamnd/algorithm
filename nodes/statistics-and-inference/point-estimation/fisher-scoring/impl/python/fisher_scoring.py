# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fisher-scoring/. The authors are listed in prov/Y142G8.jsonl.

import math
from collections.abc import Callable, Sequence
from typing import NamedTuple

Vector = list
Matrix = list


class ScoringResult(NamedTuple):
    theta: list            # the last iterate
    cov: list              # inverse expected information at theta
    iterations: int        # number of steps taken
    converged: bool        # True when the decrement g' I^-1 g fell to tol
    path: list             # all iterates, path[0] = theta0
    logliks: list          # log-likelihood at each iterate (empty without loglik)


def solve(a: Matrix, b: Vector) -> Vector:
    """Solve a x = b by Gaussian elimination with partial pivoting.

    Works for float and Fraction entries. Precondition: a is square and
    nonsingular. Cost: O(k^3) for a k x k matrix.
    """
    k = len(a)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ZeroDivisionError("singular information matrix")
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, k):
            f = m[r][c] / m[c][c]
            if f != 0:
                for j in range(c, k + 1):
                    m[r][j] = m[r][j] - f * m[c][j]
    x = [0] * k
    for r in range(k - 1, -1, -1):
        s = m[r][k]
        for j in range(r + 1, k):
            s = s - m[r][j] * x[j]
        x[r] = s / m[r][r]
    return x


def inverse(a: Matrix) -> Matrix:
    """Return the inverse of a nonsingular square matrix, column by column."""
    k = len(a)
    cols = [solve(a, [1 if i == j else 0 for i in range(k)]) for j in range(k)]
    return [[cols[j][i] for j in range(k)] for i in range(k)]


def fisher_scoring(
    score: Callable[[Vector], Vector],
    information: Callable[[Vector], Matrix],
    theta0: Sequence,
    loglik: Callable[[Vector], float] | None = None,
    tol: float = 1e-10,
    max_iter: int = 100,
    min_step: float = 2.0 ** -30,
) -> ScoringResult:
    """Maximize a log-likelihood by Fisher scoring with step halving.

    score(theta) is the score of the sample U_n(theta), information(theta) the
    expected information I_n(theta), which must be positive definite. With
    loglik given, each step is halved until the log-likelihood does not fall.
    Stops when g' I^-1 g <= tol. Exact for Fraction inputs when loglik is None.
    Cost per step: one score, one information, O(k^3) for the solve.
    """
    theta = list(theta0)  # @line L1
    path = [list(theta)]
    lls = [loglik(theta)] if loglik is not None else []
    for t in range(max_iter):  # @line L2
        g = score(theta)  # @line L3
        h = information(theta)  # @line L4
        delta = solve(h, g)  # @line L5
        dec = sum(gi * di for gi, di in zip(g, delta))
        if dec <= tol:  # @line L6
            return ScoringResult(theta, inverse(h), t, True, path, lls)
        s = 1  # @line L7
        new = [ti + s * di for ti, di in zip(theta, delta)]
        if loglik is not None:
            l_old = lls[-1]
            l_new = loglik(new)
            while l_new < l_old and s > min_step:  # @line L8
                s = s / 2
                new = [ti + s * di for ti, di in zip(theta, delta)]
                l_new = loglik(new)
            if l_new < l_old:  # @line L9
                return ScoringResult(theta, inverse(h), t, False, path, lls)
            lls.append(l_new)
        theta = new  # @line L10
        path.append(list(theta))
    return ScoringResult(theta, inverse(information(theta)), max_iter, False, path, lls)  # @line L11


# Generalized linear models: mean function, its derivative and the variance.

def _phi(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def _sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


LINKS = {
    # name: (mu(eta), dmu/deta(eta))
    "logit": (_sigmoid, lambda e: _sigmoid(e) * _sigmoid(-e)),
    "probit": (lambda e: 0.5 * math.erfc(-e / math.sqrt(2.0)), _phi),
    "log": (math.exp, math.exp),
    "identity": (lambda e: e, lambda e: 1.0),
}


def _binomial_ll(y: float, eta: float, link: str) -> float:
    if link == "logit":
        # log mu = -log(1 + e^-eta), log(1 - mu) = -log(1 + e^eta), computed stably
        lp = -(math.log1p(math.exp(-eta)) if eta > -30 else -eta + math.log1p(math.exp(eta)))
        lq = -(math.log1p(math.exp(eta)) if eta < 30 else eta + math.log1p(math.exp(-eta)))
    else:
        p = 0.5 * math.erfc(-eta / math.sqrt(2.0))
        q = 0.5 * math.erfc(eta / math.sqrt(2.0))
        if (y > 0 and p == 0.0) or (y < 1 and q == 0.0):
            return -math.inf
        lp = math.log(p) if p > 0 else 0.0
        lq = math.log(q) if q > 0 else 0.0
    return y * lp + (1 - y) * lq


def _poisson_ll(y: float, eta: float, link: str) -> float:
    mu = math.exp(eta) if link == "log" else eta
    if mu <= 0:
        return -math.inf if (y > 0 or link == "identity") else 0.0
    return y * math.log(mu) - mu - math.lgamma(y + 1)


FAMILIES = {
    # name: (variance(mu), loglik of one observation)
    "binomial": (lambda m: m * (1.0 - m), _binomial_ll),
    "poisson": (lambda m: m, _poisson_ll),
}


class GLMFit(NamedTuple):
    beta: list
    cov: list
    iterations: int
    converged: bool
    separated: bool
    loglik: float
    path: list


def glm_fisher_scoring(
    x: Sequence[Sequence[float]],
    y: Sequence[float],
    family: str = "binomial",
    link: str = "logit",
    beta0: Sequence[float] | None = None,
    tol: float = 1e-10,
    max_iter: int = 100,
    halving: bool = True,
) -> GLMFit:
    """Fit a GLM by Fisher scoring. x is n x p with full column rank.

    Score U = sum x_i (y_i - mu_i) mu'_i / V(mu_i); information
    I = sum x_i x_i' mu'_i^2 / V(mu_i). For the identity link with Poisson
    data, beta0 must give positive means. halving=False takes full steps
    (plain scoring). separated is True for a binomial
    fit whose fitted means all lie within 1e-8 of the responses.
    Cost per step: O(n p^2 + p^3).
    """
    mean_fn, dmean = LINKS[link]
    var_fn, ll_one = FAMILIES[family]
    p = len(x[0])

    def eta_of(b):
        return [sum(xi[j] * b[j] for j in range(p)) for xi in x]

    def score(b):
        g = [0.0] * p
        for xi, yi, e in zip(x, y, eta_of(b)):
            m, d = mean_fn(e), dmean(e)
            v = var_fn(m)
            w = (yi - m) * d / v if v > 0 else 0.0  # a mean at 0 or 1 adds nothing
            for j in range(p):
                g[j] += xi[j] * w
        return g

    def information(b):
        h = [[0.0] * p for _ in range(p)]
        for xi, e in zip(x, eta_of(b)):
            m, d = mean_fn(e), dmean(e)
            v = var_fn(m)
            w = d * d / v if v > 0 else 0.0
            for j in range(p):
                for k in range(p):
                    h[j][k] += xi[j] * xi[k] * w
        return h

    def loglik(b):
        return sum(ll_one(yi, e, link) for yi, e in zip(y, eta_of(b)))

    start = list(beta0) if beta0 is not None else [0.0] * p
    res = fisher_scoring(score, information, start, loglik if halving else None, tol, max_iter)
    mus = [mean_fn(e) for e in eta_of(res.theta)]
    separated = family == "binomial" and all(abs(m - yi) < 1e-8 for m, yi in zip(mus, y))
    return GLMFit(res.theta, res.cov, res.iterations, res.converged, separated, loglik(res.theta), res.path)
