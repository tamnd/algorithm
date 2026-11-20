# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/serial-dictatorship/. The authors are listed in prov/RKCZD9.jsonl.

from typing import Optional, Sequence


def serial_dictatorship(
    prefs: Sequence[Sequence[int]],
    order: Optional[Sequence[int]] = None,
    m: Optional[int] = None,
) -> list[int]:
    """Serial dictatorship: the agents pick in turn their best object that is still free.

    prefs[i] lists the objects acceptable to agent i, best first, without repeats. The
    objects are 0, ..., m - 1; by default m is one more than the largest listed object.
    order is a permutation of the agents 0, ..., n - 1, the first to pick first; by
    default it is 0, 1, ..., n - 1. Returns the object of each agent, or -1 for an agent
    that finds no acceptable object free when its turn comes.
    O(m + n^2) time and O(n + m) space: the k-th agent to pick reads at most k entries
    of its list, because at most k - 1 objects are taken before its turn.
    """
    n = len(prefs)
    if m is None:
        m = 1 + max((o for lst in prefs for o in lst), default=-1)
    if order is None:
        order = range(n)
    if sorted(order) != list(range(n)):
        raise ValueError("order must be a permutation of the agents")
    for lst in prefs:
        if len(set(lst)) != len(lst) or any(not 0 <= o < m for o in lst):
            raise ValueError("a preference list repeats an object or is out of range")
    taken = [False] * m  # @line L1
    match = [-1] * n  # @line L2
    for k in range(n):  # @line L3
        i = order[k]  # @line L4
        for o in prefs[i]:  # @line L5
            if not taken[o]:  # @line L6
                match[i] = o
                taken[o] = True
                break
    return match  # @line L7
