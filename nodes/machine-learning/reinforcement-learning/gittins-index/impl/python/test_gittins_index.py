# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gittins-index/. The authors are listed in prov/7M9CFD.jsonl.

import random
from fractions import Fraction

from gittins_index import (
    bernoulli_index,
    bernoulli_tree_arm,
    chain_index,
    gittins_indices,
    gittins_policy,
    optimal_values,
    policy_values,
    restart_index,
    retirement_index,
)

# The risky arm of the page: state 0 pays 0 and moves to state 1 or 2 with chance 1/2 each;
# state 1 pays 1 once and moves to state 2; state 2 pays 0.2 for ever.
RISKY = ([0.0, 1.0, 0.2], [[0.0, 0.5, 0.5], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]])
SAFE = ([0.3], [[1.0]])


def test_indices_of_the_page_example() -> None:
    r, P = RISKY
    idx = gittins_indices(r, P, 0.9)
    assert abs(idx[0] - 9 / 29) < 1e-9
    assert abs(idx[1] - 1.0) < 1e-9
    assert abs(idx[2] - 0.2) < 1e-9
    for x in range(3):
        assert abs(retirement_index(r, P, 0.9, x) - idx[x]) < 1e-8


def chain_arm(rewards, tail):
    m = len(rewards) + 1
    P = [[0.0] * m for _ in range(m)]
    for i in range(m - 1):
        P[i][i + 1] = 1.0
    P[m - 1][m - 1] = 1.0
    return [float(x) for x in rewards] + [float(tail)], P


def test_deterministic_chain_exactly() -> None:
    assert chain_index([Fraction(0), Fraction(1), Fraction(0)], Fraction(1, 2), Fraction(9, 10)) == Fraction(9, 19)
    r, P = chain_arm([0, 1, 0], Fraction(1, 2))
    assert abs(restart_index(r, P, 0.9, 0) - 9 / 19) < 1e-9
    rng = random.Random(3)
    for _ in range(20):
        rewards = [Fraction(rng.randint(0, 10), 10) for _ in range(rng.randint(1, 5))]
        tail = Fraction(rng.randint(0, 10), 10)
        gamma = Fraction(rng.choice([1, 3, 5, 8, 9]), 10)
        exact = chain_index(rewards, tail, gamma)
        r, P = chain_arm(rewards, tail)
        assert abs(restart_index(r, P, float(gamma), 0) - float(exact)) < 1e-9


def test_bounds_on_the_index() -> None:
    rng = random.Random(4)
    for _ in range(10):
        m = 4
        r = [rng.random() for _ in range(m)]
        P = []
        for _ in range(m):
            w = [rng.random() for _ in range(m)]
            P.append([x / sum(w) for x in w])
        for x, v in enumerate(gittins_indices(r, P, 0.8)):
            assert r[x] - 1e-9 <= v <= max(r) + 1e-9


def test_bernoulli_arm_with_uniform_prior() -> None:
    # Gittins' tables give 0.7029 for Beta(1, 1) and discount 0.9.
    assert abs(bernoulli_index(1, 1, 0.9, depth=150) - 0.7029) < 5e-5
    r, P, states = bernoulli_tree_arm(1, 1, 10)
    root = states.index((0, 0))
    assert abs(restart_index(r, P, 0.9, root) - bernoulli_index(1, 1, 0.9, depth=10)) < 1e-7


def random_arm(rng: random.Random, m: int):
    r = [round(rng.random(), 2) for _ in range(m)]
    P = []
    for _ in range(m):
        w = [rng.random() for _ in range(m)]
        P.append([x / sum(w) for x in w])
    return r, P


def test_index_policy_is_optimal_on_two_arms() -> None:
    for seed in range(5):
        rng = random.Random(seed)
        arms = [random_arm(rng, 3), random_arm(rng, 3)]
        opt = optimal_values(arms, 0.9)
        git = policy_values(arms, 0.9, gittins_policy(arms, 0.9))
        assert max(abs(opt[s] - git[s]) for s in opt) < 1e-8


def test_myopic_rule_is_not_optimal() -> None:
    arms = [RISKY, SAFE]
    opt = optimal_values(arms, 0.9)
    git = policy_values(arms, 0.9, gittins_policy(arms, 0.9))
    myopic = policy_values(arms, 0.9, lambda s: max(range(2), key=lambda a: (arms[a][0][s[a]], -a)))
    assert gittins_policy(arms, 0.9)((0, 0)) == 0
    assert abs(opt[(0, 0)] - 3.015) < 1e-9
    assert abs(git[(0, 0)] - 3.015) < 1e-9
    assert abs(myopic[(0, 0)] - 3.0) < 1e-9
