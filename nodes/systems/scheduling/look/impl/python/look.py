# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/look/. The authors are listed in prov/6RZ6QE.jsonl.

"""LOOK disk scheduling: SCAN that reverses at the last pending request.

Cylinders are 0 .. disk_size - 1. A direction is +1 (toward higher
cylinders) or -1. A request at the head cylinder counts as ahead.
"""

from collections import deque
from collections.abc import Sequence

UP, DOWN = 1, -1


def _check(requests: Sequence[int], head: int, direction: int, disk_size: int) -> None:
    if direction not in (UP, DOWN):
        raise ValueError("direction must be +1 or -1")
    if not 0 <= head < disk_size or any(not 0 <= x < disk_size for x in requests):
        raise ValueError("cylinders must be in 0 .. disk_size - 1")


def movement(path: Sequence[int]) -> int:
    """Length of a head path: the sum of the distances between stops."""
    return sum(abs(b - a) for a, b in zip(path, path[1:]))


def look_order(requests: Sequence[int], head: int, direction: int, disk_size: int) -> list[int]:
    """Service order of LOOK on a static batch. The head turns at the last request."""
    _check(requests, head, direction, disk_size)
    if direction == UP:
        ahead = sorted(x for x in requests if x >= head)  # @line L1
        behind = sorted((x for x in requests if x < head), reverse=True)  # @line L2
    else:
        ahead = sorted((x for x in requests if x <= head), reverse=True)
        behind = sorted(x for x in requests if x > head)
    return ahead + behind  # @line L3


def look_cost(requests: Sequence[int], head: int, direction: int, disk_size: int) -> int:
    """Total head movement of LOOK on a static batch, in cylinders."""
    return movement([head] + look_order(requests, head, direction, disk_size))


def offline_optimum(requests: Sequence[int], head: int) -> int:
    """Least total head movement over all service orders: (hi - lo) + min(|head - lo|, |head - hi|)."""
    if not requests:
        return 0
    lo, hi = min(requests), max(requests)
    return (hi - lo) + min(abs(head - lo), abs(head - hi))


def look_simulate(
    arrivals: Sequence[tuple[int, int]], head: int, direction: int, disk_size: int, service: int = 0
) -> list[int]:
    """Dynamic LOOK on a simulated clock. Returns the finish time of each request.

    arrivals[k] = (arrival time, cylinder). Each tick the head serves the
    pending requests at its cylinder (each takes `service` ticks; with 0 all
    of them finish at once) or moves one cylinder. It reverses when no
    pending request lies ahead. With no pending request the head waits.
    """
    _check([c for _, c in arrivals], head, direction, disk_size)
    if service < 0 or any(t < 0 for t, _ in arrivals):
        raise ValueError("times must be nonnegative")
    n = len(arrivals)
    by_time = sorted(range(n), key=lambda k: (arrivals[k][0], k))
    pending: dict[int, deque[int]] = {}
    finish = [-1] * n
    t = nxt = done = 0
    p, d = head, direction
    while done < n:
        while nxt < n and arrivals[by_time[nxt]][0] <= t:
            k = by_time[nxt]
            pending.setdefault(arrivals[k][1], deque()).append(k)
            nxt += 1
        if not pending:
            t = arrivals[by_time[nxt]][0]
            continue
        if p in pending:
            q = pending[p]
            if service == 0:
                while q:
                    finish[q.popleft()] = t
                    done += 1
            else:
                t += service
                finish[q.popleft()] = t
                done += 1
            if not q:
                del pending[p]
            continue
        if not any((c - p) * d > 0 for c in pending):
            d = -d
        p += d
        t += 1
    return finish
