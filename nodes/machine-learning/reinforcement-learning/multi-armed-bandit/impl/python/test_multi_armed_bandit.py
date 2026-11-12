# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-armed-bandit/. The authors are listed in prov/J62NE6.jsonl.

import random
from fractions import Fraction as F

from multi_armed_bandit import (
    decomposition,
    exact_regrets,
    explore_then_commit,
    random_pseudo_regret,
    run,
)


def test_sample_decomposition_is_exact() -> None:
    # n mu_star - sum_t mu_{A_t} = sum_i Delta_i T_i(n) on every run.
    means = [F(7, 10), F(1, 2), F(3, 10)]
    for seed in range(50):
        rng = random.Random(seed)
        actions, _ = run(explore_then_commit(3), means, 40, rng)
        assert random_pseudo_regret(means, actions) == decomposition(means, actions)


def test_expected_decomposition_by_enumeration() -> None:
    # Lemma 4.5 of Lattimore and Szepesvari, with exact expectations.
    means = [F(3, 5), F(2, 5)]
    r = exact_regrets(explore_then_commit(1), means, 4)
    assert r["counts"] == [F(67, 25), F(33, 25)]
    assert r["regret"] == r["decomposition"] == F(33, 125)
    # E[T_1(4)] = 1 + 2 * P(arm 0 gives 0 and arm 1 gives 1) = 1 + 2 * 4/25.
    assert r["counts"][1] == 1 + 2 * F(2, 5) * F(2, 5)
    for m, n in [(2, 4), (1, 5)]:
        r = exact_regrets(explore_then_commit(m), means, n)
        assert r["regret"] == r["decomposition"]
        assert sum(r["counts"]) == n


def test_expected_regret_is_at_least_pseudo_regret() -> None:
    means = [F(3, 5), F(2, 5)]
    for m, n in [(1, 4), (2, 4), (1, 5)]:
        r = exact_regrets(explore_then_commit(m), means, n)
        assert r["expected_regret"] >= r["regret"]
    r = exact_regrets(explore_then_commit(1), means, 4)
    assert r["expected_regret"] == F(38801, 78125)


def test_seeded_run_commits_to_worse_arm() -> None:
    means = [F(3, 5), F(2, 5)]
    actions, rewards = run(explore_then_commit(2), means, 10, random.Random(7))
    assert actions == [0, 1, 0, 1, 1, 1, 1, 1, 1, 1]
    assert random_pseudo_regret(means, actions) == F(8, 5)
    assert sum(rewards) == 6
