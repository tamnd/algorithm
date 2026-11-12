# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-game/. The authors are listed in prov/VR68TW.jsonl.

import random
from fractions import Fraction as F

from markov_game import (best_response_values, pair_value, shapley_operator, shapley_value_iteration,
                         solve_2x2, stage_matrix)


def rand_dist(k, rng):
    w = [rng.randint(0, 4) for _ in range(k)]
    if sum(w) == 0:
        w[rng.randrange(k)] = 1
    return [F(x, sum(w)) for x in w]


def rand_game(n, rng):
    P = [[[rand_dist(n, rng) for _ in range(2)] for _ in range(2)] for _ in range(n)]
    R = [[[F(rng.randint(-5, 5)) for _ in range(2)] for _ in range(2)] for _ in range(n)]
    return P, R


def example():
    stay, move = [F(1), F(0)], [F(0), F(1)]
    half = [F(1, 2), F(1, 2)]
    P = [[[stay, move], [move, stay]], [[half, half], [half, half]]]
    R = [[[F(3), F(-1)], [F(-2), F(2)]], [[F(1), F(0)], [F(2), F(1)]]]
    return P, R


def test_matrix_game_solver_guarantees():
    assert solve_2x2([[F(1), F(-1)], [F(-1), F(1)]]) == (0, F(1, 2), F(1, 2))
    assert solve_2x2([[F(1), F(0)], [F(2), F(1)]]) == (1, 0, 0)
    rng = random.Random(101)
    for _ in range(500):
        M = [[F(rng.randint(-6, 6)) for _ in range(2)] for _ in range(2)]
        v, p, q = solve_2x2(M)
        assert 0 <= p <= 1 and 0 <= q <= 1
        # the row strategy gets at least v against each column, the column strategy
        # gives at most v against each row
        for j in range(2):
            assert p * M[0][j] + (1 - p) * M[1][j] >= v
        for i in range(2):
            assert q * M[i][0] + (1 - q) * M[i][1] <= v
        assert sum((p if i == 0 else 1 - p) * (q if j == 0 else 1 - q) * M[i][j]
                   for i in range(2) for j in range(2)) == v


def test_shapley_operator_is_a_contraction():
    rng = random.Random(102)
    for _ in range(300):
        n = rng.choice([1, 2, 3])
        P, R = rand_game(n, rng)
        g = F(rng.randint(0, 9), 10)
        u = [F(rng.randint(-20, 20), rng.randint(1, 4)) for _ in range(n)]
        w = [F(rng.randint(-20, 20), rng.randint(1, 4)) for _ in range(n)]
        tu, _, _ = shapley_operator(P, R, g, u)
        tw, _, _ = shapley_operator(P, R, g, w)
        assert max(abs(a - b) for a, b in zip(tu, tw)) <= g * max(abs(a - b) for a, b in zip(u, w))


def test_fixed_point_and_equilibrium():
    rng = random.Random(103)
    games = [example()] + [rand_game(rng.choice([2, 3]), rng) for _ in range(15)]
    for P, R in games:
        g = 0.9
        Pf = [[[[float(z) for z in t] for t in row] for row in s] for s in P]
        Rf = [[[float(z) for z in row] for row in s] for s in R]
        v, x, y, _ = shapley_value_iteration(Pf, Rf, g, 1e-9)
        tv, _, _ = shapley_operator(Pf, Rf, g, v)
        assert max(abs(a - b) for a, b in zip(tv, v)) < 1e-9
        assert max(abs(a - b) for a, b in zip(pair_value(Pf, Rf, g, x, y), v)) < 1e-8
        best_row, best_col = best_response_values(Pf, Rf, g, x, y)
        assert all(b <= a + 1e-8 for a, b in zip(v, best_row))
        assert all(b >= a - 1e-8 for a, b in zip(v, best_col))


def test_example_values():
    P, R = example()
    v, x, y, k = shapley_value_iteration(P, R, F(9, 10), F(1, 10 ** 6))
    tv, _, _ = shapley_operator(P, R, F(9, 10), v)
    assert max(abs(a - b) for a, b in zip(tv, v)) < F(1, 10 ** 6)
    _, p, q = solve_2x2(stage_matrix(P, R, F(9, 10), v, 1))
    assert (p, q) == (0, 0)
    exact = [F(29, 4), F(31, 4)]
    assert shapley_operator(P, R, F(9, 10), exact) == (exact, [F(1, 2), 0], [F(51, 142), 0])
    assert max(abs(a - b) for a, b in zip(v, exact)) < F(1, 10 ** 6)
