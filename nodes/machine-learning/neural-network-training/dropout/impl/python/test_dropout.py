# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dropout/. The authors are listed in prov/8V15DT.jsonl.

import random
from fractions import Fraction as F

from dropout import (all_masks, dropout_backward, dropout_forward, dropout_penalty, dropout_regression_solution,
                     exact_moments, expected_dropout_loss, train_linear_with_dropout)

XS = [[1, 0], [0, 1], [1, 1], [2, 1], [1, 3]]
YS = [1, 2, 2, 4, 5]


def test_mask_probabilities_sum_to_one() -> None:
    assert sum(prob for _, prob in all_masks(4, F(2, 3))) == 1


def test_inverted_dropout_is_unbiased_with_the_stated_variance() -> None:
    x = [F(3), F(-1, 2), F(0), F(7, 3)]
    for p in [F(1, 2), F(4, 5), F(9, 10), F(1)]:
        mean, var = exact_moments(x, p)
        assert mean == x
        assert var == [(1 - p) / p * xi * xi for xi in x]


def test_eval_mode_is_the_identity_and_train_mode_scales_kept_units() -> None:
    rng = random.Random(0)
    x = [0.5, -1.0, 2.0, 3.0, 4.0]
    assert dropout_forward(x, 0.8, rng, train=False)[0] == x
    out, mask = dropout_forward(x, 0.8, rng)
    assert all(o == (xi / 0.8 if m else 0.0) for o, xi, m in zip(out, x, mask))


def test_backward_uses_the_same_mask() -> None:
    rng = random.Random(1)
    x = [rng.gauss(0.0, 1.0) for _ in range(6)]
    c = [rng.gauss(0.0, 1.0) for _ in range(6)]
    out, mask = dropout_forward(x, 0.5, rng)
    grad = dropout_backward(c, mask, 0.5)
    h = 1e-6
    for i in range(6):
        xp = x[:]
        xp[i] += h
        outp = [m * v / 0.5 for m, v in zip(mask, xp)]
        fd = (sum(a * b for a, b in zip(c, outp)) - sum(a * b for a, b in zip(c, out))) / h
        assert abs(fd - grad[i]) < 1e-6


def test_hand_example() -> None:
    assert expected_dropout_loss([1, 1], [1, 2], 4, F(1, 2)) == 6


def test_expected_loss_is_squared_error_plus_adaptive_penalty() -> None:
    rng = random.Random(2)
    for _ in range(30):
        d = rng.randint(1, 5)
        x = [F(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(d)]
        w = [F(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(d)]
        y = F(rng.randint(-9, 9), rng.randint(1, 3))
        p = F(rng.randint(1, 9), 10)
        plain = (y - sum(a * b for a, b in zip(w, x))) ** 2
        assert expected_dropout_loss(w, x, y, p) == plain + dropout_penalty(w, x, p)


def test_closed_form_solution_and_its_stationarity() -> None:
    p = F(1, 2)
    w = dropout_regression_solution(XS, YS, p)
    assert w == [F(41, 50), F(113, 150)]
    assert dropout_regression_solution(XS, YS, F(1)) == [F(9, 8), F(65, 48)]
    total = lambda v: sum(expected_dropout_loss(v, x, y, p) for x, y in zip(XS, YS))
    eps = F(1, 10 ** 6)
    for j in range(2):
        up = w[:]
        up[j] += eps
        dn = w[:]
        dn[j] -= eps
        assert total(up) == total(dn)


def test_penalty_is_invariant_to_rescaling_a_feature() -> None:
    p = F(1, 2)
    scaled = [[x[0], 5 * x[1]] for x in XS]
    w = dropout_regression_solution(XS, YS, p)
    ws = dropout_regression_solution(scaled, YS, p)
    assert ws == [w[0], w[1] / 5]


def test_sgd_with_dropout_approaches_the_closed_form() -> None:
    w = train_linear_with_dropout(XS, YS, 0.5, 0.005, 4000, random.Random(3))
    target = dropout_regression_solution(XS, YS, F(1, 2))
    assert all(abs(a - float(b)) < 0.03 for a, b in zip(w, target))
