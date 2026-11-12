# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bellman-optimality-equation/. The authors are listed in prov/R9MX23.jsonl.

import random
from fractions import Fraction as F

from bellman_optimality_equation import (brute_force, greedy, optimality_operator, optimality_operator_q,
                                         policy_value, q_values, solve_exact, value_iteration)

P_EX = [[[F(1), F(0)], [F(1, 2), F(1, 2)]], [[F(1, 4), F(3, 4)], [F(1), F(0)]]]
R_EX = [[F(1), F(0)], [F(2), F(3)]]


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
    v, d = solve_exact(P_EX, R_EX, g)
    assert v == [F(360, 31), F(440, 31)] and d == (1, 0)
    assert brute_force(P_EX, R_EX, g) == v
    q = q_values(P_EX, R_EX, g, v)
    assert q == [[F(355, 31), F(360, 31)], [F(440, 31), F(417, 31)]]
    assert optimality_operator_q(P_EX, R_EX, g, q) == q
    # the optimal policy changes with the discount
    assert solve_exact(P_EX, R_EX, F(1, 2))[1] == (0, 1)
    assert solve_exact(P_EX, R_EX, F(7, 10))[1] == (0, 0)


def test_exact_solution_equals_brute_force_and_is_the_fixed_point():
    rng = random.Random(71)
    for _ in range(50):
        n, m = rng.choice([(2, 2), (3, 2), (3, 3), (4, 2)])
        P, R = rand_mdp(n, m, rng)
        g = F(rng.randint(0, 9), 10)
        v, d = solve_exact(P, R, g)
        assert v == brute_force(P, R, g)
        assert optimality_operator(P, R, g, v) == v
        assert policy_value(P, R, g, greedy(P, R, g, v)) == v
        w = [x + F(rng.randint(-3, 3), 7) for x in v]
        if w != v:
            assert optimality_operator(P, R, g, w) != w


def test_value_iteration_with_floats_converges():
    rng = random.Random(72)
    for _ in range(20):
        n, m = 4, 3
        P, R = rand_mdp(n, m, rng)
        g = F(rng.randint(1, 9), 10)
        v = [float(x) for x in brute_force(P, R, g)]
        Pf = [[[float(x) for x in row] for row in ps] for ps in P]
        Rf = [[float(x) for x in row] for row in R]
        e0 = max(abs(x) for x in v)
        for k in (5, 30, 80):
            vk = value_iteration(Pf, Rf, float(g), [0.0] * n, k)
            assert max(abs(x - y) for x, y in zip(vk, v)) <= float(g) ** k * e0 + 1e-9
