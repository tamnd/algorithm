# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berkeley-algorithm/. The authors are listed in prov/YCTSW0.jsonl.

"""The Berkeley algorithm (Gusella and Zatti, TEMPO in 4.3BSD), in a small
discrete event simulator.

Machine 0 is the master. Machine i has the clock H_i(t) = t + offsets[i]; the
round is short, so drift is left out. Each one-way delay is at least dmin and
is drawn by a seeded generator. The master:

  L1  for each slave i: send a request, note the send time on its own clock
  L2  on each reply (i, T_i): RTT_i <- now - sent_i;
      delta_i <- T_i + RTT_i / 2 - now        (Cristian's estimate of H_i - H_0)
  L3  delta_0 <- 0
  L4  G <- the largest set of deltas whose spread (max - min) is at most gamma
  L5  avg <- the mean of G
  L6  for each machine i: send the correction avg - delta_i (the master applies its own)

Each machine adds its correction to its clock. The master sends corrections,
not times, so the delay of the correction message does not matter.
"""

import heapq
import random
from typing import Callable


def largest_cluster(values: dict[int, float], gamma: float) -> list[int]:
    """The keys of a largest set of values with max - min <= gamma.

    Sort, then slide a window. Ties go to the smaller spread, then to the window
    that starts first. O(k log k) for k values.
    """
    order = sorted(values, key=lambda i: (values[i], i))
    best = (0, 0.0, 0)  # (size, -spread, -start)
    best_range = (0, 0)
    lo = 0
    for hi in range(len(order)):
        while values[order[hi]] - values[order[lo]] > gamma:
            lo += 1
        size = hi - lo + 1
        key = (size, -(values[order[hi]] - values[order[lo]]), -lo)
        if key > best:
            best, best_range = key, (lo, hi)
    lo, hi = best_range
    return order[lo : hi + 1]


def berkeley_round(
    offsets: list[float],
    gamma: float,
    dmin: float,
    delay: Callable[[random.Random], float],
    rng: random.Random,
) -> dict:
    """Run one round. Returns the estimates, the chosen set, the corrections
    and the new offsets of all machines."""
    n = len(offsets)
    clock = lambda i, t: t + offsets[i]  # noqa: E731
    events: list[tuple[float, int, str, int, float]] = []  # (time, seq, kind, machine, value)
    seq = 0
    sent: dict[int, float] = {}
    for i in range(1, n):  # @line L1
        sent[i] = clock(0, 0.0)
        heapq.heappush(events, (0.0 + delay(rng), seq, "request", i, 0.0))
        seq += 1
    delta: dict[int, float] = {0: 0.0}  # @line L3
    rtts: dict[int, float] = {}
    while events:
        t, _, kind, i, value = heapq.heappop(events)
        if kind == "request":  # the slave reads its clock and replies at once
            heapq.heappush(events, (t + delay(rng), seq, "reply", i, clock(i, t)))
            seq += 1
        else:  # @line L2
            now = clock(0, t)
            rtts[i] = now - sent[i]
            delta[i] = value + rtts[i] / 2 - now
    chosen = largest_cluster(delta, gamma)  # @line L4
    avg = sum(delta[i] for i in chosen) / len(chosen)  # @line L5
    corrections = {i: avg - delta[i] for i in range(n)}  # @line L6
    new_offsets = [offsets[i] + corrections[i] for i in range(n)]
    return {
        "delta": delta,
        "rtt": rtts,
        "chosen": sorted(chosen),
        "avg": avg,
        "corrections": corrections,
        "new_offsets": new_offsets,
    }
