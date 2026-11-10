# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jones-plassmann/. The authors are listed in prov/R3VG3J.jsonl.

"""Jones-Plassmann coloring, simulated round by round.

Each vertex gets one random priority, fixed for the whole run. A vertex is
colored in the first round in which all its neighbours of higher priority are
colored; it takes the least color that none of them has.

Precondition: adj is an undirected adjacency list without self-loops.
priority, if given, is a list of distinct numbers, one for each vertex.
Cost: each edge is looked at O(1) times (a count of the uncolored neighbours
of higher priority, decremented when one of them is colored), and each vertex
scans its neighbours once to pick its color, so the work is O(n + m). A round
has O(log n) span, and the number of rounds is the number of vertices on the
longest path of decreasing priority, O(Delta + log n) with high probability.
"""

import math
import random


class Cost:
    """Counters for work, span and rounds."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.rounds = 0


def jones_plassmann(
    adj: list[list[int]],
    rng: random.Random | None = None,
    cost: Cost | None = None,
    priority: list[float] | None = None,
) -> list[int]:
    """Return colors 0, 1, 2, ... with adjacent vertices colored differently."""
    rng = rng if rng is not None else random.Random(0)
    c = cost if cost is not None else Cost()
    n = len(adj)
    if priority is None:
        perm = list(range(n))
        rng.shuffle(perm)
        priority = perm  # @line L1 (distinct random priorities, drawn once)
    color = [-1] * n
    wait = [sum(1 for u in adj[v] if priority[u] > priority[v]) for v in range(n)]  # @line L2
    c.work += n + sum(len(a) for a in adj)
    c.span += max(1, math.ceil(math.log2(n + 1)))
    ready = [v for v in range(n) if wait[v] == 0]  # @line L3
    while ready:  # @line L4
        c.rounds += 1
        for v in ready:  # @line L5 (in parallel: no two ready vertices are adjacent)
            used = {color[u] for u in adj[v] if priority[u] > priority[v]}
            k = 0
            while k in used:
                k += 1
            color[v] = k  # @line L6 (the least color not used by a higher neighbour)
        nxt = []
        for v in ready:  # @line L7
            for u in adj[v]:
                if priority[u] < priority[v]:
                    wait[u] -= 1  # @line L8 (a fetch-and-add)
                    if wait[u] == 0:
                        nxt.append(u)
        c.work += len(ready) + 2 * sum(len(adj[v]) for v in ready)
        c.span += 2 * max(1, math.ceil(math.log2(n + 1)))
        ready = nxt  # @line L9
    return color  # @line L10
