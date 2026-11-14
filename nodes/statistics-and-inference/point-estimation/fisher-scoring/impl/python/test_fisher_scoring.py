# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fisher-scoring/. The authors are listed in prov/Y142G8.jsonl.

import math
import random
from fractions import Fraction
from statistics import NormalDist

from fisher_scoring import LINKS, FAMILIES, fisher_scoring, glm_fisher_scoring, inverse, solve

ND = NormalDist()


# Reference: Newton-Raphson with the observed information, derived by hand.
# For a GLM, -d2 l / d beta d beta' = sum x x' [mu'^2 / V - (y - mu) c'(eta)], c = mu' / V.

def c_prime(link: str, eta: float) -> float:
    if link in ("logit", "log"):
        return 0.0  # canonical links: c = 1
    if link == "probit":
        p = 0.5 * math.erfc(-eta / math.sqrt(2.0))
        f = math.exp(-0.5 * eta * eta) / math.sqrt(2.0 * math.pi)
        v = p * (1.0 - p)
        return (-eta * f * v - f * f * (1.0 - 2.0 * p)) / (v * v)
    if link == "identity":
        return -1.0 / (eta * eta)  # Poisson with identity link: c = 1 / eta
    raise ValueError(link)


def newton_glm(x, y, family, link, beta0, tol=1e-10, max_iter=100):
    mean_fn, dmean = LINKS[link]
    var_fn, _ = FAMILIES[family]
    p = len(x[0])
    b = list(beta0)
    path = [list(b)]
    for _ in range(max_iter):
        g = [0.0] * p
        j = [[0.0] * p for _ in range(p)]
        for xi, yi in zip(x, y):
            e = sum(xi[k] * b[k] for k in range(p))
            m, d = mean_fn(e), dmean(e)
            v = var_fn(m)
            w = (yi - m) * d / v
            h = d * d / v - (yi - m) * c_prime(link, e)
            for r in range(p):
                g[r] += xi[r] * w
                for s in range(p):
                    j[r][s] += xi[r] * xi[s] * h
        delta = solve(j, g)
        if sum(a * c for a, c in zip(g, delta)) <= tol:
            return b, path
        b = [bi + di for bi, di in zip(b, delta)]
        path.append(list(b))
    return b, path


def make_data(seed, n, beta, family, link):
    rng = random.Random(seed)
    mean_fn, _ = LINKS[link]
    x, y = [], []
    for _ in range(n):
        xi = [1.0, rng.gauss(0, 1), rng.gauss(0, 1)]
        m = mean_fn(sum(a * c for a, c in zip(xi, beta)))
        if family == "binomial":
            yi = 1.0 if rng.random() < m else 0.0
        else:
            # Poisson by inversion of the distribution function
            u, k, pk = rng.random(), 0, math.exp(-m)
            cum = pk
            while u > cum:
                k += 1
                pk *= m / k
                cum += pk
            yi = float(k)
        x.append(xi)
        y.append(yi)
    return x, y


def test_solve_and_inverse_exact():
    a = [[Fraction(4), Fraction(1), Fraction(2)], [Fraction(1), Fraction(3), Fraction(0)], [Fraction(2), Fraction(0), Fraction(5)]]
    inv = inverse(a)
    for i in range(3):
        for j in range(3):
            assert sum(a[i][k] * inv[k][j] for k in range(3)) == (1 if i == j else 0)


def test_poisson_mean_one_step_exact():
    # l(mu) = sum y log mu - n mu, U = sum y / mu - n, I = n / mu. One step lands on y-bar.
    ys = [3, 0, 4, 1, 1, 5, 2]
    n, s = len(ys), sum(ys)
    for mu0 in (Fraction(1, 3), Fraction(1), Fraction(10)):
        res = fisher_scoring(lambda t: [s / t[0] - n], lambda t: [[n / t[0]]], [mu0], tol=0)
        assert res.path[1] == [Fraction(s, n)]
        assert res.converged and res.iterations == 1
        assert res.cov == [[Fraction(s, n) / n]]  # inverse information: y-bar / n


