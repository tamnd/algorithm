# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/golub-welsch-algorithm/. The authors are listed in prov/H4E8X2.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from golub_welsch_algorithm import golub_welsch, hermite_recurrence, laguerre_recurrence, legendre_recurrence

U = 2.0 ** -53


def oracle_rule(alpha, beta, n):
    """Independent oracle: Sturm-count bisection for the nodes, Christoffel numbers for the weights."""
    def count(x):
        c, d = 0, 1.0
        for k in range(n):
            d = (alpha[k] - x) - (beta[k] / d if k else 0.0)
            if d == 0.0:
                d = -1e-300
            c += d < 0.0
        return c
    rad = max(abs(alpha[k]) + 2 * math.sqrt(max(beta[1:n] or [0.0])) for k in range(n)) + 1.0
    nodes, weights = [], []
    for j in range(n):
        lo, hi = -rad, rad
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if mid <= lo or mid >= hi:
                break
            if count(mid) >= j + 1:
                hi = mid
            else:
                lo = mid
        x = 0.5 * (lo + hi)
        p_prev, p = 0.0, 1.0 / math.sqrt(beta[0])
        s = [p * p]
        for k in range(n - 1):
            p_prev, p = p, ((x - alpha[k]) * p - (math.sqrt(beta[k]) * p_prev if k else 0.0)) / math.sqrt(beta[k + 1])
            s.append(p * p)
        nodes.append(x)
        weights.append(1.0 / math.fsum(s))
    return nodes, weights


def test_worked_example_three_points():
    x, w = golub_welsch(*legendre_recurrence(3), 3)
    r = math.sqrt(0.6)
    assert x == pytest.approx([-r, 0.0, r], abs=1e-15)
    assert w == pytest.approx([5 / 9, 8 / 9, 5 / 9], abs=1e-15)


@pytest.mark.parametrize("n", [1, 2, 3, 6, 10, 17, 25])
def test_exact_to_degree_2n_minus_1_and_not_2n(n):
    x, w = golub_welsch(*legendre_recurrence(n), n)
    for k in range(2 * n):
        q = math.fsum(wi * xi ** k for xi, wi in zip(x, w))
        assert abs(q - (2 / (k + 1) if k % 2 == 0 else 0.0)) <= 50 * n * U
    q = math.fsum(wi * xi ** (2 * n) for xi, wi in zip(x, w))
    norm2 = F(2 ** (2 * n + 1) * math.factorial(n) ** 4, (2 * n + 1) * math.factorial(2 * n) ** 2)
    assert (2 / (2 * n + 1) - q) == pytest.approx(float(norm2), rel=1e-8, abs=1e-14)


def test_random_polynomials_rational_oracle():
    rng = random.Random(1969)
    rules = {n: golub_welsch(*legendre_recurrence(n), n) for n in range(1, 13)}
    for _ in range(600):
        n = rng.randint(1, 12)
        c = [F(rng.randint(-30, 30), rng.randint(1, 7)) for _ in range(rng.randint(1, 2 * n))]
        exact = sum(ck * F(2, k + 1) for k, ck in enumerate(c) if k % 2 == 0)
        x, w = rules[n]
        terms = [wi * sum(float(ck) * xi ** k for k, ck in enumerate(c)) for xi, wi in zip(x, w)]
        size = math.fsum(abs(t) for t in terms) + abs(float(exact))
        assert abs(math.fsum(terms) - float(exact)) <= 1e-13 * size + 1e-300


def test_random_jacobi_matrices_against_bisection_oracle():
    rng = random.Random(42)
    for _ in range(300):
        n = rng.randint(1, 15)
        alpha = [rng.uniform(-3, 3) for _ in range(n)]
        beta = [rng.uniform(0.5, 4)] + [rng.uniform(1e-3, 3) for _ in range(n - 1)]
        x, w = golub_welsch(alpha, beta, n)
        xo, wo = oracle_rule(alpha, beta, n)
        scale = max(abs(a) for a in alpha) + 2 * math.sqrt(max(beta))
        for a, b in zip(x, xo):
            assert abs(a - b) <= 1e-12 * scale
        for a, b in zip(w, wo):
            assert abs(a - b) <= 1e-11 * beta[0]
        assert math.fsum(w) == pytest.approx(beta[0], rel=1e-13)
        assert all(wi >= 0.0 for wi in w)


