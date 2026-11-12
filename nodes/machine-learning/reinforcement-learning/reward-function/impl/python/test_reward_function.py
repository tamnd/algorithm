# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reward-function/. The authors are listed in prov/AMCRZY.jsonl.

import random
from fractions import Fraction as F
from itertools import product

import pytest

from reward_function import (affine, expected_from_next_state, from_dynamics, k_step_value_by_paths,
                             k_step_value_expected, optimal_deterministic, policy_value)

P_EX = [[[F(1), F(0)], [F(1, 2), F(1, 2)]], [[F(1, 4), F(3, 4)], [F(1), F(0)]]]
R_EX = [[F(1), F(0)], [F(2), F(3)]]


def rand_dist(k, rng):
    w = [rng.randint(0, 4) for _ in range(k)]
    if sum(w) == 0:
        w[rng.randrange(k)] = 1
    return [F(x, sum(w)) for x in w]


def test_example_next_state_reward():
    R3 = [[[F(1), F(1)], [F(-2), F(2)]], [[F(2), F(2)], [F(3), F(3)]]]
    assert expected_from_next_state(P_EX, R3) == R_EX


def test_dynamics_split():
    p4 = [[{(0, F(1)): F(1)}, {(0, F(-2)): F(1, 2), (1, F(2)): F(1, 2)}],
          [{(0, F(2)): F(1, 4), (1, F(2)): F(3, 4)}, {(0, F(0)): F(1, 2), (0, F(6)): F(1, 2)}]]
    P, R = from_dynamics(p4)
    assert P == P_EX and R == R_EX
    with pytest.raises(ValueError):
        from_dynamics([[{(0, F(1)): F(1, 2)}]])


def test_expected_reward_gives_the_same_values():
    rng = random.Random(3)
    for _ in range(30):
        n, m = rng.choice([(2, 2), (3, 2)])
        P = [[rand_dist(n, rng) for _ in range(m)] for _ in range(n)]
        R3 = [[[F(rng.randint(-4, 4)) for _ in range(n)] for _ in range(m)] for _ in range(n)]
        R = expected_from_next_state(P, R3)
        g = rng.choice([F(1), F(1, 2), F(9, 10)])
        for d in product(range(m), repeat=n):
            for k in range(4):
                assert k_step_value_by_paths(P, R3, d, g, k) == k_step_value_expected(P, R, d, g, k)


def test_positive_affine_map_keeps_optimal_policies():
    rng = random.Random(17)
    for _ in range(30):
        n, m = 3, 2
        P = [[rand_dist(n, rng) for _ in range(m)] for _ in range(n)]
        R = [[F(rng.randint(-4, 4)) for _ in range(m)] for _ in range(n)]
        g = F(4, 5)
        c, b = F(rng.randint(1, 5), rng.randint(1, 3)), F(rng.randint(-6, 6))
        R2 = affine(R, c, b)
        assert optimal_deterministic(P, R, g) == optimal_deterministic(P, R2, g)
        for d in product(range(m), repeat=n):
            v, w = policy_value(P, R, d, g), policy_value(P, R2, d, g)
            assert w == [c * x + b / (1 - g) for x in v]


def test_constant_shift_changes_an_episodic_task():
    # state 0: action 0 ends the episode (to the terminal state 1), action 1 loops.
    # The terminal state 1 always gives 0, so a shift does not reach it.
    P = [[[F(0), F(1)], [F(1), F(0)]], [[F(0), F(1)], [F(0), F(1)]]]
    R = [[F(0), F(-1)], [F(0), F(0)]]
    g = F(1, 2)
    assert {d[0] for d in optimal_deterministic(P, R, g)} == {0}
    shifted = [[x + 3 for x in R[0]], R[1]]
    assert {d[0] for d in optimal_deterministic(P, shifted, g)} == {1}
