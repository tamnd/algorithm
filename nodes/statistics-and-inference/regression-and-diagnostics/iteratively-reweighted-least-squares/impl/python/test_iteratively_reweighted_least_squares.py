# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iteratively-reweighted-least-squares/. The authors are listed in prov/N4YG7R.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from iteratively_reweighted_least_squares import (
    L1, Biweight, Huber, Logistic, Poisson, Probit, irls, separation_suspected, weighted_ls,
)

EX_X = [[1.0, float(t)] for t in [1, 2, 3, 4, 5, 6]]
EX_Y = [0, 0, 1, 0, 1, 1]


def solve(a, b):
    """Gauss-Jordan elimination; exact when the entries are Fractions."""
    k = len(a)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(k):
        piv = max(range(c, k), key=lambda r: abs(m[r][c]))
        m[c], m[piv] = m[piv], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [u - f * v for u, v in zip(m[r], m[c])]
    return [m[i][k] / m[i][i] for i in range(k)]


def newton_step_logistic(x, y, b, mean):
    """b + (X^T W X)^(-1) X^T (y - mu), W = diag(mu (1 - mu)): Newton on the log-likelihood."""
    p = len(b)
    mu = [mean(sum(a * c for a, c in zip(xi, b))) for xi in x]
    h = [[sum(m * (1 - m) * xi[i] * xi[j] for xi, m in zip(x, mu)) for j in range(p)] for i in range(p)]
    g = [sum((yi - m) * xi[i] for xi, yi, m in zip(x, y, mu)) for i in range(p)]
    d = solve(h, g)
    return [bi + di for bi, di in zip(b, d)]


def test_first_logistic_step_is_the_newton_step_exact():
    """At b = 0 every mu is 1/2, so the working weights 1/4 and responses 4y - 2 are exact floats."""
    rng = random.Random(1)
    for _ in range(10):
        n, p = rng.randint(5, 9), rng.randint(1, 3)
        x = [[1] + [rng.randint(-3, 3) for _ in range(p - 1)] for _ in range(n)]
        y = [rng.randint(0, 1) for _ in range(n)]
        w, z = Logistic().working(y, [0.0] * n)
        assert w == [0.25] * n and z == [4.0 * v - 2.0 for v in y]
        xf = [[Fraction(v) for v in r] for r in x]
        g = [[sum(Fraction(wi) * r[i] * r[j] for r, wi in zip(xf, w)) for j in range(p)] for i in range(p)]
        if any(c == 0 for c in [g[i][i] for i in range(p)]):
            continue
        try:
            irls_step = solve(g, [sum(Fraction(wi) * r[i] * Fraction(zi) for r, wi, zi in zip(xf, w, z)) for i in range(p)])
        except ZeroDivisionError:
            continue  # singular design
        newton = newton_step_logistic(xf, y, [Fraction(0)] * p, lambda e: Fraction(1, 2))
        assert irls_step == newton
    b1 = weighted_ls(EX_X, *reversed(Logistic().working(EX_Y, [0.0] * 6)))
    assert b1 == pytest.approx([-2.8, 0.8], abs=1e-12)
    assert newton_step_logistic([[Fraction(int(v)) for v in r] for r in EX_X], EX_Y, [Fraction(0)] * 2,
                                lambda e: Fraction(1, 2)) == [Fraction(-14, 5), Fraction(4, 5)]


def test_logistic_step_is_the_newton_step_anywhere():
    rng = random.Random(2)
    m = Logistic()
    for _ in range(20):
        n = rng.randint(6, 12)
        x = [[1.0, rng.uniform(-2, 2), rng.uniform(-2, 2)] for _ in range(n)]
        y = [rng.randint(0, 1) for _ in range(n)]
        b = [rng.uniform(-1, 1) for _ in range(3)]
        eta = [sum(a * c for a, c in zip(xi, b)) for xi in x]
        w, z = m.working(y, eta)
        step = weighted_ls(x, z, w)
        assert step == pytest.approx(newton_step_logistic(x, y, b, m.mean), rel=1e-9, abs=1e-9)


def test_page_example_converges_to_the_mle():
    fit = irls(EX_X, EX_Y, Logistic())
    assert fit.converged and fit.iterations <= 8
    assert fit.b == pytest.approx([-4.2490966, 1.2140276], abs=1e-6)
    mu = [Logistic().mean(r[0] * fit.b[0] + r[1] * fit.b[1]) for r in EX_X]
    for j in range(2):  # the score X^T (y - mu) is zero at the MLE
        assert abs(sum((yi - mi) * r[j] for r, yi, mi in zip(EX_X, EX_Y, mu))) < 1e-10
    assert fit.objective[-1] == pytest.approx(4.955973670099, abs=1e-9)
    assert not separation_suspected(EX_X, EX_Y, fit.b)


