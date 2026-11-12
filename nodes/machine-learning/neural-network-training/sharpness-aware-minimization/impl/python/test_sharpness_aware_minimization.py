# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sharpness-aware-minimization/. The authors are listed in prov/GSR20V.jsonl.

import math
import random
from fractions import Fraction as F

from sharpness_aware_minimization import p_norm, perturbation, sam, sam_gradient, sharpness

H = [[F(2), F(1)], [F(1), F(3)]]
B = [F(-1), F(2)]


def quad_grad(w):
    # L(w) = 1/2 w^T H w + b^T w, gradient H w + b.
    return [sum(h * x for h, x in zip(row, w)) + b for row, b in zip(H, B)]


def test_sam_gradient_on_a_quadratic_is_exact() -> None:
    # w = (2, 0) has gradient (3, 4), so ||g|| = 5 and everything is rational.
    w = [F(2), F(0)]
    g = quad_grad(w)
    assert g == [F(3), F(4)]
    rho = F(1, 20)
    hg = [sum(h * x for h, x in zip(row, g)) for row in H]
    expect = [gi + rho * hgi / 5 for gi, hgi in zip(g, hg)]
    assert sam_gradient(quad_grad, w, rho) == expect == [F(31, 10), F(83, 20)]
    assert perturbation(g, rho) == [F(3, 100), F(1, 25)]


def test_two_gradient_evaluations_per_step() -> None:
    calls = []

    def counting(w):
        calls.append(1)
        return quad_grad(w)

    sam(counting, [F(0), F(0)], 7, lr=F(1, 10), rho=F(1, 20))
    assert len(calls) == 14


def test_perturbation_has_norm_rho() -> None:
    rng = random.Random(1)
    for p in (2, 3, 1.5, math.inf):
        g = [rng.gauss(0, 1) for _ in range(6)]
        assert math.isclose(p_norm(perturbation(g, 0.3, p), p), 0.3, rel_tol=1e-12)


def test_perturbation_maximizes_the_linearization() -> None:
    rng = random.Random(2)
    for p in (2, 3, math.inf):
        q = 1 if p == math.inf else p / (p - 1)
        g = [rng.gauss(0, 1) for _ in range(5)]
        best = sum(a * b for a, b in zip(g, perturbation(g, 0.5, p)))
        assert math.isclose(best, 0.5 * p_norm(g, q), rel_tol=1e-12)
        for _ in range(500):
            e = [rng.gauss(0, 1) for _ in range(5)]
            n = p_norm(e, p)
            assert sum(a * 0.5 * b / n for a, b in zip(g, e)) <= best + 1e-12


def test_zero_gradient_is_a_fixed_point() -> None:
    # H w + b = 0 at w = (1, -1).
    w = [F(1), F(-1)]
    assert quad_grad(w) == [0, 0]
    assert perturbation(quad_grad(w), F(1, 10)) == [0, 0]
    assert sam(quad_grad, w, 3, lr=F(1, 10), rho=F(1, 10))[-1] == w


def test_first_order_maximizer_error_is_second_order() -> None:
    # L(w) = sum log(1 + exp(w_i)) + w_0 w_1^2: compare L(w + eps_hat) with the
    # true maximum of L over the circle of radius rho.
    def loss(w):
        return sum(math.log1p(math.exp(x)) for x in w) + w[0] * w[1] ** 2

    def grad(w):
        s = [1 / (1 + math.exp(-x)) for x in w]
        return [s[0] + w[1] ** 2, s[1] + 2 * w[0] * w[1]]

    w = [0.3, -0.7]
    dirs = [[math.cos(2 * math.pi * k / 20000), math.sin(2 * math.pi * k / 20000)] for k in range(20000)]
    errs = []
    for rho in (0.04, 0.02):
        eps = perturbation(grad(w), rho)
        errs.append(sharpness(loss, w, rho, dirs) + loss(w) - loss([a + e for a, e in zip(w, eps)]))
    assert errs[0] > 0 and 0 < errs[1] < 0.35 * errs[0]


def test_sharp_minimum_has_larger_sam_loss() -> None:
    # At the minimum of 1/2 h x^2 the SAM loss is 1/2 h rho^2.
    dirs = [[1.0], [-1.0]]
    for h in (1.0, 30.0):
        assert math.isclose(sharpness(lambda w: 0.5 * h * w[0] ** 2, [0.0], 0.05, dirs), 0.5 * h * 0.0025)


def test_sam_with_momentum_approaches_the_minimum() -> None:
    g = lambda w: [float(v) for v in quad_grad(w)]
    w = sam(g, [5.0, 5.0], 300, lr=0.05, rho=0.01, momentum=0.5)[-1]
    assert abs(w[0] - 1) < 0.02 and abs(w[1] + 1) < 0.02
