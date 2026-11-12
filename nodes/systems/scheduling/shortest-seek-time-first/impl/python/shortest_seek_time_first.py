# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shortest-seek-time-first/. The authors are listed in prov/PME9E7.jsonl.

"""Shortest seek time first (SSTF) disk scheduling.

Cylinders are the integers 0 .. disk_size - 1. A direction is +1 (toward
higher cylinders) or -1. Tie rule: when the nearest pending requests lie at
the same distance on both sides of the head, SSTF keeps the direction of its
last move (at the start, the direction that the caller gives).
"""

from bisect import bisect_left
from collections import deque
from collections.abc import Sequence

UP, DOWN = 1, -1


def _check(requests: Sequence[int], head: int, direction: int, disk_size: int) -> None:
    if direction not in (UP, DOWN):
        raise ValueError("direction must be +1 or -1")
    if not 0 <= head < disk_size or any(not 0 <= x < disk_size for x in requests):
        raise ValueError("cylinders must be in 0 .. disk_size - 1")


def head_movement(order: Sequence[int], head: int) -> int:
    """Total head movement, in cylinders, to serve `order` from `head`."""
    total, p = 0, head
    for x in order:
        total += abs(x - p)
        p = x
    return total


def sstf_order(requests: Sequence[int], head: int, direction: int, disk_size: int) -> list[int]:
    """Service order of SSTF on a static batch, in O(n log n) time.

    The served requests always form a run of the sorted array around the
    start, so the nearest pending request is A[i] or A[j].
    """
    _check(requests, head, direction, disk_size)
    a = sorted(requests)  # @line L1
    n = len(a)
    i = bisect_left(a, head) - 1  # @line L2: a[i] < head <= a[j]
    j = i + 1
    p, d, out = head, direction, []  # @line L3
    while i >= 0 or j < n:  # @line L4
        dl = p - a[i] if i >= 0 else None  # @line L5
        du = a[j] - p if j < n else None  # @line L6
        if dl is None or (du is not None and (du < dl or (du == dl and d == UP))):  # @line L7
            x = a[j]
            j += 1
        else:  # @line L8
            x = a[i]
            i -= 1
        if x != p:  # @line L9
            d = UP if x > p else DOWN
        p = x  # @line L10
        out.append(x)
    return out  # @line L11


def sstf_cost(requests: Sequence[int], head: int, direction: int, disk_size: int) -> int:
    """Total head movement of SSTF on a static batch."""
    return head_movement(sstf_order(requests, head, direction, disk_size), head)


def _nearest(pending: dict[int, deque[int]], p: int, d: int) -> int:
    best = None
    for c in pending:
        if best is None or abs(c - p) < abs(best - p) or (abs(c - p) == abs(best - p) and (c - p) * d > 0):
            best = c
    assert best is not None
    return best


def sstf_simulate(
    arrivals: Sequence[tuple[int, int]], head: int, direction: int, disk_size: int, service: int = 0
) -> list[int]:
    """Dynamic SSTF on a simulated clock. Returns the finish time of each request.

    arrivals[k] = (arrival time, cylinder). Each tick the head serves the
    pending requests at its cylinder (each takes `service` ticks; with 0 all
    of them finish at once) or moves one cylinder toward the nearest pending
    request. With no pending request the head waits.
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
        target = _nearest(pending, p, d)
        d = UP if target > p else DOWN
        p += d
        t += 1
    return finish
