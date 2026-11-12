# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/disk-scheduling/. The authors are listed in prov/683RCB.jsonl.

"""The disk scheduling problem on a line of cylinders: cost of an order,
first come first served, and the offline optimum of a static batch."""

from collections.abc import Sequence
from itertools import permutations


def head_movement(order: Sequence[int], head: int) -> int:
    """Total head movement, in cylinders, to serve `order` from `head`."""
    total, p = 0, head
    for x in order:
        total += abs(x - p)
        p = x
    return total


def fcfs_cost(requests: Sequence[int], head: int) -> int:
    """Head movement of first come first served: the arrival order."""
    return head_movement(requests, head)


def optimal_order(requests: Sequence[int], head: int) -> list[int]:
    """An order of least head movement: sweep to the nearer end of the
    request range, then sweep to the other end."""
    if not requests:
        return []
    lo, hi = min(requests), max(requests)
    below = sorted((x for x in requests if x < head), reverse=True)
    above = sorted(x for x in requests if x >= head)
    if head - lo <= hi - head:
        return below + sorted(above)
    return above + below


def offline_optimum(requests: Sequence[int], head: int) -> int:
    """(hi - lo) + min(|head - lo|, |head - hi|), or 0 for no request."""
    if not requests:
        return 0
    lo, hi = min(requests), max(requests)
    return (hi - lo) + min(abs(head - lo), abs(head - hi))


def brute_force_optimum(requests: Sequence[int], head: int) -> int:
    """Least head movement over all n! orders. Use only for small n."""
    return min(head_movement(p, head) for p in permutations(requests))