def test_normal_linear_model_one_step_equals_least_squares_exact():
    x = [[Fraction(1), Fraction(v)] for v in (0, 1, 2, 3, 5)]
    y = [Fraction(v) for v in (1, 2, 2, 5, 7)]
    xtx = [[sum(r[i] * r[j] for r in x) for j in range(2)] for i in range(2)]
    xty = [sum(r[i] * yi for r, yi in zip(x, y)) for i in range(2)]
    ols = solve(xtx, xty)

    def score(b):
        res = [yi - r[0] * b[0] - r[1] * b[1] for r, yi in zip(x, y)]
        return [sum(r[i] * e for r, e in zip(x, res)) for i in range(2)]

    out = fisher_scoring(score, lambda b: xtx, [Fraction(-4), Fraction(9)], tol=0)
    assert out.path[1] == ols and out.theta == ols and out.iterations == 1


def test_canonical_links_scoring_equals_newton_step_by_step():
    cases = [
        ("binomial", "logit", [-0.5, 1.0, -0.7], 11),
        ("poisson", "log", [0.3, 0.5, -0.4], 12),
    ]
    for family, link, beta, seed in cases:
        x, y = make_data(seed, 200, beta, family, link)
        fit = glm_fisher_scoring(x, y, family, link, halving=False)
        _, npath = newton_glm(x, y, family, link, [0.0, 0.0, 0.0])
        assert fit.converged
        # with step halving the path may differ, but the limit is the same
        safe = glm_fisher_scoring(x, y, family, link)
        assert max(abs(u - v) for u, v in zip(safe.beta, fit.beta)) < 1e-8
        assert len(fit.path) == len(npath)
        for a, b in zip(fit.path, npath):
            assert max(abs(u - v) for u, v in zip(a, b)) < 1e-12


def test_non_canonical_links_same_mle_different_path():
    cases = [
        ("binomial", "probit", [-0.3, 0.8, -0.5], 21, [0.0, 0.0, 0.0]),
        ("poisson", "identity", [3.0, 0.6, -0.5], 22, [3.0, 0.0, 0.0]),
    ]
    for family, link, beta, seed, start in cases:
        x, y = make_data(seed, 300, beta, family, link)
        fit = glm_fisher_scoring(x, y, family, link, beta0=start, tol=1e-20)
        nb, npath = newton_glm(x, y, family, link, start, tol=1e-20)
        assert fit.converged
        assert max(abs(u - v) for u, v in zip(fit.beta, nb)) < 1e-8
        # the plain iterates differ (for probit not at step 1: at eta = 0 the
        # observed and expected information agree, so the first steps coincide)
        plain = glm_fisher_scoring(x, y, family, link, beta0=start, halving=False)
        assert max(abs(u - v) for u, v in zip(plain.path[2], npath[2])) > 1e-6


def test_two_group_closed_forms():
    rng = random.Random(5)
    g = [0] * 40 + [1] * 60
    # Poisson log link: beta0 = log ybar0, beta1 = log(ybar1 / ybar0)
    y = []
    for gi in g:
        m = 2.0 if gi == 0 else 3.5
        u, k, pk = rng.random(), 0, math.exp(-m)
        cum = pk
        while u > cum:
            k += 1
            pk *= m / k
            cum += pk
        y.append(float(k))
    x = [[1.0, float(gi)] for gi in g]
    s0, s1 = sum(y[:40]), sum(y[40:])
    fit = glm_fisher_scoring(x, y, "poisson", "log", tol=1e-20)
    assert abs(fit.beta[0] - math.log(s0 / 40)) < 1e-10
    assert abs(fit.beta[1] - math.log((s1 / 60) / (s0 / 40))) < 1e-10
    assert abs(fit.cov[1][1] - (1 / s0 + 1 / s1)) < 1e-10
    # Probit: beta0 = Phi^-1(p0), beta1 = Phi^-1(p1) - Phi^-1(p0)
    yb = [1.0 if rng.random() < (0.3 if gi == 0 else 0.6) else 0.0 for gi in g]
    p0, p1 = sum(yb[:40]) / 40, sum(yb[40:]) / 60
    fit = glm_fisher_scoring(x, yb, "binomial", "probit", tol=1e-20)
    assert abs(fit.beta[0] - ND.inv_cdf(p0)) < 1e-8
    assert abs(fit.beta[1] - (ND.inv_cdf(p1) - ND.inv_cdf(p0))) < 1e-8


