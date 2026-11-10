# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/follow-the-leader/. The authors are listed in prov/DKX8AG.jsonl.

"""Follow the leader (FTL) and follow the perturbed leader (FTPL) for experts.

losses[t][i] is the loss of expert i in round t, a Fraction (or float) in
[0, 1]. FTL picks the expert with the least total loss so far, the least
index on ties.
"""

import random
from fractions import Fraction


def follow_the_leader(losses: list[list[Fraction]]) -> tuple[list[int], Fraction]:
    """Return the expert chosen in each round and the total loss of FTL.

    Cost: O(n) per round.
    """
    n = len(losses[0]) if losses else 0
    total_of = [Fraction(0)] * n  # @line L1
    picks: list[int] = []
    paid = Fraction(0)
    for row in losses:  # @line L2
        if len(row) != n:
            raise ValueError("each round needs one loss per expert")
        low = min(total_of)
        i = total_of.index(low)  # @line L3
        picks.append(i)  # @line L4
        paid += row[i]  # @line L5
        total_of = [a + b for a, b in zip(total_of, row)]  # @line L6
    return picks, paid


def best_fixed(losses: list[list[Fraction]]) -> Fraction:
    n = len(losses[0])
    return min(sum((row[i] for row in losses), Fraction(0)) for i in range(n))


def alternating_losses(t: int) -> list[list[Fraction]]:
    """The sequence (1/2, 0), (0, 1), (1, 0), (0, 1), ... on which FTL fails."""
    out = []
    for r in range(t):
        if r == 0:
            out.append([Fraction(1, 2), Fraction(0)])
        elif r % 2 == 1:
            out.append([Fraction(0), Fraction(1)])
        else:
            out.append([Fraction(1), Fraction(0)])
    return out


def follow_the_perturbed_leader(losses: list[list[float]], eps: float, rng: random.Random) -> tuple[list[int], float]:
    """FTPL of Kalai and Vempala with a fresh perturbation in each round.

    The perturbation is uniform on [0, 1/eps]^n and is subtracted from the
    totals, so a large draw favors an expert. Cost: O(n) per round.
    """
    if eps <= 0:
        raise ValueError("eps must be positive")
    n = len(losses[0]) if losses else 0
    total_of = [0.0] * n
    picks: list[int] = []
    paid = 0.0
    for row in losses:
        noisy = [total_of[i] - rng.uniform(0, 1 / eps) for i in range(n)]
        i = min(range(n), key=lambda k: noisy[k])
        picks.append(i)
        paid += float(row[i])
        total_of = [a + float(b) for a, b in zip(total_of, row)]
    return picks, paid


def ftl_squared_loss(zs: list[Fraction], start: Fraction = Fraction(1, 2)) -> tuple[list[Fraction], Fraction]:
    """FTL for the losses (x - z_t)^2 on [0, 1]: play the mean of the past z's.

    Return the points played and the regret against the best fixed x in [0, 1],
    which is the mean of all z's. Cost: O(1) per round.
    """
    xs: list[Fraction] = []
    s = Fraction(0)
    for t, z in enumerate(zs):
        xs.append(start if t == 0 else s / t)
        s += z
    if not zs:
        return xs, Fraction(0)
    best = s / len(zs)
    alg = sum(((x - z) ** 2 for x, z in zip(xs, zs)), Fraction(0))
    opt = sum(((best - z) ** 2 for z in zs), Fraction(0))
    return xs, alg - opt