def test_poisson_and_probit_solve_their_score_equations():
    y = [2, 0, 3, 1, 4, 2, 7]
    fit = irls([[1.0]] * 7, y, Poisson())
    assert math.exp(fit.b[0]) == pytest.approx(sum(y) / 7, rel=1e-12)
    rng = random.Random(3)
    x = [[1.0, rng.uniform(0, 2)] for _ in range(40)]
    yc = [sum(1 for _ in range(10) if rng.random() < 1 - math.exp(-math.exp(0.2 + 0.7 * r[1]) / 10)) for r in x]
    fit = irls(x, yc, Poisson())
    mu = [math.exp(r[0] * fit.b[0] + r[1] * fit.b[1]) for r in x]
    for j in range(2):
        assert abs(sum((a - m) * r[j] for r, a, m in zip(x, yc, mu))) < 1e-8
    yb = [1 if rng.random() < 0.5 + 0.2 * (r[1] - 1) else 0 for r in x]
    fit = irls(x, yb, Probit())
    assert fit.converged
    pr = Probit()
    for j in range(2):
        s = 0.0
        for r, a in zip(x, yb):
            e = r[0] * fit.b[0] + r[1] * fit.b[1]
            mu = pr.mean(e)
            s += (a - mu) * math.exp(-e * e / 2) / math.sqrt(2 * math.pi) / (mu * (1 - mu)) * r[j]
        assert abs(s) < 1e-8


def test_m_estimation_never_increases_the_loss():
    """Majorize-minimize: for rho(r) = f(r^2) with f concave the loss is nonincreasing."""
    rng = random.Random(4)
    for _ in range(15):
        n = 25
        x = [[1.0, rng.uniform(0, 10)] for _ in range(n)]
        y = [1.0 + 0.5 * r[1] + rng.gauss(0, 1) + (rng.choice([0, 0, 0, 15]) if rng.random() < 0.3 else 0) for r in x]
        for rule in [Huber(1.345, 1.0), Biweight(4.685, 1.0), L1(1e-4)]:
            b0 = weighted_ls(x, y, [1.0] * n)
            start = rule.objective(y, [r[0] * b0[0] + r[1] * b0[1] for r in x])
            fit = irls(x, y, rule, b0=b0, maxit=60)
            seq = [start] + fit.objective
            for a, b in zip(seq, seq[1:]):
                assert b <= a * (1 + 1e-12) + 1e-12


def test_l1_is_within_n_delta_over_2_of_least_absolute_deviations():
    """A least absolute deviations line passes through two data points, so the minimum is found by trying all pairs."""
    rng = random.Random(5)
    for _ in range(8):
        n, delta = 12, 1e-3
        xs = [rng.uniform(0, 10) for _ in range(n)]
        y = [2.0 - 0.3 * v + rng.expovariate(1.0) * rng.choice([-1, 1]) for v in xs]
        x = [[1.0, v] for v in xs]
        best = math.inf
        for i, j in itertools.combinations(range(n), 2):
            s = (y[j] - y[i]) / (xs[j] - xs[i])
            a = y[i] - s * xs[i]
            best = min(best, sum(abs(yi - a - s * v) for yi, v in zip(y, xs)))
        fit = irls(x, y, L1(delta), maxit=500, tol=1e-13)
        loss = sum(abs(yi - fit.b[0] - fit.b[1] * v) for yi, v in zip(y, xs))
        assert best - 1e-9 <= loss <= best + n * delta / 2 + 1e-9


def test_huber_with_huge_threshold_is_least_squares():
    x = [[1.0, float(t)] for t in range(8)]
    y = [0.3, 1.1, 1.9, 3.2, 3.8, 5.1, 6.0, 30.0]
    fit = irls(x, y, Huber(c=1e9))
    assert fit.converged and fit.iterations == 2
    assert fit.b == pytest.approx(weighted_ls(x, y, [1.0] * 8), abs=1e-12)


def test_robust_rules_resist_an_outlier():
    x = [[1.0, float(t)] for t in range(1, 11)]
    y = [1.1, 2.0, 2.9, 4.2, 5.0, 5.9, 7.1, 8.0, 30.0, 10.1]
    assert weighted_ls(x, y, [1.0] * 10)[1] > 1.8
    for rule in [Huber(1.345, 0.5), Biweight(4.685, 0.5), L1(1e-6)]:
        fit = irls(x, y, rule, maxit=200)
        assert fit.converged and abs(fit.b[1] - 1.0) < 0.05


def test_separation_is_flagged():
    y = [0, 0, 0, 1, 1, 1]
    fit = irls(EX_X, y, Logistic(), maxit=50)
    assert not fit.converged
    assert separation_suspected(EX_X, y, fit.b)
    assert fit.objective[-1] < 1e-10  # the deviance goes to 0, its infimum, which no finite b attains


def test_bad_inputs():
    with pytest.raises(ValueError):
        L1(0.0)
    with pytest.raises(ValueError):
        irls([[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [0, 1, 0], Logistic())
    with pytest.raises(ValueError):
        irls([], [], Logistic())
