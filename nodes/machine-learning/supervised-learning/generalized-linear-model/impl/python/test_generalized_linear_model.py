# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-linear-model/. The authors are listed in prov/KTAMYG.jsonl.

import math
import random

from generalized_linear_model import FAMILIES, LINKS, irls, log_likelihood, score

EX_X = [[1.0, 0.0], [1.0, 1.0], [1.0, 2.0], [1.0, 3.0], [1.0, 4.0]]
EX_Y = [1.0, 1.0, 2.0, 4.0, 7.0]


def poisson(rng, lam):
    # Knuth's method; lam is small here.
    limit, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= limit:
            return k
        k += 1


def design(rng, n, d):
    return [[1.0] + [rng.uniform(-1, 1) for _ in range(d - 1)] for _ in range(n)]


def draw(rng, family):
    while True:
        n, d = rng.randrange(15, 31), rng.randrange(2, 4)
        X = design(rng, n, d)
        beta = [rng.uniform(-1, 1) for _ in range(d)]
        eta = [sum(a * b for a, b in zip(x, beta)) for x in X]
        if family == "poisson":
            y = [float(poisson(rng, math.exp(e))) for e in eta]
        elif family == "binomial":
            y = [1.0 if rng.random() < 1 / (1 + math.exp(-e)) else 0.0 for e in eta]
        elif family == "gamma":
            y = [rng.gammavariate(2.0, math.exp(e) / 2.0) for e in eta]
        else:
            y = [e + rng.gauss(0, 1) for e in eta]
        if family != "binomial":
            return X, y
        if d == 2:
            # With one feature the MLE exists exactly when the classes overlap both ways.
            x0 = [x[1] for x, t in zip(X, y) if t == 0]
            x1 = [x[1] for x, t in zip(X, y) if t == 1]
            if x0 and x1 and max(x0) > min(x1) and max(x1) > min(x0):
                return X, y


def matvec_t(X, r):
    return [sum(x[j] * ri for x, ri in zip(X, r)) for j in range(len(X[0]))]


def test_poisson_example() -> None:
    beta, it = irls(EX_X, EX_Y, "poisson")
    assert it < 15
    mu = [math.exp(b0 + b1 * x) for (_, x), (b0, b1) in zip(EX_X, [beta] * 5)]
    # Canonical link: the fitted means match the data in total and in the first moment.
    assert abs(sum(mu) - sum(EX_Y)) < 1e-9
    assert abs(sum(m * x[1] for m, x in zip(mu, EX_X)) - sum(y * x[1] for y, x in zip(EX_Y, EX_X))) < 1e-9
    assert abs(beta[0] + 0.334262) < 1e-6 and abs(beta[1] - 0.566096) < 1e-6


def test_score_equations_canonical() -> None:
    # For a canonical link the score is X^T (y - mu), computed here from scratch.
    rng = random.Random(71)
    for case in range(500):
        family = ("poisson", "binomial", "gaussian")[case % 3]
        X, y = draw(rng, family)
        beta, it = irls(X, y, family)
        assert it < 100
        inv = LINKS[FAMILIES[family].canonical].inverse
        mu = [inv(sum(a * b for a, b in zip(x, beta))) for x in X]
        s = matvec_t(X, [yi - m for yi, m in zip(y, mu)])
        assert max(abs(v) for v in s) < 1e-6 * (1 + sum(abs(t) for t in y))
        # The fit is a maximum: small moves do not raise the likelihood.
        ll = log_likelihood(X, y, beta, family, FAMILIES[family].canonical)
        for _ in range(2):
            b2 = [b + rng.uniform(-0.01, 0.01) for b in beta]
            assert log_likelihood(X, y, b2, family, FAMILIES[family].canonical) <= ll + 1e-12


def test_score_matches_finite_differences() -> None:
    rng = random.Random(72)
    h = 1e-6
    cases = [("poisson", "log"), ("binomial", "logit"), ("gamma", "log"), ("gaussian", "identity")]
    for case in range(500):
        family, link = cases[case % 4]
        X, y = draw(rng, family)
        beta = [rng.uniform(-0.5, 0.5) for _ in X[0]]
        s = score(X, y, beta, family, link)
        j = rng.randrange(len(beta))
        bp, bm = list(beta), list(beta)
        bp[j] += h
        bm[j] -= h
        fd = (log_likelihood(X, y, bp, family, link) - log_likelihood(X, y, bm, family, link)) / (2 * h)
        assert abs(fd - s[j]) < 1e-5 * (1 + abs(s[j]))


def test_noncanonical_gamma_log() -> None:
    # Fisher scoring still solves the score equations X^T [(y - mu) / mu] = 0.
    rng = random.Random(73)
    for _ in range(100):
        X, y = draw(rng, "gamma")
        beta, it = irls(X, y, "gamma", "log")
        assert it < 100
        mu = [math.exp(sum(a * b for a, b in zip(x, beta))) for x in X]
        s = matvec_t(X, [(yi - m) / m for yi, m in zip(y, mu)])
        assert max(abs(v) for v in s) < 1e-6 * len(y)


def hessian_fd(X, y, beta, family, link, h=1e-5):
    d = len(beta)
    H = [[0.0] * d for _ in range(d)]
    for j in range(d):
        bp, bm = list(beta), list(beta)
        bp[j] += h
        bm[j] -= h
        sp, sm = score(X, y, bp, family, link), score(X, y, bm, family, link)
        for k in range(d):
            H[k][j] = (sp[k] - sm[k]) / (2 * h)
    return H


def fisher(X, beta, family, link):
    fam, lk = FAMILIES[family], LINKS[link]
    d = len(beta)
    F = [[0.0] * d for _ in range(d)]
    for x in X:
        mu = lk.inverse(sum(a * b for a, b in zip(x, beta)))
        w = 1.0 / (fam.variance(mu) * lk.derivative(mu) ** 2)
        for a in range(d):
            for c in range(d):
                F[a][c] += w * x[a] * x[c]
    return F


def test_fisher_scoring_is_newton_for_canonical_link() -> None:
    rng = random.Random(74)
    worst_noncanonical = 0.0
    for case in range(200):
        family, link = [("poisson", "log"), ("binomial", "logit"), ("gamma", "log")][case % 3]
        X, y = draw(rng, family)
        beta = [rng.uniform(-0.5, 0.5) for _ in X[0]]
        H = hessian_fd(X, y, beta, family, link)
        F = fisher(X, beta, family, link)
        gap = max(abs(H[a][c] + F[a][c]) for a in range(len(beta)) for c in range(len(beta)))
        if family == "gamma":
            worst_noncanonical = max(worst_noncanonical, gap)
        else:
            assert gap < 1e-4 * (1 + max(abs(v) for r in F for v in r))
    # For a non-canonical link the observed and expected information differ.
    assert worst_noncanonical > 1.0
