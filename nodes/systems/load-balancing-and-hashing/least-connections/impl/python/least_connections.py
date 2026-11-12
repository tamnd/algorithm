# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-connections/. The authors are listed in prov/MKYZP0.jsonl.

"""Least connections load balancing (join the shortest queue).

LeastConnections keeps the number of active connections a[j] of each backend.
pick() returns the first backend that is up with the smallest a[j] and counts
the new connection; done(j) counts a closed one. Cost: Theta(n) per pick,
Theta(1) per done, Theta(n) space.

The module also has a discrete-event model of n FCFS servers with immediate
dispatch, used to compare least connections (JSQ) with random and round robin.
"""

import random
from collections import deque
from typing import Callable, List, Optional, Sequence


class LeastConnections:
    """Pick the backend with the fewest active connections. Ties go to the lowest index."""

    def __init__(self, n: int) -> None:
        self.a = [0] * n
        self.up = [True] * n

    def pick(self) -> Optional[int]:
        best = None  # @line L1
        for j in range(len(self.a)):  # @line L2
            if self.up[j] and (best is None or self.a[j] < self.a[best]):  # @line L3
                best = j
        if best is not None:  # @line L4
            self.a[best] += 1
        return best  # @line L5

    def done(self, j: int) -> None:
        if self.a[j] <= 0:
            raise ValueError("no active connection on this backend")
        self.a[j] -= 1  # @line L6


Policy = Callable[[List[int]], int]


def fcfs_farm(policy: Policy, arrivals: Sequence[float], sizes: Sequence[float],
              n: int) -> List[float]:
    """Response times of n unit-speed FCFS servers; policy(active) returns a server index.

    active[j] is the number of requests in the system at server j (queued or in
    service) at the arrival time. This is exactly the active connection count
    that a least-connections balancer keeps. Cost: O(m n) for m requests.
    """
    finish: List[deque] = [deque() for _ in range(n)]
    last = [0.0] * n
    out = []
    for t, s in zip(arrivals, sizes):
        for q in finish:
            while q and q[0] <= t:
                q.popleft()
        j = policy([len(q) for q in finish])
        last[j] = max(t, last[j]) + s
        finish[j].append(last[j])
        out.append(last[j] - t)
    return out


def jsq_policy(active: List[int]) -> int:
    """Least connections as a farm policy, through the class above."""
    lc = LeastConnections(len(active))
    lc.a = list(active)
    return lc.pick()


def poisson_arrivals(rng: random.Random, rate: float, m: int) -> List[float]:
    t, out = 0.0, []
    for _ in range(m):
        t += rng.expovariate(rate)
        out.append(t)
    return out


def erlang_m1_response(n: int, rho: float, mu: float = 1.0) -> float:
    """Mean response time of an E_n/M/1 queue: round robin over n servers of a Poisson stream.

    Each server sees Erlang-n gaps with phase rate n * rho * mu. sigma solves
    sigma = (L / (L + mu (1 - sigma)))^n with L = n rho mu, found by fixed-point
    iteration; the mean response time is 1 / (mu (1 - sigma)).
    """
    lam = n * rho * mu
    s = 0.5
    for _ in range(10000):
        s = (lam / (lam + mu * (1 - s))) ** n
    return 1 / (mu * (1 - s))
