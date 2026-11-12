# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exp3/. The authors are listed in prov/N3XXFK.jsonl.

"""Exp3 of Auer, Cesa-Bianchi, Freund and Schapire (2002) for adversarial bandits."""

import math
import random
from typing import Callable, Sequence


def distribution(weights: Sequence, gamma) -> list:
    """p_i = (1 - gamma) w_i / W + gamma / K. Works with floats or Fractions."""
    k = len(weights)
    total = sum(weights)
    return [(1 - gamma) * w / total + gamma / k for w in weights]


def estimates(p: Sequence, a: int, x) -> list:
    """Importance-weighted estimate of the whole reward vector: x / p_a at arm a, 0 elsewhere."""
    return [x / p[a] if i == a else 0 * x for i in range(len(p))]


def optimal_gamma(k: int, g: float) -> float:
    """Corollary 3.2: gamma = min(1, sqrt(K ln K / ((e - 1) g))) for an upper bound g on G_max."""
    return min(1.0, math.sqrt(k * math.log(k) / ((math.e - 1) * g)))


def regret_bound(k: int, g: float) -> float:
    """Corollary 3.2: G_max - E[G_Exp3] <= 2 sqrt(e - 1) sqrt(g K ln K) when g >= G_max."""
    return 2 * math.sqrt(math.e - 1) * math.sqrt(g * k * math.log(k))


def exp3(
    reward: Callable[[int, int], float],
    k: int,
    n: int,
    gamma: float,
    rng: random.Random,
    trace: list | None = None,
) -> tuple[list[int], list[float]]:
    """Run Exp3 for n rounds. reward(t, a) in [0, 1] is the reward of arm a in round t.

    The weights are kept as logarithms, so that they do not overflow.
    """
    log_w = [0.0] * k  # @line L1
    actions, rewards = [], []
    for t in range(n):  # @line L2
        top = max(log_w)
        p = distribution([math.exp(v - top) for v in log_w], gamma)  # @line L3
        a = rng.choices(range(k), weights=p)[0]  # @line L4
        x = reward(t, a)  # @line L5
        x_hat = x / p[a]  # @line L6
        log_w[a] += gamma * x_hat / k  # @line L7
        if trace is not None:
            trace.append((p, a, x, x_hat))
        actions.append(a)
        rewards.append(x)
    return actions, rewards


def table_rewards(table: Sequence[Sequence[float]]) -> Callable[[int, int], float]:
    """An oblivious adversary: the reward table is fixed before the run."""
    return lambda t, a: table[t][a]


def best_fixed_arm_total(table: Sequence[Sequence[float]]) -> float:
    k = len(table[0])
    return max(sum(row[i] for row in table) for i in range(k))
