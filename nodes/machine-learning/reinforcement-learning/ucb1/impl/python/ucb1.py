# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ucb1/. The authors are listed in prov/WS67AB.jsonl.

"""UCB1 of Auer, Cesa-Bianchi and Fischer (2002) for rewards in [0, 1]."""

import math
import random
from typing import Callable, Sequence


def ucb1(pull: Callable[[int], float], k: int, n: int) -> tuple[list[int], list[float]]:
    """Run UCB1 for n >= k rounds. pull(a) returns a reward of arm a in [0, 1].

    Each arm is pulled once. After that, round t pulls the arm with the
    largest index mean_i + sqrt(2 ln(t - 1) / N_i), where t - 1 is the number
    of pulls so far. Ties go to the smallest index.
    """
    counts, sums = [0] * k, [0.0] * k
    actions, rewards = [], []
    for a in range(k):  # @line L1
        x = pull(a)
        counts[a], sums[a] = 1, x
        actions.append(a)
        rewards.append(x)
    for t in range(k + 1, n + 1):  # @line L2
        log_plays = math.log(t - 1)
        best, best_u = 0, -math.inf
        for i in range(k):  # @line L3
            u = sums[i] / counts[i] + math.sqrt(2 * log_plays / counts[i])
            if u > best_u:  # @line L4
                best, best_u = i, u
        x = pull(best)  # @line L5
        counts[best] += 1  # @line L6
        sums[best] += x
        actions.append(best)
        rewards.append(x)
    return actions, rewards


def ucb1_bound(means: Sequence[float], n: int) -> float:
    """Theorem 1: sum over suboptimal i of 8 ln n / Delta_i, plus (1 + pi^2/3) sum_j Delta_j."""
    best = max(means)
    gaps = [best - m for m in means]
    return 8 * math.log(n) * sum(1 / g for g in gaps if g > 0) + (1 + math.pi**2 / 3) * sum(gaps)


def bernoulli_arms(means: Sequence[float], rng: random.Random) -> Callable[[int], int]:
    return lambda a: 1 if rng.random() < means[a] else 0


def regret(means: Sequence[float], actions: Sequence[int]) -> float:
    best = max(means)
    return sum(best - means[a] for a in actions)


def mean_regret_curve(means: Sequence[float], checkpoints: Sequence[int], seeds) -> list[float]:
    """Average random pseudo-regret at each checkpoint, one run of length max(checkpoints) per seed."""
    n = max(checkpoints)
    out = [0.0] * len(checkpoints)
    for s in seeds:
        actions, _ = ucb1(bernoulli_arms(means, random.Random(s)), len(means), n)
        best = max(means)
        acc, j = 0.0, 0
        for t, a in enumerate(actions, 1):
            acc += best - means[a]
            while j < len(checkpoints) and checkpoints[j] == t:
                out[j] += acc
                j += 1
    return [v / len(seeds) for v in out]
