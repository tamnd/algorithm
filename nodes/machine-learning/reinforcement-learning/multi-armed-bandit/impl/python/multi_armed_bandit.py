# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-armed-bandit/. The authors are listed in prov/J62NE6.jsonl.

"""The stochastic K-armed Bernoulli bandit, its regret and the regret decomposition.

A policy is a function policy(t, counts, sums) that returns an arm in
range(K). It sees the round t (1-based), the number of pulls of each arm and
the sum of the rewards of each arm. The functions below run a policy on a
bandit and compute the regret, either on one seeded run or exactly, by
enumeration of all reward tables.
"""

import itertools
import random
from fractions import Fraction
from typing import Callable, Sequence

Policy = Callable[[int, list[int], list], int]


def explore_then_commit(m: int) -> Policy:
    """Pull each arm m times in turn, then commit to the arm with the best mean.

    The choice is made once, after round m * K, and kept to the end. Ties go
    to the arm with the lowest index. The policy is deterministic; it resets
    its state when t = 1, so one policy object can be run many times.
    """
    state = {"arm": 0}

    def policy(t: int, counts: list[int], sums: list) -> int:
        k = len(counts)
        if t <= m * k:
            return (t - 1) % k
        if t == m * k + 1:
            best = 0
            for i in range(1, k):
                if sums[i] > sums[best]:  # equal counts m, so compare the sums
                    best = i
            state["arm"] = best
        return state["arm"]

    return policy


def run(policy: Policy, means: Sequence, n: int, rng: random.Random) -> tuple[list[int], list[int]]:
    """Run the policy for n rounds on Bernoulli arms. Return (actions, rewards)."""
    k = len(means)
    counts, sums = [0] * k, [0] * k
    actions, rewards = [], []
    for t in range(1, n + 1):
        a = policy(t, counts, sums)
        x = 1 if rng.random() < means[a] else 0
        counts[a] += 1
        sums[a] += x
        actions.append(a)
        rewards.append(x)
    return actions, rewards


def gaps(means: Sequence) -> list:
    best = max(means)
    return [best - m for m in means]


def random_pseudo_regret(means: Sequence, actions: Sequence[int]) -> object:
    """n * mu_star minus the sum of the means of the pulled arms."""
    return len(actions) * max(means) - sum(means[a] for a in actions)


def decomposition(means: Sequence, actions: Sequence[int]) -> object:
    """sum_i Delta_i T_i(n) with the realized counts T_i(n)."""
    counts = [0] * len(means)
    for a in actions:
        counts[a] += 1
    return sum(d * c for d, c in zip(gaps(means), counts))


def exact_regrets(policy: Policy, means: Sequence[Fraction], n: int) -> dict:
    """Exact expectations for a deterministic policy, by enumeration.

    The model is the time indexed reward table: X[i][t] for each arm i and
    round t, all independent, X[i][t] = 1 with probability means[i]. The
    policy sees X[a][t] only for the arm a that it pulls in round t.
    Returns the exact regret n * mu_star - E[sum_t X_t], the expected counts
    E[T_i(n)], the decomposition sum_i Delta_i E[T_i(n)], and the expected
    regret E[max_i sum_t X[i][t] - sum_t X_t] against the best arm in hindsight.
    """
    k = len(means)
    exp_reward = Fraction(0)
    exp_counts = [Fraction(0)] * k
    exp_best_hindsight = Fraction(0)
    for bits in itertools.product((0, 1), repeat=k * n):
        table = [bits[i * n:(i + 1) * n] for i in range(k)]
        p = Fraction(1)
        for i in range(k):
            for x in table[i]:
                p *= means[i] if x else 1 - means[i]
        counts, sums = [0] * k, [0] * k
        total = 0
        for t in range(1, n + 1):
            a = policy(t, counts, sums)
            x = table[a][t - 1]
            counts[a] += 1
            sums[a] += x
            total += x
        exp_reward += p * total
        exp_best_hindsight += p * max(sum(row) for row in table)
        for i in range(k):
            exp_counts[i] += p * counts[i]
    regret = n * max(means) - exp_reward
    return {
        "regret": regret,
        "counts": exp_counts,
        "decomposition": sum(d * c for d, c in zip(gaps(means), exp_counts)),
        "expected_regret": exp_best_hindsight - exp_reward,
    }
