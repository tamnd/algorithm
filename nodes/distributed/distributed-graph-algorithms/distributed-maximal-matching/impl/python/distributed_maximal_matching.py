# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-maximal-matching/. The authors are listed in prov/YK5M1K.jsonl.

"""Maximal matching in the synchronous LOCAL model, with rounds counted.

The algorithm is Luby's MIS algorithm run on the line graph and simulated on
G. A phase takes three rounds. Round 1: for each live edge, the end with the
smaller identifier draws a fresh random priority and sends it to the other
end. Round 2: every node sends the least priority among its live edges to its
neighbours. Then an edge joins the matching when its priority is the least at
both of its ends, which both ends can now see. Round 3: matched nodes tell
their neighbours, and the edges at matched nodes leave.

Precondition: adj is an undirected simple graph given by adjacency lists.
Cost: O(log m) phases with high probability, by Luby's bound on the line
graph; messages hold one priority of O(log n) bits.
"""

import random


def is_maximal_matching(adj: list[list[int]], mate: list[int]) -> bool:
    """True if mate is a matching (mate[v] = -1 when v is unmatched) and no edge can be added."""
    for v, nbrs in enumerate(adj):
        if mate[v] >= 0 and (mate[v] not in nbrs or mate[mate[v]] != v):
            return False
        if mate[v] < 0 and any(mate[u] < 0 for u in nbrs):
            return False
    return True


def luby_matching_local(
    adj: list[list[int]], rng: random.Random, stats: list[int] | None = None
) -> tuple[list[int], int]:
    """Return (mate, rounds). stats, if given, gets the number of live edges at the start of each phase."""
    n = len(adj)
    mate = [-1] * n
    rounds = 0
    while True:
        live = [(u, v) for u in range(n) if mate[u] < 0 for v in adj[u] if u < v and mate[v] < 0]
        if not live:
            return mate, rounds
        if stats is not None:
            stats.append(len(live))
        # round 1: the smaller end of each live edge draws its priority and sends it
        prio = {e: (rng.random(), e) for e in live}
        rounds += 1
        # round 2: every node sends the least priority of its live edges
        least: dict[int, tuple[float, tuple[int, int]]] = {}
        for e, p in prio.items():
            for x in e:
                if x not in least or p < least[x]:
                    least[x] = p
        rounds += 1
        # an edge joins when it is the least at both ends; round 3: matched nodes announce it
        for (u, v), p in prio.items():
            if least[u] == p and least[v] == p:
                mate[u], mate[v] = v, u
        rounds += 1
