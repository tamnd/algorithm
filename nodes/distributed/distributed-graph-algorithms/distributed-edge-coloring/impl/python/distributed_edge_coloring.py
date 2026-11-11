# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-edge-coloring/. The authors are listed in prov/2M70EM.jsonl.

"""(2 Delta - 1)-edge colouring by random colour trials, with rounds counted.

This is the random trial algorithm for (Delta' + 1)-vertex colouring, run on
the line graph and simulated on G. In each trial, every uncoloured edge
becomes active with probability 1/2. An active edge picks a colour uniformly
from its palette, the colours 0 to 2 Delta - 2 that no coloured adjacent edge
has. It keeps the colour if no adjacent active edge picked the same colour.
One trial takes two rounds of G: the end with the smaller identifier picks
and sends the colour to the other end, and then each end tells the other
whether the colour clashes at its side.

Precondition: adj is an undirected simple graph given by adjacency lists.
Cost: an uncoloured edge is coloured in a trial with probability at least
1/4, so O(log m) trials suffice with high probability. Messages hold one
colour, O(log Delta) bits, so the algorithm also runs in CONGEST.
"""

import random

Edge = tuple[int, int]


def edges_of(adj: list[list[int]]) -> list[Edge]:
    """The edges (u, v) with u < v."""
    return [(u, v) for u in range(len(adj)) for v in adj[u] if u < v]


def is_proper_edge_coloring(adj: list[list[int]], colour: dict[Edge, int]) -> bool:
    """True if every edge has a colour and the edges at each node have distinct colours."""
    if set(colour) != set(edges_of(adj)):
        return False
    for v, nbrs in enumerate(adj):
        seen = [colour[(min(u, v), max(u, v))] for u in nbrs]
        if len(seen) != len(set(seen)):
            return False
    return True


def random_trial_edge_coloring(
    adj: list[list[int]], rng: random.Random, stats: list[int] | None = None
) -> tuple[dict[Edge, int], int]:
    """Return (colour, rounds). stats, if given, gets the number of uncoloured edges before each trial."""
    delta = max((len(a) for a in adj), default=0)
    k = max(2 * delta - 1, 1)
    colour: dict[Edge, int] = {}
    used: list[set[int]] = [set() for _ in adj]  # colours of coloured edges at each node
    left = edges_of(adj)
    rounds = 0
    while left:
        if stats is not None:
            stats.append(len(left))
        # round 1: the smaller end of each active edge picks a colour from its palette and sends it
        trial: dict[Edge, int] = {}
        for u, v in left:
            if rng.random() < 0.5:
                palette = [c for c in range(k) if c not in used[u] and c not in used[v]]
                trial[(u, v)] = rng.choice(palette)
        rounds += 1
        # round 2: each end reports whether the colour clashes with another trial at that end
        count: dict[tuple[int, int], int] = {}
        for (u, v), c in trial.items():
            count[(u, c)] = count.get((u, c), 0) + 1
            count[(v, c)] = count.get((v, c), 0) + 1
        rounds += 1
        for (u, v), c in trial.items():
            if count[(u, c)] == 1 and count[(v, c)] == 1:
                colour[(u, v)] = c
                used[u].add(c)
                used[v].add(c)
        left = [e for e in left if e not in colour]
    return colour, rounds
