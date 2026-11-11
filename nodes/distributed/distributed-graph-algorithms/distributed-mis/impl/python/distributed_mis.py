# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-mis/. The authors are listed in prov/CESMCY.jsonl.

"""Maximal independent set in the synchronous LOCAL model, with rounds counted.

luby_mis_local runs Luby's random-priority algorithm. A phase takes two
rounds: the live nodes exchange fresh random priorities, then the local
minima join and tell their neighbours, which leave. mis_from_coloring turns a
proper k-colouring into an MIS in exactly k rounds, one colour class per round.
coloring_from_mis gives a (Delta + 1)-colouring from an MIS of the product
graph G x K_(Delta + 1), each node simulating its Delta + 1 copies.

Precondition: adj is an undirected simple graph given by adjacency lists.
Cost: Luby takes O(log n) phases with high probability, with O(log n)-bit
messages; mis_from_coloring takes k rounds and one-bit messages.
"""

import random


def is_mis(adj: list[list[int]], member: list[bool]) -> bool:
    """True if member marks an independent set that no node can join."""
    for v, nbrs in enumerate(adj):
        if member[v] and any(member[u] for u in nbrs):
            return False
        if not member[v] and not any(member[u] for u in nbrs):
            return False
    return True


def luby_mis_local(
    adj: list[list[int]], rng: random.Random, stats: list[int] | None = None
) -> tuple[list[bool], int]:
    """Return (membership, rounds). stats, if given, gets the number of live edges at the start of each phase."""
    n = len(adj)
    live = [True] * n
    member = [False] * n
    rounds = 0
    while any(live):
        if stats is not None:
            stats.append(sum(1 for v in range(n) if live[v] for u in adj[v] if live[u] and u > v))
        # round 1: every live node sends a fresh random priority to its neighbours
        prio = {v: (rng.random(), v) for v in range(n) if live[v]}
        rounds += 1
        # round 2: local minima join and tell their neighbours
        joiners = [v for v in prio if all(prio[v] < prio[u] for u in adj[v] if live[u])]
        rounds += 1
        for v in joiners:
            member[v] = True
        for v in joiners:
            live[v] = False
            for u in adj[v]:
                live[u] = False
    return member, rounds


def mis_from_coloring(adj: list[list[int]], col: list[int], k: int) -> tuple[list[bool], int]:
    """Given a proper colouring with colours in [0, k), return (MIS, k rounds)."""
    n = len(adj)
    member = [False] * n
    for x in range(k):
        # one round: nodes of colour x with no neighbour in the set join, and announce it
        joining = [v for v in range(n) if col[v] == x and not any(member[u] for u in adj[v])]
        for v in joining:
            member[v] = True
    return member, k


def product_graph(adj: list[list[int]], delta: int) -> list[list[int]]:
    """The graph G x K_(delta + 1): node v * (delta + 1) + i is the copy (v, i)."""
    k = delta + 1
    out: list[list[int]] = [[] for _ in range(len(adj) * k)]
    for v, nbrs in enumerate(adj):
        for i in range(k):
            a = v * k + i
            out[a].extend(v * k + j for j in range(k) if j != i)
            out[a].extend(u * k + i for u in nbrs)
    return out


def coloring_from_mis(adj: list[list[int]], delta: int, rng: random.Random) -> tuple[list[int], int]:
    """Return a (delta + 1)-colouring of G and the rounds, by Luby on G x K_(delta + 1)."""
    k = delta + 1
    member, rounds = luby_mis_local(product_graph(adj, delta), rng)
    col = [-1] * len(adj)
    for a, inside in enumerate(member):
        if inside:
            col[a // k] = a % k
    return col, rounds
