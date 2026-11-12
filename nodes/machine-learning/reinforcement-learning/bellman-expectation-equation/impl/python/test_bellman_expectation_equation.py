# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bellman-expectation-equation/. The authors are listed in prov/MAY0T7.jsonl.

import random
from fractions import Fraction as F

from bellman_expectation_equation import (bellman_operator, bellman_operator_q, iterate, solve,
                                          truncated_by_paths)

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
    v = solve(P_EX, R_EX, UNIFORM, g)
    assert v == [F(715, 71), F(875, 71)]
    assert bellman_operator(P_EX, R_EX, UNIFORM, g, v) == v
    q = [[F(1429, 142), F(1431, 142)], [F(1787, 142), F(1713, 142)]]
    assert bellman_operator_q(P_EX, R_EX, UNIFORM, g, q) == q


def test_exact_solution_is_a_fixed_point_and_unique():
    rng = random.Random(61)
    for _ in range(40):
        n, m = rng.choice([(2, 2), (3, 2), (4, 3)])
        P, R = rand_mdp(n, m, rng)
        pi = [rand_dist(m, rng) for _ in range(n)]
        g = F(rng.randint(0, 9), 10)
        v = solve(P, R, pi, g)
        assert bellman_operator(P, R, pi, g, v) == v
        w = [F(rng.randint(-9, 9)) for _ in range(n)]
        if w != v:
            assert bellman_operator(P, R, pi, g, w) != w


def test_iterates_equal_truncated_returns():
    rng = random.Random(62)
    for _ in range(20):
        P, R = rand_mdp(2, 2, rng)
        pi = [rand_dist(2, rng) for _ in range(2)]
        g = F(rng.randint(1, 9), 10)
        for k in range(5):
            vk = iterate(P, R, pi, g, [F(0), F(0)], k)
            assert vk == [truncated_by_paths(P, R, pi, g, s, k) for s in range(2)]


def test_float_iteration_converges_geometrically():
    rng = random.Random(63)
    for _ in range(20):
        n, m = 4, 3
        P, R = rand_mdp(n, m, rng)
        pi = [rand_dist(m, rng) for _ in range(n)]
        g = F(rng.randint(1, 9), 10)
        v = [float(x) for x in solve(P, R, pi, g)]
        Pf = [[[float(x) for x in row] for row in ps] for ps in P]
        Rf = [[float(x) for x in row] for row in R]
        pif = [[float(x) for x in row] for row in pi]
        e0 = max(abs(x) for x in v)
        for k in (5, 20, 60):
            vk = iterate(Pf, Rf, pif, float(g), [0.0] * n, k)
            assert max(abs(x - y) for x, y in zip(vk, v)) <= float(g) ** k * e0 + 1e-9