def test_cauchy_location_against_grid_search():
    rng = random.Random(7)
    xs = [2.0 + math.tan(math.pi * (rng.random() - 0.5)) for _ in range(25)]
    n = len(xs)

    def ll(t):
        return -sum(math.log1p((v - t[0]) ** 2) for v in xs)

    def score(t):
        return [sum(2 * (v - t[0]) / (1 + (v - t[0]) ** 2) for v in xs)]

    start = sorted(xs)[n // 2]
    res = fisher_scoring(score, lambda t: [[n / 2]], [start], ll, tol=1e-14)
    assert res.converged
    assert all(b >= a for a, b in zip(res.logliks, res.logliks[1:]))
    lo, hi = min(xs), max(xs)
    best = max((ll([lo + (hi - lo) * i / 20000]), lo + (hi - lo) * i / 20000) for i in range(20001))
    w = 2 * (hi - lo) / 20000
    best = max((ll([best[1] - w + 2 * w * i / 20000]), best[1] - w + 2 * w * i / 20000) for i in range(20001))
    assert abs(res.theta[0] - best[1]) < 1e-5
    assert ll(res.theta) >= best[0] - 1e-12


def test_step_halving_keeps_loglik_from_falling():
    x, y = make_data(31, 150, [-0.3, 0.8, -0.5], "binomial", "probit")
    fit = glm_fisher_scoring(x, y, "binomial", "probit", beta0=[4.0, -4.0, 4.0], tol=1e-20)
    ref = glm_fisher_scoring(x, y, "binomial", "probit", tol=1e-20)
    assert fit.converged
    assert max(abs(u - v) for u, v in zip(fit.beta, ref.beta)) < 1e-7
    # recompute the log-likelihood along the path; it never falls
    _, ll_one = FAMILIES["binomial"]
    lls = [sum(ll_one(yi, sum(a * c for a, c in zip(xi, b)), "probit") for xi, yi in zip(x, y)) for b in fit.path]
    assert all(b >= a for a, b in zip(lls, lls[1:]))


def test_complete_separation_is_flagged():
    x = [[1.0, float(t)] for t in (-3, -2, -1, 1, 2, 3)]
    y = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]
    fit = glm_fisher_scoring(x, y, "binomial", "logit", max_iter=200)
    assert fit.separated
    assert fit.beta[1] > 5
    ok = glm_fisher_scoring(x, [0.0, 1.0, 0.0, 1.0, 0.0, 1.0], "binomial", "logit")
    assert ok.converged and not ok.separated


def test_wald_interval_coverage_measured():
    # Measured, not proved: coverage of beta1 +- 1.96 se for logistic data, n = 200.
    beta = [-0.5, 1.0, -0.7]
    z = ND.inv_cdf(0.975)
    hits, r = 0, 300
    for rep in range(r):
        x, y = make_data(1000 + rep, 200, beta, "binomial", "logit")
        fit = glm_fisher_scoring(x, y, "binomial", "logit")
        se = math.sqrt(fit.cov[1][1])
        hits += abs(fit.beta[1] - beta[1]) <= z * se
    cover = hits / r
    assert abs(cover - 0.95) < 3 * math.sqrt(0.95 * 0.05 / r)