@pytest.mark.parametrize("rec,mu0", [(legendre_recurrence, 2.0), (laguerre_recurrence, 1.0),
                                      (hermite_recurrence, math.sqrt(math.pi))])
def test_classical_weights_match_oracle(rec, mu0):
    for n in [5, 20, 60]:
        x, w = golub_welsch(*rec(n), n)
        xo, wo = oracle_rule(*rec(n), n)
        assert x == pytest.approx(xo, rel=1e-12, abs=1e-13)
        assert max(abs(a - b) / b for a, b in zip(w, wo) if b > 0) < 1e-11
        assert math.fsum(w) == pytest.approx(mu0, rel=1e-13)


def test_closed_forms():
    x, w = golub_welsch(*legendre_recurrence(20), 20)
    q = lambda f, a, b: 0.5 * (b - a) * math.fsum(wi * f(0.5 * (a + b) + 0.5 * (b - a) * xi) for xi, wi in zip(x, w))
    assert q(math.exp, 0, 1) == pytest.approx(math.e - 1, abs=1e-15)
    assert q(math.sin, 0, math.pi) == pytest.approx(2.0, abs=1e-14)
    assert q(lambda t: 1 / (1 + t * t), -1, 1) == pytest.approx(math.pi / 2, abs=1e-12)
    assert q(lambda t: math.exp(math.cos(t)), 0, 2 * math.pi) == pytest.approx(2 * math.pi * 1.2660658777520082, abs=1e-12)
    assert q(lambda t: math.cos(10 * t), -1, 1) == pytest.approx(math.sin(10) / 5, abs=1e-12)
    # sqrt has an endpoint singularity in its derivative: slow algebraic convergence
    assert 1e-6 < abs(q(math.sqrt, 0, 1) - 2 / 3) < 1e-4
    xl, wl = golub_welsch(*laguerre_recurrence(30), 30)
    assert math.fsum(wi * math.sin(xi) for xi, wi in zip(xl, wl)) == pytest.approx(0.5, abs=1e-14)
    xh, wh = golub_welsch(*hermite_recurrence(20), 20)
    assert math.fsum(wi * math.cos(xi) for xi, wi in zip(xh, wh)) == pytest.approx(math.sqrt(math.pi) * math.exp(-0.25), abs=1e-14)
    # x^(-1/2) singularity carried by the weight x^(-1/2) e^(-x)
    xs, ws = golub_welsch(*laguerre_recurrence(30, -0.5), 30)
    ex = math.sqrt(math.pi) * math.cos(math.pi / 8) / 2 ** 0.25
    assert math.fsum(wi * math.cos(xi) for xi, wi in zip(xs, ws)) == pytest.approx(ex, abs=1e-13)


def test_tiny_weights_keep_relative_accuracy_in_this_range():
    x, w = golub_welsch(*hermite_recurrence(60), 60)
    xo, wo = oracle_rule(*hermite_recurrence(60), 60)
    assert min(wo) < 1e-40
    assert abs(w[0] - wo[0]) / wo[0] < 1e-10


def test_edge_cases():
    x, w = golub_welsch([0.25], [3.0], 1)
    assert x == [0.25] and w == [3.0]
    with pytest.raises(ValueError):
        golub_welsch([], [], 0)
    with pytest.raises(ValueError):
        golub_welsch([0.0, 0.0], [2.0, 0.0], 2)
    with pytest.raises(ValueError):
        golub_welsch([0.0], [2.0], 2)
    # nearly decoupled matrix: tiny off-diagonal entries deflate at once
    x, w = golub_welsch([1.0, 2.0, 3.0], [1.0, 1e-40, 1e-40], 3)
    assert x == pytest.approx([1.0, 2.0, 3.0], abs=1e-15)
    assert w[0] == pytest.approx(1.0, rel=1e-15)


def test_large_n():
    n = 200
    x, w = golub_welsch(*legendre_recurrence(n), n)
    assert math.fsum(w) == pytest.approx(2.0, rel=1e-13)
    assert all(x[i] < x[i + 1] for i in range(n - 1))
    assert math.fsum(wi * math.exp(xi) for xi, wi in zip(x, w)) == pytest.approx(math.e - 1 / math.e, rel=1e-13)
