# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/advantage-function/. The authors are listed in prov/H7XRK4.jsonl.

import random
from fractions import Fraction as F
from itertools import product

from advantage_function import (advantage, expected_td_error, gae, performance_difference,
                                state_value)

P_EX = [[[F(1), F(0)], [F(1, 2), F(1, 2)]], [[F(1, 4), F(3, 4)], [F(1), F(0)]]]
R_EX = [[F(1), F(0)], [F(2), F(3)]]
UNIFORM = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]
G = F(9, 10)


def rand_dist(k, rng):
    w = [rng.randint(0, 4) for _ in range(k)]
    if sum(w) == 0:
        w[rng.randrange(k)] = 1
    return [F(x, sum(w)) for x in w]


def rand_mdp(n, m, rng):
    P = [[rand_dist(n, rng) for _ in range(m)] for _ in range(n)]
    R = [[F(rng.randint(-5, 5)) for _ in range(m)] for _ in range(n)]
    return P, R


def det(d, m):
    return [[F(1 if b == d[s] else 0) for b in range(m)] for s in range(len(d))]


def test_example():
    adv, q, v = advantage(P_EX, R_EX, UNIFORM, G)
    assert adv == [[F(-1, 142), F(1, 142)], [F(37, 142), F(-37, 142)]]
    best = det((1, 0), 2)
    gain = state_value(P_EX, R_EX, best, G)[0] - v[0]
    assert gain == F(3395, 2201)
    assert performance_difference(P_EX, R_EX, best, UNIFORM, G, [F(1), F(0)]) == gain
    adv_star, _, _ = advantage(P_EX, R_EX, best, G)
    assert adv_star == [[F(-5, 31), F(0)], [F(0), F(-23, 31)]]


def test_policy_average_is_zero_and_td_error():
    rng = random.Random(51)
    for _ in range(40):
        n, m = rng.choice([(2, 2), (3, 2), (2, 3), (3, 3)])
        P, R = rand_mdp(n, m, rng)
        pi = [rand_dist(m, rng) for _ in range(n)]
        g = F(rng.randint(0, 9), 10)
        adv, q, v = advantage(P, R, pi, g)
        for s in range(n):
            assert sum(pi[s][a] * adv[s][a] for a in range(m)) == 0
            for a in range(m):
                assert expected_td_error(P, R, g, v, s, a) == adv[s][a]


def test_optimal_advantage_and_performance_difference():
    rng = random.Random(52)
    for _ in range(30):
        n, m = rng.choice([(2, 2), (3, 2)])
        P, R = rand_mdp(n, m, rng)
        g = F(rng.randint(0, 9), 10)
        vals = {d: state_value(P, R, det(d, m), g) for d in product(range(m), repeat=n)}
        vstar = [max(v[s] for v in vals.values()) for s in range(n)]
        dstar = next(d for d, v in vals.items() if v == vstar)
        adv, _, _ = advantage(P, R, det(dstar, m), g)
        for s in range(n):
            assert max(adv[s]) == 0
        pi_old = [rand_dist(m, rng) for _ in range(n)]
        pi_new = [rand_dist(m, rng) for _ in range(n)]
        mu = rand_dist(n, rng)
        lhs = sum(mu[s] * (x - y) for s, (x, y) in
                  enumerate(zip(state_value(P, R, pi_new, g), state_value(P, R, pi_old, g))))
        assert lhs == performance_difference(P, R, pi_new, pi_old, g, mu)


def test_gae_ends():
    rng = random.Random(53)
    for _ in range(30):
        T = rng.randint(1, 8)
        r = [F(rng.randint(-3, 3)) for _ in range(T)]
        v = [F(rng.randint(-3, 3)) for _ in range(T + 1)]
        g = F(rng.randint(1, 9), 10)
        deltas = [r[t] + g * v[t + 1] - v[t] for t in range(T)]
        assert gae(r, v, g, F(0)) == deltas
        one = gae(r, v, g, F(1))
        for t in range(T):
            ret = sum(g ** (k - t) * r[k] for k in range(t, T)) + g ** (T - t) * v[T]
            assert one[t] == ret - v[t]
