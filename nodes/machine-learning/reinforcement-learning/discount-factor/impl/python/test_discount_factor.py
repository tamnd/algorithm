# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discount-factor/. The authors are listed in prov/E1K7NT.jsonl.

import math
import random
from fractions import Fraction as F
from itertools import product

import pytest

from discount_factor import (discounted_k_step, discounted_value, geometric_horizon_value,
                             horizon_for_tolerance, optimal_policies, undiscounted_k_step)

P_EX = [[[F(1), F(0)], [F(1, 2), F(1, 2)]], [[F(1, 4), F(3, 4)], [F(1), F(0)]]]
R_EX = [[F(1), F(0)], [F(2), F(3)]]


def rand_mdp(n, m, rng):
    P = []
    for _ in range(n):
        rows = []
        for _ in range(m):
            w = [rng.randint(0, 4) for _ in range(n)]
            if sum(w) == 0:
                w[rng.randrange(n)] = 1
            rows.append([F(x, sum(w)) for x in w])
        P.append(rows)
    R = [[F(rng.randint(-5, 5)) for _ in range(m)] for _ in range(n)]
    return P, R


def test_geometric_horizon_equals_discounting_exactly():
    rng = random.Random(21)
    for _ in range(40):
        n, m = rng.choice([(2, 2), (3, 2), (4, 2)])
        P, R = rand_mdp(n, m, rng)
        g = F(rng.randint(0, 9), 10)
        for d in product(range(m), repeat=n):
            assert geometric_horizon_value(P, R, d, g) == discounted_value(P, R, d, g)


def test_geometric_horizon_truncated_sum():
    # E[sum_(t < min(tau, K)) R_(t+1)] = sum_(t < K) gamma^t E[R_(t+1)], with
    # Pr(tau = T) = (1 - gamma) gamma^(T - 1), computed term by term.
    rng = random.Random(8)
    for _ in range(20):
        P, R = rand_mdp(3, 2, rng)
        g = F(rng.randint(1, 9), 10)
        d = (rng.randrange(2), rng.randrange(2), rng.randrange(2))
        K = 5
        lhs = [F(0)] * 3
        for T in range(1, K):
            w = (1 - g) * g ** (T - 1)
            vT = undiscounted_k_step(P, R, d, T)
            lhs = [x + w * y for x, y in zip(lhs, vT)]
        vK = undiscounted_k_step(P, R, d, K)
        lhs = [x + g ** (K - 1) * y for x, y in zip(lhs, vK)]
        assert lhs == discounted_k_step(P, R, d, g, K)


def test_horizon_for_tolerance():
    assert horizon_for_tolerance(F(9, 10), F(1, 100)) == 44
    assert horizon_for_tolerance(F(99, 100), F(1, 100)) == 459
    assert horizon_for_tolerance(F(1, 2), F(1)) == 0
    for g in (F(1, 2), F(9, 10), F(99, 100)):
        for e in (F(1, 10), F(1, 1000)):
            h = horizon_for_tolerance(g, e)
            assert g ** h <= e and (h == 0 or g ** (h - 1) > e)
            # gamma^H <= exp(-(1 - gamma) H), so ln(1/eps)/(1 - gamma) steps always suffice
            assert h <= math.ceil(math.log(1 / float(e)) / float(1 - g)) + 1
    with pytest.raises(ValueError):
        horizon_for_tolerance(F(1), F(1, 2))


def test_example_optimal_policy_depends_on_gamma():
    assert optimal_policies(P_EX, R_EX, F(0)) == [(0, 1)]
    assert optimal_policies(P_EX, R_EX, F(1, 2)) == [(0, 1)]
    assert optimal_policies(P_EX, R_EX, F(2, 3)) == [(0, 0), (0, 1)]
    assert optimal_policies(P_EX, R_EX, F(3, 4)) == [(0, 0)]
    assert optimal_policies(P_EX, R_EX, F(4, 5)) == [(0, 0), (1, 0)]
    assert optimal_policies(P_EX, R_EX, F(9, 10)) == [(1, 0)]


def test_constant_reward_value():
    P = [[[F(1)]]]
    for g in (F(0), F(1, 2), F(9, 10), F(99, 100)):
        assert discounted_value(P, [[F(1)]], (0,), g) == [1 / (1 - g)]
