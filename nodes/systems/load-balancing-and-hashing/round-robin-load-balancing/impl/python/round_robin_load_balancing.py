# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/round-robin-load-balancing/. The authors are listed in prov/JZRZJJ.jsonl.

"""Round-robin load balancing.

The balancer keeps one index i. Request k goes to backend i, and i moves to
(i + 1) mod n. Backends that are marked down are skipped. A pick costs O(1)
when all backends are up and O(n) in the worst case, and the state is one
index plus the up flags.

The module also holds a small discrete-event model of a server farm: each
backend is one FCFS server, and the balancer sends each request at its arrival
time. It is used to compare round robin with other policies.
"""

import random
from collections import deque
from typing import Callable, List, Optional, Sequence


class RoundRobin:
    """Cyclic choice over n backends. Precondition: n >= 0."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.i = 0
        self.up = [True] * n

    def pick(self) -> Optional[int]:
        """Return the next backend that is up, or None when all are down."""
        for _ in range(self.n):  # @line L1
            j = self.i  # @line L2
            self.i = (self.i + 1) % self.n  # @line L3
            if self.up[j]:  # @line L4
                return j
        return None  # @line L5


Policy = Callable[[List[int]], int]


def fcfs_farm(policy: Policy, arrivals: Sequence[float], sizes: Sequence[float], n: int,
              speeds: Optional[Sequence[float]] = None) -> List[float]:
    """Simulate n FCFS servers with immediate dispatch.

    policy(active) gets the number of requests in the system at each server at
    the arrival time and returns a server index. Request k arrives at
    arrivals[k] (non-decreasing) and needs sizes[k] units of work; server j
    does speeds[j] units per time unit. Returns the response time of each
    request. Cost: O(m) amortized for m requests, plus the cost of the policy.
    """
    speeds = list(speeds) if speeds is not None else [1.0] * n
    finish: List[deque] = [deque() for _ in range(n)]  # finish times, in order, per server
    last = [0.0] * n
    out = []
    for t, s in zip(arrivals, sizes):
        for q in finish:
            while q and q[0] <= t:
                q.popleft()
        j = policy([len(q) for q in finish])
        start = max(t, last[j])
        done = start + s / speeds[j]
        last[j] = done
        finish[j].append(done)
        out.append(done - t)
    return out


def poisson_arrivals(rng: random.Random, rate: float, m: int) -> List[float]:
    """m arrival times of a Poisson process with the given rate."""
    t, out = 0.0, []
    for _ in range(m):
        t += rng.expovariate(rate)
        out.append(t)
    return out


def pareto_sizes(rng: random.Random, alpha: float, mean: float, m: int) -> List[float]:
    """m Pareto sizes with shape alpha > 1, scaled to the given mean."""
    xm = mean * (alpha - 1) / alpha
    return [xm * rng.paretovariate(alpha) for _ in range(m)]


def percentile(xs: Sequence[float], p: float) -> float:
    """The nearest-rank p-th percentile, 0 < p <= 100."""
    ys = sorted(xs)
    k = max(1, -(-len(ys) * p // 100))
    return ys[int(k) - 1]
