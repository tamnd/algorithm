# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/state-value-function/. The authors are listed in prov/ZWKZEG.jsonl.

import random
from fractions import Fraction as F

from state_value_function import (optimal_state_value, sample_return, state_value,
                                  truncated_value_by_paths)

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
    assert state_value(P_EX, R_EX, UNIFORM, g) == [F(715, 71), F(875, 71)]
    assert optimal_state_value(P_EX, R_EX, g) == [F(360, 31), F(440, 31)]
    assert state_value(P_EX, R_EX, UNIFORM, F(0)) == [F(1, 2), F(5, 2)]


def test_exact_value_against_truncated_path_sums():
    rng = random.Random(31)
    for _ in range(25):
        n, m = 2, 2
        P, R = rand_mdp(n, m, rng)
        pi = [rand_dist(m, rng) for _ in range(n)]
        g = F(rng.randint(0, 9), 10)
        v = state_value(P, R, pi, g)
        rmax = max(abs(x) for row in R for x in row)
        for H in (1, 3, 5):
            for s in range(n):
                part = truncated_value_by_paths(P, R, pi, g, s, H)
                assert abs(v[s] - part) <= g ** H * rmax / (1 - g)


def test_bounds_and_optimality():
    rng = random.Random(32)
    for _ in range(40):
        n, m = rng.choice([(2, 2), (3, 2), (3, 3)])
        P, R = rand_mdp(n, m, rng)
        g = F(rng.randint(0, 9), 10)
        vstar = optimal_state_value(P, R, g)
        rmax = max(abs(x) for row in R for x in row)
        for _ in range(5):
            pi = [rand_dist(m, rng) for _ in range(n)]
            v = state_value(P, R, pi, g)
            assert all(abs(x) <= rmax / (1 - g) for x in v)
            assert all(v[s] <= vstar[s] for s in range(n))


def test_monte_carlo_average_is_close():
    rng = random.Random(2018)
    g = 0.9
    est = sum(sample_return(P_EX, R_EX, UNIFORM, g, 0, 120, rng) for _ in range(3000)) / 3000
    # exact value 715/71; the truncation error is below 0.9^120 * 3 / 0.1 < 1e-4
    assert abs(est - 715 / 71) < 0.2
