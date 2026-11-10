# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hu-algorithm/. The authors are listed in prov/7VB7QV.jsonl.

import heapq


def levels(succ: list[int | None]) -> list[int]:
    """Return level(j) for each job of an in-forest.

    succ[j] is the only successor of job j, or None when j is a root.
    The level of a root is 1, and level(j) = 1 + level(succ[j]).
    The cost is O(n): each job gets its level once.
    """
    n = len(succ)
    level = [0] * n
    for j in range(n):
        path = []
        v: int | None = j
        while v is not None and level[v] == 0:
            path.append(v)
            v = succ[v]
            if len(path) > n:
                raise ValueError("the successor map has a cycle")
        base = 0 if v is None else level[v]
        for u in reversed(path):
            base += 1
            level[u] = base
    return level


def hu_algorithm(succ: list[int | None], m: int) -> list[int]:
    """Schedule unit jobs of an in-forest on m identical machines by Hu's rule.

    succ[j] is the successor of job j, or None for a root. Each job takes
    one time unit. At each integer time the algorithm starts the available
    jobs of highest level, at most m of them. The result is the list of
    slots: job j runs in [slot[j] - 1, slot[j]). The makespan is the largest
    slot. Precondition: m >= 1 and succ describes an in-forest.
    Cost: O(n log n) time with a binary heap, O(n) extra space.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    n = len(succ)
    level = levels(succ)  # @line L1
    waiting = [0] * n  # @line L2
    for j in range(n):
        s = succ[j]
        if s is not None:
            waiting[s] += 1
    avail = [(-level[j], j) for j in range(n) if waiting[j] == 0]  # @line L3
    heapq.heapify(avail)
    slot = [0] * n
    t = 0  # @line L4
    while avail:  # @line L5
        t += 1  # @line L6
        batch = [heapq.heappop(avail)[1] for _ in range(min(m, len(avail)))]  # @line L7
        for j in batch:  # @line L8
            slot[j] = t
        for j in batch:  # @line L9
            s = succ[j]
            if s is not None:
                waiting[s] -= 1
                if waiting[s] == 0:
                    heapq.heappush(avail, (-level[s], s))
    return slot  # @line L10


def hu_lower_bound(succ: list[int | None], m: int) -> int:
    """Return max over h of (h - 1 + ceil(N(h) / m)), where N(h) counts jobs of level >= h."""
    level = levels(succ)
    if not level:
        return 0
    top = max(level)
    count = [0] * (top + 2)
    for v in level:
        count[v] += 1
    best, above = 0, 0
    for h in range(top, 0, -1):
        above += count[h]
        best = max(best, h - 1 + -(-above // m))
    return best
