# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/c-scan/. The authors are listed in prov/PAACQ9.jsonl.

"""C-SCAN (circular SCAN) disk scheduling.

Cylinders are 0 .. disk_size - 1. The head serves requests only while it
moves in `direction` (+1 toward higher cylinders, or -1). At the end of the
disk it returns to the other end without serving and starts a new sweep. A
request at the head cylinder counts as ahead.
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
        behind = sorted(x for x in requests if x < head)  # @line L2
    else:
        ahead = sorted((x for x in requests if x <= head), reverse=True)
        behind = sorted((x for x in requests if x > head), reverse=True)
    return ahead, behind


def c_scan_order(requests: Sequence[int], head: int, direction: int, disk_size: int) -> list[int]:
    """Service order of C-SCAN on a static batch."""
    _check(requests, head, direction, disk_size)
    ahead, behind = _split(requests, head, direction)
    return ahead + behind  # @line L5


def c_scan_path(requests: Sequence[int], head: int, direction: int, disk_size: int) -> list[int]:
    """Stops of the head, with the two disk ends of the return jump when there is one."""
    _check(requests, head, direction, disk_size)
    ahead, behind = _split(requests, head, direction)
    ends = [disk_size - 1, 0] if direction == UP else [0, disk_size - 1]  # @line L3
    jump = ends if behind else []  # @line L4
    return [head] + ahead + jump + behind


def c_scan_cost(
    requests: Sequence[int], head: int, direction: int, disk_size: int, count_return: bool = True
) -> int:
    """Total head movement of C-SCAN on a static batch.

    The return jump from one end to the other is disk_size - 1 cylinders.
    Whether it counts is a convention; count_return chooses it.
    """
    path = c_scan_path(requests, head, direction, disk_size)
    total = movement(path)
    if not count_return and any(x < head if direction == UP else x > head for x in requests):
        total -= disk_size - 1
    return total


def c_scan_simulate(
    arrivals: Sequence[tuple[int, int]],
    head: int,
    direction: int,
    disk_size: int,
    service: int = 0,
    return_ticks: int | None = None,
) -> list[int]:
    """Dynamic C-SCAN on a simulated clock. Returns the finish time of each request.

    arrivals[k] = (arrival time, cylinder). Each tick the head serves the
    pending requests at its cylinder (each takes `service` ticks; with 0 all
    of them finish at once) or moves one cylinder in `direction`. At the end
    of the disk it jumps to the other end and serves nothing on the way. The
    jump takes `return_ticks` ticks; the default disk_size - 1 is the time of
    a full sweep. With no pending request the head waits.
    """
    _check([c for _, c in arrivals], head, direction, disk_size)
    if return_ticks is None:
        return_ticks = disk_size - 1
    if service < 0 or return_ticks < 0 or any(t < 0 for t, _ in arrivals):
        raise ValueError("times must be nonnegative")
    n = len(arrivals)
    by_time = sorted(range(n), key=lambda k: (arrivals[k][0], k))
    pending: dict[int, deque[int]] = {}
    finish = [-1] * n
    t = nxt = done = 0
    p, d = head, direction
    last = disk_size - 1 if d == UP else 0
    first = disk_size - 1 - last
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
        if p == last:
            p = first
            t += return_ticks
        else:
            p += d
            t += 1
    return finish
