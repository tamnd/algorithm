# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimax-q/. The authors are listed in prov/ZSSWVB.jsonl.

import random
from fractions import Fraction

from minimax_q import (closed_form_2x2, example_game, float_game, matrix_game, minimax_q,
                       shapley, stage_matrix, worst_case_value)

VSTAR = [Fraction(29, 4), Fraction(31, 4)]


def certify(M, value, x, y):
    """x guarantees at least value, y holds the row player to at most value."""
    m, n = len(M), len(M[0])
    assert sum(x) == 1 and sum(y) == 1 and min(x) >= 0 and min(y) >= 0
    assert min(sum(x[i] * M[i][j] for i in range(m)) for j in range(n)) == value
    assert max(sum(M[i][j] * y[j] for j in range(n)) for i in range(m)) == value


def test_simplex_value_is_certified_exactly():
    rng = random.Random(0)
    for _ in range(200):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        M = [[Fraction(rng.randint(-5, 5)) for _ in range(n)] for _ in range(m)]
        value, x, y = matrix_game(M)
        certify(M, value, x, y)
        if m == n == 2:
            assert value == closed_form_2x2(M)


def test_matching_pennies():
    M = [[Fraction(1), Fraction(-1)], [Fraction(-1), Fraction(1)]]
    value, x, y = matrix_game(M)
    assert value == 0 and x == [Fraction(1, 2)] * 2 and y == [Fraction(1, 2)] * 2


def test_one_column_is_a_max():
    M = [[Fraction(3)], [Fraction(-1)], [Fraction(7)]]
    assert matrix_game(M)[0] == 7


def test_example_value_is_a_fixed_point():
    game = example_game()
    for s in range(2):
        value, x, y = matrix_game(stage_matrix(game, s, VSTAR))
        assert value == VSTAR[s]
    value, x, y = matrix_game(stage_matrix(game, 0, VSTAR))
    assert x == [Fraction(1, 2), Fraction(1, 2)]
    assert y == [Fraction(51, 142), Fraction(91, 142)]


def test_shapley_iteration():
    v, sweeps = shapley(float_game(example_game()), 0.01)
    assert sweeps == 70
    assert max(abs(a - float(b)) for a, b in zip(v, VSTAR)) < 0.005


def test_minimax_q_learns_the_value_and_a_safe_strategy():
    game = float_game(example_game())
    for seed in range(3):
        Q, V, pi = minimax_q(game, 100000, random.Random(seed))
        assert max(abs(a - float(b)) for a, b in zip(V, VSTAR)) < 0.1
        assert abs(pi[0][0] - 0.5) < 0.02
        assert pi[1][1] > 0.98
        safe = worst_case_value(game, pi)
        assert all(w > float(b) - 0.1 for w, b in zip(safe, VSTAR))


def test_best_response_to_a_random_opponent_can_be_exploited():
    """What a single-agent Q-learner converges to against a uniform opponent:
    a deterministic best response, which a best-responding opponent exploits."""
    game = float_game(example_game())
    R, P, gamma = game
    v = [0.0, 0.0]
    for _ in range(2000):
        v = [max(sum(stage_matrix(game, s, v)[i]) / 2 for i in range(2)) for s in range(2)]
    greedy = [max(range(2), key=lambda i: sum(stage_matrix(game, s, v)[i])) for s in range(2)]
    pure = [[1.0 if i == greedy[s] else 0.0 for i in range(2)] for s in range(2)]
    exploited = worst_case_value(game, pure)
    assert exploited[0] < float(VSTAR[0]) - 0.5
