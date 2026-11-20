# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shapley-value-sampling/. The authors are listed in prov/SB0VDK.jsonl.
"""Monte Carlo estimation of the Shapley value by sampling orders of the players.

A TU game on the players 0 to n - 1 is a function v from frozensets to numbers with
v(frozenset()) == 0. The estimate of each player is the average of its marginal
contribution over m orders drawn uniformly at random.
"""

import math
from typing import Callable, Hashable


def shapley_sampling(n: int, v: Callable[[frozenset], float], m: int, rng) -> list[float]:
    """Estimate the Shapley values of v from m random orders.

    rng is a random.Random instance (or any object with a shuffle method). The function calls
    v exactly n m times. The estimates sum to v(N) up to rounding, because the marginal
    contributions along one order sum to v(N).
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    total = [0] * n  # @line L1
    for _ in range(m):  # @line L2
        order = list(range(n))
        rng.shuffle(order)  # @line L3: a uniform random order (Fisher-Yates)
        members: set[Hashable] = set()
        prev = 0  # @line L4: v of the empty coalition
        for i in order:  # @line L5
            members.add(i)  # @line L6
            cur = v(frozenset(members))  # @line L7
            total[i] += cur - prev  # @line L8
            prev = cur  # @line L9
    return [t / m for t in total]  # @line L10


def samples_needed(r: float, eps: float, delta: float, players: int = 1) -> int:
    """The number m of orders that the Hoeffding bound asks for.

    If every marginal contribution of a player lies in an interval of length r, then with
    m >= r^2 ln(2 players / delta) / (2 eps^2) orders, all the given players are within eps of
    their Shapley values at the same time, with probability at least 1 - delta.
    """
    if r < 0 or eps <= 0 or not 0 < delta < 1 or players < 1:
        raise ValueError("need r >= 0, eps > 0, 0 < delta < 1 and players >= 1")
    return max(1, math.ceil(r * r * math.log(2 * players / delta) / (2 * eps * eps)))


def hoeffding_failure_bound(r: float, eps: float, m: int) -> float:
    """The Hoeffding bound 2 exp(-2 m eps^2 / r^2) on P(|estimate - phi_i| >= eps) for one player."""
    if r == 0:
        return 0.0
    return min(1.0, 2 * math.exp(-2 * m * eps * eps / (r * r)))
