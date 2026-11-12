# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-entropy-rl/. The authors are listed in prov/X97YP9.jsonl.

import math
import random

from maximum_entropy_rl import (entropy, hard_value_iteration, log_sum_exp, q_from_v, soft_backup,
                                soft_greedy_policy, soft_policy_value, soft_value_iteration)

P = [[[1 / 2, 1 / 4], [0, 3 / 4]], [[1 / 2, 0], [0, 0]]]
R = [[1, 0], [0, 3]]
GAMMA = 0.5


def test_log_sum_exp_is_stable():
    assert abs(log_sum_exp([1000.0, 1000.0]) - (1000 + math.log(2))) < 1e-9
    assert abs(log_sum_exp([-1000.0, -1000.0 + math.log(3)]) - (-1000 + math.log(4))) < 1e-9
    # a small temperature gives the maximum plus alpha log of the number of ties
    assert abs(log_sum_exp([5.0, 5.0, 1.0], 1e-3) - (5 + 1e-3 * math.log(2))) < 1e-12


def test_one_step_bandit_gives_softmax():
    # one state, the episode ends after one step: V = log(e^0 + e^(log 2)) = log 3 and pi = (1/3, 2/3)
    V, Q = soft_value_iteration([[[0.0], [0.0]]], [[0.0, math.log(2)]], GAMMA, 1.0)
    assert abs(V[0] - math.log(3)) < 1e-12
    pi = soft_greedy_policy(Q, V, 1.0)
    assert abs(pi[0][0] - 1 / 3) < 1e-12 and abs(pi[0][1] - 2 / 3) < 1e-12


def test_fixed_point_satisfies_the_soft_bellman_equation():
    for alpha in [2.0, 1.0, 0.5, 0.1]:
        V, Q = soft_value_iteration(P, R, GAMMA, alpha)
        assert max(abs(x - y) for x, y in zip(soft_backup(P, R, V, GAMMA, alpha), V)) < 1e-11
        pi = soft_greedy_policy(Q, V, alpha)
        for row in pi:
            assert abs(sum(row) - 1) < 1e-10
        # the soft greedy policy attains the soft optimal value: V(s) = E_pi[Q] + alpha H(pi)
        for s in range(2):
            assert abs(sum(p * q for p, q in zip(pi[s], Q[s])) + alpha * entropy(pi[s]) - V[s]) < 1e-11


def test_soft_backup_is_a_contraction():
    rng = random.Random(1)
    for _ in range(50):
        U = [rng.uniform(-5, 5) for _ in range(2)]
        W = [rng.uniform(-5, 5) for _ in range(2)]
        a, b = soft_backup(P, R, U, GAMMA, 0.7), soft_backup(P, R, W, GAMMA, 0.7)
        assert max(abs(x - y) for x, y in zip(a, b)) <= GAMMA * max(abs(x - y) for x, y in zip(U, W)) + 1e-12


def test_soft_optimal_policy_beats_other_policies():
    alpha, rng = 1.0, random.Random(0)
    V, Q = soft_value_iteration(P, R, GAMMA, alpha)
    assert abs(soft_policy_value(P, R, soft_greedy_policy(Q, V, alpha), GAMMA, alpha)[0] - V[0]) < 1e-10
    for _ in range(100):
        pi = []
        for _ in range(2):
            x = rng.random()
            pi.append([x, 1 - x])
        W = soft_policy_value(P, R, pi, GAMMA, alpha)
        assert W[0] <= V[0] + 1e-12 and W[1] <= V[1] + 1e-12


def test_soft_values_lie_between_hard_values_and_the_entropy_bound():
    hard = hard_value_iteration(P, R, GAMMA)
    assert abs(hard[0] - 11 / 6) < 1e-10 and abs(hard[1] - 3) < 1e-10
    for alpha in [2.0, 1.0, 0.1, 0.01, 0.001]:
        V, _ = soft_value_iteration(P, R, GAMMA, alpha)
        for s in range(2):
            assert hard[s] - 1e-10 <= V[s] <= hard[s] + alpha * math.log(2) / (1 - GAMMA) + 1e-10
    V, Q = soft_value_iteration(P, R, GAMMA, 0.001)
    assert max(abs(x - y) for x, y in zip(V, hard)) < 2e-3
    assert soft_greedy_policy(Q, V, 0.001)[0][0] > 0.999  # the policy tends to the greedy one


def test_q_from_v_matches_hand_values():
    Q = q_from_v(P, R, [11 / 6, 3.0], GAMMA)
    assert abs(Q[0][0] - 11 / 6) < 1e-12 and abs(Q[0][1] - 9 / 8) < 1e-12 and abs(Q[1][0] - 11 / 24) < 1e-12 and Q[1][1] == 3
