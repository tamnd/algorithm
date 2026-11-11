# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/network-decomposition/. The authors are listed in prov/1Q6NFT.jsonl.

"""Randomized network decomposition in the style of Linial and Saks, and its use for MIS.

linial_saks builds an (O(log n), O(log n)) weak-diameter decomposition in
phases. In each phase every unclustered node u draws a radius r_u with
Pr[r_u >= j] = 2^(-j), cut at B = ceil(3 log2 n). A node v picks the centre u
of largest identifier with dist(u, v) <= r_u, measured in the graph of
unclustered nodes, and joins u's cluster in this phase if dist(u, v) < r_u.
Clusters of one phase are never adjacent, so the phase number is a valid
colour. mis_via_decomposition then processes the colours in turn; a cluster
gathers its nodes and their neighbours and extends the set greedily.

Precondition: adj is an undirected simple graph; ids are distinct.
Cost: each unclustered node is clustered in a phase with probability 1/2
(less only when some radius is cut, which has probability at most n^(-3) per
draw), so O(log n) phases w.h.p.; each phase takes B rounds, and the cluster
weak diameter is at most 2(B - 1).
"""

import random
from collections import deque


def bfs(adj: list[list[int]], alive: list[bool], s: int, limit: int) -> dict[int, int]:
    """Distances from s up to limit, in the graph induced by alive nodes."""
    dist = {s: 0}
    q = deque([s])
    while q:
        v = q.popleft()
        if dist[v] == limit:
            continue
        for u in adj[v]:
            if alive[u] and u not in dist:
                dist[u] = dist[v] + 1
                q.append(u)
    return dist


def draw_radius(rng: random.Random, B: int) -> int:
    r = 0
    while r < B and rng.random() < 0.5:
        r += 1
    return r


def linial_saks(
    adj: list[list[int]], ids: list[int], rng: random.Random, stats: list[tuple[int, int]] | None = None
) -> tuple[list[int], list[int], int, int]:
    """Return (centre of each node's cluster, colour of each node, phases, rounds)."""
    n = len(adj)
    B = max(1, 3 * max(1, (n - 1).bit_length()))
    alive = [True] * n  # @line L1
    centre = [-1] * n
    colour = [-1] * n
    phase = rounds = 0
    while any(alive):  # @line L2
        r = {u: draw_radius(rng, B) for u in range(n) if alive[u]}  # @line L3
        best: dict[int, tuple[int, int]] = {}  # v -> (id of chosen centre, distance)
        for u in r:  # @line L4
            for v, d in bfs(adj, alive, u, r[u]).items():
                if v not in best or ids[u] > ids[centre_of(best[v])]:
                    best[v] = (u, d)
        rounds += B
        joined = [v for v, (u, d) in best.items() if d < r[u]]  # @line L5
        for v in joined:  # @line L6
            centre[v] = best[v][0]
            colour[v] = phase
        for v in joined:  # @line L7
            alive[v] = False
        if stats is not None:
            stats.append((len(r), len(joined)))
        phase += 1  # @line L8
    return centre, colour, phase, rounds  # @line L9


def centre_of(entry: tuple[int, int]) -> int:
    return entry[0]


def check_decomposition(adj: list[list[int]], centre: list[int], colour: list[int]) -> int:
    """Assert that same-colour clusters are not adjacent; return the largest weak diameter."""
    n = len(adj)
    for v in range(n):
        for u in adj[v]:
            if colour[u] == colour[v]:
                assert centre[u] == centre[v], "two clusters of one colour are adjacent"
    clusters: dict[int, list[int]] = {}
    for v in range(n):
        clusters.setdefault(centre[v], []).append(v)
    alive = [True] * n
    worst = 0
    for members in clusters.values():
        for a in members:
            dist = bfs(adj, alive, a, n)
            worst = max(worst, max(dist[b] for b in members))
    return worst


def mis_via_decomposition(adj: list[list[int]], centre: list[int], colour: list[int], diameter: int) -> tuple[list[bool], int]:
    """MIS by processing colour classes; each costs diameter + 2 rounds (gather, decide, announce)."""
    n = len(adj)
    member = [False] * n
    colours = max(colour, default=-1) + 1
    for c in range(colours):
        for v in sorted(range(n), key=lambda x: (centre[x], x)):
            if colour[v] == c and not any(member[u] for u in adj[v]):
                member[v] = True
    return member, colours * (diameter + 2)
