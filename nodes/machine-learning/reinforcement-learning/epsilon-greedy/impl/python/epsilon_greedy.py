# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epsilon-greedy/. The authors are listed in prov/PHHMGW.jsonl.

"""Epsilon-greedy for the stochastic K-armed bandit.

The exploration rate is a schedule eps(t) for t = 1, 2, ... A constant
schedule gives the textbook rule. The schedule of Auer, Cesa-Bianchi and
Fischer (2002), eps_t = min(1, c K / (d^2 t)), is the epsilon_n-greedy rule
of their Theorem 3. The schedule eps = 0 is the pure greedy rule.
"""

import math
import random
from fractions import Fraction
from typing import Callable, Sequence

Schedule = Callable[[int], float]


def constant(eps: float) -> Schedule:
    return lambda t: eps


def auer_schedule(c, d, k: int) -> Schedule:
    """eps_t = min(1, c K / (d^2 t)); d is a lower bound on the smallest positive gap."""
    return lambda t: min(1, c * k / (d * d * t))


def greedy_arm(counts: Sequence[int], sums: Sequence[float]) -> int:
    """The arm with the largest mean; an arm never pulled counts as +infinity.

    Ties go to the smallest index.
    """
    best, best_q = 0, -math.inf
    for i, (n_i, s_i) in enumerate(zip(counts, sums)):
        q = math.inf if n_i == 0 else s_i / n_i
        if q > best_q:
            best, best_q = i, q
    return best


def epsilon_greedy(
    pull: Callable[[int], float], k: int, n: int, schedule: Schedule, rng: random.Random
) -> tuple[list[int], list[float]]:
    """Run epsilon-greedy for n rounds. pull(a) returns a reward of arm a."""
    counts, sums = [0] * k, [0.0] * k  # @line L1
    actions, rewards = [], []
    for t in range(1, n + 1):  # @line L2
        if rng.random() < schedule(t):  # @line L3
            a = rng.randrange(k)  # @line L4
        else:
            a = greedy_arm(counts, sums)  # @line L5
        x = pull(a)  # @line L6
        counts[a] += 1  # @line L7
        sums[a] += x
        actions.append(a)
        rewards.append(x)
    return actions, rewards


def bernoulli_arms(means: Sequence[float], rng: random.Random) -> Callable[[int], int]:
    return lambda a: 1 if rng.random() < means[a] else 0


def regret(means: Sequence[float], actions: Sequence[int]) -> float:
    """The random pseudo-regret sum_t (mu_star - mu_{A_t})."""
    best = max(means)
    return sum(best - means[a] for a in actions)


def mean_regret(means, n, schedule, seeds) -> float:
    total = 0.0
    for s in seeds:
        env_rng, alg_rng = random.Random(10_000 + s), random.Random(s)
        actions, _ = epsilon_greedy(bernoulli_arms(means, env_rng), len(means), n, schedule, alg_rng)
        total += regret(means, actions)
    return total / len(seeds)


def schedule_values(c: Fraction, d: Fraction, k: int, ts: Sequence[int]) -> list[Fraction]:
    """Exact values of the Auer schedule, for checks with fractions."""
    f = auer_schedule(c, d, k)
    return [Fraction(f(t)) for t in ts]
