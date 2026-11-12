# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/policy/. The authors are listed in prov/SSS4DF.jsonl.

import random
from fractions import Fraction as F

import pytest

from policy import (check_policy, deterministic, discounted_occupancy, induced_chain,
                    policy_value, state_distribution)

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


def joint_by_enumeration(P, rule, mu, t):
    """Pr(S_t = s, A_t = a) for a history dependent rule(history) -> distribution,
    by summing over all histories of length t."""
    n, m = len(P), len(P[0])
    paths = [((s,), mu[s]) for s in range(n) if mu[s]]
    for _ in range(t):
        nxt = []
        for h, p in paths:
            dist = rule(h)
            for a in range(m):
                for u in range(n):
                    q = p * dist[a] * P[h[-1]][a][u]
                    if q:
                        nxt.append((h + (a, u), q))
        paths = nxt
    joint = [[F(0)] * m for _ in range(n)]
    for h, p in paths:
        dist = rule(h)
        for a in range(m):
            joint[h[-1]][a] += p * dist[a]
    return joint


def test_example_distributions():
    d = deterministic((1, 0), 2)
    mu = [F(1), F(0)]
    assert state_distribution(P_EX, d, mu, 1) == [F(1, 2), F(1, 2)]
    assert state_distribution(P_EX, d, mu, 2) == [F(3, 8), F(5, 8)]
    occ = discounted_occupancy(P_EX, d, mu, F(9, 10))
    assert occ == [F(13, 31), F(18, 31)]
    v = policy_value(P_EX, R_EX, d, F(9, 10))
    assert v[0] == sum(occ[s] * R_EX[s][d[s].index(1)] for s in range(2)) / (1 - F(9, 10))


def test_check_policy():
    check_policy([[F(1, 2), F(1, 2)]], 2)
    with pytest.raises(ValueError):
        check_policy([[F(1, 2), F(1, 3)]], 2)


def test_state_distribution_matches_path_enumeration():
    rng = random.Random(5)
    for _ in range(30):
        n, m = rng.choice([(2, 2), (3, 2), (2, 3)])
        P, _ = rand_mdp(n, m, rng)
        pi = [rand_dist(m, rng) for _ in range(n)]
        mu = rand_dist(n, rng)
        for t in range(4):
            joint = joint_by_enumeration(P, lambda h: pi[h[-1]], mu, t)
            marg = [sum(row) for row in joint]
            assert state_distribution(P, pi, mu, t) == marg


def test_occupancy_is_a_distribution_and_gives_the_value():
    rng = random.Random(9)
    for _ in range(40):
        n, m = rng.choice([(2, 2), (3, 2), (3, 3)])
        P, R = rand_mdp(n, m, rng)
        pi = [rand_dist(m, rng) for _ in range(n)]
        mu = rand_dist(n, rng)
        g = rng.choice([F(0), F(1, 3), F(4, 5)])
        occ = discounted_occupancy(P, pi, mu, g)
        assert sum(occ) == 1 and min(occ) >= 0
        v = policy_value(P, R, pi, g)
        r_pi = [sum(pi[s][a] * R[s][a] for a in range(m)) for s in range(n)]
        assert sum(mu[s] * v[s] for s in range(n)) * (1 - g) == sum(occ[s] * r_pi[s] for s in range(n))
        # Truncated series: the error after H terms is at most gamma^H.
        H = 6
        part = [(1 - g) * sum(g ** t * state_distribution(P, pi, mu, t)[s] for t in range(H)) for s in range(n)]
        assert all(0 <= occ[s] - part[s] <= g ** H for s in range(n))


def test_markov_policy_matches_history_dependent_marginals():
    rng = random.Random(13)
    for _ in range(20):
        n, m = 2, 2
        P, _ = rand_mdp(n, m, rng)
        mu = rand_dist(n, rng)
        table = {}

        def rule(h):
            # depends on the whole history, not only on the last state
            key = h
            if key not in table:
                table[key] = rand_dist(m, rng)
            return table[key]

        for t in range(3):
            joint_h = joint_by_enumeration(P, rule, mu, t)
            # the Markov policy pi_t(a | s) = Pr(S_t = s, A_t = a) / Pr(S_t = s)
            marg = [sum(row) for row in joint_h]
            pis = []
            for k in range(t + 1):
                jk = joint_by_enumeration(P, rule, mu, k)
                mk = [sum(row) for row in jk]
                pis.append([[jk[s][a] / mk[s] if mk[s] else F(1, m) for a in range(m)] for s in range(n)])
            joint_m = joint_by_enumeration(P, lambda h: pis[(len(h) - 1) // 2][h[-1]], mu, t)
            assert joint_m == joint_h
            assert sum(marg) == 1


def test_induced_chain_rows_sum_to_one():
    q = induced_chain(P_EX, [[F(1, 2)] * 2] * 2)
    assert q == [[F(3, 4), F(1, 4)], [F(5, 8), F(3, 8)]]
