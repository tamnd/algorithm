# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/restricted-maximum-likelihood/. The authors are listed in prov/6YVPGK.jsonl.
"""Restricted (residual) maximum likelihood for variance components, by Fisher scoring.

The model is y ~ N(X b, V(theta)) with V(theta) = theta_1 V_1 + ... + theta_m V_m,
known symmetric matrices V_j and theta_j >= 0 (for example V_1 = Z Z^T for a
random effect and V_m = I for the residual). With A = X^T V^-1 X and
P = V^-1 - V^-1 X A^-1 X^T V^-1, the REML log-likelihood is

    l_R(theta) = -1/2 [ (n - p) log 2 pi + log|V| + log|A| - log|X^T X| + y^T P y ],

the log density of n - p error contrasts K^T y with K^T X = 0 and K^T K = I.
Its score is s_j = -1/2 tr(P V_j) + 1/2 y^T P V_j P y and its expected
information is I_jk = 1/2 tr(P V_j P V_k). Ordinary maximum likelihood
(method="ml") is the same with V^-1 in place of P in the trace terms.

Each step is theta + I^-1 s, projected onto theta >= 0 (a small floor keeps the
last component, the residual, positive), and halved until the log-likelihood
does not decrease. A component that ends at 0 is on the boundary; the
returned score must then be <= 0 (the Karush-Kuhn-Tucker condition).
"""

import math
from typing import NamedTuple

FLOOR = 1e-10


def _cholesky(a):
    n = len(a)
    l = [[0.0] * n for _ in range(n)]
    for j in range(n):
        d = a[j][j] - math.fsum(l[j][k] ** 2 for k in range(j))
        if not d > 0.0:
            raise ValueError("matrix is not positive definite")
        l[j][j] = math.sqrt(d)
        for i in range(j + 1, n):
            l[i][j] = (a[i][j] - math.fsum(l[i][k] * l[j][k] for k in range(j))) / l[j][j]
    return l


def _chol_solve(l, b):
    n = len(l)
    z = [0.0] * n
    for i in range(n):
        z[i] = (b[i] - math.fsum(l[i][k] * z[k] for k in range(i))) / l[i][i]
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (z[i] - math.fsum(l[k][i] * x[k] for k in range(i + 1, n))) / l[i][i]
    return x


def _logdet(l):
    return 2.0 * math.fsum(math.log(l[i][i]) for i in range(len(l)))


def _inverse(a):
    l = _cholesky(a)
    n = len(a)
    cols = [_chol_solve(l, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)]
    return [list(r) for r in zip(*cols)], _logdet(l)


