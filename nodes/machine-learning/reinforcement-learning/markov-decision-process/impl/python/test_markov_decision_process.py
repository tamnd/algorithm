# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-decision-process/. The authors are listed in prov/W1VDJ0.jsonl.

import random
from fractions import Fraction as F
from itertools import product

import pytest

from markov_decision_process import MDP, example_mdp, random_mdp


def random_stochastic_policy(n, m, rng):
    pi = []
    for _ in range(n):
        w = [rng.randint(0, 5) for _ in range(m)]
        if sum(w) == 0:
            w[0] = 1
        pi.append([F(x, sum(w)) for x in w])
    return pi


def test_example_values():
    M = example_mdp()
    want = {(0, 0): [F(10), F(170, 13)], (0, 1): [F(10), F(12)],
            (1, 0): [F(360, 31), F(440, 31)], (1, 1): [F(270, 29), F(330, 29)]}
    for d, v in want.items():
        assert M.evaluate(M.as_stochastic(d)) == v
    assert M.best_deterministic() == ((1, 0), [F(360, 31), F(440, 31)])
    assert M.evaluate([[F(1, 2)] * 2] * 2) == [F(715, 71), F(875, 71)]


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        MDP([[[F(1, 2), F(1, 3)]]], [[F(0)]], F(1, 2))
    with pytest.raises(ValueError):
        MDP([[[F(1)]]], [[F(0)]], F(1))


def test_value_solves_bellman_system():
    rng = random.Random(11)
    for _ in range(40):
        M = random_mdp(3, 2, F(4, 5), rng)
        pi = random_stochastic_policy(3, 2, rng)
        v = M.evaluate(pi)
        p_pi, r_pi = M.policy_matrices(pi)
        for s in range(3):
            assert v[s] == r_pi[s] + M.gamma * sum(p_pi[s][t] * v[t] for t in range(3))


def test_deterministic_stationary_policy_is_optimal():
    rng = random.Random(2024)
    for trial in range(60):
        n, m = rng.choice([(2, 2), (3, 2), (2, 3), (3, 3)])
        gamma = rng.choice([F(0), F(1, 2), F(9, 10)])
        M = random_mdp(n, m, gamma, rng)
        d, v_star = M.best_deterministic()
        # The best deterministic policy is greedy for its own value.
        for s in range(n):
            q = [M.R[s][a] + gamma * sum(M.P[s][a][t] * v_star[t] for t in range(n)) for a in range(m)]
            assert q[d[s]] == max(q) == v_star[s]
        # No stochastic Markov stationary policy beats it in any state.
        for _ in range(15):
            v = M.evaluate(random_stochastic_policy(n, m, rng))
            assert all(v[s] <= v_star[s] for s in range(n))


def test_finite_horizon_backward_induction_matches_brute_force():
    rng = random.Random(7)
    for _ in range(25):
        M = random_mdp(2, 2, F(0), rng)
        T = 3
        v, rules = M.finite_horizon(T)
        best = [None, None]
        for flat in product(range(2), repeat=2 * T):
            ds = [flat[2 * k:2 * k + 2] for k in range(T)]
            w = [F(0), F(0)]
            for d in reversed(ds):
                w = [M.R[s][d[s]] + sum(M.P[s][d[s]][t] * w[t] for t in range(2)) for s in range(2)]
            best = [w[s] if best[s] is None else max(best[s], w[s]) for s in range(2)]
        assert v == best
        assert len(rules) == T


def test_example_finite_horizon_is_not_stationary():
    v, rules = example_mdp().finite_horizon(3)
    assert v == [F(13, 4), F(47, 8)]
    assert rules == [(1, 0), (0, 0), (0, 1)]
