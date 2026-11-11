# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ruling-set/. The authors are listed in prov/GGJNRV.jsonl.

"""Deterministic (alpha, (alpha - 1) B)-ruling sets by bit splitting, in the LOCAL model.

Identifiers are B-bit numbers, B = ceil(log2 N). At level 0 every node is in
the set. At level j = 1, ..., B, the nodes whose identifiers agree above bit
j - 1 form a group; inside each group, a set node whose bit j - 1 is 1 leaves
the set if it has a set node of the same group with bit j - 1 equal to 0
within distance alpha - 1. One level costs alpha - 1 rounds in G (one round
on the power graph G^(alpha - 1)).

Precondition: adj is an undirected simple graph; ids are distinct integers in
[0, N); alpha >= 2.
Cost: exactly (alpha - 1) * B rounds. The result has its nodes pairwise at
distance >= alpha, and every node within distance (alpha - 1) * B of it.
"""

from collections import deque


def distances_from(adj: list[list[int]], sources: list[int], limit: int | None = None) -> list[int]:
    """Multi-source BFS distances (-1 when unreachable or beyond limit)."""
    dist = [-1] * len(adj)
    q = deque(sources)
    for s in sources:
        dist[s] = 0
    while q:
        v = q.popleft()
        if limit is not None and dist[v] == limit:
            continue
        for u in adj[v]:
            if dist[u] < 0:
                dist[u] = dist[v] + 1
                q.append(u)
    return dist


def ball(adj: list[list[int]], v: int, r: int) -> list[int]:
    dist = distances_from(adj, [v], r)
    return [u for u, d in enumerate(dist) if d >= 0]


def bit_splitting_ruling_set(adj: list[list[int]], ids: list[int], N: int, alpha: int = 2) -> tuple[set[int], int]:
    """Return (ruling set, rounds)."""
    n = len(adj)
    B = max(1, (N - 1).bit_length())
    near = [[u for u in ball(adj, v, alpha - 1) if u != v] for v in range(n)]  # neighbours in G^(alpha-1)
    in_set = [True] * n
    rounds = 0
    for j in range(1, B + 1):
        leave = []
        for v in range(n):
            if in_set[v] and (ids[v] >> (j - 1)) & 1:
                group = ids[v] >> j
                if any(in_set[u] and ids[u] >> j == group and not (ids[u] >> (j - 1)) & 1 for u in near[v]):
                    leave.append(v)
        for v in leave:
            in_set[v] = False
        rounds += alpha - 1
    return {v for v in range(n) if in_set[v]}, rounds


def ruling_parameters(adj: list[list[int]], rset: set[int]) -> tuple[int, int]:
    """Return (least distance between two set nodes, or a large value; greatest distance of a node from the set)."""
    n = len(adj)
    least = n + 1
    for r in rset:
        dist = distances_from(adj, [r])
        for s in rset:
            if s != r and dist[s] >= 0:
                least = min(least, dist[s])
    dist = distances_from(adj, list(rset))
    greatest = max(dist) if n else 0
    return least, greatest