def _matmul(a, b):
    bt = list(zip(*b))
    return [[math.fsum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


class Pieces(NamedTuple):
    loglik: float
    score: list
    info: list
    b: list


def evaluate(y, x, vs, theta, method="reml"):
    """Log-likelihood, score, expected information and GLS estimate b at theta."""
    n, p = len(y), len(x[0])
    v = [[math.fsum(t * vj[i][k] for t, vj in zip(theta, vs)) for k in range(n)] for i in range(n)]
    vi, logdet_v = _inverse(v)
    vix = _matmul(vi, x)
    a = _matmul([list(c) for c in zip(*x)], vix)
    ai, logdet_a = _inverse(a)
    proj = [[vi[i][k] - math.fsum(vix[i][s] * math.fsum(ai[s][t] * vix[k][t] for t in range(p)) for s in range(p))
             for k in range(n)] for i in range(n)]
    py = [math.fsum(proj[i][k] * y[k] for k in range(n)) for i in range(n)]
    quad = math.fsum(a_ * b_ for a_, b_ in zip(y, py))
    xty_v = [math.fsum(vix[k][s] * y[k] for k in range(n)) for s in range(p)]
    b = [math.fsum(ai[s][t] * xty_v[t] for t in range(p)) for s in range(p)]
    if method == "reml":
        xtx = _matmul([list(c) for c in zip(*x)], x)
        logdet_xtx = _logdet(_cholesky(xtx))
        loglik = -0.5 * ((n - p) * math.log(2 * math.pi) + logdet_v + logdet_a - logdet_xtx + quad)
        m = proj
    elif method == "ml":
        loglik = -0.5 * (n * math.log(2 * math.pi) + logdet_v + quad)
        m = vi
    else:
        raise ValueError("method must be 'reml' or 'ml'")
    mv = [_matmul(m, vj) for vj in vs]
    score = []
    for j, vj in enumerate(vs):
        tr = math.fsum(mv[j][i][i] for i in range(n))
        vpy = [math.fsum(vj[i][k] * py[k] for k in range(n)) for i in range(n)]
        score.append(-0.5 * tr + 0.5 * math.fsum(a_ * b_ for a_, b_ in zip(py, vpy)))
    info = [[0.5 * math.fsum(mv[j][i][k] * mv[l][k][i] for i in range(n) for k in range(n))
             for l in range(len(vs))] for j in range(len(vs))]
    return Pieces(loglik, score, info, b)


def _solve_small(a, b):
    k = len(a)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(k):
        piv = max(range(c, k), key=lambda r: abs(m[r][c]))
        m[c], m[piv] = m[piv], m[c]
        if m[c][c] == 0.0:
            raise ValueError("singular information matrix")
        for r in range(c + 1, k):
            f = m[r][c] / m[c][c]
            m[r] = [u - f * w for u, w in zip(m[r], m[c])]
    out = [0.0] * k
    for i in reversed(range(k)):
        out[i] = (m[i][k] - math.fsum(m[i][j] * out[j] for j in range(i + 1, k))) / m[i][i]
    return out


class VarianceFit(NamedTuple):
    theta: list        # the estimates of theta_1, ..., theta_m
    b: list            # the GLS estimate of b at theta
    loglik: float      # the maximized (restricted) log-likelihood
    iterations: int
    at_boundary: list  # True for each theta_j that ended at 0
    score: list        # the score at the end; <= 0 for the components at 0


def fit_variance_components(y, x, vs, method="reml", theta0=None, tol=1e-10, max_iter=200):
    """Fisher scoring with projection onto theta >= 0 and step halving."""
    m = len(vs)
    if theta0 is None:
        mean = math.fsum(y) / len(y)
        s2 = math.fsum((v - mean) ** 2 for v in y) / max(1, len(y) - 1)
        theta0 = [s2 / m] * m
    theta = [max(float(t), FLOOR) for t in theta0]  # @line L1
    cur = evaluate(y, x, vs, theta, method)  # @line L2
    for it in range(1, max_iter + 1):  # @line L3
        # Active set: a component at 0 whose step points below 0 stays at 0, and the rest is solved without it.
        free = list(range(m))  # @line L4
        while True:
            sub = _solve_small([[cur.info[i][j] for j in free] for i in free], [cur.score[i] for i in free]) if free else []  # @line L5
            step = [0.0] * m
            for i, s in zip(free, sub):
                step[i] = s
            stuck = [j for j in free if theta[j] == 0.0 and step[j] < 0.0]  # @line L6
            if not stuck:
                break
            free = [j for j in free if j not in stuck]  # @line L6
        lam = 1.0  # @line L7
        while True:
            new = [max(t + lam * s, 0.0) for t, s in zip(theta, step)]  # @line L8
            new[-1] = max(new[-1], FLOOR)  # @line L8
            try:
                nxt = evaluate(y, x, vs, new, method)  # @line L9
                if nxt.loglik >= cur.loglik - 1e-12 * abs(cur.loglik):  # @line L9
                    break
            except ValueError:
                pass
            lam /= 2.0  # @line L10
            if lam < 1e-8:  # @line L10
                new, nxt = theta, cur
                break
        change = max(abs(a - b) for a, b in zip(new, theta))
        theta, cur = new, nxt  # @line L11
        if change <= tol * (1.0 + max(abs(t) for t in theta)):  # @line L12
            break
    at_zero = [t == 0.0 for t in theta]
    return VarianceFit(theta, cur.b, cur.loglik, it, at_zero, cur.score)  # @line L13


def one_way_design(groups):
    """y, X = 1 and the matrices Z Z^T and I for a one-way random effects layout."""
    y, label = [], []
    for g, values in enumerate(groups):
        for v in values:
            y.append(float(v))
            label.append(g)
    n = len(y)
    zzt = [[1.0 if label[i] == label[k] else 0.0 for k in range(n)] for i in range(n)]
    eye = [[1.0 if i == k else 0.0 for k in range(n)] for i in range(n)]
    return y, [[1.0] for _ in range(n)], [zzt, eye]


def anova_one_way(groups):
    """The ANOVA (method of moments) estimates (sigma_u^2, sigma_e^2) for a balanced one-way layout."""
    a, m = len(groups), len(groups[0])
    if any(len(g) != m for g in groups):
        raise ValueError("the layout is not balanced")
    means = [math.fsum(g) / m for g in groups]
    grand = math.fsum(means) / a
    msb = m * math.fsum((mu - grand) ** 2 for mu in means) / (a - 1)
    msw = math.fsum((v - mu) ** 2 for g, mu in zip(groups, means) for v in g) / (a * (m - 1))
    return (msb - msw) / m, msw
