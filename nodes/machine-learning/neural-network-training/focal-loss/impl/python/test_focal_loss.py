# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/focal-loss/. The authors are listed in prov/05AH1D.jsonl.

import math
import random
from fractions import Fraction as F

from focal_loss import (best_prediction, expected_focal, focal_grad, focal_grad_softmax, focal_loss, focal_loss_softmax,
                        log_softmax, prior_bias, sigmoid)


def logit(p: float) -> float:
    return math.log(p / (1 - p))


def test_gamma_zero_is_cross_entropy() -> None:
    rng = random.Random(0)
    for _ in range(50):
        x, y = rng.gauss(0.0, 4.0), rng.choice((1, -1))
        ce = math.log1p(math.exp(-y * x))
        assert math.isclose(focal_loss(x, y, 0.0), ce, rel_tol=1e-12, abs_tol=1e-300)
        assert math.isclose(focal_loss(x, y, 0.0, alpha=0.25), (0.25 if y == 1 else 0.75) * ce, rel_tol=1e-12)
        assert math.isclose(focal_grad(x, y, 0.0), -y * (1 - sigmoid(y * x)), rel_tol=1e-12, abs_tol=1e-15)
        z = [rng.gauss(0.0, 2.0) for _ in range(4)]
        assert math.isclose(focal_loss_softmax(z, 2, 0.0), -log_softmax(z)[2], rel_tol=1e-12)


def test_modulating_factor_exactly() -> None:
    assert (1 - F(9, 10)) ** 2 == F(1, 100)
    assert (1 - F(968, 1000)) ** 2 == F(1024, 1000000)


def test_binary_gradient_matches_central_differences() -> None:
    rng = random.Random(1)
    h = 1e-6
    for _ in range(100):
        x, y = rng.uniform(-6.0, 6.0), rng.choice((1, -1))
        gamma, alpha = rng.choice((0.0, 0.5, 1.0, 2.0, 5.0)), rng.choice((None, 0.25))
        fd = (focal_loss(x + h, y, gamma, alpha) - focal_loss(x - h, y, gamma, alpha)) / (2 * h)
        assert abs(fd - focal_grad(x, y, gamma, alpha)) < 1e-7


def test_softmax_gradient_matches_central_differences() -> None:
    rng = random.Random(2)
    h = 1e-6
    for _ in range(40):
        k = rng.randint(2, 5)
        z = [rng.gauss(0.0, 2.0) for _ in range(k)]
        y, gamma = rng.randrange(k), rng.choice((0.0, 1.0, 2.0, 3.5))
        g = focal_grad_softmax(z, y, gamma)
        for j in range(k):
            zp, zm = z[:], z[:]
            zp[j] += h
            zm[j] -= h
            assert abs((focal_loss_softmax(zp, y, gamma) - focal_loss_softmax(zm, y, gamma)) / (2 * h) - g[j]) < 1e-7


def test_two_class_softmax_matches_the_binary_form() -> None:
    for x in (-3.0, -0.2, 0.0, 1.7, 4.0):
        for gamma in (0.0, 2.0):
            assert math.isclose(focal_loss_softmax([x, 0.0], 0, gamma), focal_loss(x, 1, gamma), rel_tol=1e-12)
            assert math.isclose(focal_loss_softmax([x, 0.0], 1, gamma), focal_loss(x, -1, gamma), rel_tol=1e-12)


def test_easy_negatives_stop_dominating() -> None:
    easy, hard = logit(0.99), logit(0.1)
    ce_neg, ce_pos = 10000 * focal_loss(-easy, -1, 0.0), focal_loss(hard, 1, 0.0)
    fl_neg, fl_pos = 10000 * focal_loss(-easy, -1, 2.0), focal_loss(hard, 1, 2.0)
    assert ce_neg > 40 * ce_pos
    assert fl_pos > 100 * fl_neg
    assert math.isclose(fl_pos, 0.81 * ce_pos, rel_tol=1e-12)


def test_large_logits_are_stable() -> None:
    assert focal_loss(800.0, 1, 2.0) == 0.0
    assert math.isclose(focal_loss(-800.0, 1, 2.0), 800.0)
    assert math.isclose(focal_grad(-800.0, 1, 2.0), -1.0)


def test_focal_loss_is_not_proper() -> None:
    for q in (0.6, 0.75, 0.9):
        assert abs(best_prediction(q, 0.0) - q) < 1e-6
        p = best_prediction(q, 2.0)
        assert 0.5 < p < q
        grid = min((expected_focal(i / 10000, q, 2.0), i / 10000) for i in range(1, 10000))
        assert abs(grid[1] - p) < 2e-4
    assert abs(best_prediction(0.9, 2.0) - 0.6942) < 1e-4


def test_prior_initialization() -> None:
    assert math.isclose(sigmoid(prior_bias(0.01)), 0.01, rel_tol=1e-12)
