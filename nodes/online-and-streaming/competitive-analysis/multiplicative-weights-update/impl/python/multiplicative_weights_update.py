# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiplicative-weights-update/. The authors are listed in prov/F0X9Y9.jsonl.

"""Multiplicative weights (Arora, Hazan and Kale) and Hedge (Freund and Schapire).

costs[t][i] is the cost of expert i in round t. The linear update
w <- w * (1 - eta * m) runs in exact Fraction arithmetic for costs in
[-1, 1]. Hedge uses w <- w * exp(-eta * l) for losses in [0, 1] and works
with floats in log space.
"""

import math
from fractions import Fraction


def multiplicative_weights_update(
    costs: list[list[Fraction]], eta: Fraction
) -> tuple[Fraction, list[list[Fraction]]]:
    """Run MWU with the linear update. Return the expected total cost and each p_t.

    Needs 0 < eta <= 1/2 and costs in [-1, 1]. Cost: O(n) per round.
    """
    if not 0 < eta <= Fraction(1, 2):
        raise ValueError("eta must be in (0, 1/2]")
    n = len(costs[0]) if costs else 0
    w = [Fraction(1)] * n  # @line L1
    total = Fraction(0)
    probs: list[list[Fraction]] = []
    for m in costs:  # @line L2
        if len(m) != n or any(not -1 <= x <= 1 for x in m):
            raise ValueError("each round needs n costs in [-1, 1]")
        phi = sum(w, Fraction(0))  # @line L3
        p = [x / phi for x in w]
        probs.append(p)  # @line L4
        total += sum((pi * mi for pi, mi in zip(p, m)), Fraction(0))  # @line L5
        w = [wi * (1 - eta * mi) for wi, mi in zip(w, m)]  # @line L6
    return total, probs


def hedge(losses: list[list[float]], eta: float) -> tuple[float, list[list[float]]]:
    """Run Hedge with p_{t,i} proportional to exp(-eta * L_{t-1,i}).

    Return the expected total loss and each p_t. The weights are kept as
    logarithms, shifted by their maximum, so they do not underflow.
    Cost: O(n) per round.
    """
    if eta <= 0:
        raise ValueError("eta must be positive")
    n = len(losses[0]) if losses else 0
    logw = [0.0] * n
    total = 0.0
    probs: list[list[float]] = []
    for row in losses:
        if len(row) != n or any(not 0 <= x <= 1 for x in row):
            raise ValueError("each round needs n losses in [0, 1]")
        top = max(logw)
        e = [math.exp(x - top) for x in logw]
        s = sum(e)
        p = [x / s for x in e]
        probs.append(p)
        total += sum(pi * li for pi, li in zip(p, row))
        logw = [lw - eta * li for lw, li in zip(logw, row)]
    return total, probs


def tuned_eta(n: int, t: int) -> float:
    """The rate sqrt(8 ln n / T) that gives regret at most sqrt(T ln n / 2)."""
    return math.sqrt(8 * math.log(n) / t)


def solve_zero_sum(a: list[list[float]], rounds: int) -> tuple[list[float], list[float], float]:
    """Approximate a zero-sum game with payoffs a[i][j] in [0, 1] to the row player.

    The row player runs Hedge on the losses 1 - a[i][j], and the column player
    best responds. Return the average strategies and the average payoff.
    """
    n, k = len(a), len(a[0])
    eta = tuned_eta(max(n, 2), rounds)
    logw = [0.0] * n
    avg_row, avg_col, value = [0.0] * n, [0.0] * k, 0.0
    for _ in range(rounds):
        top = max(logw)
        e = [math.exp(x - top) for x in logw]
        s = sum(e)
        p = [x / s for x in e]
        gains = [sum(p[i] * a[i][j] for i in range(n)) for j in range(k)]
        j = min(range(k), key=lambda c: gains[c])
        value += gains[j]
        avg_col[j] += 1
        for i in range(n):
            avg_row[i] += p[i]
            logw[i] -= eta * (1 - a[i][j])
    return [x / rounds for x in avg_row], [x / rounds for x in avg_col], value / rounds
