# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/overfitting/. The authors are listed in prov/3J0J4Q.jsonl.

import random

from overfitting import curves, fit_polynomial, legendre_row, select_by_validation

TABLE = curves(12, 50, 0.3, list(range(12)), random.Random(4))


def test_legendre_values() -> None:
    row = legendre_row(1.0, 4)  # t = 1: every P_j(1) = 1
    assert all(abs(v - 1) < 1e-12 for v in row)
    assert abs(legendre_row(0.75, 2)[2] - (3 * 0.25 - 1) / 2) < 1e-12


def test_recovers_a_polynomial() -> None:
    xs = [i / 7 for i in range(8)]
    g = fit_polynomial(xs, [2 - x + 4 * x ** 3 for x in xs], 5)
    assert all(abs(g(x) - (2 - x + 4 * x ** 3)) < 1e-9 for x in (0.1, 0.55, 0.99))


def test_training_error_never_rises_with_degree() -> None:
    # The classes are nested, so the least squares training error cannot increase.
    train = [row[1] for row in TABLE]
    for a, b in zip(train, train[1:]):
        assert b <= a + 1e-9


def test_full_degree_interpolates() -> None:
    assert TABLE[-1][1] < 1e-8  # 12 points, degree 11


def test_validation_choice() -> None:
    p = select_by_validation(TABLE)
    assert TABLE[p][2] == min(row[2] for row in TABLE)
    assert p == 3
    best_true = min(row[3] for row in TABLE)
    assert TABLE[p][3] - best_true < 0.01
