# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/action-value-function/. The authors are listed in prov/VRH12A.jsonl.

import random
from fractions import Fraction as F

from action_value_function import (action_value, greedy, optimal_action_value, q_from_v, state_value,
                                   v_from_q)

P_EX = [[[F(1), F(0)], [F(1, 2), F(1, 2)]], [[F(1, 4), F(3, 4)], [F(1), F(0)]]]
R_EX = [[F(1), F(0)], [F(2), F(3)]]
UNIFORM = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]


def rand_dist(k, rng):
    w = [rng.randint(0, 4) for _ in range(k)]
    if sum(w) == 0:
        w[rng.randrange(k)] = 1
    return [F(x, sum(w)) for x in w]


def rand_mdp(n, m, rng):
    P = [[rand_dist(n, rng) for _ in range(m)] for _ in range(n)]
    R = [[F(rng.randint(-5, 5)) for _ in range(m)] for _ in range(n)]
    return P, R


def test_example():
    g = F(9, 10)
    q = action_value(P_EX, R_EX, UNIFORM, g)
    assert q == [[F(1429, 142), F(1431, 142)], [F(1787, 142), F(1713, 142)]]
    assert v_from_q(UNIFORM, q) == [F(715, 71), F(875, 71)]
    qs, vs = optimal_action_value(P_EX, R_EX, g)
    assert qs == [[F(355, 31), F(360, 31)], [F(440, 31), F(417, 31)]]
    assert greedy(qs) == (1, 0)
    assert greedy(q) == (1, 0)


def test_q_system_agrees_with_v_system():
    rng = random.Random(41)
    for _ in range(40):
        n, m = rng.choice([(2, 2), (3, 2), (2, 3)])
        P, R = rand_mdp(n, m, rng)
        pi = [rand_dist(m, rng) for _ in range(n)]
        g = F(rng.randint(0, 9), 10)
        q = action_value(P, R, pi, g)
        v = state_value(P, R, pi, g)
        assert q == q_from_v(P, R, g, v)
        assert v_from_q(pi, q) == v


def test_optimal_q_fixed_point_and_greedy_policy():
    rng = random.Random(42)
    for _ in range(40):
        n, m = rng.choice([(2, 2), (3, 2), (3, 3)])
        P, R = rand_mdp(n, m, rng)
        g = F(rng.randint(0, 9), 10)
        qs, vs = optimal_action_value(P, R, g)
        for s in range(n):
            assert max(qs[s]) == vs[s]
            for a in range(m):
                assert qs[s][a] == R[s][a] + g * sum(P[s][a][t] * max(qs[t]) for t in range(n))
        d = greedy(qs)
        pi = [[F(1 if b == d[s] else 0) for b in range(m)] for s in range(n)]
        assert state_value(P, R, pi, g) == vs
