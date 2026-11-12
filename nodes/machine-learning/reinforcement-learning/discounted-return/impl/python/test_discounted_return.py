# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discounted-return/. The authors are listed in prov/HDFR24.jsonl.

import random
from fractions import Fraction as F

from discounted_return import n_step_return, return_from, returns


def test_worked_example():
    assert returns([F(1), F(0), F(2), F(3)], F(1, 2)) == [F(15, 8), F(7, 4), F(7, 2), F(3), F(0)]


def test_empty_episode():
    assert returns([], F(1, 2)) == [F(0)]


def test_backward_pass_matches_direct_sum_and_recursion():
    rng = random.Random(4)
    for _ in range(500):
        T = rng.randint(0, 12)
        g = F(rng.randint(0, 10), 10)
        rs = [F(rng.randint(-5, 5)) for _ in range(T)]
        G = returns(rs, g)
        assert len(G) == T + 1 and G[T] == 0
        for t in range(T):
            assert G[t] == return_from(rs, g, t)
            assert G[t] == rs[t] + g * G[t + 1]


def test_bound_and_tail():
    rng = random.Random(6)
    for _ in range(300):
        T = rng.randint(1, 30)
        g = F(rng.randint(0, 9), 10)
        rmax = 5
        rs = [F(rng.randint(-rmax, rmax)) for _ in range(T)]
        G = returns(rs, g)
        assert all(abs(x) <= rmax / (1 - g) for x in G)
        H = rng.randint(0, T)
        # dropping the rewards after step H changes G_0 by at most gamma^H rmax / (1 - gamma)
        assert abs(G[0] - return_from(rs[:H], g, 0)) <= g ** H * rmax / (1 - g)


def test_constant_reward():
    for g in (F(1, 2), F(9, 10)):
        G = returns([F(1)] * 200, g)
        assert 0 <= 1 / (1 - g) - G[0] <= g ** 200 / (1 - g)


def test_n_step_return_with_exact_tail_is_the_return():
    rng = random.Random(10)
    for _ in range(300):
        T = rng.randint(1, 10)
        g = F(rng.randint(0, 10), 10)
        rs = [F(rng.randint(-3, 3)) for _ in range(T)]
        G = returns(rs, g)
        for t in range(T):
            for n in range(1, T + 2):
                assert n_step_return(rs, G, g, t, n) == G[t]


def test_floats_agree_with_fractions():
    rng = random.Random(12)
    rs = [rng.uniform(-1, 1) for _ in range(1000)]
    G = returns(rs, 0.99)
    exact = returns([F(x) for x in rs], F(99, 100))
    assert all(abs(a - float(b)) < 1e-9 for a, b in zip(G, exact))
