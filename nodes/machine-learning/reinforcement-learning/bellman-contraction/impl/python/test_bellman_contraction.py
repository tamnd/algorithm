# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bellman-contraction/. The authors are listed in prov/Z62P7P.jsonl.

import random
from fractions import Fraction as F

from bellman_contraction import (greedy, max_norm, optimal_value, policy_value, t_opt, t_policy,
                                 value_iteration)

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


def rand_vec(n, rng):
    return [F(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(n)]


def test_contraction_on_random_pairs():
    rng = random.Random(81)
    for _ in range(300):
        n, m = rng.choice([(2, 2), (3, 2), (3, 3), (4, 2)])
        P, R = rand_mdp(n, m, rng)
        g = F(rng.randint(0, 9), 10)
        pi = [rand_dist(m, rng) for _ in range(n)]
        u, w = rand_vec(n, rng), rand_vec(n, rng)
        d = max_norm(u, w)
        assert max_norm(t_opt(P, R, g, u), t_opt(P, R, g, w)) <= g * d
        assert max_norm(t_policy(P, R, pi, g, u), t_policy(P, R, pi, g, w)) <= g * d


def test_modulus_gamma_is_attained():
    P, R = [[[F(1)]]], [[F(5)]]
    for g in (F(0), F(1, 3), F(9, 10)):
        u, w = [F(7)], [F(2)]
        assert max_norm(t_opt(P, R, g, u), t_opt(P, R, g, w)) == g * max_norm(u, w)


def test_not_a_contraction_in_the_euclidean_norm():
    # P^pi sends both states to state 2; u - w = (0, 1) has Euclidean length 1
    P, R = [[[F(0), F(1)]], [[F(0), F(1)]]], [[F(0)], [F(0)]]
    g = F(9, 10)
    d = [a - b for a, b in zip(t_opt(P, R, g, [F(0), F(1)]), t_opt(P, R, g, [F(0), F(0)]))]
    assert sum(x * x for x in d) == 2 * g * g > 1


def test_error_bounds_of_value_iteration():
    rng = random.Random(82)
    for _ in range(30):
        n, m = rng.choice([(2, 2), (3, 2), (3, 3)])
        P, R = rand_mdp(n, m, rng)
        g = F(rng.randint(1, 9), 10)
        vs = optimal_value(P, R, g)
        v = rand_vec(n, rng)
        e0 = max_norm(v, vs)
        for k in range(1, 7):
            w = t_opt(P, R, g, v)
            assert max_norm(w, vs) <= g ** k * e0
            assert max_norm(w, vs) <= g / (1 - g) * max_norm(w, v)
            v = w


def test_stopping_rule_gives_eps_optimal_policy():
    rng = random.Random(83)
    for _ in range(30):
        n, m = rng.choice([(2, 2), (3, 2), (3, 3)])
        P, R = rand_mdp(n, m, rng)
        g = F(rng.randint(1, 9), 10)
        eps = F(rng.randint(1, 20), 10)
        vs = optimal_value(P, R, g)
        v, d, _ = value_iteration(P, R, g, eps)
        assert max_norm(v, vs) < eps / 2
        assert max_norm(policy_value(P, R, g, d), vs) < eps


def test_loss_of_greedy_policy():
    rng = random.Random(84)
    for _ in range(200):
        n, m = rng.choice([(2, 2), (3, 2), (3, 3)])
        P, R = rand_mdp(n, m, rng)
        g = F(rng.randint(0, 9), 10)
        vs = optimal_value(P, R, g)
        v = [x + F(rng.randint(-6, 6), 4) for x in vs]
        loss = max_norm(vs, policy_value(P, R, g, greedy(P, R, g, v)))
        residual = max_norm(t_opt(P, R, g, v), v)
        assert loss <= 2 * g * residual / (1 - g)  # Williams and Baird
        assert loss <= 2 * g * max_norm(v, vs) / (1 - g)  # Singh and Yee


def test_example_sweeps():
    v, d, k = value_iteration(P_EX, R_EX, F(9, 10), F(1, 100), [F(0), F(0)])
    assert d == (1, 0)
    assert max_norm(v, [F(360, 31), F(440, 31)]) < F(1, 200)
