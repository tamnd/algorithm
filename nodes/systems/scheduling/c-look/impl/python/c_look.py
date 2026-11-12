# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/c-look/. The authors are listed in prov/GARAAY.jsonl.

"""C-LOOK (circular LOOK) disk scheduling.

Cylinders are 0 .. disk_size - 1. The head serves requests only while it
moves in `direction` (+1 toward higher cylinders, or -1). When no pending
request lies ahead, it jumps to the farthest pending request on the other
side and starts a new sweep there. A request at the head cylinder counts as
ahead.
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


def c_look_order(requests: Sequence[int], head: int, direction: int, disk_size: int) -> list[int]:
    """Service order of C-LOOK on a static batch."""
    _check(requests, head, direction, disk_size)
    if direction == UP:
        ahead = sorted(x for x in requests if x >= head)  # @line L1
        behind = sorted(x for x in requests if x < head)  # @line L2
    else:
        ahead = sorted((x for x in requests if x <= head), reverse=True)
        behind = sorted((x for x in requests if x > head), reverse=True)
    return ahead + behind  # @line L3


def c_look_cost(
    requests: Sequence[int], head: int, direction: int, disk_size: int, count_return: bool = True
) -> int:
    """Total head movement of C-LOOK on a static batch.

    The return jump goes from the last request of the first sweep (or the
    start, if no request lies ahead) to the first request of the second
    sweep. Whether it counts is a convention; count_return chooses it.
    """
    order = c_look_order(requests, head, direction, disk_size)
    n_ahead = sum(1 for x in requests if (x >= head if direction == UP else x <= head))
    total = movement([head] + order)
    if not count_return and n_ahead < len(order):
        top = order[n_ahead - 1] if n_ahead else head
        total -= abs(top - order[n_ahead])
    return total


def c_look_simulate(
    arrivals: Sequence[tuple[int, int]],
    head: int,
    direction: int,
    disk_size: int,
    service: int = 0,
    return_ticks: int | None = None,
) -> list[int]:
    """Dynamic C-LOOK on a simulated clock. Returns the finish time of each request.

    arrivals[k] = (arrival time, cylinder). Each tick the head serves the
    pending requests at its cylinder (each takes `service` ticks; with 0 all
    of them finish at once) or moves one cylinder in `direction`. When no
    pending request lies ahead, it jumps to the farthest pending request
    behind and serves nothing on the way. The jump takes `return_ticks`
    ticks, or by default one tick per cylinder of the jump. With no pending
    request the head waits.
    """
    _check([c for _, c in arrivals], head, direction, disk_size)
    if service < 0 or (return_ticks is not None and return_ticks < 0) or any(t < 0 for t, _ in arrivals):
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
        if any((c - p) * d > 0 for c in pending):
            p += d
            t += 1
        else:
            far = min(pending) if d == UP else max(pending)
            t += abs(p - far) if return_ticks is None else return_ticks
            p = far
    return finish
