# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iteratively-reweighted-least-squares/. The authors are listed in prov/N4YG7R.jsonl.
"""Iteratively reweighted least squares for GLMs and for M-estimation.

Each iteration computes the linear predictor eta = X b, asks a working rule
for weights w_i >= 0 and a working response z_i, and solves the weighted
least squares problem min sum w_i (z_i - x_i^T b)^2 by a Householder QR of
the rows scaled by sqrt(w_i).

Working rules:
  GLM rules (logistic, probit, Poisson): z = eta + (y - mu) g'(mu) and
  w = 1 / (V(mu) g'(mu)^2). This is Fisher scoring, and Newton for a canonical link.
  M rules (Huber, Tukey biweight, L1 with a floor delta): z = y and
  w = f'(r^2) for the loss rho(r) = f(r^2) with f concave, which makes each
  step a majorize-minimize step, so the loss never increases.
"""

import math
from statistics import NormalDist
from typing import NamedTuple

RANK_TOL = 1e-12
_STD = NormalDist()


class IRLSResult(NamedTuple):
    b: list            # the final coefficients
    iterations: int    # weighted least squares solves done
    converged: bool    # True if the step test of line L6 passed
    objective: list    # the objective after each iteration (deviance or M loss)


def weighted_ls(x: list, z: list, w: list) -> list:
    """argmin sum w_i (z_i - x_i^T b)^2 by Householder QR of the scaled rows; rows with w_i = 0 drop out."""
    rows = [[math.sqrt(wi) * v for v in xi] for xi, wi in zip(x, w) if wi > 0.0]
    rhs = [math.sqrt(wi) * zi for zi, wi in zip(z, w) if wi > 0.0]
    n = len(rows)
    p = len(x[0])
    if n < p:
        raise ValueError("fewer rows with positive weight than coefficients")
    col = [math.sqrt(math.fsum(rows[i][j] ** 2 for i in range(n))) for j in range(p)]
    for j in range(p):
        norm = math.sqrt(math.fsum(rows[i][j] ** 2 for i in range(j, n)))
        if norm == 0.0 or norm <= RANK_TOL * col[j]:
            raise ValueError("the weighted design has rank below p")
        alpha = -norm if rows[j][j] >= 0.0 else norm
        v = [rows[j][j] - alpha] + [rows[i][j] for i in range(j + 1, n)]
        vv = math.fsum(t * t for t in v)
        for k in range(j, p):
            s = 2.0 * math.fsum(v[i - j] * rows[i][k] for i in range(j, n)) / vv
            for i in range(j, n):
                rows[i][k] -= s * v[i - j]
        s = 2.0 * math.fsum(v[i - j] * rhs[i] for i in range(j, n)) / vv
        for i in range(j, n):
            rhs[i] -= s * v[i - j]
    b = [0.0] * p
    for i in range(p - 1, -1, -1):
        b[i] = (rhs[i] - math.fsum(rows[i][k] * b[k] for k in range(i + 1, p))) / rows[i][i]
    return b


# ---------- GLM working rules: (w, z) from (y, eta), and the deviance ----------

def _xlogy(a: float, b: float) -> float:
    return 0.0 if a == 0.0 else a * math.log(b)


class Logistic:
    """Bernoulli response with the logit link (canonical): w = mu (1 - mu), z = eta + (y - mu) / w."""
    MU_EPS = 1e-12

    def mean(self, eta: float) -> float:
        return 1.0 / (1.0 + math.exp(-eta)) if eta >= 0.0 else math.exp(eta) / (1.0 + math.exp(eta))

    def working(self, y: list, eta: list) -> tuple[list, list]:
        w, z = [], []
        for yi, e in zip(y, eta):
            mu = min(max(self.mean(e), self.MU_EPS), 1.0 - self.MU_EPS)
            v = mu * (1.0 - mu)
            w.append(v)
            z.append(e + (yi - mu) / v)
        return w, z

    def objective(self, y: list, eta: list) -> float:
        """The deviance -2 log-likelihood, computed without overflow."""
        return 2.0 * math.fsum(math.log1p(math.exp(-abs(e))) + max(e, 0.0) - yi * e
                               for yi, e in zip(y, eta))


class Probit:
    """Bernoulli response with the probit link (not canonical): Fisher scoring, not Newton."""
    MU_EPS = 1e-12

    def mean(self, eta: float) -> float:
        return _STD.cdf(eta)

    def working(self, y: list, eta: list) -> tuple[list, list]:
        w, z = [], []
        for yi, e in zip(y, eta):
            mu = min(max(self.mean(e), self.MU_EPS), 1.0 - self.MU_EPS)
            d = max(_STD.pdf(e), 1e-300)  # d mu / d eta = 1 / g'(mu)
            w.append(d * d / (mu * (1.0 - mu)))
            z.append(e + (yi - mu) / d)
        return w, z

    def objective(self, y: list, eta: list) -> float:
        out = []
        for yi, e in zip(y, eta):
            mu = min(max(self.mean(e), self.MU_EPS), 1.0 - self.MU_EPS)
            out.append(-2.0 * (_xlogy(yi, mu) + _xlogy(1.0 - yi, 1.0 - mu)))
        return math.fsum(out)


