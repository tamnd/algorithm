# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/luby-mis/. The authors are listed in prov/HV73GG.jsonl.

"""Luby's maximal independent set algorithm (random priority form), simulated round by round.

Each round reads the live graph from before the round and then removes the
new members and their neighbours, as one synchronous parallel step.

Precondition: adj is an undirected adjacency list without self-loops, with
adj[v] the neighbours of v (each edge listed at both ends).
Cost: a round with n' live vertices and m' live edges does O(n' + m') work and
has O(log n) span (a minimum over each neighbourhood and a pack). The expected
number of live edges halves in each round, so the expected work is O(n + m)
and the number of rounds is O(log n) with high probability.
"""

import math
import random


class Cost:
    """Counters for work, span, rounds and the live edges at the start of each round."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.rounds = 0
        self.edges: list[int] = []


def luby_mis(
    adj: list[list[int]],
    rng: random.Random | None = None,
    cost: Cost | None = None,
    first: list[int] | None = None,
) -> set[int]:
    """Return a maximal independent set of the graph. first, if given, fixes the priorities of round 1."""
    rng = rng if rng is not None else random.Random(0)
    c = cost if cost is not None else Cost()
    n = len(adj)
    I: set[int] = set()  # @line L1
    live = set(range(n))
    while live:  # @line L2
        c.rounds += 1
        m_live = sum(1 for v in live for u in adj[v] if u in live) // 2
        c.edges.append(m_live)
        order = sorted(live)
        if first is not None and c.rounds == 1:
            r = {v: first[v] for v in order}
        else:
            perm = list(range(len(order)))
            rng.shuffle(perm)
            r = {v: perm[i] for i, v in enumerate(order)}  # @line L3 (distinct random priorities)
        join = {v for v in live if all(r[v] < r[u] for u in adj[v] if u in live)}  # @line L4
        I |= join  # @line L5
        removed = {v for v in live if v in join or any(u in join for u in adj[v])}  # @line L6
        live -= removed  # @line L7 (a pack of the live vertices and edges)
        c.work += 2 * (len(order) + 2 * m_live)
        c.span += 2 * max(1, math.ceil(math.log2(len(order) + 1))) + 2
    return I  # @line L8
