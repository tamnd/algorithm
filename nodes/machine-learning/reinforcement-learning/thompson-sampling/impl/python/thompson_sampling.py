# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thompson-sampling/. The authors are listed in prov/JKGDPY.jsonl.

"""Thompson sampling with Beta priors for Bernoulli bandits (Agrawal and Goyal 2012)."""

import random
from typing import Callable, Sequence


def thompson_sampling(
    pull: Callable[[int], float],
    k: int,
    n: int,
    rng: random.Random,
    prior: tuple[int, int] = (1, 1),
    trace: list | None = None,
) -> tuple[list[int], list[float], list[int], list[int]]:
    """Run Thompson sampling for n rounds. pull(a) returns a reward of arm a in [0, 1].

    Each arm has a Beta(alpha, beta) posterior on its mean. Each round draws one
    sample from each posterior and pulls the arm with the largest sample. A reward
    x that is not 0 or 1 is turned into a Bernoulli trial with success chance x.
    Returns the actions, the rewards and the final alpha and beta of each arm.
    """
    alpha, beta = [prior[0]] * k, [prior[1]] * k  # @line L1
    actions, rewards = [], []
    for _ in range(n):  # @line L2
        theta = [rng.betavariate(alpha[i], beta[i]) for i in range(k)]  # @line L3
        a = max(range(k), key=lambda i: theta[i])  # @line L4
        x = pull(a)  # @line L5
        y = x if x in (0, 1) else int(rng.random() < x)
        if y == 1:  # @line L6
            alpha[a] += 1
        else:
            beta[a] += 1
        if trace is not None:
            trace.append(theta)
        actions.append(a)
        rewards.append(x)
    return actions, rewards, alpha, beta


def posterior(prior: tuple[int, int], outcomes: Sequence[int]) -> tuple[int, int]:
    """Beta posterior after a sequence of Bernoulli outcomes: Beta(a + s, b + f)."""
    s = sum(outcomes)
    return prior[0] + s, prior[1] + len(outcomes) - s


def bernoulli_arms(means: Sequence[float], rng: random.Random) -> Callable[[int], int]:
    return lambda a: 1 if rng.random() < means[a] else 0


def regret(means: Sequence[float], actions: Sequence[int]) -> float:
    best = max(means)
    return sum(best - means[a] for a in actions)


def mean_regret_curve(means: Sequence[float], checkpoints: Sequence[int], seeds) -> list[float]:
    """Average random pseudo-regret at each checkpoint. Seed s: arms Random(s), policy Random(10000 + s)."""
    n = max(checkpoints)
    best = max(means)
    out = [0.0] * len(checkpoints)
    for s in seeds:
        arms = bernoulli_arms(means, random.Random(s))
        actions, _, _, _ = thompson_sampling(arms, len(means), n, random.Random(10000 + s))
        acc, j = 0.0, 0
        for t, a in enumerate(actions, 1):
            acc += best - means[a]
            while j < len(checkpoints) and checkpoints[j] == t:
                out[j] += acc
                j += 1
    return [v / len(seeds) for v in out]