class Poisson:
    """Poisson response with the log link (canonical): w = mu, z = eta + (y - mu) / mu."""

    def mean(self, eta: float) -> float:
        return math.exp(eta)

    def working(self, y: list, eta: list) -> tuple[list, list]:
        mus = [math.exp(e) for e in eta]
        return mus, [e + (yi - mu) / mu for yi, e, mu in zip(y, eta, mus)]

    def objective(self, y: list, eta: list) -> float:
        """The deviance 2 sum (y log(y / mu) - (y - mu))."""
        return 2.0 * math.fsum(_xlogy(yi, yi) - yi * e - (yi - math.exp(e)) for yi, e in zip(y, eta))


# ---------- M-estimation rules: rho(r / s) = f((r / s)^2) with f concave ----------

class Huber:
    """rho(u) = u^2 / 2 for |u| <= c, c |u| - c^2 / 2 beyond; weight min(1, c / |u|)."""

    def __init__(self, c: float = 1.345, scale: float = 1.0):
        self.c, self.s = c, scale

    def working(self, y: list, eta: list) -> tuple[list, list]:
        w = []
        for yi, e in zip(y, eta):
            u = abs(yi - e) / self.s
            w.append(1.0 if u <= self.c else self.c / u)
        return w, list(y)

    def objective(self, y: list, eta: list) -> float:
        c = self.c
        return math.fsum(u * u / 2.0 if u <= c else c * u - c * c / 2.0
                         for u in (abs(yi - e) / self.s for yi, e in zip(y, eta)))


class Biweight:
    """Tukey's biweight: rho(u) = (c^2 / 6)(1 - (1 - (u / c)^2)^3) for |u| <= c, c^2 / 6 beyond;
    weight (1 - (u / c)^2)^2, zero beyond c. The loss is not convex."""

    def __init__(self, c: float = 4.685, scale: float = 1.0):
        self.c, self.s = c, scale

    def working(self, y: list, eta: list) -> tuple[list, list]:
        w = []
        for yi, e in zip(y, eta):
            t = ((yi - e) / (self.s * self.c)) ** 2
            w.append((1.0 - t) ** 2 if t < 1.0 else 0.0)
        return w, list(y)

    def objective(self, y: list, eta: list) -> float:
        c = self.c
        out = []
        for yi, e in zip(y, eta):
            t = ((yi - e) / (self.s * c)) ** 2
            out.append(c * c / 6.0 * (1.0 - (1.0 - t) ** 3) if t < 1.0 else c * c / 6.0)
        return math.fsum(out)


class L1:
    """Least absolute deviations with a floor delta > 0: weight 1 / max(|r|, delta).
    This is exact majorize-minimize for the smoothed loss r^2 / (2 delta) (|r| <= delta),
    |r| - delta / 2 (beyond), which is within delta / 2 of |r|."""

    def __init__(self, delta: float = 1e-6):
        if not delta > 0.0:
            raise ValueError("delta must be positive")
        self.delta = delta

    def working(self, y: list, eta: list) -> tuple[list, list]:
        return [1.0 / max(abs(yi - e), self.delta) for yi, e in zip(y, eta)], list(y)

    def objective(self, y: list, eta: list) -> float:
        d = self.delta
        return math.fsum(r * r / (2.0 * d) if r <= d else r - d / 2.0
                         for r in (abs(yi - e) for yi, e in zip(y, eta)))


# ---------- the algorithm ----------

def _eta(x: list, b: list) -> list:
    return [math.fsum(a * c for a, c in zip(xi, b)) for xi in x]


def irls(x: list, y: list, rule, b0: list | None = None, tol: float = 1e-10,
         maxit: int = 100) -> IRLSResult:
    """Iteratively reweighted least squares with the given working rule.

    Each iteration costs one weighted least squares solve, Theta(n p^2).
    """
    if len(x) != len(y) or not x:
        raise ValueError("x and y must be nonempty and of the same length")
    p = len(x[0])
    b = list(b0) if b0 is not None else [0.0] * p  # @line L1
    history = []
    for k in range(1, maxit + 1):  # @line L2
        eta = _eta(x, b)  # @line L3
        w, z = rule.working(y, eta)  # @line L4
        b_new = weighted_ls(x, z, w)  # @line L5
        history.append(rule.objective(y, _eta(x, b_new)))
        step = math.sqrt(math.fsum((u - v) ** 2 for u, v in zip(b_new, b)))
        size = math.sqrt(math.fsum(v * v for v in b_new))
        if step <= tol * (size + tol):  # @line L6
            return IRLSResult(b_new, k, True, history)
        b = b_new  # @line L7
    return IRLSResult(b, maxit, False, history)  # @line L8


def separation_suspected(x: list, y: list, b: list, eps: float = 1e-8) -> bool:
    """For a binary GLM: True if some fitted probability is within eps of 0 or 1,
    the symptom of (quasi-)complete separation, where the MLE does not exist."""
    m = Logistic()
    return any(m.mean(e) < eps or m.mean(e) > 1.0 - eps for e in _eta(x, b))
