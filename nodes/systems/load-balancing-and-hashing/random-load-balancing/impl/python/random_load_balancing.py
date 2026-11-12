# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-load-balancing/. The authors are listed in prov/FXC04X.jsonl.

"""Random load balancing: send each request to a server drawn at random.

random_server draws a uniform server. WeightedPicker draws server i with
probability w_i / sum(w) by binary search on prefix sums. round_robin is the
deterministic baseline that the page compares with.
"""

import bisect
import random
from typing import Sequence


def random_server(n: int, rng: random.Random) -> int:
    """RANDOM-DISPATCH: a server index drawn uniformly from 0 .. n - 1."""
    if n < 1:
        raise ValueError("no servers")
    return rng.randrange(n)  # @line L1


def dispatch(n: int, m: int, rng: random.Random) -> list[int]:
    """Send m equal requests to n servers at random. Return the request count of each server."""
    loads = [0] * n
    for _ in range(m):
        loads[random_server(n, rng)] += 1  # @line L2
    return loads


class WeightedPicker:
    """Draw server i with probability w[i] / sum(w), for non-negative weights."""

    def __init__(self, weights: Sequence[float]) -> None:
        if not weights or any(w < 0 for w in weights) or sum(weights) <= 0:
            raise ValueError("weights must be non-negative with a positive sum")
        self.prefix: list[float] = []
        total = 0.0
        for w in weights:
            total += w
            self.prefix.append(total)  # prefix[i] = w[0] + ... + w[i]
        self.total = total

    def pick(self, rng: random.Random) -> int:
        u = rng.random() * self.total  # @line L3
        i = bisect.bisect_right(self.prefix, u)  # @line L4
        return min(i, len(self.prefix) - 1)  # guards u == total after rounding


def weighted_dispatch(weights: Sequence[float], m: int, rng: random.Random) -> list[int]:
    picker = WeightedPicker(weights)
    loads = [0] * len(weights)
    for _ in range(m):
        loads[picker.pick(rng)] += 1
    return loads


def round_robin(n: int, m: int) -> list[int]:
    """Deterministic baseline: request t goes to server t mod n."""
    loads = [0] * n
    for t in range(m):
        loads[t % n] += 1
    return loads


def queue_lengths(n: int, lam: float, steps: int, burn: int, rng: random.Random) -> float:
    """Mean number of jobs per server when Poisson arrivals of rate lam * n go to
    random servers that each serve at rate 1 (uniformized chain). Each server is
    then an M/M/1 queue with mean lam / (1 - lam) jobs."""
    q = [0] * n
    total = 0
    acc = 0
    p_arrival = lam / (lam + 1)
    for t in range(burn + steps):
        if rng.random() < p_arrival:
            q[rng.randrange(n)] += 1
            total += 1
        else:
            j = rng.randrange(n)
            if q[j]:
                q[j] -= 1
                total -= 1
        if t >= burn:
            acc += total
    return acc / (steps * n)
