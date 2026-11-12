# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scan-algorithm/. The authors are listed in prov/5V7681.jsonl.

"""SCAN (the elevator algorithm) for disk scheduling.

Cylinders are 0 .. disk_size - 1. A direction is +1 (toward higher
cylinders) or -1. The head serves every request in its direction, goes on to
the end of the disk, reverses, and serves the rest. A request at the head
cylinder counts as ahead in both directions.
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


def _split(requests: Sequence[int], head: int, direction: int) -> tuple[list[int], list[int]]:
    if direction == UP:
        ahead = sorted(x for x in requests if x >= head)  # @line L1
        behind = sorted((x for x in requests if x < head), reverse=True)  # @line L2
    else:
        ahead = sorted((x for x in requests if x <= head), reverse=True)
        behind = sorted(x for x in requests if x > head)
    return ahead, behind


def scan_order(requests: Sequence[int], head: int, direction: int, disk_size: int) -> list[int]:
    """Service order of SCAN on a static batch."""
    _check(requests, head, direction, disk_size)
    ahead, behind = _split(requests, head, direction)
    return ahead + behind  # @line L5


def scan_path(requests: Sequence[int], head: int, direction: int, disk_size: int) -> list[int]:
    """Stops of the head: the start, each request, and the disk end where it reverses."""
    _check(requests, head, direction, disk_size)
    ahead, behind = _split(requests, head, direction)
    end = disk_size - 1 if direction == UP else 0  # @line L3
    turn = [end] if behind else []  # @line L4: go to the end only if a request is behind
    return [head] + ahead + turn + behind


def scan_cost(requests: Sequence[int], head: int, direction: int, disk_size: int) -> int:
    """Total head movement of SCAN on a static batch, in cylinders."""
    return movement(scan_path(requests, head, direction, disk_size))


def scan_simulate(
    arrivals: Sequence[tuple[int, int]], head: int, direction: int, disk_size: int, service: int = 0
) -> list[int]:
    """Dynamic SCAN on a simulated clock. Returns the finish time of each request.

    arrivals[k] = (arrival time, cylinder). Each tick the head serves the
    pending requests at its cylinder (each takes `service` ticks; with 0 all
    of them finish at once) or moves one cylinder in its direction, and it
    reverses at the end of the disk. With no pending request the head waits.
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
        if (d == UP and p == disk_size - 1) or (d == DOWN and p == 0):
            d = -d
        p += d
        t += 1
    return finish
