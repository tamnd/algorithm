# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/islip/. The authors are listed in prov/QBWMZS.jsonl.

"""iSLIP, the round-robin crossbar scheduler of McKeown (1999), and RRM.

The scheduler keeps a grant pointer g[j] at each output and an accept
pointer a[i] at each input. Each iteration:

1. Request: each unmatched input requests each unmatched output it has a cell for.
2. Grant: each unmatched output grants the requesting input that comes first
   in round-robin order, starting at g[j].
3. Accept: each input that got grants accepts the output that comes first in
   round-robin order, starting at a[i].

iSLIP moves g[j] to one past the granted input and a[i] to one past the
accepted output, only for an accepted grant, and only in the first iteration.
RRM (round-robin matching) moves g[j] past the granted input whether or not
the grant is accepted, and a[i] past the accepted output, in every iteration.
"""

import random


def first_from(pointer: int, candidates: list[int], n: int) -> int:
    """The candidate that comes first in the order pointer, pointer + 1, ... mod n."""
    return min(candidates, key=lambda x: (x - pointer) % n)


class Scheduler:
    def __init__(self, n: int, iterations: int = 1, rrm: bool = False) -> None:
        self.n = n
        self.iterations = iterations
        self.rrm = rrm
        self.g = [0] * n  # grant pointer of each output
        self.a = [0] * n  # accept pointer of each input

    def schedule(self, req: list[list[bool]]) -> list[int]:
        """One time slot: return match[i] = output of input i, or -1."""
        n = self.n
        in_match = [-1] * n
        out_match = [-1] * n
        for it in range(self.iterations):  # @line L1
            requests: list[list[int]] = [[] for _ in range(n)]
            for i in range(n):  # @line L2
                if in_match[i] < 0:
                    for j in range(n):
                        if out_match[j] < 0 and req[i][j]:
                            requests[j].append(i)
            grants: list[list[int]] = [[] for _ in range(n)]
            granted_to = [-1] * n
            for j in range(n):  # @line L3
                if requests[j]:
                    i = first_from(self.g[j], requests[j], n)  # @line L4
                    grants[i].append(j)
                    granted_to[j] = i
            for i in range(n):  # @line L5
                if grants[i]:
                    j = first_from(self.a[i], grants[i], n)  # @line L6
                    in_match[i] = j  # @line L7
                    out_match[j] = i
                    if self.rrm or it == 0:  # @line L8
                        self.a[i] = (j + 1) % n  # @line L9
                        if not self.rrm:
                            self.g[j] = (i + 1) % n  # @line L10
            if self.rrm:
                for j in range(n):
                    if granted_to[j] >= 0:
                        self.g[j] = (granted_to[j] + 1) % n
            if all(not r for r in requests):
                break
        return in_match  # @line L11


def saturated_run(sched: Scheduler, slots: int) -> list[int]:
    """Every VOQ is always backlogged. Returns the matching size of each slot."""
    full = [[True] * sched.n for _ in range(sched.n)]
    return [sum(1 for j in sched.schedule(full) if j >= 0) for _ in range(slots)]


def bernoulli_run(
    sched: Scheduler, load: float, slots: int, rng: random.Random, q: list[list[int]] | None = None
) -> tuple[int, int, int]:
    """VOQ switch with Bernoulli(load) arrivals and uniform outputs.

    q holds the VOQ lengths and is updated in place, so that a run can go on.
    Returns (arrivals, departures, cells left at the end).
    """
    n = sched.n
    if q is None:
        q = [[0] * n for _ in range(n)]
    arrivals = departures = 0
    for _ in range(slots):
        match = sched.schedule([[q[i][j] > 0 for j in range(n)] for i in range(n)])
        for i, j in enumerate(match):
            if j >= 0:
                q[i][j] -= 1
                departures += 1
        for i in range(n):
            if rng.random() < load:
                q[i][rng.randrange(n)] += 1
                arrivals += 1
    return arrivals, departures, sum(map(sum, q))
